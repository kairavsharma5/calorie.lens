import { useState, useEffect, useRef } from 'react'

// ─────────────────────────────────────────
// CHATBOT COMPONENT
// A simple chat interface that talks to POST /chat/message
// Props:
//   user   - the logged-in user object (has .token)
//   onBack - function to return to the main menu
// ─────────────────────────────────────────
function Chatbot({ user, onBack }) {
  // the actual conversation — both shown on screen AND sent to the API.
  // starts empty; the friendly greeting below is UI-only, not a real message,
  // because Claude's API requires the first message to be role "user"
  const [messages, setMessages] = useState([])

  // what the user is currently typing
  const [input, setInput] = useState('')

  // true while waiting for Claude's reply
  const [sending, setSending] = useState(false)

  const [error, setError] = useState('')

  // used to auto-scroll to the newest message
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, sending])

  // ─────────────────────────────────────────
  // Send the current input as a new message
  // ─────────────────────────────────────────
  const handleSend = async (e) => {
    e.preventDefault()

    const trimmed = input.trim()
    if (!trimmed || sending) return

    // add the user's message to the conversation right away,
    // so it appears on screen instantly instead of waiting for the API
    const userMessage = { role: 'user', content: trimmed }
    const updatedMessages = [...messages, userMessage]

    setMessages(updatedMessages)
    setInput('')
    setSending(true)
    setError('')

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/chat/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${user.token}`
        },
        body: JSON.stringify({ messages: updatedMessages })
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Failed to get a response')
      }

      // add Claude's reply to the conversation
      setMessages([...updatedMessages, { role: 'assistant', content: data.reply }])
    } catch (err) {
      setError(err.message)
    } finally {
      setSending(false)
    }
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2>🤖 AI Nutritionist</h2>
        <button className="btn btn-secondary" onClick={onBack}>← Back</button>
      </div>

      <div className="chat-container">
        <div className="chat-messages">
          {/* UI-only greeting — never sent to the API */}
          {messages.length === 0 && (
            <div className="chat-bubble chat-bubble-assistant">
              Hey {user.username}! I'm your AI nutritionist. Ask me about your
              goals, what to eat next, or anything nutrition-related.
            </div>
          )}

          {messages.map((msg, index) => (
            <div
              key={index}
              className={`chat-bubble ${msg.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-assistant'}`}
            >
              {msg.content}
            </div>
          ))}

          {sending && (
            <div className="chat-bubble chat-bubble-assistant chat-typing">
              <span className="chat-typing-dot"></span>
              <span className="chat-typing-dot"></span>
              <span className="chat-typing-dot"></span>
            </div>
          )}

          {/* invisible anchor used to auto-scroll to the latest message */}
          <div ref={messagesEndRef} />
        </div>

        {error && <p className="error-message">{error}</p>}

        <form onSubmit={handleSend} className="chat-input-row">
          <input
            type="text"
            className="chat-input"
            placeholder="Ask about nutrition, meals, or goals..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={sending}
          />
          <button
            type="submit"
            className="btn btn-primary chat-send-btn"
            disabled={sending || !input.trim()}
          >
            Send
          </button>
        </form>
      </div>
    </div>
  )
}

export default Chatbot
