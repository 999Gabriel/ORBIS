import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const OIL_COUNTRIES = [
  { id: 'US', name: 'United States',  lat: 39.5,  lon: -98.3,  role: 'producer', grade: 'WTI',          mb_day: 12.9 },
  { id: 'SA', name: 'Saudi Arabia',   lat: 23.9,  lon: 45.1,   role: 'producer', grade: 'Arab Light',    mb_day: 10.5 },
  { id: 'RU', name: 'Russia',         lat: 61.5,  lon: 90.0,   role: 'producer', grade: 'Urals',         mb_day: 10.1 },
  { id: 'CA', name: 'Canada',         lat: 56.1,  lon: -106.3, role: 'producer', grade: 'WCS',           mb_day: 5.8  },
  { id: 'IQ', name: 'Iraq',           lat: 33.2,  lon: 43.7,   role: 'producer', grade: 'Basrah Light',  mb_day: 4.5  },
  { id: 'CN', name: 'China',          lat: 35.9,  lon: 104.2,  role: 'both',     grade: 'Daqing',        mb_day: 4.1  },
  { id: 'IR', name: 'Iran',           lat: 32.4,  lon: 53.7,   role: 'producer', grade: 'Iranian Light',  mb_day: 3.6 },
  { id: 'AE', name: 'UAE',            lat: 23.4,  lon: 53.8,   role: 'producer', grade: 'Murban',         mb_day: 3.4 },
  { id: 'BR', name: 'Brazil',         lat: -14.2, lon: -51.9,  role: 'both',     grade: 'Brent',          mb_day: 3.1 },
  { id: 'KW', name: 'Kuwait',         lat: 29.3,  lon: 47.5,   role: 'producer', grade: 'Kuwait Export',  mb_day: 2.8 },
  { id: 'NO', name: 'Norway',         lat: 64.5,  lon: 17.9,   role: 'producer', grade: 'Brent',          mb_day: 1.8 },
  { id: 'NG', name: 'Nigeria',        lat: 9.1,   lon: 8.7,    role: 'producer', grade: 'Bonny Light',    mb_day: 1.8 },
  { id: 'KZ', name: 'Kazakhstan',     lat: 48.0,  lon: 66.9,   role: 'producer', grade: 'CPC Blend',      mb_day: 1.8 },
  { id: 'MX', name: 'Mexico',         lat: 23.6,  lon: -102.5, role: 'producer', grade: 'Maya',           mb_day: 1.7 },
  { id: 'QA', name: 'Qatar',          lat: 25.4,  lon: 51.2,   role: 'producer', grade: 'Qatar Marine',   mb_day: 2.0 },
  { id: 'LY', name: 'Libya',          lat: 26.3,  lon: 17.2,   role: 'producer', grade: 'Es Sider',       mb_day: 1.2 },
  { id: 'VE', name: 'Venezuela',      lat: 6.4,   lon: -66.6,  role: 'producer', grade: 'Merey',          mb_day: 0.8 },
  { id: 'IN', name: 'India',          lat: 20.6,  lon: 78.9,   role: 'consumer', grade: 'Brent',          mb_day: 4.7 },
  { id: 'JP', name: 'Japan',          lat: 36.2,  lon: 138.3,  role: 'consumer', grade: 'Dubai',          mb_day: 3.2 },
  { id: 'DE', name: 'Germany',        lat: 51.2,  lon: 10.5,   role: 'consumer', grade: 'Brent',          mb_day: 2.1 },
]

export const useOilStore = defineStore('oil', () => {
  const prices     = ref({ wti: [], brent: [] })
  const selected   = ref(null)
  const loading    = ref(false)
  const loadedOnce = ref(false)
  const error      = ref(null)

  async function fetchPrices() {
    if (loadedOnce.value) return
    loading.value = true
    error.value   = null
    try {
      const res = await fetch('/api/oil/prices')
      if (!res.ok) throw new Error(`Oil API ${res.status}`)
      prices.value = await res.json()
    } catch (e) {
      error.value = e
      console.error('[oil]', e)
    } finally {
      loadedOnce.value = true
      loading.value    = false
    }
  }

  function selectCountry(c) { selected.value = c }
  function clearCountry()   { selected.value = null }

  const currentWTI = computed(() => prices.value.wti?.[0]?.price ?? null)
  const currentBrent = computed(() => prices.value.brent?.[0]?.price ?? null)

  const changeWTI = computed(() => {
    const d = prices.value.wti
    if (!d || d.length < 2) return null
    return +(d[0].price - d[1].price).toFixed(2)
  })
  const changeBrent = computed(() => {
    const d = prices.value.brent
    if (!d || d.length < 2) return null
    return +(d[0].price - d[1].price).toFixed(2)
  })

  return {
    prices, selected, loading, loadedOnce, error,
    fetchPrices, selectCountry, clearCountry,
    currentWTI, currentBrent, changeWTI, changeBrent,
  }
})
