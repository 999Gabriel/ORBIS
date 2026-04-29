<template>
  <div ref="containerRef" class="globe-wrap">
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
const { init, updatePoints, flyTo, resize } = useGlobe()
const newsStore = useNewsStore()
const layersStore = useLayersStore()

onMounted(async () => {
  await init(containerRef.value, {
    onPinClick: (pin) => newsStore.selectPin(pin),
    onPinHover: () => {},
  })
  refreshPoints()
})

function refreshPoints() {
  const showPins = layersStore.isActive('news')
  updatePoints(showPins ? newsStore.filteredPins : [], newsStore.selectedPin)
}

watch(() => layersStore.isActive('news'), refreshPoints)
watch(() => newsStore.filteredPins, refreshPoints, { deep: true })
watch(() => newsStore.selectedPin, (pin) => {
  if (pin) flyTo(pin.lat, pin.lon, 1.8, 900)
  refreshPoints()
})

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
  position: fixed;
  inset: 0;
  z-index: var(--z-globe);
  cursor: grab;
  background: var(--canvas);
}
.globe-wrap:active { cursor: grabbing; }

.globe-hint {
  position: absolute;
  bottom: calc(var(--timeline-height) + var(--space-8));
  left: 50%;
  transform: translateX(-50%);
  pointer-events: none;
  z-index: 1;
}

.globe-hint__text {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--ink-mute);
  padding: var(--space-3) var(--space-5);
  background: var(--canvas-soft);
  border: 1px solid var(--line);
  border-radius: var(--radius-pill);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--t-slow), transform var(--t-slow);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(8px);
}
</style>
