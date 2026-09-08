/* Τα πεδία του προτύπου διαβάζονται στη γλώσσα, γράφονται ελληνικά, και το
   μήνυμα βγαίνει σωστό όποια γλώσσα κι αν γράφτηκε. */
const { chromium } = require('playwright');
const H = require('./walk.js');
const path0 = require('path');
const APP = 'file://' + (process.env.KOAD_INDEX || path0.resolve(__dirname, '../../index.html'));
(async () => {
  const b = await chromium.launch({ executablePath: process.env.KOAD_CHROME || undefined, args:['--no-sandbox'] });
  let bad = 0;
  const step = async (n, f) => { try { const x = await f(); console.log('ok   ' + n + (x?' — '+x:'')); }
    catch(e){ console.log('FAIL ' + n + ' — ' + e.message); bad++; } };

  for (const [L, want, at] of [['it','{PROVA}','ore'], ['fr','{EPREUVE}','à'],
                               ['de','{PRUEFUNG}','um'], ['en','{TRIAL}','at'],
                               ['es','{PRUEBA}','a las']]) {
    const p = await (await b.newContext({viewport:{width:900,height:1400}})).newPage();
    p.on('pageerror', e => { console.log('PAGEERROR ' + L + ': ' + e.message); bad++; });
    await p.goto(APP,{waitUntil:'domcontentloaded'});
    await p.waitForTimeout(300);
    await p.evaluate(`window.LANG=${JSON.stringify(L)}`);
    await H.seed(p);
    await p.evaluate(()=>{S.view='settings';render();});
    await p.waitForTimeout(250);

    await step(L + ': τα πεδία διαβάζονται στη γλώσσα', async () => {
      const v = await p.$eval('#smsTpl', e=>e.value);
      if(!v.includes(want)) throw new Error(v);
      if(/ΑΓΩΝΑΣ|ΗΜΕΡΟΜΗΝΙΑ|ΤΟΠΟΘΕΣΙΑ|ΩΡΑ/.test(v)) throw new Error('έμεινε ελληνικό πεδίο: ' + v);
      if(!v.includes(at)) throw new Error('το κείμενο δεν γύρισε: ' + v);
      const lab = await p.$eval('#smsTpl', e=>e.parentElement.querySelector('label').textContent);
      if(!lab.includes(want)) throw new Error('η ετικέτα κρατά ελληνικά: ' + lab);
      return v.split('\n')[1];
    });

    await step(L + ': η επικεφαλίδα του μηνύματος βγαίνει γεμάτη', async () => {
      const h = await p.evaluate(()=>smsHead(trialById('T'), trialById('T').days[0]));
      if(/\{/.test(h)) throw new Error('έμεινε πεδίο ασυμπλήρωτο: ' + h);
      if(!h.includes('Κάτω Μονή') || !h.includes('07:00')) throw new Error(h);
      return h.replace(/\n/g,' | ');
    });

    await step(L + ': Αποθήκευση χωρίς αλλαγή δεν παγώνει τη γλώσσα', async () => {
      await p.evaluate(()=>{ ACT.saveSms(); });
      const stored = await p.evaluate(()=>DB.settings.sms);
      if(stored !== await p.evaluate(()=>DEFAULT_SMS))
        throw new Error('η προεπιλογή πάγωσε: ' + JSON.stringify(stored));
      return 'μένει προεπιλογή';
    });

    await step(L + ': δικό του κείμενο μένει όπως γράφτηκε, με ελληνικά κλειδιά', async () => {
      await p.evaluate(w=>{ el("smsTpl").value = "TEST " + w + " X"; ACT.saveSms(); }, want);
      const stored = await p.evaluate(()=>DB.settings.sms);
      if(!stored.includes("{ΑΓΩΝΑΣ}")) throw new Error('δεν γύρισε σε ελληνικό κλειδί: ' + stored);
      const h = await p.evaluate(()=>smsHead(trialById('T'), trialById('T').days[0]));
      if(!h.includes('Κάτω Μονή')) throw new Error('δεν αντικαταστάθηκε: ' + h);
      return stored + '  →  ' + h;
    });
    await p.close();
  }
  await b.close();
  console.log(bad ? '\n' + bad + ' fail' : '\nτα πεδία γυρίζουν, η βάση μένει ελληνική');
  process.exit(bad?1:0);
})();
