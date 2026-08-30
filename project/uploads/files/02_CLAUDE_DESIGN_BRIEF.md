# Κ.Ο.Α.Δ. Trial Manager — Design Brief for Claude Design

## 0. Skills you must use

| Skill | Use it for |
|---|---|
| **`/frontend-design`** | The whole visual direction. Read it before you draw anything. Work in two passes as it describes: a compact token plan first, a self-critique against the brief second, then build. Take one real aesthetic risk and justify it. |
| **`/hellenic-linguist`** | Every word in the interface is Greek. Correct monotonic accents, correct grammar in labels, buttons, errors and empty states. A misplaced τόνος in a button is a visible defect. |
| **`/greek-how-to-write`** | Register. This is a hunting club regulation made into software, not a consumer app. Plain, technical, unexcited Greek. |
| **`/write-like-a-human`** | Every string. No marketing tone, no exclamation marks, no encouragement. Errors say what happened and what to do. Empty states are instructions. |

The client rejects anything that reads as translated or templated. Run the Greek skills over the finished string list before you hand over.

---

## 1. The situation you are designing for

It is 06:40 on a hillside outside Kato Moni. The head judge is standing in a field with forty handlers and their dogs around him, wind, low sun, one bar of signal. He has a phone in one hand and a lead in the other. He needs to split the entries into terrains, run the draw, and get the order out to everyone in under ten minutes, without a laptop and without a printer.

That is the design problem. Not a dashboard. A field instrument.

Later that day two judges walk the ground with the dogs and record what each dog did. They tap notes between actions, in sunlight, one-handed, without looking at the screen for long.

Everything else — the registry, imports, history, standings, exports — happens the night before or the week after, at a kitchen table, and can be dense.

**Two registers in one app.** *Field mode* is large, high-contrast, thumb-driven, almost brutally simple. *Desk mode* is a proper data application. Same tokens, different densities. Do not compromise field mode to make desk mode prettier.

A working build exists: `KOAD_Trial_Manager.html`. Open it, use it, then improve it. It is the functional target, not the visual ceiling.

**It must look and behave identically on a laptop, an iPhone and an Android phone.** There is no server and no native app — it is one page, installed to the home screen from a web address. Design accordingly:

- **iOS safe areas.** The header sits under the notch and the bottom action bar sits above the home indicator. Both use `env(safe-area-inset-*)`. Check your layouts on a notched iPhone in landscape too, because judges hold the phone sideways to read a wide brace list.
- **No iOS zoom on focus.** Every input is at least 16px. This is a design constraint, not an implementation detail.
- **Installed, there is no browser chrome.** No back button, no address bar. Your in-app navigation is the only navigation, and every screen needs a way back.
- **The storage warning bar.** When the app cannot save — someone opened the file directly on an iPhone instead of the installed version — a red bar sits under the navigation and stays there. Design it to be impossible to ignore and impossible to dismiss. Losing a day of results is worse than an ugly bar.
- **Touch targets and text sizes are set by field mode, not by the laptop.** Design mobile first and let the laptop inherit; the reverse produces a phone screen nobody can use with cold hands.

---

## 2. Brand

- **ΚΥΠΡΙΑΚΟΣ ΟΜΙΛΟΣ ΑΓΓΛΙΚΩΝ ΔΕΙΚΤΩΝ (Κ.Ο.Α.Δ.)** — Cyprus Pointer & Setter Club, founded 1992.
- The badge is supplied: a circular navy emblem, two dog heads in white line, Greek text around the top ring and English around the bottom, `1992` at the centre foot. It is already embedded in the build and it is the only supplied artwork. The horizontal wordmark exists but only as a photograph of a screen, so **set the wordmark in type rather than using that image**.
- The club's subject is English Pointers and English, Irish and Gordon Setters, working Cyprus hill country on partridge, francolin and woodcock.
- The club writes plainly and technically about its own sport. Match that.

## 3. Palette

Pull from the badge and from the ground these dogs work: navy and silver from the emblem, dry limestone hillside, stubble, the red-brown of an Irish Setter's coat.

| Token | Value | Use |
|---|---|---|
| `--navy` | `#1E2B4D` | Header, brand surfaces — taken from the badge |
| `--navy-d` | `#141E36` | Navigation |
| `--stone` | `#EFEAE0` | Page background; limestone, and it reads in sunlight |
| `--ink` | `#171A21` | Primary text |
| `--slate` | `#6B6A64` | Secondary text, dividers |
| `--setter` | `#8C3A1E` | The single accent |
| `--stubble` | `#C8A24A` | Warnings, in-season flags, pending SMS |

One accent only. `--setter` marks what is happening **now** — the running brace, the primary action — and nothing else. If everything is highlighted, nothing is. You may revise these once you have the badge open in front of you; if you do, say what you changed and why.

## 4. Typography

Greek coverage is mandatory. Many display faces have none, so check before choosing.

- **Display**: a Greek-capable grotesque with real character — *Commissioner* and *Manrope* both carry full Greek. Set large and tight for terrain names and brace numbers.
- **Body**: *Noto Sans* or *Source Sans 3*. Reliable Greek, boring in the right way.
- **Numerals**: tabular figures wherever numbers align — brace numbers, points, segment counts, the standings matrix. Not negotiable.

Field mode starts large: brace number 48–64px, dog name 24px, everything else 17px minimum. Nothing below 15px in field mode, ever.

If the app must work fully offline with no font files, fall back to a system stack with Greek coverage and make the type work through scale, weight and spacing instead.

## 5. The signature element

**The brace card.** It is the one thing this app exists to produce and it should be unmistakable.

Two dogs side by side, split down the middle, the brace number very large across the top. The left half is the dog drawn first — right of the jury — and the card says so in small caps, because handlers argue about this. A hairline rule down the centre, the way a brace is two dogs on one ground.

States to design, all of them:

| State | Treatment |
|---|---|
| Εκκρεμεί | Outlined, quiet |
| Τρέχει | Filled `--setter`, unmistakable from arm's length |
| Ολοκληρώθηκε | Dimmed, with the qualification chip |
| Μονός | One half struck through, the word ΜΟΝΟΣ, and a **+ Trailer** action |
| Με trailer | The added dog labelled TRAILER on his side, chip on the header |
| Επανάκληση | A `--stubble` chip reading ΕΠΑΝΑΚΛΗΣΗ; this is a second run of the same dog under Άρθρο 30 and must never be mistaken for a duplicate |
| Χειροκίνητη αλλαγή | Marked, including in print |

Scrolling a terrain, you should know where you are without reading.

## 6. Screens

**Αγώνες** — desk. Cards by season, status chip (Πρόχειρος / Δηλώσεις / Κληρωμένος / Σε εξέλιξη / Κλειστός).

**Στήσιμο αγώνα** — type, format, game, award, dates, days, place. Validation as inline hints in the club's own words: «Η Μεγάλη Έρευνα γίνεται πάντα σε ζεύγη», «Για CACIT χρειάζονται 3 κριτές ανά τερέν».

**Μητρώο** — dogs, people, judges. The dog form carries its owner: pick from the registry or type a new name and mobile in the same screen. Never make someone leave to create an owner.

**Εισαγωγή** — the file picker, then the mapping screen: each column of their file on the left with a sample value, the field it maps to on the right, a header-row selector and a preview. This screen decides whether the import is trusted. Make it legible and calm; it is the only chance to catch a wrong column.

**Συμμετοχές** — table with search, flags for πληρωμένο and οίστρος (shown for bitches only), running count against the minimums.

**Τερέν & Κριτές** — one column per terrain with its judges on top. Conflicts surface immediately and specifically: «Ο κριτής Χ έχει σκύλο σε αυτό το τερέν (Άρθρο 49)» with a one-tap fix.

**Κλήρωση** — the moment this app exists for. One screen, one large button. On tap, a short deliberate reveal, braces appearing one at a time about 150ms apart, in order. Not decoration: it mirrors a public draw where names are read out one by one, and it gives the crowd something to watch. Respect `prefers-reduced-motion` with an instant reveal. Below the button, small and permanent: the seed, the timestamp, the fingerprint, and «Η σειρά είναι ενδεικτική – Άρθρο 16». Re-draw exists but is styled as a secondary, slightly uncomfortable action.

**Τερέν (live)** — field mode. Brace cards stacked, the live one expanded with a 15-minute countdown, the rest collapsed to a number and two names. The next-brace action is a full-width bar fixed to the bottom, reachable with a thumb.

**Σημειώσεις σκύλου** — field mode, and the hardest screen. Chips and steppers, not dropdowns and not free text as the primary path. Three taps to log a point. The Άρθρο 33 elimination faults live behind a red-bordered section needing a second confirm. Free text at the bottom with the dictation button prominent. Autosave with a quiet «Αποθηκεύτηκε», never a modal.

**Βαθμολόγηση** — the judge picks the qualification. The app's computed hints are advice and clearly subordinate: «2 λευκές φέρμες → μέγιστο ΠΟΛΥ ΚΑΛΟΣ (Άρθρο 27)». The judge always overrides. Sign-off locks the record and the lock looks like a lock.

**SMS** — one row per handler with the message preview, a large Αποστολή that opens the phone's own composer, and rows ticking green. Two things must be visible before he starts: the total segment estimate and each message's own segment count, amber above six. He is paying for these. The mode switch (Πλήρης σειρά ημέρας / Μόνο τα δικά του ζεύγη) sits at the top of this screen, not buried in settings.

**Αποτελέσματα & Εξαγωγές** — desk. Results table, then Excel, Word, CSV, print, and the sharing buttons for sending the order to a WhatsApp or Viber group.

**Στατιστικά** — dogs as rows, trials as columns, points in the cells, totals both ways. Rotated column headers, tabular figures, sticky first column. This is the season at a glance and it should look like a record, not a report.

**Ιστορικό σκύλου** — one page per dog: every trial, terrain, brace number, judges, qualification, points, and what each judge wrote, including both runs when the dog was recalled. This is the page breeders will actually use. Give it room: a quiet chronological timeline, newest first.

**Μεταφορά** — sending the data to another device. Explain the round trip in three lines and make merge the obvious default.

## 7. Field-mode rules

- Minimum tap target 48×48px. Assume cold hands and gloves.
- Primary actions in the bottom third. The top of a phone is unreachable one-handed.
- Contrast ratio 7:1 or better for anything that matters. Test against a screenshot at 50% brightness.
- No hover-dependent behaviour anywhere.
- Offline state is permanent chrome, not a toast: «Εκτός σύνδεσης – 6 αλλαγές σε αναμονή».
- Destructive or irreversible actions — re-draw, unlock, eliminate, replace-all on import — always need an explicit second confirmation.

## 8. Copy rules

Greek, sentence case, no exclamation marks, no encouragement. Use the club's own vocabulary exactly: τερέν, ζεύγος, κυναγωγός, φέρμα, πόντος, λευκή φέρμα, ποντάρισμα, συναίνεση, μπαράζ, κλήρωση, επανάκληση, βαθμολογία, οίστρος. Never invent a synonym.

Buttons say what happens, and the confirmation matches: press «Κλήρωση», see «Η κλήρωση ολοκληρώθηκε».

Errors state the fact and the fix, and cite the article where one applies:
«Το τερέν Β έχει 2 ζεύγη. Χρειάζονται τουλάχιστον 3 (Άρθρο 40). Μεταφέρετε σκύλους ή συγχωνεύστε τερέν.»

Empty states are instructions: «Καμία συμμετοχή ακόμη. Εισαγάγετε αρχείο Excel ή προσθέστε σκύλο.»

## 9. Deliverables

1. A token file — colours, type scale, spacing, radii, shadows — as CSS custom properties.
2. High-fidelity mobile screens for Κλήρωση, Τερέν (live), Σημειώσεις and SMS. These are the field screens and they carry the product.
3. Desktop screens for Μητρώο, Εισαγωγή (the mapping step), Στατιστικά and Ιστορικό σκύλου.
4. The brace card as a component with every state in §5.
5. A print stylesheet for the draw list and a blank judge note sheet — A4 portrait, black and white, legible after photocopying. It will be photocopied.
