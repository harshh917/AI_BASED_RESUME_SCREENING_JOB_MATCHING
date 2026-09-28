import api from './api'

export async function register({ name, email, password, role }) {
  const { data } = await api.post('/api/auth/register', { name, email, password, role })
  persistAuth(data)
  return data
}

export async function login({ email, password }) {
  const { data } = await api.post('/api/auth/login', { email, password })
  persistAuth(data)
  return data
}

export function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user')
}

export function getStoredUser() {
  const raw = localStorage.getItem('user')
  return raw ? JSON.parse(raw) : null
}

function persistAuth(data) {
  localStorage.setItem('access_token', data.access_token)
  localStorage.setItem('user', JSON.stringify(data.user))
}
