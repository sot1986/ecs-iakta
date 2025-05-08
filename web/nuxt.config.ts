import tailwindcss from "@tailwindcss/vite";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: ['@nuxt/eslint', 'nuxt-headlessui'],
  runtimeConfig: {
    apiHostUrl: '',
  },
  future: {
    compatibilityVersion: 4,
  },
  css: [
    '~/assets/css/tailwind.css',
  ],
  vite: {
    plugins: [
      tailwindcss()
    ]
  },
  headlessui: {
    prefix: 'Headless'
}
  // routeRules: {
  //   '/api/**': {
  //     proxy: `${process.env.NUXT_API_HOST_URL}/**`,
  //   }
  // }
  // vite: {
  //   server: {
  //     proxy: {
  //       '/api': {
  //         target: process.env.NUXT_API_HOST_URL,
  //         changeOrigin: true,
  //         rewrite: (path) => path.replace(/^\/api/, ''),
  //       },
  //     },
  //   }
  // }
  // nitro: {
  //   devProxy: {
  //     '/api': {
  //       target: process.env.NUXT_API_HOST_URL,
  //       changeOrigin: true,
  //     },
  //   }
  // }
})
