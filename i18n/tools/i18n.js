/* Ο έλεγχος που κρίνει τη δουλειά: περπατά κάθε οθόνη σε κάθε γλώσσα και
   αναφέρει ό,τι έμεινε ελληνικό χωρίς λόγο.

   Λόγος υπάρχει σε τρεις περιπτώσεις, και μόνο σε τρεις:
   1. δεδομένα — ονόματα ανθρώπων, σκύλων, τόπων, σημειώσεις κριτών
   2. το ίδιο το όνομα της λέσχης, που είναι κύριο όνομα
   3. το Γλωσσάρι, όπου τα ελληνικά είναι το ίδιο το αντικείμενο, και οι
      τεκμηριωμένες τρύπες του: όροι που δεν στέκουν στους κανονισμούς μιας
      γλώσσας και δεν συμπληρώθηκαν με εικασία. */
const { chromium } = require('playwright');
const path0 = require('path');
/* Το αρχείο της εφαρμογής: δίπλα στο αποθετήριο, ή όπου το δείξει το KOAD_INDEX. */
const APP = 'file://' + (process.env.KOAD_INDEX || path0.resolve(__dirname, '../../index.html'));
const H = require('./walk.js');
const fs = require('fs');

const GR = /[Α-Ωα-ωΆ-ώΪΫϊϋΐΰ]/;
const DATA = [/Α\.\s|Β\.\s|Γ\.\s/, /ΑΡΗΣ|ΝΤΙΝΑ|ΛΟΥΝΑ|ΜΠΙΛΥ|ΡΕΞ|ΖΑΡΑ/,
  /Κάτω Μονή|Αθαλάσσα|Ξυλοφάγου/, /Τερέν [ΑΒΓΔ]/, /Καλή φέρμα στη ρεματιά/,
  /ΠΚ-ΚΑΤΩΜΟΝΗ|ΔΕΙΓΜΑ|ΠΕΡΙΣΤΡΟΦΗ/, /π\.μ\.|μ\.μ\./,
  /Μ\d/            /* αριθμός μέλους του δείγματος */];
/* Το όνομα της λέσχης, κεφαλαία στα τυπωμένα φύλλα και πεζά στην κάρτα του
   ιδιοκτήτη — κύριο όνομα και στις δύο μορφές, δεν μεταφράζεται. */
const CLUB = /Κ\.Ο\.Α\.Δ\.|ΚΥΠΡΙΑΚΟΣ ΟΜΙΛΟΣ|Κυπριακός Όμιλος|Κ\.Ο\.Κ\.|Ε\.Κ\.Ι\.|Ε\.ΦΥ\.Π\.|Τ\.Μ\.Ε\.|Μ\.Ε\./;
/* Τρία ακόμη που είναι σωστά ελληνικά και μένουν:
   — τα ονόματα των τερέν είναι Α, Β, Γ, Δ· γράμματα, όχι λέξεις
   — το πρότυπο SMS και τα πεδία του είναι δεδομένα των Ρυθμίσεων, τα γράφει ο
     γραμματέας και φεύγουν σε Κύπριους κυναγωγούς
   — ο επιλογέας γλώσσας δείχνει κάθε γλώσσα με το δικό της όνομα, και τη λέξη
     «φέρμα» δίπλα στα Ελληνικά */
const ON_PURPOSE = [/Α, Β, Γ, Δ/, /\{ΑΓΩΝΑΣ\}|\{ΗΜΕΡΟΜΗΝΙΑ\}|\{ΤΟΠΟΘΕΣΙΑ\}|\{ΩΡΑ\}/,
  /^Η σειρά είναι ενδεικτική \(Άρθρο 16\)\. Να είστε στη διάθεση των κριτών\.$/,
  /^Ελληνικά$/, /^ΕΛ$/, /^φέρμα$/];
/* Οι όροι που το γλωσσάρι δηλώνει κενούς σε κάποια γλώσσα. */
const GLOSSARY_GAPS = { de: [/επανάκληση/i], it: [/οίστρος/i], en: [], fr: [] };
const EVERY = [/Θηραματοφοβία/, /Κλαφούνισμα/, /Προσπέρασμα/];

(async () => {
  const b = await chromium.launch({ executablePath: process.env.KOAD_CHROME || undefined,
    args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  let bad = 0;
  const report = {};
  for (const L of ['en', 'fr', 'de', 'it']) {
    const page = await (await b.newContext({ viewport: { width: 1180, height: 2200 } })).newPage();
    page.setDefaultTimeout(6000);
    const errs = [];
    page.on('pageerror', e => errs.push(e.message));
    page.on('dialog', d => d.dismiss().catch(() => {}));
    await page.goto(APP, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(400);
    await page.evaluate(`window.LANG=${JSON.stringify(L)}`);
    await H.seed(page);
    const left = new Map();
    await H.walk(page, async where => {
      if (where === 'terms') return;            /* το γλωσσάρι είναι τα ελληνικά */
      for (const [s] of await page.evaluate(H.GRAB, where)) {
        if (!GR.test(s)) continue;
        if (DATA.some(r => r.test(s)) || CLUB.test(s)) continue;
        if (EVERY.some(r => r.test(s))) continue;
        if (ON_PURPOSE.some(r => r.test(s))) continue;
        if (GLOSSARY_GAPS[L].some(r => r.test(s))) continue;
        if (!left.has(s)) left.set(s, where);
      }
    });
    await page.close();
    report[L] = [...left].map(([s, w]) => ({ s, where: w }));
    const n = left.size;
    bad += n;
    console.log(`${L}: ${n ? n + ' αμετάφραστα' : 'καθαρό'}${errs.length ? '  ΣΦΑΛΜΑΤΑ: ' + errs.join('; ') : ''}`);
    [...left].slice(0, 12).forEach(([s, w]) => console.log(`     ${w.padEnd(18)} ${s.slice(0, 76)}`));
  }
  await b.close();
  fs.writeFileSync(__dirname + '/i18n-left.json', JSON.stringify(report, null, 1));
  console.log(bad ? '\n' + bad + ' συνολικά' : '\nκάθε οθόνη γυρίζει, και στις τέσσερις γλώσσες');
  process.exit(bad ? 1 : 0);
})();
