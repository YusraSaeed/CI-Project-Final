import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import ChatCustomizer from './ChatCustomizer'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ChatCustomizer />
  </StrictMode>,
)
