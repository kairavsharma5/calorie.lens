# 🍽️ CalorieLens Frontend - Setup Guide

Welcome! This is your **CalorieLens Frontend** - built with React, Vite, HTML, and CSS.

---

## 📋 What You Have

✅ **React Components:**
- `LoginForm.jsx` - Signup/Login page
- `UploadForm.jsx` - Food image upload
- `ResultsDisplay.jsx` - Show analysis results

✅ **Styling:**
- Dark gray/black theme with orange/red accents
- Fully responsive design (works on mobile, tablet, desktop)
- Smooth animations and hover effects

✅ **Ready-to-Use Features:**
- User authentication (login/signup)
- Image upload with drag-and-drop
- Direct connection to Flask backend
- Loading states and error handling

---

## 🚀 Getting Started

### Step 1: Install Vite (Development Server)

In your terminal (in the `CalorieLens-Frontend` folder), type:

```bash
npm install --save-dev @vitejs/plugin-react vite
```

This downloads Vite, which helps you run the frontend locally.

---

### Step 2: Start the Frontend Development Server

In your terminal, type:

```bash
npm run dev
```

You should see output like:
```
  VITE v4.4.0  ready in 123 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

**Copy the `http://localhost:5173/` link** and open it in your browser. You should see the CalorieLens login page!

---

### Step 3: Start Your Flask Backend (In Another Terminal)

Open a **NEW terminal** (keep the first one running) and navigate to your `CalorieLens-Backend` folder:

```bash
cd C:\Users\Virat\Desktop\GitHub\c-learning-\proj\CalorieLens-Backend
```

Then start Flask:

```bash
python app.py
```

Your backend should be running on `http://localhost:5000`

---

### Step 4: Test Everything Together

Now you have:
- ✅ Frontend running on `http://localhost:5173`
- ✅ Backend running on `http://localhost:5000`

Try this workflow:
1. Go to the frontend (localhost:5173)
2. Create an account or login
3. Upload a food image
4. The frontend sends it to the backend
5. Backend analyzes it
6. Results display on the frontend

---

## 📁 Project Structure

```
CalorieLens-Frontend/
├── index.html              # Main HTML file
├── package.json            # Project dependencies
├── vite.config.js          # Vite configuration
├── .env                    # Backend API URL (localhost:5000)
└── src/
    ├── main.jsx            # React entry point
    ├── App.jsx             # Main app component
    ├── App.css             # All styling (dark theme)
    └── components/
        ├── LoginForm.jsx   # Login/Signup
        ├── UploadForm.jsx  # Upload food image
        └── ResultsDisplay.jsx # Show results
```

---

## 🔌 Backend Connection

The frontend connects to your Flask backend at **`http://localhost:5000`**

**API Endpoints it uses:**
- `POST /api/auth/login` - Login user
- `POST /api/auth/signup` - Create account
- `POST /api/analyze-food` - Analyze food image

Make sure your Flask backend has these endpoints set up!

---

## 🎨 Design Details

### Color Scheme:
- **Background:** Dark gray/black (#0f0f0f, #1a1a1a, #2a2a2a)
- **Accent Color:** Orange/Red (#ff6b35)
- **Text:** White and light gray (#ffffff, #b0b0b0)
- **Borders:** Dark borders (#3a3a3a)

### Key Features:
- Fully responsive (works on mobile, tablet, desktop)
- Smooth animations and transitions
- Hover effects on buttons and cards
- Loading spinners for async operations
- Error and success messages
- Drag-and-drop image upload

---

## 📝 How the Frontend Works

### 1. **Login Screen**
- User enters email and password
- Can toggle between login and signup
- Validation for email format, password length, matching passwords
- Makes POST request to Flask backend

### 2. **Upload Screen** (After Login)
- User sees drag-and-drop upload area
- Can click or drag image to upload
- Shows preview of selected image
- Sends image to Flask backend's `/api/analyze-food` endpoint

### 3. **Results Screen** (After Analysis)
- Displays:
  - Food image
  - Food name
  - Calories, Protein, Carbs, Fat (in cards)
  - Detected ingredients list
  - Nutrition tips
  - Health summary
- Can analyze another meal or save to history

---

## 🔧 Important Files to Know

### `src/App.jsx`
- Main component that manages the workflow
- Handles switching between login → upload → results screens
- Manages user state

### `src/App.css`
- ALL styling is here (dark theme with orange accents)
- CSS variables for easy color changes
- Responsive design for mobile/tablet/desktop

### `src/components/LoginForm.jsx`
- Handles user signup and login
- Validates email and password
- Makes requests to backend auth endpoints

### `src/components/UploadForm.jsx`
- Handles food image upload
- Drag-and-drop functionality
- File validation
- Sends image to backend

### `src/components/ResultsDisplay.jsx`
- Shows analysis results from backend
- Displays nutrition cards
- Shows ingredients and tips

---

## 🚨 Troubleshooting

### Frontend won't load (blank page)
- Make sure `npm run dev` is running
- Check that http://localhost:5173 is open in your browser
- Check the browser console (F12) for errors

### Can't login/upload (errors from backend)
- Make sure Flask backend is running on http://localhost:5000
- Check that Flask server says "Running on http://localhost:5000"
- Make sure your Flask endpoints are set up

### Image upload not working
- Check browser console (F12) for errors
- Make sure the Flask backend has the `/api/analyze-food` endpoint
- Check that CORS is enabled in Flask (Flask-CORS)

### Styling looks different
- Clear your browser cache (Ctrl+Shift+Delete)
- Hard refresh the page (Ctrl+Shift+R)
- Make sure App.css is being loaded

---

## 📱 Responsive Design

The frontend is fully responsive:
- **Desktop:** Full width with all features
- **Tablet:** Adjusted layout, grid changes
- **Mobile:** Single column, touch-friendly buttons

---

## 🔐 Security Notes

⚠️ **For Development Only:**
- This frontend connects to Flask without extra security
- For production, add:
  - HTTPS
  - CORS configuration in Flask
  - JWT tokens for authentication
  - Environment variables for API URL

---

## 📚 Learning Points

As you work through this, understand:
1. **React Components** - Reusable UI pieces
2. **State Management** - useState hook manages data
3. **Event Handling** - onClick, onChange, onSubmit
4. **Form Validation** - Email format, password length checks
5. **API Calls** - Axios sends data to backend
6. **CSS Styling** - Dark theme with variables
7. **File Upload** - FormData for sending files

---

## 🎯 Next Steps

1. ✅ Install Vite (`npm install --save-dev @vitejs/plugin-react vite`)
2. ✅ Run frontend (`npm run dev`)
3. ✅ Run backend (Flask) in another terminal
4. ✅ Test login/upload/results workflow
5. 📝 Study the code line by line to understand how it works

---

## 📞 Quick Reference

**Start Frontend:**
```bash
npm run dev
```

**Start Backend (in another terminal):**
```bash
python app.py
```

**Frontend URL:** http://localhost:5173
**Backend URL:** http://localhost:5000

---

Good luck! You're building something amazing. 🚀
