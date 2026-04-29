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
import NavBar from '@/components/NavBar.vue'
import FilterBar from '@/components/FilterBar.vue'
import GlobeView from '@/components/GlobeView.vue'
import NewsSidebar from '@/components/NewsSidebar.vue'
import TimelineSlider from '@/components/TimelineSlider.vue'
</script>

<style scoped>
.orbis-app {
  position: fixed;
  inset: 0;
  overflow: hidden;
  background: var(--canvas);
}
</style>
