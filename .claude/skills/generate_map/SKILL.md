---
name: generate_map
description: Generate a choropleth (coroplético) PNG map of Rio de Janeiro -- by bairro, Área de Planejamento, or Região de Planejamento -- from any bairro-level table in this project (Censo, DataSUS/Tabnet, CadÚnico, etc.), using geopandas, a drawn-style basemap (contextily), surrounding state/UF and neighboring-municipality context, a north arrow, scale bar, and a cartographic footnote (spatial reference + data source). Discrete classes for absolute counts, continuous colorbar for percentages/rates -- a fixed project convention. Use when the user asks for a map, mapa coroplético, or "mapa por bairro/AP/RP" of some indicator, or to refresh/regenerate an existing one in mapas/.
---

**Note (v6, `specs/2026-09-14_relatorio-interativo`):** this skill's PNG pipeline is still
the source for the notebook, the PDF export, and the geometry itself, but
`relatorio/index.html` (the interactive HTML report) no longer embeds these
PNGs for most indicators — `.claude/skills/export_pdf_report/scripts/build_html_report.py`
now renders an inline interactive SVG choropleth instead (`mapa_svg()`:
GeoJSON → SVG paths, tooltip per bairro/AP/RP/CAP, outlier toggle, CSV
download), reusing the same `dados_locais/geo/*.geojson` files and
`_CORES_TEMA_MAPA` palette this skill documents. If you're asked to add a
new map to the interactive HTML report specifically, check whether
`mapa_svg()` already covers the needed nivel/join before reaching for this
skill's PNG output — this skill is still the right (only) tool for the
notebook/PDF, and for `nivel='cap'` it points at a **different** geojson
(`dados_locais/geo/limite_ap_saude_rio.geojson`, key `cod_ap_sms`) than the
`ap`/`rp` planning levels below — don't conflate the two, they're different
administrative boundaries with similarly-formatted codes.

# Generate map (mapa coroplético por bairro / AP / RP)

Produces a matplotlib/geopandas choropleth PNG of the Rio de Janeiro
municipality, colored by bairro (or by a coarser planning-level
aggregation), from any table in this project that has a per-bairro value.
This was built for the Censo 0-4 anos maps
(`mapas/mapa_censo_0_4_absoluto.png`, `mapas/mapa_censo_0_4_percentual.png`,
plus `_ap`/`_rp` variants of each, generated in `analise.py`'s Censo
section), but the function and join key generalize to every other
bairro-level table in the project.

## Iteration history (read this before assuming today's version is final)

This function went through nine rounds of user feedback in one session,
each changing a real design decision — not just polish. If you're picking
this up cold, skim this table before re-deriving choices from scratch; the
detailed sections below explain the *why* behind each row.

| Round | What changed | Why |
|---|---|---|
| 1 | Built the base function: bairro-level choropleth, `codbairro` join, discrete-bins legend matching `mapa_referencia.jpeg`, plain white background | Initial ask — reproduce the reference map's look in Python |
| 2 | Added `fundo` (satellite **and** drawn-map style), UF boundary overlay, wide aspect ratio, north arrow, scale bar, 300 DPI | User wanted a background image + orientation elements, "like an academic map" |
| 3 | **Dropped satellite entirely** (kept only the drawn-map style, and swapped its provider from `WorldStreetMap` to label-free `OceanBasemap`), added `nivel`/AP/RP aggregation + `agrega_bairros_por_nivel`, neighbor-municipality labels, serif title font, ~10-15% larger text, narrowed to ~A4-landscape ratio | Direct preference after comparing both background styles side by side; new aggregation-level requirement; typography/format polish requests |
| 4 | Absolute counts always discrete bins (even at AP/RP level — was continuous there), continuous colorbar moved down for top clearance, bolder/darker legend text, footnote citing spatial reference + data source | Consistency fix + three legibility/citation requests |
| 5 | Continuous colorbar: **moved back up** (round 4's "move down for clearance" had made overlap with real bairro data worse, not better) **and** given a white background panel behind its tick labels/axis label, which had no backing at all | User reported the colorbar was "still over the map area" after round 4 — the actual bug was missing text backing, not just position; see "Layout" below for why round 4's fix was the wrong mechanism |
| 6 | Removed the border (`edgecolor`) from that round-5 background panel, on the continuous-colorbar (percentage) maps only — kept the white fill | Direct ask to remove "the outer box" from the top-left legend on percent-scale maps; the discrete legend's own bordered box (absolute-count maps) wasn't part of the request and is untouched |
| 7 | Removed the round-5 background panel's `facecolor` too (the whole rectangle is gone now) — legibility moved from a backing box to a white `path_effects.withStroke` halo on each text element instead, the same technique the neighbor-municipality labels already used | Follow-up ask ("remove the fill for the percentage map") — no box left at all behind the continuous colorbar |
| 8 | Footnote's spatial-reference line now says "SIRGAS 2000, UTM - Fuso 23S", copied verbatim from `mapa_referencia.jpeg`'s own citation, instead of a generic "SIRGAS 2000 (EPSG:4326)" | Direct ask to match the reference map's exact wording — a citation choice, not a change to which CRS the code actually plots in (still `EPSG:4326`/`EPSG:3857`, never `EPSG:31983`) |
| 9 | Footnote's `x` anchor nudged left, `0.62 → 0.55` | Round 8's longer citation text pushed the footnote's right edge into the scale bar again — a direct consequence of round 8, not an unrelated request |
| 10 (current) | Default `fundo` changed from `'mapa'` (`Esri.OceanBasemap`) to `'mapa_oceano_base'` (`Ocean/World_Ocean_Base`) | The old service has answered HTTP 500 since 2026-09 (tile requests still failing on 2026-09-25); the successor has the same style. User approved after a side-by-side comparison of the same map (`specs/2026-09-25_relatorio_latex`). Only 8 call sites passed the new key explicitly before, so a full notebook run failed on every other map |

**Print variant (2026-09-25, `specs/2026-09-25_relatorio_latex` Bloco 5):** `mapa_coropletico_bairros` also saves `mapas/a4/<nome>.pdf` via `_a4_mapa` — final A4 size (16 cm), no title/footnote (they go to the ABNT caption), smaller legend/arrow/scale, background downscaled and lightened (38% white) and embedded with `interpolation='none'` (~0.4 MB per map instead of 1.25 MB), and a 95th-percentile colour cap on continuous bairro maps (decision D5). The screen PNG conventions in this file are unchanged.

The throughline: **background style, aggregation level, citation
requirements, and even a prior round's own "fix" all changed after
shipping** — this function is not "done" in the sense of being unlikely to
change again. Treat any hardcoded visual constant here (`_ZONA_LEGENDA`, the
`cax` rect, `x=0.55` for the footnote, the
per-level `bins`) as tuned-by-eye for the current layout, not derived from a
formula — expect to re-tune them together if you change the figure size,
padding, or add another on-map element. And when a user reports the same
*symptom* twice in a row ("it's over the map"), don't assume the same fix
applies — round 4 assumed repositioning would fix round 5's complaint too,
and it didn't, because the actual cause (unbacked text) was different from
what round 4 had actually addressed (clearance from the top edge).

## The reusable piece: `mapa_coropletico_bairros`

Defined in `analise.py`, in **Pacotes e Funções Auxiliares → 📈 Funções de
visualização**. Signature:

```python
mapa_coropletico_bairros(df, coluna_valor, titulo, nome_arquivo, chave=None, nivel='bairro',
                          bins=None, cmap='Oranges', legenda_titulo=None,
                          fundo='mapa', alpha=None, fonte_dados=None,
                          caminho_geojson='dados_locais/geo/limite_bairros_rio.geojson',
                          caminho_uf='dados_locais/geo/limite_uf_brasil.geojson',
                          caminho_municipios='dados_locais/geo/limite_municipios_rj.geojson',
                          formato='png')
```

- `nivel`: `'bairro'` (default) | `'ap'` (Área de Planejamento, 5 regions)
  | `'rp'` (Região de Planejamento, 16 regions). Bairro polygons are
  `.dissolve()`d by the matching geojson column (`area_plane` for `'ap'`,
  `cod_rp` for `'rp'`) before the join with `df`. See "Aggregation levels"
  below — `df` must already carry the matching per-row value at that level
  (use `agrega_bairros_por_nivel` to get there from a per-bairro table).
- `df` needs one row per unit (bairro/AP/RP) and a numeric `coluna_valor`
  column, plus a `chave` column to join against the dissolved boundary layer
  — defaults to the level's own geojson column name (`codbairro`/`area_plane`/`cod_rp`)
  if not given explicitly.
- `bins`: **fixed project convention — always pass `bins` for an absolute
  count, always omit it for a percentage/rate.** A list of upper class
  boundaries (e.g. `[1000, 2500, 5000, 10000]`) → discrete classes with a
  legend styled `Até X` / `X a Y` / `Mais de Z` (matches
  `mapas/mapa_referencia.jpeg`'s legend convention), drawn **inside** the
  map (`loc='upper left'`). Percentages/rates always use a continuous
  colorbar instead (`bins=None`) — also inside the map, via `ax.inset_axes`
  at the same corner (the two modes are mutually exclusive per call, so
  reusing the corner is safe). This was tightened after an early version
  left AP/RP-level absolute counts on a continuous colorbar (to dodge
  picking bins for their very different value range) — the user then asked
  for discrete classes there too, so **each `nivel` needs its own `bins`**,
  see "Aggregation levels" below for the actual numbers used and why one
  fixed list doesn't work across levels. Only the title lives outside the
  map, in the figure's white margin — this is deliberate, see "Layout"
  below.
- `fundo`: `'mapa'` (default — drawn/cartographic basemap, currently Esri
  Ocean Basemap) | `None` (plain white background, no geographic context, no
  north arrow/scale bar/UF overlay/neighbor labels/footnote). **A
  `'satelite'` option existed briefly and was removed** — the user
  explicitly preferred the drawn-map look; see "Background style" below
  before reintroducing satellite imagery.
- `alpha`: choropleth fill opacity. Defaults to `1.0` with no `fundo`, `0.82`
  with one (lets some basemap texture show through).
- `fonte_dados`: short string naming the thematic data's source (e.g.
  `'Censo Demográfico 2022 (IBGE/Data.Rio)'`), shown in the map's footnote
  alongside the spatial reference system — see "Footnote" below. Pass it on
  every real call; it's optional only so the function doesn't hard-fail on
  an old call site that predates this parameter.
- Saves to `mapas/{nome_arquivo}.png` at **300 DPI** with
  `bbox_inches='tight'` (crops the figure to content + a small pad, so no
  wasted white space) and also calls `plt.show()` (consistent with the other
  `visualizacoes/` plotting helpers in the notebook).

## Aggregation levels (`nivel`) and `agrega_bairros_por_nivel`

Rio's bairros nest into two coarser official planning levels, both already
present as columns on the bairro boundary geojson (`dados_locais/geo/limite_bairros_rio.geojson`)
and, conveniently, on the raw Censo/Data.Rio export too
(`dados_locais/censo/pop_censo_2022_datario.csv` → `df_censo`):
- **Área de Planejamento (AP)** — 5 regions, column `area_plane` (int `1`-`5`).
- **Região de Planejamento (RP)** — 16 regions, column `cod_rp` (a string
  like `'4.2'`, i.e. `AP.subregion` — **do not cast to numeric**, `4.2` isn't
  meaningfully orderable/comparable as a float and some values would collide
  or lose precision; keep it as `str` on both the geojson and `df` sides,
  which is what `_NIVEIS_AGREGACAO['rp']['tipo'] = str` does).

To build a `df` for an AP/RP-level map from a per-bairro table, use:

```python
agrega_bairros_por_nivel(df, nivel, colunas_soma)
```

It sums `colunas_soma` (absolute counts only — e.g. `['0 a 4 anos', 'Total']`)
grouped by the level's column, which `df` must already have (true for
`df_censo` — the raw Data.Rio census export already carries `area_plane`
and `cod_rp` per bairro row, natively, so **no merge with the geojson is
needed** for this). **Never aggregate a percentage column by summing or
averaging it directly** — a straight mean of per-bairro percentages ignores
each bairro's population and misrepresents the combined rate. Always sum
the numerator and denominator absolute columns first, then divide:

```python
df_nivel = agrega_bairros_por_nivel(df_censo, 'ap', colunas_soma=['0 a 4 anos', 'Total'])
df_nivel['Percentual 0 a 4'] = (df_nivel['0 a 4 anos'] / df_nivel['Total']) * 100
```

This was a real bug caught during development: an earlier draft of
`agrega_bairros_por_nivel` re-derived the bairro→AP/RP correspondence by
re-reading the boundary geojson and merging it in — which broke, because
`df_censo` already has its own `area_plane`/`cod_rp` columns, so the merge
produced `area_plane_x`/`area_plane_y` duplicate columns and a `KeyError`
downstream. Fixed by dropping the merge entirely and just using the columns
`df` already has. If you extend this to a table that *doesn't* carry
`area_plane`/`cod_rp` natively (e.g. a DataSUS/Tabnet export, which only has
`codigo`/`bairro`), you'll need to join it to `df_censo` (or the geojson) on
`codbairro`/`codigo` first to bring those columns in, *then* call
`agrega_bairros_por_nivel` — don't try to make the function itself do both
steps again, that's the bug that was just fixed.

**Bins are level-specific — don't reuse the bairro list.** AP has only 5
units and a much bigger value range per unit than RP's 16 (both far bigger
than any single bairro), so each level needs its own hand-picked round-number
`bins`, chosen by actually looking at that level's aggregated
min/max/distribution before picking breakpoints (not an automatic
quantile/`scheme=` generator — see "Number formatting" for why this project
avoids `scheme=` for legends generally). For the Censo 0-4 anos absolute
maps specifically:
- bairro: `[1000, 2500, 5000, 10000]` (range ~15 – 18,505)
- AP: `[25000, 50000, 75000, 100000]` (range ~13,699 – 103,779 across 5 units)
- RP: `[12000, 18000, 24000, 30000]` (range ~8,476 – 37,533 across 16 units)

If you add a map for a different indicator/table, recompute its own
level-specific ranges the same way (e.g. `df_censo.groupby('area_plane')[...].sum().describe()`)
rather than copying these numbers — they're specific to "crianças 0-4 anos"
counts and won't fit a different indicator's scale.

## The join key at bairro level: use `codbairro`, not the bairro name

Do **not** join on bairro name strings — this project already has at least
two independently-sourced name spellings (Censo's `Jacarepaguá` vs. the IPP
layer's `Jacarepaguá`/accented variants, `Freguesia (Jacarepaguá)` vs.
`Freguesia (Ilha)` disambiguation, etc.) and matching on strings is fragile.

Instead join on the numeric bairro code, which is consistent across sources
in this project:
- The IPP/Data.Rio boundary layer (`dados_locais/geo/limite_bairros_rio.geojson`)
  has it as `codbairro` (string, zero-padded, e.g. `"001"`).
- The raw Censo file (`dados_locais/censo/pop_censo_2022_datario.csv`) has it
  as `codbairro` too — already carried through into `df_censo` and exported
  in `tabelas_finais/censo_por_bairro.csv`.
- Every DataSUS/Tabnet export cleaned via `limpeza_tabnet_bairros` /
  `carrega_raca_bairro` produces a `codigo` column (e.g. `"001"` for Saúde,
  `"144"` for Campo Grande) — **verified to use the same numbering as
  `codbairro`** (checked against `dados_locais/nascidos_vivos/nascidos_vivos_bairros_2006_a_2025.csv`:
  `001 SAUDE`, `002 GAMBOA`, `003 SANTO CRISTO`... lines up 1:1 with the
  geojson's `codbairro` order). So any of the `df_vivos`, `df_baixo_peso`,
  `df_mortalidade_raca_bairro`, `df_final` (datasus_por_bairro) tables can
  reuse this same join, passing `chave='codigo'`.
- Always cast both sides to `int` before merging (`"001"` vs `1`) — the
  function already does this internally for its own `chave` column and for
  `codbairro`, but if you're joining manually first (e.g. filtering to one
  `ano` before plotting), cast explicitly.

If you ever add a table whose only bairro identifier is a name string, don't
guess a fuzzy match — instead join it to `tabelas_finais/censo_por_bairro.csv`
(or any other table with `codbairro`) via `bairro` first with an exact/
normalized-string join, confirm 166 matches, then carry `codbairro` forward.
`Tabelas_finais/censo_por_bairro.csv`'s `bairro` column is correctly
UTF-8-accented on disk (`Jacarepaguá`, not mojibake) — an earlier mojibake
reading you might see is a terminal/`Bash` tool display artifact when
printing raw bytes with a non-UTF-8 codepage, not a real encoding bug in the
file.

## Boundary layer: `dados_locais/geo/limite_bairros_rio.geojson`

- Source: Data.Rio's ArcGIS Hub item "Limite de Bairros"
  (id `dc94b29fc3594a5bb4d297bee0c9a3f2`), backed by the ArcGIS Feature
  Service at
  `https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Cartografia/Limites_administrativos/MapServer/4`.
  To refresh it: `curl` that URL's `/query?outFields=*&where=1%3D1&f=geojson`
  endpoint. (The Data.Rio Hub page itself is a JS SPA — `WebFetch` won't
  render dataset links off it; the working discovery path was querying
  `https://www.data.rio/api/search/v1/collections/dataset/items?q=<name>`
  and reading the `url` field of the returned Feature Service item.)
- 166 features, CRS `EPSG:4326`, columns include `codbairro`, `nome`,
  `regiao_adm`, `rp` (região de planejamento).
- **Geometry is simplified** (`shapely.simplify(0.00005, preserve_topology=True)`,
  ~98k points → ~19.5k points) to shrink the file from ~4.2MB to ~1MB before
  committing — the original layer's coordinate precision is far beyond what's
  visible at municipality-wide PNG scale. If you ever need higher-fidelity
  geometry (e.g. zooming into a single bairro), re-download the un-simplified
  version rather than assuming this file is full-resolution.
- Unlike `mapas/` and `tabelas_finais/`, `dados_locais/` is **not**
  gitignored in this project — files placed here (including this geojson)
  get committed. Verify with `git status` before assuming otherwise.

## State/UF boundary layer: `dados_locais/geo/limite_uf_brasil.geojson`

- Source: IBGE's malhas API —
  `https://servicodados.ibge.gov.br/api/v3/malhas/paises/BR?intrarregiao=UF&formato=application/vnd.geo+json&qualidade=intermediaria`.
  All 27 UF, ~250KB, no simplification needed (already small).
- CRS `EPSG:4326`. The only property is `codarea` (IBGE's 2-digit UF code,
  e.g. `'33'` = Rio de Janeiro, `'35'` = São Paulo, `'31'` = Minas Gerais,
  `'32'` = Espírito Santo) — no name/`sigla` field, so if you ever need to
  label or filter by UF name, map `codarea` yourself against IBGE's standard
  UF code table.
- Because Rio de Janeiro municipality sits well inside RJ state (not
  bordering another state anywhere near the Censo maps' zoom level), the
  dashed boundary line you see in the rendered maps is mostly the **state's
  coastline**, not an inter-state land border — that's correct/expected,
  not a bug: it's genuinely where the RJ state polygon's edge is. A future
  map at a different zoom/region might actually show a land border with SP
  or MG.

Only used when `fundo` is set — see "Background styles" below for how it's
overlaid.

## Style reference

`mapas/mapa_referencia.jpeg` is an externally-generated (QGIS) reference map
of crianças 0-4 anos por bairro, with a satellite basemap and a 5-class
orange legend (`Até 1.000` / `1.001 a 2.500` / `2.501 a 5.000` / `5.001 a
10.000` / `Mais de 10.000`). `mapa_coropletico_bairros`'s discrete-bins mode
reproduces that legend convention and bin edges regardless of `fundo` — the
default `fundo='mapa'` diverges from the reference in *look* (drawn map, not
satellite: the user's explicit call after seeing both side by side) but the
choropleth classes/legend styling still match it.

## Background style (`fundo='mapa'`): Esri Ocean Basemap

With `fundo` set, the function reprojects to Web Mercator (`EPSG:3857`),
fetches basemap tiles via `contextily.add_basemap`, overlays the Brazil UF
(state) boundary in dashed yellow from `dados_locais/geo/limite_uf_brasil.geojson`,
labels neighboring municipalities, and expands the axis limits beyond the
mapped bounds (15% vertically, 3% horizontally — see "Layout" below) so the
surrounding region (metro area, Baía de Guanabara, open sea) is visible —
this is what makes the state-boundary overlay and neighbor labels
meaningful; without the padding there's no "surrounding" area in frame. The
choropleth is drawn at `alpha≈0.82` on top so basemap texture still shows
through.

The provider (`_PROVEDORES_FUNDO['mapa']`) is
`contextily.providers.Esri.OceanBasemap` — chosen over several alternatives
after visual comparison, in this order:
1. **`Esri.WorldImagery`** (real satellite photography) was the first
   choice, matching `mapa_referencia.jpeg` almost exactly (its "Earthstar
   Geographics" attribution is in fact this same source for many regions).
   The user compared it against a drawn-map alternative and **explicitly
   preferred the drawn style and asked to drop satellite** — don't
   reintroduce it as the default without being asked again.
2. **`Esri.WorldStreetMap`** was the first drawn-map pick — good quality,
   but labels neighboring municipalities (Niterói, Duque de Caxias, Nova
   Iguaçu, Itaguaí, Seropédica...) directly on the map, which the user then
   asked to remove.
3. **`Esri.OceanBasemap`** (current) — same Esri family (no API key, no
   usage-policy risk, `max_zoom=13` which is enough at municipality scale),
   relief-shaded terrain, blue sea, roads shown but **no city/municipality
   name labels**. This is the "higher quality background, without the names
   of neighboring cities" the user asked for.

**Other providers were tried and rejected** — don't reach for them without a
reason to revisit:
- `contextily.providers.CartoDB.Voyager` now renders a big `"API KEY
  REQUIRED"` watermark across every tile — Carto locked free anonymous
  access at some point after this provider preset was added to `contextily`.
- `contextily.providers.OpenStreetMap.Mapnik` returned `403 Access blocked
  — App is not following the tile usage policy of OpenStreetMap's
  volunteer-run servers` — OSM's tile server explicitly disallows this kind
  of unattributed programmatic/bulk fetching.
- `contextily.providers.Esri.WorldTerrain` and `Esri.WorldShadedRelief`
  returned "Map data not yet available" / only support very low zoom levels
  (0-8) at the Rio extent — too coarse for a municipality-scale map.
- `contextily.providers.Esri.WorldPhysical` renders but tiles are visibly
  blurry/pixelated at the zoom this map needs — fails the "higher quality"
  ask.
- **A dedicated Rio/PCRJ basemap was investigated but not used**: the user
  pointed at `https://www.data.rio/apps/mapa-digital-do-rio-de-janeiro-cartografia/explore`
  (an ArcGIS Web AppBuilder app, JS-rendered — blocked automated fetches
  with a 403). Its underlying `pgeo3.rio.rj.gov.br` server exposes individual
  *vector* layers (`Cartografia/Uso_do_Solo`, `CadLog/Trechos_Logradouros`,
  `Quadras_Lotes_Edificacoes`, etc. — land use, street segments, cadastral
  lots) rather than one pre-rendered/cached basemap tile service. Using it
  would mean styling and rendering those vector layers ourselves — a much
  bigger effort than swapping a `contextily` provider, not attempted since
  `Esri.OceanBasemap` already satisfied the ask. Revisit only if a future
  request specifically wants official PCRJ cartographic styling.

## Layout, north arrow and scale bar

Several choices work together to keep the figure's white margin limited to
just the title (per an explicit user request — legend/colorbar, north arrow,
scale bar and neighbor labels all live *inside* the mapped area, never in a
separate white strip):
- **Narrow-ish figure, tuned toward A4 landscape.** Figure size is computed
  from the padded bounding box's actual width/height ratio — `altura_fig =
  8.5` inches, width derived from that ratio, not a fixed square. The
  bairros' own bounding box is intrinsically wide (~1.9:1, Rio is very
  elongated east-west); a square figure around that landscape-shaped content
  is what produced big empty white bands above/below the map in an earlier
  version — don't reintroduce a fixed square/near-square figsize. On top of
  that, **horizontal and vertical padding are deliberately asymmetric**:
  `pady = altura*0.15` (generous vertical context) but `padx = largura*0.03`
  (minimal horizontal context) — set this way on request, to trim the
  basemap's left/right margins (not the bairro data itself) and land close
  to A4 landscape's 1.41:1 ratio; the actual result is ~1.46:1. If a future
  ask wants it even narrower, reducing `padx` further (even slightly
  negative, cropping a couple percent into the bairros' own bbox) gets
  closer to exact A4 — the math: with `pady` fixed at 15%, `aspecto ≈ 1.91 *
  (1 + 2·padx_frac) / 1.3`; solve for the target ratio.
- **`bbox_inches='tight', pad_inches=0.15`** on `savefig` crops the exported
  PNG to content + a small pad, instead of the figure's nominal size — this
  is what actually removes leftover white space, not `plt.tight_layout()`
  alone (kept too, for spacing between elements pre-crop).
- **Legend/colorbar corner:** always `'upper left'` (discrete legend's
  `loc`, or the continuous colorbar's `ax.inset_axes` position) — chosen to
  clear `contextily`'s bottom-left attribution text. Its approximate
  bounding box is hardcoded as `_ZONA_LEGENDA = (0.0, 0.46, 0.34, 1.0)`
  (axes-fraction `x0, y0, x1, y1`) and used to keep neighbor-municipality
  labels from landing on top of it — see below. **Keep `_ZONA_LEGENDA` in
  sync with the colorbar's `cax` rect** if you move either — they're two
  independent hardcoded values that happen to need to agree; nothing
  enforces that automatically.
- **Continuous colorbar position and text legibility:** `cax = ax.inset_axes([0.035, 0.60, 0.03, 0.30])`
  (x0, y0, width, height). This took five rounds to settle — each round
  fixed a real, distinct problem, not a re-litigation of the same one
  (rounds 4 and 5 in particular look like they're undoing round 3, but
  they're not: round 3 solved *legibility*, rounds 4-5 removed the *visual
  weight* of the solution while keeping legibility solved a different way):
  1. Original `y0=0.55, height=0.35` (top at 0.90, only 10% clearance from
     the map's top edge) — flagged as sitting too close to the top ("so it
     don't go over the image").
  2. Moved down to `y0=0.48, height=0.32` (top at 0.80, 20% clearance) —
     this actually made the *overlap-with-real-data* problem worse, not
     better: at bairro level (unlike AP/RP), Rio's Zona Oeste bairros extend
     almost to the top of the padded frame on the left side, so a lower
     colorbar sat squarely on top of colored bairro polygons instead of
     empty basemap margin. The user then reported it was "still over the
     map area" and asked to move it toward the top.
  3. Moved back up to `y0=0.60, height=0.30` (closer to the original
     position, not further from it — round 2 moved the wrong direction),
     **plus** a white background patch (`ax.add_patch(plt.Rectangle(...))`,
     drawn just before `cax` is created) sized to cover the bar *and* its
     tick labels *and* its rotated axis label — `(cax_x0-0.02, cax_y0-0.025)`
     to `+0.175 width, +0.05 height`. This was the fix that actually
     mattered: **tick labels and the y-axis label render outside `cax`'s own
     bounds, in the parent axes' space, with no opaque background of their
     own** (unlike the discrete legend, which gets a white box for free via
     `legend_kwds={'framealpha':..., 'facecolor': 'white'}`) — so no matter
     where the colorbar sits, its *text* was always going to be unreadable
     over a busy basemap/choropleth without an explicit backing. Moving
     `y0` alone was solving the wrong problem; don't repeat that mistake if
     asked to reposition this again — check whether it's a legibility
     complaint (needs the backing panel) or a pure overlap-with-data
     complaint (needs repositioning) before picking a fix.
  4. **`edgecolor` on that background patch was then set to `'none'`**
     (originally `'#c9c9c9'`, matching the discrete legend's border) — the
     user asked to remove "the outer box" from the percentage-scale maps
     specifically. Scoped to the continuous-colorbar branch only; the
     discrete legend's own bordered box (absolute-count maps) was never in
     question and still has `edgecolor='#c9c9c9'`.
  5. **The background patch was then removed entirely** (`facecolor` too,
     not just the border — the user's next ask was "remove the fill for the
     percentage map" as well). With no backing box left at all, legibility
     had to move to the *text itself*: the colorbar's tick labels and axis
     label each get a white halo via
     `matplotlib.patheffects.withStroke(linewidth=3, foreground='white')`
     (`.set_path_effects([...])`, applied after `.set_fontweight`/`.set_color`)
     — the same technique `_adiciona_rotulos_municipios_vizinhos` already
     used for neighbor-city labels. This is the current state: **no
     rectangle patch of any kind behind the continuous colorbar**, only a
     halo on each text element. If asked to add any box/panel back here,
     confirm first — three consecutive rounds (3, 4, 5) removed it piece by
     piece on direct request, so reintroducing one is very likely to be
     unwanted rather than an oversight to "fix."
  If you touch the position again, `_ZONA_LEGENDA`'s `y0` (above) needs to
  stay ≤ this `cax`'s `y0` with some margin, and re-check the footnote/scale-bar
  corners below don't newly collide with whatever moved.
- **North arrow** (`_adiciona_rosa_dos_ventos`, right above the main
  function): a simple annotated arrow + "N" label at axes-fraction
  `(0.94, 0.90)`, i.e. upper-right — deliberately a plain arrow, not an
  imported compass icon/image, to avoid another asset dependency for
  something this simple.
- **Scale bar** (`matplotlib_scalebar.scalebar.ScaleBar`, lower-right):
  needs a real ground-distance-per-map-unit `dx`. Web Mercator (`EPSG:3857`)
  distorts distance by latitude — **1 map unit ≠ 1 meter** except at the
  equator. The function computes `cos(radians(latitude_media))` from the
  mapped geometry's mean latitude (~-23° for Rio → correction factor
  ≈0.921) and passes that as `dx`. Skipping this correction would overstate
  every distance on the scale bar by ~8.6% — don't hardcode `dx=1` for a Web
  Mercator map at any real-world latitude.
- North arrow, scale bar, and the UF overlay only apply when `fundo` is set
  — with `fundo=None` there's no basemap to orient against. The footnote
  (below) is the one exception: it's added **unconditionally**, with or
  without `fundo` — only its "sistema de referência" line's wording changes.

## Footnote: spatial reference + data source citation

Every map gets a small citation box, bottom-center-ish, reproducing the
convention on `mapas/mapa_referencia.jpeg` (which has its own boxed footer:
"Sistema de Referência: SIRGAS 2000, UTM - Fuso 23S" / "Fonte: DATA.RIO").
Two lines:
1. Spatial reference — `'Sistema de referência: SIRGAS 2000, UTM - Fuso 23S
   (dados) | Web Mercator EPSG:3857 (mapa)'` when `fundo` is set (the
   geometry gets reprojected to Web Mercator for basemap tiles to align —
   the same reason the scale bar needs a latitude correction, see above),
   or just `'Sistema de referência: SIRGAS 2000, UTM - Fuso 23S'` with
   `fundo=None` (no reprojection happens, data stays in the source CRS).
   **"SIRGAS 2000, UTM - Fuso 23S" is copied verbatim from
   `mapa_referencia.jpeg`'s own citation** — it's the standard
   name/projection combo Brazilian cartography uses for Rio de Janeiro
   (SIRGAS 2000 datum, UTM zone 23S projection, `EPSG:31983`), added on
   direct request to match that reference exactly. **This is a citation of
   the data's nominal/official reference system, not a technically precise
   description of what's actually plotted**: the source geojson is read
   back by geopandas as `EPSG:4326` (geographic degrees, not the projected
   UTM 23S metres), and with `fundo` set the geometry is further
   reprojected to `EPSG:3857` for basemap tiles — the code never touches
   `EPSG:31983` at any point. Don't "fix" this by reprojecting the geometry
   to actually match the label; the wording follows the same convention
   the reference map itself uses (citing the region's standard SIRGAS
   2000/UTM 23S reference by name, independent of the specific CRS a given
   render happens to use).
2. `'Fonte: {fonte_dados}'` — only appended if the caller passed
   `fonte_dados`; every real call site in `analise.py` does (`fonte_censo =
   'Censo Demográfico 2022 (IBGE/Data.Rio)'`, reused across all 6 Censo map
   calls).

**Placement took four tries** — every corner is already claimed by
something else, so this is worth understanding before moving it again:
- Bottom-right (first try): collided with the scale bar, which also lives
  bottom-right — the scale bar's black bar and "15 km" label were rendering
  right through/behind the footnote box.
- Bottom-center, single line joined with `|` (second try): cleared the
  scale bar, but at `fontsize=7` on one line it ran wide enough to collide
  with `contextily`'s bottom-left attribution text (itself 2 lines,
  variable width depending on which basemap tiles/sources were used for
  that particular render).
- `x=0.62` (third try, two lines): cleared both at the time, but the
  spatial-reference line later grew longer ("SIRGAS 2000, UTM - Fuso 23S"
  added — see the Footnote text section above) and started crowding the
  scale bar again on its right edge.
- **What it does now:** `x=0.55` (nudged left from 0.62), still two lines
  (`\n`-joined, not `|`-joined), `fontsize=6.5` — clear of both the
  attribution (left) and the scale bar (right) across bairro/AP/RP renders
  with the current (longer) text. If you change the footnote text length
  materially again (e.g. a much longer `fonte_dados`, or another line),
  re-check both edges — `x=0.55` was tuned by rendering and eyeballing, not
  computed from measured text widths, and has already needed to move once
  as the text grew.
- Rendered as `ax.annotate(..., bbox=dict(boxstyle='square,pad=0.35',
  facecolor='white', alpha=0.8, edgecolor='none'))` — a translucent white
  box behind the text, same idea as `contextily`'s own attribution
  background, for legibility over the busy basemap without needing a
  per-character halo like the neighbor labels use.

## Neighboring municipality labels

`_adiciona_rotulos_municipios_vizinhos` (right above the main function)
labels the RJ-state municipalities bordering Rio de Janeiro — added back
after switching the basemap away from `WorldStreetMap` (which had these
baked into the tiles) to the label-free `OceanBasemap`; the user
specifically asked for the neighbor names back, but not Rio de Janeiro's own
name (redundant — it's the map's whole subject).

Source: `dados_locais/geo/limite_municipios_rj.geojson` — all 92 RJ-state
municipality boundaries + names, built from two IBGE endpoints (geometry
from the malhas API, names from the localidades API, joined on the 7-digit
municipality code) and lightly simplified. Same "not gitignored" rule as
the other `dados_locais/geo/` layers applies — it's tracked in git.

Getting a clean label per visible municipality took two iterations, both
worth knowing before touching this function again:
1. **Naive approach (representative point of the full, unclipped polygon,
   only keeping points that fall inside the padded window):** wrongly
   *excludes* legitimate neighbors whose visible chunk is a real, sizeable
   sliver near the frame edge (Niterói, São Gonçalo, Duque de Caxias, Nova
   Iguaçu, Magé...) — their true polygon centroid sits well outside the
   window even though a meaningful, clearly-visible piece of their territory
   is on screen.
2. **Naive fix (representative point of the window-clipped fragment):**
   solves that, but now wrongly *includes* municipalities that barely touch
   a corner of the frame with a razor-thin sliver (e.g. Rio Claro, ~35km
   away, clipped down to a tiny triangle) — the label renders half cut off
   by the plot edge, since its clipped fragment's representative point sits
   right on the boundary.
3. **What the function actually does:** representative point of the
   clipped fragment (fixes #1), *then* discard any such point closer than
   `margem=0.02` (2% of the window's width/height) to the frame edge (fixes
   #2 — a genuinely tiny corner sliver's clipped centroid ends up near that
   edge; a real, substantially-visible neighbor's doesn't). Verified: with
   this margin, Rio Claro drops out and Niterói/São Gonçalo/Duque de
   Caxias/etc. stay in. If you change the window padding (`padx`/`pady` in
   the main function) or the label margin, re-check both a genuinely-tiny
   sliver case and a real-neighbor-near-the-edge case, not just one.
4. On top of that, any label landing inside `_ZONA_LEGENDA` (see "Layout"
   above) is dropped — otherwise e.g. Itaguaí/Seropédica's labels collide
   with the upper-left legend/colorbar in the narrower (post-A4-fit) crop.

Labels use a white `path_effects.withStroke` halo instead of an opaque
background box, so they stay legible over the busy basemap without adding
more visual chrome.

## Dependencies

`geopandas`, `shapely`, `pyproj`, `pyogrio`, `mapclassify` for the vector
side; `contextily` (and its own deps: `affine`, `geopy`, `joblib`,
`mercantile`, `rasterio`, `xyzservices`) for basemap tile fetching;
`matplotlib-scalebar` for the scale bar — all pinned in `requirements.txt`.
`mapclassify` is only needed if you use geopandas' `scheme=` machinery
directly; the current `mapa_coropletico_bairros` implementation builds bins
manually with `pd.cut` instead (for full control over pt-BR-formatted legend
labels — see next section), so it's a soft dependency, but keep it installed
in case a future variant wants a `scheme=` (quantiles, natural breaks,
etc.). Fetching basemap tiles needs network access at render time (unlike
the plain `fundo=None` mode, which is fully offline once the two
`dados_locais/geo/` files are on disk).

## Design choices (per the `dataviz` skill)

`Oranges` (a single-hue sequential ramp, light→dark) is the right color
choice for this map's job — magnitude by bairro/AP/RP — per `dataviz`'s
color formula (sequential = one hue; never a rainbow for magnitude), and it
was already the project's convention before this skill existed, so it
wasn't changed. It's a standard ColorBrewer-family ramp; the skill's
`validate_palette.js` targets web/CSS hex palettes for categorical/diverging
use and doesn't add value re-checking a single well-established sequential
ramp here, so it wasn't run for this raster/PNG output. Other polish applied
per the same skill's spirit (thin marks, legible legend, recessive
chrome): 0.4pt bairro borders instead of heavier lines, a white
`framealpha≈0.9` legend background with a light `#c9c9c9` border for
contrast over a busy basemap, and dark neutral ink (`#262626`) for the north
arrow/scale bar/neighbor labels rather than pure black.

**Legend text contrast:** legend/colorbar text is set to `color='#111111'`
(near-black, via `legend_kwds={'labelcolor': ...}` for the discrete legend,
`cax.tick_params(colors=...)` + `.yaxis.label.set_color(...)` for the
colorbar) plus a heavier weight — `'semibold'` for legend items and colorbar
ticks, `'bold'` for both titles/labels — applied by grabbing the rendered
objects after `.plot()` (`ax.get_legend()` for the discrete case,
`cax.get_yticklabels()`/`cax.yaxis.label` for the continuous one) since
`legend_kwds` alone doesn't expose a font-weight knob. Requested directly
("give the fonts for the legends a little more contrast") after the plain
default-black legend text read as a bit thin/light against the textured
basemap underneath it. On the continuous colorbar specifically, this
color/weight styling is no longer enough on its own since the backing box
behind it was later removed entirely (see "Layout" above, rounds 5-7) — a
white `path_effects.withStroke` halo on each text element does the rest of
the legibility work there.

**Typography** ("think of it as an academic publication map" — a direct
request): the title uses `_FONTE_TITULO = 'Palatino Linotype'` (bold,
`fontsize=22`, up from a sans-serif default at `15`) — a classic humanist
serif with a scholarly-atlas feel, available as a Windows system font (no
bundling/licensing needed; confirmed via `matplotlib.font_manager` against
this machine's installed fonts — `Cambria`, `Constantia`, `Georgia`, `Times
New Roman` are the other available serif options if `Palatino Linotype`
isn't installed in some other environment). Every other on-map text
(legend items/title, colorbar ticks/label, north arrow, scale bar, neighbor
labels) stayed in the default sans-serif but got ~10-15% larger than the
pre-existing sizes — legend items `9→10`, legend title (newly set
explicitly, previously same as items) `→12`, colorbar ticks `8→9`, colorbar
axis label (newly set) `→11`, north arrow `13→15`. The title's jump is
proportionally much bigger than the rest — that's intentional, matching
"make the title larger" as a separate, stronger instruction from "other text
elements 10 to 15% larger."

## Number formatting

Legend labels for the discrete-bins mode use `_numero_ptbr` (also in
analise.py, right above `mapa_coropletico_bairros`) to render thousands with
a `.` separator (`10000` → `"10.000"`), matching Brazilian convention and
the reference map. This was a deliberate choice over geopandas/mapclassify's
built-in `scheme='UserDefined'` + `legend_kwds={'fmt': ...}`, which was
tried first and does **not** apply the `fmt` to scheme-based legends — it
prints the raw bin-edge tuples (`"15,  1000"`) instead. Don't reach for
`scheme=`/`classification_kwds` for this project's legends; build the
categorical column with `pd.cut` and pre-formatted labels instead, as the
current function does.

## Quick recipe for a new map

```python
# bairro level, absolute count: df has one row per bairro with a 'codigo' or 'codbairro' column
mapa_coropletico_bairros(
    df, coluna_valor='sua_coluna_absoluta',
    titulo='Título do mapa',
    nome_arquivo='mapa_nome_do_arquivo',   # -> mapas/mapa_nome_do_arquivo.png
    chave='codigo',                          # or 'codbairro', matching df's column
    bins=[...],                              # absolute counts: ALWAYS pass bins (discrete classes)
    legenda_titulo='Legenda',
    fonte_dados='Nome da fonte (ano)',       # shown in the footnote alongside the CRS
    # fundo='mapa' is already the default (drawn basemap + north arrow + scale bar
    # + neighbor labels + footnote); pass fundo=None for a plain white background
    # with no geographic context (footnote still shows, minus the basemap-specific bits).
)

# bairro level, percentage/rate: omit bins -- ALWAYS a continuous colorbar
mapa_coropletico_bairros(
    df, coluna_valor='sua_taxa', titulo='Título', nome_arquivo='mapa_taxa',
    legenda_titulo='% ...', fonte_dados='Nome da fonte (ano)',
)

# AP/RP level: aggregate first (df must carry 'area_plane'/'cod_rp' -- true for
# df_censo; for other tables, join those in from df_censo/the geojson first). Absolute
# still needs bins -- but level-specific ones (AP's 5 units and RP's 16 have very
# different value ranges from each other and from bairro-level; look at the actual
# aggregated min/max before picking round numbers, don't reuse the bairro list)
df_nivel = agrega_bairros_por_nivel(df, nivel='ap', colunas_soma=['sua_coluna_absoluta', 'Total'])
df_nivel['sua_taxa'] = df_nivel['sua_coluna_absoluta'] / df_nivel['Total'] * 100  # nunca média das taxas
mapa_coropletico_bairros(
    df_nivel, coluna_valor='sua_coluna_absoluta', nivel='ap',
    titulo='Título do mapa, por Área de Planejamento',
    nome_arquivo='mapa_nome_do_arquivo_ap', bins=[...], legenda_titulo='Legenda',
    fonte_dados='Nome da fonte (ano)',
)
```

Run it from a cell within `analise.py` (or standalone with the function
copy-pasted, as done to validate this skill) after `df_censo`/the relevant
DataSUS table is loaded. `mapas/` is gitignored, so regenerating these PNGs
never shows up as a diff to review — only `analise.py` changes (new call
sites) and any changes to `dados_locais/geo/` or `tabelas_finais/` schemas
(e.g. adding a `codbairro` export column, as done for Censo) are.

## Nível `ra` (Região Administrativa)

`nivel='ra'`, `chave='codra'` (inteiro): une os bairros por `codra` (33 RAs, não existe a 32) — mesma rota de AP/RP, sem geojson extra.
Junte sempre pelo `codra` numérico (o IPS traz numeral romano + nome; converta com `numeral_romano_para_int`). Se o basemap padrão
(`Ocean_Basemap`) devolver HTTP 500, use `fundo='mapa_oceano_base'`.
