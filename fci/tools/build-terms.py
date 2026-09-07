#!/usr/bin/env python3
"""Χτίζει το γλωσσάρι κρίσης σε πέντε γλώσσες, με παραπομπή σε κάθε όρο.

Κάθε όρος βγήκε από τα κείμενα που βρίσκονται στο αποθετήριο. Τίποτα δεν
μεταφράστηκε από μνήμη. Δύο βαθμίδες τεκμηρίωσης, και φαίνεται ποια ισχύει:

  aco  — ο όρος στέκει στο ΙΔΙΟ άρθρο του κανονισμού των ηπειρωτικών δεικτών
         της F.C.I. σε αγγλικά, γαλλικά και γερμανικά. Η αντιστοιχία είναι της
         ίδιας της F.C.I., όχι δική μου ανάγνωση.
  own  — κάθε γλώσσα δίνει τον όρο της από τον δικό της κανονισμό, για την ίδια
         πράξη. Η αντιστοιχία προκύπτει από τους ορισμούς, όχι από παράλληλο
         κείμενο.

Πηγές:  ACO   FCI-ACO-REG (en-2019 / fr-2011 / de-2019), ανά άρθρο
        SC    FCI-ABR-REG-S-C-en · GQ  FCI-ABR-REG-GQU-en · TIT  FCI-REG-TIT-en-2024
        SCC   SCC-CUNCA-reglement-FT-fr-2026, ανά άρθρο · LEX  SCC-lexique-travail-fr
        VPS   VPS-Pruefungsordnung-de-2026, ανά §
        ENCI  ENCI-prove-razze-da-ferma-it-2026, ανά άρθρο
"""
import json

def T(el, en, fr, de, it, basis, group, koad="", note=""):
    """κάθε γλώσσα: (λήμμα, πηγή, κατά λέξη φράση) ή None όταν δεν στέκει στα κείμενα.
       Η φράση είναι ό,τι υπάρχει αυτούσιο στο έγγραφο· ο ελεγκτής την επαληθεύει."""
    row = {"el": el, "group": group, "basis": basis}
    for k, v in (("en", en), ("fr", fr), ("de", de), ("it", it)):
        row[k] = None if v is None else {"t": v[0], "src": v[1], "q": v[2] if len(v) > 2 else v[0]}
    if koad: row["koad"] = koad
    if note: row["note"] = note
    return row

TERMS = [

# ─────────── Ο αγώνας ───────────
T("τερέν",
  ("terrain",                 "ACO II.1 heading", "TERRAIN"),
  ("terrain",                 "ACO II.1 heading; SCC art. 33", "TERRAIN"),
  ("Prüfungsgelände, Gelände","ACO II.1 heading; ACO II.8", "DAS PRÜFUNGSGELÄNDE"),
  ("terreno",                 "ENCI art. 3"),
  "aco", "αγώνας", "Άρθρο 48"),

T("ζεύγος",
  ("brace, couple",   "ACO IX.25; ACO II.12"),
  ("couple",          "ACO II.12; ACO IX.25"),
  ("Paar, Paarlauf",  "ACO II.12; VPS Paarsuche (PS)"),
  ("coppia",          "ENCI art. 8"),
  "aco", "αγώνας", "Άρθρο 4"),

T("διαδρομή",
  ("run, round",  "ACO II.5; SC art. 14"),
  ("tour, parcours", "ACO II.5; SCC art. 29"),
  ("Durchgang",   "ACO II.5"),
  ("turno",       "ENCI art. 7"),
  "aco", "αγώνας", "Άρθρο 24",
  "Η F.C.I. ορίζει τουλάχιστον δεκαπέντε λεπτά για την πρώτη διαδρομή (ACO II.5)."),

T("κλήρωση",
  ("drawing of lots", "ACO I.17; ACO IX.19; ACO VIII.8"),
  ("tirage au sort",  "ACO I.17; SCC art. 14"),
  ("Auslosung",       "ACO VIII.8"),
  ("sorteggio",       "ENCI art. 3"),
  "aco", "αγώνας", "Άρθρο 16",
  "Και οι τέσσερις πηγές λένε το ίδιο: η σειρά είναι ενδεικτική. ACO I.17 «The drawing "
  "is only an indication of the running order»."),

T("επανάκληση",
  ("recall", "SC art. 14, 15", "recall"),
  ("rappel",             "ACO II.7; SCC art. 34"),
  None,
  ("richiamo, turno di richiamo", "ENCI art. 7"),
  "own", "αγώνας", "Άρθρο 30",
  "Ο γερμανικός όρος στο ACO II.7 στέκει ως «beim erneuten Aufrufen»· δεν υπάρχει "
  "μονολεκτικό ουσιαστικό στα κείμενα που έχουμε."),

T("μπαράζ",
  ("barrage, run-off", "ACO I.25, I.26; SC art. 22"),
  ("barrage",          "SCC art. 3; LEX «C.A.C.I.T.»"),
  None,
  (None, None) if False else (None, None),
  "own", "αγώνας", "",
  "Στα ιταλικά δεν βρέθηκε αντίστοιχος όρος: η ENCI λύνει το ίδιο πρόβλημα με «turni "
  "per l'assegnazione del CACIT» και «batterie» (ENCI art. 4), όχι με ξεχωριστή λέξη."),

T("κυναγωγός",
  ("handler",    "ACO II.11"),
  ("conducteur", "ACO II.11"),
  ("Führer",     "ACO II.11; VPS § 9 Führen der Hunde"),
  ("conduttore", "ENCI art. 8"),
  "aco", "αγώνας", "Άρθρο 5"),

T("κριτής",
  ("judge",          "ACO II.11"),
  ("juge",           "ACO II.11"),
  ("Richter",        "ACO II.11; VPS § 5"),
  ("esperto giudice","ENCI art. 11"),
  "aco", "αγώνας", "Άρθρο 48"),

T("Πρόεδρος Κριτών",
  ("chief judge, president of the jury", "SC art. 9; ACO IX.25"),
  ("président du jury",                  "ACO IX.25; SCC art. 14"),
  None,
  (None, None) if False else (None, None),
  "own", "αγώνας", "Άρθρο 48"),

T("οίστρος",
  ("bitches in season", "SC art. 3b", "Bitches in season"),
  ("chiennes en chaleurs", "SCC art. 3", "chiennes en chaleurs"),
  ("läufige Hündin",  "ACO I.6"),
  (None, None) if False else (None, None),
  "own", "αγώνας", "",
  "Οι κανονισμοί δεν συμφωνούν: το SC art. 3b δέχεται θηλυκές σε οίστρο στο τέλος του "
  "γύρου και μόνο μεταξύ τους· το ACO I.6 τις αποκλείει εντελώς. Δεν είναι θέμα "
  "ορολογίας — είναι δύο διαφορετικοί κανόνες, βρετανικός και ηπειρωτικός."),

# ─────────── Η διαδρομή ───────────
T("έρευνα",
  ("quest",  "ACO IX.25; ACO II.15"),
  ("quête",  "ACO II.15; ACO IX.25; SCC art. 33"),
  ("Suche",  "ACO II.15; VPS § 6"),
  ("cerca",  "ENCI art. 8"),
  "aco", "διαδρομή", "",
  "ACO II.15: «ενεργητική, έξυπνη και μεθοδική, χωρίς να ρυθμίζεται με τη σφυρίχτρα»."),

T("μύτη",
  ("nose", "GQ art. 5", "nose"),
  ("nez", "SCC art. 33", "nez et de la façon de prendre connaissance du gi"),
  ("Nase",   "VPS § 5 Nase, § 5 Nasengebrauch"),
  ("potenza olfattiva", "ENCI art. 17, 25", "olfattiva"),
  "own", "διαδρομή"),

T("ύφος",
  ("style", "SC art. 22", "style in relation to its breed"),
  ("style", "SCC art. 3", "style inhérent à la race"),
  ("Stil",   "VPS § 6 Stil der Suche"),
  ("stile",  "ENCI art. 11 §3 «Stile non conforme alla razza»"),
  "own", "διαδρομή", "",
  "Και οι τέσσερις το δένουν με τη φυλή: ασύμβατο ύφος είναι σφάλμα, όχι γούστο."),

T("ρυθμός",
  ("pace", "ACO IX.25", "insufficient in pace or in quest"),
  ("allure", "ACO IX.25", "insuffisant en allure"),
  ("Schnelligkeit und Ausdauer", "VPS § 7", "Ausdauer"),
  ("azione, fondo", "ENCI art. 11 §1, §7"),
  "own", "διαδρομή"),

T("πόντος",
  ("point", "ACO II.13"),
  ("point", "ACO II.13"),
  ("Punkt", "ACO II.13"),
  ("punto", "ENCI art. 8"),
  "aco", "διαδρομή", "",
  "ACO II.13: κανένα βραβείο σε σκύλο χωρίς έναν τουλάχιστον ολοκληρωμένο πόντο."),

# ─────────── Η ανατομία του πόντου — ACO II.13 ───────────
T("ανέβασμα στην αναθυμίαση",
  ("winding game", "ACO II.13", "winds game and points standing and rigid"),
  ("remontée d'émanation",  "ACO II.13"),
  ("weites Anziehen", "ACO II.13", "weitem Anziehen"),
  (None, None) if False else (None, None),
  "aco", "πόντος", "",
  "Το πρώτο σκέλος του πόντου στο ACO II.13. Στα ιταλικά δεν στέκει ως ξεχωριστός όρος "
  "στον κανονισμό της ENCI."),

T("φέρμα",
  ("pointing", "ACO II.13", "points standing and rigid"),
  ("arrêt debout tendu",       "ACO II.13"),
  ("festes Vorstehen, stehend und straff", "ACO II.13; VPS § 7"),
  ("ferma",                    "ENCI art. 11, 17"),
  "aco", "πόντος", "",
  "Και τα τέσσερα κείμενα ζητούν όρθια και τεντωμένη φέρμα. Ξαπλωτή φέρμα δεν "
  "αποκλείει, αλλά κόβει το ΕΞΑΙΡΕΤΟΣ (ACO II.13· ENCI art. 11 §12 «Ferma non rigida»)."),

T("ποντάρισμα",
  ("commanded approach", "ACO II.13"),
  ("coulé à l'ordre",    "ACO II.13"),
  ("Nachziehen auf Befehl", "ACO II.13; VPS § 11, § 13"),
  ("guidata, accostata", "ENCI art. 25; art. 11 §16"),
  "aco", "πόντος", "",
  "Η άρνηση αποκλείει και στα τέσσερα: ACO II.13 «Refusal to execute a commanded "
  "approach leads to elimination»· ENCI art. 11 §16 «Rifiuto di guidare»."),

T("ξεσήκωμα κατόπιν εντολής",
  ("commanded flush",  "ACO II.13"),
  ("flush à l'ordre",  "ACO II.13"),
  ("Herausstoßen auf Befehl", "ACO II.13"),
  (None, None) if False else (None, None),
  "aco", "πόντος"),

T("ακινησία στο πέταγμα",
  ("immobile when the game leaves", "ACO II.13"),
  ("immobilité au départ du gibier","ACO II.13"),
  ("Unbeweglichkeit beim Aufstehen des Wildes", "ACO II.13",
   "Unbeweglichkeit an Ort und Stelle beim Aufstehen des Wildes"),
  ("immobilità a frullo",           "ENCI art. 11 §5"),
  "aco", "πόντος"),

T("ακινησία στον πυροβολισμό",
  ("steady at gunshot", "ACO II.13"),
  ("sagesse au coup de feu", "ACO II.13; ACO II.10"),
  ("Ruhe beim Schuss, Schussruhe", "ACO II.13; VPS § 15, § 17"),
  ("immobilità allo sparo", "ENCI art. 11 §5", "immobilità a frullo e sparo"),
  "aco", "πόντος"),

T("συναίνεση",
  ("backing, honouring", "ACO IX.25; ACO II.19; GQ art. 8"),
  ("patron, patronner",  "ACO II.19; SCC art. 3"),
  ("Sekundieren, Mitstehen", "ACO II.19; VPS § 11, § 12, § 14"),
  ("consenso",           "ENCI art. 9"),
  "aco", "πόντος", "",
  "Η άρνηση αποκλείει: GQ art. 8 «A refusal to back is an eliminating fault»· "
  "SCC art. 3 «Le refus de patron … est éliminatoire»· ENCI art. 11 §8."),

T("λευκή φέρμα",
  ("pointing without result, false pointing", "ACO II.19; ACO IX.25"),
  ("faux arrêt",     "ACO II.19"),
  ("leeres Vorstehen","ACO II.19"),
  ("ferma a vuoto", "ENCI art. 11 §14, art. 25", "ferme a vuoto"),
  "aco", "πόντος", "Άρθρο 27",
  "Ο Κ.Ο.Α.Δ. κόβει στο ΠΟΛΥ ΚΑΛΟΣ με δύο λευκές (Άρθρο 27)· η ENCI art. 11 §14 "
  "αποκλείει πάνω από τρεις."),

T("απόρτ",
  ("retrieve", "SC art. 20", "retrieve game shot"),
  ("rapport",     "LEX· SCC art. 15"),
  ("Apportieren, Bringen", "VPS § 11, § 13"),
  ("riporto",     "ENCI art. 10"),
  "own", "πόντος"),

# ─────────── Σφάλματα αποκλεισμού — Άρθρο 33 ───────────
T("Συνειδητό ξεσήκωμα",
  ("intentional flush", "ACO II.8; GQ art. 7"),
  ("mettre sciemment à l'envol", "ACO II.8", "mettra sciemment à l’envol"),
  ("wissentliches Herausstoßen", "ACO II.8", "wissentlich Wild herausstößt"),
  ("avvertire e forzare", "ENCI art. 11 §15"),
  "aco", "σφάλματα", "Άρθρο 33"),

T("Κουτούλημα",
  ("flush",   "ACO II.8"),
  ("tape",    "ACO II.8"),
  ("Herausstoßen von Wild", "ACO II.8"),
  ("sfrullo", "ENCI art. 11 §2 (δεύτερος κατάλογος)"),
  "aco", "σφάλματα", "Άρθρο 33",
  "Ακούσιο ξεσήκωμα. Δεν μετρά στο πρώτο πέρασμα με τον άνεμο, δεξιά και αριστερά "
  "(ACO II.8· ENCI art. 11)."),

T("Προσπέρασμα",
  None,
  None,
  (None, None) if False else (None, None),
  ("sorpasso, trascuro del selvatico", "ENCI art. 11 §3 (δεύτερος κατάλογος)"),
  "own", "σφάλματα", "Άρθρο 33"),

T("Εκτός ελέγχου",
  ("out of hand",   "ACO II.9"),
  ("sortie de main","ACO II.9; SCC art. 27"),
  ("aus der Hand", "ACO II.9", "aus der Hand"),
  ("fuori mano",    "ENCI art. 11 §6"),
  "aco", "σφάλματα", "Άρθρο 33",
  "Το μόνο σφάλμα που αποκλείει ακόμη και μέσα στο ελεύθερο πρώτο λεπτό "
  "(SCC art. 27)."),

T("Τρεις λευκές σε διαφορετική κατεύθυνση",
  ("pointing without result", "ACO II.19", "pointing without result"),
  ("faux arrêts", "ACO II.19", "faux arrêts"),
  ("leeres Vorstehen", "ACO II.19", "leeres Vorstehen"),
  ("più di tre ferme a vuoto", "ENCI art. 11 §14"),
  "own", "σφάλματα", "Άρθρο 33"),

T("Άρνηση συναίνεσης",
  ("refusal of backing (honouring)", "ACO IX.25; GQ art. 8"),
  ("refus de patron", "SCC art. 3"),
  ("Nichtsekundieren, Verweigern des Sekundierens", "VPS § 14.3"),
  ("rifiuto di consenso", "ENCI art. 11 §8"),
  "own", "σφάλματα", "Άρθρο 33",
  "Προσοχή: η VPS § 14.3 λέει ρητά ότι το Nichtsekundieren ΔΕΝ αποκλείει από τη "
  "γερμανική εξέταση. Ο όρος είναι κοινός, ο κανόνας όχι."),

T("Κροτοφοβία",
  ("gun-shy", "ACO II.10", "gun-shy"),
  ("crainte caractérisée du coup de feu", "ACO II.10; SCC art. 32"),
  ("Schussscheue", "ACO II.10", "Schussscheue"),
  ("paura del colpo allo sparo", "ENCI art. 11 §19"),
  "aco", "σφάλματα", "Άρθρο 33"),

T("Θηραματοφοβία",
  (None, None) if False else (None, None),
  (None, None) if False else (None, None),
  None,
  (None, None) if False else (None, None),
  "own", "σφάλματα", "Άρθρο 33",
  "Δεν στέκει ως όρος στα κείμενα της F.C.I., της S.C.C. ή της ENCI. Μόνο η γερμανική "
  "εξέταση έχει ξεχωριστό κεφάλαιο για τη συμπεριφορά μπροστά σε θήραμα που ο σκύλος "
  "βλέπει."),

T("Κλαφούνισμα",
  None,
  ("donner de la voix", "SCC art. 3"),
  None,
  ("canizza persistente", "ENCI art. 11 §18"),
  "own", "σφάλματα", "Άρθρο 33",
  "Η αγγλική στήλη δεν έχει πηγή στα κείμενα που έχουμε — η S.C.C. art. 3 το λέει "
  "εξίσου αποκλειστικό με την άρνηση συναίνεσης, αλλά στα γαλλικά."),

T("Ανεπαρκής έρευνα",
  ("insufficient in quest", "ACO IX.25", "insufficient in pace or in quest"),
  ("insuffisant en quête", "ACO IX.25", "insuffisant en allure"),
  ("unplanmäßige Suche",    "ACO II.19"),
  ("cerca disordinata",     "ENCI art. 11 §2"),
  "aco", "σφάλματα", "Άρθρο 33"),

T("Παρενόχληση συνδιαγωνιζόμενου",
  ("hindering the brace mate", "ACO IX.25", "hinders its brace mate persistently"),
  ("gêner son concurrent", "ACO IX.25", "gênerait son concurrent"),
  ("den Konkurrenten behindern", "ACO II.19", "behindert"),
  ("rimorchio e disturbo al compagno di coppia", "ENCI art. 11 §5"),
  "aco", "σφάλματα", "Άρθρο 33"),

T("Καταδίωξη επί μακρόν",
  ("chasing", "ACO II.9", "chasing"),
  ("poursuite", "SCC art. 27", "poursuite"),
  ("Hetze", "VPS § 15 Gehorsam am Haarnutzwild", "Hetze"),
  ("rincorsa a fondo del selvatico", "ENCI art. 11 §17"),
  "own", "σφάλματα", "Άρθρο 33"),

T("Άρνηση πονταρίσματος",
  ("refusal to execute a commanded approach", "ACO II.13"),
  ("refus de couler à l'ordre", "ACO II.13"),
  ("Verweigern des Befehls zum Nachziehen", "ACO II.13"),
  ("rifiuto di guidare quando è in condizione di farlo", "ENCI art. 11 §16"),
  "aco", "σφάλματα", "Άρθρο 33"),

T("Πτώση ρυθμού",
  ("insufficient in pace", "ACO IX.25"),
  ("insuffisant en allure","ACO IX.25"),
  ("mangelnde Ausdauer", "VPS § 7", "Ausdauer"),
  ("mancanza di fondo",    "ENCI art. 11 §7"),
  "own", "σφάλματα", "Άρθρο 33"),

# ─────────── Βαθμολογία ───────────
T("ΕΞΑΙΡΕΤΟΣ",
  ("EXCELLENT",   "ACO II.13; SC art. 20"),
  ("Excellent",   "LEX «B., T.B., Exc.»; SCC art. 3"),
  ("Hervorragend","ACO II.13"),
  ("Eccellente",  "ENCI art. 25"),
  "aco", "βαθμολογία", "Άρθρο 27"),

T("ΠΟΛΥ ΚΑΛΟΣ",
  ("VERY GOOD",  "SC art. 20"),
  ("Très Bon",   "LEX «B., T.B., Exc.»"),
  ("Sehr gut",   "ACO"),
  ("Molto Buono","ENCI art. 26"),
  "own", "βαθμολογία", "Άρθρο 27"),

T("ΚΑΛΟΣ",
  ("GOOD",  "SC art. 20"),
  ("Bon",   "LEX «B., T.B., Exc.»"),
  ("Gut",   "ACO"),
  ("Buono", "ENCI"),
  "own", "βαθμολογία", "Άρθρο 27"),

T("Π.Φ.Π. (CQN)",
  ("CQN", "SC art. 20", "CQN will only be awarded"),
  ("C.Q.N.", "LEX", "C.Q.N. (CERTIFICAT DE QUALITES NATURELLES)"),
  (None, None) if False else (None, None),
  (None, None) if False else (None, None),
  "own", "βαθμολογία", "",
  "Εκτός κατάταξης, σε σκύλο μεγάλης αξίας με σφάλμα δρεσαρίσματος: SC art. 20 και "
  "LEX λένε το ίδιο, με τα ίδια λόγια."),

T("CACT / RCACT / CACIT / RCACIT",
  ("CACT / RCACT / CACIT / RCACIT", "TIT· SC art. 22"),
  ("CACT / RCACT / CACIT / RCACIT", "LEX· SCC art. 3"),
  ("CACT / RCACT / CACIT / RCACIT", "ACO I.25"),
  ("CAC / CACIT",                   "ENCI art. 4"),
  "own", "βαθμολογία", "",
  "Διεθνή αρκτικόλεξα — ίδια σε κάθε γλώσσα, δεν μεταφράζονται."),
]

for r in TERMS:
    for k in ("en", "fr", "de", "it"):
        if r[k] and r[k]["t"] is None: r[k] = None

out = {
 "about": "Ορολογία κρίσης field trial σε πέντε γλώσσες. Κάθε όρος με την πηγή του "
          "μέσα στα έγγραφα του αποθετηρίου. Τίποτα δεν μεταφράστηκε από μνήμη· όπου "
          "μια γλώσσα δεν έχει τον όρο στα κείμενα, το πεδίο είναι null και λέγεται.",
 "basis": {
   "aco": "Ο όρος στέκει στο ίδιο άρθρο του κανονισμού ηπειρωτικών δεικτών της F.C.I. "
          "σε αγγλικά, γαλλικά και γερμανικά — η αντιστοιχία είναι της F.C.I.",
   "own": "Κάθε γλώσσα δίνει τον όρο της από τον δικό της κανονισμό για την ίδια πράξη· "
          "η αντιστοιχία προκύπτει από τους ορισμούς."
 },
 "sources": {
   "ACO":  "fci/FCI-ACO-REG-{en-2019,fr-2011,de-2019}.pdf — ανά άρθρο",
   "SC":   "fci/FCI-ABR-REG-S-C-en.pdf",
   "GQ":   "fci/FCI-ABR-REG-GQU-en.pdf",
   "TIT":  "fci/FCI-REG-TIT-en-2024.pdf",
   "SCC":  "national/SCC-CUNCA-reglement-FT-fr-2026.pdf — ανά άρθρο",
   "LEX":  "national/SCC-lexique-travail-fr.pdf",
   "VPS":  "national/VPS-Pruefungsordnung-de-2026.pdf — ανά §",
   "ENCI": "national/ENCI-prove-razze-da-ferma-it-2026.pdf — ανά άρθρο"
 },
 "terms": TERMS,
}
json.dump(out, open('fci/terms-5lang.json', 'w'),
          ensure_ascii=False, indent=1)

n = len(TERMS)
full = sum(1 for r in TERMS if all(r[k] for k in "en fr de it".split()))
aco  = sum(1 for r in TERMS if r["basis"] == "aco")
gaps = [(r["el"], [k for k in ("en","fr","de","it") if not r[k]]) for r in TERMS
        if not all(r[k] for k in ("en","fr","de","it"))]
print(f"{n} όροι · {full} με πλήρεις τις πέντε γλώσσες · {aco} με αντιστοιχία της F.C.I.")
print(f"\nκενά ({len(gaps)}):")
for el, ks in gaps: print(f"  {el:<38} λείπει: {', '.join(ks)}")
