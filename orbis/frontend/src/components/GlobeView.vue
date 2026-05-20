<template>
  <div ref="containerRef" class="globe-wrap">
    <Transition name="fade">
      <div v-if="layersStore.activeCount === 0" class="globe-hint">
        <p class="globe-hint__text">{{ t('globe.hint') }}</p>
      </div>
    </Transition>

    <Transition name="fade">
      <div v-if="showWeatherStatus" class="weather-status" role="status" aria-live="polite">
        <span class="weather-status__code">05</span>
        <span class="weather-status__text">{{ weatherStatusText }}</span>
      </div>
    </Transition>

    <WeatherSearch @select="selectWeatherPin" />

    <Teleport to="body">
      <WeatherPanel />
    </Teleport>

    <!-- Teleport escapes the globe's stacking context so the panel
         can appear above NavBar (z-nav=30) at z-sidebar=20. -->
    <Teleport to="body">
      <Transition name="cluster-slide">
        <ClusterGlobeModal
          v-if="activeCluster"
          :cluster="activeCluster"
          @close="closeCluster"
          @select="selectFromCluster"
        />
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { computed, ref, watch, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useGlobe } from '@/composables/useGlobe.js'
import { useNewsStore } from '@/stores/news.js'
import { useLayersStore } from '@/stores/layers.js'
import ClusterGlobeModal from '@/components/ClusterGlobeModal.vue'
import WeatherSearch from '@/components/WeatherSearch.vue'
import WeatherPanel from '@/components/WeatherPanel.vue'
import { useWeatherStore } from '@/stores/weather.js'

const { t } = useI18n()
const containerRef = ref(null)
const { init, updatePoints, updateRings, updateWeather, flyTo, resize, destroy } = useGlobe()
const newsStore    = useNewsStore()
const layersStore  = useLayersStore()
const weatherStore = useWeatherStore()

const activeCluster = ref(null)

const showWeatherStatus = computed(() => {
  if (!layersStore.isActive('weather')) return false
  return weatherStore.loading || weatherStore.error || (weatherStore.loadedOnce && weatherStore.pins.length === 0)
})

const weatherStatusText = computed(() => {
  if (weatherStore.loading) return t('weather.loading')
  if (weatherStore.error) return t('weather.error')
  return t('weather.empty')
})

const CLUSTER_THRESHOLD = 1.2

function clusterPoints(pins, selectedPin = null) {
  const clusters   = []
  const used       = new Set()
  const selectedId = selectedPin?.id ?? null

  for (let i = 0; i < pins.length; i++) {
    if (used.has(i)) continue
    if (pins[i].id === selectedId) continue

    const group = [pins[i]]
    used.add(i)

    for (let j = i + 1; j < pins.length; j++) {
      if (used.has(j)) continue
      if (pins[j].id === selectedId) continue
      if (
        Math.abs(pins[i].lat - pins[j].lat) < CLUSTER_THRESHOLD &&
        Math.abs(pins[i].lon - pins[j].lon) < CLUSTER_THRESHOLD
      ) {
        group.push(pins[j])
        used.add(j)
      }
    }

    if (group.length === 1) {
      clusters.push(group[0])
    } else {
      const lat = group.reduce((s, p) => s + p.lat, 0) / group.length
      const lon = group.reduce((s, p) => s + p.lon, 0) / group.length
      clusters.push({
        _cluster: true,
        _pins:    group,
        _count:   group.length,
        id:       `cluster-${group[0].id}`,
        lat, lon,
        sentiment: 'neutral',
      })
    }
  }

  if (selectedId) {
    const sel = pins.find(p => p.id === selectedId)
    if (sel) clusters.push(sel)
  }

  return clusters
}

function handlePinClick(pin) {
  if (pin._cluster) {
    newsStore.clearPin()
    activeCluster.value = pin
  } else {
    activeCluster.value = null
    newsStore.selectPin(pin)
  }
}

function closeCluster() {
  activeCluster.value = null
}

function selectFromCluster(pin) {
  activeCluster.value = null
  newsStore.selectPin(pin)
}

onMounted(async () => {
  await init(containerRef.value, {
    onPinClick:     handlePinClick,
    onPinHover:     () => {},
    onWeatherClick: (pt) => weatherStore.selectPin(pt),
  })
  refreshPoints()
  await syncWeatherLayer(layersStore.isActive('weather'))
})

function refreshPoints() {
  const showPins  = layersStore.isActive('news')
  const rawPins   = showPins ? newsStore.filteredPins : []
  const clustered = clusterPoints(rawPins, newsStore.selectedPin)
  updatePoints(clustered, newsStore.selectedPin)
  updateRings(clustered.filter(p => !p._cluster))
}

watch(() => layersStore.isActive('news'), (active) => {
  if (!active) {
    newsStore.clearPin()
    activeCluster.value = null
  }
  refreshPoints()
})

async function syncWeatherLayer(active) {
  if (active) {
    if (!weatherStore.pins.length) await weatherStore.fetchWeather()
    updateWeather(weatherStore.pins, weatherStore.selected)
  } else {
    updateWeather([], null)
    weatherStore.clearPin()
  }
}

// Weather layer — fetch on first activation, clear when deactivated
watch(() => layersStore.isActive('weather'), syncWeatherLayer)
watch(() => weatherStore.pins, (pins) => {
  if (layersStore.isActive('weather')) updateWeather(pins, weatherStore.selected)
})
watch(() => weatherStore.selected, (pin) => {
  if (!layersStore.isActive('weather')) return
  updateWeather(weatherStore.pins, pin)
  if (pin) flyTo(pin.lat, pin.lon, 1.35, 900)
})
watch(() => newsStore.filteredPins, (pins) => {
  // Close cluster modal if its pins are no longer visible after filtering
  if (activeCluster.value) {
    const stillVisible = activeCluster.value._pins?.some(p =>
      pins.some(fp => fp.id === p.id)
    )
    if (!stillVisible) activeCluster.value = null
  }
  // Deselect pin if it no longer appears in the filtered set
  if (newsStore.selectedPin && !pins.some(p => p.id === newsStore.selectedPin.id)) {
    newsStore.clearPin()
  }
  refreshPoints()
}, { deep: true })
watch(() => newsStore.selectedPin, (pin) => {
  if (pin) flyTo(pin.lat, pin.lon, 1.8, 900)
  refreshPoints()
})

function selectWeatherPin(pin) {
  weatherStore.selectPin(pin)
}

function handleResize() {
  if (containerRef.value) resize(containerRef.value.offsetWidth, containerRef.value.offsetHeight)
}
window.addEventListener('resize', handleResize)
onUnmounted(() => { window.removeEventListener('resize', handleResize); destroy() })
</script>

<style scoped>
.globe-wrap {
  position: fixed; inset: 0;
  z-index: var(--z-globe);
  cursor: grab;
  background: var(--canvas);
}
.globe-wrap:active { cursor: grabbing; }

/* ── Globe hint ── */
.globe-hint {
  position: absolute;
  bottom: calc(var(--timeline-height) + var(--space-8));
  left: 50%; transform: translateX(-50%);
  pointer-events: none; z-index: 1;
  animation: fade-up 0.4s ease both;
}
.globe-hint__text {
  font-family: var(--font-display);
  font-size: 8px; letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--ink-whisper);
  padding: var(--space-3) var(--space-5);
  border: 1px solid var(--line);
  border-radius: var(--radius-pill);
  white-space: nowrap;
  background: rgba(254, 254, 254, 0.90);
  backdrop-filter: blur(8px);
}

.weather-status {
  position: absolute;
  top: calc(var(--nav-height) + var(--space-6));
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
  display: inline-flex;
  align-items: center;
  gap: var(--space-3);
  padding: 10px 14px;
  pointer-events: none;
  color: var(--ink-mute);
  background:
    linear-gradient(90deg, rgba(254, 254, 254, 0.94), rgba(245, 245, 245, 0.86));
  border: 1px solid var(--line);
  box-shadow: 0 14px 40px rgba(0, 0, 0, 0.05);
  backdrop-filter: blur(12px);
}

.weather-status__code {
  font-family: var(--font-display);
  font-size: 9px;
  letter-spacing: 0.12em;
  color: var(--ink);
}

.weather-status__text {
  font-family: var(--font-display);
  font-size: 8px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--ink-whisper);
  white-space: nowrap;
}

@media (max-width: 720px) {
  .weather-status {
    left: var(--space-4);
    right: var(--space-4);
    transform: none;
    justify-content: center;
  }
}
</style>

<!-- Cluster panel slide-in — non-scoped so Transition classes reach the child component -->
<style>
.cluster-slide-enter-active,
.cluster-slide-leave-active {
  transition: transform 0.30s cubic-bezier(0.4, 0, 0.2, 1),
              opacity  0.30s ease;
}
.cluster-slide-enter-from,
.cluster-slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>
