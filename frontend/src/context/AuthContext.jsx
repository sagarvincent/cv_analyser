// Layer: 2 — auth state provider; holds current user identity for the whole session
import { createContext, useContext, useState, useCallback } from 'react';
import { appConfig } from '../config/appConfig';

const AuthContext = createContext(null);

// -------------------- AuthProvider ----------- START ----------
// -- Calls : nothing (leaf — provides context value)
// -- Called by: App
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isGuest, setIsGuest] = useState(false);

  // -------------------- login ----------- START ----------
  // -- Calls : fetch /api/profile/verify
  // -- Called by: AuthScreen
  const login = useCallback(async (username, passwordHash) => {
    if (appConfig.useMockData) {
      setUser({ username, full_name: 'Demo User', email: 'demo@example.com', age: 0, location: null, experience: [], qualifications: [], aspirations: [], projects: [] });
      return { ok: true };
    }
    try {
      const res = await fetch(`${appConfig.apiBaseUrl}/profile/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password_hash: passwordHash }),
      });
      if (!res.ok) return { ok: false, error: 'Invalid username or password.' };
      setUser(await res.json());
      return { ok: true };
    } catch {
      return { ok: false, error: 'Network error. Please try again.' };
    }
  }, []);
  // -------------------- login ------------- END ----------------

  // -------------------- signup ----------- START ----------
  // -- Calls : fetch /api/profile/ (multipart)
  // -- Called by: AuthScreen
  const signup = useCallback(async (formData) => {
    if (appConfig.useMockData) {
      setUser({ username: formData.get('username'), full_name: formData.get('full_name'), email: formData.get('email'), age: 0, location: formData.get('location') || null, experience: [], qualifications: [], aspirations: [], projects: [] });
      return { ok: true };
    }
    try {
      const res = await fetch(`${appConfig.apiBaseUrl}/profile/`, { method: 'POST', body: formData });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        return { ok: false, error: err.detail || 'Signup failed.' };
      }
      setUser(await res.json());
      return { ok: true };
    } catch {
      return { ok: false, error: 'Network error. Please try again.' };
    }
  }, []);
  // -------------------- signup ------------- END ----------------

  // -------------------- loginAsGuest ----------- START ----------
  // -- Calls : nothing (leaf)
  // -- Called by: AuthScreen
  const loginAsGuest = useCallback(() => {
    setIsGuest(true);
    setUser(null);
  }, []);
  // -------------------- loginAsGuest ------------- END ----------------

  // -------------------- logout ----------- START ----------
  // -- Calls : nothing (leaf)
  // -- Called by: Sidebar, ProfilePage
  const logout = useCallback(() => {
    setUser(null);
    setIsGuest(false);
  }, []);
  // -------------------- logout ------------- END ----------------

  // -------------------- refreshProfile ----------- START ----------
  // -- Calls : fetch /api/profile/{username}
  // -- Called by: ProfilePage after successful save
  const refreshProfile = useCallback(async () => {
    if (!user?.username || appConfig.useMockData) return;
    try {
      const res = await fetch(`${appConfig.apiBaseUrl}/profile/${user.username}`);
      if (res.ok) setUser(await res.json());
    } catch { /* silent refresh failure */ }
  }, [user?.username]);
  // -------------------- refreshProfile ------------- END ----------------

  return (
    <AuthContext.Provider value={{ user, isGuest, login, signup, loginAsGuest, logout, refreshProfile }}>
      {children}
    </AuthContext.Provider>
  );
}
// -------------------- AuthProvider ------------- END ----------------

// -------------------- useAuth ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: AuthScreen, App, Sidebar, ProfilePage
export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
// -------------------- useAuth ------------- END ----------------
