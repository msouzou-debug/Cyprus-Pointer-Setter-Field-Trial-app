/* Κοινό βήμα για κάθε έλεγχο γλώσσας: στήνει έναν πλήρη αγώνα και περπατάει
   κάθε οθόνη, κάθε καρτέλα και κάθε διάλογο, μαζεύοντας ό,τι φαίνεται. */

const DATA = ['Α. Παπά','Β. Βασιλείου','Γ. Σάββα','ΑΡΗΣ','ΝΤΙΝΑ','ΛΟΥΝΑ','ΜΠΙΛΥ','ΡΕΞ','ΖΑΡΑ',
  'Α. Κριτής','Β. Δεύτερος','Κάτω Μονή','Αθαλάσσα','Ξυλοφάγου','Τερέν Α','Τερέν Β',
  'Καλή φέρμα στη ρεματιά','Κ.Ο.Α.Δ.'];

const seedFn = () => {
  const people = ['Α. Παπά','Β. Βασιλείου','Γ. Σάββα']
    .map((n, i) => ({ id: 'p' + i, name: n, phone: '+3579911111' + i, member: 'Μ' + i, country: 'CY' }));
  const dogs = ['ΑΡΗΣ','ΝΤΙΝΑ','ΛΟΥΝΑ','ΜΠΙΛΥ','ΡΕΞ','ΖΑΡΑ']
    .map((n, i) => ({ id: 'd' + i, name: n, breed: BREEDS[i % 6], sex: i % 3 ? 'Α' : 'Θ',
      reg: 'CY-' + (400 + i), dob: '2021-01-01', kennel: '', ownerId: 'p' + (i % 3),
      cy: true, country: 'CY' }));
  const judges = ['Α. Κριτής','Β. Δεύτερος'].map((n, i) => ({ id: 'j' + i, name: n,
    phone: '+3579620000' + i, licence: 'ΕΠΙΣΗΜΟΣ', me: i === 0, personId: '', country: 'CY' }));
  const t = { id: 'T', title: 'Κάτω Μονή', type: 'Πρακτικού Κυνηγίου', format: 'ΖΕΥΓΗ',
    game: 'Πέρδικα', wild: true, award: 'CACT', place: 'Κάτω Μονή', dateStart: '2026-02-14',
    time: '07:00', status: 'ΔΗΛΩΣΕΙΣ',
    entries: dogs.map((d, i) => ({ id: 'e' + i, dogId: d.id, handlerId: d.ownerId,
      status: 'ΔΗΛΩΜΕΝΟΣ', paid: i % 2 === 0, season: i === 5 })),
    results: {}, notes: {}, sms: {},
    days: [{ date: '2026-02-14', terrains: [
      { id: 'trA', name: 'Τερέν Α', breedGroup: '', judgeIds: ['j0','j1'], slots: ['j0','j1'],
        headJudgeId: 'j0', entryIds: [], braces: [] }], draw: null }] };
  const old = { id: 'T2', title: 'Αθαλάσσα', type: 'Έρευνας Κυνηγίου', format: 'ΑΤΟΜΙΚΑ',
    game: 'Μπεκάτσα', wild: false, award: 'CACIT', place: 'Αθαλάσσα', dateStart: '2025-11-22',
    time: '06:30', status: 'ΟΛΟΚΛΗΡΩΜΕΝΟΣ',
    entries: dogs.slice(0, 3).map((d, i) => ({ id: 'o' + i, dogId: d.id, handlerId: d.ownerId,
      status: 'ΕΤΡΕΞΕ', paid: true, season: false })),
    results: { o0: { qual: 'ΕΞΑΙΡΕΤΟΣ', award: 'CACIT' }, o1: { qual: 'ΠΟΛΥ ΚΑΛΟΣ', award: '-' },
               o2: { qual: 'ΑΠΟΚΛΕΙΣΤΗΚΕ', award: '-' } },
    notes: {}, sms: {}, days: [{ date: '2025-11-22', terrains: [], draw: null }] };
  DB = { v: 1, people, judges, dogs, settings: DB.settings, trials: [t, old] };
  DB.settings.lang = window.LANG || 'el';
  save();
  const tr = trialById('T');
  tr.days[0].terrains[0].entryIds = tr.entries.map(e => e.id);
  const r = runDraw(tr, 0, 'ΔΕΙΓΜΑ', 'ΠΕΡΙΣΤΡΟΦΗ');
  if (r && r.braces) tr.braces = r.braces;
  tr.status = 'ΣΕ ΕΞΕΛΙΞΗ';
  const b = tr.braces || [];
  if (b[0]) { b[0].status = 'ΕΤΡΕΞΕ'; b[0].startedAt = Date.now() - 900000; }
  if (b[1]) { b[1].status = 'ΤΡΕΧΕΙ'; b[1].startedAt = Date.now() - 300000; }
  if (b[2]) { b[2].recall = true; }
  tr.notes['e0'] = { pts: [{ kind: 'ΠΟΝΤΟΣ', t: 120, ok: true, note: 'Καλή φέρμα στη ρεματιά' }],
                     faults: ['ΑΝΑΚΡΙΒΕΙΑ'], text: 'Καλή φέρμα στη ρεματιά' };
  tr.results['e0'] = { qual: 'ΕΞΑΙΡΕΤΟΣ', award: 'CACT' };
  tr.results['e1'] = { qual: 'ΑΠΟΚΛΕΙΣΤΗΚΕ', award: '-' };
  tr.sms['p0'] = { sentAt: Date.now(), chan: 'sms' };
  save(); S.view = 'trials'; S.trialId = null; render();
};

const GRAB = w => {
  const out = [];
  const ATTRS = ['placeholder', 'title', 'aria-label', 'alt'];
  const roots = [document.getElementById('app'), document.getElementById('warn'),
                 document.getElementById('fab'), document.querySelector('nav'),
                 document.getElementById('dlgBody')].filter(Boolean);
  for (const root of roots) {
    const wk = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let n;
    while ((n = wk.nextNode())) {
      const s = n.nodeValue.replace(/\s+/g, ' ').trim();
      if (s) out.push([s, w, (n.parentElement || {}).tagName || '']);
    }
    root.querySelectorAll('*').forEach(e => {
      ATTRS.forEach(a => { const v = e.getAttribute(a);
        if (v && v.trim()) out.push([v.replace(/\s+/g, ' ').trim(), w, '@' + a]); });
    });
  }
  return out;
};

async function seed(page) {
  await page.evaluate(seedFn);
  await page.waitForTimeout(300);
}

/* Περπατά τα πάντα· καλεί το take(where) σε κάθε στάση. */
async function walk(page, take) {
  const go = (js, arg) => page.evaluate(js, arg);
  const at = async (where, fn) => {
    try { await fn(); await page.waitForTimeout(150); await take(where); }
    catch (e) { if (process.env.WALK_VERBOSE) console.error('skip ' + where + ': ' + e.message); }
  };
  await at('trials', () => go(() => { S.view = 'trials'; S.trialId = null; render(); }));
  for (const tab of ['entries','terrains','draw','sms','braces','results','export'])
    await at('trial/' + tab, () => go(k => { S.view = 'trial'; S.trialId = 'T'; S.day = 0;
      S.tab = k; render(); }, tab));
  for (const rt of ['handlers','dogs','judges'])
    await at('registry/' + rt, () => go(k => { S.view = 'registry'; S.regTab = k; render(); }, rt));
  await at('dog',      () => go(() => { S.view = 'dog'; S.dogId = 'd0'; render(); }));
  await at('stats',    () => go(() => { S.view = 'stats'; S.stat = null; render(); }));
  await at('settings', () => go(() => { S.view = 'settings'; render(); }));
  await at('install',  () => go(() => { S.view = 'install'; render(); }));
  await at('terms',    () => go(() => { S.view = 'terms'; render(); }));

  const byBtn = [
    ['newTrial',   () => go(() => { S.view='trials'; render(); }), '[data-act="newTrial"]'],
    ['addEntry',   () => go(() => { S.view='trial'; S.trialId='T'; S.tab='entries'; render(); }),
                   '[data-act="addEntry"]'],
    ['newDog',     () => go(() => { S.view='registry'; S.regTab='dogs'; render(); }),
                   '[data-act="newDog"]'],
    ['newHandler', () => go(() => { S.regTab='handlers'; render(); }), '[data-act="newHandler"]'],
    ['newJudge',   () => go(() => { S.regTab='judges'; render(); }), '[data-act="newJudge"]'],
    ['lang',       () => go(() => { S.view='trials'; render(); }), '#langBtn'],
  ];
  for (const [name, pre, sel] of byBtn)
    await at('dlg/' + name, async () => {
      await page.evaluate(() => { try { closeDlg(); } catch (e) {} });
      await pre(); await page.waitForTimeout(120);
      const h = await page.$(sel);
      if (!h) throw new Error('no ' + sel);
      await h.click(); await page.waitForTimeout(180);
    });

  const byData = [['note','[data-note]'], ['swap','[data-swap]'], ['recall','[data-recall]'],
                  ['editdog','[data-editdog]'], ['edithandler','[data-edithandler]'],
                  ['editjudge','[data-editjudge]'], ['editterrain','[data-editterrain]'],
                  ['editentry','[data-editentry]'], ['bstat','[data-bstat]'],
                  ['smspick','[data-smspick]']];
  for (const [name, sel] of byData)
    await at('dlg/' + name, async () => {
      await page.evaluate(() => { try { closeDlg(); } catch (e) {} });
      for (const v of [['trial','braces'],['trial','results'],['trial','entries'],
                       ['trial','terrains'],['trial','sms'],['registry','dogs'],
                       ['registry','handlers'],['registry','judges']]) {
        await go(([view, tab]) => { S.view = view;
          if (view === 'trial') { S.trialId = 'T'; S.tab = tab; } else S.regTab = tab;
          render(); }, v);
        await page.waitForTimeout(100);
        const h = await page.$(sel);
        if (h) { await h.click({ force: true }); await page.waitForTimeout(200);
          if (await page.$('#dlg[open]')) return; }
      }
      throw new Error('nowhere to click ' + sel);
    });
  await page.evaluate(() => { try { closeDlg(); } catch (e) {} });
}

/* Περπατά και επιστρέφει τα πάντα μαζί. */
async function grabAll(page) {
  const all = [];
  await walk(page, async where => {
    (await page.evaluate(GRAB, where)).forEach(x => all.push(x));
  });
  return all;
}

module.exports = { seed, walk, grabAll, GRAB, DATA };
