import { ref, onUnmounted } from 'vue'

// Stub — real WebSocket connection wired in Phase 2 when backend is live.
export function useWebSocket(url) {
  const isConnected = ref(false)
  const lastMessage = ref(null)
  let ws = null

  function connect() {
    // No-op until backend exists
    console.info('[WebSocket] stub — backend not yet available')
  }

  function disconnect() {
    if (ws) {
      ws.close()
      ws = null
      isConnected.value = false
    }
  }

  function send(data) {
    if (ws && isConnected.value) {
      ws.send(JSON.stringify(data))
    }
  }

  onUnmounted(disconnect)

  return { isConnected, lastMessage, connect, disconnect, send }
}
