<script setup lang="ts">
import HeroForm from '~/components/HeroForm.vue'
import UiDrawer from '~/components/UiDrawer.vue'
import type { Hero, ApiResponse } from '~/types'

defineOptions({
  name: 'HomePage',
})

const { data, refresh } = await useFetch<ApiResponse<Hero[]>>('/api/heroes', undefined, { server: false })
const { $api } = useNuxtApp()

const showEditHero = ref(false)
const selectedHero = ref<Hero>()

function savedHero() {
  refresh()
  showEditHero.value = false
}

function deleteHero(hero: Hero) {
  if (confirm(`Are you sure you want to delete ${hero.name}?`)) {
    $api(`/api/heroes/${hero.id}`, {
      method: 'DELETE',
    })
      .then(() => {
        refresh()
      })
      .catch((error) => {
        console.error('Error deleting hero:', error)
      })
  }
}

function editHero(hero: Hero) {
  selectedHero.value = hero
  showEditHero.value = true
}

function createHero() {
  selectedHero.value = undefined
  showEditHero.value = true
}
</script>

<template>
  <div>
    <div class="px-4 sm:px-6 lg:px-8">
    <div class="sm:flex sm:items-center">
      <div class="sm:flex-auto">
        <h1 class="text-base font-semibold text-gray-900">Heroes v2</h1>
        <p class="mt-2 text-sm text-gray-700">A list of all iakta heroes.</p>
      </div>
      <div class="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
        <button type="button" class="block rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600" @click="createHero">Add hero</button>
      </div>
    </div>
    <div v-if="data?.data.length" class="mt-8 flow-root">
      <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
          <table class="min-w-full divide-y divide-gray-300">
            <thead>
              <tr>
                <th scope="col" class="py-3.5 pr-3 pl-4 text-left text-sm font-semibold text-gray-900 sm:pl-0">Name</th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Secret Name</th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Age</th>
                <th scope="col" class="relative py-3.5 pr-4 pl-3 sm:pr-0">
                  <span class="sr-only">Edit</span>
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr v-for="hero in data?.data" :key="hero.id">
                <td class="py-4 pr-3 pl-4 text-sm font-medium whitespace-nowrap text-gray-900 sm:pl-0">{{ hero.name }}</td>
                <td class="px-3 py-4 text-sm whitespace-nowrap text-gray-500">{{ hero.secret_name }}</td>
                <td class="px-3 py-4 text-sm whitespace-nowrap text-gray-500">{{ hero.age }}</td>
              
                <td class="relative py-4 pr-4 pl-3 text-right text-sm font-medium whitespace-nowrap sm:pr-0 space-x-2">
                  <button type="button" class="text-indigo-600 hover:text-indigo-900" @click="editHero(hero)">
                    Edit<span class="sr-only">, {{ hero.name }}</span>
                  </button>
                  <button type="button" class="text-red-600 hover:text-red-900" @click="deleteHero(hero)">Delete<span class="sr-only">, {{ hero.name }}</span></button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <p v-else class="mt-8 text-center text-sm text-gray-500">
      No heroes found...
    </p>
  </div>
    <UiDrawer v-model="showEditHero">
      <HeroForm :hero="selectedHero" @saved="savedHero" />
    </UiDrawer>
  </div>
</template>
