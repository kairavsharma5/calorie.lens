import { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const DIETARY_OPTIONS = [
  { key: 'vegetarian',  label: 'Vegetarian' },
  { key: 'vegan',       label: 'Vegan' },
  { key: 'no_dairy',    label: 'No Dairy' },
  { key: 'no_nuts',     label: 'No Nuts' },
  { key: 'gluten_free', label: 'Gluten Free' },
  { key: 'keto',        label: 'Keto' }
]

const APP_VERSION = '1.0.0'

// ─────────────────────────────────────────
// SETTINGS SCREEN
// Props:
//   user      - { token, username }
//   onBack    - go back to main menu
//   onLogout  - logs the user out completely (from App.jsx)
// ─────────────────────────────────────────
function Settings({ user, onBack, onLogout }) {
  const authHeader = { headers: { Authorization: `Bearer ${user.token}` } }

  const [loading, setLoading]   = useState(true)
  const [message, setMessage]   = useState('') // success text, green
  const [error, setError]       = useState('') // error text, red

  // profile fields
  const [username, setUsername] = useState('')
  const [email, setEmail]       = useState('')
  const [phone, setPhone]       = useState('')

  // password fields
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword]         = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  // dietary tags
  const [dietaryTags, setDietaryTags] = useState([])

  // delete account confirmation
  const [deletePassword, setDeletePassword] = useState('')
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)

  // clear banners automatically after a few seconds
  const flash = (setFn, text) => {
    setFn(text)
    setTimeout(() => setFn(''), 3000)
  }

  // ── LOAD CURRENT PROFILE ON MOUNT ──────────────────────
  useEffect(() => {
    const loadProfile = async () => {
      try {
        const res = await axios.get(`${API_BASE_URL}/user/profile`, authHeader)
        setUsername(res.data.username || '')
        setEmail(res.data.email || '')
        setPhone(res.data.phone || '')
        setDietaryTags(res.data.dietary_preferences || [])
      } catch (err) {
        setError('Could not load profile')
      } finally {
        setLoading(false)
      }
    }
    loadProfile()
  }, [])

  // ── SAVE PROFILE ──────────────────────
  const handleSaveProfile = async (e) => {
    e.preventDefault()
    try {
      await axios.put(`${API_BASE_URL}/user/profile`, { username, email, phone }, authHeader)
      flash(setMessage, 'Profile updated successfully')
    } catch (err) {
      flash(setError, err.response?.data?.error || 'Failed to update profile')
    }
  }

  // ── CHANGE PASSWORD ──────────────────────
  const handleChangePassword = async (e) => {
    e.preventDefault()
    if (newPassword !== confirmPassword) {
      flash(setError, 'New passwords do not match')
      return
    }
    if (newPassword.length < 6) {
      flash(setError, 'New password must be at least 6 characters')
      return
    }
    try {
      await axios.put(`${API_BASE_URL}/user/password`, {
        current_password: currentPassword,
        new_password: newPassword
      }, authHeader)
      flash(setMessage, 'Password changed successfully')
      setCurrentPassword('')
      setNewPassword('')
      setConfirmPassword('')
    } catch (err) {
      flash(setError, err.response?.data?.error || 'Failed to change password')
    }
  }

  // ── TOGGLE A DIETARY TAG ──────────────────────
  const toggleTag = (key) => {
    setDietaryTags(prev =>
      prev.includes(key) ? prev.filter(t => t !== key) : [...prev, key]
    )
  }

  const handleSaveDietary = async () => {
    try {
      await axios.put(`${API_BASE_URL}/user/dietary-preferences`, {
        dietary_preferences: dietaryTags
      }, authHeader)
      flash(setMessage, 'Dietary preferences saved')
    } catch (err) {
      flash(setError, err.response?.data?.error || 'Failed to save preferences')
    }
  }

  // ── RESET STREAK ──────────────────────
  const handleResetStreak = async () => {
    const confirmed = window.confirm('Reset your streak back to 0? This cannot be undone.')
    if (!confirmed) return
    try {
      await axios.post(`${API_BASE_URL}/user/streak/reset`, {}, authHeader)
      flash(setMessage, 'Streak reset to 0')
    } catch (err) {
      flash(setError, 'Failed to reset streak')
    }
  }

  // ── DELETE ALL DATA ──────────────────────
  const handleDeleteData = async () => {
    const confirmed = window.confirm(
      'This will permanently delete ALL your logged meals and custom foods. Your account will stay active. Continue?'
    )
    if (!confirmed) return
    try {
      await axios.delete(`${API_BASE_URL}/user/data`, authHeader)
      flash(setMessage, 'All data deleted')
    } catch (err) {
      flash(setError, 'Failed to delete data')
    }
  }

  // ── DELETE ACCOUNT ──────────────────────
  const handleDeleteAccount = async () => {
    if (!deletePassword) {
      flash(setError, 'Enter your password to confirm account deletion')
      return
    }
    try {
      await axios.delete(`${API_BASE_URL}/user/account`, {
        ...authHeader,
        data: { password: deletePassword }
      })
      // account is gone — log out immediately
      onLogout()
    } catch (err) {
      flash(setError, err.response?.data?.error || 'Failed to delete account')
    }
  }

  if (loading) {
    return (
      <div className="dashboard-container">
        <p className="loading-text">Loading settings...</p>
      </div>
    )
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2>Settings</h2>
        <button className="btn btn-secondary" onClick={onBack}>← Back</button>
      </div>

      {message && <div className="success-message">{message}</div>}
      {error && <div className="error-message">{error}</div>}

      {/* ── PROFILE ── */}
      <div className="dashboard-card">
        <h3>Edit Profile</h3>
        <form onSubmit={handleSaveProfile}>
          <div className="form-group">
            <label className="form-label">Username</label>
            <input className="form-input" value={username} onChange={e => setUsername(e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Email</label>
            <input className="form-input" type="email" value={email} onChange={e => setEmail(e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Phone</label>
            <input className="form-input" value={phone} onChange={e => setPhone(e.target.value)} placeholder="Optional" />
          </div>
          <button type="submit" className="btn btn-primary">Save Profile</button>
        </form>
      </div>

      {/* ── PASSWORD ── */}
      <div className="dashboard-card">
        <h3>Change Password</h3>
        <form onSubmit={handleChangePassword}>
          <div className="form-group">
            <label className="form-label">Current Password</label>
            <input className="form-input" type="password" value={currentPassword} onChange={e => setCurrentPassword(e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">New Password</label>
            <input className="form-input" type="password" value={newPassword} onChange={e => setNewPassword(e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Confirm New Password</label>
            <input className="form-input" type="password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} />
          </div>
          <button type="submit" className="btn btn-primary">Change Password</button>
        </form>
      </div>

      {/* ── DIETARY PREFERENCES ── */}
      <div className="dashboard-card">
        <h3>Dietary Preferences</h3>
        <div className="dietary-tags-grid" style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', margin: '1rem 0' }}>
          {DIETARY_OPTIONS.map(opt => (
            <button
              key={opt.key}
              type="button"
              onClick={() => toggleTag(opt.key)}
              className={dietaryTags.includes(opt.key) ? 'btn btn-primary' : 'btn btn-secondary'}
            >
              {opt.label}
            </button>
          ))}
        </div>
        <button className="btn btn-primary" onClick={handleSaveDietary}>Save Preferences</button>
      </div>

      {/* ── STREAK ── */}
      <div className="dashboard-card">
        <h3>Streak</h3>
        <p className="loading-text">Made a mistake or want a fresh start?</p>
        <button className="btn btn-secondary" onClick={handleResetStreak}>Reset Streak to 0</button>
      </div>

      {/* ── DATA & ACCOUNT (danger zone) ── */}
      <div className="dashboard-card">
        <h3>Data & Account</h3>
        <p className="loading-text">These actions are permanent and cannot be undone.</p>

        <button
          className="btn btn-secondary"
          style={{ borderColor: '#ff6b35', color: '#ff6b35', marginBottom: '1rem' }}
          onClick={handleDeleteData}
        >
          Delete All My Data
        </button>

        {!showDeleteConfirm ? (
          <button
            className="btn btn-secondary"
            style={{ borderColor: '#e53e3e', color: '#e53e3e' }}
            onClick={() => setShowDeleteConfirm(true)}
          >
            Delete Account
          </button>
        ) : (
          <div className="form-group">
            <label className="form-label">Enter your password to confirm</label>
            <input
              className="form-input"
              type="password"
              value={deletePassword}
              onChange={e => setDeletePassword(e.target.value)}
              placeholder="Password"
            />
            <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem' }}>
              <button
                className="btn btn-secondary"
                style={{ borderColor: '#e53e3e', color: '#e53e3e' }}
                onClick={handleDeleteAccount}
              >
                Confirm Delete Account
              </button>
              <button className="btn btn-secondary" onClick={() => { setShowDeleteConfirm(false); setDeletePassword('') }}>
                Cancel
              </button>
            </div>
          </div>
        )}
      </div>

      {/* ── LOGOUT ── */}
      <div className="dashboard-card">
        <button className="btn btn-primary" onClick={onLogout} style={{ width: '100%' }}>
          Logout
        </button>
      </div>

      {/* ── ABOUT ── */}
      <div className="dashboard-card" style={{ textAlign: 'center' }}>
        <p className="loading-text">CalorieLens v{APP_VERSION}</p>
      </div>
    </div>
  )
}

export default Settings
