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
| 1g Μητρώο | `vRegistry()` |
| 1h Εισαγωγή, the mapping step | `renderImport()` |
| 1i Στατιστικά | `vStats()` |
| 1j Ιστορικό σκύλου | `vDog()` |
| 1k print | `drawSheet()` (draw list) and `noteSheet()` (blank judge sheet) |

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

## Two fixes to the existing build

- `__BADGE__` in the `<link rel="icon">` tags was never substituted; both now point at `./icon.jpg`.
- `render()` set the header chip to the storage state and then immediately overwrote it with the
  connection state, so «Χωρίς αποθήκευση» could never appear. The storage state now wins, which is
  what the brief asks for.

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

## Worth a second opinion

`--slate` (#6B6A64) on `--stone` (#EFEAE0) is about 4.3:1. It is the canvas's own pairing and all
primary text is far above 7:1, but secondary text on the field screens — breed, handler, the meta
line under a dog's name — sits at that ratio and the brief asks for 7:1 on anything that matters.
Darkening `--slate` to roughly #55544F would clear it without touching the palette's character.
