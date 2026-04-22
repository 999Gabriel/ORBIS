import { shallowRef, ref } from 'vue'

const GLOBE_IMAGE_URL = '//unpkg.com/three-globe/example/img/earth-night.jpg'
const BG_IMAGE_URL    = '//unpkg.com/three-globe/example/img/night-sky.png'

export const SENTIMENT_COLORS = {
  positive: '#52C97A',
  neutral:  '#E09A3A',
  negative: '#E05252',
}

export function useGlobe() {
  const globeInstance = shallowRef(null)
  const isReady = ref(false)

  async function init(containerEl, { onPinClick, onPinHover } = {}) {
    const { default: Globe } = await import('globe.gl')

    const globe = Globe()
      .globeImageUrl(GLOBE_IMAGE_URL)
      .backgroundImageUrl(BG_IMAGE_URL)
      .atmosphereColor('#4a90e2')
      .atmosphereAltitude(0.18)
      .width(containerEl.offsetWidth)
      .height(containerEl.offsetHeight)
      // points layer (news pins)
      .pointsData([])
      .pointLat('lat')
      .pointLng('lon')
      .pointColor(d => SENTIMENT_COLORS[d.sentiment] ?? SENTIMENT_COLORS.neutral)
      .pointRadius(d => (d._selected ? 0.9 : 0.55))
      .pointAltitude(0.015)
      .pointResolution(16)
      .pointsMerge(false)
      .onPointClick((point, _event) => onPinClick?.(point))
      .onPointHover((point) => {
        containerEl.style.cursor = point ? 'pointer' : 'grab'
        onPinHover?.(point)
      })
      (containerEl)

    // Controls
    globe.controls().autoRotate = true
    globe.controls().autoRotateSpeed = 0.35
    globe.controls().enableDamping = true
    globe.controls().dampingFactor = 0.1
    globe.controls().minDistance = 200
    globe.controls().maxDistance = 800

    // Stop auto-rotate on user interaction, resume after 3s
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
    globeInstance.value.pointsData(tagged)
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
    globeInstance.value = null
    isReady.value = false
  }

  return { globeInstance, isReady, init, updatePoints, flyTo, resize, destroy }
}
