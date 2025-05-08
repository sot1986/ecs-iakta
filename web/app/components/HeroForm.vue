<script setup lang="ts">
import type { ApiResponse, Hero } from '~/types';

defineOptions({
  name: 'HeroForm',
  inheritAttrs: false,
})

const props = defineProps<{
  hero?: Hero
}>()

const emits = defineEmits<{
  (e: 'saved', data: Hero): void
}>()

const { $api } = useNuxtApp()

const heroData = reactive({
  name: '',
  secret_name: '',
  age: 18,
})

function resetData() {
  heroData.name = props.hero?.name || ''
  heroData.secret_name = props.hero?.secret_name || ''
  heroData.age = props.hero?.age || 18
}

onMounted(resetData)

watch(() => props.hero?.id, resetData)

async function submit() {
  try {
    const url = props.hero?.id ? `/api/heroes/${props.hero.id}` : '/api/heroes'
    const resp = await $api<ApiResponse<Hero>>(
      url, { 
        method: props.hero?.id ? 'PUT' : 'POST',
        body: heroData,
      })
    if (resp.ok) {
      emits('saved', resp.data)
    }
    else {
      console.error('Error submitting form:', resp)
    }
  }
  catch (error) {
    console.error('Error submitting form:', error)
  }
  
}

</script>

<template>
  <form class="space-y-6" @submit.prevent="submit" @reset="resetData">
    <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
      <div class="col-span-full">
        <div>
          <label for="name" class="block text-sm/6 font-medium text-gray-900">
            Name
          </label>
          <div class="mt-2">
            <input id="name" v-model="heroData.name" type="text" name="name" class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6" placeholder="Superman" >
          </div>
        </div>
      </div>

      <div class="col-span-full">
        <label for="secret-name" class="block text-sm/6 font-medium text-gray-900">
          Secret name
        </label>
        <div class="mt-2">
          <input id="secret-name" v-model="heroData.secret_name" type="text" name="secret-name" class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6" placeholder="Real name" >
        </div>
      </div>

      <div class="sm:col-span-3">
        <label for="age" class="block text-sm/6 font-medium text-gray-900">
          Age
        </label>
        <div class="mt-2">
          <input id="age" v-model="heroData.age" type="number" name="age" class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6" placeholder="18" >
        </div>
      </div>
    </div>

    <div class="flex gap-4 justify-end">
      <button type="reset" class="inline-block rounded-md bg-gray-200 px-3 py-2 text-sm font-semibold text-gray-900 shadow-xs hover:bg-gray-300 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-900">
        Reset
      </button>
      <button type="submit" class="inline-block rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
        Save
      </button>
    </div>
  </form>
</template>
