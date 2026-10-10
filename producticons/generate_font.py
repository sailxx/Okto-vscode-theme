from pathlib import Path

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen


ROOT = Path(__file__).parent
UPM = 1000


def glyph(contours):
    pen = TTGlyphPen(None)
    for points in contours:
        pen.moveTo(points[0])
        for point in points[1:]:
            pen.lineTo(point)
        pen.closePath()
    return pen.glyph()


def rect(x1, y1, x2, y2):
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]


def line(x1, y1, x2, y2, width=76):
    # Horizontal and vertical Okto strokes as compact filled bars.
    if x1 == x2:
        return rect(x1 - width // 2, min(y1, y2), x1 + width // 2, max(y1, y2))
    if y1 == y2:
        return rect(min(x1, x2), y1 - width // 2, max(x1, x2), y1 + width // 2)
    # Diagonal strokes use a deliberate stair-step silhouette at icon scale.
    d = width // 2
    if (x2 - x1) * (y2 - y1) > 0:
        return [(x1-d,y1),(x1+d,y1-2*d),(x2+d,y2-2*d),(x2+d,y2),(x2-d,y2+2*d),(x1-d,y1+2*d)]
    return [(x1-d,y1),(x1+d,y1+2*d),(x2+d,y2+2*d),(x2+d,y2),(x2-d,y2-2*d),(x1-d,y1-2*d)]


def octo_tile():
    # The chamfered modular tile mark anchors every product glyph.
    return [[(150,80),(570,80),(920,430),(920,850),(500,850),(150,500)]]


icons = {
    "okto-files": [rect(255,220,650,780), rect(400,120,745,680), line(475,560,670,560,52), line(475,450,670,450,52)],
    "okto-search": [rect(170,570,645,645), rect(565,170,640,390)],
    "okto-source": [rect(230,650,770,730), rect(460,300,540,690), rect(460,170,540,260), rect(720,480,800,650), rect(200,300,280,470), rect(680,380,760,460)],
    "okto-run": [rect(230,230,330,770), [(330,230),(800,500),(330,770)]],
    "okto-extensions": [rect(365,160,635,840), rect(160,365,840,635), rect(230,230,365,365), rect(635,635,770,770)],
    "okto-beaker": [rect(410,690,590,810), rect(360,260,640,340), line(420,340,270,650,64), line(580,340,730,650,64), rect(280,610,720,690)],
    "okto-python": [rect(220,520,560,820), rect(440,180,780,480), rect(440,440,560,560), rect(360,340,440,440), rect(560,560,640,660)],
    "okto-spark": [rect(455,130,545,870), rect(130,455,870,545), line(230,230,770,770,65), line(230,770,770,230,65)],
    "okto-settings": [rect(455,150,545,850), rect(150,455,850,545), rect(250,280,750,360), rect(250,640,750,720)],
    "okto-account": [rect(360,600,640,840), rect(380,190,620,470)],
}

glyph_order = [".notdef"] + list(icons)
glyphs = {".notdef": glyph([])}
metrics = {".notdef": (1000, 0)}
for name, contours in icons.items():
    glyphs[name] = glyph(contours)
    metrics[name] = (1000, 0)

fb = FontBuilder(UPM, isTTF=True)
fb.setupGlyphOrder(glyph_order)
fb.setupCharacterMap({0xE000 + i: name for i, name in enumerate(icons)})
fb.setupGlyf(glyphs)
fb.setupHorizontalMetrics(metrics)
fb.setupHorizontalHeader(ascent=900, descent=-100)
fb.setupNameTable({
    "familyName": "Okto Product Icons",
    "styleName": "Regular",
    "uniqueFontIdentifier": "OktoProductIcons-Regular",
    "fullName": "Okto Product Icons Regular",
    "psName": "OktoProductIcons-Regular",
    "version": "Version 1.0",
})
fb.setupOS2(sTypoAscender=900, sTypoDescender=-100, usWinAscent=900, usWinDescent=100)
fb.setupPost()
fb.setupMaxp()
font = fb.font
font.flavor = "woff"
font.save(ROOT / "fonts" / "okto-product-icons.woff")
