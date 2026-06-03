<template>
  <nav class="navbar" role="navigation">
    <div class="navbar__left">
      <img class="navbar__logo" src="@/assets/orbis-logo.png" alt="ORBIS" height="28" />
    </div>

    <div class="navbar__right">
      <button
        class="refresh-btn"
        :class="{ 'refresh-btn--spinning': newsStore.refreshing }"
        @click="newsStore.triggerRefresh()"
        :disabled="newsStore.refreshing"
        :aria-label="newsStore.refreshing ? 'Refreshing…' : 'Refresh news'"
        :title="newsStore.refreshing ? 'Refreshing…' : 'Refresh news'"
      >
        <svg width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true">
          <path d="M11.5 6.5A5 5 0 1 1 9 2.07" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
          <path d="M9 .5v2h2" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>

      <span class="navbar__sep" aria-hidden="true"></span>

      <div class="lang" role="group" aria-label="Language">
        <button class="lang__btn" :class="{ 'lang__btn--active': locale === 'en' }" @click="switchLocale('en')">EN</button>
        <span class="lang__divider" aria-hidden="true">/</span>
        <button class="lang__btn" :class="{ 'lang__btn--active': locale === 'de' }" @click="switchLocale('de')">DE</button>
      </div>
    </div>
  </nav>

  <!-- Layer dock: bottom-left, above timeline -->
  <div class="layer-dock" role="group" :aria-label="t('layers.title')">
    <button
      v-for="layer in layers"
      :key="layer.id"
      class="layer-tile"
      :class="{ 'layer-tile--active': layersStore.isActive(layer.id) }"
      @click="toggleLayer(layer.id)"
      :aria-pressed="layersStore.isActive(layer.id)"
    >
      <!-- Status indicator is a STRUCTURAL swap (v-if), not a colour
           transition — this forces a reflow so the active state always
           paints, even inside the backdrop-filter container. -->
      <span class="layer-tile__status" aria-hidden="true">
        <span v-if="layersStore.isActive(layer.id)" class="layer-tile__dot layer-tile__dot--on"></span>
        <span v-else class="layer-tile__dot layer-tile__dot--off"></span>
      </span>
      <span class="layer-tile__name">{{ t(`layers.${layer.id}`) }}</span>
    </button>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { setLocale } from '@/i18n/index.js'
import { useLayersStore } from '@/stores/layers.js'
import { useNewsStore } from '@/stores/news.js'

const { t, locale } = useI18n()
const layersStore = useLayersStore()
const newsStore = useNewsStore()

const layers = [
  { id: 'news' },
  { id: 'oil' },
  { id: 'weather' },
]

function switchLocale(lang) { setLocale(lang) }
function toggleLayer(id)    { layersStore.toggle(id) }
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: var(--nav-height);
  z-index: var(--z-nav);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-8);
  background: rgba(254, 254, 254, 0.97);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--line);
}

.navbar__logo {
  display: block;
  height: 52px;
  width: auto;
  object-fit: contain;
}

.navbar__right {
  display: flex;
  align-items: center;
  gap: var(--space-5);
}

.navbar__sep {
  width: 1px; height: 14px;
  background: var(--line-strong);
  flex-shrink: 0;
}

.refresh-btn {
  display: flex; align-items: center; justify-content: center;
  width: 28px; height: 28px;
  border-radius: var(--radius-xs);
  color: var(--ink-whisper);
  border: 1px solid var(--line);
  background: transparent;
  transition: color var(--t-fast), border-color var(--t-fast), background var(--t-fast);
}
.refresh-btn:hover:not(:disabled) {
  color: var(--ink-mute);
  border-color: var(--line-strong);
  background: var(--surface);
}
.refresh-btn:disabled { opacity: 0.35; cursor: default; }
.refresh-btn--spinning svg { animation: spin 1s linear infinite; }

.lang { display: inline-flex; align-items: center; gap: var(--space-2); }
.lang__btn {
  font-family: var(--font-display);
  font-size: 9px; letter-spacing: 0.12em;
  color: var(--ink-whisper);
  padding: 2px 0;
  transition: color var(--t-fast);
}
.lang__btn:hover   { color: var(--ink-mute); }
.lang__btn--active { color: var(--ink); }
.lang__divider {
  font-size: 9px; color: var(--line-strong);
  font-family: var(--font-display);
}

/* ── Layer dock — bottom-left ── */
.layer-dock {
  position: fixed;
  bottom: calc(var(--timeline-height) + var(--space-5));
  left: var(--space-8);
  z-index: var(--z-panel);
  display: flex;
  align-items: stretch;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius-xs);
  overflow: hidden;
  background: rgba(254, 254, 254, 0.94);
  backdrop-filter: blur(12px);
}

.layer-tile {
  display: flex; flex-direction: row;
  align-items: center; justify-content: flex-start;
  gap: var(--space-2);
  min-width: 96px;
  height: 50px;
  padding: 0 var(--space-4);
  border-right: 1px solid var(--line);
  white-space: nowrap;
}
.layer-tile:last-child { border-right: none; }
.layer-tile:hover:not(.layer-tile--active) { background: var(--surface-hover); }

/* Active: black tile, white text — clear inversion.
   translateZ promotes the tile to its own compositing layer so the
   opaque fill paints independently of the backdrop-filter parent. */
.layer-tile--active {
  background: #0A0A0B;
  transform: translateZ(0);
}
.layer-tile--active .layer-tile__name { color: #FFFFFF; }

/* ── Status dot — structural on/off indicator ── */
.layer-tile__status {
  display: inline-flex;
  align-items: center; justify-content: center;
  width: 10px; height: 10px;
  flex-shrink: 0;
}
.layer-tile__dot { border-radius: var(--radius-pill); }
.layer-tile__dot--off {
  width: 7px; height: 7px;
  border: 1.5px solid var(--ink-whisper);
}
.layer-tile__dot--on {
  width: 9px; height: 9px;
  background: #FFFFFF;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.18);
}
.layer-tile:hover:not(.layer-tile--active) .layer-tile__dot--off {
  border-color: var(--ink-mute);
}

.layer-tile__name {
  font-family: var(--font-display);
  font-size: 8px; letter-spacing: 0.10em;
  text-transform: uppercase;
  color: var(--ink-mute);
  line-height: 1.2;
}
.layer-tile:hover:not(.layer-tile--active) .layer-tile__name { color: var(--ink); }
</style>
