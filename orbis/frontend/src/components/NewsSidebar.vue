<template>
  <Transition name="slide-right">
    <aside v-if="newsStore.selectedPin" class="sidebar" role="complementary" :aria-label="t('sidebar.aria')">

      <header class="sidebar__head">
        <div class="sidebar__meta numeric">
          <span>{{ newsStore.selectedPin.city }}, {{ newsStore.selectedPin.country }}</span>
          <span class="sidebar__bull" aria-hidden="true">·</span>
          <time>{{ formatTime(newsStore.selectedPin.timestamp) }}</time>
        </div>
        <button class="sidebar__close" @click="newsStore.clearPin()" :aria-label="t('sidebar.close')">
          <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
            <path d="M1 1l8 8M9 1L1 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </button>
      </header>

      <h2 class="sidebar__headline">{{ newsStore.selectedPin.title }}</h2>

      <div class="sidebar__tags">
        <span class="sidebar__category">{{ t(`filter.${newsStore.selectedPin.category}`) }}</span>
        <span class="sidebar__sentiment" :class="`sent--${newsStore.selectedPin.sentiment}`">
          <span class="sidebar__sentiment-dot" aria-hidden="true"></span>
          {{ t(`sidebar.sentiment.${newsStore.selectedPin.sentiment}`) }}
        </span>
      </div>

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
  top: 0; right: 0; bottom: 0;
  width: var(--sidebar-width);
  z-index: var(--z-sidebar);
  padding: calc(var(--nav-height) + var(--space-6)) var(--space-8) var(--space-8);
  background: #FFFFFF;
  border-left: 1px solid var(--line);
  display: flex; flex-direction: column; gap: var(--space-5);
  overflow-y: auto;
}

.sidebar__head {
  display: flex; justify-content: space-between; align-items: flex-start;
}

.sidebar__meta {
  display: flex; align-items: center; gap: var(--space-2);
  font-size: 10px; color: var(--ink-whisper); letter-spacing: 0.04em;
}
.sidebar__bull { opacity: 0.4; }

.sidebar__close {
  width: 28px; height: 28px;
  display: flex; align-items: center; justify-content: center;
  color: var(--ink-whisper);
  border: 1px solid var(--line);
  border-radius: var(--radius-xs);
  flex-shrink: 0;
  transition: color var(--t-fast), border-color var(--t-fast);
}
.sidebar__close:hover { color: var(--ink); border-color: var(--line-strong); }

/* Alumni Sans Pinstripe — the showstopper. Big, thin, editorial. */
.sidebar__headline {
  font-family: var(--font-pinstripe);
  font-size: 54px; font-weight: 400;
  line-height: 0.95; letter-spacing: 0.01em;
  color: var(--ink); word-break: break-word;
}

.sidebar__tags {
  display: flex; align-items: center; gap: var(--space-4);
}

.sidebar__category {
  font-family: var(--font-display);
  font-size: 8px; letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--ink-whisper);
  padding: 4px 8px;
  border: 1px solid var(--line);
  border-radius: var(--radius-xs);
}

.sidebar__sentiment {
  display: inline-flex; align-items: center; gap: 5px;
  font-family: var(--font-display);
  font-size: 8px; letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--ink-whisper);
}
.sidebar__sentiment-dot {
  width: 5px; height: 5px; border-radius: 50%; flex-shrink: 0;
}
.sent--positive .sidebar__sentiment-dot { background: var(--positive); }
.sent--positive { color: var(--positive); }
.sent--neutral  .sidebar__sentiment-dot { background: var(--ink-whisper); }
.sent--negative .sidebar__sentiment-dot { background: var(--negative); }
.sent--negative { color: var(--negative); }

.sidebar__section {
  display: flex; flex-direction: column; gap: var(--space-3);
  padding-top: var(--space-4);
  border-top: 1px solid var(--line);
}

.sidebar__summary {
  list-style: none; display: flex; flex-direction: column; gap: var(--space-3);
}
.sidebar__summary li {
  position: relative; padding-left: var(--space-5);
  font-size: 13px; line-height: 1.65; color: var(--ink-mute);
}
.sidebar__summary li::before {
  content: '';
  position: absolute; left: 0; top: 11px;
  width: 10px; height: 1px; background: var(--line-strong);
}

/* Plain outlined button — no fill */
.sidebar__link {
  margin-top: auto;
  display: inline-flex; align-items: center; justify-content: space-between;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  font-family: var(--font-display);
  font-size: 9px; letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--ink);
  border: 1px solid var(--line-strong);
  border-radius: var(--radius-xs);
  transition: border-color var(--t-fast), background var(--t-fast);
}
.sidebar__link:hover { border-color: var(--ink); background: var(--surface); }
.sidebar__link:hover .sidebar__arrow { transform: translateX(4px); }
.sidebar__arrow { transition: transform var(--t-fast); font-size: 14px; line-height: 1; }

.slide-right-enter-active, .slide-right-leave-active {
  transition: transform var(--t-slow), opacity var(--t-slow);
}
.slide-right-enter-from, .slide-right-leave-to { transform: translateX(100%); opacity: 0; }
</style>
