<template>
  <div class="timeline" role="region" :aria-label="t('timeline.aria')">
    <div class="timeline__inner">
      <span class="eyebrow timeline__label">{{ t('timeline.title') }}</span>

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
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()
const dayOffset = ref(0)

const formattedRange = computed(() => {
  if (dayOffset.value === 0) return t('timeline.live')
  const target = new Date(Date.now() - dayOffset.value * 86400000)
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
  background: linear-gradient(to top, var(--canvas) 0%, rgba(10,10,11,0.6) 70%, transparent 100%);
}

.timeline__inner {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: var(--space-6);
  width: 100%;
  max-width: 880px;
  margin: 0 auto;
}

.timeline__label { white-space: nowrap; }

.timeline__track {
  position: relative;
  height: 16px;
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
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--ink);
  cursor: grab;
  transition: transform var(--t-fast);
}
.timeline__slider::-webkit-slider-thumb:hover { transform: scale(1.3); }
.timeline__slider::-webkit-slider-thumb:active { cursor: grabbing; }

.timeline__slider::-moz-range-thumb {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--ink);
  border: none;
  cursor: grab;
}

.timeline__value {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.08em;
  color: var(--ink);
  white-space: nowrap;
  min-width: 110px;
  text-align: right;
}
</style>
