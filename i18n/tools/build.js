/* Ο αριθμός έκδοσης ζει σε δύο αρχεία και πρέπει να είναι ο ίδιος:
   το CACHE στο sw.js ορίζει τι κατεβαίνει, το APP_BUILD μέσα στο index.html
   λέει τι τρέχει. Αν ξεφύγουν, η οθόνη γράφει μόνιμα «εκκρεμεί επαναφόρτωση»
   σε κόσμο που είναι ήδη ενήμερος — δηλαδή ξαναλέει ψέματα, ανάποδα.

   Τρέχει σαν: node i18n/tools/build.js */
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '../..');
const sw = fs.readFileSync(path.join(root, 'sw.js'), 'utf8');
const ix = fs.readFileSync(path.join(root, 'index.html'), 'utf8');

const cache = (sw.match(/const CACHE\s*=\s*"([^"]+)"/) || [])[1];
const app   = (ix.match(/const APP_BUILD\s*=\s*"([^"]+)"/) || [])[1];

let bad = 0;
const say = (ok, msg) => { console.log((ok ? 'ok   ' : 'FAIL ') + msg); if(!ok) bad++; };

say(!!cache, 'το sw.js ορίζει CACHE' + (cache ? ' — ' + cache : ''));
say(!!app,   'το index.html ορίζει APP_BUILD' + (app ? ' — ' + app : ''));
say(cache === app, 'οι δύο αριθμοί συμφωνούν'
  + (cache === app ? '' : ' — sw.js ' + cache + ' ≠ index.html ' + app));
say(/^koad-v\d+$/.test(app || ''), 'η μορφή είναι koad-vN');

console.log(bad ? '\n' + bad + ' fail' : '\nη έκδοση που κατεβαίνει είναι η έκδοση που τρέχει');
process.exit(bad ? 1 : 0);
