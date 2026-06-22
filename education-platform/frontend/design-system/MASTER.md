# EduPlatform — Design System MASTER

> Generated via `ui-ux-pro-max-skill` · Style: **Minimalism & Swiss Style** with **Data-Dense Dashboard** layout behavior · Product type: **B2B Internal Tool / School Management SaaS**
>
> Do not edit color/type/spacing values here manually. If the design direction changes, re-run the generator and replace this file.

---

## Table of contents

1. [Design direction summary](#1-design-direction-summary)
2. [Color tokens](#2-color-tokens)
3. [Typography](#3-typography)
4. [Spacing & layout grid](#4-spacing--layout-grid)
5. [Border radius & shadows](#5-border-radius--shadows)
6. [Component patterns](#6-component-patterns)
7. [Interaction & animation rules](#7-interaction--animation-rules)
8. [Page layout blueprints](#8-page-layout-blueprints)
9. [Dark mode](#9-dark-mode)
10. [Accessibility checklist](#10-accessibility-checklist)
11. [CSS custom properties (copy-paste)](#11-css-custom-properties-copy-paste)
12. [Anti-patterns (avoid)](#12-anti-patterns-avoid)

---

## 1. Design direction summary

| Dimension    | Choice                           | Reasoning                                                            |
| ------------ | -------------------------------- | -------------------------------------------------------------------- |
| Style        | Minimalism & Swiss Style         | Admin/teacher users value clarity, speed, and information density     |
| Layout       | Data-dense 12-column grid        | Rosters, tables, KPI cards need maximum visible data                 |
| Color mood   | Professional navy + CTA blue     | Trust, authority, readable at all screen sizes                       |
| Typography   | Poppins (headings) / Open Sans   | Poppins gives structure; Open Sans is highly legible in tables/forms |
| Iconography  | Lucide React (SVG)               | Consistent 24px grid, tree-shakeable, never emoji-as-icon            |
| Interactions | Subtle (150–250ms ease-out)      | Users are on this screen all day — no flashy animations              |
| Complexity   | Low (no glassmorphism, no blurs) | Fast rendering, WCAG AA minimum, works on older school hardware      |

**One-sentence pitch:** A clean, trust-worthy admin shell — dark navy sidebar, white content canvas, data tables as the hero element.

---

## 2. Color tokens

### Semantic palette (B2B Professional Navy)

| Token name              | Hex       | Usage                                            |
| ----------------------- | --------- | ------------------------------------------------ |
| `--color-primary`       | `#0F172A` | Sidebar background, headings, primary text       |
| `--color-on-primary`    | `#FFFFFF` | Text on primary backgrounds                      |
| `--color-secondary`     | `#334155` | Secondary nav items, sub-headings                |
| `--color-accent`        | `#0369A1` | CTA buttons, links, active states, focus rings   |
| `--color-accent-hover`  | `#0284C7` | Accent on hover (lighter step)                   |
| `--color-background`    | `#F8FAFC` | App background / content canvas                  |
| `--color-foreground`    | `#020617` | Primary text on light background                 |
| `--color-card`          | `#FFFFFF` | Card / panel surface                             |
| `--color-card-fg`       | `#020617` | Text on card surface                             |
| `--color-muted`         | `#E8ECF1` | Disabled states, table striping, dividers        |
| `--color-muted-fg`      | `#64748B` | Placeholder text, metadata, timestamps           |
| `--color-border`        | `#E2E8F0` | Card borders, table rules, input borders         |
| `--color-destructive`   | `#DC2626` | Delete buttons, error states, danger badges      |
| `--color-destructive-fg`| `#FFFFFF` | Text on destructive backgrounds                  |
| `--color-success`       | `#059669` | Enrolled badge, active status, positive metrics  |
| `--color-success-fg`    | `#FFFFFF` | Text on success backgrounds                      |
| `--color-warning`       | `#D97706` | Warning states, pending enrollment               |
| `--color-warning-fg`    | `#FFFFFF` | Text on warning backgrounds                      |
| `--color-ring`          | `#0369A1` | Focus ring (3px solid, 2px offset)               |

### Sidebar-specific tokens

| Token                    | Hex       |
| ------------------------ | --------- |
| `--sidebar-bg`           | `#0F172A` |
| `--sidebar-item-fg`      | `#CBD5E1` |
| `--sidebar-item-hover`   | `#1E293B` |
| `--sidebar-item-active`  | `#0369A1` |
| `--sidebar-item-active-fg`| `#FFFFFF`|
| `--sidebar-border`       | `#1E293B` |

### Status badge palette

| Status      | Background  | Text      |
| ----------- | ----------- | --------- |
| Active      | `#D1FAE5`   | `#065F46` |
| Inactive    | `#F1F5F9`   | `#475569` |
| Enrolled    | `#DBEAFE`   | `#1E40AF` |
| Pending     | `#FEF3C7`   | `#92400E` |
| Removed     | `#FEE2E2`   | `#991B1B` |

---

## 3. Typography

### Font pairing: Modern Professional

| Role     | Font       | Weights  | Source                                     |
| -------- | ---------- | -------- | ------------------------------------------ |
| Headings | Poppins    | 500, 600, 700 | Google Fonts                          |
| Body     | Open Sans  | 300, 400, 500, 600 | Google Fonts                     |

**Google Fonts import** (in `styles/globals.css`):
```css
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700&family=Poppins:wght@500;600;700&display=swap');
```

### Type scale

| Token             | Font      | Size      | Weight | Line height | Usage                          |
| ----------------- | --------- | --------- | ------ | ----------- | ------------------------------ |
| `--text-2xl`      | Poppins   | 1.5rem    | 700    | 1.2         | Page titles                    |
| `--text-xl`       | Poppins   | 1.25rem   | 600    | 1.3         | Section headings               |
| `--text-lg`       | Poppins   | 1.125rem  | 600    | 1.4         | Card titles, modal headers     |
| `--text-base`     | Open Sans | 1rem      | 400    | 1.6         | Body copy, table cell content  |
| `--text-sm`       | Open Sans | 0.875rem  | 400    | 1.5         | Labels, metadata, help text    |
| `--text-xs`       | Open Sans | 0.75rem   | 500    | 1.4         | Badges, timestamps, captions   |

### Font stack fallbacks
```css
--font-heading: 'Poppins', 'Segoe UI', system-ui, sans-serif;
--font-body:    'Open Sans', 'Segoe UI', system-ui, sans-serif;
```

---

## 4. Spacing & layout grid

### Base unit: 4px

All spacing is a multiple of 4px. Use the token scale below — never hardcode pixel values.

| Token        | Value | Rem    | Usage example                             |
| ------------ | ----- | ------ | ----------------------------------------- |
| `--space-1`  | 4px   | 0.25rem| Icon padding, tight gaps                  |
| `--space-2`  | 8px   | 0.5rem | Inline element gaps                       |
| `--space-3`  | 12px  | 0.75rem| Table cell padding (compact)              |
| `--space-4`  | 16px  | 1rem   | Card padding, form field spacing          |
| `--space-5`  | 20px  | 1.25rem| Section gaps within a card                |
| `--space-6`  | 24px  | 1.5rem | Card-to-card gap, modal padding           |
| `--space-8`  | 32px  | 2rem   | Page section spacing                      |
| `--space-10` | 40px  | 2.5rem | Large section gaps                        |
| `--space-12` | 48px  | 3rem   | Page-level vertical rhythm                |

### 12-column grid

```css
--grid-columns:     12;
--grid-gap:         var(--space-6);    /* 24px gutter */
--content-max-width: 1440px;
--sidebar-width:    240px;
--header-height:    64px;
```

#### Column spans used

| Element                     | Span (of 12) |
| --------------------------- | ------------ |
| KPI stat card               | 3 (4-up row) |
| Main content area (sidebar open) | 9–10    |
| Sidebar                     | 2–3          |
| Full-width table             | 12           |
| Modal (centered)            | 5–6          |
| Form (in a card)            | 6–8          |

---

## 5. Border radius & shadows

### Border radius

| Token          | Value  | Usage                              |
| -------------- | ------ | ---------------------------------- |
| `--radius-sm`  | 4px    | Badges, tags, small buttons        |
| `--radius-md`  | 8px    | Cards, inputs, most components     |
| `--radius-lg`  | 12px   | Modals, drawer panels              |
| `--radius-full`| 9999px | Avatar circles, toggle pills       |

### Shadows

| Token             | Value                              | Usage                        |
| ----------------- | ---------------------------------- | ---------------------------- |
| `--shadow-xs`     | `0 1px 2px rgba(0,0,0,0.05)`      | Table row hover              |
| `--shadow-sm`     | `0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06)` | Cards |
| `--shadow-md`     | `0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06)` | Dropdowns, tooltips |
| `--shadow-lg`     | `0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05)` | Modals |

**Rule:** Never use `box-shadow` values not in this table — one of the most common causes of inconsistent depth perception across pages.

---

## 6. Component patterns

### Button

```
Primary:    bg accent (#0369A1), text white, hover (#0284C7), radius-md, h-10
Secondary:  bg white, border border, text foreground, hover bg-muted
Danger:     bg destructive (#DC2626), text white
Ghost:      no bg/border, text accent, hover bg-muted
Icon-only:  40×40px, radius-md, ghost variant
```

All buttons: `cursor-pointer`, `transition: background 150ms ease-out`, `focus-visible: ring`.
Disabled: `opacity-50`, `cursor-not-allowed`.

### Input / Select

```
Height:        40px (--space-10)
Border:        1px solid var(--color-border)
Border-radius: var(--radius-md)
Padding:       0 var(--space-3)
Focus:         border-color: accent, box-shadow: 0 0 0 3px rgba(3,105,161,0.2)
Error:         border-color: destructive
```

Labels always above the field, never as placeholder-only. Help text below in `--text-xs --color-muted-fg`.

### Table

```
Header:       bg --color-primary (dark), text white, --text-sm font-weight 600
Rows:         white default, --color-muted on :nth-child(even) striping
Row hover:    bg #EFF6FF (very light blue), transition 150ms
Cell padding: var(--space-3) var(--space-4)
Border:       bottom 1px solid var(--color-border) on each row
Sticky header: position sticky, top 0, z-index 10
```

Always show loading skeleton (3 ghost rows) while data fetches — never a blank table.

### Badge / Status pill

```
Padding:       var(--space-1) var(--space-2)
Border-radius: var(--radius-sm)
Font:          --text-xs, font-weight 500, uppercase, letter-spacing 0.5px
```

Use status badge palette from §2 — never invent new badge colors.

### Card

```
Background:   var(--color-card)
Border:       1px solid var(--color-border)
Border-radius: var(--radius-md)
Shadow:       var(--shadow-sm)
Padding:      var(--space-6)
```

Cards never have colored top-border strips ("accent bar") — that's a common dashboard cliché. Use the card title and a lucide icon to distinguish card types instead.

### Modal

```
Overlay:      rgba(0,0,0,0.4), no blur
Panel:        bg white, radius-lg, shadow-lg
Width:        min(90vw, 560px)
Padding:      var(--space-6)
Header:       title (--text-lg) + close icon-button (top-right)
Footer:       right-aligned buttons (Cancel secondary, Confirm primary)
```

### Sidebar (navigation)

```
Width:         240px (fixed, not collapsible in v1)
Background:    var(--sidebar-bg) = #0F172A
Logo area:     height var(--header-height), padding var(--space-4)
Nav item:      height 44px, padding 0 var(--space-4), radius-md (inner margin 8px)
               icon (20px) + label --text-sm
Active item:   bg var(--sidebar-item-active), text white, icon accent-colored
Hover item:    bg var(--sidebar-item-hover), transition 150ms
Section label: --text-xs, uppercase, letter-spacing 1px, --color-muted-fg, padding var(--space-4)
```

### Top header

```
Height:   var(--header-height) = 64px
Background: var(--color-card)
Border-bottom: 1px solid var(--color-border)
Content:  page title (left) + user avatar + role badge (right)
```

---

## 7. Interaction & animation rules

| Interaction        | Duration | Easing         | Property            |
| ------------------ | -------- | -------------- | ------------------- |
| Button hover       | 150ms    | ease-out       | background-color    |
| Nav item hover     | 150ms    | ease-out       | background-color    |
| Table row hover    | 150ms    | ease-out       | background-color    |
| Modal open/close   | 200ms    | ease-out       | opacity + transform (translateY 8px → 0) |
| Toast appear       | 250ms    | ease-out       | opacity + translateX |
| Dropdown open      | 150ms    | ease-out       | opacity             |
| Skeleton shimmer   | 1.5s     | linear (loop)  | background-position |

**Hard rules:**
- No `animation-duration` longer than 300ms on user-triggered interactions
- All animations must respect `@media (prefers-reduced-motion: reduce)` — wrap them in that query and provide a no-animation fallback
- No rotation, bounce, or spring physics — this is a work tool, not a game

---

## 8. Page layout blueprints

### Shell (every page)

```
┌──────────────────────────────────────────────────────┐
│  HEADER  [logo]  [page title]    [user] [role badge] │  h: 64px
├────────────┬─────────────────────────────────────────┤
│            │                                         │
│  SIDEBAR   │   CONTENT AREA                          │
│  240px     │   padding: 32px                         │
│  fixed     │   max-width: 1440px                     │
│            │   12-column grid inside                 │
│            │                                         │
└────────────┴─────────────────────────────────────────┘
```

### Dashboard page

```
Row 1: [KPI: Total Classes] [KPI: Total Lessons] [KPI: Teachers] [KPI: Students]
        col-3               col-3                col-3           col-3

Row 2: [Lessons table — recent / upcoming]              [Enrollment summary chart]
        col-8                                            col-4
```

### Class detail page

```
[← Back]  Class: 9B — Spring 2026              [Edit] [Add Lesson]

┌─────────────────────────────────────────────────────────┐
│ Lessons in this class                                   │
│  Subject     Teacher          Students   Schedule  [⋯] │
│  Math        Ahmed Hassan     24         Mon/Wed   [⋯] │
│  Physics     Leila Rahimi     21         Tue/Thu   [⋯] │
│  English     Mark Evans       27         Mon/Fri   [⋯] │
└─────────────────────────────────────────────────────────┘
```

### Lesson detail page

```
[← Back]  Mathematics — Class 9B                  [Edit] [Enroll Students]

[Teacher card — name, dept, avatar]    [Stat: 24 students enrolled]

┌─────────────────────────────────────────────────────────┐
│ Enrolled students                                       │
│  Name            Grade    Enrolled at       [Remove]   │
│  Sara Ahmed      9        2026-02-01        [×]        │
│  Ali Hassan      9        2026-02-01        [×]        │
└─────────────────────────────────────────────────────────┘
```

---

## 9. Dark mode

Dark mode support is **partial in v1** — the sidebar is already dark (`#0F172A`). Full dark mode (inverting the content canvas) is deferred to v2.

To add full dark mode later: add a `data-theme="dark"` attribute on `<html>` and provide a `:root[data-theme="dark"]` block that overrides the tokens in §2 with dark-surface values. Do not use Tailwind's `dark:` prefix — stick to CSS variables so the token system stays in one file.

---

## 10. Accessibility checklist

Before any page ships:

- [ ] **Contrast:** all text passes 4.5:1 on its background (use a contrast checker)
- [ ] **Focus visible:** every interactive element has a visible `:focus-visible` state using `--color-ring`
- [ ] **Labels:** every `<input>` has an associated `<label>` (not just a placeholder)
- [ ] **Tables:** `<thead>` with `scope="col"`, data rows in `<tbody>`
- [ ] **Buttons vs links:** `<button>` for actions, `<a>` for navigation — never a `<div onClick>`
- [ ] **Icons:** all standalone icon buttons have `aria-label` or a visually-hidden span
- [ ] **Color alone:** status is never conveyed by color alone — always pair with text or icon
- [ ] **Motion:** interactions respect `prefers-reduced-motion`
- [ ] **Keyboard nav:** modals trap focus, close on `Escape`, return focus on close
- [ ] **ARIA roles:** modal has `role="dialog"` + `aria-modal="true"` + `aria-labelledby`

---

## 11. CSS custom properties (copy-paste)

Put this entire block in `src/styles/tokens.css`. Import it before `globals.css`.

```css
/* ============================================================
   EduPlatform Design Tokens — generated from ui-ux-pro-max
   DO NOT EDIT values manually — see design-system/MASTER.md
   ============================================================ */

:root {
  /* --- Colors --- */
  --color-primary:         #0F172A;
  --color-on-primary:      #FFFFFF;
  --color-secondary:       #334155;
  --color-accent:          #0369A1;
  --color-accent-hover:    #0284C7;
  --color-background:      #F8FAFC;
  --color-foreground:      #020617;
  --color-card:            #FFFFFF;
  --color-card-fg:         #020617;
  --color-muted:           #E8ECF1;
  --color-muted-fg:        #64748B;
  --color-border:          #E2E8F0;
  --color-destructive:     #DC2626;
  --color-destructive-fg:  #FFFFFF;
  --color-success:         #059669;
  --color-success-fg:      #FFFFFF;
  --color-warning:         #D97706;
  --color-warning-fg:      #FFFFFF;
  --color-ring:            #0369A1;

  /* --- Sidebar --- */
  --sidebar-bg:              #0F172A;
  --sidebar-width:           240px;
  --sidebar-item-fg:         #CBD5E1;
  --sidebar-item-hover:      #1E293B;
  --sidebar-item-active:     #0369A1;
  --sidebar-item-active-fg:  #FFFFFF;
  --sidebar-border:          #1E293B;

  /* --- Typography --- */
  --font-heading: 'Poppins', 'Segoe UI', system-ui, sans-serif;
  --font-body:    'Open Sans', 'Segoe UI', system-ui, sans-serif;

  --text-2xl:  1.5rem;
  --text-xl:   1.25rem;
  --text-lg:   1.125rem;
  --text-base: 1rem;
  --text-sm:   0.875rem;
  --text-xs:   0.75rem;

  /* --- Spacing (4px base unit) --- */
  --space-1:  0.25rem;   /*  4px */
  --space-2:  0.5rem;    /*  8px */
  --space-3:  0.75rem;   /* 12px */
  --space-4:  1rem;      /* 16px */
  --space-5:  1.25rem;   /* 20px */
  --space-6:  1.5rem;    /* 24px */
  --space-8:  2rem;      /* 32px */
  --space-10: 2.5rem;    /* 40px */
  --space-12: 3rem;      /* 48px */

  /* --- Border radius --- */
  --radius-sm:   4px;
  --radius-md:   8px;
  --radius-lg:   12px;
  --radius-full: 9999px;

  /* --- Shadows --- */
  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07), 0 2px 4px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05);

  /* --- Layout --- */
  --header-height:      64px;
  --content-max-width:  1440px;
  --grid-gap:           var(--space-6);
}
```

---

## 12. Anti-patterns (avoid)

These are the most common mistakes that break this design system's coherence. The `ui-ux-pro-max` generator explicitly flagged them for this product type.

| Anti-pattern                        | Why it breaks the system                                   |
| ----------------------------------- | ---------------------------------------------------------- |
| Glassmorphism / backdrop-filter     | Performance hit, inconsistent on school hardware           |
| Colored card top-border "accent bar"| Cliché, adds visual noise without information              |
| Emoji as icons                      | Use Lucide SVG icons — emoji rendering is OS-dependent     |
| Placeholder-only labels             | WCAG failure, terrible UX on mobile                        |
| Hardcoded hex colors in components  | Always use CSS variables — makes theming impossible otherwise |
| `div` with onClick for navigation   | Breaks keyboard nav, screen readers, right-click-open-tab  |
| Box shadows not in §5 table         | Creates depth inconsistency across pages                   |
| Transitions longer than 300ms       | Makes the UI feel sluggish for power users                 |
| Modals without focus trapping       | WCAG 2.5.3 failure                                         |
| Unbounded list queries (no pagination) | Will break when a class has 300+ students               |
