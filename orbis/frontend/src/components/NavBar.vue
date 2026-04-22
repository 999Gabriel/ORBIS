<template>
  <nav class="navbar glass-panel">
    <!-- Left: wordmark -->
    <div class="navbar__brand">
      <span class="navbar__logo font-serif">ORBIS</span>
      <span class="navbar__live">
        <span class="navbar__live-dot" aria-hidden="true"></span>
        {{ t('nav.live') }}
      </span>
    </div>

    <!-- Center: tagline -->
    <p class="navbar__tagline">{{ t('nav.tagline') }}</p>

    <!-- Right: language switcher -->
    <div class="navbar__actions">
      <div class="lang-switcher" role="group" :aria-label="'Language / Sprache'">
        <button
          class="lang-btn"
          :class="{ 'lang-btn--active': locale === 'en' }"
          @click="switchLocale('en')"
        >EN</button>
        <span class="lang-divider" aria-hidden="true">|</span>
        <button
          class="lang-btn"
          :class="{ 'lang-btn--active': locale === 'de' }"
          @click="switchLocale('de')"
        >DE</button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { setLocale } from '@/i18n/index.js'

const { t, locale } = useI18n()

function switchLocale(lang) {
  setLocale(lang)
}
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: var(--nav-height);
  z-index: var(--z-nav);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-6);
  border-radius: 0;
  border-left: none;
  border-right: none;
  border-top: none;
}

.navbar__brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex: 0 0 auto;
}

.navbar__logo {
  font-size: 22px;
  font-style: italic;
  letter-spacing: 0.06em;
  color: var(--text-primary);
  line-height: 1;
}

.navbar__live {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.12em;
  color: var(--red);
  font-weight: 500;
}

.navbar__live-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--red);
  animation: pulse-live 1.8s ease-in-out infinite;
}

.navbar__tagline {
  font-size: 12px;
  color: var(--text-secondary);
  letter-spacing: 0.04em;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  white-space: nowrap;
}

.navbar__actions {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

/* Language switcher */
.lang-switcher {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.lang-btn {
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 0.1em;
  color: var(--text-secondary);
  padding: 4px 2px;
  border-bottom: 1px solid transparent;
  transition: color var(--transition-fast), border-color var(--transition-fast);
}

.lang-btn:hover {
  color: var(--text-primary);
}

.lang-btn--active {
  color: var(--gold);
  border-bottom-color: var(--gold);
}

.lang-divider {
  color: var(--text-muted);
  font-size: 10px;
  user-select: none;
}
</style>
