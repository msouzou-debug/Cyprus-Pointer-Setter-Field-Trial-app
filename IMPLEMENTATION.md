# Design handoff — what was built

The design canvas (`project/KOAD Trial Manager UI.dc.html`) is a visual system for the working
app that came with the bundle. This implementation applies it to that app rather than replacing
it: the draw engine, the xlsx/docx/csv importers, the SpreadsheetML export, the storage probe and
the transfer layer are untouched. Only the presentation changed, plus the small amount of
behaviour the design implies and the app did not yet have.

## Ship these four files

`index.html`, `manifest.webmanifest`, `sw.js`, `icon.jpg` — see `DEPLOY.md`. `icon.jpg` is the
club badge from the build; the same image is embedded in the page for the header, the dog page
and the printed sheets.

## Artboard by artboard

| Artboard | Where it lives |
|---|---|
| 1a tokens | the `:root` block at the top of `index.html` |
| 1b brace card, seven states | `braceCard()` / `braceBrief()` |
| 1c Κλήρωση with the staged reveal | `tDraw()` + `revealBraces()` |
| 1d Τερέν live | `tBraces()`, countdown in `clockEl()` / `startClocks()` |
| 1e Σημειώσεις | `dlgNote()` + `ptRow()` |
| 1f SMS | `tSms()` |
| 1g Μητρώο | `vRegistry()` — now handler-first, see below |
| 1h Εισαγωγή, the mapping step | `renderImport()` |
| 1i Στατιστικά | `vStats()` |
| 1j Ιστορικό σκύλου | `vDog()` |
| 1k print | `drawSheet()` (draw list) and `noteSheet()` (blank judge sheet) |
| — | Εγκατάσταση: `vInstall()`, the QR encoder `QR`, and `qrPoster()` for the printed sheet |

The six screens the designer had not drawn yet — Αγώνες, Στήσιμο, Συμμετοχές, Τερέν & Κριτές,
Βαθμολόγηση, Μεταφορά — follow the same tokens and the same two registers.

## Behaviour the design implied and the app did not have

- **Run clock (Άρθρο 24).** Starting a brace stamps `startedAt`; the card counts down from 15:00
  and keeps counting past zero, because the judge ends the run, not the timer. Παύση holds it.
- **Επόμενο ζεύγος.** The bottom bar ends the running brace and starts the next pending one.
- **Χειροκίνητη αλλαγή.** The state exists in the design, so there is now something that produces
  it: Ανταλλαγή swaps a drawn dog with another drawn dog, marks both braces `manual` with who and
  when, and the mark prints on the draw list.
- **Autosave in the notes screen**, with a quiet «Αποθηκεύτηκε» and no modal.
- **Second confirmation on elimination** (Άρθρο 33) and on re-drawing an order that has been sent.
- **Dictation** uses the Web Speech API where it exists and otherwise points at the keyboard's own
  microphone, which is what works on iOS.

## Εγκατάσταση — QR code and install guide

A fifth destination in the navigation. It shows the address the app is served
from as a QR code, so the head judge holds up his phone and the next one scans
it, plus the install route for iPhone, Android and a laptop, and a printable A4
poster to pin up at the trial.

The code is generated in the page — byte mode, error correction level M,
versions 1 to 10, about 170 lines. Fetching it from a service would have been
shorter and would have failed on the one hillside where it matters, and a
library would have broken the no-dependencies rule the whole build rests on.
It is verified two ways in the test harness: every code is decoded back with an
independent decoder (jsqr) and compared to its payload, and the matrices are
compared module by module against a reference encoder (`qrcode`) — they are
identical, mask selection included. Neither library ships.

Opened from a web address the app knows its own. Opened from a file there is
nothing to share, so the club's address is typed once and kept in settings,
which also means it travels with a backup.

The same screen carries the GitHub repository: a direct ZIP of the four files
and a link to the source. A build with no server should not depend on whoever
set it up — the club can take the files and host them somewhere else. `REPO`
is a constant at the top of that section; change it if the repository moves.

## Three fixes to the existing build

- **The debounced write had no flush.** `save()` waits 250ms before serialising, so a burst of
  taps does not rewrite the database each time. Nothing flushed that pending write when the page
  went away, and iOS discards backgrounded tabs without warning — so the last thing a judge did
  before pocketing the phone could be lost. The write is now flushed synchronously on
  `visibilitychange` (hidden) and on `pagehide`. Found by reloading immediately after a save while
  testing the hosted build.
- `__BADGE__` in the `<link rel="icon">` tags was never substituted; both now point at `./icon.jpg`.
- `render()` set the header chip to the storage state and then immediately overwrote it with the
  connection state, so «Χωρίς αποθήκευση» could never appear. The storage state now wins, which is
  what the brief asks for.

## Second round — field feedback

Reported after the first trial run, plus the intuitiveness pass.

- **The Excel export now really is Excel.** It was SpreadsheetML 2003 written to a `.xls`, which
  Excel greets with "the file format and extension don't match", and every formula cell declared
  itself an empty number while the key column returned text. It is now a genuine `.xlsx` — a ZIP
  of OOXML parts, CRC32 and all, written here rather than with a library like everything else.
  Points still come from `Παράμετροι` by VLOOKUP and the standings still add up `Δεδομένα` with
  SUMIFS, so the arithmetic stays auditable. The harness opens every generated workbook with a
  real xlsx parser and checks the sheets, cells and formulas; it does not ship.
- **Dogs can be assigned to a terrain by hand.** The draw engine had always honoured
  `terrain.assigned` + `entryIds`; no screen ever set them, so the capability was unreachable.
  Anything left unassigned still falls to the draw. *This exposed a real bug:* a hand assignment
  used to bypass Άρθρο 49 entirely. It does not outrank the regulation — an assignment that would
  put a judge's own dog in his terrain is refused, the dog is allocated elsewhere, and the head
  judge is told which ones moved.
- **Braces can be reordered after the draw.** Numbering is positional, so brace 1 moved three
  places down becomes brace 4. Both braces are marked as a manual change and the mark prints on
  the draw list, per Άρθρο 16 — the order may be changed, never silently.
- **Run length is a trial setting** (default 15, Άρθρο 24) with **+5′** on the running brace for a
  judge who extends a run. The clock already counted past the limit rather than stopping; only the
  fifteen was hard-coded.
- **The Word export carries the judges' notes** — a section per run with each judge's scores,
  points, λευκές φέρμες, Άρθρο 33 faults and free text, both runs when a dog was recalled, and the
  unlock trail if any terrain was reopened.
- **A progress strip** on the trial screen: Συμμετοχές → Τερέν → Κλήρωση → SMS → Βαθμολογία, what
  is done and what is next. The app always had an order of operations and nothing conveyed it.
- **A pre-draw check** — judges per terrain (Άρθρο 48), Άρθρο 49 conflicts, the three-brace
  minimum (Άρθρο 40), manual assignments, an existing draw — said before the button, not in an
  alert after it.
- **Sign-off** locks a terrain's scores and notes; the sheet still opens, read-only. Unlocking
  needs a reason, which is kept and printed. Spec §7 asked for this and it had never been built.
- **The entry screen asks for the handler first, then the dog.** Handlers stay with the club for
  years; dogs compete for a few. Choosing the handler groups his dogs to the top of the list —
  the ones he owns *and* any he has run in a previous trial, since a handler often brings someone
  else's dog. If exactly one of his dogs is not yet entered, it is offered. Adding a person or a
  dog mid-flow comes back with what was already chosen, and the new dog's owner is prefilled with
  the handler so no name is typed twice. Entering the same dog twice is refused.
  **Συμμετοχές is grouped the same way** — a card per handler with his dogs under it, his phone
  number under his name, and a count. One man arrives with three dogs and the head judge deals
  with him once. The search filters the dogs and drops a handler whose dogs all fall out.
- **Smaller:** a search box on Συμμετοχές; a dog can be created without leaving the entries screen
  (an empty registry used to be a dead end with a toast pointing elsewhere); the trial's tabs are
  one scrolling row instead of wrapping to three, which gives the field screens back their
  vertical space.

## Third round — the word is κυναγωγός, and the register follows the man

The app called these men **πρόσωπα** and, on the dog form, **ιδιοκτήτες**. Neither is the club's
word. The brief is explicit — τερέν, ζεύγος, κυναγωγός, φέρμα, πόντος, λευκή φέρμα, ποντάρισμα,
συναίνεση, μπαράζ, κλήρωση, επανάκληση, βαθμολογία, οίστρος, never a synonym — and this one had
slipped through on the screens the designer had not drawn.

- **Πρόσωπα is now Κυναγωγοί** everywhere it shows: the Μητρώο tab and its counts, the dialog
  titles, the dog form's section, the judges table column, the judge-linking field, the import
  field labels, the transfer and backup wording. `DB.people` keeps its name — it is the storage
  key, and every backup and transfer packet already in the field carries it.
- **Μητρώο is handler-first and lands there.** A card per κυναγωγός: his phone and membership
  number under his name, his dogs under that, «+ Σκύλος» which opens the dog form with him
  already filled in, and «Επεξεργασία στοιχείων». It is deliberately the same object as a
  Συμμετοχές card, because it is the same job — the head judge thinks in men, and the dogs move
  around underneath them. The search filters dogs and drops a κυναγωγός whose dogs all fall out,
  but keeps one whose own name matches: in the register he may have no dogs yet. Dogs with no
  κυναγωγός collect in a final card rather than disappearing.
- **The flat Σκύλοι table stays** as the second tab, with the import card. It is the desk view
  for looking a dog up by Κ.Ο.Κ., which the cards are not.
- **An entry on an empty register now asks for the κυναγωγός**, not the dog — the same order the
  entry form itself asks in, and it comes back with him already chosen.
- **Smaller:** a κυναγωγός with one dog is no longer stretched to the height of one with four;
  the dog's name in a card opens its history, so the row carries one control instead of three;
  the sex reads «αρσενικός / θηλυκός» on both screens instead of «Α / Θ» on one of them.

### Greek

The strings were read against the club's vocabulary and modern usage rather than spot-checked.
Nothing polytonic, no Latin lookalikes inside Greek words, άνω τελεία used where it belongs.
Four real errors: the workbook sheet is «Παράμετροι» and the prose had lost the accent; the iOS
install steps said «Πρόσθεση», which is the arithmetic word — Safari's own Greek is «Προσθήκη
στην οθόνη Αφετηρίας»; the Άρθρο 16 line used an en dash where the rest of the app uses an em
dash; and one instruction had lost its verb. The import failure now says «Το αρχείο δεν
διαβάστηκε» rather than the nominalised «Δεν ήταν δυνατή η ανάγνωση».

Question marks stay as U+003B. That is what a Greek keyboard produces and what Unicode
recommends; U+037E normalises back to it under NFC, so switching would be a change that undoes
itself. No `?` appears in Greek prose anywhere.

## Deliberate departures from the canvas

- **Offline chip.** The canvas shows «Εκτός σύνδεσης – 6 αλλαγές σε αναμονή». There is no server
  and no queue, so nothing is ever pending; the bar says the changes are saved on the device and
  travel by Μεταφορά instead of claiming a queue that does not exist.
- **«Αντικατάσταση όλων» on the import screen** was left out. The importer updates rather than
  duplicates by design; a destructive replace-all belongs with the other destructive actions in
  Ρυθμίσεις, where it already is.
- **Point detail behind a disclosure.** The canvas shows a logged point as a summary. Θήραμα and
  ποιότητα are always open — that is the three-tap path — and the other six attributes sit behind
  «Λεπτομέρειες διαδρομής» so the card stays short on a phone.
- **Web fonts are optional.** Commissioner and Source Sans 3 are loaded through `media="print"`
  so the request never blocks the first paint. With no network the type falls back to a system
  stack with Greek coverage. This matters: a render-blocking stylesheet is a blank screen on a
  hillside with one bar of signal.

## Contrast

`--slate` was the canvas's #6B6A64, which is 4.5:1 on `--stone` — under the 7:1 the brief asks for
on anything that matters, and it carries the breed and handler lines that get read in sunlight. It
is now **#4C4B46**: 7.3:1 on stone, 8.7:1 on white, 7.8:1 on sand. Primary text on stone is 14.5:1.

`--slate-2` (#9B968C) and `--dim` (#8F8B82) are left as drawn. They are deliberately subordinate —
third-level labels on the desk screens, and the dimming that marks a finished brace — and dimming
is doing real work there as a state signal.
