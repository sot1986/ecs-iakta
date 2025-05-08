export default defineEventHandler(async (event) => {
  // get runtime proxy url
  const { apiHostUrl } = useRuntimeConfig()
  // check the path

  const path = event.path.replace(/^\/api\//, '')

  const target = `${apiHostUrl}/${path}`
  
  return proxyRequest(event, target)
})