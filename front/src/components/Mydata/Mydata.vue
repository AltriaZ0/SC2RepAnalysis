<template>
  <div class="toolbar">

    <input v-model.trim="q" placeholder="搜索（标题/地图/玩家）" class="input" />

    <select v-model="race" class="select">
      <option value="">全部种族</option>
      <option value="Zerg">Zerg</option>
      <option value="Terran">Terran</option>
      <option value="Protoss">Protoss</option>
    </select>

    <select v-model="result" class="select">
      <option value="">全部结果</option>
      <option value="胜">胜利</option>
      <option value="负">失败</option>
    </select>

    <!-- <input type="date" v-model="dateStart" class="input" />
    <span>至</span>
    <input type="date" v-model="dateEnd" class="input" /> -->

    <select v-model="sortKey" class="select">
      <option value="date">按日期</option>
      <option value="title">按标题</option>
      <option value="map">按地图</option>
      <option value="race">按种族</option>
      <option value="result">按结果</option>
    </select>

    <button class="btn" @click="sortAsc = !sortAsc">
      {{ sortAsc ? '升序' : '降序' }}
    </button>
  </div>

  <div class="content">
    <card
      v-for="file in viewList"
      :key="file.path"
      :title="file.title"
      :map-name="file.map"
      :race="file.race"
      :date="file.date"
      :result="file.result"
      :xlsx-path="file.path"
    />
  </div>
</template>

<script setup lang="ts">
import card from '../../components/widget/Data_card.vue';
import guidebar from '../../components/widget/searchBox.vue';
import { readDir, createDir, exists } from '@tauri-apps/plugin-fs'
import { join,appDataDir,  resolveResource, BaseDirectory} from '@tauri-apps/api/path'
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'


// 响应式状态
const q = ref('')             // 关键字
const race = ref('')          // Zerg / Terran / Protoss / ''
const result = ref('')        // 胜利 / 失败 / ''
const dateStart = ref<string>('') // 'YYYY-MM-DD'
const dateEnd   = ref<string>('') // 'YYYY-MM-DD'

const sortKey = ref<'date'|'title'|'mapName'|'race'|'result'>('date')
const sortAsc = ref(false)


const toDate = (s: string) => (s ? new Date(s) : null)
const contains = (hay: string, needle: string) =>
  hay.toLowerCase().includes(needle.toLowerCase())

// 过滤 + 排序
const viewList = computed(() => {
  let arr = xlsxFiles.value

  // 过滤
  if (q.value) {
    arr = arr.filter(it =>
      contains(it.title, q.value) ||
      contains(it.map, q.value) ||
      contains(it.race, q.value)
    )
  }
  if (race.value) {
    arr = arr.filter(it => it.race === race.value)
  }
  if (result.value) {
    arr = arr.filter(it => it.result === result.value)
  }
  if (dateStart.value || dateEnd.value) {
    const s = toDate(dateStart.value)
    const e = toDate(dateEnd.value)
    arr = arr.filter(it => {
      const d = toDate(it.date)
      if (!d) return false
      if (s && d < s) return false
      if (e && d > e) return false
      return true
    })
  }

  // 排序
  const withIdx = arr.map((it, idx) => ({ it, idx }))
  withIdx.sort((a, b) => {
    let cmp = 0
    if (sortKey.value === 'date') {
      const da = toDate(a.it.date)?.getTime() ?? 0
      const db = toDate(b.it.date)?.getTime() ?? 0
      cmp = da - db
    } else {
      const ka = String(a.it[sortKey.value] ?? '')
      const kb = String(b.it[sortKey.value] ?? '')
      cmp = ka.localeCompare(kb)
    }
    if (!sortAsc.value) cmp = -cmp
    return cmp || (a.idx - b.idx)
  })
  return withIdx.map(x => x.it)
})

type XlsxInfo = {
  name: string
  path: string
  title: string
  map: string
  race: string
  date: string
  result: string
}

const xlsxFiles = ref<XlsxInfo[]>([])

function parseFileName(name: string) {
  const noExt = name.replace(/\.xlsx$/i, '')
  const [title, map, race, versus, result, describe] = noExt.split('-')
  console.log('解析文件名:', { title, map, race, versus, result, describe })
  return {
    title: title ?? noExt,
    map: map ?? '',
    race: race ?? '',
    date: versus ?? '',
    result: result ?? '',
  }
}
async function collectXlsxInDir(dir: string): Promise<XlsxInfo[]> {
  console.log('collectXlsxInDir:', dir)
  const entries = await readDir(dir)
  console.log('entries:', entries)

  const result: XlsxInfo[] = []

  for (const e of entries) {
    const base = await join(dir, e.name)
    if (e.isDirectory) {
      // 递归子目录

      const child = await collectXlsxInDir(base)
      result.push(...child)
    } else if (e.name?.toLowerCase().endsWith('.xlsx')) {
      const meta = parseFileName(e.name)
      result.push({
        path: base,
        name: e.name,
        title: meta.title,
        map: meta.map,
        race: meta.race,
        date: meta.date,
        result: meta.result,
      })
    }
  }

  return result
}

async function loadXlsxFiles() {
  try {
    const base = await appDataDir()         // C:\Users\...\Roaming\com.altria.sc2repshell\
    const folder = await join(base, 'replays')
    console.log('folder:', folder)
    const list = await collectXlsxInDir(folder)
    xlsxFiles.value = list
  } catch (err: any) {
    console.error('读取 .xlsx 失败:', err)
  }
}

let timer: number | null = null

onMounted(async () => {
  await loadXlsxFiles()
  // scan directory every 3 seconds
  timer = window.setInterval(loadXlsxFiles, 3000)
})

onBeforeUnmount(() => {
  if (timer !== null) clearInterval(timer)
})

</script>

<style scoped>
.toolbar { 
  position: fixed;
  width: 100%;
  height: var(--nav-height);
  display: flex;
  gap: 16px;
  background-color: #0f1012;
  padding: 8px 12px;
  user-select: none;
  border-bottom: 1px solid #2d2d2d;
  z-index: 10;
}

 .select, .btn {
    padding: .4rem .6rem;
    
    border-radius: .4rem;
    border: 1px solid #333;
    background:#1f1f1f;
    color:#eee; }

 .input{
    margin: 2px 5px;
    padding: .4rem .6rem;
    border-radius: .4rem;
    border: 1px solid #333;
    background:#1f1f1f;
    color:#eee; 
 }

.btn { cursor: pointer; }

.content{
  flex: 1;
  height: calc(100vh - 50px);
  margin-top: 50px;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 5px 5px;
}
</style>


