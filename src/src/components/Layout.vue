<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white" height-hint="98">
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg" />
          </q-avatar>
          Generate JET Template
        </q-toolbar-title>

        <q-btn flat round dense :icon="theme" @click="toggleTheme" />
      </q-toolbar>

      <q-tabs align="left" v-model="tab">
        <q-tab name="Panda" label="Panda" />
        <q-tab name="Duck" label="Duck" />
        <q-tab name="Tools" label="Tools" />
      </q-tabs>
    </q-header>

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
import Duck from './Duck.vue'
import Tools from './Tools.vue'

import { useQuasar } from 'quasar'

const $q = useQuasar()

const tab = ref('Panda')
const tabs = {
  Panda: Panda,
  Duck: Duck,
  Tools: Tools,
}

const theme = ref('light_mode')

const toggleTheme = () => {
  theme.value = theme.value === 'light_mode' ? 'dark_mode' : 'light_mode'

  $q.dark.toggle()
}
</script>
