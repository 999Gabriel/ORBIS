<template>
  <div class="orbis-app">
    <GlobeView />
    <NavBar />
    <FilterBar />
    <NewsSidebar />
    <TimelineSlider />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import FilterBar from '@/components/FilterBar.vue'
import GlobeView from '@/components/GlobeView.vue'
import NewsSidebar from '@/components/NewsSidebar.vue'
import TimelineSlider from '@/components/TimelineSlider.vue'
import { useNewsStore } from '@/stores/news.js'

const newsStore = useNewsStore()
onMounted(() => newsStore.fetchNews())
</script>

<style scoped>
.orbis-app {
  position: fixed; inset: 0; overflow: hidden;
  background: var(--canvas);
}
</style>
