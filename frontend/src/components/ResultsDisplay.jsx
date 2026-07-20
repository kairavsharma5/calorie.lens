import { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

export default function ResultsDisplay({ results, onBack }) {
  const [saving, setSaving]   = useState(false)
  const [saved, setSaved]     = useState(false)
  const [error, setError]     = useState('')

  const foodName      = results?.foodName      || 'Unknown Food'
  const baseCalories  = results?.calories      || 0
  const baseProtein   = results?.protein       || 0
  const baseCarbs     = results?.carbs         || 0
  const baseFat       = results?.fat           || 0
  const mealType      = results?.meal_type     || 'lunch'
  const source        = results?.source        || 'api'
  const perPieceGrams = results?.per_piece_grams || null
  const pieceName     = results?.piece_name    || 'piece'

  // does this food have piece data at all? (regardless of what the
  // backend picked as the DEFAULT unit) — this decides if we show the toggle
  const canBePieces = perPieceGrams !== null && perPieceGrams !== undefined

  // "mode" is what the USER has chosen right now — starts from the
  // backend's suggested default, but the user can flip it anytime
  const defaultMode = results?.unit_type === 'piece' && canBePieces ? 'piece' : 'g'
  const [mode, setMode]         = useState(defaultMode)
  const [quantity, setQuantity] = useState(1)

  // if a new food comes in (user analyzed something else), reset mode/qty
  useEffect(() => {
    setMode(defaultMode)
    setQuantity(1)
  }, [results])

  // calculate actual grams based on current mode + quantity
  const actualGrams = mode === 'piece'
    ? quantity * (perPieceGrams || 100)
    : quantity

  // scale nutrition based on actual grams vs base 100g
  const scaleFactor = actualGrams / 100
  const calories    = baseCalories * scaleFactor
  const protein     = baseProtein  * scaleFactor
  const carbs       = baseCarbs    * scaleFactor
  const fat         = baseFat      * scaleFactor

  const formatNum = (num) => (typeof num === 'number' ? num.toFixed(1) : '0')

  const handleQuantityChange = (e) => {
    const value = parseFloat(e.target.value)
    if (!isNaN(value) && value >= 0) {
      setQuantity(value)
    }
  }

  // switching mode resets quantity to a sensible starting point
  // so numbers don't carry over weirdly (e.g. "50" grams becoming "50" pieces)
  const switchMode = (newMode) => {
    if (newMode === mode) return
    setMode(newMode)
    setQuantity(newMode === 'piece' ? 1 : 100)
  }

  const handleSave = async () => {
    setSaving(true)
    setError('')

    try {
      const token = localStorage.getItem('token')

      const mealName = mode === 'piece'
        ? `${foodName} (${quantity} ${quantity === 1 ? pieceName : pieceName + 's'})`
        : `${foodName} (${quantity}g)`

      await axios.post(
        `${API_BASE_URL}/meals/log`,
        {
          food_name: mealName,
          calories:  Math.round(calories  * 10) / 10,
          protein:   Math.round(protein   * 10) / 10,
          carbs:     Math.round(carbs     * 10) / 10,
          fat:       Math.round(fat       * 10) / 10,
          meal_type: mealType
        },
        { headers: { Authorization: `Bearer ${token}` } }
      )

      setSaved(true)
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to save meal')
    } finally {
      setSaving(false)
    }
  }

  const getSourceLabel = () => {
    switch(source) {
      case 'indian_database': return '🇮🇳 From Indian food database'
      case 'database':        return '⚡ Found in our database'
      case 'your_foods':      return '📝 From your saved foods'
      case 'manual':          return '✍️ Manually entered'
      case 'usda':            return '🌐 Fetched from USDA'
      case 'image_scan':      return '📷 Identified from photo'
      default:                return '🌐 Fetched from database'
    }
  }

  return (
    <div className="results-container">
      <button
        className="btn btn-secondary"
        onClick={onBack}
        style={{ marginBottom: '2rem' }}
      >
        ← Analyze Another Meal
      </button>

      <div className="results-header">
        <h2 className="results-title">🍽️ {foodName}</h2>
        <p className="results-subtitle">{getSourceLabel()}</p>
      </div>

      {/* Quantity Input */}
      <div style={{
        padding:         '1.25rem',
        backgroundColor: 'var(--tertiary-dark)',
        borderRadius:    '8px',
        marginBottom:    '1.5rem',
        border:          '1px solid var(--accent-orange)'
      }}>

        {/* Mode toggle — only shown if this food has piece data available */}
        {canBePieces && (
          <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
            <button
              onClick={() => switchMode('g')}
              style={{
                flex:            1,
                padding:         '0.5rem',
                borderRadius:    '6px',
                border:          '1px solid var(--border-color)',
                cursor:          'pointer',
                fontWeight:      mode === 'g' ? 'bold' : 'normal',
                backgroundColor: mode === 'g' ? 'var(--accent-orange)' : 'var(--secondary-dark)',
                color:           mode === 'g' ? '#000' : 'var(--text-primary)'
              }}
            >
              ⚖️ Grams
            </button>
            <button
              onClick={() => switchMode('piece')}
              style={{
                flex:            1,
                padding:         '0.5rem',
                borderRadius:    '6px',
                border:          '1px solid var(--border-color)',
                cursor:          'pointer',
                fontWeight:      mode === 'piece' ? 'bold' : 'normal',
                backgroundColor: mode === 'piece' ? 'var(--accent-orange)' : 'var(--secondary-dark)',
                color:           mode === 'piece' ? '#000' : 'var(--text-primary)'
              }}
            >
              🔢 {pieceName.charAt(0).toUpperCase() + pieceName.slice(1)}s
            </button>
          </div>
        )}

        {mode === 'piece' ? (
          <>
            <label className="form-label" style={{ marginBottom: '0.5rem', display: 'block' }}>
              🔢 How many {pieceName}s did you eat?
            </label>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <button
                onClick={() => setQuantity(q => Math.max(0.5, q - 0.5))}
                style={{
                  padding:         '0.5rem 1rem',
                  backgroundColor: 'var(--secondary-dark)',
                  border:          '1px solid var(--border-color)',
                  borderRadius:    '6px',
                  color:           'var(--text-primary)',
                  cursor:          'pointer',
                  fontSize:        '1.2rem'
                }}
              >−</button>
              <input
                type="number"
                className="form-input"
                value={quantity}
                onChange={handleQuantityChange}
                min="0.5"
                step="0.5"
                style={{ flex: 1, textAlign: 'center' }}
              />
              <button
                onClick={() => setQuantity(q => q + 0.5)}
                style={{
                  padding:         '0.5rem 1rem',
                  backgroundColor: 'var(--secondary-dark)',
                  border:          '1px solid var(--border-color)',
                  borderRadius:    '6px',
                  color:           'var(--text-primary)',
                  cursor:          'pointer',
                  fontSize:        '1.2rem'
                }}
              >+</button>
              <span style={{ color: 'var(--text-secondary)', minWidth: '60px' }}>
                {quantity === 1 ? pieceName : pieceName + 's'}
              </span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '0.5rem' }}>
              1 {pieceName} ≈ {perPieceGrams}g · Total: {actualGrams}g
            </p>
          </>
        ) : (
          <>
            <label className="form-label" style={{ marginBottom: '0.5rem', display: 'block' }}>
              ⚖️ How much did you eat? (grams)
            </label>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <button
                onClick={() => setQuantity(q => Math.max(10, q - 10))}
                style={{
                  padding:         '0.5rem 1rem',
                  backgroundColor: 'var(--secondary-dark)',
                  border:          '1px solid var(--border-color)',
                  borderRadius:    '6px',
                  color:           'var(--text-primary)',
                  cursor:          'pointer',
                  fontSize:        '1.2rem'
                }}
              >−</button>
              <input
                type="number"
                className="form-input"
                value={quantity}
                onChange={handleQuantityChange}
                min="0"
                step="10"
                style={{ flex: 1, textAlign: 'center' }}
              />
              <button
                onClick={() => setQuantity(q => q + 10)}
                style={{
                  padding:         '0.5rem 1rem',
                  backgroundColor: 'var(--secondary-dark)',
                  border:          '1px solid var(--border-color)',
                  borderRadius:    '6px',
                  color:           'var(--text-primary)',
                  cursor:          'pointer',
                  fontSize:        '1.2rem'
                }}
              >+</button>
              <span style={{ color: 'var(--text-secondary)' }}>grams</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '0.5rem' }}>
              Base values are per 100g. Nutrition adjusts automatically.
            </p>
          </>
        )}
      </div>

      {/* Nutrition Grid */}
      <div className="nutrition-grid">
        <div className="nutrition-card">
          <div className="nutrition-label">Calories</div>
          <div className="nutrition-value">
            {formatNum(calories)}
            <span className="nutrition-unit">kcal</span>
          </div>
        </div>
        <div className="nutrition-card">
          <div className="nutrition-label">Protein</div>
          <div className="nutrition-value">
            {formatNum(protein)}
            <span className="nutrition-unit">g</span>
          </div>
        </div>
        <div className="nutrition-card">
          <div className="nutrition-label">Carbs</div>
          <div className="nutrition-value">
            {formatNum(carbs)}
            <span className="nutrition-unit">g</span>
          </div>
        </div>
        <div className="nutrition-card">
          <div className="nutrition-label">Fat</div>
          <div className="nutrition-value">
            {formatNum(fat)}
            <span className="nutrition-unit">g</span>
          </div>
        </div>
      </div>

      {/* Summary */}
      <div className="analysis-section">
        <div className="analysis-title">📊 Summary</div>
        <div className="analysis-content">
          <p>
            {mode === 'piece'
              ? <><strong>{quantity} {quantity === 1 ? pieceName : pieceName + 's'}</strong> of <strong>{foodName}</strong></>
              : <><strong>{quantity}g</strong> of <strong>{foodName}</strong>
              </>
            }{' '}
            contains approximately <strong>{formatNum(calories)} calories</strong> with{' '}
            <strong>{formatNum(protein)}g protein</strong>,{' '}
            <strong>{formatNum(carbs)}g carbs</strong>, and{' '}
            <strong>{formatNum(fat)}g fat</strong>.
          </p>
          <p style={{ marginTop: '1rem' }}>
            {calories > 800
              ? 'This is a substantial meal. Consider balancing it with lighter meals.'
              : calories > 400
              ? 'This is a well-balanced meal portion.'
              : 'This is a light meal. Consider adding more if needed.'}
          </p>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      {!saved ? (
        <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}>
          <button
            className="btn btn-primary"
            onClick={handleSave}
            disabled={saving || quantity <= 0}
            style={{ flex: 1 }}
          >
            {saving
              ? 'Saving...'
              : mode === 'piece'
              ? `💾 Save ${quantity} ${quantity === 1 ? pieceName : pieceName + 's'}`
              : `💾 Save ${quantity}g to My Meals`
            }
          </button>
          <button
            className="btn btn-secondary"
            onClick={onBack}
          >
            ❌ Discard
          </button>
        </div>
      ) : (
        <div style={{
          marginTop:       '2rem',
          padding:         '1rem',
          backgroundColor: 'rgba(0, 200, 100, 0.1)',
          borderRadius:    '6px',
          border:          '1px solid #00c864',
          textAlign:       'center'
        }}>
          <p style={{ color: '#00c864', fontSize: '1.1rem', fontWeight: 'bold' }}>
            ✅ Meal saved successfully!
          </p>
          <button
            className="btn btn-primary"
            onClick={onBack}
            style={{ marginTop: '1rem' }}
          >
            🍽️ Log Another Meal
          </button>
        </div>
      )}
    </div>
  )
}
