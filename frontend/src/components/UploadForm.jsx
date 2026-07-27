import { useState, useEffect, useRef } from 'react'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

export default function UploadForm({ user, onAnalysisComplete }) {
  // ── MODE: 'search' (type a name) or 'scan' (photo) ──────────────────
  const [mode, setMode] = useState('search')

  const [formData, setFormData] = useState({
    food_name: '',
    meal_type: 'lunch'
  })
  const [manualData, setManualData] = useState({
    calories: '',
    protein: '',
    carbs: '',
    fat: ''
  })
  const [loading, setLoading]           = useState(false)
  const [error, setError]               = useState('')
  const [notFound, setNotFound]         = useState(false)
  const [suggestions, setSuggestions]   = useState([])
  const [showDropdown, setShowDropdown] = useState(false)
  const dropdownRef                     = useRef(null)

  // ── IMAGE SCAN STATE ──────────────────────
  const [imagePreview, setImagePreview] = useState(null)   // for showing the photo on screen
  const [imageBase64, setImageBase64]   = useState(null)   // what actually gets sent to the backend
  const [scanLoading, setScanLoading]   = useState(false)
  const [scanResult, setScanResult]     = useState(null)   // AI's answer, before the user confirms it
  const fileInputRef                    = useRef(null)     // used only for "choose from gallery"

  // ── IN-PAGE CAMERA STATE ──────────────────────
  // We use getUserMedia instead of handing off to the phone's native camera app.
  // Native camera hand-off backgrounds the browser tab, and on low-RAM phones
  // Android/Chrome often kills that backgrounded tab to free memory. When you
  // tap the tick to return, it looks like the site "refreshed" — really the
  // whole page (and all its state) was destroyed and reloaded from scratch.
  // Keeping the camera inside the page avoids that entirely.
  const [cameraActive, setCameraActive] = useState(false)
  const [cameraError, setCameraError]   = useState('')
  const videoRef                        = useRef(null)
  const canvasRef                       = useRef(null)
  const streamRef                       = useRef(null)

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setShowDropdown(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  // stop the camera stream whenever we leave scan mode or unmount,
  // so we don't leave the phone's camera light on in the background
  useEffect(() => {
    return () => stopCamera()
  }, [])

  const handleFoodNameChange = async (e) => {
    const value = e.target.value
    setFormData(prev => ({ ...prev, food_name: value }))
    setError('')
    setNotFound(false)

    if (value.length < 2) {
      setSuggestions([])
      setShowDropdown(false)
      return
    }

    try {
      const token    = localStorage.getItem('token')
      const response = await axios.get(
        `${API_BASE_URL}/foods/suggest?name=${value}`,
        { headers: { Authorization: `Bearer ${token}` } }
      )
      const suggs = response.data.suggestions || []
      setSuggestions(suggs)
      setShowDropdown(suggs.length > 0)
    } catch (err) {
      setShowDropdown(false)
    }
  }

  const handleSuggestionClick = (suggestion) => {
    setFormData(prev => ({ ...prev, food_name: suggestion }))
    setSuggestions([])
    setShowDropdown(false)
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    setError('')
  }

  const handleManualChange = (e) => {
    const { name, value } = e.target
    setManualData(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setNotFound(false)
    setLoading(true)
    setShowDropdown(false)

    try {
      if (!formData.food_name.trim()) {
        setError('Please enter a food name')
        setLoading(false)
        return
      }

      const token    = localStorage.getItem('token')
      const response = await axios.get(
        `${API_BASE_URL}/foods/search?name=${formData.food_name}`,
        { headers: { Authorization: `Bearer ${token}` } }
      )

      if (response.data) {
        onAnalysisComplete({
          foodName:        response.data.name,
          calories:        response.data.calories,
          protein:         response.data.macros?.protein || 0,
          carbs:           response.data.macros?.carbs   || 0,
          fat:             response.data.macros?.fat     || 0,
          meal_type:       formData.meal_type,
          source:          response.data.source,
          unit_type:       response.data.unit_type       || 'g',
          per_piece_grams: response.data.per_piece_grams || 100,
          piece_name:      response.data.piece_name      || 'piece'
        })
      }
    } catch (err) {
      if (err.response?.status === 404) {
        setNotFound(true)
        setError(err.response?.data?.error || 'Food not found')
      } else {
        setError(err.response?.data?.error || err.message || 'Something went wrong')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleManualSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (!manualData.calories) {
        setError('Please enter calories')
        setLoading(false)
        return
      }

      const token = localStorage.getItem('token')

      await axios.post(
        `${API_BASE_URL}/foods/add`,
        {
          name:     formData.food_name,
          calories: parseFloat(manualData.calories),
          protein:  parseFloat(manualData.protein) || 0,
          carbs:    parseFloat(manualData.carbs)   || 0,
          fat:      parseFloat(manualData.fat)     || 0
        },
        { headers: { Authorization: `Bearer ${token}` } }
      )

      onAnalysisComplete({
        foodName:        formData.food_name,
        calories:        parseFloat(manualData.calories),
        protein:         parseFloat(manualData.protein) || 0,
        carbs:           parseFloat(manualData.carbs)   || 0,
        fat:             parseFloat(manualData.fat)     || 0,
        meal_type:       formData.meal_type,
        source:          'manual',
        unit_type:       'g',
        per_piece_grams: 100,
        piece_name:      'piece'
      })
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to save custom food')
    } finally {
      setLoading(false)
    }
  }

  // ── IMAGE CHOSEN FROM GALLERY ──────────────────────
  // reads the chosen file, converts it to base64 (a text format the
  // backend can send straight to Groq's vision API), and shows a preview
  const handleImageSelect = (e) => {
    const file = e.target.files[0]
    if (!file) return

    setError('')
    setScanResult(null)

    // basic size guard — big photos take longer and cost more tokens
    if (file.size > 4 * 1024 * 1024) {
      setError('Image is too large. Please choose a photo under 4MB.')
      return
    }

    const reader = new FileReader()
    reader.onloadend = () => {
      setImagePreview(reader.result)   // this is already a data URL, good for <img src=...>
      setImageBase64(reader.result)    // same value — this is what we send to the backend
    }
    reader.readAsDataURL(file)
  }

  // ── OPEN IN-PAGE CAMERA ──────────────────────
  // Stays inside the browser tab the whole time — no OS camera app,
  // no backgrounding, no risk of the tab getting killed on low-RAM phones.
  const startCamera = async () => {
    setCameraError('')
    setError('')
    setScanResult(null)

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: { ideal: 'environment' } },
        audio: false
      })
      streamRef.current = stream
      setCameraActive(true)

      // videoRef isn't mounted until after this render, so attach on next tick
      setTimeout(() => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream
        }
      }, 0)
    } catch (err) {
      setCameraError(
        'Could not access camera. You may need to allow camera permission, or use "Choose from Gallery" instead.'
      )
    }
  }

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop())
      streamRef.current = null
    }
    setCameraActive(false)
  }

  // ── CAPTURE A FRAME FROM THE LIVE CAMERA ──────────────────────
  const handleCapturePhoto = () => {
    const video  = videoRef.current
    const canvas = canvasRef.current
    if (!video || !canvas) return

    canvas.width  = video.videoWidth
    canvas.height = video.videoHeight
    const ctx = canvas.getContext('2d')
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

    const dataUrl = canvas.toDataURL('image/jpeg', 0.9)
    setImagePreview(dataUrl)
    setImageBase64(dataUrl)

    stopCamera()
  }

  // ── SEND IMAGE TO BACKEND FOR ANALYSIS ──────────────────────
  const handleScanImage = async () => {
    if (!imageBase64) {
      setError('Please select or capture a photo first')
      return
    }

    setError('')
    setScanLoading(true)
    setScanResult(null)

    try {
      const token    = localStorage.getItem('token')
      const response = await axios.post(
        `${API_BASE_URL}/foods/scan-image`,
        { image: imageBase64 },
        { headers: { Authorization: `Bearer ${token}` } }
      )

      // don't log it yet — let the user review/correct the AI's guess first
      setScanResult({
        foodName: response.data.name,
        calories: response.data.calories,
        protein:  response.data.macros?.protein || 0,
        carbs:    response.data.macros?.carbs   || 0,
        fat:      response.data.macros?.fat     || 0,
        confidence: response.data.confidence,
        notes:      response.data.notes
      })
    } catch (err) {
      if (err.response?.status === 404) {
        setError(err.response?.data?.error || 'No food detected in this photo. Try a clearer photo or search by name instead.')
      } else {
        setError(err.response?.data?.error || 'Failed to analyze image')
      }
    } finally {
      setScanLoading(false)
    }
  }

  // ── EDIT A FIELD OF THE AI'S SCAN RESULT BEFORE CONFIRMING ──────────────────────
  const handleScanFieldChange = (field, value) => {
    setScanResult(prev => ({ ...prev, [field]: value }))
  }

  // ── CONFIRM AND LOG THE SCANNED FOOD ──────────────────────
  const handleConfirmScan = () => {
    onAnalysisComplete({
      foodName:        scanResult.foodName,
      calories:        parseFloat(scanResult.calories) || 0,
      protein:         parseFloat(scanResult.protein)  || 0,
      carbs:           parseFloat(scanResult.carbs)    || 0,
      fat:             parseFloat(scanResult.fat)      || 0,
      meal_type:       formData.meal_type,
      source:          'image_scan',
      unit_type:       'g',
      per_piece_grams: 100,
      piece_name:      'piece'
    })
  }

  const handleReset = () => {
    setFormData({ food_name: '', meal_type: 'lunch' })
    setManualData({ calories: '', protein: '', carbs: '', fat: '' })
    setError('')
    setNotFound(false)
    setSuggestions([])
    setShowDropdown(false)
    setImagePreview(null)
    setImageBase64(null)
    setScanResult(null)
    setCameraError('')
    stopCamera()
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  const switchMode = (newMode) => {
    setMode(newMode)
    handleReset()
  }

  return (
    <div className="form-container upload-form">
      <h2 className="form-title">🍽️ Log Your Meal</h2>
      <p className="form-subtitle">
        Welcome, {user.username}!
      </p>

      {/* ── MODE SWITCHER ── */}
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }}>
        <button
          type="button"
          className={mode === 'search' ? 'btn btn-primary' : 'btn btn-secondary'}
          style={{ flex: 1 }}
          onClick={() => switchMode('search')}
        >
          🔍 Search by Name
        </button>
        <button
          type="button"
          className={mode === 'scan' ? 'btn btn-primary' : 'btn btn-secondary'}
          style={{ flex: 1 }}
          onClick={() => switchMode('scan')}
        >
          📸 Scan a Photo
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {/* ═══════════════════════════════════════ */}
      {/* SEARCH MODE — your original flow, unchanged */}
      {/* ═══════════════════════════════════════ */}
      {mode === 'search' && (
        <>
          {!notFound ? (
            <form onSubmit={handleSubmit}>
              <div className="form-group" ref={dropdownRef} style={{ position: 'relative' }}>
                <label className="form-label">What did you eat?</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="e.g., Dal Rice, Biryani, Roti, Samosa..."
                  name="food_name"
                  value={formData.food_name}
                  onChange={handleFoodNameChange}
                  disabled={loading}
                  autoComplete="off"
                />

                {showDropdown && suggestions.length > 0 && (
                  <div style={{
                    position:        'absolute',
                    top:             '100%',
                    left:            0,
                    right:           0,
                    backgroundColor: 'var(--secondary-dark)',
                    border:          '1px solid var(--accent-orange)',
                    borderRadius:    '6px',
                    zIndex:          1000,
                    maxHeight:       '200px',
                    overflowY:       'auto',
                    marginTop:       '4px'
                  }}>
                    {suggestions.map((suggestion, index) => (
                      <div
                        key={index}
                        onClick={() => handleSuggestionClick(suggestion)}
                        style={{
                          padding:      '0.75rem 1rem',
                          cursor:       'pointer',
                          color:        'var(--text-primary)',
                          fontSize:     '0.95rem',
                          borderBottom: index < suggestions.length - 1
                            ? '1px solid var(--border-color)'
                            : 'none'
                        }}
                        onMouseEnter={e => e.target.style.backgroundColor = 'var(--tertiary-dark)'}
                        onMouseLeave={e => e.target.style.backgroundColor = 'transparent'}
                      >
                        {suggestion}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="form-group" style={{ marginTop: '1rem' }}>
                <label className="form-label">Meal Type</label>
                <select
                  className="form-input"
                  name="meal_type"
                  value={formData.meal_type}
                  onChange={handleChange}
                  disabled={loading}
                >
                  <option value="breakfast">Breakfast</option>
                  <option value="lunch">Lunch</option>
                  <option value="dinner">Dinner</option>
                  <option value="snack">Snack</option>
                </select>
              </div>

              <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={!formData.food_name.trim() || loading}
                  style={{ flex: 1 }}
                >
                  {loading ? '🔍 Searching...' : '🔍 Find Nutrition'}
                </button>

                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={handleReset}
                  disabled={loading}
                >
                  Clear
                </button>
              </div>
            </form>
          ) : (
            <form onSubmit={handleManualSubmit}>
              <div style={{
                padding:         '1rem',
                backgroundColor: 'var(--tertiary-dark)',
                borderRadius:    '6px',
                marginBottom:    '1rem'
              }}>
                <p style={{ color: 'var(--text-primary)' }}>
                  📝 Adding nutrition info for: <strong>{formData.food_name}</strong>
                </p>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '0.5rem' }}>
                  This will be saved privately for you so you don't have to enter it again.
                </p>
              </div>

              <div className="form-group">
                <label className="form-label">Calories (kcal)</label>
                <input
                  type="number"
                  className="form-input"
                  placeholder="e.g., 250"
                  name="calories"
                  value={manualData.calories}
                  onChange={handleManualChange}
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Protein (g)</label>
                <input
                  type="number"
                  className="form-input"
                  placeholder="e.g., 10"
                  name="protein"
                  value={manualData.protein}
                  onChange={handleManualChange}
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Carbs (g)</label>
                <input
                  type="number"
                  className="form-input"
                  placeholder="e.g., 30"
                  name="carbs"
                  value={manualData.carbs}
                  onChange={handleManualChange}
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Fat (g)</label>
                <input
                  type="number"
                  className="form-input"
                  placeholder="e.g., 8"
                  name="fat"
                  value={manualData.fat}
                  onChange={handleManualChange}
                  disabled={loading}
                />
              </div>

              <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={!manualData.calories || loading}
                  style={{ flex: 1 }}
                >
                  {loading ? 'Saving...' : '✅ Save & Continue'}
                </button>

                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={handleReset}
                  disabled={loading}
                >
                  ← Go Back
                </button>
              </div>
            </form>
          )}

          {!notFound && (
            <div style={{
              marginTop:       '2rem',
              padding:         '1rem',
              backgroundColor: 'var(--tertiary-dark)',
              borderRadius:    '6px',
              border:          '1px solid var(--border-color)'
            }}>
              <h3 style={{ color: 'var(--accent-orange)', marginBottom: '0.5rem' }}>
                💡 Tips:
              </h3>
              <ul className="analysis-list">
                <li>Start typing and suggestions will appear automatically</li>
                <li>Works for Indian food — Biryani, Chole, Dosa, Roti and more</li>
                <li>Can't find your food? You can add it manually</li>
              </ul>
            </div>
          )}
        </>
      )}

      {/* ═══════════════════════════════════════ */}
      {/* SCAN MODE — take/choose a photo, AI estimates nutrition */}
      {/* ═══════════════════════════════════════ */}
      {mode === 'scan' && (
        <div>
          {!scanResult ? (
            <>
              <div className="form-group">
                <label className="form-label">Meal Type</label>
                <select
                  className="form-input"
                  name="meal_type"
                  value={formData.meal_type}
                  onChange={handleChange}
                  disabled={scanLoading}
                >
                  <option value="breakfast">Breakfast</option>
                  <option value="lunch">Lunch</option>
                  <option value="dinner">Dinner</option>
                  <option value="snack">Snack</option>
                </select>
              </div>

              {cameraError && <div className="error-message">{cameraError}</div>}

              {/* ── LIVE IN-PAGE CAMERA ── */}
              {cameraActive ? (
                <div style={{ marginTop: '1rem' }}>
                  <div style={{ textAlign: 'center' }}>
                    <video
                      ref={videoRef}
                      autoPlay
                      playsInline
                      muted
                      style={{
                        width:        '100%',
                        maxHeight:    '400px',
                        borderRadius: '8px',
                        border:       '1px solid var(--border-color)',
                        backgroundColor: '#000'
                      }}
                    />
                  </div>
                  {/* hidden canvas used only to grab a still frame from the video */}
                  <canvas ref={canvasRef} style={{ display: 'none' }} />

                  <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                    <button
                      type="button"
                      className="btn btn-primary"
                      onClick={handleCapturePhoto}
                      style={{ flex: 1 }}
                    >
                      📸 Capture
                    </button>
                    <button
                      type="button"
                      className="btn btn-secondary"
                      onClick={stopCamera}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <>
                  {/* ── CHOOSE HOW TO GET A PHOTO ── */}
                  <div className="form-group">
                    <label className="form-label">Take or Choose a Photo</label>
                    <div style={{ display: 'flex', gap: '1rem' }}>
                      <button
                        type="button"
                        className="btn btn-primary"
                        onClick={startCamera}
                        disabled={scanLoading}
                        style={{ flex: 1 }}
                      >
                        📷 Open Camera
                      </button>
                      <button
                        type="button"
                        className="btn btn-secondary"
                        onClick={() => fileInputRef.current?.click()}
                        disabled={scanLoading}
                        style={{ flex: 1 }}
                      >
                        🖼️ Choose from Gallery
                      </button>
                    </div>
                    {/* No `capture` attribute here — this always opens the normal
                        file/gallery picker, never the native camera app */}
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept="image/*"
                      onChange={handleImageSelect}
                      disabled={scanLoading}
                      style={{ display: 'none' }}
                    />
                  </div>

                  {imagePreview && (
                    <div style={{ marginTop: '1rem', textAlign: 'center' }}>
                      <img
                        src={imagePreview}
                        alt="Selected food"
                        style={{
                          maxWidth:     '100%',
                          maxHeight:    '300px',
                          borderRadius: '8px',
                          border:       '1px solid var(--border-color)'
                        }}
                      />
                    </div>
                  )}

                  <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
                    <button
                      type="button"
                      className="btn btn-primary"
                      onClick={handleScanImage}
                      disabled={!imageBase64 || scanLoading}
                      style={{ flex: 1 }}
                    >
                      {scanLoading ? '🔍 Analyzing photo...' : '🔍 Analyze Photo'}
                    </button>

                    <button
                      type="button"
                      className="btn btn-secondary"
                      onClick={handleReset}
                      disabled={scanLoading}
                    >
                      Clear
                    </button>
                  </div>

                  <div style={{
                    marginTop:       '2rem',
                    padding:         '1rem',
                    backgroundColor: 'var(--tertiary-dark)',
                    borderRadius:    '6px',
                    border:          '1px solid var(--border-color)'
                  }}>
                    <h3 style={{ color: 'var(--accent-orange)', marginBottom: '0.5rem' }}>
                      💡 Tips:
                    </h3>
                    <ul className="analysis-list">
                      <li>Good lighting helps the AI identify food more accurately</li>
                      <li>Nutrition values are AI estimates — you can edit them before saving</li>
                      <li>Works best with one clear dish per photo</li>
                      <li>"Open Camera" stays inside the app so your progress isn't lost</li>
                    </ul>
                  </div>
                </>
              )}
            </>
          ) : (
            // ── REVIEW SCREEN — AI's guess, editable before logging ──
            <div>
              <div style={{
                padding:         '1rem',
                backgroundColor: 'var(--tertiary-dark)',
                borderRadius:    '6px',
                marginBottom:    '1rem'
              }}>
                <p style={{ color: 'var(--text-primary)' }}>
                  🤖 AI identified: <strong>{scanResult.foodName}</strong>
                </p>
                {scanResult.notes && (
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '0.5rem' }}>
                    {scanResult.notes}
                  </p>
                )}
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '0.5rem' }}>
                  Confidence: <strong>{scanResult.confidence}</strong> — please check the numbers below before saving.
                </p>
              </div>

              <div className="form-group">
                <label className="form-label">Food Name</label>
                <input
                  type="text"
                  className="form-input"
                  value={scanResult.foodName}
                  onChange={(e) => handleScanFieldChange('foodName', e.target.value)}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Calories (kcal)</label>
                <input
                  type="number"
                  className="form-input"
                  value={scanResult.calories}
                  onChange={(e) => handleScanFieldChange('calories', e.target.value)}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Protein (g)</label>
                <input
                  type="number"
                  className="form-input"
                  value={scanResult.protein}
                  onChange={(e) => handleScanFieldChange('protein', e.target.value)}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Carbs (g)</label>
                <input
                  type="number"
                  className="form-input"
                  value={scanResult.carbs}
                  onChange={(e) => handleScanFieldChange('carbs', e.target.value)}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Fat (g)</label>
                <input
                  type="number"
                  className="form-input"
                  value={scanResult.fat}
                  onChange={(e) => handleScanFieldChange('fat', e.target.value)}
                />
              </div>

              <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
                <button
                  type="button"
                  className="btn btn-primary"
                  onClick={handleConfirmScan}
                  style={{ flex: 1 }}
                >
                  ✅ Looks Good, Log It
                </button>

                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={handleReset}
                >
                  ← Try Another Photo
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
