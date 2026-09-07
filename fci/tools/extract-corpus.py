#!/usr/bin/env python3
"""Βγάζει το κείμενο κάθε κανονισμού σε corpus/, με σημάδι σελίδας.
Πρώτο βήμα: χωρίς αυτό, τα build-terms.py και check-terms.py δεν έχουν τι να ελέγξουν.
    python3 extract-corpus.py            # από τη ρίζα του αποθετηρίου
"""
import pypdfium2 as pdfium, glob, os
os.makedirs('corpus', exist_ok=True)
for f in sorted(glob.glob('fci/*.pdf') + glob.glob('national/*.pdf')):
    p = pdfium.PdfDocument(f)
    txt = "".join(f"\n␟[p{i+1}]␟\n{p[i].get_textpage().get_text_range()}" for i in range(len(p)))
    out = 'corpus/' + os.path.basename(f).replace('.pdf', '.txt')
    open(out, 'w', encoding='utf-8').write(txt)
    print(f"{os.path.basename(f):<42} {len(p):>3} σελ")
