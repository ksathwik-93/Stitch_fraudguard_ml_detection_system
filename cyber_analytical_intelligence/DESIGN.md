---
name: Cyber-Analytical Intelligence
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#c2c6d6'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#8c909f'
  outline-variant: '#424754'
  surface-tint: '#adc6ff'
  primary: '#adc6ff'
  on-primary: '#002e6a'
  primary-container: '#4d8eff'
  on-primary-container: '#00285d'
  inverse-primary: '#005ac2'
  secondary: '#4edea3'
  on-secondary: '#003824'
  secondary-container: '#00a572'
  on-secondary-container: '#00311f'
  tertiary: '#ffb3ad'
  on-tertiary: '#68000a'
  tertiary-container: '#ff5451'
  on-tertiary-container: '#5c0008'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a42'
  on-primary-fixed-variant: '#004395'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffdad7'
  tertiary-fixed-dim: '#ffb3ad'
  on-tertiary-fixed: '#410004'
  on-tertiary-fixed-variant: '#930013'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display:
    fontFamily: Geist
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Geist
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Geist
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
  mono-data:
    fontFamily: Geist Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  container-padding: 24px
  gutter: 16px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style

The design system is engineered for high-stakes financial monitoring and cybersecurity analysis. It targets security analysts and fraud investigators who require a high-density, low-fatigue interface to process complex transactional data.

The style is **Modern Corporate** with a focus on **Analytical Precision**. It leverages a structured grid, clear information hierarchy, and a strict utility-first color application. Aesthetics are derived from data clarity rather than decoration. The interface utilizes a "Card-on-Canvas" architecture to compartmentalize distinct data streams, ensuring the user feels in control of a secure, robust environment.

Key principles:
- **Efficiency over Embellishment:** Every pixel must serve a functional purpose.
- **Trust through Clarity:** Use distinct color coding for risk levels to prevent cognitive lag.
- **State-Driven UI:** Visual prominence is determined by the severity of the fraud alert.

## Colors

The palette is optimized for long-duration monitoring. The primary background uses **Slate 950 (#0F172A)** to reduce eye strain, while interactive surfaces use **Slate 800 (#1E293B)**. 

### Semantic Mapping
- **Primary (Cyber Blue):** Used for primary actions, active navigation states, and systemic information.
- **Success (Emerald):** Denotes legitimate transactions and "Safe" status.
- **Warning (Amber):** Identifies medium-risk anomalies requiring investigation.
- **Danger (Crimson):** Flags high-risk, immediate threats, and fraudulent activity.

In **Light Mode**, the canvas shifts to a soft gray (#F8FAFC) with borders using #E2E8F0. Text contrast must remain above 4.5:1 for all status indicators to ensure accessibility.

## Typography

This design system utilizes **Geist** for its technical, precision-engineered feel. The typeface offers excellent legibility at small sizes, which is critical for dense data tables.

- **Monospace for Data:** Use the Geist Mono variant (or Geist with tabular figures enabled) for transaction IDs, IP addresses, and timestamps to ensure vertical alignment in tables.
- **Letter Spacing:** Headlines utilize slight negative tracking for a more "locked-in" professional look, while labels use positive tracking to improve readability at small scales.
- **Scale:** On mobile, `display` and `headline-lg` should downscale by 20% to avoid excessive line-wrapping in card headers.

## Layout & Spacing

The layout follows a **Fixed-Fluid Hybrid** model. Navigation is fixed to a left-side rail (240px width), while the main content area is a fluid grid that adapts to the viewport.

- **Grid:** A 12-column grid is used for dashboard layouts.
- **Rhythm:** An 8px linear scale (4, 8, 16, 24, 32, 48, 64) governs all padding and margins.
- **Density:** The system favors "Compact" density for data-heavy views (12px cell padding) and "Default" density for settings or onboarding (16px+ padding).
- **Mobile Adaptation:** On mobile devices, the 12-column grid collapses into a single-column stack with 16px side margins.

## Elevation & Depth

Depth is primarily communicated through **Tonal Layering** and **Subtle Outlines** rather than heavy shadows, maintaining a flat, professional "dashboard" aesthetic.

- **Level 0 (Canvas):** The base background layer.
- **Level 1 (Cards/Surfaces):** Raised via a 1px solid border (`#334155` in dark mode). A very subtle 4px blur shadow with 20% opacity is applied only to distinguish cards from the canvas.
- **Level 2 (Modals/Popovers):** Higher elevation using a more pronounced shadow (12px blur, 40% opacity) and a backdrop blur of 8px to maintain focus.
- **Interactions:** Buttons do not use shadows; instead, they use background color shifts (e.g., hover state is 10% lighter) to indicate interactivity.

## Shapes

The design system uses a **Soft (0.25rem)** roundedness approach. This maintains a disciplined, technical look while feeling modern and accessible.

- **Standard Elements:** Buttons, inputs, and small cards use the `rounded-sm` (4px) setting.
- **Container Elements:** Large dashboard widgets and modals use `rounded-lg` (8px).
- **Status Badges:** These are the only exception and may use a fully pill-shaped (999px) radius to distinguish them from interactive buttons.

## Components

### Buttons
- **Primary:** Solid Cyber Blue background with white text. No gradient.
- **Secondary:** Transparent background with a 1px Slate border.
- **Risk-Action:** Solid Crimson background for "Block Transaction" or "Flag Fraud."

### Data Tables
- **Header:** Slate 900 background, uppercase Label-MD typography, sticky position.
- **Rows:** 1px bottom border only. Hover state changes the row background to a slightly lighter Slate.
- **Columns:** Alignment is crucial. Numbers and dates are right-aligned; text and status badges are left-aligned.

### Status Badges (Risk Indicators)
- **High Risk:** Crimson text on a 10% opacity Crimson background.
- **Medium Risk:** Amber text on a 10% opacity Amber background.
- **Low Risk:** Emerald text on a 10% opacity Emerald background.
- Include a 6px solid dot next to the text for color-blind accessibility.

### Input Fields
- Dark backgrounds with 1px borders. Focus state uses a 2px Cyber Blue ring. Use "Geist Mono" for inputs involving account numbers or API keys.

### Cards
- White/Slate-800 background, 1px border, 16px internal padding. Headers should be separated by a subtle horizontal rule.