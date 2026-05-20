import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useWeatherStore = defineStore('weather', () => {
  const pins      = ref([])
  const selected  = ref(null)
  const loading   = ref(false)
  const loadedOnce = ref(false)
  const error     = ref(null)

  async function fetchWeather() {
    loading.value = true
    error.value = null
    try {
      const res = await fetch('/api/weather')
      if (!res.ok) throw new Error(`Weather API ${res.status}`)
      pins.value = await res.json()
    } catch (e) {
      error.value = e
      console.error('[weather]', e)
    } finally {
      loadedOnce.value = true
      loading.value = false
    }
  }

  function upsertPin(pin) {
    const index = pins.value.findIndex(p => p.city_id === pin.city_id)
    if (index >= 0) {
      pins.value[index] = pin
    } else {
      pins.value = [...pins.value, pin]
    }
  }

  function selectPin(pin) { selected.value = pin }
  function clearPin()     { selected.value = null }

  return { pins, selected, loading, loadedOnce, error, fetchWeather, upsertPin, selectPin, clearPin }
})
