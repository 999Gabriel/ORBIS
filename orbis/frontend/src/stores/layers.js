import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const LAYER_IDS = ['news', 'flights', 'earthquakes', 'fires', 'weather']

export const useLayersStore = defineStore('layers', () => {
  const active = ref(new Set(['news']))

  function toggle(id) {
    const next = new Set(active.value)
    if (next.has(id)) {
      next.delete(id)
    } else {
      next.add(id)
    }
    active.value = next
  }

  function isActive(id) {
    return active.value.has(id)
  }

  function activate(id) {
    active.value = new Set(active.value).add(id)
  }

  function deactivate(id) {
    const next = new Set(active.value)
    next.delete(id)
    active.value = next
  }

  const activeCount = computed(() => active.value.size)

  return { active, toggle, isActive, activate, deactivate, activeCount }
})
