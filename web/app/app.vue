<script setup lang="ts">
import { NuxtPage } from '#components'

defineOptions({
  name: 'App',
  inheritAttrs: false,
})


provideHeadlessUseId(() => useId())


</script>

<template>
  <div>
    <NuxtPage class="mt-8" />
  </div>
</template>
