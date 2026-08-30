# Κ.Ο.Α.Δ. Trial Manager — Build Instructions for Claude Code

**Client:** Κυπριακός Όμιλος Αγγλικών Δεικτών (Κ.Ο.Α.Δ.) / Cyprus Pointer & Setter Club
**What it does:** the head judge runs the brace draw on a phone or laptop in the field, notifies handlers by SMS, records structured judge notes and qualifications, and keeps a permanent history of trials, dogs and results.
**UI language:** Greek only. Code, comments and database identifiers in English.

---

## 0. Skills you must use

These are not optional. Load each one before you write the code it governs.

| Skill | Use it for |
|---|---|
| **`/hellenic-linguist`** | Every string that reaches the screen. All UI labels, buttons, validation messages, SMS text, export headers and print output are Greek. Monotonic system, correct grammar and syntax, no machine-translation phrasing. |
| **`/greek-how-to-write`** | Making the Greek read like a Cypriot cynophile wrote it, not like a translated app. The trial vocabulary is fixed by the club's own regulation — τερέν, ζεύγος, κυναγωγός, φέρμα, πόντος, λευκή φέρμα, ποντάρισμα, συναίνεση, μπαράζ, κλήρωση, επανάκληση, βαθμολογία. Never invent a synonym for any of these. |
| **`/write-like-a-human`** | Error messages, empty states, help text, README and code comments. No promotional tone, no significance inflation. An error states what happened and what to do about it. |
| **`/frontend-design`** | All visual and interaction work. Read it together with the design brief (`02_CLAUDE_DESIGN_BRIEF.md`) before building any screen. |

Run `/hellenic-linguist` and `/write-like-a-human` again over the finished string table as a review pass before handover. Bad Greek in a Greek-only app is a defect, the same as a broken draw.

---

## 1. What already exists

`KOAD_Trial_Manager.html` is a working single-file app, about 140 KB, no dependencies, no internet required. It is the **reference implementation and the acceptance target**, not a mockup. It already does:

- dog / handler / judge registry, with the dog and its owner entered on one screen
- import from Excel (.xlsx), Word (.docx table) and CSV, with automatic header detection and a column-mapping step
- trial setup, unlimited terrains, judges assigned to each terrain by the head judge
- a seeded, reproducible, constraint-respecting brace draw
- trailer dogs on odd braces, and επανάκληση (Άρθρο 30) with its own note sheet
- an SMS queue that sends the full day order with each handler's own braces marked, from the head judge's phone
- structured judge notes, qualifications, points and season standings
- Excel export with live formulas, plus Word, CSV and print/PDF
- device-to-device transfer through the phone's share sheet (WhatsApp, Viber, Messenger, email)

**Read that file before you start.** Do not redesign what works. Your job is one of the two tracks below.

**Scope: one app, two devices.** It runs as a single HTML file with no server and no build step, and it must work identically on a laptop, an iPhone and an Android phone. That is the requirement, not a preference. There is no backend, no database server and no hosting to administer. Do not propose one.

Data moves between devices as a file the user sends over WhatsApp, Viber, Messenger or email — see §10.

---

## 1a. Cross-device requirements — read this before writing anything

The app must behave the same on all three targets. Two of them have traps.

**Safari refuses `localStorage` on `file://` URLs.** If someone emails himself the HTML and opens it from the Files app on an iPhone, every save silently fails and the data is gone on close. This is the single most likely way to lose a season of results. The app therefore:

- probes the store at startup by writing and reading back a test key
- falls back `window.storage` → `localStorage` → memory
- when it lands on memory, shows a permanent red bar in Greek saying data will not be saved and what to do about it, plus a red chip in the header

Verified: hosted over https → `local`; opened from a file on iPhone → `memory` with the warning; Claude artifact sandbox → `app`; no storage API → `memory`.

**The fix is a web address, not a workaround.** Ship the app as four files — `index.html`, `manifest.webmanifest`, `sw.js`, `icon.jpg` — on any free static host (Cloudflare Pages, Netlify Drop, GitHub Pages). No server, no cost, no maintenance. Both phones and the laptop open the same URL and install it to the home screen. `DEPLOY.md` in the bundle has the steps.

**Platform details that must stay in:**

| Concern | Handling |
|---|---|
| iOS home-screen install | `apple-mobile-web-app-capable`, `apple-mobile-web-app-title`, `apple-touch-icon`, `theme-color` |
| Notch and home indicator | `viewport-fit=cover` plus `env(safe-area-inset-*)` on the header, the sticky nav and the fixed bottom action bar |
| iOS zooming form fields | inputs at 16px or larger, `-webkit-text-size-adjust:100%` |
| `sms:` URI | `sms:<number>?&body=<encoded>` — the one form both iOS and Android accept |
| Service worker | registered only when `location.protocol` starts with `http`, so opening the file directly fails silently instead of throwing |
| `DecompressionStream` (xlsx/docx import) | Safari 16.4+ and Chrome 80+. Below that, the import throws a clear Greek message telling the user to save as CSV |
| `navigator.share({files})` | iOS 15+ and Android Chrome. Falls back to download plus a pre-written email on laptops |
| Clipboard | `navigator.clipboard` needs a secure context; hosted over https it works, from a file it does not, so there is an `alert` fallback |
| Cache updates | bump `CACHE` in `sw.js` on every release or installed phones keep serving the old build |

---

## 2. Source of truth for the rules

Everything follows **ΚΑΝΟΝΙΣΜΟΙ Α.Κ.Ι. Κ.Ο.Α.Δ.** (pointersetterclubcy.com). The articles that drive logic:

| Article | Rule | Behaviour |
|---|---|---|
| Άρθρο 2 | Types: Πρακτικού Κυνηγίου, Έρευνας Κυνηγίου, Μεγάλης Έρευνας (pairs only), Κλασικοί. Plus Derby (Άρ. 43), Ε.Κ.Ι., Ε.ΦΥ.Π. | `trial.type`; ΜΕ forces brace format |
| Άρθρο 8 | Entry carries dog name and Κ.Ο.Κ. number, tattoo/chip, work-book number, owner, handler | Required entry fields |
| Άρθρο 9 | A bitch in season may be withdrawn or substituted on the day | `season` flag, shown for females only |
| Άρθρο 10 | The draw is made by the organisers, normally 3 days before, sometimes just before | Draw runnable and re-runnable any time before the start |
| Άρθρο 16 | **The draw is only an indication of order** | This sentence appears on every SMS, every shared list and every printed page |
| Άρθρο 24 | Each run lasts 15 minutes | Default run timer |
| Άρθρο 27 | One λευκή does not block CAC; two cap at ΠΟΛΥ ΚΑΛΟΣ; three in different directions eliminate | Shown to the judge as a hint, never as a block |
| Άρθρο 30 | Επανάκληση of a dog of great value | Adds a run at the end of that terrain, with its own notes |
| Άρθρο 32 | Μπαράζ between equal dogs from different terrains | Barrage module, phase 6 |
| Άρθρο 33 | The elimination-fault list | The exact list, no paraphrase, in the notes screen |
| Άρθρο 40 | The trial counts if at least 3 braces ran | Validation warning |
| Άρθρο 44 | Qualification ladder | `qualification` enum |
| Άρθρο 48 | Braces need ≥2 judges, solo ≥1, ΜΕ with CACIT needs 3 (one a ΜΕ judge) | Terrain validation |
| Άρθρο 49 | **A judge may not present his own dog in the terrain he judges** | Hard constraint in the draw |
| ΕΚ Άρ. 5 | ΕΚ needs ≥6 dogs and ≥3 braces | Validation warning |
| Άρ. 43 | Derby: separate Pointer and Setter terrains, dogs ≤24 months, Cypriot-bred | Derby mode, breed-group filter, age check |
| Αξιολόγηση | CACIT 14, RCACIT 13, CACT 12, RCACT 11, 1ος ΕΞ 10, 2ος ΕΞ 9, ΕΞ 8, Τ.Μ.Ε. 7, 1ος ΠΚ 6, ΠΚ 5, ΚΑΛΟΣ 4. Braces ×2. ΕΚ/ΠΚ on wild game: (2+1) solo, (2+2) brace | Points engine; the table is **data, not code** |

Italian and FCI practice adopted, confirmed by the client: in a brace the **first dog drawn stands to the right of the jury, the second to the left**. Store the position; handlers argue about it.

---

## 3. Roles

| Role | Can do |
|---|---|
| **Πρόεδρος Κριτών** | Everything: trials, entries, terrains, judges, the draw, SMS, all terrains, results, exports |
| **Κριτής** | Only his own terrain. Structured notes, proposed qualification, sign-off |
| **Γραμματεία** | Registry and imports. No draw, no scoring |
| **Handler** | No login. Receives an SMS |

With no server this is a view filter, not access control, and the interface says so plainly. Anyone holding the file holds all of it. That is acceptable because the file only ever goes to the head judge and the judges of that trial.

---

## 4. Data model

```
people        id, full_name, phone_e164, email, member_no
judges        id, person_id, licence ENUM(ΕΠΙΣΗΜΟΣ,ΔΟΚΙΜΟΣ), me_qualified, cacit_qualified
dogs          id, name, kok_reg_no, chip_or_tattoo, work_book_no,
              breed ENUM(POINTER,ENGLISH_SETTER,IRISH_SETTER,GORDON_SETTER),
              sex ENUM(M,F), dob, owner_person_id, kennel, cypriot_bred
trials        id, title, type, format ENUM(SOLO,BRACE), game, game_is_wild,
              award ENUM(NONE,CACT,CACIT), place, head_judge_id, date_start, status
trial_days    id, trial_id, day_no, date
terrains      id, trial_day_id, name, breed_group NULL, assigned BOOL
              -- a "terrain" is the Italian batteria: braces judged by one jury on one ground
terrain_judges terrain_id, judge_id
entries       id, trial_id, dog_id, handler_person_id, fee_paid, in_season,
              status ENUM(ΔΗΛΩΜΕΝΟΣ, ΑΠΟΣΥΡΘΗΚΕ, ΑΠΩΝ, ΣΥΜΠΛΗΡΩΜΑΤΙΚΟΣ)
braces        id, terrain_id, order_no, entry_a_id, entry_b_id NULL, is_solo,
              is_trailer, is_recall, status, started_at, ended_at
              -- entry_a = drawn first = right of the jury; entry_b = left
draws         id, trial_day_id, seed, algo_version, constraints_json, performed_by,
              performed_at, result_hash, is_current, supersedes_draw_id
run_notes     id, brace_id, entry_id, judge_id, <fields in §7>, free_text, updated_at, device_id
results       id, entry_id, terrain_id, qualification, award, placing,
              points_awarded, signoff_by, signoff_at, locked
sms_log       id, trial_id, entry_id, phone, body, segments, status, sent_at
points_table  score_key, base_points          -- editable by the club
settings      sms_header, sms_footer, sms_mode ENUM(FULL,OWN), sms_show_judges,
              avoid_owner, avoid_kennel, season_last
audit_log     id, actor_id, action, entity, entity_id, before_json, after_json, at
```

Two things that look like details and are not:

- **Every brace needs its own id.** Notes are keyed on `entry_id + brace_id`, because a dog recalled under Άρθρο 30 runs twice and each run gets its own note sheet. Keying notes on the entry alone silently overwrites the first run.
- **`points_table` is data.** The club changes its scoring by editing a table, never by a redeploy.

`ΣΥΜΠΛΗΡΩΜΑΤΙΚΟΣ` is a trailer dog added to fill an odd brace. He is excluded from the draw and does not count toward the three-brace minimum.

---

## 5. Draw engine

This is the part that must be right. Everything else is data entry.

### Constraints

**Hard — never violated unless arithmetically impossible:**
- H1. Two dogs of the same handler are never braced together.
- H2. A dog owned or handled by a judge never lands in that judge's terrain (Άρθρο 49).
- H3. Derby: a dog only goes to a terrain matching its breed group.
- H4. A dog runs once per day, recalls excepted and marked as such.

**Soft — toggleable, violated only when unavoidable, and reported:**
- S1. Avoid the same owner in a brace.
- S2. Avoid the same kennel in a brace.
- S3. Bitches in season run in the last brace of their terrain.

### Algorithm

```
1  seed  = the head judge's own string, or a random 128-bit value
2  rng   = seeded PRNG (mulberry32 over an FNV hash of the seed) — deterministic
3  clear any terrain allocation left by a previous draw; only an explicit manual
     assignment survives, otherwise the draw stops being reproducible from its seed
4  allocate entries to terrains: for each dog pick, among the terrains satisfying
     H2 and H3, the one where THAT HANDLER has fewest dogs, then the emptiest.
     Balancing by handler is what makes step 6 solvable.
5  per terrain: shuffle with rng; if S3, hold the in-season bitches back
6  pair greedily: for each dog choose at random among partners satisfying hard and
     soft; if none, among those satisfying hard only; if none, take any
7  repair pass (2-opt): swap partners between braces to clear any remaining
     violation — hard first, then soft. In-season dogs are locked in place so the
     repair cannot drag them out of the last brace.
8  odd count -> the last turn is solo; the head judge may add a trailer afterwards
9  number braces 1..N; entry_a = drawn first = RIGHT of jury, entry_b = LEFT
10 persist {seed, algo_version, constraints, result_hash = hash(ordered braces)}
11 the previous draw becomes is_current = false; the new one records supersedes_draw_id
```

Steps 4 and 7 are not refinements. Without balanced allocation and the repair pass, greedy pairing corners itself and leaves same-handler braces that a valid arrangement would have avoided — measured at 211 bad braces in 500 draws before, 0 after.

**Reproducibility is the whole point.** The same seed with the same entries and constraints must produce a byte-identical brace list and a matching hash. Provide a verify endpoint that re-runs and compares. When a handler challenges the draw, the head judge shows the seed and re-runs it in front of him.

Manual swaps after a draw are allowed, written to `audit_log`, and printed as «Χειροκίνητη αλλαγή». Never let a drawn list be edited silently.

### Multi-day
Day 1 is drawn. Later days offer **Νέα κλήρωση** or **Περιστροφή** — dogs rotate to the next terrain and the order shifts, so pairings do not repeat. Περιστροφή is the default and follows Italian practice.

---

## 6. SMS

**The head judge sends from his own handset, on his own number and his own credit.** No gateway, no server-side sending.

Each handler gets one message: all his own runs first, then the **full running order of the day** with his own braces marked `>>` and `<-- ΕΣΕΙΣ`. Plain-text markers, because SMS has no formatting.

```
Κ.Ο.Α.Δ. – {ΑΓΩΝΑΣ}, {ΗΜΕΡΟΜΗΝΙΑ}

Οι διαδρομές σας:
• ΑΡΗΣ — Τερέν Α, ζεύγος 1ο
• ΡΕΞ — Τερέν Β, ζεύγος 2ο

ΣΕΙΡΑ ΤΗΣ ΗΜΕΡΑΣ
▸ Τερέν Α (Α. Κριτής)
>> 1. ΑΡΗΣ / ΝΤΙΝΑ  <-- ΕΣΕΙΣ
2. ΛΟΥΝΑ / ΜΠΙΛΥ
...

Η σειρά είναι ενδεικτική (Άρθρο 16). Να είστε στη διάθεση των κριτών.
```

Sending opens the phone's own composer via `sms:<number>?&body=<encoded>`, which works on iOS and Android. The queue marks each row as sent. Per-row fallbacks: copy to clipboard, WhatsApp deep link.

**Cost must be visible.** Greek goes out as UCS-2: 70 characters in the first segment, 67 in each one after. Measured on a realistic trial of 40 dogs, 14 handlers, 3 terrains:

| Mode | Total segments |
|---|---|
| Full order | 166 |
| Full order without judge names | 163 |
| Own braces only | 49 |

So the mode is a switch, not a decision: **Πλήρης σειρά ημέρας** / **Μόνο τα δικά του ζεύγη**, plus a judge-names toggle. Show the estimated total before sending, and a per-message segment count that turns amber above six. The head judge should never discover the cost on his bill.

Build `SmsProvider` as a swappable interface from day one, so a gateway (Twilio, Vonage, Cyta bulk) drops in later as configuration rather than a rewrite.

---

## 7. Structured judge notes

One record per **judge × dog × run**. Everything optional except the proposed qualification.

**Έρευνα** — πάθος 1–5, μεθοδικότητα 1–5, καλπασμός και στυλ φυλής 1–5, επαφή με κυναγωγό 1–5, πλάτος έρευνας (Στενή / Κανονική / Ανοικτή / Πολύ ανοικτή).

**Πόντοι** — repeatable rows: θήραμα, ποιότητα (Ανέβασμα στην αναθυμίαση / Πόντος έκπληξης / Εξαίρετη ένδειξη), φέρμα, ποντάρισμα, ακινησία στο πέταγμα, ακινησία στον πυροβολισμό, απόρτ, συναίνεση. A judge must be able to log a point in three taps.

**Λευκές φέρμες** — a counter, with the Άρθρο 27 cap shown as advice.

**Σφάλματα αποκλεισμού** — the exact Άρθρο 33 list, behind a red-bordered section that needs a second confirmation. Eliminating a dog is serious.

**Ελεύθερο σχόλιο** — free text, dictation-friendly.

Editable until sign-off, then locked. The head judge can unlock with a reason, audited.

---

## 8. Import

`.xlsx` and `.docx` are ZIP containers, and the browser inflates them natively with `DecompressionStream("deflate-raw")`. Parse them yourself. Do not add a library — the app stays a single offline file.

- **xlsx**: read `xl/workbook.xml` and its rels for the real sheet names and order, then `sharedStrings.xml`, then the sheet XML. Handle `t="s"`, `t="inlineStr"` and bare numbers. **Decode numeric character references** (`&#922;`) — Excel writes Greek that way, and skipping this produces mojibake.
- **docx**: take the largest `<w:tbl>`; fall back to tab-separated paragraphs.
- **csv**: `;`, `,` or tab, BOM-tolerant.

Then auto-detect the header row (the first row where at least two columns look like known fields — club files open with a title and a blank line), auto-map the columns by keyword, and **show the mapping screen anyway** so the head judge can correct it. Never import blind.

Normalise on the way in: breed spellings (`Pointer`, `english setter`, `gordon`, `Πόιντερ`), sex (`Αρσενικό`, `Θηλυκό`, `M`, `F`), dates (`2022-03-11`, `15/09/2023`, and raw Excel serial numbers). Match existing dogs on Κ.Ο.Κ. number, then name, and **update rather than duplicate**. Create owners and their phone numbers as people automatically. Report what was skipped and what was defaulted — a dog with no breed is filed as Pointer and the count is shown, never guessed silently.

---

## 9. Exports

Every export carries the club badge, trial title, date, terrain, judges and the Άρθρο 16 disclaimer.

**Excel — the formulas must be live.** Sheets: `Ζευγη` (the draw list), `Δεδομενα` (flat results with a key column `=IF(award<>"-",award,qualification)` and points `=IFERROR(VLOOKUP(key,Παραμετροι!...,2,FALSE)*coefficient,0)`), `Παραμετροι` (the editable points table), and `Στατιστικα` (dogs as rows, trials as columns, cells built with `SUMIFS` over `Δεδομενα`, totals both ways). No constant is ever hardcoded inside a formula — anyone who opens the workbook can audit the arithmetic.

The build emits SpreadsheetML 2003, which needs no library and works offline. Excel opens it with a format notice; LibreOffice opens it clean. Both keep the formulas live, which is the point.

**Word** — the results announcement for the Κ.Ο.Κ. submission due within 15 days (Άρθρο 12γ).
**Print and PDF** — the draw list per terrain, blank judge note sheets, and a results sheet with signature lines. It will be photocopied, so design for black and white.

---

## 10. Transfer and offline

Terrains are on mountains with unreliable signal. Offline is not a feature, it is the operating condition.

- PWA: manifest plus service worker, installable on iOS via Safari and on Android via Chrome. **The draw runs entirely client-side** and works with no signal at all.
- Local store: `window.storage` → `localStorage` → memory, probed at startup (see §1a).
- Persistent chrome, not a toast: «Εκτός σύνδεσης – 6 αλλαγές σε αναμονή».

**Device-to-device transfer.** There is no server, so this is the only sync there is. Export JSON and send it with `navigator.share({files})`, which is what puts WhatsApp, Viber, Messenger and Mail in the list. On a laptop that sheet usually does not exist, so download the file and open a pre-written email instead. Receiving accepts `.json` and `.txt`, because messaging apps rename attachments.

Loading offers **merge** or **replace**. Merge resolves per record by id, the file wins, and anything the file does not mention is left alone — that is what makes laptop → phone → laptop round trips safe. Say plainly in the interface that editing the same trial on both devices between transfers means the later file overwrites the earlier one.

There is also a single-trial packet: one trial plus only the dogs, handlers and judges it references. A 40-dog trial stays well under 50 KB, which every messaging app handles.

SMS cannot carry the database. Say so in the interface rather than letting someone try.

---

## 11. Stack and hosting

No framework, no build step, no dependencies, no backend. One HTML file plus three small static files. That is not a limitation to work around — it is what makes the thing survive on a hillside and travel by WhatsApp.

Everything is vanilla: the draw engine, the xlsx and docx readers (native `DecompressionStream`, no library), the SpreadsheetML export, the storage layer. If you find yourself reaching for a package, stop and check whether the platform already does it.

**Hosting** is any free static host — Cloudflare Pages, Netlify, GitHub Pages. Upload four files. There is nothing to run and nothing to patch. Do not introduce a server; if the club ever needs several judges writing to one trial live, that is a separate conversation and a separate product.

**Releasing:** replace `index.html`, bump `CACHE` in `sw.js`, upload. Stored data survives updates because it lives in the browser's store, not in the app file.

## 12. Acceptance tests

The current build passes all of these. Yours must too.

| # | Test | Expected |
|---|---|---|
| 1 | 23 dogs, 3 terrains, brace format | 23 placed, 4/4/4 braces, exactly one solo, no dog twice |
| 2 | Two dogs of one handler, 500 seeded draws | never braced together where a valid arrangement exists; every genuine impossibility warned by terrain and brace |
| 3 | A judge owns an entered dog, 200 draws | no placements in his terrain |
| 4 | The same seed twice | identical brace list and matching hash |
| 5 | Bitch in season, 200 draws | last brace of her terrain every time |
| 6 | Points | ΕΚ, braces, wild game gives ×4; ΕΞΑΙΡΕΤΟΣ 32; CACT 48; solo non-wild ΠΟΛΥ ΚΑΛΟΣ 5 |
| 7 | Derby with Pointer and Setter terrains | no cross-breed placements; a 25-month dog rejected with the reason shown |
| 8 | The only terrain is judged by an owner's judge | a clear error, not a bad draw |
| 9 | Four dogs, all one handler | pairs anyway and warns; the impossibility is reported, not hidden |
| 10 | Every brace | a unique, non-empty id |
| 11 | Excel import with a title row, a blank row, Greek headers, mixed dates and serials, mixed breed and sex spellings, and a dog with no registration number | header found automatically, all columns mapped, dates and breeds normalised, blank row reported |
| 12 | Re-import the same file | no duplicates, existing records updated |
| 13 | A Word table imported into a trial | dogs and entries created with handlers attached |
| 14 | laptop → phone (merge) → result and trailer added → back to a laptop that gained a dog meanwhile | both new dogs present, result preserved, no duplicates |
| 15 | Airplane mode: create a trial, import, draw, write notes, sign off | everything persists; syncs on reconnect with no duplicates |
| 16 | The Excel export opened in Excel and LibreOffice | points cells contain formulas; editing `Παραμετροι` recalculates `Στατιστικα` |
| 17 | 40 handlers, one with 3 dogs | 38 messages; the multi-dog handler gets one listing all three; the segment estimate is shown before sending |
| 18 | Opened from a file on an iPhone | the red no-storage bar appears; nothing is saved silently |
| 19 | Installed from a URL on iPhone and on Android, then airplane mode | opens, draws, records notes, all offline |
| 20 | Bottom action bar on a notched iPhone | clears the home indicator; nav clears the notch |
| 21 | Tapping any input on iOS | no page zoom |

---

## 13. Build order

1. **Registry and import** — dogs, people, judges; Excel, Word and CSV with mapping. Nothing works without the data.
2. **Trial, terrains, draw** — the constraint engine, the brace list, Excel and PDF export. This alone replaces the paper process.
3. **SMS** — the queue, the full-order message, segment costs, share fallbacks.
4. **Notes and results** — the structured card, sign-off, qualifications, Word export.
5. **History and standings** — dog pages, the dogs × trials matrix, title progress under Άρθρο 51.
6. **Multi-day rotation, μπαράζ, morphology shows.**

Ship steps 1 to 3 before a real trial and let the head judge run one live. That will teach you more than the rest of this document.
