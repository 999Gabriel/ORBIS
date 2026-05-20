<template>
  <Transition name="slide-right">
    <aside v-if="weatherStore.selected" class="wpanel" role="complementary" aria-label="Weather details">

      <header class="wpanel__head">
        <div class="wpanel__meta">
          <span>{{ weatherStore.selected.city }}</span>
          <span class="wpanel__bull" aria-hidden="true">·</span>
          <span>{{ weatherStore.selected.country }}</span>
        </div>
        <button class="wpanel__close" @click="weatherStore.clearPin()" aria-label="Close">
          <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
            <path d="M1 1l8 8M9 1L1 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </button>
      </header>

      <!-- Temperature — big editorial display -->
      <div class="wpanel__temp-row">
        <img
          class="wpanel__icon"
          :src="`https://openweathermap.org/img/wn/${weatherStore.selected.icon}@2x.png`"
          :alt="weatherStore.selected.condition"
          width="64" height="64"
        />
        <span class="wpanel__temp">{{ Math.round(weatherStore.selected.temp) }}°</span>
      </div>

      <p class="wpanel__condition">{{ capitalize(weatherStore.selected.condition) }}</p>

      <!-- Detail grid -->
      <div class="wpanel__grid">
        <div class="wpanel__cell">
          <span class="wpanel__label">Feels like</span>
          <span class="wpanel__value">{{ Math.round(weatherStore.selected.feels_like) }}°C</span>
        </div>
        <div class="wpanel__cell">
          <span class="wpanel__label">Humidity</span>
          <span class="wpanel__value">{{ weatherStore.selected.humidity }}%</span>
        </div>
        <div class="wpanel__cell">
          <span class="wpanel__label">Wind</span>
          <span class="wpanel__value">{{ Math.round(weatherStore.selected.wind_speed) }} m/s</span>
        </div>
        <div class="wpanel__cell">
          <span class="wpanel__label">Direction</span>
          <span class="wpanel__value">{{ windDir(weatherStore.selected.wind_deg) }}</span>
        </div>
      </div>

      <p class="wpanel__updated">
        Updated {{ formatAge(weatherStore.selected.fetched_at) }}
      </p>

    </aside>
  </Transition>
</template>

<script setup>
import { useWeatherStore } from '@/stores/weather.js'

const weatherStore = useWeatherStore()

function capitalize(s) {
  return s ? s.charAt(0).toUpperCase() + s.slice(1) : ''
}

function windDir(deg) {
  const dirs = ['N','NE','E','SE','S','SW','W','NW']
  return dirs[Math.round((deg ?? 0) / 45) % 8]
}

function formatAge(ts) {
  if (!ts) return ''
  const mins = Math.floor((Date.now() / 1000 - ts) / 60)
  if (mins < 1)  return 'just now'
  if (mins < 60) return `${mins} min ago`
  return `${Math.floor(mins / 60)} h ago`
}
</script>

<style scoped>
.wpanel {
  position: fixed;
  top: 0; right: 0; bottom: 0;
  width: var(--sidebar-width);
  z-index: var(--z-sidebar);
  padding: calc(var(--nav-height) + var(--space-6)) var(--space-8) var(--space-8);
  background: #FFFFFF;
  border-left: 1px solid var(--line);
  display: flex; flex-direction: column; gap: var(--space-5);
  overflow-y: auto;
}

.wpanel__head {
  display: flex; justify-content: space-between; align-items: flex-start;
}

.wpanel__meta {
  display: flex; align-items: center; gap: var(--space-2);
  font-family: var(--font-display);
  font-size: 10px; color: var(--ink-whisper); letter-spacing: 0.04em;
}
.wpanel__bull { opacity: 0.4; }

.wpanel__close {
  width: 28px; height: 28px;
  display: flex; align-items: center; justify-content: center;
  color: var(--ink-whisper);
  border: 1px solid var(--line);
  border-radius: var(--radius-xs);
  flex-shrink: 0;
  transition: color var(--t-fast), border-color var(--t-fast);
}
.wpanel__close:hover { color: var(--ink); border-color: var(--line-strong); }

/* Big temperature + icon */
.wpanel__temp-row {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.wpanel__icon {
  width: 64px; height: 64px;
  flex-shrink: 0;
}

.wpanel__temp {
  font-family: var(--font-pinstripe, var(--font-display));
  font-size: 80px;
  font-weight: 400;
  line-height: 1;
  letter-spacing: -0.02em;
  color: var(--ink);
}

.wpanel__condition {
  font-size: 14px;
  color: var(--ink-mute);
  line-height: 1.4;
  margin-top: calc(var(--space-2) * -1);
}

/* 2×2 detail grid */
.wpanel__grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1px;
  background: var(--line);
  border: 1px solid var(--line);
  border-radius: var(--radius-xs);
  overflow: hidden;
  margin-top: var(--space-2);
}

.wpanel__cell {
  background: #FFFFFF;
  display: flex; flex-direction: column;
  gap: var(--space-1);
  padding: var(--space-4) var(--space-5);
}

.wpanel__label {
  font-family: var(--font-display);
  font-size: 8px; letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--ink-whisper);
}

.wpanel__value {
  font-size: 18px;
  font-weight: 500;
  color: var(--ink);
}

.wpanel__updated {
  margin-top: auto;
  font-family: var(--font-display);
  font-size: 8px; letter-spacing: 0.10em; text-transform: uppercase;
  color: var(--ink-whisper);
}

/* Same slide transition as NewsSidebar */
.slide-right-enter-active, .slide-right-leave-active {
  transition: transform var(--t-slow), opacity var(--t-slow);
}
.slide-right-enter-from, .slide-right-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>
