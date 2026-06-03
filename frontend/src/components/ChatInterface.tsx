'use client';

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { PropertyCard } from './PropertyCard';

interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  ui_component?: string | null;
  ui_data?: any | null;
  timestamp: Date;
}

interface ChatInterfaceProps {
  onPropertySelect: (property: any) => void;
  isDark: boolean;
}

let _id = 0;
const uid = () => ++_id;

const SUGGESTIONS = [
  'Tell me about The Maldives by Bilaad',
  'What is The Bali Island project?',
  'Bilaad sustainability standards',
  'Properties available in Gwarinpa',
];

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ onPropertySelect, isDark }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: uid(),
      role: 'assistant',
      timestamp: new Date(),
      content:
        'Welcome to <strong>Bilaad Realty</strong>. I can provide detailed analysis on our premium Abuja portfolio — including <strong>The Maldives</strong> in Gwarinpa and <strong>The Bali Island</strong> in Life Camp. How may I assist you?',
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const feedRef = useRef<HTMLDivElement>(null);

  const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const send = useCallback(
    async (text: string) => {
      const trimmed = text.trim();
      if (!trimmed || isLoading) return;

      setMessages((p) => [
        ...p,
        { id: uid(), role: 'user', content: trimmed, timestamp: new Date() },
      ]);
      setInput('');
      setIsLoading(true);

      try {
        const history = messages.map((m) => ({ role: m.role, content: m.content }));
        const res = await fetch(`${API}/chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: trimmed, history }),
        });
        if (!res.ok) throw new Error('Network error');
        const data = await res.json();

        setMessages((p) => [
          ...p,
          {
            id: uid(),
            role: 'assistant',
            content: data.response_text,
            ui_component: data.ui_component,
            ui_data: data.ui_data,
            timestamp: new Date(),
          },
        ]);
        if (data.ui_component === 'PropertyCard' && data.ui_data) {
          onPropertySelect(data.ui_data);
        }
      } catch {
        setMessages((p) => [
          ...p,
          {
            id: uid(),
            role: 'assistant',
            content:
              'Unable to reach the server. Please ensure the backend is running on <code>localhost:8000</code>.',
            timestamp: new Date(),
          },
        ]);
      } finally {
        setIsLoading(false);
        setTimeout(() => inputRef.current?.focus(), 50);
      }
    },
    [messages, isLoading, onPropertySelect]
  );



  const fmt = (d: Date) =>
    d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  const showSuggestions = messages.length === 1 && !isLoading;

  return (
    <div id="chat-pane">
      {/* ── Toolbar ─────────────────────────────────── */}
      <div
        style={{
          flexShrink: 0,
          display: 'flex',
          alignItems: 'center',
          padding: '0 16px',
          height: '44px',
          borderBottom: '1px solid var(--border)',
          background: 'var(--bg-panel)',
        }}
      >
        <span
          style={{
            fontSize: '13px',
            fontWeight: 600,
            color: 'var(--fg)',
            letterSpacing: '0.01em',
          }}
        >
          Bilaad AI
        </span>
      </div>

      {/* ── Centered Chat Column ─────────────────────── */}
      <div id="chat-column">

        {/* Suggestion chips — shown above messages when fresh */}
        {showSuggestions && (
          <div id="suggestions-wrap">
            <p
              style={{
                fontSize: '11px',
                fontWeight: 600,
                textTransform: 'uppercase',
                letterSpacing: '0.14em',
                color: 'var(--fg-faint)',
                marginBottom: '10px',
              }}
            >
              Try asking
            </p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {SUGGESTIONS.map((s, i) => (
                <button
                  key={i}
                  id={`suggestion-${i}`}
                  onClick={() => send(s)}
                  className="suggestion-chip"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Message Feed */}
        <div id="message-feed" ref={feedRef}>
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`msg-row ${msg.role === 'user' ? 'user' : 'ai'} animate-fade-up`}
            >
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: msg.role === 'user' ? 'flex-end' : 'flex-start' }}>
                <div
                  className={`msg-bubble ${msg.role === 'user' ? 'user' : 'ai'}`}
                  dangerouslySetInnerHTML={
                    msg.ui_component === 'PropertyCard' && msg.ui_data
                      ? undefined
                      : { __html: msg.content }
                  }
                >
                  {msg.ui_component === 'PropertyCard' && msg.ui_data ? (
                    <>
                      <div dangerouslySetInnerHTML={{ __html: msg.content }} />
                      <div className="inline-card" style={{ marginTop: '12px' }}>
                        <PropertyCard
                          title={msg.ui_data.title}
                          location={msg.ui_data.location}
                          type={msg.ui_data.type}
                          features={msg.ui_data.features}
                          starting_price={msg.ui_data.starting_price}
                          image_url={msg.ui_data.image_url}
                        />
                      </div>
                    </>
                  ) : null}
                </div>
                <span className="msg-time">{fmt(msg.timestamp)}</span>
              </div>
            </div>
          ))}

          {/* Typing indicator */}
          {isLoading && (
            <div className="msg-row ai animate-fade-in">
              <div
                className="msg-bubble ai"
                style={{ padding: '14px 18px', display: 'flex', gap: '5px', alignItems: 'center' }}
              >
                <span className="typing-dot" />
                <span className="typing-dot" />
                <span className="typing-dot" />
              </div>
            </div>
          )}

          <div ref={bottomRef} style={{ height: '1px' }} />
        </div>

        {/* Input */}
        <div id="chat-input-area">
          <form
            onSubmit={(e) => { e.preventDefault(); send(input); }}
            id="chat-input-wrap"
          >
            <input
              id="chat-input"
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Message Bilaad AI…"
              autoComplete="off"
            />
            <button
              id="send-btn"
              type="submit"
              disabled={!input.trim() || isLoading}
              aria-label="Send message"
            >
              <svg
                width="16" height="16" viewBox="0 0 24 24"
                fill="none" stroke={!input.trim() || isLoading ? 'var(--fg-faint)' : (isDark ? '#212121' : '#ffffff')}
                strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"
              >
                <line x1="22" y1="2" x2="11" y2="13" />
                <polygon points="22 2 15 22 11 13 2 9 22 2" />
              </svg>
            </button>
          </form>

          {/* Footer note */}
          <p id="chat-footer-note">
            Bilaad AI can make mistakes. Always verify investment decisions independently.
          </p>
        </div>

      </div>
    </div>
  );
};
