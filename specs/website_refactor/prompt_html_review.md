# Task: Refactor Web Architecture & Modernize HTML/UX Interface

## Context & Objective
We are separating the project's PDF generator and HTML presentation logic into distinct pipelines. While the PDF format will later be expanded into an academic report layout, this task focuses **exclusively on the HTML website**. 

The goal is to refactor the monolithic HTML output into a modular directory structure under `website/`, deployable to GitHub Pages, and redesign the UI/UX to feature tabbed main navigation, sticky elements, an interactive right-hand outline/progress navigator, and a modernized visual design.

---

## Technical Constraints & Non-Negotiables
1. **GitHub Pages Compatibility:** Must build and serve purely via static files (vanilla HTML/CSS/JS or simple static site builder without non-standard server runtimes).
2. **Directory Isolation:** All web-related content, scripts, and stylesheets must live inside a `/website` root folder.
3. **Scope Fence:** **Do not modify PDF generation logic or layout in this phase.** Keep PDF and HTML architectures completely decoupled.
4. **Mobile Scope:** Full responsive design will be tackled in a future iteration. Focus on desktop layouts first, but structure CSS using modern practices (Flexbox/Grid/CSS Variables) to simplify upcoming mobile work.

---

## UX/UI Design Specifications

### 1. Banner Header (Top Area)
- **Content:** Title, project logo/icon, and a brief description.
- **Visual Style:** Softened, modern aesthetic with updated color palettes and high-contrast, accessible typography optimized for screen reading.
- **Scroll Behavior:** Renders naturally at the top of the page. Scrolls away normal as the user scrolls down, leaving only the main horizontal navigation bar pinned to the top.

### 2. Main Horizontal Navigation (Sticky Bar)
- **Positioning:** Located directly below the header banner. Sticks to the top of the viewport (`position: sticky; top: 0`) when scrolling down.
- **Functionality:** Replaces the current single long-page layout. Clicking a section button toggles the active main section without full page reloads.

### 3. Content Panel & Rounded Aesthetic
- **Visual Structure:** Clean, modern UI with rounded corners (`border-radius`), subtle box shadows, and reduced hard edges.
- **Section Sources Box:** Add a distinct callout container at the end of each main section summarizing sources used (styled similarly to the "Key Findings" box).
- **Iconography:** Replace current section icons with standard, clean vector SVGs.

### 4. Right-Hand Progress & Outline Navigation
- **Behavior:** Transforms current summary view into an interactive sticky side-bar navigation guide on the right side of the main content area.
- **Functionality:** Shows the inner sub-headings/content markers for the *currently active* main section. Highlights progress as the user scrolls through sub-sections.

---

## Required Architecture & Directory Layout
Reorganize the repository structure to isolate web code under `website/`:

website/
├── index.html            # Main entry point
├── css/
│   ├── main.css          # Base styles, variables, typography
│   ├── components.css    # Banner, sticky nav, progress bar, callout boxes
│   └── layout.css        # Grid, sticky positioning, sidebar
├── js/
│   ├── navigation.js     # Section switching & sticky nav state
│   └── sidebar.js        # Right-side scroll-spy & progress tracking
└── assets/
├── icons/            # SVG clean iconography
└── images/           # Banner assets / photos

---

## Implementation Plan & Process

Follow the required planning and verification lifecycle:

### Phase 1: Planning & Specification
1. Review the existing codebase and create a detailed breakdown of current HTML sections.
2. Draft a detailed file split plan moving template sections into `website/`.

### Phase 2: Design & Component Validation
1. Prototype CSS variables (colors, fonts, radii, spacing) for the refined layout.
2. Validate mock layout structures using test CSS before applying final styling across all sections.

### Phase 3: Core Implementation
1. Restructure files into the `website/` directory.
2. Implement sticky horizontal navigation and dynamic view-switching logic.
3. Build the right-side interactive progress and table-of-contents navigator.
4. Apply modernized typography, rounded cards, and updated iconography.
5. Implement section source callout boxes at the end of each section.

### Phase 4: Testing & Verification
1. Verify GitHub Pages compatibility (relative link paths, static file serving).
2. Validate section-switching and sticky navigation across Chrome, Firefox, and Safari.
3. Document outstanding tasks for the upcoming **Mobile Responsive Update** in a roadmap document (`website/ROADMAP.md`).

---

## Instructions for Execution
Before making changes:
1. Provide a brief plan outlining how you will split the existing HTML file/template into the `/website` directory.
2. Wait for confirmation or proceed directly with Phase 1 to output the formal spec.
