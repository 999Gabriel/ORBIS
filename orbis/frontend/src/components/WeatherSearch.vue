<template>
  <Transition name="weather-search">
    <section v-if="layersStore.isActive('weather')" class="wsearch" aria-label="Weather search">
      <div class="wsearch__head">
        <span class="wsearch__code">05</span>
        <span class="wsearch__label">{{ t('weather.searchLabel') }}</span>
        <span class="wsearch__count">{{ pins.length }}</span>
      </div>

      <label class="wsearch__input-wrap">
        <span class="wsearch__scope">{{ t('weather.searchScope') }}</span>
        <input
          v-model.trim="query"
          class="wsearch__input"
          type="search"
          autocomplete="off"
          spellcheck="false"
          :placeholder="t('weather.searchPlaceholder')"
          @keydown.enter.prevent="selectFirst"
        />
      </label>

      <div v-if="weatherStore.loading" class="wsearch__state">
        {{ t('weather.loading') }}
      </div>
      <div v-else-if="weatherStore.error" class="wsearch__state">
        {{ t('weather.error') }}
      </div>
      <div v-else-if="searchLoading" class="wsearch__state">
        {{ t('weather.searching') }}
      </div>
      <div v-else-if="searchError" class="wsearch__state">
        {{ t('weather.searchError') }}
      </div>
      <div v-else-if="query && !matches.length" class="wsearch__state">
        {{ t('weather.noMatch') }}
      </div>

      <ul v-else class="wsearch__results">
        <li v-for="pin in visibleMatches" :key="pin.city_id">
          <button
            class="wsearch__result"
            :class="{ 'wsearch__result--active': pin.city_id === weatherStore.selected?.city_id }"
            @click="selectPin(pin)"
          >
            <span class="wsearch__place">
              <span>{{ pin.city }}</span>
              <span>{{ countryName(pin.country) }}</span>
            </span>
            <span class="wsearch__weather">
              <span class="wsearch__temp">{{ Math.round(pin.temp) }}°</span>
              <span class="wsearch__condition">{{ capitalize(pin.condition) }}</span>
            </span>
          </button>
        </li>
      </ul>
    </section>
  </Transition>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useLayersStore } from '@/stores/layers.js'
import { useWeatherStore } from '@/stores/weather.js'

const emit = defineEmits(['select'])

const { t, locale } = useI18n()
const layersStore = useLayersStore()
const weatherStore = useWeatherStore()
const query = ref('')
const remoteResults = ref([])
const searchLoading = ref(false)
const searchError = ref(null)
let searchToken = 0

const pins = computed(() => weatherStore.pins)

const displayNames = computed(() => {
  try {
    return new Intl.DisplayNames([locale.value], { type: 'region' })
  } catch {
    return null
  }
})

const matches = computed(() => {
  const q = normalize(query.value)
  if (!q) return pins.value.slice().sort(sortByCity)

  const localMatches = pins.value
    .filter(pin => {
      const country = countryName(pin.country)
      return [
        pin.city,
        pin.country,
        country,
        `${pin.city} ${country}`,
      ].some(value => normalize(value).includes(q))
    })
    .sort(sortByCity)

  const localIds = new Set(localMatches.map(pin => pin.city_id))
  const remoteMatches = remoteResults.value
    .filter(pin => !localIds.has(pin.city_id))
    .sort(sortByCity)

  return [...localMatches, ...remoteMatches]
})

const visibleMatches = computed(() => matches.value.slice(0, query.value ? 8 : 4))

function selectFirst() {
  if (visibleMatches.value[0]) selectPin(visibleMatches.value[0])
}

function selectPin(pin) {
  weatherStore.upsertPin(pin)
  weatherStore.selectPin(pin)
  emit('select', pin)
}

watch(query, (value) => {
  const q = value.trim()
  const token = ++searchToken
  searchError.value = null
  remoteResults.value = []
  if (q.length < 2) {
    searchLoading.value = false
    return
  }

  searchLoading.value = true
  window.setTimeout(async () => {
    if (token !== searchToken) return
    try {
      const params = new URLSearchParams({
        q,
        limit: '8',
        language: locale.value.slice(0, 2),
      })
      const res = await fetch(`/api/weather/search?${params}`)
      if (!res.ok) throw new Error(`Weather search ${res.status}`)
      const data = await res.json()
      if (token === searchToken) remoteResults.value = Array.isArray(data) ? data : []
    } catch (error) {
      if (token === searchToken) searchError.value = error
      console.error('[weather-search]', error)
    } finally {
      if (token === searchToken) searchLoading.value = false
    }
  }, 220)
})

function countryName(code) {
  return displayNames.value?.of(code) || code
}

function normalize(value) {
  return String(value || '')
    .toLocaleLowerCase(locale.value)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
}

function sortByCity(a, b) {
  return a.city.localeCompare(b.city, locale.value)
}

function capitalize(value) {
  return value ? value.charAt(0).toUpperCase() + value.slice(1) : ''
}
</script>

<style scoped>
.wsearch {
  position: fixed;
  top: calc(var(--nav-height) + var(--space-6));
  left: var(--space-8);
  z-index: var(--z-panel);
  width: min(340px, calc(100vw - var(--space-8) * 2));
  color: var(--ink);
  background: rgba(254, 254, 254, 0.94);
  border: 1px solid var(--line);
  box-shadow: 0 18px 50px rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(14px);
}

.wsearch__head {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: var(--space-3);
  padding: 12px 14px;
  border-bottom: 1px solid var(--line);
}

.wsearch__code,
.wsearch__label,
.wsearch__count,
.wsearch__scope {
  font-family: var(--font-display);
  text-transform: uppercase;
}

.wsearch__code {
  font-size: 8px;
  letter-spacing: 0.12em;
  color: var(--ink);
}

.wsearch__label {
  font-size: 8px;
  letter-spacing: 0.14em;
  color: var(--ink-whisper);
}

.wsearch__count {
  font-size: 8px;
  letter-spacing: 0.10em;
  color: var(--ink-mute);
}

.wsearch__input-wrap {
  display: grid;
  grid-template-columns: auto 1fr;
  align-items: center;
  gap: var(--space-3);
  padding: 12px 14px;
  border-bottom: 1px solid var(--line);
}

.wsearch__scope {
  font-size: 7px;
  letter-spacing: 0.12em;
  color: var(--ink-whisper);
}

.wsearch__input {
  width: 100%;
  min-width: 0;
  border: 0;
  outline: 0;
  background: transparent;
  font-family: var(--font-display);
  font-size: 10px;
  letter-spacing: 0.08em;
  color: var(--ink);
  text-transform: uppercase;
}

.wsearch__input::placeholder {
  color: var(--ink-whisper);
}

.wsearch__results {
  list-style: none;
  max-height: min(42vh, 360px);
  overflow-y: auto;
}

.wsearch__result {
  width: 100%;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: var(--space-4);
  align-items: center;
  padding: 13px 14px;
  text-align: left;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  transition: background var(--t-fast), color var(--t-fast);
}

.wsearch__result:hover,
.wsearch__result--active {
  background: #0A0A0B;
  color: #FFFFFF;
}

.wsearch__place,
.wsearch__weather {
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.wsearch__place span:first-child {
  font-size: 13px;
  line-height: 1.25;
}

.wsearch__place span:last-child,
.wsearch__condition {
  font-family: var(--font-display);
  font-size: 7px;
  letter-spacing: 0.10em;
  text-transform: uppercase;
  color: var(--ink-whisper);
}

.wsearch__result:hover .wsearch__place span:last-child,
.wsearch__result:hover .wsearch__condition,
.wsearch__result--active .wsearch__place span:last-child,
.wsearch__result--active .wsearch__condition {
  color: rgba(255, 255, 255, 0.52);
}

.wsearch__weather {
  align-items: flex-end;
  text-align: right;
}

.wsearch__temp {
  font-family: var(--font-pinstripe, var(--font-display));
  font-size: 28px;
  line-height: 1;
}

.wsearch__state {
  padding: 18px 14px;
  font-family: var(--font-display);
  font-size: 8px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--ink-whisper);
}

.weather-search-enter-active,
.weather-search-leave-active {
  transition: opacity var(--t-base), transform var(--t-base);
}

.weather-search-enter-from,
.weather-search-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

@media (max-width: 720px) {
  .wsearch {
    top: calc(var(--nav-height) + var(--space-4));
    left: var(--space-4);
    right: var(--space-4);
    width: auto;
  }
}
</style>
