# Visitenkarte

Print-ready business card (85 × 55 mm, 3 mm bleed, crop marks, CMYK, PDF/X-4 with ISO Coated v2) for
Heenemann's same-day business cards, built by `build_card.py`. Text is shaped with HarfBuzz and drawn as
outlines, so no fonts are embedded.

| file | |
|---|---|
| `build_card.py` | the card: front (logo, name, role), back (PaaSbox pitch, contact, QR code to the German homepage) |
| `kontakt.toml` | the texts and contact details |
| `kontakt.local.toml` | git-ignored: `phone = "+49 …"`, so the number stays out of the public repository |

Build:

```sh
python3 -m venv /tmp/card-venv
/tmp/card-venv/bin/pip install reportlab pikepdf fonttools brotli uharfbuzz segno
curl -sSLo /tmp/eci.zip https://www.eci.org/lib/exe/eci_offset_2009.zip
unzip -o -j /tmp/eci.zip "*ISOcoated_v2_eci.icc" -d /tmp/icc
/tmp/card-venv/bin/python build_card.py <repo>/themes/paasbox/static/fonts /tmp/icc/ISOcoated_v2_eci.icc Visitenkarte_Mitja_Martini_85x55_PDFX4.pdf
```

Add `--no-marks` for a page of exactly the bleed format (91 × 61 mm, trim 3 mm inside, no crop marks).
This is the variant to upload when the printer's preview shows the page as it is, crop marks included:
`Visitenkarte_Mitja_Martini_85x55_PDFX4_ohne-Schnittmarken.pdf`.

The fonts are Fraunces and Inter from the paasbox theme (`themes/paasbox/static/fonts`, OFL). The script
prints the size the role line needed to fit the 4 mm safe area and where the QR code sits.

History: version 1 (2026-10-06) said "AI Engineer · Berlin" with the address and a vCard QR code.
Version 2 (2026-10-08) says "KI-automatisierter Betrieb · Berlin", carries the PaaSbox pitch on the back,
drops the address, and the QR code opens https://mitjamartini.com/de/.
