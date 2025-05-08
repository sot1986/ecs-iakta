export default defineNuxtPlugin(() => {
  const api = $fetch.create({
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
  })

  return {
    provide: {
      api
    }
  }
})