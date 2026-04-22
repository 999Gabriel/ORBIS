import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const LAYER_IDS = ['news', 'flights', 'earthquakes', 'fires', 'weather']

export const useLayersStore = defineStore('layers', () => {
  const active = ref(new Set())

  function toggle(id) {
    if (active.value.has(id)) {
      active.value.delete(id)
    } else {
      active.value.add(id)
    }
  }

  function isActive(id) {
    return active.value.has(id)
  }

  function activate(id) {
    active.value.add(id)
  }

  function deactivate(id) {
    active.value.delete(id)
  }

  const activeCount = computed(() => active.value.size)

  return { active, toggle, isActive, activate, deactivate, activeCount }
})
