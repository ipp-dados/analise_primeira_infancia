# TASK SPECIFICATION: 30-Slide Presentation Strategy & Markdown Pipeline

## 1. Context & Objectives
We are developing a high-impact, 30-slide presentation (45-minute delivery) focusing on an early childhood data hub for Rio de Janeiro (Instituto Pereira Passos - IPP).

- **Primary Goal:** Present the project's macro data architecture, city-wide demographic landscape, methodological boundaries, and final digital deliverables (report & website).
- **Secondary Goal:** Make a strong institutional call-for-cooperation to city secretariats to share, enrich, and integrate primary data.
- **Key Focus:** Heavy emphasis on general data trends, city-wide overviews, and territorial distributions, with streamlined thematic sections.

---

## 2. Target Presentation Outline (30 Slides)

### Part I: Context & Call for Collaboration (~6 Slides)
1. **Cover**
2. **Introduction:** What the project is and why it matters
3. **The Data Hub:** A unified repository for Rio’s early childhood
4. **Methodological Scope:** Limitations of relying solely on secondary/administrative data
5. **Call for Cooperation:** Engaging secretariats to contribute domain expertise & data streams
6. **Data Governance & Integration:** Data linkage challenges and source quality overview

### Part II: Macro Data Landscape & Methodology (~14 Slides)
7–8. **Territorial Lens:** Spatial granularity as the report's core value proposition (maps & spatial patterns)
9–10. **Demographic Estimation:** Population estimation methodology (Combining Censo + RIPSA)
11–12. **Data Bias & Nuance:** Why CadÚnico alone is non-representative of Rio's full childhood population
13–20. **City-Wide General Picture (Core Focus):** 
    - Macro demographic trends across Rio
    - Socioeconomic and territorial disparities
    - City-wide childhood indicators and spatial hotspots

### Part III: Concise Section Overview & Products (~10 Slides)
21–25. **Thematic Summary:** High-level sweep of key domain areas (combining minor sections; 1 concise slide per topic with 1–2 key stats)
26. **Deliverables:** The interactive website & printed report ecosystem
27. **Live Demo / Mobile Access:** Website presentation + QR code for immediate mobile access
28–30. **Closing Remarks, Governance Next Steps & Q&A**

---

## 3. Design Guidelines & Visual Standards
- **Institutional Context:** Consult Instituto Pereira Passos (IPP) guidelines to match institutional visual identity and branding standards (palette, typography, layout rules).
- **Text-to-Visual Ratio:** Highly visual. Keep text minimal; prioritize high-impact headlines and key takeaways.
- **Visualization Priority:** Strong preference for maps, spatial heatmaps, demographic charts, and city-wide infographics over text blocks.
- **Key Metrics:** Highlight core macro stats using large callout numbers paired with minimal explanatory text.

---

## 4. Templating Engine (Offshoot / Derivative Versions)
We need a reusable architecture to build derivative/offshoot versions of this deck by simply modifying a single Markdown file.

- **Markdown Schema:** Define a structured markdown template (e.g., `presentation.md`) with clean frontmatter and section flags.
- **Dynamic Ingestion:** Ensure content (text, metric callouts, map references) seamlessly feeds into the slide builder (e.g., Marp, Slidev, or reveal.js).
- **Configurability:** Allow users to swap out target audiences or secretariats by toggling or editing specific markdown blocks.

---

## 5. Execution Routine & Workflow Rules

### Phase 1: Planning & Requirements Gathering
1. Review the proposed 30-slide macro-focused outline against IPP brand and domain goals.
2. Draft slide-by-slide visual layout concepts, prioritizing map visuals and macro charts.
3. Identify missing data points, mapping assets, or technical requirements.
4. **Interactive Checkpoint:** Group all questions logically and prompt the user via `AskUserInput` (or clear text prompts) before moving forward.

### Phase 2: System Setup & Implementation
1. Once approved, create a dedicated Git branch (e.g., `feature/presentation-spec-and-template`).
2. Build the Markdown template schema, slide generator setup, and build pipeline.
3. Generate the core 30-slide deck and document how to generate offshoot decks via Markdown updates.