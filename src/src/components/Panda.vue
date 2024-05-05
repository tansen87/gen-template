<template>
  <div
    class="q-pa-md"
    style="display: flex; justify-content: space-between; max-width: 1500px; margin: 0 auto"
  >
    <!-- column 1 -->
    <div class="q-gutter-y-md" style="flex-basis: 23%; max-width: 350px">
      <q-input color="teal" v-model="input.entity" label="Entity">
        <template v-slot:prepend>
          <q-icon name="room" />
          <q-select
            v-model="input.entitySelect"
            :options="entitySelectOptions"
            label="mode"
            style="width: 70px"
          />
          <q-select
            v-model="input.entityLang"
            :options="entityLangOptions"
            label="lang"
            style="width: 60px"
          />
        </template>
      </q-input>
      <q-input color="teal" v-model="input.dateEffective" label="Date Effective">
        <template v-slot:prepend>
          <q-icon name="timer" />
          <q-select
            v-model="input.dateSelect"
            :options="dateSelectOptions"
            label="mode"
            style="width: 70px"
          />
        </template>
      </q-input>
      <q-input color="teal" v-model="input.lineDescription" label="Line Description">
        <template v-slot:prepend>
          <q-icon name="payments" />
        </template>
      </q-input>
      <q-input color="teal" v-model="input.currency" label="Currency">
        <template v-slot:prepend>
          <q-icon name="attach_money" />
          <q-select
            v-model="input.currencySelect"
            :options="currencySelectOptions"
            label="mode"
            style="width: 70px"
          />
        </template>
      </q-input>
    </div>

    <!-- column 2 -->
    <div class="q-gutter-y-md" style="flex-basis: 23%; max-width: 350px">
      <q-input color="teal" v-model="input.company" label="Company Name">
        <template v-slot:prepend>
          <q-icon name="room" />
          <q-select
            v-model="input.companySelect"
            :options="companySelectOptions"
            label="mode"
            style="width: 80px"
          />
        </template>
      </q-input>
      <q-input color="teal" v-model="input.dateEntered" label="Date Entered">
        <template v-slot:prepend>
          <q-icon name="timer" />
          <q-select
            v-model="input.dateSelect"
            :options="dateSelectOptions"
            label="mode"
            style="width: 70px"
          />
        </template>
      </q-input>
      <q-input color="teal" v-model="input.amount" label="Amount">
        <template v-slot:prepend>
          <q-icon name="account_balance_wallet" />
          <q-select
            v-model="input.amountSelect"
            :options="amountSelectOptions"
            label="mode"
            style="width: 70px"
          />
        </template>
      </q-input>
      <q-input color="teal">
        <template v-slot:prepend>
          <q-select
            v-model="input.ami"
            :options="amiSelectOptions"
            label="Auto Manual Interface"
            style="width: 350px"
          />
        </template>
      </q-input>
    </div>

    <!-- column 3 -->
    <div class="q-gutter-y-md" style="flex-basis: 23%; max-width: 350px">
      <q-input color="teal" v-model="input.journalNumber" label="Journal Number">
        <template v-slot:prepend>
          <q-icon name="loyalty" />
          <q-select
            v-model="input.jnConnect"
            :options="jnConnectOptions"
            label="connect"
            style="width: 80px"
          />
        </template>
      </q-input>
      <q-input color="teal" v-model="input.userEntered" label="User Entered">
        <template v-slot:prepend>
          <q-icon name="people" />
          <q-select
            v-model="input.userSelect"
            :options="userSelectOptions"
            label="mode"
            style="width: 70px"
          />
          <q-select
            v-model="input.userLang"
            :options="userLangOptions"
            label="lang"
            style="width: 60px"
          />
        </template>
      </q-input>
      <q-input color="teal" v-model="input.account" label="Account Number">
        <template v-slot:prepend>
          <q-icon name="scatter_plot" />
          <q-select
            v-model="input.accountSelect"
            :options="accountSelectOptions"
            label="mode"
            style="width: 70px"
          />
        </template>
      </q-input>
      <q-input color="teal">
        <template v-slot:prepend>
          <q-select
            v-model="input.sep"
            :options="sepOptions"
            label="Separator"
            style="width: 175px"
          />
          <q-select
            v-model="input.encoding"
            :options="encodingOptions"
            label="Encoding"
            style="width: 175px"
          />
        </template>
      </q-input>
    </div>

    <!-- column 4 -->
    <div class="q-gutter-y-md" style="flex-basis: 23%; max-width: 350px">
      <q-input color="teal" v-model="input.journalType" label="Journal Type">
        <template v-slot:prepend>
          <q-icon name="loyalty" />
        </template>
      </q-input>
      <q-input color="teal" v-model="input.userUpdated" label="User Updated">
        <template v-slot:prepend>
          <q-icon name="people" />
          <q-select
            v-model="input.userSelect"
            :options="userSelectOptions"
            label="mode"
            style="width: 70px"
          />
          <q-select
            v-model="input.userLang"
            :options="userLangOptions"
            label="lang"
            style="width: 60px"
          />
        </template>
      </q-input>
      <q-input color="teal" v-model="input.accountDescription" label="Account Description">
        <template v-slot:prepend>
          <q-icon name="scatter_plot" />
          <q-select
            v-model="input.accountSelect"
            :options="accountSelectOptions"
            label="mode"
            style="width: 70px"
          />
        </template>
      </q-input>
      <q-input color="teal">
        <template v-slot:prepend>
          <q-btn color="primary" label="open file" @click="openFile" style="width: 110px" />
          <q-btn color="secondary" label="process" @click="process" style="width: 110px" />
        </template>
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
import { useQuasar, QSpinnerGears } from 'quasar'

const $q = useQuasar()

const tableData = ref([])
const columns = ref([])
const input = reactive({
  entity: '被审计单位',
  entitySelect: 'column',
  entityLang: 'EN',
  company: '',
  companySelect: '',
  journalNumber: '凭证编号',
  jnConnect: 'yes',
  journalType: '',
  dateEffective: '记账时间',
  dateEntered: '',
  dateSelect: 'equal',
  userEntered: '',
  userUpdated: '',
  userSelect: 'unequal',
  userLang: 'EN',
  lineDescription: '业务说明',
  amount: '借方发生额|贷方发生额',
  amountSelect: 'd|c',
  account: '科目编号',
  accountDescription: '科目名称',
  accountSelect: 'unequal',
  currency: 'CNY',
  currencySelect: 'input',
  ami: 'Manual',
  sep: ',',
  encoding: 'utf-8'
})
const entitySelectOptions = ['column', 'input']
const entityLangOptions = ['EN', 'CN']
const companySelectOptions = ['column', 'input']
const jnConnectOptions = ['yes', 'no']
const dateSelectOptions = ['equal', 'unequal']
const userSelectOptions = ['equal', 'unequal']
const userLangOptions = ['EN', 'CN']
const amountSelectOptions = ['d|c', 'amount']
const accountSelectOptions = ['equal', 'unequal']
const currencySelectOptions = ['column', 'input']
const amiSelectOptions = ['Auto', 'Manual', 'Interface']
const sepOptions = [',', '|', '\\t', ';']
const encodingOptions = ['utf-8', 'utf_8_sig', 'utf-16le', 'gbk']

// 打开文件
function openFile() {
  window.pywebview.api.panda_open_file(input.sep, input.encoding).then((res) => {
    const jsData = JSON.parse(res)
    columns.value = Object.keys(jsData[0]).map((key) => ({ name: key, label: key, field: key }))
    tableData.value = jsData
  })
}

// 生成模板
async function process() {
  const notif = $q.notify({
    color: 'info',
    icon: 'info',
    position: 'top-right',
    group: false,
    timeout: 0,
    spinner: QSpinnerGears,
    message: 'running...'
  })
  try {
    const res = await window.pywebview.api.panda_process(
      input.entity,
      input.entitySelect,
      input.entityLang,
      input.company,
      input.companySelect,
      input.journalNumber,
      input.jnConnect,
      input.journalType,
      input.dateEffective,
      input.dateEntered,
      input.dateSelect,
      input.userEntered,
      input.userUpdated,
      input.userSelect,
      input.userLang,
      input.lineDescription,
      input.amount,
      input.amountSelect,
      input.account,
      input.accountDescription,
      input.accountSelect,
      input.currency,
      input.currencySelect,
      input.ami,
      input.sep,
      input.encoding
    )
    if (typeof res === 'string' && res.includes('Error')) {
      let notifId = notif({
        message: res,
        color: 'negative',
        icon: 'sentiment_very_dissatisfied',
        spinner: false,
        actions: [
          {
            label: 'ok',
            color: 'white',
            handler: () => {
              notifId = null
            }
          }
        ]
      })
    } else if (res && typeof res === 'number') {
      let notifId = notif({
        message: 'cost time: ' + res.toString(),
        color: 'positive',
        icon: 'sentiment_satisfied_alt',
        spinner: false,
        actions: [
          {
            label: 'ok',
            color: 'white',
            handler: () => {
              notifId = null
            }
          }
        ]
      })
    } else {
      let notifId = notif({
        message: res.toString(),
        color: 'negative',
        icon: 'sentiment_very_dissatisfied',
        spinner: false,
        actions: [
          {
            label: 'ok',
            color: 'white',
            handler: () => {
              notifId = null
            }
          }
        ]
      })
    }
  } catch (error) {
    let notifId = notif({
      message: error,
      color: 'negative',
      icon: 'sentiment_very_dissatisfied',
      spinner: false,
      actions: [
        {
          label: 'ok',
          color: 'white',
          handler: () => {
            notifId = null
          }
        }
      ]
    })
  }
}
</script>
