import { useState } from 'react'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

export default function LoginForm({ onLoginSuccess }) {
  const [isLogin, setIsLogin] = useState(true)
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  // ── OTP STEP STATE ──────────────────────
  // when true, we show the OTP box instead of the register/login form
  const [awaitingOtp, setAwaitingOtp] = useState(false)
  const [otp, setOtp] = useState('')
  const [otpMessage, setOtpMessage] = useState('')

  // ── FORGOT PASSWORD STATE ──────────────────────
  const [showForgotPassword, setShowForgotPassword] = useState(false)
  const [forgotEmail, setForgotEmail] = useState('')
  const [awaitingResetOtp, setAwaitingResetOtp] = useState(false)
  const [resetOtp, setResetOtp] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmNewPassword, setConfirmNewPassword] = useState('')

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    setError('')
  }

  const isValidEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (!formData.email || !formData.password) {
        setError('Email and password are required')
        setLoading(false)
        return
      }

      if (!isValidEmail(formData.email)) {
        setError('Please enter a valid email address')
        setLoading(false)
        return
      }

      if (!isLogin) {
        if (!formData.username) {
          setError('Username is required')
          setLoading(false)
          return
        }

        if (formData.password !== formData.confirmPassword) {
          setError('Passwords do not match')
          setLoading(false)
          return
        }

        if (formData.password.length < 6) {
          setError('Password must be at least 6 characters')
          setLoading(false)
          return
        }

        // register — this now creates an UNVERIFIED account and
        // sends an OTP by email, instead of logging in right away
        await axios.post(`${API_BASE_URL}/auth/register`, {
          username: formData.username,
          email: formData.email,
          password: formData.password
        })

        // move to the OTP entry screen instead of auto-login
        setOtpMessage(`We sent a 6-digit code to ${formData.email}`)
        setAwaitingOtp(true)
      } else {
        // login — backend will reject this with needs_verification
        // if the account was never verified
        const response = await axios.post(`${API_BASE_URL}/auth/login`, {
          email: formData.email,
          password: formData.password
        })

        const token = response.data.token
        const username = response.data.username

        localStorage.setItem('token', token)
        localStorage.setItem('username', username)

        onLoginSuccess({ username, token })
      }
    } catch (err) {
      // if login failed specifically because the account isn't verified yet,
      // send them straight to the OTP screen instead of just showing an error
      if (err.response?.data?.needs_verification) {
        setOtpMessage(`Your email isn't verified yet. Enter the code sent to ${formData.email}`)
        setAwaitingOtp(true)
      } else {
        const errorMsg = err.response?.data?.error || err.message || 'An error occurred'
        setError(errorMsg)
      }
    } finally {
      setLoading(false)
    }
  }

  // ── VERIFY OTP ──────────────────────
  const handleVerifyOtp = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await axios.post(`${API_BASE_URL}/auth/verify-otp`, {
        email: formData.email,
        otp: otp
      })

      const token = response.data.token
      const username = response.data.username

      localStorage.setItem('token', token)
      localStorage.setItem('username', username)

      // verified and logged in in one step
      onLoginSuccess({ username, token })
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Invalid or expired OTP'
      setError(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  // ── RESEND OTP ──────────────────────
  const handleResendOtp = async () => {
    setError('')
    try {
      await axios.post(`${API_BASE_URL}/auth/resend-otp`, { email: formData.email })
      setOtpMessage(`A new code was sent to ${formData.email}`)
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to resend OTP')
    }
  }

  // ── FORGOT PASSWORD: SEND OTP ──────────────────────
  const handleForgotPasswordSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await axios.post(`${API_BASE_URL}/auth/forgot-password`, { email: forgotEmail })
      setAwaitingResetOtp(true)
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to send reset code')
    } finally {
      setLoading(false)
    }
  }

  // ── FORGOT PASSWORD: VERIFY OTP + SET NEW PASSWORD ──────────────────────
  const handleResetPasswordSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (newPassword !== confirmNewPassword) {
      setError('Passwords do not match')
      return
    }
    if (newPassword.length < 6) {
      setError('Password must be at least 6 characters')
      return
    }

    setLoading(true)
    try {
      await axios.post(`${API_BASE_URL}/auth/reset-password`, {
        email: forgotEmail,
        otp: resetOtp,
        new_password: newPassword
      })

      // success — send them back to the normal login form
      setShowForgotPassword(false)
      setAwaitingResetOtp(false)
      setForgotEmail('')
      setResetOtp('')
      setNewPassword('')
      setConfirmNewPassword('')
      setError('')
      setOtpMessage('')
      alert('Password reset successfully. Please log in with your new password.')
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to reset password')
    } finally {
      setLoading(false)
    }
  }

  const toggleForm = () => {
    setIsLogin(!isLogin)
    setFormData({ username: '', email: '', password: '', confirmPassword: '' })
    setError('')
  }

  // ─────────────────────────────────────────
  // OTP ENTRY SCREEN (shown after register, or if login says unverified)
  // ─────────────────────────────────────────
  if (awaitingOtp) {
    return (
      <div className="form-container login-form">
        <h2 className="form-title">📧 Verify Your Email</h2>
        <p className="form-subtitle">{otpMessage}</p>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleVerifyOtp}>
          <div className="form-group">
            <label className="form-label">Enter 6-Digit Code</label>
            <input
              type="text"
              className="form-input"
              placeholder="000000"
              maxLength={6}
              value={otp}
              onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))}
              disabled={loading}
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading || otp.length !== 6}>
            {loading ? 'Verifying...' : 'Verify & Continue'}
          </button>
        </form>

        <div className="toggle-form">
          Didn't get the code?
          <button type="button" onClick={handleResendOtp} disabled={loading}>
            Resend Code
          </button>
        </div>
      </div>
    )
  }

  // ─────────────────────────────────────────
  // FORGOT PASSWORD — STEP 1: enter email
  // ─────────────────────────────────────────
  if (showForgotPassword && !awaitingResetOtp) {
    return (
      <div className="form-container login-form">
        <h2 className="form-title">🔑 Forgot Password</h2>
        <p className="form-subtitle">We'll email you a code to reset it</p>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleForgotPasswordSubmit}>
          <div className="form-group">
            <label className="form-label">Email Address</label>
            <input
              type="email"
              className="form-input"
              placeholder="Enter your email"
              value={forgotEmail}
              onChange={(e) => setForgotEmail(e.target.value)}
              disabled={loading}
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Sending...' : 'Send Reset Code'}
          </button>
        </form>

        <div className="toggle-form">
          <button type="button" onClick={() => { setShowForgotPassword(false); setError('') }} disabled={loading}>
            Back to Login
          </button>
        </div>
      </div>
    )
  }

  // ─────────────────────────────────────────
  // FORGOT PASSWORD — STEP 2: enter OTP + new password
  // ─────────────────────────────────────────
  if (showForgotPassword && awaitingResetOtp) {
    return (
      <div className="form-container login-form">
        <h2 className="form-title">🔑 Reset Password</h2>
        <p className="form-subtitle">Enter the code sent to {forgotEmail}</p>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleResetPasswordSubmit}>
          <div className="form-group">
            <label className="form-label">6-Digit Code</label>
            <input
              type="text"
              className="form-input"
              placeholder="000000"
              maxLength={6}
              value={resetOtp}
              onChange={(e) => setResetOtp(e.target.value.replace(/\D/g, ''))}
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label className="form-label">New Password</label>
            <input
              type="password"
              className="form-input"
              placeholder="Enter new password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Confirm New Password</label>
            <input
              type="password"
              className="form-input"
              placeholder="Confirm new password"
              value={confirmNewPassword}
              onChange={(e) => setConfirmNewPassword(e.target.value)}
              disabled={loading}
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Resetting...' : 'Reset Password'}
          </button>
        </form>
      </div>
    )
  }

  // ─────────────────────────────────────────
  // NORMAL LOGIN / REGISTER FORM
  // ─────────────────────────────────────────
  return (
    <div className="form-container login-form">
      <h2 className="form-title">
        {isLogin ? '🔓 Login' : '✍️ Create Account'}
      </h2>
      <p className="form-subtitle">
        {isLogin
          ? 'Welcome back to CalorieLens'
          : 'Join CalorieLens and start tracking your meals'}
      </p>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit}>
        {!isLogin && (
          <div className="form-group">
            <label className="form-label">Username</label>
            <input
              type="text"
              className="form-input"
              placeholder="Choose a username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              disabled={loading}
            />
          </div>
        )}

        <div className="form-group">
          <label className="form-label">Email Address</label>
          <input
            type="email"
            className="form-input"
            placeholder="Enter your email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label className="form-label">Password</label>
          <input
            type="password"
            className="form-input"
            placeholder="Enter your password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            disabled={loading}
          />
        </div>

        {!isLogin && (
          <div className="form-group">
            <label className="form-label">Confirm Password</label>
            <input
              type="password"
              className="form-input"
              placeholder="Confirm your password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              disabled={loading}
            />
          </div>
        )}

        <button
          type="submit"
          className="btn btn-primary"
          disabled={loading}
        >
          {loading
            ? (isLogin ? 'Logging in...' : 'Creating account...')
            : (isLogin ? 'Login' : 'Create Account')}
        </button>
      </form>

      {isLogin && (
        <div className="toggle-form">
          <button type="button" onClick={() => setShowForgotPassword(true)} disabled={loading}>
            Forgot Password?
          </button>
        </div>
      )}

      <div className="toggle-form">
        {isLogin ? "Don't have an account?" : 'Already have an account?'}
        <button type="button" onClick={toggleForm} disabled={loading}>
          {isLogin ? 'Sign Up' : 'Login'}
        </button>
      </div>
    </div>
  )
}
