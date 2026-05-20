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

  function selectPin(pin) { selected.value = pin }
  function clearPin()     { selected.value = null }

  return { pins, selected, loading, loadedOnce, error, fetchWeather, selectPin, clearPin }
})
