#!/usr/bin/env python3
"""Build the wallpaper landing pages and sitemap from the app's catalog.

Each page targets a wallpaper search (Ahrefs, US, Nov 2026):
  art wallpaper 3.5K/mo · wallpaper art 1.4K · painting wallpaper 1.1K
  starry night wallpaper 1.2K · van gogh wallpaper 500 · renaissance wallpaper 500
  monet wallpaper 450 · great wave wallpaper 150 · japanese art wallpaper 200
  klimt wallpaper 100
All have keyword difficulty 0-3. The results are mostly peel-and-stick wallpaper shops,
so a page that actually serves phone and Mac wallpapers matches the intent better.

Titles, dates, museums, licenses and download links come from curated_catalog.json, so
the pages never promise a painting the app doesn't have. Preview thumbnails are made from
the CDN's portrait crop and cached in images/wallpapers/.

    python3 tools/build_pages.py [--catalog PATH]
"""
import argparse, datetime, html, json, os, subprocess, sys

from PIL import Image

SITE = "https://dailycanvasapp.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CATALOG = os.path.join(os.path.dirname(ROOT), "Artpapers", "ArtpapersKit", "Sources",
                               "ArtpapersKit", "Resources", "curated_catalog.json")
APP_URL = "https://apps.apple.com/us/app/daily-canvas/id6792569506"
CATALOG_COUNT = "3,500+"
THUMB_W = 480

# id -> (short display title or None, one-line note). Notes are written by hand.
NOTES = {
    # Van Gogh
    "wikimedia-Q45585": (None, "Painted in June 1889 at the asylum in Saint-Rémy, from the view out of his east-facing window before sunrise."),
    "wikimedia-Q3365921": (None, "Arles at night in September 1888: gaslight on the river and the Plough overhead, painted on the spot."),
    "wikimedia-Q846341": (None, "His first painting with a starry sky, set on the Place du Forum in Arles in September 1888."),
    "wikimedia-Q152509": (None, "One of the sunflower still lifes he painted in Arles in August 1888 to decorate the room for Gauguin's visit."),
    "met-436528": (None, "One of two still lifes of irises painted in May 1890, days before he left Saint-Rémy."),
    "met-436535": (None, "Painted outdoors in July 1889; Van Gogh counted it among his best summer canvases."),
    "aic-28560": (None, "The second of three versions of his bedroom in the Yellow House in Arles."),
    "nga-163323": (None, "Painted in Auvers-sur-Oise in the last weeks of his life, in 1890."),
    # Monet
    "wikimedia-Q208230": (None, "The harbor of Le Havre in 1872: the painting that gave Impressionism its name."),
    "aic-97933": (None, "A late canvas of the pond Monet built and painted at Giverny for the last three decades of his life."),
    "aic-87088": (None, "The Japanese footbridge over his water garden at Giverny, painted in 1900."),
    "cleveland-136510": (None, "A panel from the vast water lily cycle Monet worked on through the 1910s and 1920s."),
    "aic-4783": (None, "A poppy field near his house at Giverny, 1890–91."),
    "aic-64818": (None, "From the series that showed one subject in changing light and season, 1890–91."),
    "aic-14620": (None, "Two figures on the Normandy cliffs above the sea, 1882."),
    "aic-103139": (None, "From his London series, painted from a window of the Savoy Hotel."),
    # Klimt
    "wikimedia-Q209755": (None, "The high point of his golden period, with gold leaf laid into the oil paint."),
    "wiki-klimt-farm-garden-with-sunflowers": (None, "One of the square landscapes he painted on summer holidays at the Attersee."),
    "wiki-klimt-birch-forest-birkenwald": (None, "A square landscape of birch trunks on a carpet of fallen leaves."),
    "wiki-klimt-attersee": (None, "The Austrian lake where he spent his summers, painted as an almost abstract field of water."),
    "wiki-klimt-hope-ii": (None, "A pregnant woman in a gold-patterned robe, 1907–08, now at MoMA."),
    "wiki-klimt-pallas-athene": (None, "The goddess of wisdom as the emblem of the Vienna Secession."),
    "wiki-klimt-death-and-life": (None, "An allegory he reworked for five years, from 1910 to 1915."),
    "met-436819": ("Mäda Primavesi", "Portrait of the nine-year-old daughter of his patrons, 1912–13."),
    # Japanese prints
    "met-45434": ("The Great Wave off Kanagawa", "A wave about to break over three boats, with Mount Fuji small in the distance."),
    "met-55736": ("South Wind, Clear Sky (Red Fuji)", "Fuji lit red by early autumn sun, from the same series as the Great Wave."),
    "met-57006": ("Storm below Mount Fuji", "Lightning strikes the foot of the mountain while the summit stays clear."),
    "met-39800": ("Kajikazawa in Kai Province", "A fisherman on a rock above a churning river."),
    "met-55022": ("The Amida Falls", "From Hokusai's series A Tour of Waterfalls in Various Provinces."),
    "met-55433": ("Sudden Shower over Shin-Ōhashi Bridge", "Hiroshige's rain-soaked bridge, which Van Gogh copied in oil in 1887."),
    "met-37093": ("Fireworks at Ryōgoku Bridge", "From Hiroshige's One Hundred Famous Views of Edo."),
    "met-56915": ("Evening Snow at Kanbara", "From Hiroshige's Fifty-three Stations of the Tōkaidō."),
    # Renaissance
    "wikimedia-Q81689": (None, "Venus arrives on a shell, blown ashore by the winds."),
    "wikimedia-Q184212": (None, "Botticelli's allegory of spring, with hundreds of identifiable plants underfoot."),
    "wikimedia-Q12418": (None, "Leonardo's portrait of Lisa Gherardini, which he kept working on for years."),
    "wikimedia-Q128910": (None, "The mural on the refectory wall of Santa Maria delle Grazie in Milan."),
    "wikimedia-Q175036": (None, "Raphael's fresco of the ancient philosophers, in the Vatican's papal apartments."),
    "wikimedia-Q122953": (None, "The fresco at the center of the Sistine Chapel ceiling."),
    "wikimedia-Q29473": (None, "Home of the two cherubs at the bottom edge, among the most copied details in art."),
    "nga-28": (None, "A small panel from about 1506 of the knight and the dragon."),
    # Hub extras
    "wikimedia-Q81087": (None, "Vermeer's study of a girl in a turban and a single pearl."),
    "wikimedia-Q321816": (None, "A lone figure on a crag above the fog: the emblem of Romanticism."),
    "aic-27992": ("A Sunday on La Grande Jatte", "Seurat spent two years building the scene from small dots of color."),
    "wikimedia-Q736882": (None, "A warship towed up the Thames to be broken up, at sunset."),
}

PAGES = [
    dict(
        slug="art-wallpaper",
        title="Art Wallpaper: Famous Paintings for iPhone and Mac",
        h1="Art wallpaper from the world's great museums",
        description="Free art wallpapers for iPhone and Mac: Starry Night, The Kiss, The Great Wave and more, cropped to fit your screen. Or get a new masterpiece every morning.",
        lede=("Famous paintings make the best wallpapers: they were composed to be looked at every day. "
              "Every image here is a public-domain masterpiece from a museum's open-access collection, "
              "already cropped for an iPhone lock screen and a Mac desktop. Download one free, or let "
              f"Daily Canvas set a new one from {CATALOG_COUNT} works every morning."),
        ids=["wikimedia-Q45585", "wikimedia-Q209755", "met-45434", "wikimedia-Q81689",
             "wikimedia-Q81087", "wikimedia-Q321816", "wikimedia-Q208230", "aic-27992",
             "wikimedia-Q846341", "aic-87088", "wikimedia-Q736882", "wikimedia-Q12418"],
        crumb="Art wallpaper",
        hero="wikimedia-Q45585",
    ),
    dict(
        slug="van-gogh-wallpaper",
        title="Van Gogh Wallpaper: Starry Night and More for iPhone and Mac",
        h1="Van Gogh wallpaper",
        description="Free Van Gogh wallpapers for iPhone and Mac: The Starry Night, Café Terrace at Night, Sunflowers, Irises and more, cropped to fit your screen.",
        lede=("The Starry Night is the most requested painting wallpaper there is, and Van Gogh's "
              "swirling skies and thick color hold up beautifully on a phone. These are his best-known "
              "works from Arles, Saint-Rémy and Auvers, each cropped for an iPhone lock screen and a "
              "Mac desktop."),
        ids=["wikimedia-Q45585", "wikimedia-Q3365921", "wikimedia-Q846341", "wikimedia-Q152509",
             "met-436528", "met-436535", "aic-28560", "nga-163323"],
        crumb="Van Gogh",
        hero="wikimedia-Q45585",
        artist="Vincent van Gogh",
    ),
    dict(
        slug="monet-wallpaper",
        title="Monet Wallpaper: Water Lilies and More for iPhone and Mac",
        h1="Monet wallpaper",
        description="Free Claude Monet wallpapers for iPhone and Mac: Water Lilies, Impression, Sunrise, the Japanese footbridge and more, cropped to fit your screen.",
        lede=("Monet's soft light and open water make calm, readable wallpapers: your clock and "
              "widgets sit easily on top of them. Here are Impression, Sunrise, the Giverny water "
              "lilies and more, each cropped for an iPhone lock screen and a Mac desktop."),
        ids=["wikimedia-Q208230", "aic-97933", "aic-87088", "cleveland-136510",
             "aic-4783", "aic-64818", "aic-14620", "aic-103139"],
        crumb="Monet",
        hero="aic-87088",
        artist="Claude Monet",
    ),
    dict(
        slug="klimt-wallpaper",
        title="Klimt Wallpaper: The Kiss and More for iPhone and Mac",
        h1="Klimt wallpaper",
        description="Free Gustav Klimt wallpapers for iPhone and Mac: The Kiss, Hope II, the Attersee landscapes and more, cropped to fit your screen.",
        lede=("Klimt's gold and pattern were made for a glowing screen. Alongside The Kiss are the "
              "square lake and forest landscapes he painted in the summers, which work especially "
              "well behind iPhone widgets."),
        ids=["wikimedia-Q209755", "wiki-klimt-farm-garden-with-sunflowers",
             "wiki-klimt-birch-forest-birkenwald", "wiki-klimt-attersee", "wiki-klimt-hope-ii",
             "wiki-klimt-pallas-athene", "wiki-klimt-death-and-life", "met-436819"],
        crumb="Klimt",
        hero="wikimedia-Q209755",
        artist="Gustav Klimt",
    ),
    dict(
        slug="great-wave-wallpaper",
        title="The Great Wave Wallpaper and Japanese Art for iPhone and Mac",
        h1="The Great Wave and Japanese art wallpaper",
        description="Free Japanese art wallpapers for iPhone and Mac: Hokusai's Great Wave off Kanagawa, Red Fuji and Hiroshige's views of Edo, cropped to fit your screen.",
        lede=("Japanese woodblock prints were designed with flat color and strong outlines, so they "
              "stay crisp at any size. Here are Hokusai's Great Wave and Red Fuji alongside Hiroshige's "
              "rain, snow and fireworks, from the Metropolitan Museum's open-access collection."),
        ids=["met-45434", "met-55736", "met-57006", "met-39800", "met-55022",
             "met-55433", "met-37093", "met-56915"],
        crumb="Great Wave",
        hero="met-45434",
        artist="Katsushika Hokusai",
    ),
    dict(
        slug="renaissance-wallpaper",
        title="Renaissance Wallpaper: Botticelli, Leonardo and Raphael",
        h1="Renaissance wallpaper",
        description="Free Renaissance art wallpapers for iPhone and Mac: The Birth of Venus, the Mona Lisa, The School of Athens, The Creation of Adam and more.",
        lede=("The Renaissance gave us the most recognizable images in Western art. Here are "
              "Botticelli, Leonardo, Michelangelo and Raphael, each cropped around the faces and "
              "figures that matter so they survive the lock screen clock."),
        ids=["wikimedia-Q81689", "wikimedia-Q184212", "wikimedia-Q12418", "wikimedia-Q128910",
             "wikimedia-Q175036", "wikimedia-Q122953", "wikimedia-Q29473", "nga-28"],
        crumb="Renaissance",
        hero="wikimedia-Q81689",
    ),
]

FAQ_COMMON = [
    ("Are these wallpapers free to download?",
     "Yes. Every painting here is in the public domain or released under CC0 by the museum that "
     "holds it, so you can download and use it as your wallpaper for free."),
    ("How do I set a painting as my iPhone wallpaper?",
     "Tap iPhone under the painting and save the image to Photos. Then open Settings, tap "
     "Wallpaper, tap Add New Wallpaper, choose Photos and pick the painting. The download is "
     "already 1290 × 2796, the size of a large iPhone screen."),
    ("How do I set a painting as my Mac desktop?",
     "Tap Mac under the painting to download it, then right-click the file in Finder and choose "
     "Set Desktop Picture. The Mac download is 3456 × 2234, cropped for a MacBook Pro display."),
    ("Can my iPhone wallpaper change to a new painting every day?",
     "Yes. Daily Canvas, a free app, picks a new painting each morning and sets it as your "
     "wallpaper. On iPhone it uses a Shortcuts automation that takes about 30 seconds to set up "
     "once; on Mac it changes your desktop on its own."),
]

HUB_SLUG = "art-wallpaper"


def esc(s):
    return html.escape(s or "", quote=True)


def load_catalog(path):
    with open(path) as f:
        return {p["id"]: p for p in json.load(f)["paintings"]}


def fetch(url, out):
    # curl, not urllib: the CDN's bot protection refuses Python's default user agent.
    subprocess.run(["curl", "-sfL", "-o", out, url], check=True)


def save_jpeg(img, out, quality):
    img.convert("RGB").save(out, "JPEG", quality=quality, optimize=True, progressive=True)


def thumb(p):
    """Download the portrait crop once and shrink it to a web preview."""
    rel = f"images/wallpapers/{p['id']}.jpg"
    out = os.path.join(ROOT, rel)
    if not os.path.exists(out):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        tmp = out + ".full"
        fetch(p["images"]["portrait"], tmp)
        with Image.open(tmp) as im:
            h = round(im.height * THUMB_W / im.width)
            save_jpeg(im.resize((THUMB_W, h), Image.LANCZOS), out, 70)
        os.remove(tmp)
    with Image.open(out) as im:
        return "/" + rel, im.width, im.height


def og_image(p, slug):
    rel = f"images/og/{slug}.jpg"
    out = os.path.join(ROOT, rel)
    if not os.path.exists(out):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        tmp = out + ".full"
        fetch(p["images"]["landscape"], tmp)
        with Image.open(tmp) as im:
            # The landscape crop is 16:9 around the focal point; trim to 1200x630 at the center.
            im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
            top = (im.height - 630) // 2
            save_jpeg(im.crop((0, top, 1200, top + 630)), out, 78)
        os.remove(tmp)
    return f"{SITE}/{rel}"


def title_of(p):
    short = NOTES.get(p["id"], (None, ""))[0]
    return short or p["title"]


def year_of(p):
    return (p.get("year") or "").replace("-", "–")


def license_label(p):
    return "CC0" if (p.get("license") or "").upper() == "CC0" else "Public domain"


APPLE_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.8-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/></svg>')
LOGO_SVG = ('<svg class="logo-mark" viewBox="0 0 43 26" aria-hidden="true"><path fill-rule="evenodd" d="M21.5 3.164A13 13 0 1 1 21.5 22.836A13 13 0 1 1 21.5 3.164ZM7.55 6H12.05A7 7 0 0 1 12.05 20H7.55ZM10.55 9V17H12.05A4 4 0 0 0 12.05 9ZM35.554 8.34A7.25 7.25 0 1 0 35.554 17.66L33.256 15.732A4.25 4.25 0 1 1 33.256 10.268Z"/></svg>')

GA = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-Z7CVLJXFN3"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-Z7CVLJXFN3');
    </script>"""


def card(p, eager=False):
    src, w, h = thumb(p)
    t = title_of(p)
    artist = p["artist"]["name"]
    note = NOTES.get(p["id"], (None, ""))[1]
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f"""      <figure class="card">
        <img src="{src}" width="{w}" height="{h}" {loading} decoding="async" alt="{esc(t)} by {esc(artist)}, {esc(year_of(p))}, as an iPhone wallpaper">
        <figcaption>
          <h3>{esc(t)}</h3>
          <p class="meta">{esc(artist)} · {esc(year_of(p))}</p>
          <p class="meta">{esc(p['museum'])} · {license_label(p)}</p>
          <p class="note">{esc(note)}</p>
          <p class="dl"><a href="{esc(p['images']['portrait'])}" download>iPhone</a><a href="{esc(p['images']['macLandscape'])}" download>Mac</a><a href="{esc(p['images']['iPadPortrait'])}" download>iPad</a></p>
        </figcaption>
      </figure>"""


def artwork_ld(p):
    return {
        "@type": "VisualArtwork",
        "name": title_of(p),
        "creator": {"@type": "Person", "name": p["artist"]["name"]},
        "dateCreated": year_of(p),
        "artMedium": p.get("medium") or None,
        "image": p["images"]["portrait"],
        "license": ("https://creativecommons.org/publicdomain/zero/1.0/"
                    if license_label(p) == "CC0" else "https://creativecommons.org/publicdomain/mark/1.0/"),
        "locationCreated": None,
        "isPartOf": {"@type": "Museum", "name": p["museum"]},
    }


def clean(d):
    if isinstance(d, dict):
        return {k: clean(v) for k, v in d.items() if v not in (None, "")}
    if isinstance(d, list):
        return [clean(v) for v in d]
    return d


def page_html(page, cat, all_pages):
    url = f"{SITE}/{page['slug']}"
    works = [cat[i] for i in page["ids"]]
    og = og_image(cat[page["hero"]], page["slug"])
    faq = list(FAQ_COMMON)
    if page.get("artist"):
        bio = next((p["artist"].get("biography") for p in works
                    if p["artist"]["name"] == page["artist"] and p["artist"].get("biography")), None)
    else:
        bio = None

    cards = "\n".join(card(p, eager=(n < 2)) for n, p in enumerate(works))
    others = [pg for pg in all_pages if pg["slug"] not in (page["slug"],)]
    related = "\n".join(f'        <li><a href="/{pg["slug"]}">{esc(pg["h1"])}</a></li>' for pg in others)

    crumbs = [("Daily Canvas", SITE + "/")]
    if page["slug"] != HUB_SLUG:
        crumbs.append(("Art wallpaper", f"{SITE}/{HUB_SLUG}"))
    crumbs.append((page["crumb"], url))
    crumb_html = " <span aria-hidden=\"true\">/</span> ".join(
        f'<a href="{u.replace(SITE, "") or "/"}">{esc(n)}</a>' if i < len(crumbs) - 1 else f'<span aria-current="page">{esc(n)}</span>'
        for i, (n, u) in enumerate(crumbs))

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "CollectionPage", "@id": url, "url": url, "name": page["title"],
             "description": page["description"], "inLanguage": "en",
             "isPartOf": {"@id": f"{SITE}/#website"},
             "about": {"@type": "Person", "name": page["artist"]} if page.get("artist") else None,
             "primaryImageOfPage": og,
             "mainEntity": {"@type": "ItemList", "numberOfItems": len(works),
                            "itemListElement": [{"@type": "ListItem", "position": n + 1, "item": artwork_ld(p)}
                                                for n, p in enumerate(works)]}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": n + 1, "name": nm, "item": u} for n, (nm, u) in enumerate(crumbs)]},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
        ],
    }
    faq_html = "\n".join(f"""      <details>
        <summary>{esc(q)}</summary>
        <p>{esc(a)}</p>
      </details>""" for q, a in faq)

    bio_html = (f"""
    <section class="band">
      <h2>About {esc(page['artist'])}</h2>
      <p>{esc(bio)}</p>
    </section>""" if bio else "")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    {GA}
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(page['title'])}</title>
    <meta name="description" content="{esc(page['description'])}">
    <link rel="canonical" href="{url}">
    <meta name="theme-color" content="#0A0A0A">
    <meta name="apple-itunes-app" content="app-id=6792569506">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Daily Canvas">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{esc(page['title'])}">
    <meta property="og:description" content="{esc(page['description'])}">
    <meta property="og:image" content="{og}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/images/apple-touch-icon.png">
    <link rel="preconnect" href="https://cdn.dailycanvasapp.com">
    <link rel="stylesheet" href="/wallpapers.css">
    <script type="application/ld+json">{json.dumps(clean(ld), ensure_ascii=False)}</script>
</head>
<body>
  <nav>
    <a href="/" class="nav-logo">{LOGO_SVG}Daily Canvas</a>
    <a href="{APP_URL}" class="btn">{APPLE_SVG}<span>App Store</span></a>
  </nav>

  <main>
    <header class="intro">
      <p class="crumbs">{crumb_html}</p>
      <h1>{esc(page['h1'])}</h1>
      <p class="lede">{esc(page['lede'])}</p>
    </header>

    <section class="grid" aria-label="Wallpapers">
{cards}
    </section>

    <section class="band daily">
      <h2>Or wake up to a new one every morning</h2>
      <p>Daily Canvas picks one painting a day from {CATALOG_COUNT} public-domain masterpieces in the styles you choose, crops it around what matters, and sets it as your wallpaper. On Mac it changes your desktop by itself. On iPhone a 30-second Shortcuts setup does it each morning. It also fills your widgets, Apple Watch face and Apple TV. Free, with Pro at $9.99 a year for unlimited shuffles and full-collection search.</p>
      <a href="{APP_URL}" class="btn btn-large">{APPLE_SVG}<span>Download Daily Canvas</span></a>
    </section>
{bio_html}
    <section class="band">
      <h2>Questions</h2>
{faq_html}
    </section>

    <section class="band">
      <h2>More painting wallpapers</h2>
      <ul class="related">
{related}
      </ul>
    </section>
  </main>

  <footer>
    <p><a href="/">Daily Canvas</a> · <a href="/art-wallpaper">Art wallpaper</a> · <a href="/privacy">Privacy</a> · <a href="/terms">Terms</a> · <a href="mailto:support@dailycanvasapp.com">Support</a></p>
    <p class="fine">Images courtesy of the museums named on each painting, from their open-access collections.</p>
  </footer>
</body>
</html>
"""


def write_sitemap(slugs):
    today = datetime.date.today().isoformat()
    urls = ["", *slugs, "privacy", "terms"]
    body = "\n".join(f"  <url>\n    <loc>{SITE}/{u}</loc>\n    <lastmod>{today}</lastmod>\n  </url>" for u in urls)
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", default=DEFAULT_CATALOG)
    args = ap.parse_args()
    cat = load_catalog(args.catalog)
    missing = [i for pg in PAGES for i in pg["ids"] if i not in cat]
    if missing:
        sys.exit(f"Not in catalog: {missing}")
    for pg in PAGES:
        with open(os.path.join(ROOT, pg["slug"] + ".html"), "w") as f:
            f.write(page_html(pg, cat, PAGES))
        print("wrote", pg["slug"] + ".html")
    write_sitemap([pg["slug"] for pg in PAGES])
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
