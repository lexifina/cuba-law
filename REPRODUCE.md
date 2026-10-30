# How this repository was made (Cuba)

This file is written by the build on 2026-10-30, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Gaceta Oficial de la República de Cuba: No. 5 Extraordinaria, 10 April 2019 | <https://www.gacetaoficial.gob.cu/sites/default/files/goc-2019-ex5.pdf> | 2026-10-29 | no licence stated |
| Gaceta Oficial de la República de Cuba: No. 93 Ordinaria, 1 September 2022 (Ley 151/2022, Código Penal) | <https://www.gacetaoficial.gob.cu/sites/default/files/goc-2022-o93_0.pdf> | 2026-10-30 | no licence stated |
| Gaceta Oficial de la República de Cuba: Ley No. 59 Código Civil, versión actualizada al 8 de noviembre de 2022 | <https://www.gacetaoficial.gob.cu/sites/default/files/codigo_civil_actualizado_0.pdf> | 2026-10-30 | no licence stated |
| Gaceta Oficial de la República de Cuba: No. 99 Ordinaria, 27 September 2022 (Ley 156/2022, Código de las Familias) | <https://www.gacetaoficial.gob.cu/sites/default/files/goc-2022-o99.pdf> | 2026-10-30 | no licence stated |
| Gaceta Oficial de la República de Cuba: No. 140 Ordinaria, 7 December 2021 (Ley 143/2021, Ley del Proceso Penal) | <https://www.gacetaoficial.gob.cu/sites/default/files/goc-2021-o140_1.pdf> | 2026-10-30 | no licence stated |
| Gaceta Oficial de la República de Cuba: No. 138 Ordinaria, 7 December 2021 (Ley 141/2021, Código de Procesos) | <https://www.gacetaoficial.gob.cu/sites/default/files/goc-2021-o138.pdf> | 2026-10-30 | no licence stated |
| Gaceta Oficial de la República de Cuba: No. 29 Extraordinaria, 17 June 2014 (Ley 116/2013, Código de Trabajo) | <https://www.gacetaoficial.gob.cu/sites/default/files/go_x_029_2014.pdf> | 2026-10-30 | no licence stated |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitucion` | Constitución de la República de Cuba (2019) | 1 | 2019-04-10 to 2019-04-10 |
| `codigo-penal` | Código Penal (Ley No. 151/2022) | 1 | 2022-12-01 to 2022-12-01 |
| `codigo-civil` | Código Civil (Ley No. 59/1987), versión actualizada | 1 | 2022-11-08 to 2022-11-08 |
| `codigo-de-las-familias` | Código de las Familias (Ley No. 156/2022) | 1 | 2022-09-26 to 2022-09-26 |
| `ley-del-proceso-penal` | Ley del Proceso Penal (Ley No. 143/2021) | 1 | 2022-01-01 to 2022-01-01 |
| `codigo-de-procesos` | Código de Procesos (Ley No. 141/2021) | 1 | 2022-01-01 to 2022-01-01 |
| `codigo-de-trabajo` | Código de Trabajo (Ley No. 116/2013) | 1 | 2014-06-17 to 2014-06-17 |

The build made 7 commits:

| Commits | Kind |
| ---: | --- |
| 7 | first version of an act |
| 0 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-10-30.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 6 laws in the record.
- 12 tags.

## Dates

Each commit is dated at noon (America/Havana) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Final provision Segunda: the Constitution enters into force, once proclaimed, from its publication in the Gaceta Oficial; it was proclaimed on 10 April 2019 (Gaceta Oficial No. 5 Extraordinaria, 10 April 2019). https://www.gacetaoficial.gob.cu/sites/default/files/goc-2019-ex5.pdf

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `2aa0233db29c809124253c1ca2e94ab4a658d9dcd8711e9e80af2d42956a5763` (2458393 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3d00541d258745461ab52b1b0cb4e1716a27a95d`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

7 versions of 7 acts read back from git on the day each took effect and on the day before: 0 mismatches. Trailers: 0 commits whose trailers git cannot parse. Health: 0 merge commits on main, 0 commit dates that go backwards, 0 commits dated after the build.

A second build from the same corpus into an empty folder gave identical hashes for all 7 history commits and 12 tags (history tip `443599ff27654ecd0c47b8566b3c8a744d345310`).

## Decisions made by hand

- Spanish is built: the official text is Spanish; no official English text was used.
- One version dated 2019-04-10, the proclamation date, which the final provision makes the in-force date.
- TÍTULO, CAPÍTULO and SECCIÓN headings are kept at the start of the article that follows them; line wraps in the PDF are joined into paragraphs.
- Código Penal (Ley 151/2022): one version dated 2022-12-01. Final provision Segunda makes the Law enter into force ninety days after publication in the Gaceta Oficial (1 September 2022); the first day after those ninety days is 1 December 2022, the date Cuban press gave. Credited to Ley 151/2022 as the act as enacted.
- Código Penal: Libro, Título, Capítulo and Sección headings are kept at the start of the article that follows them; the Anexo (definitions) is its own file; the enacting formula, signatures and page headers are left out.
- Código Civil: the Gaceta Oficial site publishes only an updated edition, current to 8 November 2022; it is recorded as one version dated 2022-11-08, the oldest version available, with the 1987 law as an earlier law. Earlier consolidated texts are not online. Notes in the edition on derogated or modified provisions are kept.
- Código Civil: Libro, Título, Capítulo and Sección headings are kept at the start of the article that follows them; Artículos 542 a 544 (repealed) are one file; page headers are left out.
- Código de las Familias (Ley 156/2022): one version dated 2022-09-26, credited to Ley 156/2022 as the act as enacted. Its final provision Cuadragesimoquinta puts it in force once ratified by the popular referendum; the Gaceta (No. 99 Ordinaria, 27 September 2022) records the referendum of 25 September and the President's signature on ratification on 26 September 2022, which is taken as the in-force day. The text is the ratified edition of No. 99, not the pre-referendum edition of No. 87.
- Phase 2 laws from the Gaceta Oficial: the preamble runs from the first POR CUANTO to the enacting words; Libro, Título, Capítulo and Sección headings are kept at the start of the article that follows them; special, transitional and final provisions are one file each; the formula "PUBLÍQUESE ...", the place and date of approval, the signatures and the page headers are left out; words hyphenated across a line break are joined.
- Ley del Proceso Penal (Ley 143/2021): one version dated 2022-01-01, the in-force day its final provision Séptima sets; credited to Ley 143/2021 as the act as enacted. Later amendments are not replayed.
- Phase 2 laws from the Gaceta Oficial: the preamble runs from the first POR CUANTO to the enacting words; Libro, Título, Capítulo and Sección headings are kept at the start of the article that follows them; special, transitional and final provisions are one file each; the formula "PUBLÍQUESE ...", the place and date of approval, the signatures and the page headers are left out; words hyphenated across a line break are joined.
- Código de Procesos (Ley 141/2021): one version dated 2022-01-01, the in-force day its final provision Quinta sets; credited to Ley 141/2021 as the act as enacted. Later amendments are not replayed.
- Phase 2 laws from the Gaceta Oficial: the preamble runs from the first POR CUANTO to the enacting words; Libro, Título, Capítulo and Sección headings are kept at the start of the article that follows them; special, transitional and final provisions are one file each; the formula "PUBLÍQUESE ...", the place and date of approval, the signatures and the page headers are left out; words hyphenated across a line break are joined.
- Código de Trabajo (Ley 116/2013): one version dated 2014-06-17, the day of its publication in the Gaceta Oficial within the one hundred and eighty days after approval that its final provision Sexta allows, credited to Ley 116/2013 as the act as enacted; its regulation (Decreto 326/2014, in the same issue) and later amendments are not included.
- Phase 2 laws from the Gaceta Oficial: the preamble runs from the first POR CUANTO to the enacting words; Libro, Título, Capítulo and Sección headings are kept at the start of the article that follows them; special, transitional and final provisions are one file each; the formula "PUBLÍQUESE ...", the place and date of approval, the signatures and the page headers are left out; words hyphenated across a line break are joined.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code wrote the parser; it did not write or alter any legal text. 0 model calls at data-build time.
- none
- none
- none
- none
