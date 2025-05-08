export interface ApiResponse<T> {
  ok: boolean
  data: T
}

export interface Hero {
  id: number
  name: string
  secret_name: string
  age: number
}