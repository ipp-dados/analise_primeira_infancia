# Refactoring Task: 30-Slide Deck Update to 32-Slide Deck

## Objective
Refactor the existing 30-slide presentation codebase into a updated 32-slide presentation. Follow the global rules, structural reordering matrix, and slide-by-slide directives below.

---

## Global Directives (Project-Wide Rules)
Apply these rules consistently across ALL slides in the deck:

1. **Age Range Terminology**:
   - Replace all occurrences of `"0 a 5 anos"` with `"72 meses"` (for clarity).
   - Ensure explicit visual/text notes clarify that "0 a 5 anos" corresponds to 72 months.
2. **Poverty & Income Terminology**:
   - Replace `"extrema pobreza"` with `"pobreza"`.
   - Replace `"pobreza/baixa renda"` with `"baixa renda"`.
3. **Cartography & Map Palette Rule**:
   - **NEVER use blue to represent land** on any map visualization.
   - Use warm or neutral tones (e.g., terracotta, ochre, soft grey, or teal accents) distinct from existing palettes.
4. **Zika Terminology**:
   - Standardize all historical Zika references to `"Zika de 2015-2016"`.
5. **Infancy Terminology**:
   - Ensure the phrase `"primeira infância"` is used consistently instead of generic `"infância"`.
6. **Reference Metric Standard**:
   - Use `393 mil` as the standardized population reference across all applicable metric slides (replacing 469 mil where present).
7. **Note about outliers**:
   - make sure you add notes explaining the removal of outliers when needed.

---

## Slide Reordering & Migration Matrix

| New Slide # | Source Slide | Action / Content Summary |
| :--- | :--- | :--- |
| **Slide 01** | Original S01 | Update subtitle |
| **Slide 02** | Original S02 | Update bullet 2 & add bullet 3 |
| **Slide 03** | Original S03 | No changes |
| **Slide 04** | Original S05 | Move S05 → S04; remove bullet; update Zika term |
| **Slide 05** | Original S04 | Move S04 → S05; remove indicator count; edit text |
| **Slide 06** | Original S07 | Move S07 → S06; remove 4th box; group under Data Governance |
| **Slide 07** | Original S08 | No changes |
| **Slide 08** | Original S11 | Move S11 → S08; update reference to 393 mil |
| **Slide 09** | Original S12 | Move S12 → S09; change 469 → 393; highlight center box |
| **Slide 10** | Original S09 | Move S09 → S10; append "principal" to title; recolor map |
| **Slide 11** | Original S10 | Move S10 → S11; no changes |
| **Slide 12** | Original S13 | Update "0 a 5 anos" → "72 meses" |
| **Slide 13** | Original S15 | Move S15 → S13 |
| **Slide 14** | Original S16 | Move S16 → S14; update 0–6 graph to 0–5 (72 meses) |
| **Slide 15** | Original S17 | Move S17 → S15; no changes |
| **Slide 16** | Original S18 | Move S18 → S16; use map without outliers + add note |
| **Slide 17** | Original S19 | Move S19 → S17; add "primeira" before "infância" |
| **Slide 18** | Original S20 | Move S20 → S18; no changes |
| **Slide 19** | Original S14 | Relocate S14 here (Prioridades); update poverty terms |
| **Slide 20** | Original S21 | No changes |
| **Slide 21** | **NEW SLIDE**| Add slide: "Causas Evitáveis por Faixa Etária" |
| **Slide 22** | Original S22 | Move S22 → S22; no changes |
| **Slide 23** | Original S23 | Move S23 → S23; no changes |
| **Slide 24** | Original S24 | Move S24 → S24; reinforce note on "família monoparental" |
| **Slide 25** | Original S25 | Move S25 → S25; generic title; display sum of father + mother |
| **Slide 26** | **NEW SLIDE**| Add slide: Map of Notifications by Bairro (2025) |
| **Slide 27** | Original S26 | Move S26 → S27; no changes |
| **Slide 28** | Original S27 | Move S27 → S28; map without outliers; remove 2nd text block |
| **Slide 29** | **NEW SLIDE**| Add slide: Incomplete Axes (Inclusão, Moradia, Brincar) |
| **Slide 30** | **NEW SLIDE**| Add slide: Missing Axes (Direito à Cidade, Participação) |
| **Slide 31** | Original S29 | Move S29 → S31; no changes |
| **Slide 32** | Original S30 | Move S30 → S32; update contact email |

*(Note: Original Slide 06 is permanently removed from the deck.)*

---

## Detailed Slide Directives

### Slide 01 (Original Slide 1)
- **Subtitle Update**: Set subtitle to:  
  `"Um hub de dados para a Política Municipal Integrada da Primeira Infância do Rio de Janeiro"`

### Slide 02 (Original Slide 2)
- **Bullet 2 Update**: Change to:  
  `"A Política Municipal Integrada da Primeira Infância Carioca precisa de um retrato comum da cidade"`
- **Bullet 3 Addition**: Add new bullet point:  
  `"Precisamos de um retrato das especificidades das diferentes partes da cidade"`

### Slide 03 (Original Slide 3)
- No changes.

### Slide 04 (Original Slide 5)
- **Source**: Move Original Slide 05 to Position 04.
- **Content Removal**: Remove bullet regarding secondary research vs. administrative registers (`"A second group of points about the difference between using Secondary Research public available... vs using Administrative Registers..."`).
- **Terminology**: Update Zika reference to `"Zika de 2015-2016"`.

### Slide 05 (Original Slide 4)
- **Source**: Move Original Slide 04 to Position 05.
- **Content Updates**:
  - Remove explicit mention of the total number of indicators.
  - Change `"só lugar"` to `"centro"`.

*(Original Slide 06 is removed entirely)*

### Slide 06 (Original Slide 7)
- **Source**: Move Original Slide 07 to Position 06.
- **Structure Updates**:
  - Remove the 4th box.
  - Rename the remaining 3 box titles to: `Consistência`, `Periodicidade`, and `Privacidade`.
  - Group these 3 boxes under a single overarching header/concept: `Governança de Dados`.

### Slide 07 (Original Slide 8)
- No changes.

### Slide 08 (Original Slide 11)
- **Source**: Move Original Slide 11 to Position 08.
- **Metric Update**: Update title, main numbers, and body text to use the `393 mil` population reference.

### Slide 09 (Original Slide 12)
- **Source**: Move Original Slide 12 to Position 09.
- **Title Update**: Replace `469` with `393`.
- **Layout & Notes**:
  - Keep 3 boxes, but visually **highlight/emphasize the central box**.
  - Add an explanatory note specifying that `0 a 5 anos` represents `72 meses`.

### Slide 10 (Original Slide 9)
- **Source**: Move Original Slide 09 to Position 10.
- **Title Update**: Append `"principal"` to the end of the slide title.
- **Map Recoloring**: Replace blue land shading with a neutral/warm color tone (Global Cartography Rule).

### Slide 11 (Original Slide 10)
- **Source**: Move Original Slide 10 to Position 11.
- No internal changes.

### Slide 12 (Original Slide 13)
- **Terminology Update**: Change `"0 a 5 anos"` to `"72 meses"`.

### Slide 13 (Original Slide 15)
- **Source**: Move Original Slide 15 to Position 13.

### Slide 14 (Original Slide 16)
- **Source**: Move Original Slide 16 to Position 14.
- **Visualization Update**: Update graph and accompanying text from `0 a 6` to `0 a 5` (72 meses).

### Slide 15 (Original Slide 17)
- **Source**: Move Original Slide 17 to Position 15.
- No changes.

### Slide 16 (Original Slide 18)
- **Source**: Move Original Slide 18 to Position 16.
- **Map Update**: Use the map variant without outliers and include an explanatory note.

### Slide 17 (Original Slide 19)
- **Source**: Move Original Slide 19 to Position 17.
- **Text Update**: Change `"infância"` to `"primeira infância"`.

### Slide 18 (Original Slide 20)
- **Source**: Move Original Slide 20 to Position 18.
- No changes.

### Slide 19 (Original Slide 14)
- **Source**: Relocate Original Slide 14 to Position 19 (classified under the **"Prioridades"** section).
- **Terminology Updates**:
  - Replace `"extrema pobreza"` with `"pobreza"`.
  - Replace `"pobreza/baixa renda"` with `"baixa renda"`.

### Slide 20 (Original Slide 21)
- Move Original Slide 21 to Position 20.
- No changes.

### Slide 21 (NEW SLIDE)
- **New Content**: Create a new slide titled `"Causas Evitáveis por Faixa Etária"`.
- **Visual Asset**: Incorporate the comparison visualization displaying preventable causes across the 3 age groups.

### Slide 22 (Original Slide 22)
- Move Original Slide 22 to Position 22.
- No changes.

### Slide 23 (Original Slide 23)
- Move Original Slide 23 to Position 23.
- No changes.

### Slide 24 (Original Slide 24)
- Move Original Slide 24 to Position 24.
- **Copy Emphasis**: Reinforce and highlight the callout/note regarding `"família monoparental"`.

### Slide 25 (Original Slide 25)
- Move Original Slide 25 to Position 25.
- **Title Update**: Replace specific mention of "mãe" with a broader term (e.g., "pais" / "responsáveis").
- **Chart Update**: Display the combined sum of both father and mother ("pai e mãe"), while preserving individual segregated data as an available option.

### Slide 26 (NEW SLIDE)
- **New Content**: Add a new slide displaying a map of notification totals by neighbourhood in 2025 (`"Soma de Notificações por Bairro em 2025"`).

### Slide 27 (Original Slide 26)
- Move Original Slide 26 to Position 27.
- No changes.

### Slide 28 (Original Slide 27)
- Move Original Slide 27 to Position 28.
- **Visual & Copy Update**:
  - Display map variant without outliers.
  - Remove the second text block (moved to Slide 29).

### Slide 29 (NEW SLIDE)
- **New Content**: Create slide focusing on **Eixos Incompletos ou Ausentes**:
  - **Inclusão e Moradia**: CadÚnico data mapped and currently being imported.
  - **Direito a Brincar**: Incomplete data; requires support from secretariats to integrate existing geospatial administrative records.

### Slide 30 (NEW SLIDE)
- **New Content**: Create slide focusing on missing axes:
  - **Direito à Cidade** & **Participação**: Lack of public data; collaborative solutions needed.
  - Highlight the imperative to incorporate primary research to fill areas without available administrative data.

### Slide 31 (Original Slide 29)
- Move Original Slide 29 to Position 31.
- No changes.

### Slide 32 (Original Slide 30)
- Move Original Slide 30 to Position 32.
- **Contact Update**: Change contact email to:  
  `pesquisaeavaliacao.ipp@prefeitura.rio`