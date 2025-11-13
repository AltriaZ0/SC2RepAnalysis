<template>
  <div class="page">
    <!-- 顶部工具条 -->
    <header class="toolbar">
      <div class="left">
        <h1 class="title">单文件分析</h1>
      </div>
      <!-- <div class="right">
        <div class="search-box">
          <svg class="icon" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke="currentColor" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M21 21l-4.3-4.3M10 18a8 8 0 1 1 0-16 8 8 0 0 1 0 16z"/>
          </svg>
          <input v-model="keyword" type="text" placeholder="搜索历史记录…" @input="onSearch" />
        </div>
        <button class="btn ghost" @click="openHistory = !openHistory">历史记录</button>
      </div> -->
    </header>

    <div class="content">
      <!-- 左：上传与选项 -->
      <section class="left-pane">
        <div
          class="dropzone"
          :class="{ dragover }"
          @dragover.prevent="dragover = true"
          @dragleave.prevent="dragover = false"
          @drop.prevent="onDrop"
          v-if="!fileMeta"
        >
          <div class="dz-inner">
            <svg class="dz-icon" viewBox="0 0 24 24" aria-hidden="true">
              <path fill="currentColor" d="M16.59 5.59 12 1 7.41 5.59 8.83 7l2.17-2.17V14h2V4.83L15.17 7 16.59 5.59zM19 10h-2v6H7v-6H5v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6z"/>
            </svg>
            <p class="dz-title">拖拽含有<span>.SC2Replay文件</span> 的文件夹到此处</p>
            <p class="dz-sub">或 <button class="link" @click="pickFile">点击选择</button> 本地文件夹</p>
            <input ref="fileInput" class="hidden" type="file" accept=".SC2Replay,.sc2replay" @change="onFile" />
          </div>
        </div>

        <div class="card" v-if="fileMeta">
          <div class="card-header">
            <div class="file-name" :title="fileMeta.name">{{ fileMeta.name }}</div>
            <button class="btn tiny" @click="clearFile">移除</button>
          </div>
          <ul class="meta">
            <li><span>大小</span><span>{{ prettySize(fileMeta.size) }}</span></li>
            <li><span>修改时间</span><span>{{ fileMeta.mtime }}</span></li>
            <li><span>路径</span><span class="truncate" :title="fileMeta.path">{{ fileMeta.path }}</span></li>
          </ul>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-title">分析选项</div>
            <button class="btn ghost tiny" @click="resetOptions">重置</button>
          </div>
          <div class="options">
            <label class="opt"><input type="checkbox" v-model="opts.basic"/>只统计有事件发生的时间</label>
            <label class="opt"><input type="checkbox" v-model="opts.bo"/> 建筑建造统计 </label>
            <label class="opt"><input type="checkbox" v-model="opts.actions"/> 科技升级统计 </label>
            <label class="opt"><input type="checkbox" v-model="opts.units"/> 单位建造统计 </label>
            <label class="opt"><input type="checkbox" v-model="opts.mapheat"/> 农民数量统计(demo) </label>
            <label class="opt"><input type="checkbox" v-model="opts.exportXlsx"/> 导出 Excel（.xlsx）</label>
            <label class="opt"><input type="checkbox" /> 导出 txt（旧功能）</label>
          </div>
          <div class="row">
            <div class="col">
              <label class="label">时区</label>
              <select v-model="opts.tz" class="select">
                <option value="local">本地</option>
                <option value="UTC">UTC</option>
              </select>
            </div>
            <div class="col">
              <label class="label">语言</label>
              <select v-model="opts.lang" class="select">
                <option value="zh">中文</option>
                <option value="en">English</option>
              </select>
            </div>
          </div>

          <div class="actions">
            <button class="btn primary" :disabled="!fileMeta || busy" @click="startAnalyze">
              {{ busy ? '分析中…' : '开始分析' }}
            </button>
            <button class="btn" :disabled="!fileMeta || busy" @click="quickPreview">快速预览</button>
          </div>

          <div class="progress" v-if="busy">
            <div class="bar" :style="{ width: progress + '%' }"></div>
          </div>
          <p class="hint" v-if="errorMsg">{{ errorMsg }}</p>
        </div>
      </section>

      <!-- 右：结果展示 -->
      <section class="right-pane">
        <div class="placeholder" v-if="!result">
          <p class="muted">尚未开始分析</p>
          <p class="muted">选择一个 .SC2Replay 文件并点击「开始分析」</p>
        </div>

        <div v-else class="result">
          <div class="card">
            <div class="card-header">
              <div class="card-title">概览</div>
              <div class="card-sub">分析耗时：{{ result.elapsed }} ms</div>
            </div>
            <div class="overview-grid">
              <div class="kv"><span>地图</span><b>{{ result.map }}</b></div>
              <div class="kv"><span>时长</span><b>{{ result.duration }}</b></div>
              <div class="kv"><span>胜负</span><b :class="{ win: result.win }">{{ result.win ? '胜利' : '失败' }}</b></div>
              <div class="kv"><span>种族</span><b>{{ result.race }}</b></div>
              <div class="kv"><span>APM</span><b>{{ result.apm }}</b></div>
              <div class="kv"><span>回放版本</span><b>{{ result.version }}</b></div>
            </div>
          </div>

          <div class="card" v-if="result.bo?.length">
            <div class="card-header">
              <div class="card-title">Build Order</div>
              <button class="btn tiny ghost" @click="copyBO">复制</button>
            </div>
            <ol class="bo-list">
              <li v-for="(step, i) in result.bo" :key="i">
                <span class="time">{{ step.t }}</span>
                <span class="what">{{ step.action }}</span>
              </li>
            </ol>
          </div>

          <div class="card" v-if="result.exportPath">
            <div class="card-header">
              <div class="card-title">导出</div>
            </div>
            <div class="export-row">
              <span class="muted">已生成 Excel：</span>
              <button class="btn success" @click="openFile(result.exportPath)">打开结果 (.xlsx)</button>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- 分析历史：未启用 -->
    <transition name="slide">
      <aside class="history" v-if="openHistory">
        <div class="history-header">
          <h2>最近分析</h2>
          <button class="btn ghost tiny" @click="openHistory = false">关闭</button>
        </div>
        <div class="history-list">
          <div v-for="item in filteredHistory" :key="item.id" class="history-card">
            <div class="top">
              <div class="title" :title="item.name">{{ item.name }}</div>
              <div class="meta">{{ item.date }} · {{ prettySize(item.size) }}</div>
            </div>
            <div class="bottom">
              <button class="btn tiny" @click="restoreHistory(item)">恢复</button>
              <button class="btn ghost tiny" @click="removeHistory(item.id)">删除</button>
            </div>
          </div>
        </div>
      </aside>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onBeforeUnmount } from 'vue'
import { invoke } from '@tauri-apps/api/core'
import { listen, UnlistenFn } from '@tauri-apps/api/event'
import { open } from '@tauri-apps/plugin-dialog'
import {appDataDir} from '@tauri-apps/api/path'

const keyword = ref('')
const openHistory = ref(false)
const dragover = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

const fileMeta = ref<null | { name: string; size: number; mtime: string; path: string }>(null)
const busy = ref(false)
const progress = ref(0)
const errorMsg = ref('')

const opts = reactive({
  analyze_type: "multi",
  output_dir: '' as string,
  basic: true,
  bo: true,
  actions: true,
  units: true,
  mapheat: false,
  exportXlsx: true,
  tz: 'local',
  lang: 'zh'
})

interface ResultBO { t: string; action: string }

interface AnalyzeResult {
  elapsed: number
  map: string
  duration: string
  win: boolean
  race: string
  apm: number
  version: string
  bo?: ResultBO[]
  exportPath?: string
}

const result = ref<AnalyzeResult | null>(null)

// 历史
// const history = ref(
//   Array.from({ length: 6 }).map((_, i) => ({
//     id: String(i + 1),
//     name: `Replay_${i + 1}.SC2Replay`,
//     size: 2_000_000 + i * 1024,
//     date: `2025/11/${6 - i}`,
//     path: `C:/replays/Replay_${i + 1}.SC2Replay`
//   }))
// )

// const filteredHistory = computed(() =>
//   history.value.filter(h => h.name.toLowerCase().includes(keyword.value.trim().toLowerCase()))
// )

async function pickFile() {
  const selected = await open({
    directory: true,
    multiple: true,
  })
  if (!selected) return
  console.log('selected:', selected)
  const path = Array.isArray(selected) ? selected[0] : selected
  const name = path.split(/[/\\]/).pop() || '回放文件'
  console.log('name:', name)
  console.log('path:', path)

  fileMeta.value = {
    name,
    size: 0,
    mtime: new Date().toLocaleString(),
    path, 
  }

  result.value = null
  errorMsg.value = ''
}

function onFile(e: Event) {
  const f = (e.target as HTMLInputElement).files?.[0]
  if (!f) return
  attachFile(f)
}

function onDrop(e: DragEvent) {
  dragover.value = false
  const f = e.dataTransfer?.files?.[0]
  if (!f) return
  attachFile(f)
}

function attachFile(f: File) {
  const mtime = new Date().toLocaleString()
  fileMeta.value = {
    name: f.name,
    size: f.size,
    mtime,
    path: (f as any).path || '本地选择的回放'
  }
  result.value = null
  errorMsg.value = ''
}

function clearFile() {
  fileMeta.value = null
  result.value = null
}

function resetOptions() {
  opts.analyze_type = "multi"
  output_dir: '' as string,
  opts.basic = true
  opts.bo = true
  opts.actions = true
  opts.units = true
  opts.mapheat = false
  opts.exportXlsx = true
  opts.tz = 'local'
  opts.lang = 'zh'
}


let unlisten: UnlistenFn | null = null
let unlistenProgress: UnlistenFn | null = null
let unlistenFileDrop: UnlistenFn | null = null

onMounted(async () => {
  // 监听 Rust 侧发来的进度事件
  unlisten = await listen<{ percent: number }>('analyze_progress', (e) => {
    progress.value = Math.max(progress.value, Math.min(99, e.payload.percent ?? 0))
  })

  opts.output_dir = await appDataDir() 

  unlistenFileDrop = await listen<string[]>('tauri://drag-drop', (event) => {

    const paths = event.payload.paths
    if (!paths || !paths.length) return
    console.log("测试通过")
    const path = paths[0]
    const name = path.split(/[/\\]/).pop() || '回放文件'

    fileMeta.value = {
      name,
      size: 0,
      mtime: new Date().toLocaleString(),
      path,
    }
    result.value = null
    errorMsg.value = ''
  })


})

onBeforeUnmount(() => { 
  unlisten?.(); unlisten = null
  unlistenFileDrop?.(); unlistenFileDrop = null
})

async function startAnalyze() {
  if (!fileMeta.value) return
  busy.value = true
  progress.value = 0
  errorMsg.value = ''
  result.value = null

  // TODO: 增加进度条
    try {
    // invoke Rust command
    console.log("fileMeta.value.path:",fileMeta.value.path)
    console.log("opts:",opts)
    const res = await invoke<AnalyzeResult>('analyze_replay', {
      path: fileMeta.value.path,
      options: {...opts }
    })
    progress.value = 100
    result.value = res
  } catch (e: any) {
    errorMsg.value = e?.message || '分析失败，请稍后重试'
  } finally {
    busy.value = false
  }

}

function quickPreview() {
  if (!fileMeta.value) return
  result.value = {
    elapsed: 0,
    map: '—',
    duration: '—',
    win: false,
    race: '—',
    apm: 0,
    version: '—'
  }
}

function copyBO() {
  if (!result.value?.bo?.length) return
  const text = result.value.bo.map(s => `${s.t}\t${s.action}`).join('\n')
  navigator.clipboard.writeText(text)
}

function openFile(path: string) {
  console.log('open:', path)
}

function removeHistory(id: string) {
  history.value = history.value.filter(h => h.id !== id)
}

function restoreHistory(item: any) {
  fileMeta.value = { name: item.name, size: item.size, mtime: item.date, path: item.path }
  openHistory.value = false
}

function prettySize(size: number) {
  if (size < 1024) return size + ' B'
  if (size < 1024 * 1024) return (size / 1024).toFixed(1) + ' KB'
  return (size / 1024 / 1024).toFixed(2) + ' MB'
}

function fakeProgress() {
  return new Promise<void>(resolve => {
    const timer = setInterval(() => {
      progress.value = Math.min(98, progress.value + Math.random() * 12)
    }, 120)
    setTimeout(() => {
      clearInterval(timer)
      progress.value = 100
      setTimeout(() => resolve(), 180)
    }, 1200)
  })
}
</script>

<style scoped>


.page { display: flex; flex-direction: column; height: 100%; background: var(--bg); color: var(--text); }
/* .toolbar {
   display: flex; align-items: center; justify-content: space-between; padding: 14px 20px; border-bottom: 1px solid var(--border); background: #0e1012; position: sticky; top: 0; z-index: 2; 
  } */
.title { font-size: 18px; margin: 4px 4px; font-weight: 700; }
.toolbar .right { display: flex; align-items: center; gap: 10px; }

.search-box { display: flex; align-items: center; gap: 8px; background: var(--panel); border: 1px solid var(--border); padding: 8px 10px; border-radius: 12px; width: 320px; }
.search-box .icon { width: 18px; height: 18px; color: var(--muted); }
.search-box input { background: transparent; border: none; outline: none; color: var(--text); width: 100%; }

.content {
  margin-top: 50px;
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: 16px;
  padding: 16px 20px; 
  height: calc(100vh - 50px);
  box-sizing: border-box;
  overflow: hidden;
   }
.left-pane, .right-pane { height: 100%; overflow: auto; padding-right: 6px; }

.dropzone { border: 1.5px dashed var(--border); background: var(--panel-2); border-radius: 16px; padding: 26px; text-align: center; transition: .15s ease; }
.dropzone.dragover { border-color: var(--primary); background: #101318; box-shadow: 0 0 0 3px rgba(59,130,246,.12) inset; }
.dz-inner { display: grid; gap: 6px; place-items: center; }
.dz-icon { width: 44px; height: 44px; color: var(--muted); }
.dz-title { font-weight: 600; border:#ffffff}
.dz-title span { color: var(--primary); }
.dz-sub { color: var(--muted); }
.hidden { display: none; }
.link { color: var(--primary); background: transparent; border: none; cursor: pointer; padding: 0; }

.card { background: var(--panel); border: 1px solid var(--border); border-radius: 16px; padding: 14px; margin-top: 12px; }
.card-header { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-bottom: 8px; }
.card-title { font-weight: 700; }
.card-sub { color: var(--muted); font-size: 12px; }
.file-name { font-weight: 600; max-width: calc(100% - 80px); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.meta { list-style: none; padding: 0; margin: 0; display: grid; gap: 6px; }
.meta li { display: flex; justify-content: space-between; border-bottom: 1px dashed var(--border); padding: 6px 0; }
.meta li:last-child { border-bottom: none; }
.truncate { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.options { display: grid; grid-template-columns: 1fr; gap: 8px; margin: 8px 0 10px; }
.opt { display: flex; align-items: center; gap: 8px; user-select: none; }
.row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 6px; }
.col { display: flex; flex-direction: column; gap: 6px; }
.label { color: var(--muted); font-size: 12px; }
.select { background: #0f1317; border: 1px solid var(--border); color: var(--text); padding: 8px 10px; border-radius: 10px; }

.actions { display: flex; gap: 10px; margin-top: 12px; }
.btn { border: 1px solid var(--border); background: #0f1317; color: var(--text); padding: 8px 12px; border-radius: 10px; cursor: pointer; transition: .15s ease; }
.btn:hover { filter: brightness(1.1); }
.btn:disabled { opacity: .5; cursor: not-allowed; }
.btn.primary { background: var(--primary); border-color: transparent; color: white; }
.btn.success { background: var(--success); border-color: transparent; color: #0b1b10; }
.btn.ghost { background: transparent; }
.btn.tiny { padding: 6px 10px; font-size: 12px; border-radius: 8px; }

.progress { height: 8px; border-radius: 999px; background: #0f1317; border: 1px solid var(--border); overflow: hidden; margin-top: 10px; }
.progress .bar { height: 100%; background: linear-gradient(90deg, var(--primary), #67a3ff); width: 0%; transition: width .2s ease; }

.hint { color: #fca5a5; margin-top: 8px; }

.placeholder { display: grid; place-items: center; height: 100%; gap: 8px; }
.muted { color: var(--muted); }

.result { display: grid; gap: 12px; }
.overview-grid { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 10px; }
.kv { background: #111418; border: 1px solid var(--border); border-radius: 12px; padding: 12px; display: flex; flex-direction: column; gap: 6px; }
.kv span { color: var(--muted); font-size: 12px; }
.kv b { font-size: 16px; }
.kv b.win { color: var(--success); }

.bo-list { margin: 0; padding-left: 18px; display: grid; gap: 6px; }
.bo-list .time { color: var(--muted); margin-right: 10px; }

.export-row { display: flex; align-items: center; gap: 10px; }

/* 历史抽屉 */
.history { position: fixed; right: 0; top: 60px; bottom: 0; width: 420px; background: #0e1012; border-left: 1px solid var(--border); padding: 14px; overflow: auto; }
.history-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.history-list { display: grid; gap: 10px; }
.history-card { background: var(--panel); border: 1px solid var(--border); border-radius: 14px; padding: 12px; }
.history-card .top { display: flex; justify-content: space-between; gap: 12px; }
.history-card .title { font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.history-card .meta { color: var(--muted); font-size: 12px; }
.history-card .bottom { margin-top: 10px; display: flex; gap: 10px; }

/* 过渡 */
.slide-enter-active, .slide-leave-active { transition: transform .18s ease, opacity .18s ease; }
.slide-enter-from, .slide-leave-to { transform: translateX(20px); opacity: 0; }

/* 滚动条 */
.left-pane::-webkit-scrollbar, .right-pane::-webkit-scrollbar, .history::-webkit-scrollbar { width: 10px; height: 10px; }
.left-pane::-webkit-scrollbar-thumb, .right-pane::-webkit-scrollbar-thumb, .history::-webkit-scrollbar-thumb { background: #23272e; border-radius: 8px; }
</style>
