import { shallowRef, ref } from 'vue'
import earthDayUrl from '@/assets/globe/earth-day.jpg'

let cachedLightMap = null
const _geomCache = new Map()
const _matCache  = new Map()

export const SENTIMENT_COLORS = {
  positive: '#2D7A4A',
  neutral:  '#888880',
  negative: '#B83232',
}

const PIN_COLOR     = '#E85A4F'
const CLUSTER_COLOR = '#F3C843'
const OIL_COLOR     = '#F3C843'

export function useGlobe() {
  const globeInstance = shallowRef(null)
  const isReady = ref(false)

  async function init(containerEl, { onPinClick, onPinHover, onWeatherClick } = {}) {
    const [{ default: Globe }, THREE] = await Promise.all([
      import('globe.gl'),
      import('three'),
    ])

    const w = containerEl.offsetWidth || window.innerWidth
    const h = containerEl.offsetHeight || window.innerHeight

    const dotMap = await createDotEarthTexture(THREE)

    const globe = new Globe(containerEl, { rendererConfig: { antialias: true, alpha: true } })
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
      // ── Objects (3-D bars) ───────────────────────────────────────────────
      .objectsData([])
      .objectLat('lat')
      .objectLng('lon')
      .objectAltitude(0.002)
      // objectFacesSurface rotates each object so its local +Z points radially
      // outward — our cylinders are pre-rotated to align their axis with +Z,
      // so they stand upright on the globe and are fully clickable.
      .objectFacesSurface(true)
      .objectThreeObject(d => createPinObject(THREE, d))
      .onObjectClick((pin) => onPinClick?.(pin))
      .onObjectHover((pin) => {
        containerEl.style.cursor = pin ? 'pointer' : 'grab'
        onPinHover?.(pin)
      })
      // ── Weather heatmap (temperature gradient) ───────────────────────────
      .heatmapsData([])
      .heatmapPointLat('lat')
      .heatmapPointLng('lon')
      .heatmapPointWeight('weight')
      .heatmapBandwidth(10)
      .heatmapColorFn(() => t => _tempGradient(t))
      .heatmapColorSaturation(2.5)
      .heatmapBaseAltitude(0.005)
      // ── Weather city labels (name + temperature) ──────────────────────────
      .labelsData([])
      .labelLat('lat')
      .labelLng('lon')
      .labelText(d => `${Math.round(d.temp)}°  ${d.city}`)
      .labelColor(d => d._selected ? '#F3C843' : 'rgba(255,255,255,0.88)')
      .labelSize(0.55)
      .labelDotRadius(d => d._selected ? 0.55 : 0.38)
      .labelDotOrientation(() => 'right')
      .labelResolution(3)
      .labelAltitude(0.005)
      .onLabelClick(lbl => onWeatherClick?.(lbl))
      .onLabelHover(lbl => {
        containerEl.style.cursor = lbl ? 'pointer' : 'grab'
      })
      // ── Points layer (kept empty; reserved for future use) ───────────────
      .pointsData([])
      // ── Pulsing rings (globe.gl built-in animated layer) ─────────────────
      .ringsData([])
      .ringLat('lat')
      .ringLng('lon')
      .ringColor(() => [PIN_COLOR, 'rgba(232,90,79,0)'])
      .ringMaxRadius(2.5)
      .ringPropagationSpeed(2.0)
      .ringRepeatPeriod(1200)
      .ringAltitude(0.001)

    globe.lights([
      new THREE.AmbientLight('#FFFFFF', 0.55),
      new THREE.DirectionalLight('#FFFFFF', 2.20),
      new THREE.DirectionalLight('#E0E0E0', 0.40),
    ])
    globe.controls().autoRotate = true
    globe.controls().autoRotateSpeed = 0.24
    globe.controls().enableDamping = true
    globe.controls().dampingFactor = 0.1
    globe.controls().minDistance = 200
    globe.controls().maxDistance = 800

    globe.controls().addEventListener('start', () => {
      globe.controls().autoRotate = false
    })
    globe.controls().addEventListener('end', () => {
      setTimeout(() => { globe.controls().autoRotate = true }, 3000)
    })

    globeInstance.value = globe
    isReady.value = true
  }

  function updatePoints(points, selectedPin = null) {
    if (!globeInstance.value) return
    const tagged = points.map(p => ({ ...p, _selected: p.id === selectedPin?.id }))
    globeInstance.value.objectsData(tagged)
  }

  function updateRings(singlePins) {
    if (!globeInstance.value) return
    globeInstance.value.ringsData(singlePins)
  }

  function updateWeatherMap(pins, selectedPin = null) {
    if (!globeInstance.value) return
    if (!pins.length) {
      globeInstance.value.heatmapsData([]).labelsData([])
      return
    }
    const selectedId = selectedPin?.city_id ?? null
    const temps = pins.map(p => p.temp).filter(t => t != null)
    const minT  = Math.min(...temps)
    const maxT  = Math.max(...temps)
    const range = maxT - minT || 1
    const tagged = pins.map(p => ({
      ...p,
      weight:    Math.max(0, Math.min(1, (p.temp - minT) / range)),
      _selected: p.city_id === selectedId,
    }))
    globeInstance.value
      .heatmapsData([tagged])
      .labelsData(tagged)
  }

  function flyTo(lat, lon, altitude = 1.8, duration = 900) {
    if (!globeInstance.value) return
    globeInstance.value.pointOfView({ lat, lng: lon, altitude }, duration)
  }

  function resize(width, height) {
    if (!globeInstance.value) return
    globeInstance.value.width(width).height(height)
  }

  function destroy() {
    globeInstance.value?._destructor?.()
    globeInstance.value = null
    isReady.value = false
  }

  return { globeInstance, isReady, init, updatePoints, updateRings, updateWeatherMap, flyTo, resize, destroy }
}

// ── Geometry cache ────────────────────────────────────────────────────────────
// Cylinders are pre-rotated so their axis aligns with local +Z.
// objectFacesSurface(true) makes +Z point radially outward — cylinders stand upright.
function _getGeom(THREE, rTop, rBot, height, segments = 8) {
  const key = `${rTop.toFixed(2)}-${rBot.toFixed(2)}-${height.toFixed(2)}-${segments}`
  if (!_geomCache.has(key)) {
    const g = new THREE.CylinderGeometry(rTop, rBot, height, segments)
    // Rotate +90° around X: cylinder axis Y → Z
    g.applyMatrix4(new THREE.Matrix4().makeRotationX(Math.PI / 2))
    // Pivot at base: Z=0 sits at the globe surface, Z=height sticks outward
    g.translate(0, 0, height / 2)
    _geomCache.set(key, g)
  }
  return _geomCache.get(key)
}

// ── Material cache ────────────────────────────────────────────────────────────
function _getMat(THREE, color, emissiveIntensity = 0.25) {
  const key = `${color}-${emissiveIntensity}`
  if (!_matCache.has(key)) {
    _matCache.set(key, new THREE.MeshPhongMaterial({
      color,
      emissive: color,
      emissiveIntensity,
      shininess: 55,
    }))
  }
  return _matCache.get(key)
}

// ── Pin / cluster / oil marker builder ───────────────────────────────────────
function createPinObject(THREE, pin) {
  const group = new THREE.Group()

  if (pin._type === 'oil') {
    const sel = pin._selected
    const r   = sel ? 5.0 : 3.8
    const h   = 1.6
    const disc = new THREE.CylinderGeometry(r, r * 1.05, h, 16)
    disc.applyMatrix4(new THREE.Matrix4().makeRotationX(Math.PI / 2))
    disc.translate(0, 0, h / 2)
    group.add(new THREE.Mesh(disc, _getMat(THREE, OIL_COLOR, sel ? 0.75 : 0.45)))
    if (sel) {
      const ring = new THREE.RingGeometry(r + 1.5, r + 3.0, 32)
      group.add(new THREE.Mesh(ring, new THREE.MeshBasicMaterial({
        color: OIL_COLOR, side: THREE.DoubleSide, transparent: true, opacity: 0.55,
      })))
    }
    return group
  }

  if (pin._cluster) {
    const n      = Math.min(pin._count, 20)
    const rBot   = Math.min(2.8 + n * 0.18, 6.0)
    const rTop   = rBot * 0.60
    const height = Math.min(18.0 + n * 1.4, 36.0)
    group.add(new THREE.Mesh(
      _getGeom(THREE, rTop, rBot, height),
      _getMat(THREE, CLUSTER_COLOR, 0.50),
    ))
    return group
  }

  const sel    = pin._selected
  const rBot   = sel ? 2.2 : 1.5
  const rTop   = sel ? 1.1 : 0.75
  const height = sel ? 18  : 12

  group.add(new THREE.Mesh(
    _getGeom(THREE, rTop, rBot, height),
    _getMat(THREE, PIN_COLOR, sel ? 0.65 : 0.32),
  ))

  if (sel) {
    // Halo ring at the cylinder base — lies flat on the globe surface
    // because objectFacesSurface makes +Z point outward and RingGeometry
    // is in the XY plane (normal along +Z), so it appears as a coin on the surface.
    const ringGeom = new THREE.RingGeometry(3.0, 5.2, 32)
    const ring = new THREE.Mesh(
      ringGeom,
      new THREE.MeshBasicMaterial({
        color: PIN_COLOR,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.55,
      }),
    )
    group.add(ring)
  }

  return group
}

// ── Temperature → colour gradient (cold → hot) ───────────────────────────────
function _tempGradient(t) {
  const stops = [
    [0.00, [26,  68, 194]],
    [0.20, [ 0, 184, 212]],
    [0.40, [76, 175,  80]],
    [0.58, [243, 200,  67]],
    [0.78, [255, 140,   0]],
    [1.00, [230,  48,  48]],
  ]
  for (let i = 1; i < stops.length; i++) {
    if (t <= stops[i][0]) {
      const [t0, c0] = stops[i - 1]
      const [t1, c1] = stops[i]
      const f = (t - t0) / (t1 - t0)
      const r = Math.round(c0[0] + f * (c1[0] - c0[0]))
      const g = Math.round(c0[1] + f * (c1[1] - c0[1]))
      const b = Math.round(c0[2] + f * (c1[2] - c0[2]))
      return `rgba(${r},${g},${b},0.72)`
    }
  }
  return 'rgba(230,48,48,0.72)'
}

// ── Dot-earth texture ─────────────────────────────────────────────────────────
export function createDotEarthTexture(THREE) {
  if (cachedLightMap) return Promise.resolve(cachedLightMap)

  return new Promise((resolve, reject) => {
    const image = new Image()
    image.onload = () => {
      const src = document.createElement('canvas')
      src.width  = image.naturalWidth
      src.height = image.naturalHeight
      const srcCtx = src.getContext('2d', { willReadFrequently: true })
      srcCtx.drawImage(image, 0, 0)
      const pixels = srcCtx.getImageData(0, 0, src.width, src.height).data

      const out = document.createElement('canvas')
      out.width  = src.width
      out.height = src.height
      const ctx = out.getContext('2d')

      ctx.fillStyle = '#050505'
      ctx.fillRect(0, 0, out.width, out.height)

      const STEP = 5
      const R    = 1.5
      ctx.fillStyle = '#FFFFFF'

      for (let y = STEP / 2; y < out.height; y += STEP) {
        for (let x = STEP / 2; x < out.width; x += STEP) {
          const ix   = Math.floor(x)
          const iy   = Math.floor(y)
          const base = (iy * src.width + ix) * 4
          const r    = pixels[base]
          const g    = pixels[base + 1]
          const b    = pixels[base + 2]
          const isOcean = b > r + 18 && b > g + 6
          if (!isOcean) {
            ctx.beginPath()
            ctx.arc(x, y, R, 0, Math.PI * 2)
            ctx.fill()
          }
        }
      }

      const texture = new THREE.CanvasTexture(out)
      texture.colorSpace = THREE.SRGBColorSpace
      texture.anisotropy = 4
      texture.needsUpdate = true
      cachedLightMap = texture
      resolve(texture)
    }
    image.onerror = reject
    image.src = earthDayUrl
  })
}
