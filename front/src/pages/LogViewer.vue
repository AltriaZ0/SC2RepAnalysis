  <script setup lang="ts">
  import { ref, onMounted, onBeforeUnmount } from 'vue'
  import { invoke } from '@tauri-apps/api/core'
  import { listen, UnlistenFn } from '@tauri-apps/api/event'

  const lines = ref<string[]>([])
  let unOut: UnlistenFn | null = null
  let unErr: UnlistenFn | null = null

  function push(line: string, tag: 'OUT'|'ERR') {
    const ts = new Date().toLocaleTimeString()
    lines.value.push(`[${ts}] ${tag} ${line}`)
    requestAnimationFrame(() => {
      const box = document.getElementById('log-box')
      if (box) box.scrollTop = box.scrollHeight
    })
  }

  async function startPy() { await invoke('start_python', { logLevel: 'DEBUG' }) }
  async function stopPy() { await invoke('stop_python') }

  onMounted(async () => {
    unOut = await listen<string>('py:stdout', e => push(e.payload, 'OUT'))
    unErr = await listen<string>('py:stderr', e => push(e.payload, 'ERR'))
  })
  onBeforeUnmount(() => { unOut?.(); unErr?.() })
  </script>

  <template>
    <div class="p-4 space-y-3">
      <div class="space-x-2">
        <button @click="startPy">启动 Python</button>
        <button @click="stopPy">停止 Python</button>
      </div>
      <div id="log-box" style="height:420px; overflow:auto; white-space:pre; font-family:monospace; border:1px solid #ccc; padding:8px;">
        <div v-for="(l,i) in lines" :key="i">{{ l }}</div>
      </div>
    </div>
  </template>
