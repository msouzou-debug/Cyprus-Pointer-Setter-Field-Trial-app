# Handoff: Cynegeticus app logo (option 4b, black-figure hunter and hound)

## Overview
Replace the placeholder emblem currently used by the Cynegeticus app with its own mark: a black silhouette of a hunter (petasos, chlamys, two spears) with a Laconian hound, drawn in the manner of Attic vase painting. The mark ships as raster PNGs in `assets/`. This document tells you where each file goes and how the lockups are built.

## About the design files
`Cynegeticus Logo.dc.html` is an HTML design reference showing the mark in context (icon sizes, header bars, owner card). It is not production code. Recreate the lockups below in the app's own framework and component patterns.

## Fidelity
High-fidelity for colours, spacing ratios and typography. The mark itself is a PNG crop of an illustration, so treat the icon sizes as final and the layout rules as exact.

## Assets (`assets/`)
Mark, transparent background, tight-cropped, 4% padding:
- `mark-black-{1024,512,192,96,64,48}.png` — ink #171A21, for light backgrounds
- `mark-cream-{512,192,96,64,48}.png` — #EFEAE0, for dark backgrounds (nav bars, splash)

App icon, square terracotta tile #C8763A with the black mark at 72% of the tile (14% safe margin each side), no rounded corners (the OS/launcher applies its own mask):
- `app-icon-{1024,512,192,180,167,152,120,96,72,48}.png`
  - 1024: App Store / Play Store listing
  - 180, 167, 152, 120: iOS `apple-touch-icon` sizes
  - 512, 192: PWA `manifest.json` icons (`"purpose": "any maskable"`)
  - 96, 72, 48: Android legacy densities

Favicon:
- `favicon-32.png`, `favicon-16.png` (same tile composition)

Source: the mark is variant 4b from the user-supplied sheet `uploads/logo-sheet.png`. If a vector is produced later, regenerate this set from it with the same margins.

## Where each asset goes

### Web / PWA
```html
<link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/icons/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/icons/app-icon-180.png">
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#1E2B4D">
```
`manifest.json`:
```json
{
  "name": "Cynegeticus",
  "short_name": "Cynegeticus",
  "icons": [
    { "src": "/icons/app-icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable" },
    { "src": "/icons/app-icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable" }
  ],
  "background_color": "#EFEAE0",
  "theme_color": "#1E2B4D"
}
```

### iOS
Drop `app-icon-1024.png` into the asset catalogue AppIcon (single-size). Xcode generates the rest.

### Android
`app-icon-512.png` as Play Store icon. For adaptive icons: background layer solid #C8763A, foreground layer `mark-black-512.png` centred on a 108 dp canvas with the mark occupying the 66 dp safe zone.

## Lockups

### Header bar (dark, primary)
- Bar background #1E2B4D, height 56 px, horizontal padding 16 px
- `mark-cream-96.png` rendered at 40×40 (contain), left aligned
- Gap 12 px
- Wordmark: text "CYNEGETICUS", Source Serif 4, 600, 20 px, letter-spacing 0.12em, colour #EFEAE0, vertically centred

### Header bar (light)
Same geometry. Background #EFEAE0, `mark-black-96.png`, wordmark colour #1E2B4D.

### Owner / about card (settings, install screen, footer)
- Card background #EFEAE0, padding 28 px, radius 6 px, content centred in a column, gap 16 px
- `mark-black-192.png` at 128×128
- Wordmark: Source Serif 4, 600, 22 px, letter-spacing 0.12em, #1E2B4D
- Owner row: 44 px circular avatar image of Κ.Ο.Α.Δ. (supplied separately by the owner), gap 12 px, then two lines:
  - "Κυπριακός Όμιλος Αγγλικών Δεικτών" — 13 px, 600, #171A21
  - "Κ.Ο.Α.Δ." — 11 px, 400, #5B5F6A

### Splash / loading
Background #171A21, `mark-cream-512.png` at 160×160 centred, wordmark beneath (Source Serif 4, 600, 22 px, 0.12em, #EFEAE0), gap 20 px.

## Rules
- Never place the black mark on #1E2B4D or #171A21; use the cream mark there.
- Never recolour the mark to anything other than #171A21 or #EFEAE0.
- Minimum rendered size of the mark alone: 40 px. Below that use the tiled app icon (the tile keeps it legible at 16–32 px).
- Keep the wordmark in capitals with 0.12em tracking; do not set it in the body font.
- No drop shadows, gradients or outlines on the mark.

## Design tokens
Colours
- Ink #171A21
- Cream #EFEAE0
- Terracotta tile #C8763A
- Deep blue (bars, theme colour) #1E2B4D
- Secondary text #5B5F6A

Typography
- Wordmark: Source Serif 4 (Google Fonts), 600
- 20 px in 56 px bars; 22 px in cards and splash; letter-spacing 0.12em throughout

Spacing
- Bar: 56 px high, 16 px side padding, 12 px icon-to-text gap
- Card: 28 px padding, 16 px gap, 6 px radius
- Icon tile safe margin: 14% per side

## Files
- `Cynegeticus Logo.dc.html` (project root) — design reference; option 4b is the card labelled "4b".
- `assets/` — all deliverable PNGs listed above.
