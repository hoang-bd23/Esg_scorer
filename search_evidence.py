# -*- coding: utf-8 -*-
import os, sys
import pdfplumber

def search():
    folder = 'company evaluation document'
    files = [f for f in os.listdir(folder) if f.endswith('.pdf')]
    for f in files:
        if "SAM" not in f:
            continue
        path = os.path.join(folder, f)
        print("Checking", f)
        try:
            with pdfplumber.open(path) as pdf:
                # Print page 23, 24, 25 (0-indexed 22, 23, 24)
                for i in [22, 23, 24]:
                    p = pdf.pages[i]
                    text = p.extract_text(x_tolerance=2, y_tolerance=3) or ""
                    print(f"--- PAGE {p.page_number} ---")
                    print(text[:200])
                    
        except Exception as e:
            print("Error", f, e)

if __name__ == "__main__":
    search()
