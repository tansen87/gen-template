<template>
  <q-layout view="hHh lpR fFf">
    <div class="row no-wrap">
      <div class="col">
        <q-tabs align="left" v-model="tab" class="text-right">
          <q-tab name="Panda" label="Panda" />
          <q-tab name="Tools" label="Tools" />
        </q-tabs>
      </div>
      <div class="col-auto">
        <q-btn flat round dense :icon="theme" @click="toggleTheme" />
      </div>
    </div>

    <q-page-container>
      <KeepAlive>
        <component :is="tabs[tab]"></component>
      </KeepAlive>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import Panda from './Panda.vue'
import Tools from './Tools.vue'

import { useQuasar } from 'quasar'

const $q = useQuasar()

const tab = ref('Panda')
const tabs = {
  Panda: Panda,
  Tools: Tools,
}

const theme = ref('light_mode')

const toggleTheme = () => {
  theme.value = theme.value === 'light_mode' ? 'dark_mode' : 'light_mode'

  $q.dark.toggle()
}
</script>
