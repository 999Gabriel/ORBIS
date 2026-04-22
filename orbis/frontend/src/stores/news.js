import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const now = Date.now()
const h = (n) => now - n * 3_600_000

export const MOCK_NEWS = [
  {
    id: 1, lat: 51.5074, lon: -0.1278,
    title: 'UK Parliament Passes Landmark Climate Bill',
    sentiment: 'positive', country: 'United Kingdom', city: 'London',
    category: 'politics',
    summary: [
      'The UK Parliament passed sweeping climate legislation requiring net-zero emissions by 2040, a decade ahead of previous targets.',
      'The bill mandates a 70% reduction in industrial carbon output within five years, with binding quarterly reviews.',
      'Environmental groups called it the most ambitious climate law in European history.',
    ],
    url: '#', timestamp: h(1),
  },
  {
    id: 2, lat: 40.7128, lon: -74.006,
    title: 'Wall Street Hits Record High Amid AI Investment Surge',
    sentiment: 'positive', country: 'United States', city: 'New York',
    category: 'economy',
    summary: [
      'US equity markets reached all-time highs as institutional investors poured capital into AI infrastructure companies.',
      'The S&P 500 gained 2.3% in a single session, led by semiconductor and cloud computing stocks.',
      'Analysts warn that valuations may be outpacing fundamentals, signalling a potential correction.',
    ],
    url: '#', timestamp: h(2),
  },
  {
    id: 3, lat: 35.6762, lon: 139.6503,
    title: 'Tokyo Deploys Next-Generation Earthquake Early Warning System',
    sentiment: 'neutral', country: 'Japan', city: 'Tokyo',
    category: 'technology',
    summary: [
      'Japan activated an upgraded seismic early-warning network capable of issuing alerts up to 90 seconds before shaking begins.',
      'The system uses a distributed sensor grid of over 4,000 stations across the archipelago.',
      'Authorities estimate the new network could save tens of thousands of lives in a major metropolitan earthquake.',
    ],
    url: '#', timestamp: h(4),
  },
  {
    id: 4, lat: -33.8688, lon: 151.2093,
    title: 'Australia Declares State of Emergency as Heatwave Breaks Records',
    sentiment: 'negative', country: 'Australia', city: 'Sydney',
    category: 'climate',
    summary: [
      'New South Wales declared a state of emergency after temperatures in western Sydney exceeded 47°C for a third consecutive day.',
      'Power grids across three states were put on red alert as air-conditioning demand overwhelmed capacity.',
      'Climate scientists linked the extreme event to a strengthening La Niña cycle compounded by long-term warming trends.',
    ],
    url: '#', timestamp: h(5),
  },
  {
    id: 5, lat: 48.8566, lon: 2.3522,
    title: 'Paris Fashion Week Draws Record International Attendance',
    sentiment: 'positive', country: 'France', city: 'Paris',
    category: 'culture',
    summary: [
      'Paris Fashion Week attracted over 800,000 visitors, generating an estimated €1.2 billion for the local economy.',
      'Several major houses debuted collections blending traditional couture with sustainable materials and AI-generated prints.',
      'The event solidified Paris\'s position as the global capital of fashion despite growing competition from Milan and Seoul.',
    ],
    url: '#', timestamp: h(6),
  },
  {
    id: 6, lat: 55.7558, lon: 37.6176,
    title: 'Moscow Power Grid Hit by Widespread Disruptions',
    sentiment: 'negative', country: 'Russia', city: 'Moscow',
    category: 'infrastructure',
    summary: [
      'Rolling blackouts affected over two million residents in Moscow after a transformer failure cascaded through the regional grid.',
      'Emergency crews worked overnight to restore power to hospitals and critical infrastructure.',
      'The incident reignited debate about underinvestment in Russia\'s aging energy infrastructure.',
    ],
    url: '#', timestamp: h(8),
  },
  {
    id: 7, lat: 30.0444, lon: 31.2357,
    title: 'Egypt Unveils $15bn Saharan Solar Megaproject',
    sentiment: 'positive', country: 'Egypt', city: 'Cairo',
    category: 'climate',
    summary: [
      'Egypt signed agreements with a consortium of European and Gulf investors to build a 10-gigawatt solar farm in the Western Sahara.',
      'The project is projected to supply 30% of Egypt\'s electricity needs and enable significant green hydrogen exports by 2030.',
      'Construction is expected to create 120,000 jobs during its peak phase, beginning in late 2025.',
    ],
    url: '#', timestamp: h(10),
  },
  {
    id: 8, lat: -23.5505, lon: -46.6333,
    title: 'Brazil\'s Fiscal Crisis Deepens as Inflation Hits 14%',
    sentiment: 'negative', country: 'Brazil', city: 'São Paulo',
    category: 'economy',
    summary: [
      'Brazil\'s annual inflation rate climbed to 14.2%, the highest level in two decades, driven by food and fuel price surges.',
      'The central bank raised its benchmark rate to 13.75%, prompting fears of a broader economic contraction.',
      'Street protests erupted in São Paulo and Rio de Janeiro as purchasing power eroded sharply for lower-income households.',
    ],
    url: '#', timestamp: h(12),
  },
  {
    id: 9, lat: 28.6139, lon: 77.209,
    title: 'India\'s Tech Sector Attracts Record $18bn in Foreign Investment',
    sentiment: 'positive', country: 'India', city: 'New Delhi',
    category: 'economy',
    summary: [
      'India\'s technology and startup ecosystem received a record $18 billion in foreign direct investment in the first quarter.',
      'The surge was driven by major commitments from US and Japanese semiconductor firms seeking to diversify from Taiwan.',
      'The government announced an additional $5 billion in incentives to accelerate domestic chip manufacturing capacity.',
    ],
    url: '#', timestamp: h(14),
  },
  {
    id: 10, lat: 1.3521, lon: 103.8198,
    title: 'Singapore Launches World\'s First AI-Governed Smart Port',
    sentiment: 'positive', country: 'Singapore', city: 'Singapore',
    category: 'technology',
    summary: [
      'Singapore\'s Maritime Port Authority activated Tuas Terminal Phase 2, the world\'s first fully AI-governed container port.',
      'The facility handles 20 million TEUs annually with zero human operators on the quayside, managed entirely by autonomous systems.',
      'Officials estimate the technology will reduce docking delays by 40% and cut port emissions by 25%.',
    ],
    url: '#', timestamp: h(16),
  },
  {
    id: 11, lat: -1.2921, lon: 36.8219,
    title: 'Kenya\'s Wildlife Corridors Shrink as Climate Shifts Savannah',
    sentiment: 'negative', country: 'Kenya', city: 'Nairobi',
    category: 'climate',
    summary: [
      'A new study found that climate-driven drought has reduced Kenya\'s critical wildlife corridors by 38% over the past decade.',
      'Elephant and wildebeest migration routes are increasingly blocked by expanding human settlements chasing retreating water sources.',
      'Conservation groups called for emergency intervention from the African Union and international donors.',
    ],
    url: '#', timestamp: h(18),
  },
  {
    id: 12, lat: 52.52, lon: 13.405,
    title: 'Germany Accelerates Green Transition with New Grid Law',
    sentiment: 'positive', country: 'Germany', city: 'Berlin',
    category: 'climate',
    summary: [
      'Germany\'s Bundestag passed the Grid Modernisation Act, committing €200 billion to upgrade the national electricity transmission network.',
      'The law includes fast-track permitting for offshore wind connections and mandates 100% renewable electricity by 2035.',
      'Industry groups welcomed the move, saying it removes the biggest bottleneck to decarbonising German heavy industry.',
    ],
    url: '#', timestamp: h(20),
  },
  {
    id: 13, lat: 25.2048, lon: 55.2708,
    title: 'Dubai Global AI Summit Draws 190 Nations',
    sentiment: 'positive', country: 'UAE', city: 'Dubai',
    category: 'technology',
    summary: [
      'The inaugural Dubai Global AI Summit brought together heads of state and technology executives from 190 countries.',
      'Delegates signed the Dubai AI Charter, a non-binding framework for responsible AI development and cross-border data governance.',
      'The UAE announced a $100 billion sovereign AI fund targeting healthcare, logistics, and climate modelling applications.',
    ],
    url: '#', timestamp: h(22),
  },
  {
    id: 14, lat: 37.5665, lon: 126.978,
    title: 'South Korea\'s Chip Fabs Break Global Production Records',
    sentiment: 'positive', country: 'South Korea', city: 'Seoul',
    category: 'economy',
    summary: [
      'Samsung and SK Hynix reported record quarterly output of advanced memory chips, capturing 62% of global HBM supply.',
      'The milestone was driven by surging demand from AI accelerator manufacturers in the United States and Taiwan.',
      'South Korea\'s government extended its semiconductor investment tax credit programme for a further five years.',
    ],
    url: '#', timestamp: h(24),
  },
  {
    id: 15, lat: -34.6037, lon: -58.3816,
    title: 'Argentina Hyperinflation Crisis Triggers IMF Emergency Talks',
    sentiment: 'negative', country: 'Argentina', city: 'Buenos Aires',
    category: 'economy',
    summary: [
      'Argentina\'s monthly inflation rate hit 22%, pushing the annual figure above 270% and triggering emergency talks with the IMF.',
      'The peso fell to a historic low against the dollar on both official and parallel markets.',
      'President Milei announced an emergency austerity package cutting public sector wages and subsidies in an attempt to stabilise finances.',
    ],
    url: '#', timestamp: h(26),
  },
]

export const useNewsStore = defineStore('news', () => {
  const pins = ref(MOCK_NEWS)
  const selectedPin = ref(null)
  const activeFilter = ref('all')

  const filteredPins = computed(() => {
    if (activeFilter.value === 'all') return pins.value
    return pins.value.filter(p => p.category === activeFilter.value)
  })

  function selectPin(pin) {
    selectedPin.value = pin
  }

  function clearPin() {
    selectedPin.value = null
  }

  function setFilter(category) {
    activeFilter.value = category
  }

  return { pins, selectedPin, activeFilter, filteredPins, selectPin, clearPin, setFilter }
})
