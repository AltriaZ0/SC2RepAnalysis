<template>
  <div class="page">
    <!-- 顶部工具条 -->
    <header class="toolbar">
      <div class="left">       <h1 class="title">设置</h1> </div>

      <div class="spacer" />
      <button class="btn" @click="importConfig">导入配置</button>
      <button class="btn" @click="exportConfig">导出配置</button>
      <button class="btn" @click="resetAll">恢复默认</button>
      <button class="btn primary" @click="saveAll">保存</button>
    </header>

    <div class="content">
      <!-- 左：分类导航 -->
      <aside class="side">
        <ul class="nav">
          <li v-for="s in sections" :key="s.key" :class="{ active: active===s.key }" @click="active=s.key">{{ s.name }}</li>
        </ul>
      </aside>

      <!-- 右：设置内容 -->
      <main class="main">
        <!-- 通用 -->
        <section v-if="active==='general'" class="card">
          <div class="card-header"><div class="card-title">通用</div></div>
          <div class="grid-3">
            <div>
              <label class="label">界面语言</label>
              <select v-model="cfg.general.language" class="input">
                <option value="zh">中文</option>
                <option value="en">English</option>
              </select>
            </div>
            <div>
              <label class="label">主题</label>
              <select v-model="cfg.general.theme" class="input">
                <option value="system">跟随系统</option>
                <option value="dark">深色</option>
                <option value="light">浅色</option>
              </select>
            </div>
            <div>
              <label class="label">日期格式</label>
              <select v-model="cfg.general.dateFormat" class="input">
                <option value="YYYY/MM/DD">YYYY/MM/DD</option>
                <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                <option value="MM/DD/YYYY">MM/DD/YYYY</option>
              </select>
            </div>
          </div>
          <div class="grid-3">
            <div>
              <label class="label">启动时打开</label>
              <select v-model="cfg.general.startupPage" class="input">
                <option value="home">首页</option>
                <option value="single">单文件分析</option>
                <option value="batch">批量分析</option>
                <option value="practice">流程练习</option>
                <option value="reminder">屏幕提醒</option>
              </select>
            </div>
            <div>
              <label class="label">自动保存设置</label>
              <select v-model.number="cfg.general.autosaveSec" class="input">
                <option :value="0">关闭</option>
                <option :value="5">5 秒</option>
                <option :value="15">15 秒</option>
                <option :value="30">30 秒</option>
                <option :value="60">60 秒</option>
              </select>
            </div>
            <div>
              <label class="label">检查更新</label>
              <select v-model="cfg.general.updateChannel" class="input">
                <option value="stable">稳定版</option>
                <option value="beta">测试版</option>
                <option value="off">关闭</option>
              </select>
            </div>
          </div>
        </section>

        <!-- 数据与目录 -->
        <section v-if="active==='paths'" class="card">
          <div class="card-header"><div class="card-title">数据与目录</div></div>
          <div class="grid-1">
            <div class="row-line">
              <div class="grow">
                <label class="label">重放文件目录（SC2Replay）</label>
                <input class="input" v-model="cfg.paths.replayDir" placeholder="选择或输入目录路径"/>
              </div>
              <button class="btn" @click="pickDir('replayDir')">选择</button>
            </div>
            <div class="row-line">
              <div class="grow">
                <label class="label">导出目录（Excel/日志）</label>
                <input class="input" v-model="cfg.paths.exportDir" placeholder="选择或输入目录路径"/>
              </div>
              <button class="btn" @click="pickDir('exportDir')">选择</button>
            </div>
            <div class="row-line">
              <div class="grow">
                <label class="label">缓存目录</label>
                <input class="input" v-model="cfg.paths.cacheDir" placeholder="选择或输入目录路径"/>
              </div>
              <button class="btn" @click="pickDir('cacheDir')">选择</button>
            </div>
          </div>
          <div class="grid-3">
            <div>
              <label class="label">最大缓存大小 (MB)</label>
              <input type="number" class="input" v-model.number="cfg.paths.cacheLimitMB" min="64" step="64"/>
            </div>
            <div>
              <label class="label">日志级别</label>
              <select class="input" v-model="cfg.paths.logLevel">
                <option value="info">info</option>
                <option value="debug">debug</option>
                <option value="warn">warn</option>
                <option value="error">error</option>
              </select>
            </div>
            <div>
              <label class="label">保留天数</label>
              <input type="number" class="input" v-model.number="cfg.paths.retentionDays" min="1"/>
            </div>
          </div>
        </section>

        <!-- 分析默认值 -->
        <section v-if="active==='analysis'" class="card">
          <div class="card-header"><div class="card-title">分析默认选项</div></div>
          <div class="options">
            <label class="opt"><input type="checkbox" v-model="cfg.analysis.basic"/> 基本信息</label>
            <label class="opt"><input type="checkbox" v-model="cfg.analysis.bo"/> Build Order</label>
            <label class="opt"><input type="checkbox" v-model="cfg.analysis.actions"/> APM/Actions</label>
            <label class="opt"><input type="checkbox" v-model="cfg.analysis.units"/> 单位与升级统计</label>
            <label class="opt"><input type="checkbox" v-model="cfg.analysis.mapheat"/> 地图事件热力</label>
            <label class="opt"><input type="checkbox" v-model="cfg.analysis.exportXlsx"/> 导出 Excel</label>
          </div>
          <div class="grid-3">
            <div>
              <label class="label">并发度</label>
              <select class="input" v-model.number="cfg.analysis.workers">
                <option :value="1">1</option>
                <option :value="2">2</option>
                <option :value="3">3</option>
                <option :value="4">4</option>
              </select>
            </div>
            <div>
              <label class="label">语言</label>
              <select class="input" v-model="cfg.analysis.lang">
                <option value="zh">中文</option>
                <option value="en">English</option>
              </select>
            </div>
            <div>
              <label class="label">时区</label>
              <select class="input" v-model="cfg.analysis.tz">
                <option value="local">本地</option>
                <option value="UTC">UTC</option>
              </select>
            </div>
          </div>
        </section>

        <!-- 提醒与通知 -->
        <section v-if="active==='reminder'" class="card">
          <div class="card-header"><div class="card-title">提醒与通知</div></div>
          <div class="options">
            <label class="opt"><input type="checkbox" v-model="cfg.reminder.enableBanner"/> 启用屏幕顶部提醒（与“屏幕提醒”页联动）</label>
            <label class="opt"><input type="checkbox" v-model="cfg.reminder.sound"/> 完成分析时播放提示音</label>
            <label class="opt"><input type="checkbox" v-model="cfg.reminder.systemNotif"/> 使用系统通知（仅桌面端）</label>
          </div>
          <div class="grid-3">
            <div>
              <label class="label">提示音音量</label>
              <input type="range" min="0" max="1" step="0.05" v-model.number="cfg.reminder.volume" />
            </div>
            <div>
              <label class="label">提醒默认文本</label>
              <input class="input" v-model="cfg.reminder.defaultText" placeholder="如：保持手速，注意补农"/>
            </div>
            <div>
              <label class="label">自动隐藏（秒）</label>
              <input class="input" type="number" v-model.number="cfg.reminder.autoHideSec" min="0" />
            </div>
          </div>
        </section>

        <!-- 快捷键 -->
        <section v-if="active==='shortcuts'" class="card">
          <div class="card-header"><div class="card-title">快捷键</div></div>
          <div class="grid-1">
            <div class="row-line">
              <span class="key">Ctrl+Shift+S</span>
              <span class="desc">显示/隐藏 屏幕提醒</span>
              <button class="btn ghost tiny" disabled>修改</button>
            </div>
            <div class="row-line">
              <span class="key">Ctrl+F</span>
              <span class="desc">聚焦搜索</span>
              <button class="btn ghost tiny" disabled>修改</button>
            </div>
            <div class="row-line">
              <span class="key">Ctrl+Shift+B</span>
              <span class="desc">开始批量分析</span>
              <button class="btn ghost tiny" disabled>修改</button>
            </div>
          </div>
          <p class="muted">（如需系统级快捷键，在 Tauri 中需要注册全局热键）</p>
        </section>

        <!-- 隐私与遥测 -->
        <section v-if="active==='privacy'" class="card">
          <div class="card-header"><div class="card-title">隐私与遥测</div></div>
          <div class="options">
            <label class="opt"><input type="checkbox" v-model="cfg.privacy.telemetry"/> 允许匿名使用数据（帮助我们改进产品）</label>
            <label class="opt"><input type="checkbox" v-model="cfg.privacy.crashReport"/> 允许发送崩溃报告</label>
            <label class="opt"><input type="checkbox" v-model="cfg.privacy.autoClean"/> 启动时自动清理旧日志/缓存</label>
          </div>
        </section>

        <!-- 备份与重置 -->
        <section v-if="active==='backup'" class="card">
          <div class="card-header"><div class="card-title">备份与重置</div></div>
          <div class="grid-1">
            <div class="row-line">
              <span>备份当前设置到文件</span>
              <button class="btn" @click="exportConfig">导出配置</button>
            </div>
            <div class="row-line">
              <span>从文件恢复设置</span>
              <button class="btn" @click="importConfig">导入配置</button>
            </div>
            <div class="row-line">
              <span>恢复默认设置（不可撤销）</span>
              <button class="btn danger" @click="resetAll">恢复默认</button>
            </div>
          </div>
        </section>
      </main>
    </div>

    <input ref="fileImport" class="hidden" type="file" accept="application/json" @change="onImportFile" />
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, watch, onMounted } from 'vue'

const sections = [
  { key: 'general', name: '通用' },
  { key: 'paths', name: '数据与目录' },
  { key: 'analysis', name: '分析默认' },
  { key: 'reminder', name: '提醒与通知' },
  { key: 'shortcuts', name: '快捷键' },
  { key: 'privacy', name: '隐私' },
  { key: 'backup', name: '备份与重置' },
]
const active = ref<'general'|'paths'|'analysis'|'reminder'|'shortcuts'|'privacy'|'backup'>('general')

// 默认配置
function defaultConfig() {
  return {
    general: { language: 'zh', theme: 'system', dateFormat: 'YYYY/MM/DD', startupPage: 'home', autosaveSec: 15, updateChannel: 'stable' },
    paths: { replayDir: '', exportDir: '', cacheDir: '', cacheLimitMB: 512, logLevel: 'info', retentionDays: 7 },
    analysis: { basic: true, bo: true, actions: true, units: true, mapheat: false, exportXlsx: true, workers: 2, lang: 'zh', tz: 'local' },
    reminder: { enableBanner: false, sound: false, systemNotif: false, volume: 0.6, defaultText: '', autoHideSec: 0 },
    shortcuts: {},
    privacy: { telemetry: false, crashReport: true, autoClean: true },
  }
}

const cfg = reactive(defaultConfig())

// 保存/加载
const STORE_KEY = 'app-settings-v1'
function saveAll() {
  localStorage.setItem(STORE_KEY, JSON.stringify(cfg))
}
function loadAll() {
  try { const raw = localStorage.getItem(STORE_KEY); if (raw) Object.assign(cfg, JSON.parse(raw)) } catch {}
}
function resetAll() { Object.assign(cfg, defaultConfig()); saveAll() }

// 导出/导入
function exportConfig() {
  const blob = new Blob([JSON.stringify(cfg, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a'); a.href = url; a.download = 'settings.json'; a.click(); URL.revokeObjectURL(url)
}
const fileImport = ref<HTMLInputElement|null>(null)
function importConfig() { fileImport.value?.click() }
function onImportFile(e: Event) {
  const f = (e.target as HTMLInputElement).files?.[0]; if (!f) return
  const reader = new FileReader(); reader.onload = () => { try { Object.assign(cfg, JSON.parse(String(reader.result))); saveAll() } catch {} }
  reader.readAsText(f)
}

// 选择目录（Tauri/浏览器占位）
async function pickDir(key: 'replayDir'|'exportDir'|'cacheDir') {
  // 在 Tauri 中可使用：
  // const { open } = await import('@tauri-apps/plugin-dialog');
  // const dir = await open({ directory: true, multiple: false })
  // if (dir) (cfg.paths as any)[key] = String(dir)
  const dir = prompt('输入目录路径：')
  if (dir) (cfg.paths as any)[key] = dir
}

onMounted(() => {
  loadAll()
  if (cfg.general.autosaveSec > 0) setInterval(saveAll, cfg.general.autosaveSec * 1000)
})

watch(cfg, () => { /* 可在此节流自动保存 */ }, { deep: true })
</script>

<style scoped>
.page{ display:flex; flex-direction:column; height:100%; background:var(--bg); color:var(--text); }
/* .toolbar{ display:flex; align-items:center; gap:10px; padding:14px 20px; border-bottom:1px solid var(--border); background:#0e1012; } */
.title{ font-size:18px; margin:4px 4px; font-weight:700; }
.spacer{ flex:1; }
.content{
 display:grid; 
 grid-template-columns: 240px 1fr; 
 gap:14px; padding:14px 16px; 
 height: calc(100vh - 50px); 
 margin-top: 50px;
 box-sizing:border-box;
  overflow:hidden; }
.side{ background:#0e1012; border:1px solid var(--border); border-radius:12px; padding:8px; overflow:auto; }
.nav{ list-style:none; padding:0; margin:0; display:grid; gap:6px; }
.nav li{ padding:10px 12px; border-radius:10px; cursor:pointer; color:#c7d0df; }
.nav li:hover{ background:#15181d; }
.nav li.active{ background:#1d2330; color:white; }
.main{ overflow:auto; padding-right:6px; }

.card{ background:var(--panel); border:1px solid var(--border); border-radius:16px; padding:14px; margin-bottom:12px; }
.card-header{ display:flex; align-items:center; justify-content:space-between; margin-bottom:8px; }
.card-title{ font-weight:700; }

.grid-1{ display:grid; gap:10px; }
.grid-3{ display:grid; grid-template-columns: repeat(3,1fr); gap:10px; }
.row-line{ display:flex; align-items:center; gap:10px; }
.row-line .grow{ flex:1; }

.label{ color:var(--muted); font-size:12px; margin-bottom:6px; display:block; }
.input{ background:#0f1317; border:1px solid var(--border); color:var(--text); padding:8px 10px; border-radius:10px; width:100%; box-sizing:border-box; }
.options{ display:grid; gap:8px; margin:8px 0 10px; }
.opt{ display:flex; gap:8px; align-items:center; }

.btn{ border:1px solid var(--border); background:#0f1317; color:var(--text); padding:8px 12px; border-radius:10px; cursor:pointer; }
.btn:hover{ filter:brightness(1.1); }
.btn.primary{ background:var(--primary); border-color:transparent; color:white; }
.btn.ghost{ background:transparent; }
.btn.danger{ background:#ef4444; border-color:transparent; color:white; }

.hidden{ display:none; }
.muted{ color:var(--muted); }
</style>
