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

export function useGlobe() {
  const globeInstance = shallowRef(null)
  const isReady = ref(false)

  async function init(containerEl, { onPinClick, onPinHover } = {}) {
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
      .objectsData([])
      .objectLat('lat')
      .objectLng('lon')
      .objectAltitude(0.002)
      .objectThreeObject(d => createPinObject(THREE, d))
      .onObjectClick((pin) => onPinClick?.(pin))
      .onObjectHover((pin) => {
        containerEl.style.cursor = pin ? 'pointer' : 'grab'
        onPinHover?.(pin)
      })

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

  return { globeInstance, isReady, init, updatePoints, flyTo, resize, destroy }
}

// Shared geometry cache — keyed by dimensions so identical shapes reuse buffers
function _getGeom(THREE, rTop, rBot, height, segments = 8) {
  const key = `${rTop.toFixed(2)}-${rBot.toFixed(2)}-${height.toFixed(2)}-${segments}`
  if (!_geomCache.has(key)) {
    const g = new THREE.CylinderGeometry(rTop, rBot, height, segments)
    g.translate(0, height / 2, 0)   // pivot at base so altitude=0.002 sits the cylinder ON the surface
    _geomCache.set(key, g)
  }
  return _geomCache.get(key)
}

// Shared material cache — keyed by color + emissive intensity
function _getMat(THREE, color, emissiveIntensity = 0.18) {
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

function createPinObject(THREE, pin) {
  const group = new THREE.Group()

  if (pin._cluster) {
    // Scale cluster cylinder with article count (capped so it doesn't dominate)
    const n      = Math.min(pin._count, 12)
    const rBot   = Math.min(0.85 + n * 0.07, 1.65)
    const rTop   = rBot * 0.72
    const height = Math.min(3.0 + n * 0.38, 7.0)
    group.add(new THREE.Mesh(
      _getGeom(THREE, rTop, rBot, height),
      _getMat(THREE, '#BEBDB4', 0.22),
    ))
    return group
  }

  const color  = SENTIMENT_COLORS[pin.sentiment] ?? SENTIMENT_COLORS.neutral
  const sel    = pin._selected
  const rBot   = sel ? 0.90 : 0.62
  const rTop   = sel ? 0.50 : 0.33
  const height = sel ? 5.2  : 3.5

  group.add(new THREE.Mesh(
    _getGeom(THREE, rTop, rBot, height),
    _getMat(THREE, color, sel ? 0.48 : 0.18),
  ))

  if (sel) {
    // Glowing halo ring flat on the globe surface at the cylinder base
    const ringGeom = new THREE.RingGeometry(1.05, 1.75, 28)
    const ringMat  = new THREE.MeshBasicMaterial({
      color,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.50,
    })
    const ring = new THREE.Mesh(ringGeom, ringMat)
    ring.rotation.x = -Math.PI / 2
    group.add(ring)
  }

  return group
}

// Black globe with white land dots — matches the logo aesthetic
function createDotEarthTexture(THREE) {
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
