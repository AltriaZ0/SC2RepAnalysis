<template>
  <div class="page">
    <!-- 顶部工具条 -->
    <header class="toolbar">
      <div class="left">
        <h1 class="title">流程练习</h1>
      </div>
      <!-- <div class="right">
        <button class="btn ghost" @click="toggleHistory">历史记录</button>
      </div> -->
    </header>

    <div class="content">
      <!-- 左：选择 .xlsx 与练习选项 -->
      <section class="left-pane">
        <div
          class="dropzone"
          :class="{ dragover }"
          @dragover.prevent="dragover = true"
          @dragleave.prevent="dragover = false"
          @drop.prevent="onDrop"
        >
          <div class="dz-inner">
            <svg class="dz-icon" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16.59 5.59 12 1 7.41 5.59 8.83 7l2.17-2.17V14h2V4.83L15.17 7 16.59 5.59zM19 10h-2v6H7v-6H5v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6z"/></svg>
            <p class="dz-title">拖拽 <span>.xlsx</span> 到此处</p>
            <p class="dz-sub">或 <button class="link" @click="pickFile">点击选择</button> 本地 Excel</p>
            <input ref="fileInput" class="hidden" type="file" accept=".xlsx" @change="onFile" />
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
            <div class="card-title">练习选项</div>
            <button class="btn ghost tiny" @click="resetOptions">重置</button>
          </div>
          <div class="options">
            <label class="opt"><input type="checkbox" v-model="opts.shuffle"/> 随机顺序</label>
            <label class="opt"><input type="checkbox" v-model="opts.loop"/> 循环播放/练习</label>
            <label class="opt"><input type="checkbox" v-model="opts.strictMode"/> 严格模式（必须正确才能进入下一步）</label>
            <label class="opt"><input type="checkbox" v-model="opts.audioCue"/> 声音提示</label>
          </div>

          <div class="row">
            <div class="col">
              <label class="label">题目范围</label>
              <select v-model="opts.range" class="select">
                <option value="all">全部</option>
                <option value="selected">当前筛选</option>
              </select>
            </div>
            <div class="col">
              <label class="label">每轮题量</label>
              <input class="input" v-model.number="opts.batch" type="number" min="1" max="200" />
            </div>
          </div>

          <div class="row">
            <div class="col">
              <label class="label">节奏（每步停留 ms）</label>
              <input class="input" v-model.number="opts.stepMs" type="number" min="300" step="100" />
            </div>
            <div class="col">
              <label class="label">显示字段</label>
              <select v-model="opts.columns" class="select" multiple size="4">
                <option value="id">编号 / ID</option>
                <option value="title">标题</option>
                <option value="detail">内容/步骤</option>
                <option value="tag">标签</option>
              </select>
            </div>
          </div>

          <div class="actions">
            <button class="btn primary" :disabled="!fileMeta || busy" @click="startPractice">{{ busy ? '准备中…' : '开始练习' }}</button>
            <button class="btn" :disabled="!started" @click="pauseResume">{{ paused ? '继续' : '暂停' }}</button>
            <button class="btn ghost" :disabled="!started" @click="stop">停止</button>
          </div>

          <div class="progress" v-if="started">
            <div class="bar" :style="{ width: percent + '%' }"></div>
          </div>
          <p class="hint" v-if="errorMsg">{{ errorMsg }}</p>
        </div>
      </section>

      <!-- 右：预览/当前练习 -->
      <section class="right-pane">
        <div class="card">
          <div class="card-header">
            <div class="card-title">预览/当前</div>
            <div class="card-sub" v-if="started">{{ currentIndex + 1 }} / {{ total }}</div>
          </div>
          <div class="practice">
            <div class="practice-block" v-if="started">
              <div class="title">{{ currentItem.title || '（无标题）' }}</div>
              <div class="detail" v-if="showColumn('detail')">{{ currentItem.detail || '——' }}</div>
              <div class="meta">
                <span v-if="showColumn('id')">#{{ currentItem.id }}</span>
                <span v-if="showColumn('tag')" class="tag">{{ currentItem.tag || 'untagged' }}</span>
              </div>
            </div>
            <div class="placeholder" v-else>
              <p class="muted">尚未开始练习</p>
              <p class="muted">选择一个 .xlsx 并设置练习选项后点击「开始练习」</p>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- 历史抽屉 -->
    <transition name="slide">
      <aside class="history" v-if="openHistory">
        <div class="history-header">
          <h2>历史记录</h2>
          <button class="btn ghost tiny" @click="openHistory = false">关闭</button>
        </div>
        <div class="history-list">
          <div v-for="h in history" :key="h.id" class="history-card">
            <div class="top">
              <div class="title" :title="h.file">{{ h.file }}</div>
              <div class="meta">{{ h.date }} · 题量 {{ h.count }}</div>
            </div>
            <div class="bottom">
              <button class="btn tiny" @click="restore(h)">恢复</button>
              <button class="btn ghost tiny" @click="removeHistory(h.id)">删除</button>
            </div>
          </div>
        </div>
      </aside>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'

// 选择文件
const dragover = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)
const fileMeta = ref<null | { name: string; size: number; mtime: string; path: string }>(null)

function pickFile() { fileInput.value?.click() }
function onFile(e: Event) {
  const f = (e.target as HTMLInputElement).files?.[0]; if (!f) return; attachFile(f)
}
function onDrop(e: DragEvent) {
  dragover.value = false; const f = e.dataTransfer?.files?.[0]; if (!f) return; attachFile(f)
}
function attachFile(f: File) {
  fileMeta.value = { name: f.name, size: f.size, mtime: new Date().toLocaleString(), path: (f as any).path || '本地 Excel' }
}
function clearFile() { fileMeta.value = null }

// 练习选项
const opts = reactive({
  shuffle: true,
  loop: false,
  strictMode: false,
  audioCue: false,
  range: 'all',
  batch: 20,
  stepMs: 1500,
  columns: ['title','detail','id','tag'] as string[],
})

function resetOptions() {
  opts.shuffle = true; opts.loop = false; opts.strictMode = false; opts.audioCue = false
  opts.range = 'all'; opts.batch = 20; opts.stepMs = 1500; opts.columns = ['title','detail','id','tag']
}

// 练习运行态
const busy = ref(false)
const started = ref(false)
const paused = ref(false)
const errorMsg = ref('')
const percent = ref(0)

const list = ref<any[]>([])
const total = computed(() => list.value.length)
const currentIndex = ref(0)
const currentItem = computed(() => list.value[currentIndex.value] || {})

function showColumn(c: string) { return opts.columns.includes(c) }

async function startPractice() {
  if (!fileMeta.value) return
  busy.value = true; errorMsg.value = ''
  try {
    // TODO: 读取 .xlsx -> 数组；这里用模拟数据
    list.value = mockLoad(opts.batch)
    if (opts.shuffle) list.value = shuffle(list.value)
    started.value = true; paused.value = false; percent.value = 0; currentIndex.value = 0
    tick()
  } catch (e: any) {
    errorMsg.value = e?.message || '初始化失败'
  } finally { busy.value = false }
}

function pauseResume() { paused.value = !paused.value; if (!paused.value) tick() }
function stop() { started.value = false; paused.value = false; percent.value = 0 }

function tick() {
  if (!started.value || paused.value) return
  // 前进一步
  percent.value = Math.round(((currentIndex.value + 1) / Math.max(1, total.value)) * 100)
  if (currentIndex.value < total.value - 1) {
    setTimeout(() => { if (!paused.value && started.value) { currentIndex.value++; tick() } }, opts.stepMs)
  } else if (opts.loop) {
    currentIndex.value = 0; setTimeout(() => tick(), opts.stepMs)
  }
}

// 历史
const openHistory = ref(false)
const history = ref<any[]>([
  { id: 'h1', file: '训练题-流程手册.xlsx', date: '2025/11/06', count: 120, opts: JSON.parse(JSON.stringify(opts)) },
])
function toggleHistory() { openHistory.value = !openHistory.value }
function restore(h: any) { Object.assign(opts, h.opts); openHistory.value = false }
function removeHistory(id: string) { history.value = history.value.filter(i => i.id !== id) }

// 辅助
function prettySize(size: number) { if (size < 1024) return size + ' B'; if (size < 1024 * 1024) return (size/1024).toFixed(1)+' KB'; return (size/1024/1024).toFixed(2)+' MB' }

function shuffle<T>(arr: T[]) { return [...arr].sort(() => Math.random() - 0.5) }
function mockLoad(n: number) {
  return Array.from({length: n}).map((_, i) => ({ id: i+1, title: `步骤 ${i+1}`, detail: `这是第 ${i+1} 步的说明……`, tag: i%2? 'A':'B' }))
}
</script>

<style scoped>

.page { display:flex; flex-direction:column; height:100%; background:var(--bg); color:var(--text); }
/* .toolbar { display:flex; align-items:center; justify-content:space-between; padding:14px 20px; border-bottom:1px solid var(--border); background:#0e1012; position:sticky; top:0; z-index:2; } */
.title{ font-size:18px; margin:4px 4px; font-weight:700; }
.content { display:grid;
      grid-template-columns: 420px 1fr; 
      gap:16px; 
      padding:16px 20px;
      height: calc(100vh - 50px);
      margin-top: 50px;   
      box-sizing:border-box;
      overflow:hidden; }
.left-pane, .right-pane { height:100%; overflow:auto; padding-right:6px; }

.dropzone { border:1.5px dashed var(--border); background:var(--panel-2); border-radius:16px; padding:26px; text-align:center; transition:.15s ease; }
.dropzone.dragover { border-color:var(--primary); background:#101318; box-shadow:0 0 0 3px rgba(59,130,246,.12) inset; }
.dz-inner{ display:grid; gap:6px; place-items:center; }
.dz-icon{ width:44px; height:44px; color:var(--muted); }
.dz-title{ font-weight:600; }
.dz-title span{ color:var(--primary); }
.dz-sub{ color:var(--muted); }
.hidden{ display:none; }
.link{ color:var(--primary); background:transparent; border:none; cursor:pointer; padding:0; }

.card { background: var(--panel); border:1px solid var(--border); border-radius:16px; padding:14px; margin-top:12px; }
.card-header { display:flex; align-items:center; justify-content:space-between; gap:10px; margin-bottom:8px; }
.card-title { font-weight:700; }
.card-sub { color:var(--muted); font-size:12px; }
.file-name { font-weight:600; max-width: calc(100% - 80px); overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.meta { list-style:none; padding:0; margin:0; display:grid; gap:6px; }
.meta li { display:flex; justify-content:space-between; border-bottom:1px dashed var(--border); padding:6px 0; }
.meta li:last-child{ border-bottom:none; }
.truncate{ overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }

.options { display:grid; grid-template-columns: 1fr; gap:8px; margin:8px 0 10px; }
.opt { display:flex; align-items:center; gap:8px; user-select:none; }
.row { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:6px; }
.col { display:flex; flex-direction:column; gap:6px; }
.label{ color:var(--muted); font-size:12px; }
.input, .select { background:#0f1317; border:1px solid var(--border); color:var(--text); padding:8px 10px; border-radius:10px; }

.actions { display:flex; gap:10px; margin-top:12px; }
.btn { border:1px solid var(--border); background:#0f1317; color:var(--text); padding:8px 12px; border-radius:10px; cursor:pointer; transition:.15s ease; }
.btn:hover { filter:brightness(1.1); }
.btn:disabled { opacity:.5; cursor:not-allowed; }
.btn.primary{ background:var(--primary); border-color:transparent; color:white; }
.btn.ghost{ background:transparent; }
.btn.tiny{ padding:6px 10px; font-size:12px; border-radius:8px; }

.progress { height:8px; border-radius:999px; background:#0f1317; border:1px solid var(--border); overflow:hidden; margin-top:10px; }
.progress .bar { height:100%; background: linear-gradient(90deg, var(--primary), #67a3ff); width:0%; transition: width .2s ease; }
.hint { color:#fca5a5; margin-top:8px; }
.muted { color:var(--muted); }
.placeholder { display:grid; place-items:center; height:180px; gap:8px; }

.practice .title{ font-size:22px; font-weight:700; }
.practice .detail{ margin-top:8px; color:#cdd3df; }
.practice .meta{ margin-top:10px; display:flex; gap:10px; color:#a6adbb; font-size:12px; }
.practice .tag{ background:#0f1317; border:1px solid var(--border); padding:2px 6px; border-radius:999px; }

/* 历史抽屉 */
.history { position: fixed; right: 0; top: 60px; bottom: 0; width: 420px; background: #0e1012; border-left: 1px solid var(--border); padding: 14px; overflow: auto; }
.history-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }
.history-list{ display:grid; gap:10px; }
.history-card { background: var(--panel); border:1px solid var(--border); border-radius:14px; padding:12px; }
.history-card .top { display:flex; justify-content:space-between; gap:12px; }
.history-card .title { font-weight:600; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.history-card .meta { color:var(--muted); font-size:12px; }
.history-card .bottom { margin-top:10px; display:flex; gap:10px; }

/* 过渡 */
.slide-enter-active, .slide-leave-active { transition: transform .18s ease, opacity .18s ease; }
.slide-enter-from, .slide-leave-to { transform: translateX(20px); opacity: 0; }
</style>
