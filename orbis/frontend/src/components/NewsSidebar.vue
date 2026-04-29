<template>
  <Transition name="slide-right">
    <aside
      v-if="newsStore.selectedPin"
      class="sidebar"
      role="complementary"
      :aria-label="t('sidebar.aria')"
    >
      <header class="sidebar__head">
        <span class="sidebar__sentiment" :class="`sent--${newsStore.selectedPin.sentiment}`">
          <span class="sidebar__sentiment-dot" aria-hidden="true"></span>
          {{ t(`sidebar.sentiment.${newsStore.selectedPin.sentiment}`) }}
        </span>
        <button class="sidebar__close" @click="newsStore.clearPin()" :aria-label="t('sidebar.close')">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M2 2l10 10M12 2L2 12" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
          </svg>
        </button>
      </header>

      <div class="sidebar__meta numeric">
        <span>{{ newsStore.selectedPin.city }}, {{ newsStore.selectedPin.country }}</span>
        <span class="sidebar__dot" aria-hidden="true"></span>
        <time>{{ formatTime(newsStore.selectedPin.timestamp) }}</time>
      </div>

      <h2 class="sidebar__headline">{{ newsStore.selectedPin.title }}</h2>

      <span class="sidebar__category">{{ t(`filter.${newsStore.selectedPin.category}`) }}</span>

      <section class="sidebar__section">
        <p class="eyebrow">{{ t('sidebar.aiSummary') }}</p>
        <ul class="sidebar__summary">
          <li v-for="(s, i) in newsStore.selectedPin.summary" :key="i">{{ s }}</li>
        </ul>
      </section>

      <a class="sidebar__link" :href="newsStore.selectedPin.url" target="_blank" rel="noopener noreferrer">
        <span>{{ t('sidebar.readArticle') }}</span>
        <span class="sidebar__arrow" aria-hidden="true">→</span>
      </a>
    </aside>
  </Transition>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useNewsStore } from '@/stores/news.js'

const { t, locale } = useI18n()
const newsStore = useNewsStore()

function formatTime(ts) {
  const d = new Date(ts)
  const diffMin = Math.floor((Date.now() - d) / 60000)
  const diffHr = Math.floor(diffMin / 60)
  if (diffMin < 1) return t('sidebar.justNow')
  if (diffMin < 60) return t('sidebar.minutesAgo', { n: diffMin })
  if (diffHr < 24) return t('sidebar.hoursAgo', { n: diffHr })
  return d.toLocaleDateString(locale.value === 'de' ? 'de-DE' : 'en-US', {
    day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit',
  })
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: var(--sidebar-width);
  z-index: var(--z-sidebar);
  padding: calc(var(--nav-height) + var(--space-6)) var(--space-8) var(--space-8);
  background: var(--canvas);
  border-left: 1px solid var(--line);
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
  overflow-y: auto;
}

.sidebar__head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar__sentiment {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.sidebar__sentiment-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.sent--positive { color: var(--positive); }
.sent--positive .sidebar__sentiment-dot { background: var(--positive); }
.sent--neutral  { color: var(--beige); }
.sent--neutral  .sidebar__sentiment-dot { background: var(--beige); }
.sent--negative { color: var(--negative); }
.sent--negative .sidebar__sentiment-dot { background: var(--negative); }

.sidebar__close {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  color: var(--ink-mute);
  border: 1px solid var(--line);
  transition: color var(--t-fast), border-color var(--t-fast);
}
.sidebar__close:hover {
  color: var(--ink);
  border-color: var(--line-strong);
}

.sidebar__meta {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 11px;
  letter-spacing: 0.04em;
  color: var(--ink-mute);
}

.sidebar__dot {
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: var(--ink-whisper);
}

.sidebar__headline {
  font-size: 28px;
  font-weight: 300;
  line-height: 1.2;
  letter-spacing: -0.02em;
  color: var(--ink);
}

.sidebar__category {
  align-self: flex-start;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--navy);
  padding: 4px 10px;
  border: 1px solid var(--navy-soft);
  background: var(--navy-soft);
  border-radius: var(--radius-pill);
}

.sidebar__section {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  padding-top: var(--space-5);
  border-top: 1px solid var(--line);
}

.sidebar__summary {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.sidebar__summary li {
  position: relative;
  padding-left: var(--space-4);
  font-size: 14px;
  line-height: 1.6;
  color: var(--ink-mute);
}

.sidebar__summary li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 11px;
  width: 6px;
  height: 1px;
  background: var(--ink-whisper);
}

.sidebar__link {
  margin-top: auto;
  display: inline-flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.06em;
  color: var(--canvas);
  background: var(--ink);
  border-radius: var(--radius-pill);
  transition: transform var(--t-fast), background var(--t-fast);
}

.sidebar__link:hover {
  background: var(--beige);
}

.sidebar__link:hover .sidebar__arrow {
  transform: translateX(3px);
}

.sidebar__arrow {
  transition: transform var(--t-fast);
}

.slide-right-enter-active,
.slide-right-leave-active {
  transition: transform var(--t-slow), opacity var(--t-slow);
}
.slide-right-enter-from,
.slide-right-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>
