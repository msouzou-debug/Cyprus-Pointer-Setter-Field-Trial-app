# Regulations — what is here, and what each one is good for

Uploaded 5 September 2026 as 25 files. Ten distinct documents; the other fifteen were
**byte-identical** re-downloads of the same file, so nothing had to be judged between versions —
every set of duplicates had one identical SHA-256. They were removed. Four more arrived on
7 September — the S.C.C. and Verein für Pointer und Setter regulations, the ENCI breed
nomenclature, and the current ENCI trial regulation. One more on 12 September: the **European
Cup Grande Quête** regulation, the one that governs the club's own breeds in a team competition
and was the single document missing. Four files arrived with it and were byte-identical to copies
already here, so nothing was replaced.

## F.C.I. — the international baseline

| File | Document | Pages | Approved |
|---|---|---|---|
| `FCI-ABR-REG-S-C-en.pdf` | International Field Trial Regulations for **Individual and Paired** events for British Pointing Dogs | 6 | — |
| `FCI-ABR-REG-GQU-en.pdf` | International Regulations of **Grande Quête** field trials for British Pointing Dogs | 2 | — |
| `FCI-ABR-REG-GQU-CDE-en.pdf` | Regulations of the **European Cup Grande Quête** field trials for British Pointing Dogs | 4 | amendments approved by the F.C.I. General Committee, online meeting September 2020; in force 1 January 2021 |
| `FCI-ACO-REG-en-2019.pdf` | Official Rules and Bylaws, **Continental Pointers** | 42 | ratified June 1999, Mexico City; §VIII amended Como, September 2019 |
| `FCI-ACO-REG-de-2019.pdf` | the same, German | 41 | §VII amended Como, September 2019 |
| `FCI-ACO-REG-fr-2011.pdf` | the same, French | 41 | **older edition** — bold text approved Paris, July 2011 |
| `FCI-REG-TIT-en-2024.pdf` | Regulations for the F.C.I. **International Championship** — C.I.T., CACIT, RCACIT | 21 | amended March 2024 and September 2024 |
| `FCI-ABR-REG-S-C-da.pdf` | the Individual and Paired regulations, **in Danish** | 6 | — |

The first two are the ones that govern what Κ.Ο.Α.Δ. runs.

### The European Cup, and which one it is

There are two, and they are different documents with different numbers.

- **British breeds — `FCI-ABR-REG-GQU-CDE-en.pdf`.** The *European Cup Grande Quête*, created in
  1950 by France, Belgium, Italy and Switzerland. This is the one that concerns Κ.Ο.Α.Δ.'s own
  breeds. Teams of **one to four dogs plus two substitutes**, run **in couple**, and a rule the
  ordinary draw does not have: *"dogs belonging to the same team may not run together"*. Even when
  held over two days it produces **one ranking**. Three judges — a chief judge and two wings.
  Bitches in heat may compete provided their partner is also female. The English text is the
  authentic one; it says so itself.
- **Continental breeds — `FCI-ACO-REG-en-2019.pdf`, Section VIII.** The *Spring European Cup*,
  created 1985. Teams of **two to four plus one substitute**, run **solo over two days**, groups of
  at most 14, and a bonus of 4 or 2 points for a team of four or three different breeds.

Both place a team the same way: **at least two dogs classified and a minimum of 9 points**
(CDE-GQ *Classification* · ACO VIII.11.4). Their points tables are not the same table — the
CDE-GQ scale runs 12 / 11 / 10 / 9 / 8 / 7 / 4 / 2 down from *EXC.CAC and FCI-CACIT*, and gives the
third Excellent its own row, which is why the app's qualification list has a **3ος ΕΞΑΙΡΕΤΟΣ**.

Two places where the same word carries a different rule, worth reading before anything is treated
as common:

- **The handler.** Under CDE-GQ he *may* run for more than one country, and *"the dogs composing
  his team represent the country of their owner"*. Under ACO VIII.5.3 and IX.13 he may **not**.
  The app therefore takes the team from the dog's own record, never from its handler.
- **Bitches in season.** CDE-GQ admits them if the partner is a female. `FCI-ABR-REG-S-C` art. 3b
  puts them at the end of the round and only with each other. ACO I.6 excludes them outright.

`FCI-ACO-REG-en-2019.pdf` Section IX is a third team competition, the **World Championship of
Practical Hunting**, and it is the only one of the three open to British *and* Continental teams at
once. It scores **the two days added together** (IX.29, IX.33) — which the app cannot yet do, since
it keeps one result per dog per trial.

### How the app holds all three

A team is a record on the trial, not a label on a dog: country, captain, the dogs in it and the
named substitutes. A trial that is a Cup carries the numbers of the regulation it is run under, and
they differ enough that they cannot be one setting:

| | dogs | substitutes | placed with | breed bonus | one handler, one country | per group | studbook | export stamp |
|---|---|---|---|---|---|---|---|---|
| **CDE-GQ** (British, European Cup) | 1–4 | 2 | 2 classified, 9 points | no | **no** — he may run for several | — | registered, no term | ≥ 6 months |
| **ACO VIII** (Continental, Spring European Cup) | 2–4 | 1 | 2 classified, 9 points | 4 breeds +4, 3 breeds +2 | yes | **14** | ≥ 12 months | — |
| **ACO IX** (World, Practical Hunting) | 2–4 | 1 | 2 classified | no | yes | — | ≥ 12 months | — |

All three require the owner's nationality, or twelve months' residence, in the country the dog
represents. Only ACO VIII locks a dog to its first country (VIII.5.3).

Picking the cup fills those numbers in; a club running something else edits them. The screen then
reports what does not hold — a team under or over strength, too many substitutes, a dog in two
teams, a handler running for two countries where that is forbidden, an entered dog in no team — each
line naming the article that requires it.

Three consequences worth knowing:

- **Membership is the record, never the registry tag.** Once a trial has one team, a dog belongs to
  the team that holds it or to none; the `Εθνική ομάδα` field on the dog is only the suggestion the
  *Fill in from the register* button acts on. Before the first team exists the tag is still used, so
  a trial just declared a Cup is not empty.
- **The substitute is a member who does not score.** He appears in the team, he is kept out of his
  compatriot's brace by the draw, and he brings neither points nor a breed to the bonus — *"with the
  exception of the substitute dog"* (ACO VIII.5.4a).
- **A Cup has no coefficient.** The regulation's table is an absolute scale and the nine points are
  measured on it.
- **The group cap shapes the draw, not just a warning.** ACO VIII.8.1 caps a group at 14 and
  VIII.8.2's table — *less than 15 = 1 group, more than 14 and less than 29 = 2* — is exactly
  `ceil(n/14)`; the draw screen says how many terrains that needs against how many exist. Inside
  the draw a full terrain drops out of the candidates, and VIII.8.3's proportional spread is the
  *first* sort key in a Cup, ahead of the app's own habit of scattering one handler's dogs. That
  order matters: with the handler first, five teams over three terrains came out 2-0-4; with the
  team first, 2-2-2. If the terrains genuinely cannot hold everyone the cap yields rather than
  leaving a dog out of the trial — the warning has already been given, and a dog missing from the
  running order is the worse failure.
- **An empty eligibility field is reported, not assumed good.** The four fields live folded away on
  the dog's record, because a club that never hosts a Cup should not scroll past them; the checks
  read them only when the trial is a Cup, and each line names the article behind it. The one
  exception is the export stamp: blank there means home-bred, which is not a gap.

The exports carry all of it. The workbook gains two sheets ahead of the rest — **Ομάδες**, the
classification per country, and **Συγκρότηση**, every dog with its role and its captain — and the
`Δεδομένα` sheet gains a team and a role column. The classification is computed *in the file*, by
`SUMIFS` and `COUNTIFS` over `Δεδομένα` with every threshold read from a block of the regulation's
own numbers at the foot of the sheet: correct a qualification and the placings re-sort themselves,
with no app involved. One number is data rather than formula and says so in a comment — the count
of distinct breeds, which no portable spreadsheet formula expresses legibly; the bonus *rule* is
still live `IF` logic over that count. Word opens on the team result before the individual one, and
the drawn order — in the workbook and in the CSV — shows the team on each side of every brace, which
is where the committee checks that no pair holds two compatriots.

## National

| File | Document | Pages | Date |
|---|---|---|---|
| `../national/SCC-CUNCA-reglement-FT-fr-2026.pdf` | S.C.C. / C.U.N.C.A., **Règlements des Épreuves de Travail pour chiens d'arrêt** — field-trials, Grande Quête, épreuves à la française, BICP, TAN | 53 | in force 1 February 2026; amendments approved by the S.C.C. Committee 29 January 2026 |
| `../national/SCC-lexique-travail-fr.pdf` | S.C.C., Lexique travail — French working-trial vocabulary | 5 | — |
| `../national/VPS-Pruefungsordnung-de-2026.pdf` | Verein für Pointer und Setter e.V., **Prüfungsordnung** | 48 | Fassung Januar 2013, Stand 14 August 2026 |
| `../national/ENCI-prove-razze-da-ferma-it-2026.pdf` | ENCI, **Regolamento delle prove – verifiche zootecniche per i cani delle razze da ferma** | 26 | amended by the Consiglio Direttivo 17 April 2026, in force the same day |
| `../national/ENCI-prove-razze-da-ferma-it-2024.pdf` | the same, **superseded** — kept only to read a change against | 24 | Consiglio Direttivo 6 February 2024 |
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

## `TERMS.md` και `terms-5lang.json` — η ορολογία κρίσης σε πέντε γλώσσες

**43 όροι**, από τον κανονισμό στην κάρτα σημειώσεων: το τερέν και το ζεύγος, η ανατομία
του πόντου, τα δεκατέσσερα σφάλματα αποκλεισμού του Άρθρου 33, η βαθμολογία. Ελληνικά,
αγγλικά, γαλλικά, γερμανικά, ιταλικά. 33 πλήρεις και στις πέντε.

Τίποτα δεν μεταφράστηκε. Κάτω από κάθε όρο στέκει **η φράση αυτούσια όπως είναι γραμμένη
στον κανονισμό**, με την παραπομπή της, και ο έλεγχος επαληθεύει ότι υπάρχει πράγματι
μέσα στο έγγραφο εκείνης της γλώσσας. 153 παραπομπές, όλες περνούν.

**Το εύρημα που κάνει το υπόλοιπο αξιόπιστο** είναι ότι ο κανονισμός των ηπειρωτικών
δεικτών της F.C.I. υπάρχει εδώ σε αγγλικά, γαλλικά και γερμανικά — το ίδιο κείμενο,
άρθρο προς άρθρο. 193 άρθρα ευθυγραμμίστηκαν. Όπου ένας όρος στέκει στο ίδιο άρθρο και
στις τρεις γλώσσες, η αντιστοιχία είναι της ίδιας της F.C.I., όχι δική μας ανάγνωση —
24 από τους 43 όρους στέκουν έτσι. Το πιο πυκνό είναι το **ACO II.13**, που ορίζει τον
πόντο σκέλος προς σκέλος και δίνει μονομιάς τα πεδία σημειώσεων της εφαρμογής:

| | | |
|---|---|---|
| ανέβασμα στην αναθυμίαση | *winds game* | *remontée d'émanation* · *weitem Anziehen* |
| φέρμα | *points standing and rigid* | *arrêt debout tendu* · *festes Vorstehen* |
| ποντάρισμα | *commanded approach* | *coulé à l'ordre* · *Nachziehen auf Befehl* |
| ακινησία στο πέταγμα | *immobile when the game leaves* | *immobilité au départ du gibier* |
| ακινησία στον πυροβολισμό | *steady at gunshot* | *sagesse au coup de feu* · *Schussruhe* |

**Τα κενά είναι εύρημα, όχι παράλειψη.** Δέκα όροι δεν έχουν αντίστοιχο σε κάποια
γλώσσα και το κελί μένει κενό αντί να συμπληρωθεί με εικασία. Η *Θηραματοφοβία* δεν
στέκει σε κανέναν από τους τέσσερις κανονισμούς. Το *μπαράζ* δεν υπάρχει ως λέξη στα
ιταλικά — η ENCI λύνει το ίδιο πρόβλημα με «batterie». Ο ελεγκτής βρήκε **29 λάθη στο
πρώτο πέρασμα**: λήμματα γραμμένα αντί για τη γραμμένη μορφή, και τρεις παραπομπές που
απλώς δεν έστεκαν — «nose» δεν υπάρχει στο ACO II.13, όπως νόμιζα.

Δύο σημεία όπου ο **όρος είναι κοινός αλλά ο κανόνας όχι**, και αξίζουν προσοχή πριν
διαβαστεί κάτι ως ενιαίο:

- **Άρνηση συναίνεσης.** Αποκλείει κατά F.C.I. (GQ art. 8), κατά S.C.C. (art. 3) και κατά
  ENCI (art. 11 §8). Η γερμανική VPS § 14.3 λέει ρητά το αντίθετο: το Nichtsekundieren
  **δεν** αποκλείει από την εξέταση.
- **Οίστρος.** Το FCI-ABR-REG-S-C art. 3b δέχεται θηλυκές σε οίστρο στο τέλος του γύρου
  και μόνο μεταξύ τους· το ACO I.6 τις αποκλείει εντελώς. Βρετανικός και ηπειρωτικός
  κανόνας, δύο διαφορετικά πράγματα.

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

## What changed in the ENCI regulation, 2024 → 2026

Both editions are here, so the change is readable rather than asserted. The text is 93.9% the same;
23 places differ, 24 lines out and 108 in, and four amendments the 2024 copy predates — 23 July
2024, 17 October 2024, 27 February 2025, 24/25 September 2025 — plus 17 April 2026 itself. What
actually moved:

- **A closed season.** Trials on wild game, woodcock, snipe, partridge and woodcock monitoring
  **may not be held between 15 April and 15 July**, the breeding period. New rule, no equivalent
  in 2024.
- **The tracking collar is now named and confined.** Where 2024 allowed a generic *localizzatore*
  alongside the bell, the 2026 text names one device — the **ENCI BTB6000 HYBRID** — says the jury
  consults it *only* to locate a dog on point, gives the handler its palmare / smartwatch / phone
  *only* to recover a dog in difficulty, and **forbids any other locating device on the collar**.
  This is repeated in every trial type, which is most of the 108 added lines.
- **British breeds run in couple** except now also **in snipe trials**, alongside the first round of
  the Derby, woodcock and mountain game. The same exception is added for the continentals.
- **Derby**: entry is now by age — partridge and wild-game trials **after 12 months** — instead of
  "not before 1 September of the previous year", and having run in *any* free trial now bars entry.
- **Prize money** on classic quail trials, capped at 40% of entries in 2024, is simply "not
  permitted" now.
- **A judge may judge only one batteria per sub-trial per day** (continentali mista, mista
  continentali italiani, mista inglesi, and so on). New.
- **Shot-game trials and the retrieving certificate** may only be run inside the open hunting season,
  organised by ENCI or an authorised specialist association, with the Regional Decree attached to
  the jury request.
- Grande quête and classic quail trials **now count as special trials** for championship purposes,
  provided the qualifications are Italian.

None of this binds Κ.Ο.Α.Δ. — these are Italian national rules and the club runs under the F.C.I.
They matter here only as the Italian source for the judging vocabulary.

## Still missing

Nothing. Every document named in the earlier revisions of this file is now in the repository.
