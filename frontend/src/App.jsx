import { useState, useEffect } from 'react'
import LoginForm from './components/LoginForm'
import UploadForm from './components/UploadForm'
import ResultsDisplay from './components/ResultsDisplay'
import MealHistory from './components/MealHistory'
import Dashboard from './components/Dashboard'
import MainMenu from './components/MainMenu'
import Chatbot from './components/Chatbot'
import Settings from './components/Settings'
import './App.css'

function App() {
  // app now starts on the splash screen, not login
  const [currentScreen, setCurrentScreen] = useState('splash')
  const [user, setUser] = useState(null)
  const [analysisResults, setAnalysisResults] = useState(null)

  // ─────────────────────────────────────────
  // SPLASH SCREEN — runs once when the app first loads
  // Shows the animated logo, then decides where to send the user:
  // straight to the menu (already logged in) or to login (not logged in)
  // ─────────────────────────────────────────
  useEffect(() => {
    const timer = setTimeout(() => {
      const token    = localStorage.getItem('token')
      const username = localStorage.getItem('username')

      if (token && username) {
        setUser({ token, username })
        setCurrentScreen('menu')
      } else {
        setCurrentScreen('login')
      }
    }, 2000) // splash stays visible for 2 seconds

    // cleanup: cancel the timer if the component unmounts early
    return () => clearTimeout(timer)
  }, [])

  // ─────────────────────────────────────────
  // WELCOME SCREEN — runs only right after a fresh login
  // Shows "Welcome back, {username}!" then auto-moves to the menu
  // ─────────────────────────────────────────
  useEffect(() => {
    if (currentScreen === 'welcome') {
      const timer = setTimeout(() => {
        setCurrentScreen('menu')
      }, 1500) // welcome message stays for 1.5 seconds

      return () => clearTimeout(timer)
    }
  }, [currentScreen])

  const handleLoginSuccess = (userData) => {
    setUser(userData)
    setCurrentScreen('welcome') // go to the greeting, not straight to menu
  }

  const handleAnalysisComplete = (results) => {
    setAnalysisResults(results)
    setCurrentScreen('results')
  }

  const handleBackToUpload = () => {
    setAnalysisResults(null)
    setCurrentScreen('upload')
  }

  // generic navigation helper passed to MainMenu
  const handleNavigate = (screen) => {
    setCurrentScreen(screen)
  }

  // generic "go back to the hub" used by every sub-screen now
  const handleBackToMenu = () => {
    setCurrentScreen('menu')
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    setUser(null)
    setAnalysisResults(null)
    setCurrentScreen('login')
  }

  // ─────────────────────────────────────────
  // SPLASH SCREEN — full-screen, image background, no header/footer
  // ─────────────────────────────────────────
  if (currentScreen === 'splash') {
    return (
      <div className="splash-screen">
        <div className="splash-content">
          <div className="splash-icon">🍽️</div>
          <h1 className="splash-title">CalorieLens</h1>
          <p className="splash-greeting">AI-Powered Food & Nutrition Analyzer</p>
          <div className="splash-loader">
            <span className="splash-dot"></span>
            <span className="splash-dot"></span>
            <span className="splash-dot"></span>
          </div>
        </div>
      </div>
    )
  }

  // ─────────────────────────────────────────
  // WELCOME SCREEN — full-screen, image background, no header/footer
  // ─────────────────────────────────────────
  if (currentScreen === 'welcome') {
    return (
      <div className="splash-screen">
        <div className="splash-content">
          <div className="splash-icon">👋</div>
          <h1 className="splash-title">Welcome back!</h1>
          <p className="splash-greeting">Hey {user?.username}, great to see you again</p>
        </div>
      </div>
    )
  }

  // ─────────────────────────────────────────
  // LOGIN SCREEN — full-screen, image background, no header/footer
  // (previously this was inline inside the normal layout — now it
  // gets the same aesthetic hero-image treatment as splash/welcome)
  // ─────────────────────────────────────────
  if (currentScreen === 'login') {
    return (
      <div className="auth-screen">
        <div className="auth-content">
          <LoginForm onLoginSuccess={handleLoginSuccess} />
        </div>
      </div>
    )
  }

  // ─────────────────────────────────────────
  // NORMAL APP LAYOUT — everything else
  // ─────────────────────────────────────────
  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">🍽️ CalorieLens</h1>
          <p className="app-subtitle">AI-Powered Food & Nutrition Analyzer</p>
          {user && (
            <div className="user-info">
              <span>Welcome, {user.username}!</span>
              {currentScreen !== 'menu' && (
                <button
                  className="logout-btn"
                  onClick={handleBackToMenu}
                  style={{ marginRight: '0.5rem' }}
                >
                  🏠 Menu
                </button>
              )}
              <button className="logout-btn" onClick={handleLogout}>
                Logout
              </button>
            </div>
          )}
        </div>
      </header>

      <main className="app-main">
        {currentScreen === 'menu' && user && (
          <MainMenu username={user.username} onNavigate={handleNavigate} />
        )}

        {currentScreen === 'upload' && user && (
          <UploadForm
            user={user}
            onAnalysisComplete={handleAnalysisComplete}
          />
        )}

        {currentScreen === 'results' && analysisResults && (
          <ResultsDisplay
            results={analysisResults}
            onBack={handleBackToUpload}
          />
        )}

        {currentScreen === 'history' && user && (
          <MealHistory
            user={user}
            onBack={handleBackToMenu}
          />
        )}

        {currentScreen === 'dashboard' && user && (
          <Dashboard
            user={user}
            onBack={handleBackToMenu}
            onLogMeal={() => handleNavigate('upload')}
            onViewHistory={() => handleNavigate('history')}
          />
        )}

        {currentScreen === 'chatbot' && user && (
          <Chatbot user={user} onBack={handleBackToMenu} />
        )}

        {currentScreen === 'settings' && user && (
          <Settings
            user={user}
            onBack={handleBackToMenu}
            onLogout={handleLogout}
          />
        )}
      </main>

      <footer className="app-footer">
        <p>&copy; 2026 CalorieLens. Powered by AI.</p>
      </footer>
    </div>
  )
}

export default App
