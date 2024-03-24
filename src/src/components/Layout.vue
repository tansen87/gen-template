<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white" height-hint="98">
      <q-toolbar>
        <!-- <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" /> -->

        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg" />
          </q-avatar>
          Generate JET Template
        </q-toolbar-title>

        <q-btn flat round dense :icon="theme" @click="toggleTheme" />
      </q-toolbar>

      <q-tabs align="left" v-model="tab">
        <q-tab name="Pandas" label="Pandas" />
        <q-tab name="Duck" label="Duck" />
        <q-tab name="Tools" label="Tools" />
      </q-tabs>
    </q-header>

    <!-- <q-drawer show-if-above v-model="leftDrawerOpen" side="left" behavior="desktop" bordered>

    </q-drawer> -->

    <q-page-container>
      <KeepAlive>
        <component :is="tabs[tab]"></component>
      </KeepAlive>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import Pandas from './Pandas.vue'
import Duck from './Duck.vue'
import Tools from './Tools.vue'

import { useQuasar } from 'quasar'

const $q = useQuasar()

// const leftDrawerOpen = ref(true)

// const toggleLeftDrawer = () => {
//   leftDrawerOpen.value = !leftDrawerOpen.value
// }

const tab = ref('Pandas')
const tabs = {
  Pandas: Pandas,
  Duck: Duck,
  Tools: Tools,
}

const theme = ref('light_mode')

const toggleTheme = () => {
  theme.value = theme.value === 'light_mode' ? 'dark_mode' : 'light_mode'

  $q.dark.toggle()
}
</script>
