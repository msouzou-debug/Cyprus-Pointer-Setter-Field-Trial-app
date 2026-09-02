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

## Fourth round — one navigation row, and the day set up in the order it happens

Reported from a phone at the trial.

- **The trial screen carried the same six words twice.** A progress strip
  (Συμμετοχές → Τερέν → Κλήρωση → SMS → Βαθμολογία) sat directly above a tab strip with the same
  labels. On a desk they read as two registers; on a phone they read as duplicate buttons, which
  is what they were. There is now one row. It is the progress strip, extended to carry Ζεύγη as
  the step it always was, and it is the navigation: each step shows its number or its tick, its
  count, and whether it is the one open. Εξαγωγές trails as a plain button — a destination, not
  a step, and it never completes.
- **Συμμετοχές are entered by the man, not the dog.** «+ Συμμετοχές» opens one screen: choose the
  κυναγωγός, see only his dogs, tick the ones running today. He brings three and enters two in one
  pass. Re-opening him shows what is already ticked, and un-ticking withdraws the entry. A dog
  already drawn or scored cannot be un-ticked there — that is a withdrawal and it belongs in the
  entry's own form, where the status is recorded. A dog entered under another κυναγωγός shows his
  name and stays locked. Each card on Συμμετοχές has «Αλλαγή σκύλων» straight back into it.
  The one-dog form stays for editing a single entry: status, πληρωμή, οίστρος.
- **Τερέν asks how many first.** 1 / 2 / 3 / 4, named Τερέν Α, Β, Γ, Δ. Adding is free; removing
  refuses to swallow a terrain that has braces drawn, and asks before dropping manual assignments.
- **Judges are chosen on the terrain card, by seat.** Three named dropdowns — **Κεντρικός
  κριτής**, **Κριτής 1**, **Κριτής 2** — because that is how the committee on a terrain is named.
  One man cannot hold two seats: putting him in one clears the other. Clearing the κεντρικός does
  not promote whoever sits below him into the chair, so `terrain.slots` remembers the seats as
  chosen while `judgeIds` stays the compacted panel Άρθρο 48 and Άρθρο 49 are checked against, and
  `headJudgeId` is seat 0. Both articles are still stated on the card, per terrain, as they were.
  The terrain dialog now covers only the name and the breed group; judges live on the card.
- **The two ways the club works are on the screen.** Once the field is in and every terrain has
  its judges, a panel offers both: **Κλήρωση τώρα** for the draw on the hillside in front of
  everyone, or **Αποστολή στο κινητό** to carry the setup over and draw there. Do it at home
  instead and the SMS step sends the order — still indicative, Άρθρο 16. The transfer and the SMS
  both existed; nothing pointed at them from where the decision is made.

## Fifth round — the laptop, the judges, and the record

Seven reports from the field.

- **A laptop cannot send an SMS.** An `sms:` link does nothing there, and the app was marking the
  message sent anyway. The SMS screen now says so, and on a laptop the primary button is WhatsApp
  Web with the text also copied to the clipboard. Nothing is marked sent unless something actually
  opened. On a phone it is unchanged: the messaging app, with the number and body filled in.
- **Getting the day onto the phone is said where the decision is made.** After the draw, the
  Κλήρωση screen carries three buttons — send the order by SMS, send the trial (with its braces) to
  the phone, print the list — and names the load route on the other device. Both directions the
  club works in are now reachable without hunting: draw on the laptop and SMS from it, or carry the
  setup over and draw on the hillside.
- **Judges have phone numbers and get their own message.** A judge stands in the field with this
  app open and scores from it, so his message names his terrain, his seat (κεντρικός κριτής /
  κριτής 1 / κριτής 2), who he sits with, and the braces he will judge — not the whole day's list.
  The queue is keyed `j:<id>` so a judge never collides with an entry in `t.sms`.
- **Ticks on the SMS screen.** Everyone starts ticked, because the usual job is "send it to the
  lot". «Επιλογή όλων», «Κανένας», «Μόνο κυναγωγοί», «Μόνο κριτές», then one button that opens the
  next one waiting and counts down. A phone sends one message at a time and there is no bulk API to
  hand it, so the app does not pretend otherwise. «Αντιγραφή επιλεγμένων» puts them all on the
  clipboard at once, and «Σήμανση ως εσταλμένα» marks without sending.
- **The register deletes.** A κυναγωγός and a judge can now be removed — neither form had a delete
  at all. History is protected rather than the button: a κυναγωγός with entries in a trial is
  refused and told which trial holds him; a judge with notes likewise. One with no history goes,
  his dogs stay in the register under «χωρίς κυναγωγό», and a deleted judge comes off every terrain
  he was seated on.
- **A trial can be finished.** «Ολοκλήρωση αγώνα» on Εξαγωγές moves it into the record: the Αγώνες
  list splits into Σε εξέλιξη and Ιστορικό by season, and Στατιστικά says how many are closed. The
  points always counted; nothing said a trial was over, so every season stayed open. Closing warns
  about unscored dogs and unsigned terrains, deletes nothing, and can be undone.
- **The printed judge sheet carries what was written.** It was a blank form and only ever a blank
  form, which is worthless in the club's file after the run. It is now both: the scales the judge
  gave are filled black, his points fill the table, λευκές φέρμες, the Άρθρο 33 fault and the free
  comment all print, and anything he did not record stays an empty line to write on. One sheet per
  judge who scored the run, so each opinion is filed separately; a run nobody scored still prints
  one blank sheet.

## Sixth round — the whole field at once, and judges from the sheet

- **«Δηλώσεις ημέρας» is one table for the whole register.** Every κυναγωγός with his dogs under
  him, a tick against each, and a tick on his name that takes all of them. The head judge works
  down the entry list in one pass and saves once, instead of opening a dialog per man. The count,
  the number of κυναγωγοί and the braces update as he ticks, with the 6-dog / 3-brace minimum
  (ΕΚ Άρθρο 5, Άρθρο 40) stated on the same line. Search filters in place and keeps the ticks. A
  dog already drawn or scored is locked — the group tick cannot drop him either, because that is a
  withdrawal and belongs in the entry's own form. Dogs with no κυναγωγός are in the table too, so
  nothing is invisible. «+ Ένας κυναγωγός» keeps the per-man screen for whoever turns up late.
- **The importer takes judges.** `Κριτής` and `Τηλέφωνο κριτή` are mappable columns. A row carrying
  a judge is read whether or not it also names a dog, so the same importer swallows a dog list, a
  judge roster, or a sheet holding both; judges are matched by name, and an existing one only gains
  a phone he did not have. Judge-only rows are no longer counted as skipped.
- ***This found a real bug in header guessing.*** `guessField` returned the first field whose
  keyword appeared in the header, and the name keywords are substrings of the phone headers —
  «Τηλέφωνο ιδιοκτήτη» contains «ιδιοκτ», so it was read as the owner's **name**, silently, on
  every import that had such a column. The longest matching keyword now wins. Twelve real headers
  are checked in the harness.

## Seventh round

- **Terrain letters** are now the first letter not already in use, rather than one counted off the
  current list length. *I could not reproduce the reported repeat* — a fresh count of 1, 2, 3, 4
  gives Τερέν Α, Β, Γ, Δ (U+0391…U+0394), one at a time or all at once, and the harness checks the
  code points. Position-based naming does repeat itself once a terrain is renamed, so that path is
  closed either way.
- **A judge stands on one terrain.** Anyone seated elsewhere that day is no longer offered in the
  other terrains' dropdowns, and writing him in anyway is refused with the terrain that holds him.
  The man in the seat you are looking at stays visible, or the select would show nothing.
- **«Σπόρος κλήρωσης» is «Κωδικός κλήρωσης»**, prefilled with the type's initials, the trial and the
  date — `ΠΚ-ΚΑΤΩΜΟΝΗ-14022026` — and fully editable. Greek capitals carry no accents, so the name
  is stripped before uppercasing. Reopening a drawn day shows the code that was actually used, and
  the fingerprint line under the result says «κωδικός» too.
- **The trial name is a button.** It always edited from Επεξεργασία and still does — again, *not
  reproducible* — but the heading is now the control, which is where anyone would look for it.
- **One «Αποστολή σε όλους»**, sending a common message: the day's order with nobody's own braces
  marked, because a group message has no "you". «Έναν-έναν» keeps the personalised route.
- **Channels: SMS, WhatsApp, Viber — and Messenger cannot work.** Checked rather than assumed.
  Viber's `viber://forward?text=` opens with the message ready and lets the sender pick everyone,
  which is a real send-to-all. SMS can take several recipients on Android; iPhone usually takes only
  the first, and the screen says so. WhatsApp takes one number at a time, so it refuses the group
  send and puts the text on the clipboard instead of claiming to have sent it. **Messenger has no
  button**: `m.me` needs a Facebook user or page id and a phone number cannot address a Messenger
  thread. A dead button would be worse than its absence.
- **A συμπληρωματικός is not judged** (Άρθρο 40). No Σημειώσεις button on his half of the card, no
  row in Βαθμολογία, no printed sheet, no επανάκληση, and opening his notes directly is refused
  with the article. He runs so the brace is complete; he takes no place.
- **Picking his dog picks his κυναγωγός** — whoever ran him last, otherwise his registered man.
- **A dog in no register and no entry can fill a brace.** Type his name, and his handler's if that
  man is new. He is kept as a guest so the brace has something to name and the club can see what
  ran, marked ΕΠΙΣΚΕΠΤΗΣ in the register, and offered to nobody as an entry.

**Not built: item 3.** «there is a selection choice for digs under» — I could not tell what this
asks for and would rather ask than guess at it.

## Eighth round

- **A dog runs on one terrain.** Assigning used to let Τερέν Β take a dog who was already on
  Τερέν Α and quietly pull him off it. Now he is shown but locked, with the terrain that holds him
  named on the row, and the screen says to free him there first. Nothing is moved behind the head
  judge's back.
- **Day two reverses the terrains.** The dogs who ran Τερέν Α go to Τερέν Β and the other way
  round, so nobody meets the same committee on the same ground twice. The engine always did this —
  draw mode `ΠΕΡΙΣΤΡΟΦΗ` rotates each terrain's dogs one place on — but it sat in a dropdown that
  only appeared on day two and nobody opened. There is now a card that names the swap in full
  (Τερέν Α → Τερέν Β · Τερέν Β → Τερέν Α) and one button that does it and re-draws. With two
  terrains a rotation *is* a reversal, so that is what the button is called; with three or more it
  says περιστροφή. An existing day-two draw is not thrown away without asking.
- **Braces drag.** A κυναγωγός is late, so his brace goes down the order: drag the row and drop it
  where you want. Built on pointer events, so a thumb and a mouse take the same path, the rows
  slide out of the way as you go, and a tap is still a tap — a drag only starts after a few pixels,
  so the arrows inside the row keep working. The ↑ ↓ buttons stay for a cold morning with gloves
  on. Numbering is positional either way, so brace 1 dropped three places down becomes brace 4, the
  move is stamped as a χειροκίνητη αλλαγή and printed on the draw list (Άρθρο 16).

## Ninth round

- **Wild game is the default.** The club's trials are run on wild birds; a released bird is the
  exception. A new trial now opens with «Άγριο θήραμα · Ναι», which also means the coefficient is
  right (ζεύγη ×2 · άγριο ×2 = ×4) without anyone remembering to set it. A saved trial keeps
  whatever it was saved with.
- **The import was there and nobody could find it.** «Φόρτωση αρχείου» lived in Ρυθμίσεις and on a
  trial's Εξαγωγές — never on the screen a second device actually opens on. It is now on **Αγώνες**,
  in the header and in the empty state, because the first move on a phone that was just sent a
  trial is not "make a new one".
- ***And the picker was filtering itself shut.*** The file input carried
  `accept=".json,application/json"`. A `.json` that arrives through WhatsApp or Viber often reaches
  the phone with no type iOS recognises, and an accept filter greys those files out — so the button
  opened a picker in which the very file you wanted could not be chosen. The filter is gone;
  anything can be picked and the content is validated on read, with a message naming the file it
  expects.
- **Three ways in.** The picker; **dropping the file on the window** on a laptop, with the page
  saying so as you drag; and **«Επικόλληση»** for the phone that will not hand a file over at all —
  open it in the messaging app, copy the text, paste it. All three go through one loader, so the
  merge-or-replace question and the content count are identical.
- **Εγκατάσταση now says how**, per device: on iPhone save the file to Αρχεία from the share sheet
  first; on Android it is in Λήψεις; on a laptop drag it onto the page. And which answer to give the
  merge question — in the field it is almost always συγχώνευση.

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
