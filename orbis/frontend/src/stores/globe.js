import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useGlobeStore = defineStore('globe', () => {
  const autoRotate = ref(true)
  const pointOfView = ref({ lat: 20, lng: 10, altitude: 2.2 })

  function setAutoRotate(val) {
    autoRotate.value = val
  }

  function setPointOfView(pov) {
    pointOfView.value = pov
  }

  return { autoRotate, pointOfView, setAutoRotate, setPointOfView }
})
