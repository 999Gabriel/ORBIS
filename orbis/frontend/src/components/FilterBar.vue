<template>
  <Transition name="fade-down">
    <div v-if="layersStore.isActive('news')" class="filterbar" role="group" :aria-label="t('filter.label')">
      <button
        v-for="cat in categories"
        :key="cat"
        class="filter-btn"
        :class="{ 'filter-btn--active': newsStore.activeFilter === cat }"
        @click="setFilter(cat)"
        :aria-pressed="newsStore.activeFilter === cat"
      >
        <span v-if="newsStore.activeFilter === cat" class="filter-btn__dot" aria-hidden="true"></span>
        {{ t(`filter.${cat}`) }}
      </button>
    </div>
  </Transition>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useNewsStore } from '@/stores/news.js'
import { useLayersStore } from '@/stores/layers.js'

const { t } = useI18n()
const newsStore = useNewsStore()
const layersStore = useLayersStore()

const categories = ['all', 'politics', 'economy', 'technology', 'climate', 'culture', 'infrastructure']

function setFilter(category) {
  layersStore.activate('news')
  newsStore.setFilter(category)
}
</script>

<style scoped>
.filterbar {
  position: fixed;
  top: calc(var(--nav-height) + 12px);
  left: 50%; transform: translateX(-50%);
  z-index: var(--z-panel);
  display: flex; align-items: center;
  background: rgba(254, 254, 254, 0.94);
  border: 1px solid var(--line);
  border-radius: var(--radius-sm);
  backdrop-filter: blur(10px);
  padding: 0 var(--space-1);
}

.filter-btn {
  display: inline-flex; align-items: center; gap: 5px;
  font-family: var(--font-display);
  font-size: 8.5px; letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--ink-whisper);
  padding: 9px var(--space-3);
  border-bottom: 1.5px solid transparent;
  transition: color var(--t-fast), border-color var(--t-fast);
  white-space: nowrap;
}
.filter-btn:hover { color: var(--ink-mute); }
.filter-btn--active { color: var(--ink); border-bottom-color: var(--ink); }

.filter-btn__dot {
  display: inline-block; width: 4px; height: 4px;
  border-radius: 50%; background: var(--ink); flex-shrink: 0;
}

.fade-down-enter-active, .fade-down-leave-active {
  transition: opacity var(--t-base), transform var(--t-base);
}
.fade-down-enter-from, .fade-down-leave-to {
  opacity: 0; transform: translateX(-50%) translateY(-6px);
}
</style>
