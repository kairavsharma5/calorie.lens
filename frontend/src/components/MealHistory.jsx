import { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

export default function MealHistory({ user, onBack }) {
  const [meals, setMeals] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [deletingId, setDeletingId] = useState(null)

  useEffect(() => {
    fetchMeals()
  }, [])

  const fetchMeals = async () => {
    setLoading(true)
    setError('')

    try {
      const token = localStorage.getItem('token')

      const response = await axios.get(
        `${API_BASE_URL}/meals/history`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      if (response.data) {
        setMeals(response.data.meals || [])
      }
    } catch (err) {
      const errorMsg = err.response?.data?.error ||
        err.message ||
        'Failed to load meal history'
      setError(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  const deleteMeal = async (mealId) => {
    if (!window.confirm('Are you sure you want to delete this meal?')) {
      return
    }

    setDeletingId(mealId)
    setError('')

    try {
      const token = localStorage.getItem('token')

      await axios.delete(
        `${API_BASE_URL}/meals/${mealId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      setMeals(meals.filter(meal => meal.id !== mealId))

    } catch (err) {
      const errorMsg = err.response?.data?.error ||
        err.message ||
        'Failed to delete meal'
      setError(errorMsg)
    } finally {
      setDeletingId(null)
    }
  }

  const totalCalories = meals.reduce((sum, meal) => sum + (meal.calories || 0), 0)
  const totalProtein  = meals.reduce((sum, meal) => sum + (meal.macros?.protein || 0), 0)
  const totalCarbs    = meals.reduce((sum, meal) => sum + (meal.macros?.carbs || 0), 0)
  const totalFat      = meals.reduce((sum, meal) => sum + (meal.macros?.fat || 0), 0)

  return (
    <div className="results-container">
      <button
        className="btn btn-secondary"
        onClick={onBack}
        style={{ marginBottom: '2rem' }}
      >
        ← Back to Upload
      </button>

      <div className="results-header">
        <h2 className="results-title">📋 Meal History</h2>
        <p className="results-subtitle">All your logged meals</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p className="loading-text">Loading your meals...</p>
        </div>
      )}

      {!loading && meals.length === 0 && (
        <div className="analysis-section">
          <div className="analysis-title">📭 No meals logged yet</div>
          <div className="analysis-content">
            <p>Start logging your meals to see them here!</p>
            <button
              className="btn btn-primary"
              onClick={onBack}
              style={{ marginTop: '1rem' }}
            >
              Log a Meal
            </button>
          </div>
        </div>
      )}

      {!loading && meals.length > 0 && (
        <>
          <div className="nutrition-grid">
            <div className="nutrition-card">
              <div className="nutrition-label">Total Calories</div>
              <div className="nutrition-value">
                {totalCalories}
                <span className="nutrition-unit">kcal</span>
              </div>
            </div>
            <div className="nutrition-card">
              <div className="nutrition-label">Total Protein</div>
              <div className="nutrition-value">
                {totalProtein.toFixed(1)}
                <span className="nutrition-unit">g</span>
              </div>
            </div>
            <div className="nutrition-card">
              <div className="nutrition-label">Total Carbs</div>
              <div className="nutrition-value">
                {totalCarbs.toFixed(1)}
                <span className="nutrition-unit">g</span>
              </div>
            </div>
            <div className="nutrition-card">
              <div className="nutrition-label">Total Fat</div>
              <div className="nutrition-value">
                {totalFat.toFixed(1)}
                <span className="nutrition-unit">g</span>
              </div>
            </div>
          </div>

          <div style={{ marginTop: '2rem' }}>
            <h3 style={{
              color: 'var(--accent-orange)',
              marginBottom: '1rem',
              fontSize: '1.2rem'
            }}>
              Your Meals ({meals.length})
            </h3>

            {meals.map((meal) => (
              <div
                key={meal.id}
                className="analysis-section"
                style={{ marginBottom: '1rem' }}
              >
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginBottom: '1rem'
                }}>
                  <div>
                    <h4 style={{
                      color: 'var(--text-primary)',
                      fontSize: '1.1rem',
                      marginBottom: '0.25rem'
                    }}>
                      {meal.food_name}
                    </h4>
                    <p style={{
                      color: 'var(--text-secondary)',
                      fontSize: '0.85rem'
                    }}>
                      {meal.meal_type} • {meal.loggedAt}
                    </p>
                  </div>
                  <button
                    className="delete-btn"
                    onClick={() => deleteMeal(meal.id)}
                    disabled={deletingId === meal.id}
                  >
                    {deletingId === meal.id ? '⟳ Deleting...' : '🗑️ Delete'}
                  </button>
                </div>

                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(4, 1fr)',
                  gap: '1rem'
                }}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ color: 'var(--accent-orange)', fontSize: '1.3rem', fontWeight: 'bold' }}>
                      {meal.calories}
                    </div>
                    <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>kcal</div>
                  </div>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ color: 'var(--accent-orange)', fontSize: '1.3rem', fontWeight: 'bold' }}>
                      {meal.macros?.protein?.toFixed(1)}
                    </div>
                    <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>g protein</div>
                  </div>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ color: 'var(--accent-orange)', fontSize: '1.3rem', fontWeight: 'bold' }}>
                      {meal.macros?.carbs?.toFixed(1)}
                    </div>
                    <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>g carbs</div>
                  </div>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ color: 'var(--accent-orange)', fontSize: '1.3rem', fontWeight: 'bold' }}>
                      {meal.macros?.fat?.toFixed(1)}
                    </div>
                    <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>g fat</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}