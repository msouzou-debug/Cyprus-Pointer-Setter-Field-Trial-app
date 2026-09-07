#!/usr/bin/env python3
"""Ελέγχει ότι κάθε όρος του γλωσσαρίου υπάρχει όντως στο έγγραφο που επικαλείται.

Δεν ελέγχει το άρθρο — ελέγχει το πιο βασικό: ότι η λέξη στέκει μέσα στο κείμενο
της συγκεκριμένης γλώσσας. Ένας όρος που δεν βρίσκεται πουθενά είναι είτε
τυπογραφικό δικό μου, είτε εικασία που ξέφυγε.
"""
import json, re, unicodedata, sys

DOC = {  # συντομογραφία πηγής -> αρχεία σώματος
 'ACO':  {'en':['FCI-ACO-REG-en-2019'], 'fr':['FCI-ACO-REG-fr-2011'], 'de':['FCI-ACO-REG-de-2019']},
 'SC':   {'en':['FCI-ABR-REG-S-C-en']},
 'GQ':   {'en':['FCI-ABR-REG-GQU-en']},
 'TIT':  {'en':['FCI-REG-TIT-en-2024']},
 'SCC':  {'fr':['SCC-CUNCA-reglement-FT-fr-2026']},
 'LEX':  {'fr':['SCC-lexique-travail-fr']},
 'VPS':  {'de':['VPS-Pruefungsordnung-de-2026']},
 'ENCI': {'it':['ENCI-prove-razze-da-ferma-it-2026']},
}
CACHE = {}
def body(stem):
    if stem not in CACHE:
        t = open(f'corpus/{stem}.txt', encoding='utf-8').read()
        t = re.sub(r'␟\[p\d+\]␟', ' ', t)
        CACHE[stem] = re.sub(r'\s+', ' ', t).lower()
    return CACHE[stem]

def norm(s):
    """πεζά, ενιαία κενά, και τα τυπογραφικά εισαγωγικά σαν απλά"""
    s = s.lower().replace('’', "'").replace('‘', "'").replace('ß', 'ss')
    return re.sub(r'\s+', ' ', s).strip()

d = json.load(open('fci/terms-5lang.json'))
bad, checked, skipped = [], 0, 0
for t in d['terms']:
    for lang in ('en', 'fr', 'de', 'it'):
        e = t[lang]
        if not e: continue
        stems = []
        for tag in set(re.findall(r'\b(ACO|SC|GQ|TIT|SCC|LEX|VPS|ENCI)\b', e['src'])):
            stems += DOC.get(tag, {}).get(lang, [])
        if not stems: skipped += 1; continue
        checked += 1
        # κάθε παραλλαγή χωριστά: «brace, couple» -> «brace» ή «couple»
        variants = [norm(v) for v in re.split(r'[,/]| ή ', e['q']) if norm(v)]
        corpus = ' ¶ '.join(norm(body(s)) for s in stems)
        if not any(v in corpus for v in variants):
            bad.append((t['el'], lang, e['q'], e['src'], stems))

print(f"ελέγχθηκαν {checked} όροι σε σώμα κειμένου · {skipped} χωρίς αντιστοιχισμένη πηγή")
if bad:
    print(f"\n{len(bad)} ΔΕΝ ΒΡΕΘΗΚΑΝ:")
    for el, l, term, src, st in bad:
        print(f"  [{l}] {el:<32} «{term}»  ← {src}  ({', '.join(st)})")
else:
    print("\n✓ κάθε όρος στέκει μέσα στο έγγραφο που επικαλείται")
sys.exit(1 if bad else 0)
