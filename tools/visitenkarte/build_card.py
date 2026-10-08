"""Print-ready business card (design A, white paper) for Heenemann, as PDF/X-4.

Heenemann (Datenblatt Visitenkarten / allgemein):
  trim 85 x 55 mm, bleed 3 mm (91 x 61 mm), safety margin 4 mm, PDF/X-4,
  CMYK with output profile ISO Coated v2 (ECI), crop marks offset 3 mm,
  single pages in order (page 1 front, page 2 back), black text in K only,
  fonts embedded or outlined, lines >= 0.25 pt.

Text is shaped with HarfBuzz (kerning) and drawn as outlines, so no fonts are
embedded at all. Usage (see README.md):

  python build_card.py <fonts dir> <icc> <out.pdf>

The contact details come from kontakt.toml next to this script, and the phone
number from kontakt.local.toml (git-ignored), so it stays out of the public
repository. Without it, the card is built without a phone number.
"""
import datetime as dt
import io
import pathlib
import sys
import tomllib
import uuid

import pikepdf
import segno
import uharfbuzz as hb
from fontTools.pens.basePen import BasePen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from reportlab.pdfgen import canvas

FONTS, ICC, OUT = sys.argv[1:4]
# --no-marks: the page is the bleed format itself (91 x 61 mm), without crop
# marks. Online printers that show the uploaded page as their preview (such as
# Heenemann's) otherwise show the marks in it.
MARKS = "--no-marks" not in sys.argv[4:]
HERE = pathlib.Path(__file__).resolve().parent
CONTACT = tomllib.loads((HERE / "kontakt.toml").read_text())
if (HERE / "kontakt.local.toml").exists():
    CONTACT |= tomllib.loads((HERE / "kontakt.local.toml").read_text())
MM = 72 / 25.4

TRIM_W, TRIM_H = 85.0, 55.0
BLEED = 3.0
MARK_OFFSET, MARK_LEN = 3.0, 5.0
OFF = MARK_OFFSET + MARK_LEN if MARKS else BLEED   # trim edge inside the media box
MEDIA_W, MEDIA_H = TRIM_W + 2 * OFF, TRIM_H + 2 * OFF

# CMYK as 0..1. Petrol #00657f through ISO Coated v2 (ECI), relative colorimetric + BPC.
PETROL = (0.82, 0.31, 0.23, 0.37)
BLACK = (0, 0, 0, 1)          # text in K only, as Heenemann asks
GREY = (0, 0, 0, 0.70)        # the address, as #59615d in the design
WHITE = (0, 0, 0, 0)          # knockout: paper white


class FontInstance:
    def __init__(self, path, axes):
        tt = instantiateVariableFont(TTFont(path), axes)
        tt.flavor = None
        data = io.BytesIO()
        tt.save(data)
        self.tt = TTFont(io.BytesIO(data.getvalue()))
        self.glyphs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        face = hb.Face(hb.Blob(data.getvalue()))
        self.upem = face.upem
        self.hb = hb.Font(face)

    def shape(self, text, size, tracking=0.0):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True, "liga": True})
        scale = size / self.upem
        x, out = 0.0, []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            out.append((self.order[info.codepoint], x + pos.x_offset * scale, pos.y_offset * scale))
            x += pos.x_advance * scale + tracking * size
        return out, x - tracking * size, scale


class CanvasPen(BasePen):
    """Draws fontTools outlines into a reportlab path (quadratics become cubics)."""
    def __init__(self, glyphs, path):
        super().__init__(glyphs)
        self.p = path

    def _moveTo(self, pt): self.p.moveTo(*pt)
    def _lineTo(self, pt): self.p.lineTo(*pt)
    def _curveToOne(self, a, b, c): self.p.curveTo(*a, *b, *c)
    def _closePath(self): self.p.close()


def fill(c, cmyk):
    c.setFillColorCMYK(*cmyk)


def X(mm_from_trim_left): return (OFF + mm_from_trim_left) * MM
def Y(mm_from_trim_top): return (OFF + TRIM_H - mm_from_trim_top) * MM


def text(c, font, s, size_pt, x_mm, baseline_mm, cmyk, tracking=0.0):
    """Draw s with its left edge at x_mm and baseline at baseline_mm (from the trim's top)."""
    glyphs, width, scale = font.shape(s, size_pt, tracking)
    path = c.beginPath()
    for name, gx, gy in glyphs:
        pen = TransformPen(CanvasPen(font.glyphs, path), (scale, 0, 0, scale, X(x_mm) + gx, Y(baseline_mm) + gy))
        font.glyphs[name].draw(pen)
    fill(c, cmyk)
    c.drawPath(path, stroke=0, fill=1, fillMode=1)  # non-zero, as TrueType outlines expect
    return width / MM


def crop_marks(c):
    c.setStrokeColorCMYK(*BLACK)
    c.setLineWidth(0.25)
    for tx in (OFF, OFF + TRIM_W):
        for ty in (OFF, OFF + TRIM_H):
            hx = -1 if tx == OFF else 1
            vy = -1 if ty == OFF else 1
            # horizontal mark at the trim line, outside the bleed
            c.line(tx * MM + hx * MARK_OFFSET * MM, ty * MM, tx * MM + hx * OFF * MM, ty * MM)
            # vertical mark
            c.line(tx * MM, ty * MM + vy * MARK_OFFSET * MM, tx * MM, ty * MM + vy * OFF * MM)


def logo(c, x_mm, top_mm, d_mm):
    """The site logo: an M (Fraunces 500, opsz 48) knocked out of a petrol disc."""
    cx, cy, r = X(x_mm + d_mm / 2), Y(top_mm + d_mm / 2), d_mm / 2 * MM
    fill(c, PETROL)
    c.circle(cx, cy, r, stroke=0, fill=1)
    f = FontInstance(f"{FONTS}/fraunces-latin-standard-normal.woff2", {"wght": 500, "opsz": 48})
    name = f.tt.getBestCmap()[ord("M")]
    bp = BoundsPen(f.glyphs)
    f.glyphs[name].draw(bp)
    x0, y0, x1, y1 = bp.bounds
    s = 0.44 * d_mm * MM / (y1 - y0)       # same proportions as scripts/logo.py
    drop = 0.5 / 64 * d_mm * MM             # the M sits a hair below centre there too
    tx = cx - (x0 + x1) / 2 * s
    ty = cy - (y0 + y1) / 2 * s - drop
    path = c.beginPath()
    f.glyphs[name].draw(TransformPen(CanvasPen(f.glyphs, path), (s, 0, 0, s, tx, ty)))
    fill(c, WHITE)
    c.drawPath(path, stroke=0, fill=1, fillMode=1)


def qr(c, x_mm, top_mm, size_mm):
    """A QR code to the German homepage (2026-10-08: no vCard any more)."""
    code = segno.make(CONTACT["qr_url"], error="m", micro=False)
    rows = [list(r) for r in code.matrix]
    n = len(rows)
    m = size_mm / n
    fill(c, BLACK)
    for j, row in enumerate(rows):
        i = 0
        while i < n:
            if row[i]:
                k = i
                while k < n and row[k]:
                    k += 1
                c.rect(X(x_mm + i * m), Y(top_mm + (j + 1) * m), (k - i) * m * MM, m * MM, stroke=0, fill=1)
                i = k
            else:
                i += 1
    return code.version, n, m


def main():
    fraunces = lambda opsz: FontInstance(f"{FONTS}/fraunces-latin-standard-normal.woff2", {"wght": 400, "opsz": opsz})
    inter = lambda w: FontInstance(f"{FONTS}/inter-latin-wght-normal.woff2", {"wght": w})
    name_front, name_back, pitch_font = fraunces(27), fraunces(15), fraunces(12)
    inter400, inter500, inter600 = inter(400), inter(500), inter(600)

    raw = io.BytesIO()
    c = canvas.Canvas(raw, pagesize=(MEDIA_W * MM, MEDIA_H * MM), invariant=1)
    L = 5.5  # left/right margin in mm (Heenemann: >= 4 mm)

    # Page 1, front: logo top left; name and role bottom left. The role is
    # sized down until it fits the safe area (Heenemann: 4 mm from the trim).
    logo(c, L, 5.0, 7.5)
    text(c, name_front, CONTACT["name"], 20.25, L, 44.3, BLACK)
    role, size = CONTACT["role"], 8.0
    while inter600.shape(role, size, 0.08)[1] / MM > TRIM_W - 2 * L:
        size -= 0.1
    text(c, inter600, role, size, L, 49.5, PETROL, tracking=0.08)
    print(f"role at {size:.1f} pt")
    if MARKS:
        crop_marks(c)
    c.showPage()

    # Page 2, back: the pitch on top; contact left and the QR code right, both
    # bottom aligned. No address (2026-10-08).
    text(c, inter600, CONTACT["pitch_eyebrow"], 6.5, L, 9.6, PETROL, tracking=0.08)
    pitch_lines = CONTACT["pitch"]
    for i, line in enumerate(pitch_lines):
        w = text(c, pitch_font, line, 10.5, L, 15.0 + i * 4.6, BLACK)
        assert L + w < TRIM_W - L, f"pitch line runs out of the safe area: {line!r}"
    lead = 8.0 * 1.45 / MM  # 8 pt at line height 1.45, in mm
    gap = 2.65
    web = 49.5
    lines = [("email", inter400, BLACK)]
    if CONTACT.get("phone"):
        lines.append(("phone", inter400, BLACK))
    y = web - lead * len(lines)
    widths = []
    text(c, name_back, CONTACT["name"], 11.25, L, y - lead - gap + 0.6, BLACK)
    for key, font, colour in lines:
        widths.append(text(c, font, CONTACT[key], 8.0, L, y, colour))
        y += lead
    widths.append(text(c, inter500, CONTACT["web"], 8.0, L, web, PETROL))
    size = 18.0
    qx, qtop = TRIM_W - L - size, web + 0.5 - size
    version, n, module = qr(c, qx, qtop, size)
    if MARKS:
        crop_marks(c)
    c.showPage()
    c.save()
    w_email = w_addr = max(widths)
    assert L + max(w_email, w_addr) < qx - 3, "text runs into the QR code"
    print(f"QR version {version}, {n} modules of {module:.3f} mm; text column ends at {L + max(w_email, w_addr):.1f} mm, QR starts at {qx:.1f} mm")

    # PDF/X-4: version, page boxes, output intent with ISO Coated v2, XMP and Info.
    pdf = pikepdf.open(io.BytesIO(raw.getvalue()))
    for page in pdf.pages:
        # reportlab opens every page with an empty text block that selects
        # Helvetica (BT /F1 12 Tf … ET). Nothing is shown with it, but a
        # preflight reports the unembedded font, so drop it and the resource.
        kept, in_text = [], False
        for operands, op in pikepdf.parse_content_stream(page):
            if str(op) == "BT":
                in_text = True
            elif str(op) == "ET":
                in_text = False
            elif not in_text:
                kept.append((operands, op))
        page.Contents = pdf.make_stream(pikepdf.unparse_content_stream(kept))
        if "/Font" in page.Resources:
            del page.Resources.Font
        page.MediaBox = pikepdf.Array([0, 0, MEDIA_W * MM, MEDIA_H * MM])
        page.TrimBox = pikepdf.Array([OFF * MM, OFF * MM, (OFF + TRIM_W) * MM, (OFF + TRIM_H) * MM])
        page.BleedBox = pikepdf.Array([(OFF - BLEED) * MM, (OFF - BLEED) * MM,
                                       (OFF + TRIM_W + BLEED) * MM, (OFF + TRIM_H + BLEED) * MM])
    icc = pdf.make_stream(open(ICC, "rb").read())
    icc.N = 4
    icc.Alternate = pikepdf.Name.DeviceCMYK
    pdf.Root.OutputIntents = pikepdf.Array([pikepdf.Dictionary(
        Type=pikepdf.Name.OutputIntent, S=pikepdf.Name.GTS_PDFX,
        OutputConditionIdentifier="FOGRA39", RegistryName="http://www.color.org",
        OutputCondition="Offset commercial and specialty printing according to ISO 12647-2:2004 / Amd 1, OFCOM, paper type 1 or 2 = coated art",
        Info="ISO Coated v2 (ECI)", DestOutputProfile=icc)])

    now = dt.datetime.now(dt.timezone.utc).astimezone().replace(microsecond=0)
    iso = now.isoformat()
    pdfdate = now.strftime("D:%Y%m%d%H%M%S") + now.strftime("%z")[:3] + "'" + now.strftime("%z")[3:] + "'"
    title = "Visitenkarte Mitja Martini"
    doc_id, inst_id = uuid.uuid4(), uuid.uuid4()
    xmp = f"""<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:xmp="http://ns.adobe.com/xap/1.0/"
    xmlns:pdf="http://ns.adobe.com/pdf/1.3/"
    xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/"
    xmlns:pdfxid="http://www.npes.org/pdfx/ns/id/">
   <dc:format>application/pdf</dc:format>
   <dc:title><rdf:Alt><rdf:li xml:lang="x-default">{title}</rdf:li></rdf:Alt></dc:title>
   <dc:creator><rdf:Seq><rdf:li>Mitja Martini</rdf:li></rdf:Seq></dc:creator>
   <xmp:CreateDate>{iso}</xmp:CreateDate>
   <xmp:ModifyDate>{iso}</xmp:ModifyDate>
   <xmp:MetadataDate>{iso}</xmp:MetadataDate>
   <xmp:CreatorTool>build_card.py (reportlab, HarfBuzz, pikepdf)</xmp:CreatorTool>
   <pdf:Producer>reportlab + pikepdf</pdf:Producer>
   <pdf:Trapped>False</pdf:Trapped>
   <xmpMM:DocumentID>uuid:{doc_id}</xmpMM:DocumentID>
   <xmpMM:InstanceID>uuid:{inst_id}</xmpMM:InstanceID>
   <xmpMM:VersionID>1</xmpMM:VersionID>
   <xmpMM:RenditionClass>default</xmpMM:RenditionClass>
   <pdfxid:GTS_PDFXVersion>PDF/X-4</pdfxid:GTS_PDFXVersion>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>"""
    meta = pdf.make_stream(xmp.encode("utf-8"))
    meta.Type = pikepdf.Name.Metadata
    meta.Subtype = pikepdf.Name.XML
    pdf.Root.Metadata = meta
    pdf.trailer.Info = pikepdf.Dictionary(
        Title=title, Author="Mitja Martini", Creator="build_card.py (reportlab, HarfBuzz, pikepdf)",
        Producer="reportlab + pikepdf", CreationDate=pdfdate, ModDate=pdfdate,
        Trapped=pikepdf.Name("/False"), GTS_PDFXVersion="PDF/X-4")
    pdf.save(OUT, min_version="1.6", force_version="1.6", compress_streams=True)


main()
