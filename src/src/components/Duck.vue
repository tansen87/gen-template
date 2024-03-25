<template>
  <div
    class="q-pa-md"
    style="display: flex; justify-content: space-between; max-width: 1500px; margin: 0 auto"
  >
    <!-- column 1 -->
    <div class="q-gutter-y-md" style="flex-basis: 23%; max-width: 350px">
      <q-input color="teal" v-model="input.tableName" label="Table Name">
        <template v-slot:prepend>
          <q-icon name="cloud" />
        </template>
      </q-input>
    </div>

    <!-- column 2 -->
    <div class="q-gutter-y-md" style="flex-basis: 23%; max-width: 350px">
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
    </div>

    <!-- column 3 -->
    <div class="q-gutter-y-md" style="flex-basis: 23%; max-width: 350px">
      <q-input color="teal">
        <template v-slot:prepend>
          <q-btn color="primary" label="open file" @click="openFile" style="width: 145px" />
          <q-btn color="secondary" label="write" @click="createDB" style="width: 145px" />
        </template>
      </q-input>
    </div>

    <!-- column 4 -->
    <div class="q-gutter-y-md" style="flex-basis: 23%; max-width: 350px">
      <q-input color="teal">
        <template v-slot:prepend> </template>
      </q-input>
    </div>
  </div>

  <div
    class="q-pa-md"
    style="display: flex; justify-content: space-between; max-width: 1500px; margin: 0 auto"
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
import { useQuasar, Notify } from 'quasar'

const $q = useQuasar()

const tableData = ref([])
const columns = ref([])
const input = reactive({
  tableName: 'duck',
  sep: ',',
  encoding: 'utf-8'
})
const sepOptions = [',', '|', '\\t', ';']
const encodingOptions = ['utf-8', 'utf_8_sig', 'utf-16le', 'gbk']

// 打开文件
function openFile() {
  try {
    window.pywebview.api.duck_open_file(input.sep, input.encoding).then((res) => {
      const jsData = JSON.parse(res)
      columns.value = Object.keys(jsData[0]).map((key) => ({ name: key, label: key, field: key }))
      tableData.value = jsData
    })
  } catch (err) {
    Notify.create({
      message: err.message,
      color: 'negative',
      icon: 'sentiment_very_dissatisfied',
      position: 'top-right',
      spinner: false,
      timeout: 3000
    })
  }
}

// 创建duckdb
async function createDB() {
  const notif = $q.notify({
    color: 'info',
    icon: 'info',
    position: 'top-right',
    group: false,
    timeout: 0,
    spinner: true,
    message: 'writing...'
  })
  await window.pywebview.api.duck_create_db(input.sep, input.tableName).then((res) => {
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
        message: 'write success: ' + res.toString(),
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
