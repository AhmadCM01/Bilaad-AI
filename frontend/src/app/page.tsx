'use client';

import React, { useState, useEffect } from 'react';
import { ChatInterface } from '../components/ChatInterface';
import { PropertyCard } from '../components/PropertyCard';

export default function Home() {
  const [activeProperty, setActiveProperty] = useState<any>(null);
  const [isDark, setIsDark] = useState(true);

  useEffect(() => {
    const root = document.documentElement;
    if (isDark) {
      root.classList.add('dark');
      root.classList.remove('light');
    } else {
      root.classList.remove('dark');
      root.classList.add('light');
    }
  }, [isDark]);

  return (
    <div id="app-shell">

      {/* ── Header ──────────────────────────────────────── */}
      <header id="app-header">

        {/* Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <img
            src="https://bilaadnigeria.com/wp-content/uploads/2023/08/bilaad-logo.png"
            alt="Bilaad Realty"
            style={{
              height: '36px',
              width: 'auto',
              objectFit: 'contain',
              filter: isDark ? 'brightness(1.08)' : 'brightness(0.9)',
            }}
            onError={(e) => {
              const el = e.target as HTMLImageElement;
              el.style.display = 'none';
              const fallback = document.getElementById('logo-fallback');
              if (fallback) fallback.style.display = 'flex';
            }}
          />
          {/* Text fallback if logo fails */}
          <div
            id="logo-fallback"
            style={{
              display: 'none',
              alignItems: 'center',
              gap: '6px',
            }}
          >
            <span
              style={{
                fontFamily: 'var(--font-playfair), serif',
                fontSize: '18px',
                fontWeight: 700,
                letterSpacing: '0.04em',
                color: 'var(--fg)',
              }}
            >
              BILAAD
            </span>
            <span
              style={{
                fontSize: '10px',
                fontWeight: 600,
                letterSpacing: '0.18em',
                color: 'var(--fg-faint)',
                textTransform: 'uppercase',
              }}
            >
              Realty
            </span>
          </div>
        </div>

        {/* Right: Theme Toggle */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {/* Label */}
          <span
            style={{
              fontSize: '10px',
              fontWeight: 600,
              letterSpacing: '0.16em',
              textTransform: 'uppercase',
              color: 'var(--fg-faint)',
            }}
            className="hidden-mobile"
          >
            {isDark ? 'Dark' : 'Light'}
          </span>

          {/* Toggle switch */}
          <button
            id="theme-toggle"
            onClick={() => setIsDark(!isDark)}
            className={`toggle-track ${isDark ? 'is-dark' : ''}`}
            aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
            title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            <span className="toggle-thumb" />
          </button>

          {/* Icon */}
          {isDark ? (
            <svg
              width="16" height="16" viewBox="0 0 24 24"
              fill="none" stroke="currentColor" strokeWidth="2"
              strokeLinecap="round" strokeLinejoin="round"
              style={{ color: 'var(--fg-faint)', flexShrink: 0 }}
            >
              <circle cx="12" cy="12" r="5"/>
              <line x1="12" y1="1" x2="12" y2="3"/>
              <line x1="12" y1="21" x2="12" y2="23"/>
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
              <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
              <line x1="1" y1="12" x2="3" y2="12"/>
              <line x1="21" y1="12" x2="23" y2="12"/>
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
              <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
            </svg>
          ) : (
            <svg
              width="16" height="16" viewBox="0 0 24 24"
              fill="none" stroke="currentColor" strokeWidth="2"
              strokeLinecap="round" strokeLinejoin="round"
              style={{ color: 'var(--fg-faint)', flexShrink: 0 }}
            >
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
            </svg>
          )}


        </div>
      </header>

      {/* ── Main Workspace ──────────────────────────────── */}
      <main id="app-main">

        {/* Left: Chat */}
        <section id="chat-pane">
          <ChatInterface onPropertySelect={setActiveProperty} isDark={isDark} />
        </section>

        {/* Right: Property Panel */}
        <aside
          id="property-pane"
          className={activeProperty ? '' : 'collapsed'}
        >
          {activeProperty && (
            <>
              {/* Panel header */}
              <div
                style={{
                  flexShrink: 0,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '0 20px',
                  height: '52px',
                  background: 'var(--bg-panel)',
                  borderBottom: '1px solid var(--border)',
                }}
              >
                <div>
                  <div
                    style={{
                      fontSize: '9px',
                      fontWeight: 700,
                      textTransform: 'uppercase',
                      letterSpacing: '0.2em',
                      color: 'var(--gold)',
                      marginBottom: '1px',
                    }}
                  >
                    Property Details
                  </div>
                  <div
                    style={{
                      fontSize: '12px',
                      fontWeight: 600,
                      color: 'var(--fg)',
                    }}
                  >
                    {activeProperty.title}
                  </div>
                </div>
                <button
                  id="close-property-btn"
                  onClick={() => setActiveProperty(null)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '5px',
                    fontSize: '10px',
                    fontWeight: 700,
                    letterSpacing: '0.12em',
                    textTransform: 'uppercase',
                    color: 'var(--fg-faint)',
                    background: 'none',
                    border: '1px solid var(--border)',
                    borderRadius: '8px',
                    padding: '6px 10px',
                    cursor: 'pointer',
                    transition: 'color 0.2s, border-color 0.2s',
                  }}
                  onMouseEnter={(e) => {
                    (e.currentTarget as HTMLElement).style.color = 'var(--gold)';
                    (e.currentTarget as HTMLElement).style.borderColor = 'var(--gold-border)';
                  }}
                  onMouseLeave={(e) => {
                    (e.currentTarget as HTMLElement).style.color = 'var(--fg-faint)';
                    (e.currentTarget as HTMLElement).style.borderColor = 'var(--border)';
                  }}
                >
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                  Close
                </button>
              </div>

              {/* Scrollable content */}
              <div
                style={{
                  flex: 1,
                  overflowY: 'auto',
                  padding: '16px',
                }}
              >
                <PropertyCard
                  title={activeProperty.title}
                  location={activeProperty.location}
                  type={activeProperty.type}
                  features={activeProperty.features}
                  starting_price={activeProperty.starting_price}
                  image_url={activeProperty.image_url}
                  isDetailed={true}
                />
              </div>
            </>
          )}
        </aside>
      </main>

      {/* ── Footer ──────────────────────────────────────── */}
      <footer id="app-footer">
        <span
          style={{
            fontSize: '11px',
            fontWeight: 400,
            color: 'var(--fg-faint)',
            letterSpacing: '0.03em',
          }}
        >
          © {new Date().getFullYear()} Bilaad Realty. All rights reserved.
        </span>
      </footer>

      {/* ── Mobile hidden class ──────────────────────────── */}
      <style>{`
        @media (max-width: 767px) {
          .hidden-mobile { display: none !important; }
        }
      `}</style>

    </div>
  );
}
