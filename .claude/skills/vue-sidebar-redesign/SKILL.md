---
name: vue-sidebar-redesign
description: Redesigns this app's Vue 3 UI shell into a modern SaaS-style layout with a dark vertical sidebar instead of the top nav bar, plus a consistent spacing/color/radius token system applied app-wide. Use when asked to "redesign the UI", "modernize the interface", "add a sidebar", "convert the top nav to a sidebar", "make it look like a SaaS app", "polish the design", or similar. Applies the redesign directly — does not stop to propose a plan first.
---

# Vue Sidebar Redesign

Transforms the app's navigation shell (`client/src/App.vue`) from a top horizontal nav bar into a
modern SaaS-style vertical sidebar, and introduces a shared design-token system (colors, spacing,
radius, shadows) that the rest of the app's global styles draw from. This is a **fixed, opinionated
design system** — apply the tokens and structure below as specified rather than inventing new ones
or trying to preserve the app's current ad hoc colors.

**This skill applies changes directly.** Do not pause to present a plan for approval — read the
current shell, implement the redesign in this turn, then report what changed and how to verify it.

**Respect the project's own `.vue` file rule**: `client/CLAUDE.md` mandates that any creation or
significant modification of a `.vue` file be delegated to the `vue-expert` subagent. This skill's
actual file edits (to `App.vue`, and to any view file touched during the polish pass) must go
through that agent — hand it this skill's design spec as its brief. Reading files yourself first to
gather context, and verifying afterward (starting the dev server, checking routes), does not need
delegation.

## Scope

1. **Primary**: rebuild `App.vue`'s layout shell — sidebar navigation, top bar, content area.
2. **Secondary (polish pass)**: add a `:root` design-token block to `App.vue`'s global `<style>` and
   migrate the existing global component styles there (`.card`, `.stat-card`, `table`, `.badge`,
   `.loading`, `.error`, etc.) to reference the tokens instead of hardcoded hex values. Since views
   inherit these global classes, this alone carries most of the "consistent spacing, polished look"
   goal across the whole app without having to rewrite every view.
3. **Do not** rewrite every view's scoped `<style>` block line by line. Only touch a view's scoped
   styles if it clashes badly with the new tokens (e.g. a wildly different accent color) or if a new
   route needs a matching sidebar entry.

## Step 1 — Gather current structure (read yourself, no delegation needed)

Read, in this order:
- `client/src/App.vue` — current top-nav markup and the global unscoped `<style>` block
- `client/src/main.js` — the route list, to enumerate every nav destination
- `client/src/locales/en.js` and `ja.js` — the existing `nav.*` i18n keys (reuse these; add new ones
  only for destinations that don't have one yet)

Build the full list of `{ path, i18n key, label }` nav entries from the route list — don't hardcode
just the ones mentioned in this file, since routes may have been added since this skill was written.

## Step 2 — Design tokens (add to `App.vue`'s global `<style>`, at the very top)

```css
:root {
  /* Accent (indigo) */
  --accent-50: #eef2ff;
  --accent-100: #e0e7ff;
  --accent-500: #6366f1;
  --accent-600: #4f46e5;
  --accent-700: #4338ca;

  /* Neutrals */
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;

  /* Semantic */
  --success: #059669;
  --success-bg: #d1fae5;
  --warning: #d97706;
  --warning-bg: #fed7aa;
  --danger: #dc2626;
  --danger-bg: #fecaca;
  --info: var(--accent-600);
  --info-bg: var(--accent-100);

  /* Surfaces & text */
  --surface: #ffffff;
  --surface-sunken: var(--gray-50);
  --border: var(--gray-200);
  --text-primary: var(--gray-900);
  --text-secondary: var(--gray-500);

  /* Sidebar (dark) */
  --sidebar-bg: #111827;
  --sidebar-text: #9ca3af;
  --sidebar-text-active: #ffffff;
  --sidebar-active-bg: rgba(99, 102, 241, 0.16);
  --sidebar-border: rgba(255, 255, 255, 0.08);
  --sidebar-width: 264px;

  /* Spacing scale (use these instead of ad hoc rem/px values) */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-8: 48px;

  /* Radius */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --radius-pill: 999px;

  /* Shadow */
  --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.04);
  --shadow-md: 0 4px 12px rgba(15, 23, 42, 0.08);
  --shadow-lg: 0 12px 32px rgba(15, 23, 42, 0.12);
}
```

Then migrate the existing global rules to use these (examples — apply the same substitution pattern
to every global rule in `App.vue`, not just these):

- `.card { background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1.25rem; }`
  → `background: var(--surface); border-color: var(--border); border-radius: var(--radius-md); padding: var(--space-5);`
- `.stat-value { color: #0f172a; }` → `color: var(--text-primary);`
- `.badge.success { background: #d1fae5; color: #065f46; }` → `background: var(--success-bg); color: var(--success);`
  (apply the equivalent for `.warning`/`.danger`/`.info`)
- `td { color: #334155; }` → `color: var(--text-secondary);` (and `th`/`thead` similarly against `--border`/`--gray-50`)

## Step 3 — Sidebar + shell markup (replace `App.vue`'s template)

Replace the `<header class="top-nav">...</header>` + `<FilterBar />` + `<main>` structure with:

```html
<div class="app">
  <button class="sidebar-toggle" @click="sidebarOpen = !sidebarOpen" aria-label="Toggle navigation">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
  </button>

  <aside class="sidebar" :class="{ open: sidebarOpen }">
    <div class="sidebar-brand">
      <div class="brand-mark">{{ t('nav.companyName').slice(0, 2).toUpperCase() }}</div>
      <div class="brand-text">
        <span class="brand-name">{{ t('nav.companyName') }}</span>
        <span class="brand-subtitle">{{ t('nav.subtitle') }}</span>
      </div>
    </div>

    <nav class="sidebar-nav">
      <!-- One nav-item per route from Step 1. Example for one entry: -->
      <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }" @click="sidebarOpen = false">
        <span class="nav-icon"><!-- icon svg, see Step 4 --></span>
        <span class="nav-label">{{ t('nav.overview') }}</span>
      </router-link>
      <!-- repeat for every route: /inventory, /orders, /restocking, /demand, /spending, /reports, and any added since -->
    </nav>

    <div class="sidebar-footer">
      <LanguageSwitcher />
    </div>
  </aside>

  <div class="app-shell">
    <header class="topbar">
      <FilterBar />
      <ProfileMenu
        @show-profile-details="showProfileDetails = true"
        @show-tasks="showTasks = true"
      />
    </header>
    <main class="main-content">
      <router-view />
    </main>
  </div>

  <ProfileDetailsModal :is-open="showProfileDetails" @close="showProfileDetails = false" />
  <TasksModal :is-open="showTasks" :tasks="tasks" @close="showTasks = false" @add-task="addTask" @delete-task="deleteTask" @toggle-task="toggleTask" />
</div>
```

Add `const sidebarOpen = ref(false)` in `setup()` and return it, for the mobile toggle (Step 5).
Everything else in `setup()` (auth, tasks, i18n) stays as-is — this is a layout-only change.

## Step 4 — Nav icons

Use these minimal inline SVGs (24×24 viewBox, `fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"`) — one per nav item, matched by route purpose:

- **Overview/dashboard**: `<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>`
- **Inventory**: `<path d="M3 7l9-4 9 4-9 4-9-4z"/><path d="M3 7v10l9 4 9-4V7"/><path d="M12 11v10"/>`
- **Orders**: `<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 2h6v3H9z"/><path d="M8 10h8M8 14h8M8 18h5"/>`
- **Restocking**: `<path d="M3 12a9 9 0 0 1 15.3-6.4L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15.3 6.4L3 16"/><path d="M3 21v-5h5"/>`
- **Finance/spending**: `<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/><path d="M6 10v.01M18 14v.01"/>`
- **Demand forecast**: `<path d="M3 17l6-6 4 4 7-8"/><path d="M15 7h5v5"/>`
- **Reports**: `<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>`

For any new route not covered above, pick the closest conceptual match or a simple generic document
icon (`<path d="M6 2h9l5 5v15H6z"/><path d="M14 2v6h6"/>`) rather than leaving a nav item iconless.

## Step 5 — Layout CSS (add to `App.vue`'s global `<style>`, replacing `.top-nav`/`.nav-container`/`.nav-tabs` rules)

```css
.app {
  display: flex;
  min-height: 100vh;
  background: var(--surface-sunken);
}

.sidebar-toggle {
  display: none;
  position: fixed;
  top: var(--space-3);
  left: var(--space-3);
  z-index: 210;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-primary);
  align-items: center;
  justify-content: center;
}
.sidebar-toggle svg { width: 20px; height: 20px; }

.sidebar {
  width: var(--sidebar-width);
  flex-shrink: 0;
  background: var(--sidebar-bg);
  display: flex;
  flex-direction: column;
  padding: var(--space-5) var(--space-3);
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 0 var(--space-3) var(--space-5);
  margin-bottom: var(--space-3);
  border-bottom: 1px solid var(--sidebar-border);
}

.brand-mark {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: var(--accent-500);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.brand-text { display: flex; flex-direction: column; min-width: 0; }
.brand-name { color: white; font-weight: 700; font-size: 0.938rem; letter-spacing: -0.01em; white-space: nowrap; }
.brand-subtitle { color: var(--sidebar-text); font-size: 0.75rem; }

.sidebar-nav { display: flex; flex-direction: column; gap: 2px; flex: 1; }

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  border-radius: var(--radius-md);
  color: var(--sidebar-text);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  position: relative;
  transition: background 0.15s ease, color 0.15s ease;
}
.nav-item:hover { background: rgba(255, 255, 255, 0.04); color: white; }
.nav-item.active { background: var(--sidebar-active-bg); color: var(--sidebar-text-active); }
.nav-item.active::before {
  content: '';
  position: absolute;
  left: -12px;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 20px;
  background: var(--accent-500);
  border-radius: var(--radius-pill);
}

.nav-icon { width: 20px; height: 20px; flex-shrink: 0; display: flex; }
.nav-icon svg { width: 100%; height: 100%; }

.sidebar-footer { padding-top: var(--space-4); border-top: 1px solid var(--sidebar-border); }

.app-shell { flex: 1; display: flex; flex-direction: column; min-width: 0; }

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-6);
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 50;
}

.main-content {
  flex: 1;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--space-6);
}

@media (max-width: 900px) {
  .sidebar-toggle { display: flex; }
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    transform: translateX(-100%);
    z-index: 200;
    transition: transform 0.2s ease;
    box-shadow: var(--shadow-lg);
  }
  .sidebar.open { transform: translateX(0); }
  .topbar { padding-left: var(--space-8); }
}
```

Remove the now-obsolete `.top-nav`, `.nav-container`, `.logo`, `.subtitle`, `.nav-tabs` rules — they
no longer apply to anything.

## Step 6 — Execute

1. Confirm the full nav-entry list from Step 1.
2. Delegate to the `vue-expert` subagent: give it this skill's Steps 2–5 verbatim as the spec, the
   exact current `App.vue` content, and the full nav-entry list, and have it produce the rewritten
   `App.vue`. Also point it at any view whose scoped styles clash with the new tokens (per Scope
   item 3) if you spotted one during Step 1.
3. After the edit lands, verify yourself (no delegation needed): start both dev servers if not
   already running, confirm the app compiles with no console errors, and that:
   - Every route from `main.js` has a working sidebar entry with correct active-state highlighting
   - `FilterBar`, `ProfileMenu`, `LanguageSwitcher`, and both modals still function
   - i18n labels render correctly (switch locale if the app has a language switcher)
   - The sidebar collapses behind the toggle button below ~900px width
4. Report which files changed and the verification steps taken — do not ask for approval before
   doing 1–3, only report the outcome afterward.
