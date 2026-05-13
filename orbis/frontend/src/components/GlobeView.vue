<template>
  <div ref="containerRef" class="globe-wrap">
    <Transition name="fade">
      <div v-if="layersStore.activeCount === 0" class="globe-hint">
        <p class="globe-hint__text">{{ t('globe.hint') }}</p>
      </div>
    </Transition>

    <!-- Cluster picker — shown when user clicks a stacked cylinder -->
    <Transition name="cluster-fade">
      <div v-if="clusterPins" class="cluster-panel" role="dialog" :aria-label="t('cluster.aria')">
        <div class="cluster-panel__header">
          <span class="cluster-panel__label">{{ clusterPins.length }} {{ t('cluster.articles') }}</span>
          <button class="cluster-panel__close" @click="clusterPins = null" :aria-label="t('sidebar.close')">×</button>
        </div>
        <ul class="cluster-panel__list">
          <li
            v-for="pin in clusterPins"
            :key="pin.id"
            class="cluster-panel__item"
            @click="selectFromCluster(pin)"
          >
            <span class="cluster-panel__dot" :style="{ background: sentimentColor(pin.sentiment) }"></span>
            <span class="cluster-panel__text">{{ pin.title }}</span>
          </li>
        </ul>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useGlobe, SENTIMENT_COLORS } from '@/composables/useGlobe.js'
import { useNewsStore } from '@/stores/news.js'
import { useLayersStore } from '@/stores/layers.js'

const { t } = useI18n()
const containerRef = ref(null)
const { init, updatePoints, flyTo, resize, destroy } = useGlobe()
const newsStore   = useNewsStore()
const layersStore = useLayersStore()

const clusterPins = ref(null)

function sentimentColor(sentiment) {
  return SENTIMENT_COLORS[sentiment] ?? SENTIMENT_COLORS.neutral
}

// Pins within this many degrees (lat AND lon) collapse into a cluster cylinder.
// 1.2° ≈ 130 km — matches the pipeline's jitter range so only genuinely
// overlapping articles (not just same-country jitter) get merged.
const CLUSTER_THRESHOLD = 1.2

function clusterPoints(pins, selectedPin = null) {
  const clusters   = []
  const used       = new Set()
  const selectedId = selectedPin?.id ?? null

  for (let i = 0; i < pins.length; i++) {
    if (used.has(i)) continue
    if (pins[i].id === selectedId) continue   // selected pin always renders individually

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

  // Always add selected pin back individually (outside any cluster)
  if (selectedId) {
    const sel = pins.find(p => p.id === selectedId)
    if (sel) clusters.push(sel)
  }

  return clusters
}

function handlePinClick(pin) {
  if (pin._cluster) {
    clusterPins.value = pin._pins
  } else {
    clusterPins.value = null
    newsStore.selectPin(pin)
  }
}

function selectFromCluster(pin) {
  clusterPins.value = null
  newsStore.selectPin(pin)
}

onMounted(async () => {
  await init(containerRef.value, {
    onPinClick: handlePinClick,
    onPinHover: () => {},
  })
  refreshPoints()
})

function refreshPoints() {
  const showPins  = layersStore.isActive('news')
  const rawPins   = showPins ? newsStore.filteredPins : []
  const clustered = clusterPoints(rawPins, newsStore.selectedPin)
  updatePoints(clustered, newsStore.selectedPin)
}

watch(() => layersStore.isActive('news'), refreshPoints)
watch(() => newsStore.filteredPins, refreshPoints, { deep: true })
watch(() => newsStore.selectedPin, (pin) => {
  if (pin) flyTo(pin.lat, pin.lon, 1.8, 900)
  refreshPoints()
})

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

/* ── Cluster panel ── */
.cluster-panel {
  position: fixed;
  top: calc(var(--nav-height) + var(--subnav-height) + var(--space-6));
  left: 50%;
  transform: translateX(-50%);
  width: min(360px, 90vw);
  max-height: 320px;
  background: rgba(11, 11, 13, 0.94);
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  z-index: var(--z-panel);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.50);
}

.cluster-panel__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) var(--space-5);
  border-bottom: 1px solid var(--line);
  flex-shrink: 0;
}

.cluster-panel__label {
  font-family: var(--font-display);
  font-size: 8px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--ink-mute);
}

.cluster-panel__close {
  background: none;
  border: none;
  color: var(--ink-mute);
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  padding: 0 var(--space-1);
  transition: color var(--t-fast);
}
.cluster-panel__close:hover { color: var(--ink); }

.cluster-panel__list {
  overflow-y: auto;
  list-style: none;
  margin: 0;
  padding: var(--space-2) 0;
}

.cluster-panel__item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-5);
  cursor: pointer;
  transition: background var(--t-fast);
}
.cluster-panel__item:hover { background: rgba(255, 255, 255, 0.06); }

.cluster-panel__dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  margin-top: 4px;
  flex-shrink: 0;
}

.cluster-panel__text {
  font-size: 11px;
  line-height: 1.55;
  color: var(--ink);
}

/* ── Transitions ── */
.fade-enter-active, .fade-leave-active {
  transition: opacity var(--t-base), transform var(--t-base);
}
.fade-enter-from, .fade-leave-to {
  opacity: 0; transform: translateX(-50%) translateY(6px);
}

.cluster-fade-enter-active, .cluster-fade-leave-active {
  transition: opacity var(--t-base), transform var(--t-base);
}
.cluster-fade-enter-from, .cluster-fade-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-8px);
}
</style>
