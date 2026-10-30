# Cuba: law history in git

The law of Cuba as a git history: one file per provision, and the law that made each change as the commit's author, so `git blame` names the law behind every line.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `cu/`.

**What is in it now (retrieved 2026-10-30)**

| Folder | Law | Versions | Language |
| --- | --- | ---: | --- |
| `constitucion/` | Constitución de la República de Cuba, proclaimed 10 April 2019 | 1 | Spanish (the official text; no official English text is used) |
| `codigo-civil/` | Código Civil, Ley No. 59/1987, updated edition current to 8 November 2022 | 1 | Spanish |
| `codigo-penal/` | Código Penal, Ley No. 151/2022 (in force from 1 December 2022) | 1 | Spanish |
| `codigo-de-las-familias/` | Código de las Familias, Ley No. 156/2022, as ratified by the referendum of 25 September 2022 | 1 | Spanish |
| `ley-del-proceso-penal/` | Ley del Proceso Penal, Ley No. 143/2021 (in force from 1 January 2022) | 1 | Spanish |
| `codigo-de-procesos/` | Código de Procesos (civil, family, commercial and labour procedure), Ley No. 141/2021 (in force from 1 January 2022) | 1 | Spanish |
| `codigo-de-trabajo/` | Código de Trabajo, Ley No. 116/2013 (labour code; in force from 17 June 2014) | 1 | Spanish |

Sources: Gaceta Oficial de la República de Cuba No. 5 Extraordinaria, 10 April 2019, No. 93 Ordinaria, 1 September 2022, No. 138 and No. 140 Ordinaria, 7 December 2021, No. 99 Ordinaria, 27 September 2022, No. 29 Extraordinaria, 17 June 2014, and the updated edition of the Código Civil on the Gaceta Oficial site (born-digital PDFs). The Gaceta publishes acts as passed and no consolidated texts, so each has one version.

This is a first, small build, not the whole statute book. It has no amendment history: each act has one version, either the act as enacted (credited to its law and dated the day it took effect) or, for the Constitution and the Código Civil, the oldest version available (credited to the publisher and dated from the source's own date). Texts are in the official language shown above; the English is a translation where marked, and the original governs.

Sources and terms are in `LICENSE`; how it was built is in `REPRODUCE.md`. Not legal advice; for anything that matters, read the original.
