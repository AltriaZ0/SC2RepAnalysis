<template>
  <div class="page">
    <!-- 顶部工具条 -->
    <header class="toolbar">
      <div class="left">
        <h1 class="title">单文件分析</h1>
      </div>
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
            <p class="dz-title">拖拽 <span>.SC2Replay</span> 到此处</p>
            <p class="dz-sub">或 <button class="link" @click="pickFile">点击选择</button> 本地文件</p>
            <input ref="fileInput" class="hidden" type="file" accept=".SC2Replay,.sc2replay" @change="onFile" />
          </div>
        </div>

        <div class="card" v-if="fileMeta">
          
          <div class="card-header">
             <div class="file-name">录像信息</div>
            <button class="btn tiny" @click="clearFile">移除</button>
          </div>
          <ul class="meta">
            <li><span clss="left" >名称</span><span clss="right">{{ fileMeta.name }}</span></li>
            <li><span clss="left">大小</span><span clss="right">{{ prettySize(fileMeta.size) }}</span></li>
            <li><span clss="left">修改时间</span><span clss="right">{{ fileMeta.mtime }}</span></li>
            <!-- <li><span>路径</span><span class="truncate" :title="fileMeta.path">{{ fileMeta.path }}</span></li> -->
          </ul>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-title">分析选项</div>
            <button class="btn ghost tiny" @click="resetOptions">重置</button>
          </div>
          <div class="options">
            <label class="opt"><input type="checkbox" v-model="opts.basic"/>只统计有事件发生的时间</label>
            <label class="opt"><input type="checkbox" v-model="opts.bo"/> 提醒建造后取消的信息 </label>
            <label class="opt"><input type="checkbox" v-model="opts.actions"/> 建筑建造统计 </label>
            <label class="opt"><input type="checkbox" v-model="opts.actions"/> 科技升级统计 </label>
            <label class="opt"><input type="checkbox" v-model="opts.units"/> 单位建造统计 </label>
            <label class="opt"><input type="checkbox" v-model="opts.units"/> 不统计Terran的建筑移动 </label>
            <label class="opt"><input type="checkbox" v-model="opts.mapheat"/> 农民数量统计(demo) </label>
            <label class="opt"><input type="checkbox" v-model="opts.exportXlsx"/> 导出 Excel（.xlsx）</label>
            <label class="opt"><input type="checkbox" /> 导出 txt（旧功能）</label>
          </div>
          <!-- <div class="row">
            <div class="col">
              <label class="label">精确过滤</label>
              <select v-model="opts.tz" class="select">
                <option value="local">忽略菌毯</option>
                <option value="UTC">忽略农民建造</option>
              </select>
            </div>
            <div class="col">
              <label class="label">语言</label>
              <select v-model="opts.lang" class="select">
                <option value="zh">中文</option>
                <option value="en">English</option>
              </select>
            </div>
          </div> -->

          <div class="actions">
            <button class="btn primary" :disabled="!fileMeta || busy" @click="startAnalyze">
              {{ busy ? '分析中…' : '开始分析' }}
            </button>
            <button class="btn success" :disabled="!fileMeta  || !result || busy" @click="openExportDir">打开导出目录</button>
            <!-- <button class="btn" :disabled="!fileMeta || busy" @click="quickPreview">快速预览</button> -->
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

      <div  v-else class="result">
        <!-- 概览卡片 -->
        <div  class="card">
          <div class="card-header">
            <div class="card-title">比赛概览</div>
          </div>
          <div class="overview-grid">
            <div class="kv"><span>地图</span><div class="ovt">{{ result.map_name }}</div></div>
            <div class="kv"><span>区域</span><div class="ovt">{{ result.region }}</div></div>
            <div class="kv"><span>时长</span><div class="ovt">{{ formatDuration(result.duration) }}</div></div>
            <div class="kv"><span>胜者</span><div class="ovt">{{ result.winner }}</div></div>
            <div class="kv"><span>对阵</span><div class="ovt">{{ result.raceBattle }}</div></div>
            <div class="kv" v-if="result.endTime"><span>结束时间</span><div class="ovt">{{ result.endTime }}</div></div>
          </div>
        </div>

        <div v-for="(info, name) in result.playersInfo"
          :key="name"
        >
          <div class="card-header">
            <div class="card-title">
              {{ name }}
              <span class="muted">({{ info.race }})</span>
            </div>
            <b :class="{ win: info.result, loss: !info.result }">
              {{ info.result ? '胜利' : '失败' }}
            </b>
          </div>
          
          <BuildBox :title=name :race=info.race :outputPath=info.outputPath :result=info.result :content="info.buildOrder" /> 
          
         </div>

      </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onBeforeUnmount } from 'vue'
import { invoke } from '@tauri-apps/api/core'
import { listen, UnlistenFn } from '@tauri-apps/api/event'
import { open } from '@tauri-apps/plugin-dialog'
import {appDataDir} from '@tauri-apps/api/path'
import BuildBox from './BuildBox.vue'
import { openPath } from '@tauri-apps/plugin-opener';

const dragover = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

const fileMeta = ref<null | { name: string; size: number; mtime: string; path: string }>(null)
const busy = ref(false)
const progress = ref(0)
const errorMsg = ref('')

const opts = reactive({
  analyze_type: "alone",
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

// 结果占位类型
interface BoStep {
  t: string
  action: string
}

interface PlayerInfo {
  race: string
  result: boolean
  buildOrder: BoStep[]
  outputPath: string
}

interface AnalyzeResult {
  map_name: string
  ladder?: boolean
  duration: number
  playersInfo: Record<string, PlayerInfo>
  winner: string
  region: string
  endTime?: string
  raceBattle: string
  output: string
}
const result = ref<AnalyzeResult | null>(null)

function formatDuration(sec: number) {
  const m = Math.floor(sec / 60)
  const s = sec % 60
  return `${m}:${s.toString().padStart(2, '0')}`
}

function copyBO(player: string) {

}


async function openExportDir() {
  console.log("result.value.playersInfo.output_dir:",result.value.output)
  const exportDir = result.value.output
  try {
    await openPath(exportDir);
    console.log("已打开导出目录:", exportDir)
  } catch (e) {
    console.error("打开目录失败:", e)
  }
  console.log('open export dir') 
}

async function pickFile() {
  const selected = await open({
    multiple: false,
    filters: [
      { name: 'SC2 Replay', extensions: ['SC2Replay', 'sc2replay'] }
    ]
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
  opts.analyze_type = "alone"
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
  // TODO：实现监听 Rust 侧发来的进度事件
  // unlisten = await listen<{ percent: number }>('analyze_progress', (e) => {
  //   progress.value = Math.max(progress.value, Math.min(99, e.payload.percent ?? 0))
  // })

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
    console.log("fileMeta.value",fileMeta.value)
    console.log("opts:",opts)
    const res = await invoke<AnalyzeResult>('analyze_replay', {
      path: fileMeta.value.path,
      options: {...opts }
    })
    progress.value = 100
    result.value = res
    console.log("result.value:",result.value)
    console.log("result.value.buildOrder:",result.value.playersInfo.buildOrder)
  } catch (e: any) {
    errorMsg.value = e?.message || '分析失败，请稍后重试'
    console.log(e)
  } finally {
    busy.value = false
  }
}

function prettySize(size: number) {
  if (size < 1024) return size + ' B'
  if (size < 1024 * 1024) return (size / 1024).toFixed(1) + ' KB'
  return (size / 1024 / 1024).toFixed(2) + ' MB'
}

</script>

<style scoped>


.page { display: flex; flex-direction: column; height: 100%; background: var(--bg); color: var(--text); }
.title { font-size: 18px; margin: 4px 4px; font-weight: 700; }
.toolbar .right { display: flex; align-items: center; gap: 10px; }

.search-box { display: flex; align-items: center; gap: 8px; background: var(--panel); border: 1px solid var(--border); padding: 8px 10px; border-radius: 12px; width: 320px; }
.search-box .icon { width: 18px; height: 18px; color: var(--muted); }
.search-box input { background: transparent; border: none; outline: none; color: var(--text); width: 100%; }

.content {
  margin-top: 50px;
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: 4px;
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

.card { 
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 12px;
  margin: 12px 4px; 
}
.card-header {
  display: flex; 
  align-items: center; 
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 8px; 
}
.card-title {
  font-weight: 700;
  margin: 0px;
  padding: 0px;
  font-size: 18px;
} 
.card-sub { color: var(--muted); font-size: 12px; }
.file-name { font-weight: 600; max-width: calc(100% - 80px); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.meta {
list-style: none;
padding: 0;
margin: 0; 
display: grid;
border-top: 1px solid #2b2e35;
}
.meta li { 
  display: flex; 
  align-items: center;
  justify-content: flex-start; 
  border-bottom: 1px dashed var(--border);
  padding: 6px 0; 
  column-gap: 16px;
}
.meta span{ 
  color: var(--muted);
  font-size: 14px;
  padding: 1px;
}

.meta li span:first-child {
  flex: 0 0 50px;
  white-space: nowrap;       /* 不允许换行 */
  color: #a0a0a0;
}

.meta li span:last-child {
  flex: 1 1 auto;
  text-align: right;          /* 右对齐 */
  word-break: break-all;     /* 自动换行 */
}
.truncate {
font-size: 12px;
overflow:scroll;
text-overflow: ellipsis;
 white-space: nowrap; 
}

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
.muted {
   color: var(--muted); 
   font-size: 13px;
}

.result { 
  display: grid; 
  gap: 2px; 
}
.overview-grid { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 10px; }
.kv { background: #111418; border: 1px solid var(--border); border-radius: 12px; padding: 12px; display: flex; flex-direction: column; gap: 6px; }
.kv span { color: var(--muted); font-size: 12px; }
.kv b { font-size: 16px; }
.kv b.win { color: var(--success); }

.bo-list { margin: 0; padding-left: 18px; display: grid; gap: 6px; }
.bo-list .time { color: var(--muted); margin-right: 10px; }

.export-row { display: flex; align-items: center; gap: 10px; }


/* 过渡 */
.slide-enter-active, .slide-leave-active { transition: transform .18s ease, opacity .18s ease; }
.slide-enter-from, .slide-leave-to { transform: translateX(20px); opacity: 0; }

/* 滚动条 */
.left-pane::-webkit-scrollbar, .right-pane::-webkit-scrollbar{ width: 10px; height: 10px; }
.left-pane::-webkit-scrollbar-thumb, .right-pane::-webkit-scrollbar-thumb { background: #23272e; border-radius: 8px; }

.player-card .card-header {
  justify-content: space-between; 
}

b.win {
  color: var(--success);
  padding: 0px 10px;
}
b.loss {
  color: #f87171;
  padding: 0px 10px;
}

.ovt{
  font-size: 14px;
  font-weight: 500;
}

</style>
