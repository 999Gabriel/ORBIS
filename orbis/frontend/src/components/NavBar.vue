<template>
  <nav class="navbar" role="navigation">
    <div class="navbar__left">
      <span class="navbar__brand">ORBIS</span>
      <span class="navbar__live numeric">
        <span class="navbar__live-dot" aria-hidden="true"></span>
        {{ t('nav.live') }}
      </span>
    </div>

    <div class="navbar__center" role="group" :aria-label="t('layers.title')">
      <button
        v-for="layer in layers"
        :key="layer.id"
        class="pill"
        :class="{ 'pill--active': layersStore.isActive(layer.id) }"
        @click="layersStore.toggle(layer.id)"
        :aria-pressed="layersStore.isActive(layer.id)"
      >
        <span class="pill__label">{{ t(`layers.${layer.id}`) }}</span>
        <span v-if="layersStore.isActive(layer.id)" class="pill__dot" aria-hidden="true"></span>
      </button>
    </div>

    <div class="navbar__right">
      <div class="lang" role="group" aria-label="Language">
        <button
          class="lang__btn"
          :class="{ 'lang__btn--active': locale === 'en' }"
          @click="switchLocale('en')"
        >EN</button>
        <span class="lang__sep" aria-hidden="true"></span>
        <button
          class="lang__btn"
          :class="{ 'lang__btn--active': locale === 'de' }"
          @click="switchLocale('de')"
        >DE</button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { setLocale } from '@/i18n/index.js'
import { useLayersStore } from '@/stores/layers.js'

const { t, locale } = useI18n()
const layersStore = useLayersStore()

const layers = [
  { id: 'news' },
  { id: 'flights' },
  { id: 'earthquakes' },
  { id: 'fires' },
  { id: 'weather' },
]

function switchLocale(lang) { setLocale(lang) }
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: var(--nav-height);
  z-index: var(--z-nav);
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  padding: 0 var(--space-6);
  background: linear-gradient(to bottom, var(--canvas) 0%, rgba(10,10,11,0.6) 80%, transparent 100%);
}

.navbar__left {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.navbar__brand {
  font-size: 18px;
  font-weight: 500;
  letter-spacing: 0.08em;
  color: var(--ink);
}

.navbar__live {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.16em;
  color: var(--ink-mute);
}

.navbar__live-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--alert);
  animation: pulse-soft 1.8s ease-in-out infinite;
}

.navbar__center {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  padding: 4px;
  background: var(--canvas-soft);
  border: 1px solid var(--line);
  border-radius: var(--radius-pill);
}

.pill {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.04em;
  color: var(--ink-mute);
  border-radius: var(--radius-pill);
  transition: color var(--t-fast), background var(--t-fast);
}

.pill:hover { color: var(--ink); }

.pill--active {
  color: var(--canvas);
  background: var(--ink);
}

.pill__dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--alert);
}

.navbar__right {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.lang {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
}

.lang__btn {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.1em;
  color: var(--ink-whisper);
  padding: 4px 2px;
  transition: color var(--t-fast);
}

.lang__btn:hover { color: var(--ink-mute); }
.lang__btn--active { color: var(--ink); }

.lang__sep {
  width: 1px;
  height: 10px;
  background: var(--line-strong);
}
</style>
