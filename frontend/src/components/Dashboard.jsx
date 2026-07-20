import { useState, useEffect } from 'react'

// ─────────────────────────────────────────
// DASHBOARD COMPONENT
// Shows: streak, today's meals (with delete), macros vs goals, goal editing,
// and quick-action buttons to log a new meal or view full history.
// Props:
//   user          - the logged-in user object (has .token)
//   onBack        - function to return to the main menu
//   onLogMeal     - function to navigate to the upload/log-meal screen
//   onViewHistory - function to navigate to the full meal history screen
// ─────────────────────────────────────────
function Dashboard({ user, onBack, onLogMeal, onViewHistory }) {
  // dashboard totals (streak, today's macros, goals)
  const [dashboardData, setDashboardData] = useState(null)

  // today's individual meals, pulled from /meals/history and filtered
  const [todaysMeals, setTodaysMeals] = useState([])

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // tracks which meal id is currently being deleted, so we can
  // disable just that one button instead of freezing the whole screen
  const [deletingId, setDeletingId] = useState(null)

  const [editingGoals, setEditingGoals] = useState(false)
  const [goalForm, setGoalForm] = useState({
    daily_calories: '',
    protein: '',
    carbs: '',
    fat: ''
  })
  const [savingGoals, setSavingGoals] = useState(false)

  // ─────────────────────────────────────────
  // Fetch dashboard totals + today's meal list together
  // ─────────────────────────────────────────
  const fetchDashboard = async () => {
    setLoading(true)
    setError('')

    try {
      // 1. get streak, goals, today's totals
      const dashboardResponse = await fetch(`${import.meta.env.VITE_API_URL}/user/dashboard`, {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${user.token}` }
      })
      const dashboardJson = await dashboardResponse.json()

      if (!dashboardResponse.ok) {
        throw new Error(dashboardJson.error || 'Failed to load dashboard')
      }

      setDashboardData(dashboardJson)
      setGoalForm({
        daily_calories: dashboardJson.goals.daily_calories,
        protein: dashboardJson.goals.protein,
        carbs: dashboardJson.goals.carbs,
        fat: dashboardJson.goals.fat
      })

      // 2. get full meal history, then filter down to just today's entries
      //    (the /user/dashboard endpoint only returns totals, not the list)
      const historyResponse = await fetch(`${import.meta.env.VITE_API_URL}/meals/history`, {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${user.token}` }
      })
      const historyJson = await historyResponse.json()

      if (historyResponse.ok) {
        // loggedAt looks like "2026-07-03 14:20" — comparing the first
        // 10 characters ("2026-07-03") tells us if a meal was today
        const todayStr = new Date().toISOString().slice(0, 10)
        const filtered = historyJson.meals.filter(
          meal => meal.loggedAt.slice(0, 10) === todayStr
        )
        setTodaysMeals(filtered)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchDashboard()
  }, [])

  // ─────────────────────────────────────────
  // Delete a meal, then refresh the dashboard so streak/totals stay accurate
  // ─────────────────────────────────────────
  const handleDeleteMeal = async (mealId) => {
    setDeletingId(mealId)
    setError('')

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/meals/${mealId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${user.token}` }
      })
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Failed to delete meal')
      }

      // re-fetch everything so streak, totals, and the meal list all stay in sync
      await fetchDashboard()
    } catch (err) {
      setError(err.message)
    } finally {
      setDeletingId(null)
    }
  }

  const handleGoalChange = (e) => {
    const { name, value } = e.target
    setGoalForm(prev => ({ ...prev, [name]: value }))
  }

  const handleSaveGoals = async (e) => {
    e.preventDefault()
    setSavingGoals(true)
    setError('')

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/user/goals`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${user.token}`
        },
        body: JSON.stringify({
          daily_calories: Number(goalForm.daily_calories),
          protein: Number(goalForm.protein),
          carbs: Number(goalForm.carbs),
          fat: Number(goalForm.fat)
        })
      })
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Failed to update goals')
      }

      setEditingGoals(false)
      await fetchDashboard()
    } catch (err) {
      setError(err.message)
    } finally {
      setSavingGoals(false)
    }
  }

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading">
          <div className="spinner"></div>
          <p className="loading-text">Loading your dashboard...</p>
        </div>
      </div>
    )
  }

  if (error && !dashboardData) {
    return (
      <div className="dashboard-container">
        <p className="error-message">{error}</p>
        <button className="btn btn-primary" onClick={fetchDashboard}>Try Again</button>
        <button className="btn btn-secondary" onClick={onBack}>Back</button>
      </div>
    )
  }

  const { streak, goals, today, remaining_calories } = dashboardData

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2>Your Dashboard</h2>
        <button className="btn btn-secondary" onClick={onBack}>← Back</button>
      </div>

      {error && <p className="error-message">{error}</p>}

      {/* ── STREAK CARD ── */}
      <div className="dashboard-card streak-card">
        <span className="streak-emoji">🔥</span>
        <span className="streak-number">{streak}</span>
        <span className="streak-label">
          {streak > 0 ? 'day streak — keep it going!' : 'day streak — start today!'}
        </span>
      </div>

      {/* ── TODAY'S MEALS LIST ── */}
      <div className="dashboard-card">
        <h3>🍽️ Today's Meals</h3>

        {todaysMeals.length > 0 ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {todaysMeals.map((meal) => (
              <div key={meal.id} className="macro-row" style={{ alignItems: 'center' }}>
                <div>
                  <div style={{ color: 'var(--text-primary)', fontWeight: 600 }}>
                    {meal.food_name}
                  </div>
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                    {meal.calories} kcal · P:{meal.macros.protein}g C:{meal.macros.carbs}g F:{meal.macros.fat}g
                  </div>
                </div>
                <button
                  className="delete-btn"
                  onClick={() => handleDeleteMeal(meal.id)}
                  disabled={deletingId === meal.id}
                >
                  {deletingId === meal.id ? '...' : '🗑️'}
                </button>
              </div>
            ))}
          </div>
        ) : (
          <p className="loading-text" style={{ textAlign: 'center', padding: '1rem 0' }}>
            No meals logged today yet
          </p>
        )}

        <button className="btn btn-primary" style={{ marginTop: '1rem' }} onClick={onLogMeal}>
          + Log New Meal
        </button>
      </div>

      {/* ── QUICK ACTION: view full history ── */}
      <button className="btn btn-secondary" style={{ width: '100%', marginBottom: '1.5rem' }} onClick={onViewHistory}>
        📋 View Previous Meals
      </button>

      {/* ── TODAY'S SUMMARY CARD ── */}
      <div className="dashboard-card">
        <h3>Today's Totals</h3>

        <div className="nutrition-grid-compact">
          <div className="nutrition-card-compact">
            <div className="nutrition-label">Calories</div>
            <div className={`nutrition-value ${today.calories > goals.daily_calories && goals.daily_calories > 0 ? 'over-goal' : ''}`}>
              {today.calories}
            </div>
            <div className="nutrition-sub">/ {goals.daily_calories}</div>
          </div>
          <div className="nutrition-card-compact">
            <div className="nutrition-label">Protein</div>
            <div className="nutrition-value">{today.protein}g</div>
            <div className="nutrition-sub">/ {goals.protein}g</div>
          </div>
          <div className="nutrition-card-compact">
            <div className="nutrition-label">Carbs</div>
            <div className="nutrition-value">{today.carbs}g</div>
            <div className="nutrition-sub">/ {goals.carbs}g</div>
          </div>
          <div className="nutrition-card-compact">
            <div className="nutrition-label">Fat</div>
            <div className="nutrition-value">{today.fat}g</div>
            <div className="nutrition-sub">/ {goals.fat}g</div>
          </div>
        </div>

        <p className="remaining-calories">
          {remaining_calories >= 0
            ? `${remaining_calories} calories remaining today`
            : `${Math.abs(remaining_calories)} calories over goal`}
        </p>
      </div>

      {/* ── GOALS CARD ── */}
      <div className="dashboard-card">
        <h3>Daily Goals</h3>

        {!editingGoals ? (
          <>
            <div className="nutrition-grid-compact">
              <div className="nutrition-card-compact">
                <div className="nutrition-label">Calories</div>
                <div className="nutrition-value">{goals.daily_calories}</div>
              </div>
              <div className="nutrition-card-compact">
                <div className="nutrition-label">Protein</div>
                <div className="nutrition-value">{goals.protein}g</div>
              </div>
              <div className="nutrition-card-compact">
                <div className="nutrition-label">Carbs</div>
                <div className="nutrition-value">{goals.carbs}g</div>
              </div>
              <div className="nutrition-card-compact">
                <div className="nutrition-label">Fat</div>
                <div className="nutrition-value">{goals.fat}g</div>
              </div>
            </div>
            <button
              className="btn btn-primary"
              style={{ marginTop: '1rem' }}
              onClick={() => setEditingGoals(true)}
            >
              ✏️ Edit Goals
            </button>
          </>
        ) : (
          <form onSubmit={handleSaveGoals} className="goal-form">
            <label>
              Daily Calories
              <input
                type="number"
                name="daily_calories"
                value={goalForm.daily_calories}
                onChange={handleGoalChange}
                required
              />
            </label>
            <label>
              Protein (g)
              <input
                type="number"
                name="protein"
                value={goalForm.protein}
                onChange={handleGoalChange}
                required
              />
            </label>
            <label>
              Carbs (g)
              <input
                type="number"
                name="carbs"
                value={goalForm.carbs}
                onChange={handleGoalChange}
                required
              />
            </label>
            <label>
              Fat (g)
              <input
                type="number"
                name="fat"
                value={goalForm.fat}
                onChange={handleGoalChange}
                required
              />
            </label>

            <div className="goal-form-buttons">
              <button type="submit" className="btn btn-primary" disabled={savingGoals}>
                {savingGoals ? 'Saving...' : 'Save Goals'}
              </button>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => setEditingGoals(false)}
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  )
}

export default Dashboard
