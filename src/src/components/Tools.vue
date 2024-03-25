<template>
  <div
    class="q-pa-md"
    style="display: flex; justify-content: space-between; max-width: 1000px; margin: 0 auto"
  >
    <!-- column 1 -->
    <div class="q-gutter-y-md" style="flex-basis: 46%; max-width: 300px">
      <q-input color="teal" outlined v-model="input.replCols" label="Columns-replace char">
        <template v-slot:prepend>
          <q-icon name="cloud" />
        </template>
      </q-input>
      <q-input color="teal" outlined v-model="input.cn2pinyinCols" label="Columns-CN2Pinyin">
        <template v-slot:prepend>
          <q-icon name="cloud" />
        </template>
      </q-input>
      <q-input
        color="teal"
        outlined
        v-model="input.replSfCols"
        label="Columns-replace specific char"
      >
        <template v-slot:prepend>
          <q-icon name="cloud" />
        </template>
      </q-input>
    </div>

    <!-- column 2 -->
    <div class="q-gutter-y-md" style="flex-basis: 46%; max-width: 300px">
      <q-input color="teal"></q-input>
      <q-input color="teal">
        <template v-slot:prepend>
          <q-select
            v-model="input.sep"
            :options="sepOptions"
            label="Separator"
            style="width: 145px"
          />
          <q-select
            v-model="input.encoding"
            :options="encodingOptions"
            label="Encoding"
            style="width: 145px"
          />
        </template>
      </q-input>
      <q-input color="teal" label="old char">
        <template v-slot:prepend>
          <q-icon name="arrow_right" />
          <q-input color="primary" label="old char" v-model="input.oldChar" style="width: 135px" />
          <q-icon name="arrow_right" />
          <q-input
            color="secondary"
            label="new char"
            v-model="input.newChar"
            style="width: 135px"
          />
        </template>
      </q-input>
    </div>

    <!-- column 3 -->
    <div class="q-gutter-y-md" style="flex-basis: 46%; max-width: 300px">
      <q-input color="teal">
        <template v-slot:prepend>
          <q-btn color="primary" label="open file" @click="openFile" style="width: 145px" />
          <q-btn color="secondary" label="replace" @click="replChar" style="width: 145px" />
        </template>
      </q-input>
      <q-input color="teal">
        <template v-slot:prepend>
          <q-btn color="primary" label="open file" @click="openFile" style="width: 145px" />
          <q-btn color="secondary" label="CN2Pinyin" @click="cn2pinyin" style="width: 145px" />
        </template>
      </q-input>
      <q-input color="teal">
        <template v-slot:prepend>
          <q-btn color="primary" label="open file" @click="openFile" style="width: 145px" />
          <q-btn color="secondary" label="replace-sp" @click="replSfChar" style="width: 145px" />
        </template>
      </q-input>
    </div>
  </div>

  <div
    class="q-pa-md"
    style="display: flex; justify-content: space-between; max-width: 1000px; margin: 0 auto"
  >
    <q-table
      :rows="tableData"
      :columns="columns"
      row-key="name"
      binary-state-sort
      style="height: 355px; width: 100%"
    >
    </q-table>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()

const tableData = ref([])
const columns = ref([])
const input = reactive({
  cn2pinyinCols: 'A|B|C',
  oldChar: '',
  newChar: '',
  replCols: 'A',
  replSfCols: 'A',
  sep: ',',
  encoding: 'utf-8'
})
const sepOptions = [',', '|', '\\t', ';']
const encodingOptions = ['utf-8', 'utf_8_sig', 'utf-16le', 'gbk']

// 打开文件
function openFile() {
  window.pywebview.api.panda_tools_open_file(input.sep, input.encoding).then((res) => {
    const jsData = JSON.parse(res)
    columns.value = Object.keys(jsData[0]).map((key) => ({ name: key, label: key, field: key }))
    tableData.value = jsData
  })
}

// 中文转拼音
async function cn2pinyin() {
  const notif = $q.notify({
    color: 'info',
    icon: 'info',
    position: 'top-right',
    group: false,
    timeout: 0,
    spinner: true,
    message: 'chinese 2 pinyin...'
  })
  await window.pywebview.api
    .panda_cn2pinyin(input.cn2pinyinCols, input.sep, input.encoding)
    .then((res) => {
      if (typeof res === 'string' && res.includes('Error')) {
        notif({
          message: res,
          color: 'negative',
          icon: 'sentiment_very_dissatisfied',
          position: 'top-right',
          spinner: false,
          timeout: 3000
        })
      } else if (res && typeof res === 'number') {
        notif({
          message: res.toString(),
          color: 'positive',
          icon: 'sentiment_satisfied_alt',
          position: 'top-right',
          spinner: false,
          timeout: 2000
        })
      } else {
        notif({
          message: res.toString(),
          color: 'negative',
          icon: 'sentiment_very_dissatisfied',
          position: 'top-right',
          spinner: false,
          timeout: 2000
        })
      }
    })
}

// 替换特殊符号
async function replChar() {
  const notif = $q.notify({
    color: 'info',
    icon: 'info',
    position: 'top-right',
    group: false,
    timeout: 0,
    spinner: true,
    message: 'repalce char...'
  })
  await window.pywebview.api
    .panda_repl_char(input.replCols, input.sep, input.encoding)
    .then((res) => {
      if (typeof res === 'string' && res.includes('Error')) {
        notif({
          message: res,
          color: 'negative',
          icon: 'sentiment_very_dissatisfied',
          position: 'top-right',
          spinner: false,
          timeout: 3000
        })
      } else if (res && typeof res === 'number') {
        notif({
          message: res.toString(),
          color: 'positive',
          icon: 'sentiment_satisfied_alt',
          position: 'top-right',
          spinner: false,
          timeout: 2000
        })
      } else {
        notif({
          message: res.toString(),
          color: 'negative',
          icon: 'sentiment_very_dissatisfied',
          position: 'top-right',
          spinner: false,
          timeout: 2000
        })
      }
    })
}

// 替换指定符号
async function replSfChar() {
  const notif = $q.notify({
    color: 'info',
    icon: 'info',
    position: 'top-right',
    group: false,
    timeout: 0,
    spinner: true,
    message: 'repalce specific char...'
  })
  await window.pywebview.api
    .panda_repl_sf_char(input.replSfCols, input.oldChar, input.newChar, input.sep, input.encoding)
    .then((res) => {
      if (typeof res === 'string' && res.includes('Error')) {
        notif({
          message: res,
          color: 'negative',
          icon: 'sentiment_very_dissatisfied',
          position: 'top-right',
          spinner: false,
          timeout: 3000
        })
      } else if (res && typeof res === 'number') {
        notif({
          message: res.toString(),
          color: 'positive',
          icon: 'sentiment_satisfied_alt',
          position: 'top-right',
          spinner: false,
          timeout: 2000
        })
      } else {
        notif({
          message: res.toString(),
          color: 'negative',
          icon: 'sentiment_very_dissatisfied',
          position: 'top-right',
          spinner: false,
          timeout: 2000
        })
      }
    })
}
</script>
