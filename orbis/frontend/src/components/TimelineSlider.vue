<template>
  <div class="timeline" role="region" :aria-label="t('timeline.aria')">
    <div class="timeline__inner">
      <span class="timeline__label">{{ t('timeline.title') }}</span>

      <div class="timeline__track">
        <input
          v-model.number="dayOffset"
          type="range"
          min="0"
          max="30"
          step="1"
          class="timeline__slider"
          :aria-label="t('timeline.title')"
        />
      </div>

      <span class="timeline__value numeric">{{ formattedRange }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useNewsStore } from '@/stores/news.js'

const { t, locale } = useI18n()
const newsStore = useNewsStore()

const dayOffset = computed({
  get: () => newsStore.dayOffset,
  set: (v) => newsStore.setDayOffset(v),
})

const formattedRange = computed(() => {
  if (dayOffset.value === 0) return t('timeline.live')
  const target = new Date(Date.now() - dayOffset.value * 86_400_000)
  return target.toLocaleDateString(locale.value === 'de' ? 'de-DE' : 'en-US', {
    day: '2-digit', month: 'short', year: 'numeric',
  })
})
</script>

<style scoped>
.timeline {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: var(--timeline-height);
  z-index: var(--z-panel);
  display: flex;
  align-items: center;
  padding: 0 var(--space-8);
  background: rgba(254, 254, 254, 0.97);
  border-top: 1px solid var(--line);
  backdrop-filter: blur(10px);
}

.timeline__inner {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: var(--space-6);
  width: 100%;
  max-width: 860px;
  margin: 0 auto;
}

.timeline__label {
  font-family: var(--font-display);
  font-size: 8px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--ink-whisper);
  white-space: nowrap;
}

.timeline__track {
  position: relative;
  height: 20px;
  display: flex;
  align-items: center;
}

.timeline__slider {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 1px;
  background: var(--line-strong);
  outline: none;
  cursor: pointer;
}

.timeline__slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--ink);
  border: 2px solid var(--canvas);
  box-shadow: 0 0 0 1px var(--ink);
  cursor: grab;
  transition: transform var(--t-fast);
}
.timeline__slider::-webkit-slider-thumb:hover  { transform: scale(1.3); }
.timeline__slider::-webkit-slider-thumb:active { cursor: grabbing; }

.timeline__slider::-moz-range-thumb {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--ink);
  border: 2px solid var(--canvas);
  cursor: grab;
}

.timeline__value {
  font-family: var(--font-display);
  font-size: 9px;
  letter-spacing: 0.08em;
  color: var(--ink-mute);
  white-space: nowrap;
  min-width: 110px;
  text-align: right;
}
</style>
