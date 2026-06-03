import React, { useState } from 'react';

export interface PropertyCardProps {
  title: string;
  location: string;
  type: string;
  features: string[];
  starting_price: string;
  image_url?: string;
  isDetailed?: boolean;
}

type Tab = 'overview' | 'sustainability' | 'consult';

const TABS: { id: Tab; label: string }[] = [
  { id: 'overview',       label: 'Overview'       },
  { id: 'sustainability', label: 'Sustainability'  },
  { id: 'consult',        label: 'Consult'         },
];

const ECO_POINTS = [
  'High-performance double-glazed insulation',
  'Subsurface greywater treatment & smart irrigation',
  'Integrated photovoltaic solar array systems',
  'Intelligent lighting & device management',
  'Low-VOC interior materials for occupant health',
];

export const PropertyCard: React.FC<PropertyCardProps> = ({
  title,
  location,
  type,
  features,
  starting_price,
  image_url,
  isDetailed = false,
}) => {
  const [tab, setTab]       = useState<Tab>('overview');
  const [name, setName]     = useState('');
  const [email, setEmail]   = useState('');
  const [tier, setTier]     = useState('₦100M – ₦250M');
  const [sent, setSent]     = useState(false);
  const [imgFail, setFail]  = useState(false);

  /* ── Compact inline card (inside chat bubble) ─── */
  if (!isDetailed) {
    return (
      <div className="card" style={{ borderRadius: '12px', overflow: 'hidden' }}>
        {/* Compact image strip */}
        <div
          style={{
            height: '100px',
            background: 'var(--bg-subtle)',
            position: 'relative',
            overflow: 'hidden',
          }}
        >
          {image_url && !imgFail ? (
            <img
              src={image_url}
              alt={title}
              onError={() => setFail(true)}
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
            />
          ) : (
            <div style={{
              width: '100%', height: '100%',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
            }}>
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1"
                style={{ color: 'var(--border)' }}>
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                <polyline points="9 22 9 12 15 12 15 22"/>
              </svg>
            </div>
          )}
          <div style={{
            position: 'absolute', inset: 0,
            background: 'linear-gradient(to top, var(--bg-panel) 0%, transparent 60%)',
          }} />
          <div style={{ position: 'absolute', bottom: '8px', left: '10px' }}>
            <span style={{
              fontSize: '8px', fontWeight: 700,
              textTransform: 'uppercase', letterSpacing: '0.15em',
              color: 'var(--gold)',
              background: 'var(--gold-alpha)',
              border: '1px solid var(--gold-border)',
              borderRadius: '4px', padding: '2px 7px',
            }}>
              {type}
            </span>
          </div>
        </div>

        <div style={{ padding: '12px' }}>
          <div style={{ fontSize: '13px', fontWeight: 700, color: 'var(--fg)', marginBottom: '4px' }}>
            {title}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px', marginBottom: '10px' }}>
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
              style={{ color: 'var(--gold)', flexShrink: 0 }}>
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
              <circle cx="12" cy="10" r="3"/>
            </svg>
            <span style={{ fontSize: '11px', color: 'var(--fg-muted)', fontWeight: 500 }}>{location}</span>
          </div>
          <div className="property-features-grid-compact">
            {features.slice(0, 4).map((f, i) => (
              <div key={i} style={{
                fontSize: '10px', color: 'var(--fg-muted)',
                background: 'var(--bg-subtle)',
                border: '1px solid var(--border)',
                borderRadius: '6px', padding: '4px 8px',
                display: 'flex', alignItems: 'center', gap: '5px',
              }}>
                <span style={{ width: '4px', height: '4px', borderRadius: '50%', background: 'var(--gold)', flexShrink: 0 }} />
                <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{f}</span>
              </div>
            ))}
          </div>
          <div style={{
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            paddingTop: '10px', borderTop: '1px solid var(--border)',
          }}>
            <span style={{ fontSize: '12px', fontWeight: 700, fontFamily: 'ui-monospace, monospace', color: 'var(--fg)' }}>
              {starting_price}
            </span>
            <span style={{
              fontSize: '9px', fontWeight: 700,
              textTransform: 'uppercase', letterSpacing: '0.1em',
              color: 'var(--gold)',
              background: 'var(--gold-alpha)',
              border: '1px solid var(--gold-border)',
              borderRadius: '6px', padding: '3px 8px',
            }}>
              View in Panel →
            </span>
          </div>
        </div>
      </div>
    );
  }

  /* ── Detailed panel card ─────────────────────── */
  return (
    <div className="card" style={{ borderRadius: '14px', overflow: 'hidden' }}>

      {/* Hero Image */}
      <div style={{ height: '200px', position: 'relative', overflow: 'hidden', background: 'var(--bg-subtle)' }}>
        {image_url && !imgFail ? (
          <img
            src={image_url}
            alt={title}
            onError={() => setFail(true)}
            style={{
              position: 'absolute', inset: 0,
              width: '100%', height: '100%', objectFit: 'cover',
              transition: 'transform 0.6s ease',
            }}
            onMouseEnter={(e) => { (e.target as HTMLElement).style.transform = 'scale(1.04)'; }}
            onMouseLeave={(e) => { (e.target as HTMLElement).style.transform = 'scale(1)'; }}
          />
        ) : (
          <div style={{
            position: 'absolute', inset: 0,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            background: 'linear-gradient(135deg, var(--bg-subtle) 0%, var(--bg-panel) 100%)',
          }}>
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1"
              style={{ color: 'var(--border)' }}>
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
              <polyline points="9 22 9 12 15 12 15 22"/>
            </svg>
          </div>
        )}
        {/* Gradient overlay */}
        <div style={{
          position: 'absolute', inset: 0,
          background: 'linear-gradient(to top, rgba(0,0,0,0.72) 0%, rgba(0,0,0,0.15) 50%, transparent 100%)',
        }} />
        {/* Title overlay */}
        <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, padding: '14px 16px' }}>
          <div style={{
            display: 'inline-block',
            fontSize: '9px', fontWeight: 700,
            textTransform: 'uppercase', letterSpacing: '0.15em',
            color: 'var(--gold)',
            background: 'rgba(0,0,0,0.45)',
            border: '1px solid var(--gold-border)',
            borderRadius: '5px', padding: '2px 8px',
            marginBottom: '6px',
            backdropFilter: 'blur(4px)',
          }}>
            {type}
          </div>
          <div style={{
            fontFamily: 'var(--font-playfair), serif',
            fontSize: '20px', fontWeight: 700,
            color: '#ffffff',
            lineHeight: 1.25,
            textShadow: '0 1px 6px rgba(0,0,0,0.5)',
          }}>
            {title}
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{
        display: 'flex',
        background: 'var(--bg-subtle)',
        borderBottom: '1px solid var(--border)',
      }}>
        {TABS.map((t) => (
          <button
            key={t.id}
            id={`tab-${t.id}`}
            onClick={() => setTab(t.id)}
            className={`tab-btn ${tab === t.id ? 'active' : ''}`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div style={{ padding: '16px', minHeight: '200px' }}>

        {/* Overview */}
        {tab === 'overview' && (
          <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>

            {/* Location */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '7px' }}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
                style={{ color: 'var(--gold)', flexShrink: 0 }}>
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
              <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--fg)' }}>{location}</span>
            </div>

            {/* Features grid */}
            <div>
              <p style={{
                fontSize: '9px', fontWeight: 700,
                textTransform: 'uppercase', letterSpacing: '0.16em',
                color: 'var(--gold)', marginBottom: '8px',
              }}>
                Key Features
              </p>
              <div className="property-features-grid">
                {features.map((f, i) => (
                  <div key={i} style={{
                    display: 'flex', alignItems: 'center', gap: '7px',
                    padding: '7px 10px',
                    background: 'var(--bg-subtle)',
                    border: '1px solid var(--border)',
                    borderRadius: '8px',
                    fontSize: '11px', color: 'var(--fg-muted)',
                  }}>
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3"
                      style={{ color: 'var(--gold)', flexShrink: 0 }}>
                      <polyline points="20 6 9 17 4 12"/>
                    </svg>
                    <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{f}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Price */}
            <div style={{
              display: 'flex', alignItems: 'center', justifyContent: 'space-between',
              paddingTop: '12px', borderTop: '1px solid var(--border)',
            }}>
              <div>
                <div style={{
                  fontSize: '9px', fontWeight: 700,
                  textTransform: 'uppercase', letterSpacing: '0.14em',
                  color: 'var(--fg-faint)', marginBottom: '2px',
                }}>
                  Starting Investment
                </div>
                <div style={{ fontSize: '16px', fontWeight: 700, fontFamily: 'ui-monospace, monospace', color: 'var(--fg)' }}>
                  {starting_price}
                </div>
              </div>
              <span style={{
                fontSize: '9px', fontWeight: 700,
                textTransform: 'uppercase', letterSpacing: '0.12em',
                padding: '4px 10px', borderRadius: '20px',
                color: 'var(--gold)',
                background: 'var(--gold-alpha)',
                border: '1px solid var(--gold-border)',
              }}>
                Available
              </span>
            </div>
          </div>
        )}

        {/* Sustainability */}
        {tab === 'sustainability' && (
          <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div style={{
              padding: '12px 14px',
              borderRadius: '10px',
              background: 'var(--gold-alpha)',
              border: '1px solid var(--gold-border)',
              display: 'flex', gap: '10px', alignItems: 'flex-start',
            }}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
                style={{ color: 'var(--gold)', flexShrink: 0, marginTop: '1px' }}>
                <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
              </svg>
              <div>
                <div style={{
                  fontSize: '10px', fontWeight: 700,
                  textTransform: 'uppercase', letterSpacing: '0.12em',
                  color: 'var(--gold)', marginBottom: '4px',
                }}>
                  Eco-Building Commitment
                </div>
                <p style={{ fontSize: '12px', lineHeight: 1.65, color: 'var(--fg-muted)', margin: 0 }}>
                  Bilaad targets a{' '}
                  <strong style={{ color: 'var(--fg)', fontWeight: 600 }}>40% reduction</strong> in grid dependence
                  through independent solar infrastructure, greywater recycling, and intelligent energy systems.
                </p>
              </div>
            </div>

            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {ECO_POINTS.map((item, i) => (
                <li key={i} style={{
                  display: 'flex', alignItems: 'center', gap: '9px',
                  fontSize: '12px', color: 'var(--fg-muted)',
                }}>
                  <span style={{
                    width: '5px', height: '5px', borderRadius: '50%',
                    background: 'var(--gold)', flexShrink: 0,
                  }} />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Consult */}
        {tab === 'consult' && (
          <div className="animate-fade-in">
            {sent ? (
              <div style={{
                padding: '20px', textAlign: 'center',
                borderRadius: '10px',
                background: 'var(--gold-alpha)',
                border: '1px solid var(--gold-border)',
              }}>
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
                  style={{ color: 'var(--gold)', margin: '0 auto 10px' }}>
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                  <polyline points="22 4 12 14.01 9 11.01"/>
                </svg>
                <div style={{
                  fontSize: '10px', fontWeight: 700,
                  textTransform: 'uppercase', letterSpacing: '0.14em',
                  color: 'var(--gold)', marginBottom: '8px',
                }}>
                  Consultation Requested
                </div>
                <p style={{ fontSize: '12px', lineHeight: 1.65, color: 'var(--fg-muted)', margin: 0 }}>
                  Thank you, <strong style={{ color: 'var(--fg)' }}>{name}</strong>.
                  Our team will reach out to <strong style={{ color: 'var(--fg)' }}>{email}</strong> within 24 hours
                  with the full prospectus for {title}.
                </p>
              </div>
            ) : (
              <form
                onSubmit={(e) => { e.preventDefault(); if (name && email) setSent(true); }}
                style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}
              >
                <div className="consult-form-grid">
                  <div>
                    <label style={{
                      display: 'block',
                      fontSize: '9px', fontWeight: 700,
                      textTransform: 'uppercase', letterSpacing: '0.14em',
                      color: 'var(--fg-faint)', marginBottom: '5px',
                    }}>
                      Full Name
                    </label>
                    <input
                      type="text" required value={name}
                      onChange={(e) => setName(e.target.value)}
                      placeholder="Your name"
                      className="field-input"
                    />
                  </div>
                  <div>
                    <label style={{
                      display: 'block',
                      fontSize: '9px', fontWeight: 700,
                      textTransform: 'uppercase', letterSpacing: '0.14em',
                      color: 'var(--fg-faint)', marginBottom: '5px',
                    }}>
                      Email
                    </label>
                    <input
                      type="email" required value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="your@email.com"
                      className="field-input"
                    />
                  </div>
                </div>

                <div>
                  <label style={{
                    display: 'block',
                    fontSize: '9px', fontWeight: 700,
                    textTransform: 'uppercase', letterSpacing: '0.14em',
                    color: 'var(--fg-faint)', marginBottom: '5px',
                  }}>
                    Investment Range
                  </label>
                  <select
                    value={tier}
                    onChange={(e) => setTier(e.target.value)}
                    className="field-input"
                    style={{ cursor: 'pointer' }}
                  >
                    <option>₦50M – ₦100M</option>
                    <option>₦100M – ₦250M</option>
                    <option>₦250M+</option>
                  </select>
                </div>

                <button
                  type="submit"
                  style={{
                    width: '100%', padding: '11px',
                    fontSize: '11px', fontWeight: 700,
                    textTransform: 'uppercase', letterSpacing: '0.14em',
                    fontFamily: 'inherit',
                    borderRadius: '9px',
                    background: 'var(--gold)',
                    color: '#0c0c10',
                    border: 'none',
                    cursor: 'pointer',
                    transition: 'background 0.2s',
                  }}
                  onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.background = 'var(--gold-hover)'; }}
                  onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.background = 'var(--gold)'; }}
                >
                  Request Private Briefing
                </button>
              </form>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
