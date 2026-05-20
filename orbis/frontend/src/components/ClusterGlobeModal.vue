<template>
  <aside class="cpanel" @click.stop>

    <!-- ── Header ── -->
    <header class="cpanel__head">
      <div class="cpanel__loc">
        <span class="cpanel__count">{{ cluster._count }}</span>
        <div class="cpanel__loc-labels">
          <span class="cpanel__city">{{ location.city }}</span>
          <span v-if="location.city" class="cpanel__sep" aria-hidden="true">·</span>
          <span class="cpanel__country">{{ location.country }}</span>
        </div>
      </div>
      <button class="cpanel__close" @click="$emit('close')" aria-label="Close">
        <svg width="10" height="10" viewBox="0 0 10 10" fill="none" aria-hidden="true">
          <path d="M1 1l8 8M9 1L1 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
      </button>
    </header>

    <!-- ── Mini globe — identical style to main globe, zoomed into cluster ── -->
    <div class="cpanel__globe-wrap">
      <div ref="miniRef" class="cpanel__globe"></div>
    </div>

    <!-- ── Article list ── -->
    <p class="cpanel__hint">Click an article to read it</p>

    <ul class="cpanel__list" role="list">
      <li
        v-for="pin in cluster._pins"
        :key="pin.id"
        class="cpanel__item"
        role="listitem"
        tabindex="0"
        @click="$emit('select', pin)"
        @keydown.enter="$emit('select', pin)"
      >
        <span class="cpanel__dot" :style="{ background: sentColor(pin.sentiment) }" aria-hidden="true"></span>
        <div class="cpanel__text">
          <span class="cpanel__title">{{ pin.title }}</span>
          <span class="cpanel__meta">
            <span v-if="pin.city && pin.city !== 'Unknown'">{{ pin.city }}, </span>{{ pin.country }}
          </span>
        </div>
        <span class="cpanel__arrow" aria-hidden="true">→</span>
      </li>
    </ul>

  </aside>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { createDotEarthTexture } from '@/composables/useGlobe.js'

const props = defineProps({
  cluster: { type: Object, required: true },
})
const emit = defineEmits(['close', 'select'])

const miniRef = ref(null)
let globeInst = null

// ── Sentiment colours ─────────────────────────────────────────────────────────
const SENT = { positive: '#A3D9B1', neutral: '#DFD2BC', negative: '#E8A5A5' }
function sentColor(s) { return SENT[s] ?? SENT.neutral }

// ── Location label ────────────────────────────────────────────────────────────
function mostCommon(arr) {
  const f = {}
  arr.forEach(v => { if (v && v !== 'Unknown') f[v] = (f[v] || 0) + 1 })
  return Object.entries(f).sort((a, b) => b[1] - a[1])[0]?.[0] ?? ''
}
const location = computed(() => ({
  city:    mostCommon(props.cluster._pins.map(p => p.city)),
  country: mostCommon(props.cluster._pins.map(p => p.country)) || 'Region',
}))

// ── Spread pins in a circle so they are visually distinct at close zoom ───────
function spreadPins(pins, centerLat, centerLon) {
  const n = pins.length
  if (n === 1) return [{ ...pins[0], lat: centerLat, lon: centerLon }]
  // Radius scales with count — more pins need more space
  const r = Math.min(1.0 + n * 0.12, 2.2)
  const cosLat = Math.max(0.1, Math.cos(centerLat * Math.PI / 180))
  return pins.map((pin, i) => ({
    ...pin,
    lat: centerLat + r * Math.cos((i / n) * 2 * Math.PI - Math.PI / 2),
    lon: centerLon + (r / cosLat) * Math.sin((i / n) * 2 * Math.PI - Math.PI / 2),
  }))
}

// ── Pin builder — same geometry as main globe ─────────────────────────────────
function createMiniPin(THREE, pin) {
  const height = 12
  const geom = new THREE.CylinderGeometry(0.75, 1.5, height, 8)
  // Align axis with +Z so objectFacesSurface(true) makes pin stand upright
  geom.applyMatrix4(new THREE.Matrix4().makeRotationX(Math.PI / 2))
  geom.translate(0, 0, height / 2)
  const mat = new THREE.MeshPhongMaterial({
    color: '#E85A4F',
    emissive: '#E85A4F',
    emissiveIntensity: 0.38,
    shininess: 55,
  })
  const group = new THREE.Group()
  group.add(new THREE.Mesh(geom, mat))
  return group
}

// ── Mini globe init ───────────────────────────────────────────────────────────
onMounted(async () => {
  const [{ default: Globe }, THREE] = await Promise.all([
    import('globe.gl'),
    import('three'),
  ])

  // Reuse cached dot texture — no extra loading if main globe already built it
  const dotMap = await createDotEarthTexture(THREE)

  const w = miniRef.value.clientWidth  || 400
  const h = miniRef.value.clientHeight || 240

  const spread = spreadPins(
    props.cluster._pins,
    props.cluster.lat,
    props.cluster.lon,
  )

  const globe = new Globe(miniRef.value, { rendererConfig: { antialias: true, alpha: true } })
    // ── Identical globe material to the main globe ──
    .globeMaterial(new THREE.MeshPhongMaterial({
      map: dotMap,
      color: '#FFFFFF',
      emissive: '#000000',
      specular: '#AAAAAA',
      shininess: 8,
      bumpScale: 0,
    }))
    .showGraticules(false)
    .backgroundColor('rgba(0,0,0,0)')
    .atmosphereColor('#CCCCCC')
    .atmosphereAltitude(0.08)
    .width(w)
    .height(h)
    .objectsData(spread)
    .objectLat('lat')
    .objectLng('lon')
    .objectAltitude(0.002)
    .objectFacesSurface(true)
    .objectThreeObject(pin => createMiniPin(THREE, pin))
    .onObjectClick(pin => {
      // Match original pin (not the spread copy) by id
      const original = props.cluster._pins.find(p => p.id === pin.id) ?? pin
      emit('select', original)
    })
    .onObjectHover(pin => {
      if (miniRef.value) miniRef.value.style.cursor = pin ? 'pointer' : 'grab'
    })

  globe.lights([
    new THREE.AmbientLight('#FFFFFF', 0.55),
    new THREE.DirectionalLight('#FFFFFF', 2.20),
    new THREE.DirectionalLight('#E0E0E0', 0.40),
  ])

  globe.controls().autoRotate     = false
  globe.controls().enableDamping  = true
  globe.controls().dampingFactor  = 0.10
  globe.controls().minDistance    = 120
  globe.controls().maxDistance    = 500

  // Zoom directly into the cluster region
  globe.pointOfView({ lat: props.cluster.lat, lng: props.cluster.lon, altitude: 0.40 })

  globeInst = globe
})

onUnmounted(() => {
  globeInst?._destructor?.()
  globeInst = null
})
</script>

<style scoped>
/* ── Panel shell ── */
.cpanel {
  position: fixed;
  top: var(--nav-height);
  right: 0;
  bottom: var(--timeline-height);
  width: var(--sidebar-width);
  z-index: var(--z-sidebar);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(22px);
  -webkit-backdrop-filter: blur(22px);
  border-left: 1px solid var(--line);
  box-shadow: -8px 0 32px rgba(0, 0, 0, 0.10);
}

/* ── Header ── */
.cpanel__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-5) var(--space-6);
  border-bottom: 1px solid var(--line);
  flex-shrink: 0;
  gap: var(--space-4);
}

.cpanel__loc {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  min-width: 0;
}

.cpanel__count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 28px;
  height: 24px;
  padding: 0 var(--space-2);
  background: #E85A4F;
  border-radius: 7px;
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  color: #FFFFFF;
  flex-shrink: 0;
}

.cpanel__loc-labels {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  min-width: 0;
  overflow: hidden;
}

.cpanel__city {
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 500;
  color: var(--ink);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cpanel__sep { color: var(--ink-whisper); font-size: 10px; flex-shrink: 0; }

.cpanel__country {
  font-family: var(--font-display);
  font-size: 11px;
  color: var(--ink-mute);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cpanel__close {
  display: flex; align-items: center; justify-content: center;
  width: 28px; height: 28px; flex-shrink: 0;
  border-radius: var(--radius-xs);
  border: 1px solid var(--line);
  color: var(--ink-whisper);
  transition: color var(--t-fast), border-color var(--t-fast);
}
.cpanel__close:hover { color: var(--ink); border-color: var(--line-strong); }

/* ── Mini globe ── */
.cpanel__globe-wrap {
  width: 100%;
  height: 220px;
  flex-shrink: 0;
  background: var(--canvas);
  border-bottom: 1px solid var(--line);
  overflow: hidden;
}

.cpanel__globe {
  width: 100%;
  height: 100%;
}

/* Make the globe.gl canvas fill the container without distortion */
.cpanel__globe :deep(canvas) {
  width: 100% !important;
  height: 100% !important;
  display: block;
}

/* ── Hint ── */
.cpanel__hint {
  padding: var(--space-2) var(--space-6);
  font-family: var(--font-display);
  font-size: 8px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--ink-whisper);
  border-bottom: 1px solid var(--line);
  flex-shrink: 0;
  margin: 0;
}

/* ── Article list ── */
.cpanel__list {
  flex: 1;
  overflow-y: auto;
  list-style: none;
  padding: 0;
  margin: 0;
}

.cpanel__list::-webkit-scrollbar { width: 3px; }
.cpanel__list::-webkit-scrollbar-track { background: transparent; }
.cpanel__list::-webkit-scrollbar-thumb { background: var(--line-strong); border-radius: 2px; }

/* ── Article item ── */
.cpanel__item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-4);
  padding: var(--space-5) var(--space-6);
  border-bottom: 1px solid var(--line);
  cursor: pointer;
  transition: background var(--t-fast);
}
.cpanel__item:hover { background: rgba(232, 90, 79, 0.04); }
.cpanel__item:focus-visible { outline: 2px solid #E85A4F; outline-offset: -2px; }

.cpanel__dot {
  width: 7px; height: 7px; border-radius: 50%;
  margin-top: 5px; flex-shrink: 0;
}

.cpanel__text {
  flex: 1; min-width: 0;
  display: flex; flex-direction: column; gap: var(--space-1);
}

.cpanel__title {
  font-size: 12px; line-height: 1.55; color: var(--ink);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.cpanel__meta {
  font-family: var(--font-display);
  font-size: 8.5px; letter-spacing: 0.09em;
  color: var(--ink-whisper); text-transform: uppercase;
}

.cpanel__arrow {
  font-size: 14px; color: var(--ink-whisper);
  margin-top: 2px; flex-shrink: 0;
  transition: transform var(--t-fast), color var(--t-fast);
}
.cpanel__item:hover .cpanel__arrow { transform: translateX(4px); color: #E85A4F; }
</style>
