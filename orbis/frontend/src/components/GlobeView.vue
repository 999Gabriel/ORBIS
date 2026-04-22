<template>
  <div ref="containerRef" class="globe-wrap">
    <!-- Globe hint when no layers active -->
    <Transition name="fade">
      <div v-if="layersStore.activeCount === 0" class="globe-hint">
        <p class="globe-hint__text">{{ t('globe.hint') }}</p>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useGlobe } from '@/composables/useGlobe.js'
import { useNewsStore } from '@/stores/news.js'
import { useLayersStore } from '@/stores/layers.js'

const { t } = useI18n()
const containerRef = ref(null)
const { init, updatePoints, flyTo, resize, isReady } = useGlobe()
const newsStore = useNewsStore()
const layersStore = useLayersStore()

onMounted(async () => {
  await init(containerRef.value, {
    onPinClick: (pin) => newsStore.selectPin(pin),
    onPinHover: () => {},
  })

  // Initial point state
  refreshPoints()
})

function refreshPoints() {
  const showPins = layersStore.isActive('news')
  updatePoints(showPins ? newsStore.filteredPins : [], newsStore.selectedPin)
}

// Sync points when layer toggled
watch(() => layersStore.isActive('news'), refreshPoints)

// Sync points when filter changes
watch(() => newsStore.filteredPins, refreshPoints, { deep: true })

// Fly to pin + re-render selected state
watch(() => newsStore.selectedPin, (pin) => {
  if (pin) flyTo(pin.lat, pin.lon, 1.8, 900)
  refreshPoints()
})

// Window resize
function handleResize() {
  if (containerRef.value) {
    resize(containerRef.value.offsetWidth, containerRef.value.offsetHeight)
  }
}
window.addEventListener('resize', handleResize)
onUnmounted(() => window.removeEventListener('resize', handleResize))
</script>

<style scoped>
.globe-wrap {
  position: absolute;
  inset: 0;
  z-index: var(--z-globe);
  cursor: grab;
  background: var(--bg-void);
}
.globe-wrap:active {
  cursor: grabbing;
}

.globe-hint {
  position: absolute;
  bottom: calc(var(--timeline-height) + var(--space-8));
  left: 50%;
  transform: translateX(-50%);
  pointer-events: none;
  z-index: 1;
}

.globe-hint__text {
  font-size: 12px;
  color: var(--text-secondary);
  letter-spacing: 0.06em;
  font-family: var(--font-mono);
  background: var(--glass);
  border: 1px solid var(--border);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
}

/* fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--transition-slow), transform var(--transition-slow);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(8px);
}
</style>
