# Regulations — what is here and what is missing

Uploaded 5 September 2026 as 25 files. Ten distinct documents; the other fifteen were
**byte-identical** re-downloads of the same file, so nothing had to be judged between versions —
every set of duplicates had one identical SHA-256. They were removed. Three more documents arrived
on 7 September and are noted below.

## F.C.I. — the international baseline

| File | Document | Pages | Approved |
|---|---|---|---|
| `FCI-ABR-REG-S-C-en.pdf` | International Field Trial Regulations for **Individual and Paired** events for British Pointing Dogs | 6 | — |
| `FCI-ABR-REG-GQU-en.pdf` | International Regulations of **Grande Quête** field trials for British Pointing Dogs | 2 | — |
| `FCI-ACO-REG-en-2019.pdf` | Official Rules and Bylaws, **Continental Pointers** | 42 | ratified June 1999, Mexico City; §VIII amended Como, September 2019 |
| `FCI-ACO-REG-de-2019.pdf` | the same, German | 41 | §VII amended Como, September 2019 |
| `FCI-ACO-REG-fr-2011.pdf` | the same, French | 41 | **older edition** — bold text approved Paris, July 2011 |
| `FCI-REG-TIT-en-2024.pdf` | Regulations for the F.C.I. **International Championship** — C.I.T., CACIT, RCACIT | 21 | amended March 2024 and September 2024 |
| `FCI-ABR-REG-S-C-da.pdf` | the Individual and Paired regulations, **in Danish** | 6 | — |

The first two are the ones that govern what Κ.Ο.Α.Δ. runs.

## National

| File | Document | Pages | Date |
|---|---|---|---|
| `../national/SCC-CUNCA-reglement-FT-fr-2026.pdf` | S.C.C. / C.U.N.C.A., **Règlements des Épreuves de Travail pour chiens d'arrêt** — field-trials, Grande Quête, épreuves à la française, BICP, TAN | 53 | in force 1 February 2026; amendments approved by the S.C.C. Committee 29 January 2026 |
| `../national/SCC-lexique-travail-fr.pdf` | S.C.C., Lexique travail — French working-trial vocabulary | 5 | — |
| `../national/VPS-Pruefungsordnung-de-2026.pdf` | Verein für Pointer und Setter e.V., **Prüfungsordnung** | 48 | Fassung Januar 2013, Stand 14 August 2026 |
| `../national/ENCI-prove-razze-da-ferma-it-2024.pdf` | ENCI, Regolamento delle prove – verifiche zootecniche per i cani delle razze da ferma | 24 | Consiglio Direttivo 6 February 2024 |
| `../national/ENCI-razze-gruppo7-it.html` | ENCI, Libro genealogico — **Elenco Razze Gruppo 7**, the Italian breed nomenclature | — | saved page, `enci.it/libro-genealogico/razze?idGruppo=7` |
| `../national/JGHV-VSwPO-VFsPO-de-2026.pdf` | JGHV Verbandsschweißprüfungsordnung / Verbandsfährtenschuhprüfungsordnung | 32 | Verbandsversammlung 15 March 2026, in force 1 December 2026 |

## `breeds-g7-5lang.json` — F.C.I. Group 7 in six languages

All 36 breeds of Group 7, keyed by **F.C.I. standard number**, with the club's Greek register name
beside the F.C.I.'s own English, French, German and Spanish and the ENCI's Italian:

```json
{"no": 6, "sec": "2", "en": "Gordon Setter", "fr": "Setter Gordon",
 "de": "Gordon Setter", "es": "Gordon Setter", "it": "SETTER GORDON",
 "country": "Great Britain", "el": "Σέττερ Γκόρντον"}
```

- **Nothing here is translated.** Each name is the one its own federation publishes. Italian comes
  from the ENCI page above and is stored exactly as ENCI writes it — capitals included, and
  *BRACCO D'ARIEGE* and *EPAGNEUL BLUE DE PICARDIE* keep ENCI's own spelling rather than being
  "corrected" towards the French. The F.C.I.'s official languages are French, English, German and
  Spanish; Italian is not among them, which is why ENCI is the authority for it.
- **How the Italian names were matched to the numbers.** 25 of the 36 ENCI pages carry the breed
  photo, and the image filename *is* the F.C.I. standard number — `002.jpg` for SETTER INGLESE,
  `202.jpg` for BRACCO ITALIANO. The other eleven have a placeholder image, so they were paired by
  name against the F.C.I. French, which each one reproduces word for word: BRACCO D'ARIEGE ↔ 177
  *Braque de l'Ariège*, EPAGNEUL DE PONT-AUDEMER ↔ 114 *Epagneul de Pont-Audemer*, and so on. The
  result was checked to be one-to-one: 36 in, 36 out, no number used twice, nothing left over on
  either side — and it joins to the app's own register exactly, 36 for 36.

## Three things worth knowing

- **`FCI-ABR-REG-S-C-da.pdf` is Danish, not English.** It was collected as an English mirror of the
  British regulations; it is the same regulation translated. Text similarity with the English
  original is 7.6% — the headings read *INTERNATIONALE MARKPRØVEREGLER FOR INDIVIDUELLE - OG PRØVER
  MED PARSØG FOR STÅENDE ENGELSKE HUNDE*. Harmless, since the genuine English text is here too.
- **The French continental regulation is an older edition than the English and German.** English and
  German carry the September 2019 amendment; the French copy stops at July 2011. For French
  terminology it is still the F.C.I.'s own wording, but a rule read from it must be checked against
  the English before it is relied on.
- **`JGHV-VSwPO-VFsPO-de-2026.pdf` is the wrong discipline.** `VSwPO / VFsPO` are the JGHV's
  *blood-tracking* and *tracking-shoe* examination rules — Schweißarbeit, not pointing-dog field
  trials. It is kept because it is a genuine JGHV document, but the German pointing-dog terminology
  comes from `VPS-Pruefungsordnung-de-2026.pdf`, which is now here.

## Still missing

- The **current ENCI trial regulation**, modified by the Consiglio Direttivo on 17 April 2026, which
  replaces the February 2024 edition held here. The 2024 copy is still usable for the shape of the
  Italian rules; a rule read from it must be checked against the current one before it is relied on.
