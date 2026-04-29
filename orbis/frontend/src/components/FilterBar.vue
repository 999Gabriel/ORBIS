<template>
  <Transition name="fade-down">
    <div v-if="layersStore.isActive('news')" class="subnav" role="group" :aria-label="t('filter.label')">
      <button
        v-for="cat in categories"
        :key="cat"
        class="subnav__item"
        :class="{ 'subnav__item--active': newsStore.activeFilter === cat }"
        @click="newsStore.setFilter(cat)"
        :aria-pressed="newsStore.activeFilter === cat"
      >
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

const categories = [
  'all', 'politics', 'economy', 'technology', 'climate', 'culture', 'infrastructure',
]
</script>

<style scoped>
.subnav {
  position: fixed;
  top: var(--nav-height);
  left: 50%;
  transform: translateX(-50%);
  height: var(--subnav-height);
  z-index: var(--z-panel);
  display: flex;
  align-items: center;
  gap: var(--space-6);
  padding: 0 var(--space-6);
}

.subnav__item {
  position: relative;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--ink-whisper);
  padding: 6px 0;
  transition: color var(--t-fast);
}

.subnav__item:hover { color: var(--ink-mute); }

.subnav__item--active { color: var(--ink); }
.subnav__item--active::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: -2px;
  transform: translateX(-50%);
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--alert);
}

.fade-down-enter-active,
.fade-down-leave-active {
  transition: opacity var(--t-base), transform var(--t-base);
}
.fade-down-enter-from,
.fade-down-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-6px);
}
</style>
