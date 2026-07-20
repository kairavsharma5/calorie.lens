// ─────────────────────────────────────────
// MAIN MENU COMPONENT
// The central hub — shows 4 big icon cards to navigate the app
// Props:
//   username    - for a friendly greeting at the top
//   onNavigate  - function(screenName) called when a card is clicked
// ─────────────────────────────────────────
function MainMenu({ username, onNavigate }) {
  return (
    <div className="menu-container">
      <h2 className="menu-title">What would you like to do, {username}?</h2>

      <div className="menu-grid">
        <div className="menu-card" onClick={() => onNavigate('dashboard')}>
          <span className="menu-icon">📊</span>
          <h3>Dashboard</h3>
          <p>View your streak, today's macros, and goals</p>
        </div>

        <div className="menu-card" onClick={() => onNavigate('chatbot')}>
          <span className="menu-icon">🤖</span>
          <h3>AI Nutritionist</h3>
          <p>Chat with your AI nutrition coach</p>
        </div>

        <div className="menu-card" onClick={() => onNavigate('upload')}>
          <span className="menu-icon">📸</span>
          <h3>Log a Meal</h3>
          <p>Snap or search food to track it</p>
        </div>

        <div className="menu-card" onClick={() => onNavigate('settings')}>
          <span className="menu-icon">⚙️</span>
          <h3>Settings</h3>
          <p>Manage your profile and preferences</p>
        </div>
      </div>
    </div>
  )
}

export default MainMenu
