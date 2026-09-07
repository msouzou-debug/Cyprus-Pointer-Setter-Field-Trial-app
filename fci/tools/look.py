#!/usr/bin/env python3
"""Ψάχνει έναν όρο στα σώματα κειμένου και δίνει σελίδα + άρθρο + συμφραζόμενα."""
import re, sys, glob, os

LANG = {
 'en': ['FCI-ABR-REG-S-C-en', 'FCI-ABR-REG-GQU-en', 'FCI-ACO-REG-en-2019', 'FCI-REG-TIT-en-2024'],
 'fr': ['SCC-CUNCA-reglement-FT-fr-2026', 'SCC-lexique-travail-fr', 'FCI-ACO-REG-fr-2011'],
 'de': ['VPS-Pruefungsordnung-de-2026', 'FCI-ACO-REG-de-2019'],
 'it': ['ENCI-prove-razze-da-ferma-it-2026'],
}

def load(stem):
    p = f'corpus/{stem}.txt'
    return open(p, encoding='utf-8').read() if os.path.exists(p) else ''

def article_at(txt, pos):
    """the nearest article heading above this position"""
    head = txt[:pos]
    m = None
    for m2 in re.finditer(r'(?:ART(?:ICLE|\.)?|Art\.|Artikel|§)\s*\.?\s*(\d+[a-z]?)', head, re.I):
        m = m2
    return ('art. ' + m.group(1)) if m else ''

def page_at(txt, pos):
    m = None
    for m2 in re.finditer(r'␟\[p(\d+)\]␟', txt[:pos]):
        m = m2
    return m.group(1) if m else '?'

def look(term, langs=None, width=150, limit=6):
    rx = re.compile(term, re.I)
    for lang in (langs or LANG):
        for stem in LANG[lang]:
            txt = load(stem)
            hits = list(rx.finditer(txt))
            if not hits: continue
            print(f"\n=== [{lang}] {stem} — {len(hits)} ===")
            for h in hits[:limit]:
                a, b = max(0, h.start()-width), min(len(txt), h.end()+width)
                ctx = re.sub(r'\s+', ' ', txt[a:b]).replace('␟','')
                print(f"  p{page_at(txt,h.start())} {article_at(txt,h.start())}: …{ctx}…")

if __name__ == '__main__':
    look(sys.argv[1], sys.argv[2:] or None)
