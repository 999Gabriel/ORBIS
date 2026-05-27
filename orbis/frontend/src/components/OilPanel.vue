<template>
  <Transition name="slide-right">
    <aside v-if="oilStore.selected" class="oil-panel" role="complementary">

      <!-- ── Header ── -->
      <header class="oil-panel__head">
        <div class="oil-panel__title-row">
          <span class="oil-panel__layer-code">03</span>
          <h2 class="oil-panel__country">{{ oilStore.selected.name }}</h2>
        </div>
        <button class="oil-panel__close" @click="oilStore.clearCountry()" aria-label="Close">
          <svg width="10" height="10" viewBox="0 0 10 10" fill="none" aria-hidden="true">
            <path d="M1 1l8 8M9 1L1 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </button>
      </header>

      <!-- ── Status / loading ── -->
      <div v-if="oilStore.loading" class="oil-panel__status">{{ t('oil.loading') }}</div>
      <div v-else-if="oilStore.error" class="oil-panel__status oil-panel__status--error">{{ t('oil.error') }}</div>
      <div v-else-if="!hasData" class="oil-panel__status">{{ t('oil.noKey') }}</div>

      <template v-else>
        <!-- ── Price cards ── -->
        <div class="oil-panel__cards">
          <div class="oil-panel__card">
            <span class="oil-panel__card-label">{{ t('oil.wti') }}</span>
            <span class="oil-panel__card-price">${{ fmt(oilStore.currentWTI) }}</span>
            <span class="oil-panel__card-unit">{{ t('oil.perBarrel') }}</span>
            <span
              v-if="oilStore.changeWTI !== null"
              class="oil-panel__card-change"
              :class="oilStore.changeWTI >= 0 ? 'change--up' : 'change--down'"
            >
              {{ oilStore.changeWTI >= 0 ? '+' : '' }}{{ oilStore.changeWTI }}
            </span>
          </div>
          <div class="oil-panel__card">
            <span class="oil-panel__card-label">{{ t('oil.brent') }}</span>
            <span class="oil-panel__card-price">${{ fmt(oilStore.currentBrent) }}</span>
            <span class="oil-panel__card-unit">{{ t('oil.perBarrel') }}</span>
            <span
              v-if="oilStore.changeBrent !== null"
              class="oil-panel__card-change"
              :class="oilStore.changeBrent >= 0 ? 'change--up' : 'change--down'"
            >
              {{ oilStore.changeBrent >= 0 ? '+' : '' }}{{ oilStore.changeBrent }}
            </span>
          </div>
        </div>

        <!-- ── Chart ── -->
        <section class="oil-panel__chart-section">
          <p class="oil-panel__chart-label eyebrow">{{ t('oil.chartLabel') }}</p>
          <div class="oil-panel__chart-wrap">
            <Line :data="chartData" :options="chartOptions" />
          </div>
        </section>
      </template>

      <!-- ── Country context ── -->
      <section class="oil-panel__meta">
        <div class="oil-panel__meta-row">
          <span class="oil-panel__meta-key">{{ t('oil.production') }}</span>
          <span class="oil-panel__meta-val">{{ oilStore.selected.mb_day }} {{ t('oil.mbDay') }}</span>
        </div>
        <div class="oil-panel__meta-row">
          <span class="oil-panel__meta-key">Grade</span>
          <span class="oil-panel__meta-val">{{ oilStore.selected.grade }}</span>
        </div>
        <div class="oil-panel__meta-row">
          <span class="oil-panel__meta-key">Role</span>
          <span class="oil-panel__meta-val">{{ t(`oil.${oilStore.selected.role}`) }}</span>
        </div>
      </section>

      <p class="oil-panel__source">{{ t('oil.source') }}</p>

    </aside>
  </Transition>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale, LinearScale, PointElement, LineElement,
  Tooltip, Legend, Filler,
} from 'chart.js'
import { useOilStore } from '@/stores/oil.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend, Filler)

const { t } = useI18n()
const oilStore = useOilStore()

const hasData = computed(() =>
  (oilStore.prices.wti?.length > 0) || (oilStore.prices.brent?.length > 0)
)

function fmt(v) {
  if (v == null) return '—'
  return v.toFixed(2)
}

const chartData = computed(() => {
  const wti   = [...(oilStore.prices.wti   ?? [])].reverse()
  const brent = [...(oilStore.prices.brent ?? [])].reverse()
  const labels = wti.map(d => d.date.slice(5))  // MM-DD

  return {
    labels,
    datasets: [
      {
        label: 'WTI',
        data: wti.map(d => d.price),
        borderColor: '#6B89C4',
        backgroundColor: 'rgba(107,137,196,0.07)',
        fill: true,
        tension: 0.3,
        pointRadius: 0,
        pointHoverRadius: 3,
        borderWidth: 1.5,
      },
      {
        label: 'Brent',
        data: brent.map(d => d.price),
        borderColor: '#F3C843',
        backgroundColor: 'rgba(243,200,67,0.05)',
        fill: true,
        tension: 0.3,
        pointRadius: 0,
        pointHoverRadius: 3,
        borderWidth: 1.5,
      },
    ],
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  plugins: {
    legend: {
      position: 'top',
      labels: {
        font: { family: "'DM Sans', sans-serif", size: 10 },
        color: 'rgba(10,10,11,0.58)',
        boxWidth: 8,
        boxHeight: 8,
        padding: 12,
      },
    },
    tooltip: {
      backgroundColor: 'rgba(255,255,255,0.96)',
      titleColor: 'rgba(10,10,11,0.58)',
      bodyColor: '#0A0A0B',
      borderColor: 'rgba(0,0,0,0.08)',
      borderWidth: 1,
      padding: 10,
      callbacks: {
        label: ctx => ` $${ctx.parsed.y.toFixed(2)} / bbl`,
      },
    },
  },
  scales: {
    x: {
      ticks: {
        font: { family: "'DM Sans', sans-serif", size: 8.5 },
        color: 'rgba(10,10,11,0.38)',
        maxTicksLimit: 6,
        maxRotation: 0,
      },
      grid: { display: false },
    },
    y: {
      ticks: {
        font: { family: "'DM Sans', sans-serif", size: 8.5 },
        color: 'rgba(10,10,11,0.38)',
        callback: v => `$${v}`,
      },
      grid: { color: 'rgba(0,0,0,0.04)' },
    },
  },
}
</script>

<style scoped>
.oil-panel {
  position: fixed;
  top: 0; right: 0; bottom: 0;
  width: var(--sidebar-width);
  z-index: var(--z-sidebar);
  padding: calc(var(--nav-height) + var(--space-6)) var(--space-8) var(--space-6);
  background: #FFFFFF;
  border-left: 1px solid var(--line);
  display: flex; flex-direction: column; gap: var(--space-5);
  overflow-y: auto;
}

/* ── Header ── */
.oil-panel__head {
  display: flex; align-items: center; justify-content: space-between;
}
.oil-panel__title-row {
  display: flex; align-items: center; gap: var(--space-3);
}
.oil-panel__layer-code {
  font-family: var(--font-display);
  font-size: 9px; letter-spacing: 0.12em;
  color: #FFFFFF;
  background: #F3C843;
  padding: 2px 6px;
  border-radius: 4px;
}
.oil-panel__country {
  font-family: var(--font-pinstripe);
  font-size: 36px; font-weight: 400;
  line-height: 1; color: var(--ink);
}
.oil-panel__close {
  width: 28px; height: 28px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  border: 1px solid var(--line); border-radius: var(--radius-xs);
  color: var(--ink-whisper);
  transition: color var(--t-fast), border-color var(--t-fast);
}
.oil-panel__close:hover { color: var(--ink); border-color: var(--line-strong); }

/* ── Status ── */
.oil-panel__status {
  font-family: var(--font-display);
  font-size: 9px; letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--ink-whisper);
  padding: var(--space-4) 0;
}
.oil-panel__status--error { color: var(--negative); }

/* ── Price cards ── */
.oil-panel__cards {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}
.oil-panel__card {
  display: flex; flex-direction: column; gap: 2px;
  padding: var(--space-4);
  border: 1px solid var(--line);
  border-radius: var(--radius-xs);
  background: var(--surface);
}
.oil-panel__card-label {
  font-family: var(--font-display);
  font-size: 8px; letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--ink-whisper);
}
.oil-panel__card-price {
  font-family: var(--font-pinstripe);
  font-size: 30px; font-weight: 400; line-height: 1.1;
  color: var(--ink);
}
.oil-panel__card-unit {
  font-family: var(--font-display);
  font-size: 8px; color: var(--ink-whisper);
}
.oil-panel__card-change {
  font-family: var(--font-display);
  font-size: 9px; font-weight: 500; margin-top: var(--space-1);
}
.change--up   { color: var(--positive); }
.change--down { color: var(--negative); }

/* ── Chart ── */
.oil-panel__chart-section {
  border-top: 1px solid var(--line);
  padding-top: var(--space-4);
  display: flex; flex-direction: column; gap: var(--space-3);
}
.oil-panel__chart-label {
  margin: 0;
}
.oil-panel__chart-wrap {
  height: 180px;
  position: relative;
}

/* ── Country meta ── */
.oil-panel__meta {
  border-top: 1px solid var(--line);
  padding-top: var(--space-4);
  display: flex; flex-direction: column; gap: var(--space-2);
}
.oil-panel__meta-row {
  display: flex; justify-content: space-between; align-items: baseline;
}
.oil-panel__meta-key {
  font-family: var(--font-display);
  font-size: 8px; letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--ink-whisper);
}
.oil-panel__meta-val {
  font-size: 11px; color: var(--ink);
}

/* ── Source ── */
.oil-panel__source {
  margin-top: auto;
  font-family: var(--font-display);
  font-size: 7.5px; letter-spacing: 0.10em; text-transform: uppercase;
  color: var(--ink-whisper);
}

.slide-right-enter-active, .slide-right-leave-active {
  transition: transform var(--t-slow), opacity var(--t-slow);
}
.slide-right-enter-from, .slide-right-leave-to { transform: translateX(100%); opacity: 0; }
</style>
