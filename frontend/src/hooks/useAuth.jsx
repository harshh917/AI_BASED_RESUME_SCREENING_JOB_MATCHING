import { createContext, useContext, useMemo, useState } from 'react'
import { getStoredUser, login as loginRequest, logout as logoutRequest, register as registerRequest } from '../services/authService'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(getStoredUser())

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: Boolean(user),
      async login(credentials) {
        const data = await loginRequest(credentials)
        setUser(data.user)
        return data
      },
      async register(payload) {
        const data = await registerRequest(payload)
        setUser(data.user)
        return data
      },
      logout() {
        logoutRequest()
        setUser(null)
      },
    }),
    [user]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return ctx
}
