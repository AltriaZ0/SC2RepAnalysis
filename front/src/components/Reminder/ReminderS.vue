<template>
  <div class="page">
    <!-- Toolbar -->
    <header class="toolbar">
      <h1 class="title">屏幕提醒</h1>
      <button class="btn" @click="reset">重置</button>
      <button class="btn" @click="saveToLocal">保存</button>
      <button class="btn primary" @click="toggleShow">
        {{ state.show ? '隐藏悬浮' : '显示悬浮' }} (Ctrl+Shift+S)
      </button>
    </header>

    <div class="content">
      <section class="left">
        <label class="label">提醒文字</label>
        <textarea
          v-model="state.text"
          class="textarea"
          rows="5"
          placeholder="在这里输入提醒文字…&#10;例如：今天 20:00 训练；喝水；保持热键连贯性。"
        />

        <div class="grid-2">
          <div>
            <label class="label">字体</label>
            <select v-model="state.font.family" class="input">
              <option value="Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, 'Apple Color Emoji', 'Segoe UI Emoji'">系统默认</option>
              <option value="'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace">等宽（JetBrains Mono）</option>
              <option value="'Noto Sans SC', 'Microsoft YaHei', 'PingFang SC', system-ui, sans-serif">思源黑体 / 微软雅黑</option>
            </select>
          </div>
          <div>
            <label class="label">粗细</label>
            <select v-model.number="state.font.weight" class="input">
              <option :value="400">Regular</option>
              <option :value="600">Semibold</option>
              <option :value="700">Bold</option>
              <option :value="800">ExtraBold</option>
            </select>
          </div>
        </div>

        <div class="grid-3">
          <div>
            <label class="label">字号：{{ state.font.size }} px</label>
            <input class="range" type="range" min="12" max="72" v-model.number="state.font.size" />
          </div>
          <div>
            <label class="label">字距：{{ state.style.letterSpacing.toFixed(1) }} px</label>
            <input class="range" type="range" min="-1" max="6" step="0.1" v-model.number="state.style.letterSpacing" />
          </div>
          <div>
            <label class="label">行高：{{ state.style.lineHeight.toFixed(2) }}</label>
            <input class="range" type="range" min="1" max="2" step="0.05" v-model.number="state.style.lineHeight" />
          </div>
        </div>

        <div class="grid-3">
          <div>
            <label class="label">文本颜色</label>
            <input class="input" type="color" v-model="state.colors.text" />
          </div>
          <div>
            <label class="label">背景颜色</label>
            <input class="input" type="color" v-model="state.colors.bg" />
          </div>
          <div>
            <label class="label">背景不透明度：{{ state.style.bgOpacity }}</label>
            <input class="range" type="range" min="0" max="1" step="0.05" v-model.number="state.style.bgOpacity" />
          </div>
        </div>

        <div class="grid-3">
          <div>
            <label class="label">顶部内边距：{{ state.style.paddingY }} px</label>
            <input class="range" type="range" min="4" max="32" step="1" v-model.number="state.style.paddingY" />
          </div>
          <div>
            <label class="label">左右内边距：{{ state.style.paddingX }} px</label>
            <input class="range" type="range" min="8" max="64" step="2" v-model.number="state.style.paddingX" />
          </div>
          <div>
            <label class="label">阴影</label>
            <select v-model="state.style.shadow" class="input">
              <option value="none">无</option>
              <option value="sm">浅</option>
              <option value="md">中</option>
              <option value="lg">重</option>
            </select>
          </div>
        </div>

        <div class="grid-3" style="margin-top: 12px;">
          <div>
            <label class="label">窗口宽度（px）</label>
            <input class="input" type="number" min="400" max="9999" v-model.number="state.window.width" />
          </div>
          <div>
            <label class="label">窗口高度（px）</label>
            <input class="input" type="number" min="40" max="600" v-model.number="state.window.height" />
          </div>
          <div>
            <label class="label">宽度模式</label>
            <select v-model="state.layout.width" class="input">
              <option value="full">全宽</option>
              <option value="center">居中（最大 960px）</option>
            </select>
          </div>
        </div>

        <div class="grid-3" style="margin-top: 12px;">
          <div>
            <label class="label">层级 z-index</label>
            <input class="input" type="number" v-model.number="state.layout.zIndex" min="10" max="999999" />
          </div>
          <div>
            <label class="label">交互</label>
            <select v-model="state.layout.pointer" class="input">
              <option value="auto">可点击</option>
              <option value="none">穿透（不拦截鼠标）</option>
            </select>
          </div>
          <div>
            <label class="label">启用 N 秒后闪烁</label>
            <select v-model="state.behavior.blinkEnabled" class="input">
              <option :value="true">启用</option>
              <option :value="false">禁用</option>
            </select>
          </div>
        </div>

        <div class="grid-3" style="margin-top: 12px;">
          <div>
            <label class="label">N 秒后开始闪烁：{{ state.behavior.blinkAfter }} s</label>
            <input class="range" type="range" min="10" max="600" step="5" v-model.number="state.behavior.blinkAfter" />
          </div>
          <div>
            <label class="label">（可选）闪烁持续秒数：{{ state.behavior.blinkDuration }} s</label>
            <input class="range" type="range" min="5" max="120" step="5" v-model.number="state.behavior.blinkDuration" />
          </div>
          <div style="display:flex;align-items:flex-end;">
            <span class="label">
              全局快捷键：
              <code>`</code> 重置闪烁倒计时
            </span>
          </div>
        </div>

        <div class="tips">
          快捷键：
          <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>S</kbd> 显示/隐藏；
          <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>↑/↓</kbd> 调整字号；
          <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>C</kbd> 复制当前文字；
          <code>`</code>（全局）重置即将闪烁的时间。
        </div>
      </section>

      <section class="right">
        <div class="preview-title">预览</div>
        <div class="preview">
          <div class="banner" :style="bannerStyle">
            {{ state.text || '（示例）保持心态平稳 · 注意热键 · 记得喝水' }}
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { WebviewWindow } from '@tauri-apps/api/webviewWindow'
import { LogicalSize } from '@tauri-apps/api/window'
import { emit } from '@tauri-apps/api/event'
import { register as registerShortcut, unregisterAll } from '@tauri-apps/plugin-global-shortcut'

const BANNER_LABEL = 'screen-banner'
let bannerWin: WebviewWindow | null = null

// ---------------- 状态 ----------------
const state = reactive({
  text: '',
  show: false,
  font: {
    size: 28,
    family: "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial",
    weight: 700
  },
  colors: { text: '#ffffff', bg: '#111827' },
  style: {
    letterSpacing: 0.2,
    lineHeight: 1.2,
    paddingX: 24,
    paddingY: 10,
    bgOpacity: 0.85,
    shadow: 'md' as 'none' | 'sm' | 'md' | 'lg',
  },
  layout: {
    width: 'full' as 'full' | 'center',
    zIndex: 99999,
    pointer: 'none' as 'none' | 'auto',
  },
  window: {
    width: 1920,
    height: 60,
  },
  behavior: {
    blinkEnabled: true,
    blinkAfter: 180,      // N 秒后开始闪烁
    blinkDuration: 30,    // 闪烁持续时间
  },
})

// 样式（发给预览 + 子窗口）
const bannerStyle = computed(() => ({
  color: state.colors.text,
  background: hexToRgba(state.colors.bg, state.style.bgOpacity),
  fontSize: state.font.size + 'px',
  fontFamily: state.font.family,
  fontWeight: String(state.font.weight),
  letterSpacing: state.style.letterSpacing + 'px',
  lineHeight: String(state.style.lineHeight),
  padding: `${state.style.paddingY}px ${state.style.paddingX}px`,
  boxShadow: shadowMap[state.style.shadow],
}))

const bannerWrapStyle = computed(() => ({
  position: 'fixed',
  top: '0', left: '0', right: '0',
  zIndex: String(state.layout.zIndex),
  pointerEvents: state.layout.pointer,
  display: 'flex',
  justifyContent: state.layout.width === 'full' ? 'stretch' : 'center',
}))

function emitUpdate() {
  emit('screen-banner:update', {
    text: state.text,
    style: bannerStyle.value,
    layout: {
      zIndex: state.layout.zIndex,
      pointer: state.layout.pointer,
      widthMode: state.layout.width,
    },
    window: {
      width: state.window.width,
      height: state.window.height,
    },
    behavior: {
      blinkEnabled: state.behavior.blinkEnabled,
      blinkAfter: state.behavior.blinkAfter,
      blinkDuration: state.behavior.blinkDuration,
    },
  })
}

// ---------------- 窗口管理 ----------------
async function openBannerWindow() {
  if (bannerWin) {
    try {
      await bannerWin.show()
      return
    } catch {
      bannerWin = null
    }
  }

  bannerWin = new WebviewWindow(BANNER_LABEL, {
    url: '/floating-banner',
    width: state.window.width,
    height: state.window.height,
    x: 0,
    y: 0,
    decorations: false,
    transparent: true,
    alwaysOnTop: true,
    resizable: false,
    focus: false,
    shadow: false
  })
  
  bannerWin.once('tauri://created', async () => {
    try {
      await bannerWin?.setIgnoreCursorEvents(true)
    } catch (e) {
      console.warn('setIgnoreCursorEvents failed', e)
    }
  })
  bannerWin.once('tauri://destroyed', () => {
    bannerWin = null
    state.show = false
  })
}

async function closeBannerWindow() {
  if (!bannerWin) return
  try {
    await bannerWin.close()
  } catch (err) {
    console.warn('close banner failed', err)
  } finally {
    bannerWin = null
  }
}

async function toggleShow() {
  state.show = !state.show

  if (state.show) {
    await openBannerWindow()
    // 打开后立刻发一次当前状态
    emitUpdate()
  } else {
    await closeBannerWindow()
  }
}

// 窗口尺寸变化时，同步给子窗口（如果已存在）
watch(
  () => [state.window.width, state.window.height],
  ([w, h]) => {
    if (bannerWin) {
      bannerWin.setSize(new LogicalSize(w, h))
      emitUpdate()
    }
  }
)

// ---------------- 工具 ----------------
const shadowMap: Record<string, string> = {
  none: 'none',
  sm: '0 1px 2px rgba(0,0,0,.25)',
  md: '0 6px 16px rgba(0,0,0,.35)',
  lg: '0 14px 28px rgba(0,0,0,.45)'
}

function hexToRgba(hex: string, a: number) {
  const m = hex.replace('#','')
  const full = m.length === 3 ? m.split('').map(ch => ch + ch).join('') : m
  const bigint = parseInt(full, 16)
  const r = (bigint >> 16) & 255
  const g = (bigint >> 8) & 255
  const b = bigint & 255
  return `rgba(${r}, ${g}, ${b}, ${a})`
}

function reset() {
  state.text = ''
  state.font.size = 28
  state.font.family = "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial"
  state.font.weight = 700
  state.colors.text = '#ffffff'
  state.colors.bg = '#111827'
  state.style.letterSpacing = 0.2
  state.style.lineHeight = 1.2
  state.style.paddingX = 24
  state.style.paddingY = 10
  state.style.bgOpacity = 0.85
  state.style.shadow = 'md'
  state.layout.width = 'full'
  state.layout.zIndex = 99999
  state.layout.pointer = 'none'
  state.window.width = 1920
  state.window.height = 60
  state.behavior.blinkEnabled = true
  state.behavior.blinkAfter = 180
  state.behavior.blinkDuration = 30
}

// 持久化（localStorage）
const STORE_KEY = 'screen-reminder-v1'
function saveToLocal() {
  localStorage.setItem(STORE_KEY, JSON.stringify(state))
}
function loadFromLocal() {
  try {
    const raw = localStorage.getItem(STORE_KEY)
    if (raw) Object.assign(state, JSON.parse(raw))
  } catch {}
}

// 快捷键（窗口内）
function onKey(e: KeyboardEvent) {
  if (!e.ctrlKey || !e.shiftKey) {
    // 单独按 ` 时，在当前窗口也重置闪烁时间
    if (e.code === 'Backquote') {
      emit('screen-banner:resetBlink')
    }
    return
  }
  if (e.code === 'KeyS') { e.preventDefault(); toggleShow() }
  if (e.code === 'ArrowUp') { e.preventDefault(); state.font.size = Math.min(96, state.font.size + 1) }
  if (e.code === 'ArrowDown') { e.preventDefault(); state.font.size = Math.max(10, state.font.size - 1) }
  if (e.code === 'KeyC') { e.preventDefault(); navigator.clipboard.writeText(state.text || '') }
}

// 生命周期
onMounted(async () => {
  loadFromLocal()
  window.addEventListener('keydown', onKey)

  // 全局快捷键：在 Windows 任意界面按 `，重置闪烁倒计时
  try {
    await registerShortcut('`', (event) => {
      console.log('global ` pressed in floating window')
      if (event.state === 'Pressed') {
        emit('screen-banner:resetBlink')
      }
    })
  } catch (err) {
    console.warn('register global shortcut failed', err)
  }
})

onUnmounted(() => {
  window.removeEventListener('keydown', onKey)
  unregisterAll().catch(() => {})
})

// 自动保存 + 同步到子窗口
watch(
  state,
  () => {
    saveToLocal()
    emitUpdate()
  },
  { deep: true }
)
</script>

<style scoped>
.page { display: flex; flex-direction: column; height: 100%; color: #e5e7eb; background: #0f1113; }
.toolbar h1 { font-size: 18px; font-weight: 700; }
.spacer { flex: 1; }
.title{ font-size:18px; margin:4px 4px; font-weight:700; }
.content {
  display:grid;
  grid-template-columns: 420px 1fr;
  gap:16px;
  padding:16px 20px;
  height: calc(100vh - 50px);
  margin-top: 50px;
  box-sizing:border-box;
  overflow:hidden;
}
.left, .right {
  background: #161a1f;
  border: 1px solid #23272e;
  border-radius: 14px;
  padding: 14px;
  overflow: auto;
}

.label { font-size: 12px; color: #a6adbb; margin-bottom: 6px; display: block; }
.input, .textarea, .range { width: 100%; box-sizing: border-box; }
.input, .textarea {
  background: #0f1317;
  color: #e5e7eb;
  border: 1px solid #2a2f36;
  border-radius: 10px;
  padding: 10px 12px;
}
.textarea { resize: vertical; }
.range { accent-color: #3b82f6; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 12px; }
.grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-top: 12px; }

.btn {
  border: 1px solid #2a2f36;
  background: #0f1317;
  color: #e5e7eb;
  padding: 4px 12px;
  border-radius: 10px;
  cursor: pointer;
}
.btn:hover { filter: brightness(1.1); }
.btn.primary { background: #3b82f6; border-color: transparent; color: white; }

.preview-title { font-size: 12px; color: #a6adbb; margin-bottom: 8px; }
.preview { border: 1px dashed #2a2f36; border-radius: 12px; padding: 10px; background: #0f1113; }
.banner { width: 100%; text-align: center; border-radius: 10px; }

/* 悬浮条容器（如果以后用 teleport） */
.floating-banner { position: fixed; top: 0; left: 0; right: 0; }

code { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
</style>
