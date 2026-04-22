<template>
  <aside class="layer-panel glass-panel" role="complementary" :aria-label="t('layers.title')">
    <p class="layer-panel__title">{{ t('layers.title') }}</p>

    <ul class="layer-panel__list">
      <li v-for="layer in layers" :key="layer.id">
        <button
          class="layer-btn"
          :class="{ 'layer-btn--active': layersStore.isActive(layer.id) }"
          @click="layersStore.toggle(layer.id)"
          :aria-pressed="layersStore.isActive(layer.id)"
          :title="t(`layers.${layer.id}`)"
        >
          <span class="layer-btn__icon" v-html="layer.icon" aria-hidden="true"></span>
          <span class="layer-btn__label">{{ t(`layers.${layer.id}`) }}</span>
          <span class="layer-btn__indicator" aria-hidden="true"></span>
        </button>
      </li>
    </ul>
  </aside>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useLayersStore } from '@/stores/layers.js'

const { t } = useI18n()
const layersStore = useLayersStore()

const layers = [
  {
    id: 'news',
    icon: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <rect x="2" y="3" width="12" height="2" rx="1" fill="currentColor"/>
      <rect x="2" y="7" width="8" height="2" rx="1" fill="currentColor"/>
      <rect x="2" y="11" width="10" height="2" rx="1" fill="currentColor"/>
    </svg>`,
  },
  {
    id: 'flights',
    icon: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <path d="M13.5 6.5L8 4 2.5 9.5l1.5.5 1-2 2 1-1.5 3.5 1.5.5 2-3.5 3 1-.5-2.5 1 .5.5-2z" fill="currentColor"/>
    </svg>`,
  },
  {
    id: 'earthquakes',
    icon: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <path d="M1 8h2l2-4 3 7 2-5 2 3 1-1h2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>`,
  },
  {
    id: 'fires',
    icon: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <path d="M8 14c2.5 0 5-2 5-5 0-2-1.5-3.5-2-4 0 1.5-1 2-1.5 2C10 5 8.5 3 8.5 1.5 7 2.5 5 4.5 5 7c0 .5.1 1 .3 1.5C4.5 8 4 7 4 7c-.5 1-1 2-1 2.5C3 12 5.5 14 8 14z" fill="currentColor"/>
    </svg>`,
  },
  {
    id: 'weather',
    icon: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <circle cx="10" cy="6" r="3" stroke="currentColor" stroke-width="1.5"/>
      <path d="M3 11h10M5 13h6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
      <path d="M10 3V1.5M13.5 4.5l1-1M15 7h-1.5M7 4.5l-1-1" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
    </svg>`,
  },
]
</script>

<style scoped>
.layer-panel {
  position: fixed;
  left: var(--space-6);
  top: 50%;
  transform: translateY(-50%);
  z-index: var(--z-panel);
  padding: var(--space-4) var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  min-width: 140px;
}

.layer-panel__title {
  font-family: var(--font-mono);
  font-size: 9px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--text-muted);
  padding: 0 var(--space-2);
}

.layer-panel__list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.layer-btn {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--space-3);
  width: 100%;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  border: 1px solid transparent;
  transition:
    color var(--transition-fast),
    background var(--transition-fast),
    border-color var(--transition-fast);
}

.layer-btn:hover {
  color: var(--text-primary);
  background: var(--glass-hover);
  border-color: var(--border);
}

.layer-btn--active {
  color: var(--gold);
  background: var(--gold-soft);
  border-color: var(--gold-dim);
}

.layer-btn--active .layer-btn__indicator {
  background: var(--gold);
  box-shadow: 0 0 6px var(--gold);
}

.layer-btn__icon {
  display: flex;
  align-items: center;
  flex-shrink: 0;
  width: 16px;
}

.layer-btn__label {
  font-size: 12px;
  font-weight: 400;
  letter-spacing: 0.03em;
  flex: 1;
  text-align: left;
}

.layer-btn__indicator {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--text-muted);
  flex-shrink: 0;
  transition: background var(--transition-fast), box-shadow var(--transition-fast);
}
</style>
