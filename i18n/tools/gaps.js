/* Ό,τι ξέρουν τα αγγλικά, πρέπει να το ξέρουν και οι άλλες τρεις — αλλιώς ο
   Ιταλός βλέπει αγγλικά μέσα σε ιταλική οθόνη. Ελέγχονται και τα κλειδιά που
   ο κώδικας ζητά ως μεταβλητή, γιατί αυτά δεν φαίνονται σε καμία σάρωση. */
const { chromium } = require('playwright');
const path0 = require('path');
/* Το αρχείο της εφαρμογής: δίπλα στο αποθετήριο, ή όπου το δείξει το KOAD_INDEX. */
const APP = 'file://' + (process.env.KOAD_INDEX || path0.resolve(__dirname, '../../index.html'));
const fs = require('fs'), path = require('path');
(async () => {
  const b = await chromium.launch({ executablePath: process.env.KOAD_CHROME || undefined,
    args: ['--no-sandbox'] });
  const p = await b.newPage();
  await p.goto(APP, { waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(400);
  /* Τα κλειδιά που ο κώδικας γράφει κυριολεκτικά, από το ίδιο το αρχείο. Όσα
     περνούν ως μεταβλητή τα προσθέτει πιο κάτω η ίδια η σελίδα. */
  const src = fs.readFileSync(APP.replace('file://', ''), 'utf8');
  const lits = [...new Set([...src.matchAll(/\btx\(\s*"((?:[^"\\]|\\.)*)"\s*\)/g)]
    .map(m => m[1].replace(/\\"/g, '"').replace(/\\\\/g, '\\')))];
  const out = await p.evaluate(ks => {
    const all = new Set(ks);
    Object.keys(STR.en || {}).forEach(k => all.add(k));
    /* και τα λεξιλόγια που περνούν ως μεταβλητή */
    [].concat(TYPES, QUALS, AWARDS, MONTHS, BREED_SECTIONS.map(x => x[1]),
      Object.keys(DEFAULT_POINTS)).forEach(k => typeof k === "string" && all.add(k));
    const r = {};
    for (const L of ['en','fr','de','it'])
      r[L] = [...all].filter(k => !(STR[L] && STR[L][k] !== undefined));
    return r;
  }, lits);
  await b.close();

  /* Ό,τι δεν μεταφράζεται ποτέ, και γιατί. */
  const NEVER = new Set([
    "-", "CACT", "RCACT", "CACIT", "RCACIT", "Derby",   /* διεθνείς τίτλοι */
    "Κ.Ο.Α.Δ.", "Κ.Ο.Α.Δ. –", "ΚΥΠΡΙΑΚΟΣ ΟΜΙΛΟΣ ΑΓΓΛΙΚΩΝ ΔΕΙΚΤΩΝ", /* κύριο όνομα */
    "Ε.Κ.Ι.", "Ε.ΦΥ.Π.", "Τ.Μ.Ε."                       /* συντομογραφίες της λέσχης */
  ]);
  /* Όροι που ο κανονισμός εκείνης της γλώσσας δεν έχει. Το γλωσσάρι τους δηλώνει
     κενούς και δεν συμπληρώθηκαν με εικασία· η οθόνη πέφτει στα αγγλικά. */
  const GLOSSARY_GAPS = {
    en: [], fr: [],
    de: ["Επανάκληση", "επανάκληση", "Μπαράζ", "μπαράζ", "Π.Φ.Π. (CQN)", "Πρόεδρος Κριτών"],
    it: ["Μπαράζ", "μπαράζ", "Οίστρος", "οίστρος", "Π.Φ.Π. (CQN)", "Πρόεδρος Κριτών",
         "Ανέβασμα στην αναθυμίαση", "ανέβασμα στην αναθυμίαση",
         "Ξεσήκωμα κατόπιν εντολής", "ξεσήκωμα κατόπιν εντολής"]
  };
  let bad = 0;
  for (const L of Object.keys(out)) {
    const left = out[L].filter(k => !NEVER.has(k) && !GLOSSARY_GAPS[L].includes(k));
    bad += left.length;
    console.log(L + ': ' + (left.length ? left.length + ' κενά — ' + left.slice(0, 8).join(' · ')
                                        : 'πλήρες'));
  }
  fs.writeFileSync(path.join(__dirname, 'gaps.json'), JSON.stringify(out, null, 1));
  console.log(bad ? '\n' + bad + ' κλειδιά χωρίς μετάφραση'
                  : '\nκάθε κλειδί που ξέρουν τα αγγλικά, το ξέρουν και οι τρεις άλλες');
  process.exit(bad ? 1 : 0);
})();
