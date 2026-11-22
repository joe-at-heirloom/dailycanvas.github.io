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

It also builds two editorial guides for informational searches, from hand-written entries:
/famous-paintings ("famous paintings", 157K/mo, KD 9) from tools/famous_paintings.py and
/art-movements ("art movements", 6.4K/mo, KD 24) from tools/art_movements.py.
And it builds the artist pages (/artists/, "famous artists" 109K/mo, KD 2, and a page per artist)
from tools/artists.py, the museum guides (/museums/) from tools/museums.py, and the period pages
(/art-movements/<slug>) from tools/periods.py.

    python3 tools/build_pages.py [--catalog PATH]
"""
import argparse, datetime, hashlib, html, json, os, re, subprocess, sys

from PIL import Image

from concurrent.futures import ThreadPoolExecutor

import art_movements as am
import artists as ar
import famous_paintings as fp
import museums as mu
import periods as pe

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


def painting_thumb(p):
    """The whole painting (not a wallpaper crop), longest side 640px, for the guide."""
    rel = f"images/paintings/{p['id']}.jpg"
    out = os.path.join(ROOT, rel)
    if not os.path.exists(out):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        tmp = out + ".full"
        fetch(p["images"]["display"], tmp)
        with Image.open(tmp) as im:
            im.thumbnail((640, 640), Image.LANCZOS)
            save_jpeg(im, out, 74)
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

    a_page = ARTIST_BY_NAME.get(page.get("artist") or "")
    more = (f'\n      <p class="dl"><a href="/artists/{a_page["slug"]}" class="more">{esc(a_page["name"])}: life, {a_page.get("works_word", "paintings")} and where to see them</a></p>'
            if a_page else "")
    bio_html = (f"""
    <section class="band">
      <h2>About {esc(page['artist'])}</h2>
      <p>{esc(bio)}</p>{more}
    </section>""" if bio else "")

    return f"""{head_html(page['title'], page['description'], url, og, ld)}

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

{FOOTER}"""


# Busts the day-long cache on wallpapers.css (see _headers) whenever the stylesheet changes.
with open(os.path.join(ROOT, "wallpapers.css"), "rb") as _f:
    CSS_VERSION = hashlib.sha1(_f.read()).hexdigest()[:8]


def head_html(title, description, url, og, ld, og_type="website"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    {GA}
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(description)}">
    <link rel="canonical" href="{url}">
    <meta name="theme-color" content="#0A0A0A">
    <meta name="apple-itunes-app" content="app-id=6792569506">
    <meta property="og:type" content="{og_type}">
    <meta property="og:site_name" content="Daily Canvas">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{esc(title)}">
    <meta property="og:description" content="{esc(description)}">
    <meta property="og:image" content="{og}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/images/apple-touch-icon.png">
    <link rel="preconnect" href="https://cdn.dailycanvasapp.com">
    <link rel="stylesheet" href="/wallpapers.css?v={CSS_VERSION}">
    <script type="application/ld+json">{json.dumps(clean(ld), ensure_ascii=False)}</script>
</head>
<body>
  <nav>
    <a href="/" class="nav-logo">{LOGO_SVG}Daily Canvas</a>
    <a href="{APP_URL}" class="btn">{APPLE_SVG}<span>App Store</span></a>
  </nav>"""


FOOTER = """  <footer>
    <p><a href="/">Daily Canvas</a> · <a href="/art-wallpaper">Art wallpaper</a> · <a href="/famous-paintings">Famous paintings</a> · <a href="/art-movements">Art movements</a> · <a href="/artists/">Famous artists</a> · <a href="/museums/">Art museums</a> · <a href="/privacy">Privacy</a> · <a href="/terms">Terms</a> · <a href="mailto:support@dailycanvasapp.com">Support</a></p>
    <p class="fine">Images courtesy of the museums named on each painting, from their open-access collections.</p>
  </footer>
</body>
</html>
"""

GUIDE_SLUG = "famous-paintings"
PAGE_NAMES = {pg["slug"]: pg for pg in PAGES}


def slugify(s):
    s = html.unescape(s).lower().replace("'", "")
    s = s.translate(str.maketrans("àáâäãåçèéêëìíîïñòóôöõùúûüý", "aaaaaaceeeeiiiinooooouuuuy"))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def guide_html(cat):
    url = f"{SITE}/{GUIDE_SLUG}"
    entries = [e for _, _, es in fp.SECTIONS for e in es]
    n_works = len(entries)
    title = f"Famous Paintings: {n_works} Masterpieces and Where to See Them"
    h1 = f"Famous paintings: {n_works} masterpieces everyone should know"
    description = (f"The world's most famous paintings, from the Mona Lisa to The Starry Night: {n_works} "
                   "masterpieces with the artist, date, museum and the story behind each one.")
    og = og_image(cat["wikimedia-Q12418"], GUIDE_SLUG)

    def wp_link(e):
        slug = e.get("wp", HUB_SLUG)
        pg = PAGE_NAMES[slug]
        label = "More art wallpapers" if slug == HUB_SLUG else f"More {pg['crumb']} wallpapers"
        return f'<a href="/{slug}" class="more">{esc(label)}</a>'

    def work(e, pos):
        p = cat[e["id"]]
        src, w, h = painting_thumb(p)
        anchor = slugify(e["t"])
        loading = 'fetchpriority="high"' if pos <= 2 else 'loading="lazy"'
        return f"""        <article class="work" id="{anchor}">
          <img src="{src}" width="{w}" height="{h}" {loading} decoding="async" alt="{esc(e['t'])} by {esc(e['a'])}, {esc(e['y'])}">
          <div>
            <h3><span class="num">{pos}.</span> {esc(e['t'])}</h3>
            <p class="meta">{artist_link(e['a'])} · {esc(e['y'])} · {esc(e['m'])}</p>
            <p class="meta">{esc(e['at'])}</p>
            <p class="note">{esc(e['n'])}</p>
            <p class="dl"><a href="{esc(p['images']['portrait'])}" download>iPhone wallpaper</a><a href="{esc(p['images']['macLandscape'])}" download>Mac wallpaper</a>{wp_link(e)}</p>
          </div>
        </article>"""

    pos = 0
    sections, toc = [], []
    for heading, intro, es in fp.SECTIONS:
        sid = slugify(heading.split(",")[0])
        toc.append(f'        <li><a href="#{sid}">{esc(heading)}</a></li>')
        items = []
        for e in es:
            pos += 1
            items.append(work(e, pos))
        sections.append(f"""    <section class="era" id="{sid}">
      <h2>{esc(heading)}</h2>
      <p class="era-intro">{esc(intro)}</p>
{chr(10).join(items)}
    </section>""")

    crumbs = [("Daily Canvas", SITE + "/"), ("Famous paintings", url)]
    lede = (f"{fp.INTRO} Below are {n_works} of the world's most famous paintings in date order: who painted each one, when, where you can see it today and why it "
            "matters. Every one is in the public domain, so each also comes as a free iPhone and Mac wallpaper.")

    def artwork(e, n):
        p = cat[e["id"]]
        src, _, _ = painting_thumb(p)
        return {"@type": "ListItem", "position": n, "url": f"{url}#{slugify(e['t'])}",
                "item": {"@type": "VisualArtwork", "name": e["t"],
                         "creator": {"@type": "Person", "name": e["a"]},
                         "dateCreated": e["y"], "artMedium": e["m"],
                         "artform": "Print" if "print" in e["m"].lower() else "Painting",
                         "image": SITE + src, "description": e["n"],
                         "isPartOf": {"@type": "Museum", "name": e["at"]}}}

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "@id": url, "url": url, "headline": h1, "name": title,
             "description": description, "inLanguage": "en", "image": og,
             "dateModified": datetime.date.today().isoformat(),
             "isPartOf": {"@id": f"{SITE}/#website"},
             "publisher": {"@id": f"{SITE}/#org"},
             "mainEntity": {"@type": "ItemList", "name": "Famous paintings", "numberOfItems": n_works,
                            "itemListOrder": "https://schema.org/ItemListOrderAscending",
                            "itemListElement": [artwork(e, n + 1) for n, e in enumerate(entries)]}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": n + 1, "name": nm, "item": u} for n, (nm, u) in enumerate(crumbs)]},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fp.FAQ]},
        ],
    }
    faq_html = "\n".join(f"""      <details>
        <summary>{esc(q)}</summary>
        <p>{esc(a)}</p>
      </details>""" for q, a in fp.FAQ)
    related = "\n".join(f'        <li><a href="/{pg["slug"]}">{esc(pg["h1"])}</a></li>' for pg in PAGES)
    related += f'\n        <li><a href="/{MOVEMENTS_SLUG}">Art movements: a timeline</a></li>'

    return f"""{head_html(title, description, url, og, ld, og_type="article")}

  <main class="guide">
    <header class="intro">
      <p class="crumbs"><a href="/">Daily Canvas</a> <span aria-hidden="true">/</span> <span aria-current="page">Famous paintings</span></p>
      <h1>{esc(h1)}</h1>
      <p class="lede">{esc(lede)}</p>
      <nav class="toc" aria-label="Periods">
        <ul>
{chr(10).join(toc)}
        </ul>
      </nav>
    </header>

{chr(10).join(sections)}

    <section class="band daily">
      <h2>See a different masterpiece every morning</h2>
      <p>Daily Canvas sets one painting a day as your wallpaper, chosen from {CATALOG_COUNT} public-domain works including every painting on this page, and tells you the story behind it. On Mac it changes your desktop by itself; on iPhone a 30-second Shortcuts setup does it each morning. Free, with Pro at $9.99 a year for unlimited shuffles and full-collection search.</p>
      <a href="{APP_URL}" class="btn btn-large">{APPLE_SVG}<span>Download Daily Canvas</span></a>
    </section>

    <section class="band">
      <h2>Questions</h2>
{faq_html}
    </section>

    <section class="band">
      <h2>Painting wallpapers</h2>
      <ul class="related">
{related}
      </ul>
    </section>
  </main>

{FOOTER}"""


MOVEMENTS_SLUG = "art-movements"


def famous_anchors():
    return {e["id"]: slugify(e["t"]) for _, _, es in fp.SECTIONS for e in es}


def movements_html(cat):
    url = f"{SITE}/{MOVEMENTS_SLUG}"
    mv = am.MOVEMENTS
    title = "Art Movements: A Timeline from the Renaissance to Pop Art"
    h1 = "Art movements: a timeline from the Renaissance to Pop Art"
    description = (f"The major art movements in order, with dates, key artists, how to recognize each one "
                   f"and examples: {len(mv)} movements from the Renaissance and Baroque to Impressionism, "
                   "Cubism and Pop Art.")
    og = og_image(cat["wikimedia-Q208230"], MOVEMENTS_SLUG)
    anchors = famous_anchors()

    rows = "\n".join(f"""          <tr><th scope="row"><a href="#{m['slug']}">{esc(m['name'])}</a></th><td>{esc(m['dates'])}</td><td>{esc(m['where'])}</td></tr>""" for m in mv)

    def example(x, eager):
        i, t, a, y, at = x
        src, w, h = painting_thumb(cat[i])
        name = esc(t)
        if i in anchors:
            name = f'<a href="/{GUIDE_SLUG}#{anchors[i]}">{name}</a>'
        loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
        museum = f'<br>{esc(at)}' if at else ""
        return f"""          <figure>
            <img src="{src}" width="{w}" height="{h}" {loading} decoding="async" alt="{esc(t)} by {esc(a)}, {esc(y)}">
            <figcaption><strong>{name}</strong><br>{esc(a)}, {esc(y)}{museum}</figcaption>
          </figure>"""

    blocks = []
    for n, m in enumerate(mv):
        if m["ex"]:
            figs = "\n".join(example(x, n == 0 and k < 2) for k, x in enumerate(m["ex"]))
            figs = f"""        <div class="examples">
{figs}
        </div>"""
        else:
            figs = '        <p class="no-ex">Works from this movement are still under copyright, so none are shown here.</p>'
        wp = ""
        if m.get("wp"):
            pg = PAGE_NAMES[m["wp"]]
            wp = f'\n        <p class="dl"><a href="/{pg["slug"]}" class="more">{esc(pg["crumb"])} wallpapers for iPhone and Mac</a></p>'
        blocks.append(f"""      <section class="movement" id="{m['slug']}">
        <h2>{esc(m['name'])}</h2>
        <p class="meta">{esc(m['dates'])} · {esc(m['where'])}</p>
        <p>{esc(m['d'])}</p>
        <p><strong>Key artists:</strong> {esc(m['artists'])}.</p>{movement_artists(m['slug'])}
        <p><strong>How to recognize it:</strong> {esc(m['look'])}</p>
{figs}{wp}{period_link(m)}
      </section>""")

    crumbs = [("Daily Canvas", SITE + "/"), ("Art movements", url)]
    lede = (f"{am.INTRO} Below is a timeline of {len(mv)} movements with their dates, where they "
            "happened, the artists who defined them, how to recognize them and public-domain examples.")
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "@id": url, "url": url, "headline": h1, "name": title,
             "description": description, "inLanguage": "en", "image": og,
             "dateModified": datetime.date.today().isoformat(),
             "isPartOf": {"@id": f"{SITE}/#website"}, "publisher": {"@id": f"{SITE}/#org"},
             "mainEntity": {"@type": "ItemList", "name": "Art movements", "numberOfItems": len(mv),
                            "itemListOrder": "https://schema.org/ItemListOrderAscending",
                            "itemListElement": [
                                {"@type": "ListItem", "position": n + 1, "url": f"{url}#{m['slug']}",
                                 "item": {"@type": "DefinedTerm", "name": m["name"],
                                          "description": f"{m['dates']}, {m['where']}. {m['d']}",
                                          "inDefinedTermSet": url}}
                                for n, m in enumerate(mv)]}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": n + 1, "name": nm, "item": u} for n, (nm, u) in enumerate(crumbs)]},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in am.FAQ]},
        ],
    }
    faq_html = "\n".join(f"""      <details>
        <summary>{esc(q)}</summary>
        <p>{esc(a)}</p>
      </details>""" for q, a in am.FAQ)
    related = "\n".join(f'        <li><a href="/{pg["slug"]}">{esc(pg["h1"])}</a></li>' for pg in PAGES)

    return f"""{head_html(title, description, url, og, ld, og_type="article")}

  <main class="guide">
    <header class="intro">
      <p class="crumbs"><a href="/">Daily Canvas</a> <span aria-hidden="true">/</span> <span aria-current="page">Art movements</span></p>
      <h1>{esc(h1)}</h1>
      <p class="lede">{esc(lede)}</p>
    </header>

    <section class="timeline" aria-label="Timeline">
      <div class="table-wrap">
        <table>
          <thead><tr><th scope="col">Movement</th><th scope="col">Dates</th><th scope="col">Where</th></tr></thead>
          <tbody>
{rows}
          </tbody>
        </table>
      </div>
    </section>

    <div class="movements">
{chr(10).join(blocks)}
    </div>

    <section class="band">
      <h2>See the famous paintings</h2>
      <p>For the individual masterpieces behind these movements, from the Mona Lisa to The Starry Night, read our guide to <a href="/{GUIDE_SLUG}">47 famous paintings and where to see them</a>.</p>
    </section>

    <section class="band daily">
      <h2>A different movement every morning</h2>
      <p>Daily Canvas sets one painting a day as your wallpaper, chosen from {CATALOG_COUNT} public-domain works in the styles you pick, from Renaissance and Baroque to Impressionism, Japanese prints and early abstraction, and tells you the story behind it. On Mac it changes your desktop by itself; on iPhone a 30-second Shortcuts setup does it each morning. Free, with Pro at $9.99 a year for unlimited shuffles and full-collection search.</p>
      <a href="{APP_URL}" class="btn btn-large">{APPLE_SVG}<span>Download Daily Canvas</span></a>
    </section>

    <section class="band">
      <h2>Questions</h2>
{faq_html}
    </section>

    <section class="band">
      <h2>Painting wallpapers</h2>
      <ul class="related">
{related}
      </ul>
    </section>
  </main>

{FOOTER}"""


# ---------------------------------------------------------------------------------------------
# Artist pages and museum guides
# ---------------------------------------------------------------------------------------------

RELIABLE = {"met", "aic", "nga", "cleveland", "smithsonian", "smk"}  # records from the museum's own open data
SOURCE_ORDER = {"aic": 0, "met": 1, "nga": 2, "cleveland": 3, "smithsonian": 4, "smk": 5}
MAX_WORKS = 20
FAMOUS = {e["id"]: e for _, _, es in fp.SECTIONS for e in es}
ARTIST_BY_NAME = {}
for _a in ar.ARTISTS:
    for _n in [_a["name"], *_a["names"]]:
        ARTIST_BY_NAME[_n] = _a
MOVEMENT_NAMES = {m["slug"]: m["name"] for m in am.MOVEMENTS}
TITLES = {**{i: t for a in ar.ARTISTS for i, t in a.get("titles", {}).items()}, **pe.TITLES}

# The catalog's museum names, with the city where it isn't already in the name.
MUSEUM_DISPLAY = {
    "The Metropolitan Museum of Art": "The Metropolitan Museum of Art, New York",
    "Metropolitan Museum of Art": "The Metropolitan Museum of Art, New York",
    "National Gallery of Art": "National Gallery of Art, Washington, DC",
    "Smithsonian American Art Museum": "Smithsonian American Art Museum, Washington, DC",
    "Hirshhorn Museum and Sculpture Garden": "Hirshhorn Museum and Sculpture Garden, Washington, DC",
    "National Museum of Asian Art": "National Museum of Asian Art, Washington, DC",
    "Rijksmuseum": "Rijksmuseum, Amsterdam",
    "Mauritshuis": "Mauritshuis, The Hague",
    "Gemäldegalerie Alte Meister": "Gemäldegalerie Alte Meister, Dresden",
    "The Frick Collection": "The Frick Collection, New York",
    "Galleria Borghese": "Galleria Borghese, Rome",
    "Uffizi Gallery": "Uffizi Galleries, Florence",
    "Vatican Museums": "Vatican Museums, Vatican City",
    "National Gallery of Ireland": "National Gallery of Ireland, Dublin",
    "Galleria Nazionale d'Arte Antica": "Palazzo Barberini, Rome",
    "Tate Britain": "Tate Britain, London",
    "Yale Center for British Art": "Yale Center for British Art, New Haven",
    "Leopold Museum": "Leopold Museum, Vienna",
    "Wien Museum": "Wien Museum, Vienna",
    "Österreichische Galerie Belvedere": "Belvedere, Vienna",
    "Národní Galerie Praha": "National Gallery Prague",
    "Private Collection": "Private collection",
    "Museum of Modern Art": "Museum of Modern Art, New York",
}


def artist_link(name):
    a = ARTIST_BY_NAME.get(name)
    return f'<a href="/artists/{a["slug"]}">{esc(name)}</a>' if a else esc(name)


def movement_artists(slug):
    found = [a for a in ar.ARTISTS if slug in a["movements"]]
    if not found:
        return ""
    links = ", ".join(f'<a href="/artists/{a["slug"]}">{esc(a["name"])}</a>' for a in found)
    return f"\n        <p><strong>Artist pages:</strong> {links}.</p>"


def year_key(y):
    m = re.search(r"\d{4}", y or "")
    return int(m.group()) if m else 9999


def norm_year(y):
    y = (y or "").strip().strip("()")
    y = re.sub(r"\s*\(.*$", "", y)          # "1857 (Ansei 4), 2nd month" -> "1857"
    y = re.sub(r"^ca\.\s*", "c. ", y)
    if "month" in y and re.search(r"\d{4}", y):   # Japanese print dates: "dated 11th month, Ox year, 1853"
        y = re.findall(r"\d{4}", y)[-1]
    return y.replace("-", "–")


def lifespan_like(y):
    ys = [int(v) for v in re.findall(r"\d{4}", y or "")]
    return len(ys) >= 2 and ys[-1] - ys[0] > 40   # an artist's dates, not a work's


def clean_title(p, a):
    t = a.get("titles", {}).get(p["id"]) or TITLES.get(p["id"]) or p["title"]
    t = t.replace("“", "").replace("”", "")
    t = re.sub(r"\s*\[(obverse|reverse)\]", "", t)
    t = re.sub(r"\s*\(obverse:[^)]*\)", "", t)
    t = re.sub(r"\s*\(died[^)]*\)", "", t)
    t = re.sub(r"\s*\([^)]*\d{4}[^)]*\)", "", t)          # sitters' life dates
    if a.get("works_word") == "prints":
        t = re.sub(r"\s*\([^)]*\)", "", t)                  # romanized Japanese titles
    t = re.sub(r"\s+,", ",", t)
    return re.sub(r"\s{2,}", " ", t).strip().rstrip(",")


def work_info(p, a=None):
    """Title, year, place and medium for display: hand-checked entries first, then the museum's record."""
    if p["id"] in FAMOUS:
        e = FAMOUS[p["id"]]
        return dict(t=e["t"], y=e["y"], at=e["at"], m=e["m"])
    if p["id"] in ar.EXTRA:
        return dict(ar.EXTRA[p["id"]])
    a = a or ARTIST_BY_NAME.get(p["artist"]["name"], {})
    medium = p.get("medium") if p["source"] in RELIABLE and not p["source"] == "smk" else None
    return dict(t=clean_title(p, a), y=norm_year(p.get("year")),
                at=MUSEUM_DISPLAY.get(p["museum"], p["museum"]),
                m=(medium[:1].upper() + medium[1:]) if medium else None)


def trusted(p):
    return p["source"] in RELIABLE or p["id"].startswith("wiki-") or p["id"] in FAMOUS or p["id"] in ar.EXTRA


def select_works(a, cat):
    names = set(a["names"])
    pool = [p for p in cat.values() if p["artist"]["name"] in names and trusted(p)
            and p["id"] not in a.get("exclude", ())]
    pool = [p for p in pool if p["id"] in FAMOUS or p["id"] in ar.EXTRA
            or (p.get("year") and not lifespan_like(p["year"]))]
    if a.get("max_year"):
        pool = [p for p in pool if year_key(work_info(p, a)["y"]) <= a["max_year"]]
    must = {i: n for n, i in enumerate(a["must"])}

    def rank(p):
        i = p["id"]
        return (0 if i in must else 1, must.get(i, 0), 0 if i in FAMOUS else 1,
                0 if p.get("curatorHighlight") else 1, SOURCE_ORDER.get(p["source"], 9), i)

    chosen, keys = [], []
    for p in sorted(pool, key=rank):
        info = work_info(p, a)
        k = (re.sub(r"[^a-z0-9]", "", info["t"].lower()), year_key(info["y"]))
        if any(k[1] == y and (k[0] == t or (min(len(k[0]), len(t)) >= 20 and (k[0].startswith(t) or t.startswith(k[0]))))
               for t, y in keys):
            continue   # the same work from two sources, or two impressions of one print
        keys.append(k)
        chosen.append(p)
        if len(chosen) == MAX_WORKS:
            break
    return sorted(chosen, key=lambda p: (year_key(work_info(p, a)["y"]), p["id"]))


def lifespan(a):
    b, d = re.search(r"\d{4}", a["born"]).group(), re.search(r"\d{4}", a["died"]).group()
    return f"{'c. ' if a['born'].startswith('c.') else ''}{b}–{d}"


def faq_block(faq):
    return "\n".join(f"""      <details>
        <summary>{esc(q)}</summary>
        <p>{esc(a)}</p>
      </details>""" for q, a in faq)


def faq_ld(faq):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


def crumbs_ld(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": n + 1, "name": nm, "item": u} for n, (nm, u) in enumerate(crumbs)]}


def crumbs_html(crumbs):
    return " <span aria-hidden=\"true\">/</span> ".join(
        f'<a href="{u.replace(SITE, "") or "/"}">{esc(n)}</a>' if i < len(crumbs) - 1 else f'<span aria-current="page">{esc(n)}</span>'
        for i, (n, u) in enumerate(crumbs))


DAILY_BAND = f"""    <section class="band daily">
      <h2>A masterpiece on your wallpaper, every morning</h2>
      <p>Daily Canvas sets one painting a day as your iPhone and Mac wallpaper, chosen from {CATALOG_COUNT} public-domain works in the styles you pick, including every painting on this page, and tells you the story behind it. On Mac it changes your desktop by itself; on iPhone a 30-second Shortcuts setup does it each morning. Free, with Pro at $9.99 a year for unlimited shuffles and full-collection search.</p>
      <a href="{APP_URL}" class="btn btn-large">{APPLE_SVG}<span>Download Daily Canvas</span></a>
    </section>"""


def unique_ids(titles):
    seen, out = {}, []
    for t in titles:
        base = slugify(t) or "work"
        seen[base] = seen.get(base, 0) + 1
        out.append(base if seen[base] == 1 else f"{base}-{seen[base]}")
    return out


def work_card(p, info, anchor, eager, note=None, show_artist=False, artist_name=None):
    src, w, h = painting_thumb(p)
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    artist = artist_name or (p["artist"]["name"] if p["id"] not in FAMOUS else FAMOUS[p["id"]]["a"])
    a_page = ARTIST_BY_NAME.get(artist)
    shown_artist = a_page["name"] if a_page else artist
    who = f'{artist_link(shown_artist)} · ' if show_artist else ""
    guide = (f'<a href="/{GUIDE_SLUG}#{slugify(FAMOUS[p["id"]]["t"])}" class="more">In the famous paintings guide</a>'
             if p["id"] in FAMOUS else "")
    note_html = f'\n            <p class="note">{esc(note)}</p>' if note else ""
    return f"""          <figure class="wcard" id="{anchor}">
            <img src="{src}" width="{w}" height="{h}" {loading} decoding="async" alt="{esc(info['t'])} by {esc(shown_artist)}, {esc(info['y'])}">
            <figcaption>
              <h3>{esc(info['t'])}</h3>
              <p class="meta">{who}{esc(info['y'])}</p>
              <p class="meta">{esc(info['at'])}</p>{note_html}
              <p class="dl"><a href="{esc(p['images']['portrait'])}" download>iPhone</a><a href="{esc(p['images']['macLandscape'])}" download>Mac</a>{guide}</p>
            </figcaption>
          </figure>"""


def artwork_entry(p, info, artist_name, page_url, anchor, n):
    src, _, _ = painting_thumb(p)
    return {"@type": "ListItem", "position": n, "url": f"{page_url}#{anchor}",
            "item": {"@type": "VisualArtwork", "name": info["t"],
                     "creator": {"@type": "Person", "name": artist_name},
                     "dateCreated": info["y"], "artMedium": info.get("m"),
                     "image": SITE + src, "isPartOf": {"@type": "Museum", "name": info["at"]}
                     if info["at"] != "Private collection" else None}}


def artist_html(a, cat, works):
    url = f"{SITE}/artists/{a['slug']}"
    ww = a.get("works_word", "paintings")
    n = len(works)
    title = f"{a['name']} {ww.capitalize()}: {n} Works, Life and Where to See Them"
    h1 = f"{a['name']}: {ww}, life and where to see them"
    description = (f"{n} {ww} by {a['name']} with their dates and museums, the story of {a['pron']} life, "
                   f"and where to see {a['pron']} work today.")
    og = og_image(cat[a["must"][0]], f"artist-{a['slug']}")
    infos = [work_info(p, a) for p in works]
    anchors = unique_ids([i["t"] for i in infos])
    cards = "\n".join(work_card(p, i, an, k < 3) for k, (p, i, an) in enumerate(zip(works, infos, anchors)))

    fam_titles = {e["t"]: slugify(e["t"]) for e in FAMOUS.values() if ARTIST_BY_NAME.get(e["a"]) is a}
    known = ", ".join(f'<a href="/{GUIDE_SLUG}#{fam_titles[t]}">{esc(t)}</a>' if t in fam_titles else esc(t)
                      for t in a["known"])
    movements = ", ".join(f'<a href="{movement_href(m)}">{esc(MOVEMENT_NAMES[m])}</a>' for m in a["movements"])
    wp = PAGE_NAMES[a.get("wp") or HUB_SLUG]
    wp_label = "Art wallpapers" if wp["slug"] == HUB_SLUG else f"{wp['crumb']} wallpapers"

    counts = {}
    for i in infos:
        if i["at"] != "Private collection":
            counts[i["at"]] = counts.get(i["at"], 0) + 1
    here = "; ".join(f"{esc(m)} ({c})" for m, c in sorted(counts.items(), key=lambda x: (-x[1], x[0])))

    group = [b for b in ar.ARTISTS if b["group"] == a["group"] and b is not a]
    related = "\n".join(f'        <li><a href="/artists/{b["slug"]}">{esc(b["name"])}</a></li>' for b in group)
    related += f'\n        <li><a href="/artists/">All famous artists</a></li>'
    related += f'\n        <li><a href="/{GUIDE_SLUG}">Famous paintings</a></li>'
    related += f'\n        <li><a href="/{MOVEMENTS_SLUG}">Art movements</a></li>'

    crumbs = [("Daily Canvas", SITE + "/"), ("Famous artists", f"{SITE}/artists/"), (a["name"], url)]
    person = {"@type": "Person", "name": a["name"], "birthDate": a["birth"], "deathDate": a["death"],
              "nationality": a["nationality"], "description": a["lede"], "url": url}
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": url, "url": url, "headline": h1, "name": title, "description": description,
         "inLanguage": "en", "image": og, "dateModified": datetime.date.today().isoformat(),
         "isPartOf": {"@id": f"{SITE}/#website"}, "publisher": {"@id": f"{SITE}/#org"}, "about": person,
         "mainEntity": {"@type": "ItemList", "name": f"{ww.capitalize()} by {a['name']}", "numberOfItems": n,
                        "itemListElement": [artwork_entry(p, i, a["name"], url, an, k + 1)
                                            for k, (p, i, an) in enumerate(zip(works, infos, anchors))]}},
        crumbs_ld(crumbs), faq_ld(a["faq"])]}
    life = "\n".join(f"      <p>{esc(x)}</p>" for x in a["life"])
    note = f'\n      <p class="no-ex">{esc(a["note"])}</p>' if a.get("note") else ""

    return f"""{head_html(title, description, url, og, ld, og_type="article")}

  <main class="guide">
    <header class="intro">
      <p class="crumbs">{crumbs_html(crumbs)}</p>
      <h1>{esc(h1)}</h1>
      <p class="lede">{esc(a['lede'])}</p>
      <dl class="facts">
        <div><dt>Born</dt><dd>{esc(a['born'])}</dd></div>
        <div><dt>Died</dt><dd>{esc(a['died'])}</dd></div>
        <div><dt>Nationality</dt><dd>{esc(a['nationality'])}</dd></div>
        <div><dt>Movement</dt><dd>{movements}</dd></div>
        <div><dt>Known for</dt><dd>{known}</dd></div>
        <div><dt>Wallpapers</dt><dd><a href="/{wp['slug']}">{esc(wp_label)}</a></dd></div>
      </dl>
    </header>

    <section class="band">
      <h2>Life</h2>
{life}
    </section>

    <section class="artist-works">
      <h2>{n} {ww} by {esc(a['short'])}</h2>
      <p class="era-intro">In date order, with where each one is today. Every one can be downloaded free as an iPhone or Mac wallpaper.</p>
      <div class="works-grid">
{cards}
      </div>{note}
    </section>

    <section class="band">
      <h2>Where to see {esc(a['short'])}'s work</h2>
      <p>{esc(a['see'])}</p>
      <p class="small">The {ww} on this page: {here}.</p>
    </section>

    <section class="band">
      <h2>Questions</h2>
{faq_block(a['faq'])}
    </section>

{DAILY_BAND}

    <section class="band">
      <h2>More famous artists</h2>
      <ul class="related">
{related}
      </ul>
    </section>
  </main>

{FOOTER}"""


def artists_index_html(cat, picks):
    url = f"{SITE}/artists/"
    n = len(ar.ARTISTS)
    title = f"Famous Artists: {n} Great Painters, Their Lives and Their Paintings"
    h1 = f"Famous artists: {n} painters everyone should know"
    description = (f"The world's most famous artists, from Botticelli and Caravaggio to Monet, Van Gogh and Matisse: "
                   f"{n} great painters with their lives, their best-known paintings and where to see them.")
    og = og_image(cat["wikimedia-Q45585"], "famous-artists")
    lede = ("The most famous artists in history include Leonardo da Vinci, Michelangelo, Rembrandt, Vincent van Gogh, "
            "Claude Monet, Pablo Picasso and Frida Kahlo. This guide covers "
            f"{n} great painters whose work is in the public domain, from Botticelli and Caravaggio to Monet, Van Gogh "
            "and Matisse, each with their life, their best-known paintings and where to see them.")
    groups = []
    for a in ar.ARTISTS:
        if a["group"] not in groups:
            groups.append(a["group"])
    toc = "\n".join(f'        <li><a href="#{slugify(g)}">{esc(g)}</a></li>' for g in groups)
    sections = []
    first = True
    for g in groups:
        cards = []
        for a in sorted([a for a in ar.ARTISTS if a["group"] == g], key=lambda a: year_key(a["born"])):
            p = cat[a["must"][0]]
            src, w, h = painting_thumb(p)
            loading = 'fetchpriority="high"' if first else 'loading="lazy"'
            first = False
            mv = ", ".join(MOVEMENT_NAMES[m] for m in a["movements"])
            known = a["known"]
            known_s = known[0] if len(known) == 1 else ", ".join(known[:-1]) + " and " + known[-1]
            cards.append(f"""          <a class="acard" href="/artists/{a['slug']}">
            <img src="{src}" width="{w}" height="{h}" {loading} decoding="async" alt="{esc(work_info(p, a)['t'])} by {esc(a['name'])}">
            <span class="aname">{esc(a['name'])}</span>
            <span class="meta">{esc(lifespan(a))} · {esc(a['nationality'])} · {esc(mv)}</span>
            <span class="meta">Known for {esc(known_s)}.</span>
            <span class="meta">{len(picks[a['slug']])} {a.get('works_word', 'paintings')} on this site</span>
          </a>""")
        sections.append(f"""    <section class="era" id="{slugify(g)}">
      <h2>{esc(g)}</h2>
      <div class="artist-grid">
{chr(10).join(cards)}
      </div>
    </section>""")
    crumbs = [("Daily Canvas", SITE + "/"), ("Famous artists", url)]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url, "url": url, "name": title, "description": description, "inLanguage": "en",
         "isPartOf": {"@id": f"{SITE}/#website"}, "primaryImageOfPage": og,
         "mainEntity": {"@type": "ItemList", "name": "Famous artists", "numberOfItems": n,
                        "itemListElement": [{"@type": "ListItem", "position": k + 1, "url": f"{SITE}/artists/{a['slug']}",
                                             "item": {"@type": "Person", "name": a["name"], "birthDate": a["birth"],
                                                      "deathDate": a["death"], "nationality": a["nationality"]}}
                                            for k, a in enumerate(ar.ARTISTS)]}},
        crumbs_ld(crumbs), faq_ld(ar.INDEX_FAQ)]}
    return f"""{head_html(title, description, url, og, ld)}

  <main class="guide">
    <header class="intro">
      <p class="crumbs">{crumbs_html(crumbs)}</p>
      <h1>{esc(h1)}</h1>
      <p class="lede">{esc(lede)}</p>
      <nav class="toc" aria-label="Periods">
        <ul>
{toc}
        </ul>
      </nav>
    </header>

{chr(10).join(sections)}

    <section class="band">
      <h2>Questions</h2>
{faq_block(ar.INDEX_FAQ)}
    </section>

{DAILY_BAND}

    <section class="band">
      <h2>More guides</h2>
      <ul class="related">
        <li><a href="/{GUIDE_SLUG}">Famous paintings</a></li>
        <li><a href="/{MOVEMENTS_SLUG}">Art movements</a></li>
        <li><a href="/museums/">The best art museums in the US</a></li>
        <li><a href="/{HUB_SLUG}">Art wallpaper</a></li>
      </ul>
    </section>
  </main>

{FOOTER}"""


def linked_see(item):
    """'Irises (Vincent van Gogh)' with the artist linked when they have a page."""
    m = re.match(r"^(.*) \(([^)]+)\)$", item)
    if not m:
        return esc(item)
    t, who = m.groups()
    name = who.split(",")[0]
    return f"{esc(t)} ({artist_link(name)}{esc(who[len(name):])})" if name in ARTIST_BY_NAME else esc(item)


def museums_index_html(cat):
    url = f"{SITE}/museums/"
    n = len(mu.MUSEUMS)
    title = f"The Best Art Museums in the US: {n} to See in Person"
    h1 = "The best art museums in the US"
    description = (f"{n} of the best art museums in the US, from the Met and MoMA to the Art Institute of Chicago and "
                   "the National Gallery of Art: what to see at each one, and which are free.")
    og = og_image(cat["aic-27992"], "art-museums")
    lede = (f"{mu.INDEX_INTRO} Here are {n} worth planning a trip around, with what to see at each one and "
            "which ones are free.")
    entries = []
    for k, m in enumerate(mu.MUSEUMS):
        facts = [m["city"]]
        if m.get("founded"):
            facts.append(f"founded {m['founded']}")
        if m.get("free"):
            facts.append(m["free"])
        see = "\n".join(f"          <li>{linked_see(x)}</li>" for x in m["see"])
        page = (f'<a href="/museums/{m["slug"]}" class="more">Famous paintings at {esc(m["short"])}</a>'
                if m.get("page") else "")
        entries.append(f"""      <article class="museum" id="{m['slug']}">
        <h2><span class="num">{k + 1}.</span> {esc(m['name'])}</h2>
        <p class="meta">{esc(' · '.join(facts))}</p>
        <p>{esc(m['why'])}</p>
        <p class="see-label">What to see:</p>
        <ul class="see">
{see}
        </ul>
        <p class="dl">{page}<a href="{esc(m['url'])}" rel="noopener">The museum's website</a></p>
      </article>""")
    crumbs = [("Daily Canvas", SITE + "/"), ("Art museums", url)]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": url, "url": url, "headline": h1, "name": title, "description": description,
         "inLanguage": "en", "image": og, "dateModified": datetime.date.today().isoformat(),
         "isPartOf": {"@id": f"{SITE}/#website"}, "publisher": {"@id": f"{SITE}/#org"},
         "mainEntity": {"@type": "ItemList", "name": "Art museums in the US", "numberOfItems": n,
                        "itemListElement": [{"@type": "ListItem", "position": k + 1, "url": f"{url}#{m['slug']}",
                                             "item": {"@type": "Museum", "name": m["name"], "url": m["url"],
                                                      "address": {"@type": "PostalAddress", "addressLocality": m["city"],
                                                                  "addressCountry": "US"},
                                                      "isAccessibleForFree": True if m.get("free") == "Free" else None}}
                                            for k, m in enumerate(mu.MUSEUMS)]}},
        crumbs_ld(crumbs), faq_ld(mu.INDEX_FAQ)]}
    return f"""{head_html(title, description, url, og, ld, og_type="article")}

  <main class="guide">
    <header class="intro">
      <p class="crumbs">{crumbs_html(crumbs)}</p>
      <h1>{esc(h1)}</h1>
      <p class="lede">{esc(lede)}</p>
    </header>

    <div class="museums">
{chr(10).join(entries)}
    </div>

    <section class="band">
      <h2>Questions</h2>
{faq_block(mu.INDEX_FAQ)}
    </section>

{DAILY_BAND}

    <section class="band">
      <h2>More guides</h2>
      <ul class="related">
        <li><a href="/artists/">Famous artists</a></li>
        <li><a href="/{GUIDE_SLUG}">Famous paintings</a></li>
        <li><a href="/{MOVEMENTS_SLUG}">Art movements</a></li>
      </ul>
    </section>
  </main>

{FOOTER}"""


def museum_html(m, pg, cat):
    url = f"{SITE}/museums/{m['slug']}"
    works = [(cat[i], note) for i, note in pg["highlights"]]
    og = og_image(works[0][0], f"museum-{m['slug']}")
    description = pg["answer"]
    if len(description) > 160:
        description = description[:description.rfind(",", 0, 157)] + "."
    infos = [work_info(p) for p, _ in works]
    anchors = unique_ids([i["t"] for i in infos])
    cards = "\n".join(work_card(p, i, an, k < 3, note=note, show_artist=True)
                      for k, ((p, note), i, an) in enumerate(zip(works, infos, anchors)))
    here = []
    for p, _ in works:
        name = FAMOUS[p["id"]]["a"] if p["id"] in FAMOUS else p["artist"]["name"]
        a = ARTIST_BY_NAME.get(name)
        if a and a not in here:
            here.append(a)
    here_html = ", ".join(f'<a href="/artists/{a["slug"]}">{esc(a["name"])}</a>' for a in here)
    admission = m.get("free") or "Ticketed; see the museum's website"
    others = [x for x in mu.MUSEUMS if x.get("page") and x is not m]
    related = "\n".join(f'        <li><a href="/museums/{x["slug"]}">Famous paintings at {esc(x["short"])}</a></li>' for x in others)
    related += '\n        <li><a href="/museums/">The best art museums in the US</a></li>'
    related += f'\n        <li><a href="/artists/">Famous artists</a></li>'
    crumbs = [("Daily Canvas", SITE + "/"), ("Art museums", f"{SITE}/museums/"), (m["name"], url)]
    museum = {"@type": "Museum", "name": m["name"], "url": m["url"],
              "address": {"@type": "PostalAddress", "addressLocality": m["city"], "addressCountry": "US"},
              "foundingDate": m.get("founded"), "isAccessibleForFree": True if m.get("free") == "Free" else None}
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": url, "url": url, "headline": pg["h1"], "name": pg["title"], "description": description,
         "inLanguage": "en", "image": og, "dateModified": datetime.date.today().isoformat(),
         "isPartOf": {"@id": f"{SITE}/#website"}, "publisher": {"@id": f"{SITE}/#org"}, "about": museum,
         "mainEntity": {"@type": "ItemList", "name": pg["h1"], "numberOfItems": len(works),
                        "itemListElement": [artwork_entry(p, i, FAMOUS[p["id"]]["a"] if p["id"] in FAMOUS else p["artist"]["name"],
                                                          url, an, k + 1)
                                            for k, ((p, _), i, an) in enumerate(zip(works, infos, anchors))]}},
        crumbs_ld(crumbs), faq_ld(pg["faq"])]}
    intro = "\n".join(f"      <p>{esc(x)}</p>" for x in pg["intro"])
    return f"""{head_html(pg['title'], description, url, og, ld, og_type="article")}

  <main class="guide">
    <header class="intro">
      <p class="crumbs">{crumbs_html(crumbs)}</p>
      <h1>{esc(pg['h1'])}</h1>
      <p class="lede">{esc(pg['answer'])}</p>
      <dl class="facts">
        <div><dt>City</dt><dd>{esc(m['city'])}</dd></div>
        <div><dt>Founded</dt><dd>{esc(m['founded'])}</dd></div>
        <div><dt>Admission</dt><dd>{esc(admission)}</dd></div>
        <div><dt>Website</dt><dd><a href="{esc(m['url'])}" rel="noopener">{esc(m['url'].replace('https://', '').replace('www.', ''))}</a></dd></div>
      </dl>
    </header>

    <section class="band">
      <h2>About the museum</h2>
{intro}
    </section>

    <section class="artist-works">
      <h2>{len(works)} paintings to see</h2>
      <p class="era-intro">Each can be downloaded free as an iPhone or Mac wallpaper. Displays change, so check the museum's site for what's on view.</p>
      <div class="works-grid">
{cards}
      </div>
    </section>

    <section class="band">
      <h2>Artists here with their own pages</h2>
      <p>{here_html}.</p>
    </section>

    <section class="band">
      <h2>Questions</h2>
{faq_block(pg['faq'])}
    </section>

{DAILY_BAND}

    <section class="band">
      <h2>More museum guides</h2>
      <ul class="related">
{related}
      </ul>
    </section>
  </main>

{FOOTER}"""


PERIOD_BY_SLUG = {pd["slug"]: pd for pd in pe.PERIODS}
BAD_IMAGES = ({i for a in ar.ARTISTS for i in a.get("exclude", ())} | {i for pd in pe.PERIODS for i in pd.get("exclude", ())}
              | set(pe.CROPPED))
MAX_PERIOD_WORKS = 24


def movement_href(slug):
    return f"/{MOVEMENTS_SLUG}/{slug}" if slug in PERIOD_BY_SLUG else f"/{MOVEMENTS_SLUG}#{slug}"


def period_link(m):
    if m["slug"] not in PERIOD_BY_SLUG:
        return ""
    label = PERIOD_BY_SLUG[m["slug"]]["works_label"]
    return f'\n        <p class="dl"><a href="/{MOVEMENTS_SLUG}/{m["slug"]}" class="more">{esc(m["name"])}: more {esc(label)}, the artists and the history</a></p>'


def select_period_works(pd, cat):
    """The movement's best-known works first, then one work per artist in turn, key artists first."""
    lo, hi = pd["window"]
    names = {}
    for disp, cat_names in pd["artists"]:
        for n in cat_names:
            names[n] = disp
    shim = {"works_word": "prints"} if pd.get("prints") else {}
    by_artist = {disp: [] for disp, _ in pd["artists"]}
    for p in cat.values():
        disp = names.get(p["artist"]["name"])
        if not disp or not trusted(p) or p["id"] in BAD_IMAGES:
            continue
        if pd.get("skip_titles") and re.search(pd["skip_titles"], p["title"]):
            continue
        info = work_info(p, shim)
        yk = year_key(info["y"])
        w_lo, w_hi = pd.get("windows", {}).get(disp, (lo, hi))
        if yk == 9999 or not (max(lo, w_lo) <= yk <= min(hi, w_hi)):
            continue
        if p["id"] not in FAMOUS and p["id"] not in ar.EXTRA and lifespan_like(p.get("year")):
            continue
        by_artist[disp].append(p)
    must = {i: n for n, i in enumerate(pd["must"])}

    def rank(p):
        i = p["id"]
        return (0 if i in must else 1, must.get(i, 0), 0 if i in FAMOUS else 1,
                0 if p.get("curatorHighlight") else 1, SOURCE_ORDER.get(p["source"], 9), i)

    for disp in by_artist:
        by_artist[disp].sort(key=rank)
    chosen, keys, owner = [], [], {}

    def take(p, disp):
        info = work_info(p, shim)
        k = (re.sub(r"[^a-z0-9]", "", info["t"].lower()), year_key(info["y"]))
        if p["id"] in owner or any(k[1] == y and (k[0] == t or (min(len(k[0]), len(t)) >= 20 and (k[0].startswith(t) or t.startswith(k[0]))))
                                   for t, y in keys):
            return False
        keys.append(k)
        chosen.append(p)
        owner[p["id"]] = disp
        return True

    for i in pd["must"]:
        for disp, ws in by_artist.items():
            if any(p["id"] == i for p in ws):
                take(cat[i], disp)
    queues = {disp: list(ws) for disp, ws in by_artist.items()}
    caps = pd.get("caps", {})
    while len(chosen) < MAX_PERIOD_WORKS and any(queues.values()):
        for disp, _ in pd["artists"]:
            q = queues[disp]
            if disp in caps and sum(1 for d in owner.values() if d == disp) >= caps[disp]:
                q.clear()
            while q and not take(q.pop(0), disp):
                pass
            if len(chosen) >= MAX_PERIOD_WORKS:
                break
    chosen.sort(key=lambda p: (year_key(work_info(p, shim)["y"]), p["id"]))
    return [(p, owner[p["id"]]) for p in chosen]


def period_html(pd, cat, works):
    m = next(x for x in am.MOVEMENTS if x["slug"] == pd["slug"])
    url = f"{SITE}/{MOVEMENTS_SLUG}/{pd['slug']}"
    shim = {"works_word": "prints"} if pd.get("prints") else {}
    n = len(works)
    description = pd["lede"] if len(pd["lede"]) <= 160 else pd["lede"][:pd["lede"].rfind(" ", 0, 156)].rstrip(",;:") + "…"
    og = og_image(works[0][0] if not pd["must"] else cat[pd["must"][0]], f"period-{pd['slug']}")
    infos = [work_info(p, shim) for p, _ in works]
    anchors = unique_ids([i["t"] for i in infos])
    cards = "\n".join(work_card(p, i, an, k < 3, show_artist=True, artist_name=disp)
                      for k, ((p, disp), i, an) in enumerate(zip(works, infos, anchors)))

    order = [x["slug"] for x in am.MOVEMENTS]
    k = order.index(pd["slug"])
    def neighbor(label, j):
        if 0 <= j < len(order):
            x = am.MOVEMENTS[j]
            return f'\n        <div><dt>{label}</dt><dd><a href="{movement_href(x["slug"])}">{esc(x["name"])}</a></dd></div>'
        return ""
    key_artists = ", ".join(artist_link(a.strip()) for a in m["artists"].split(","))

    present = []
    for _, disp in works:
        if disp not in present:
            present.append(disp)
    artists_line = ", ".join(artist_link(d) for d in present)

    related = [x for x in pe.PERIODS if x is not pd]
    related_html = "\n".join(f'        <li><a href="/{MOVEMENTS_SLUG}/{x["slug"]}">{esc(next(y["name"] for y in am.MOVEMENTS if y["slug"] == x["slug"]))}</a></li>' for x in related)
    related_html += f'\n        <li><a href="/{MOVEMENTS_SLUG}">All art movements</a></li>'

    crumbs = [("Daily Canvas", SITE + "/"), ("Art movements", f"{SITE}/{MOVEMENTS_SLUG}"), (m["name"], url)]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": url, "url": url, "headline": pd["h1"], "name": pd["title"], "description": description,
         "inLanguage": "en", "image": og, "dateModified": datetime.date.today().isoformat(),
         "isPartOf": {"@id": f"{SITE}/#website"}, "publisher": {"@id": f"{SITE}/#org"},
         "about": {"@type": "DefinedTerm", "name": m["name"], "description": pd["lede"],
                   "inDefinedTermSet": f"{SITE}/{MOVEMENTS_SLUG}"},
         "mainEntity": {"@type": "ItemList", "name": pd["works_label"].capitalize(), "numberOfItems": n,
                        "itemListElement": [artwork_entry(p, i, disp, url, an, j + 1)
                                            for j, ((p, disp), i, an) in enumerate(zip(works, infos, anchors))]}},
        crumbs_ld(crumbs), faq_ld(pd["faq"])]}
    history = "\n".join(f"      <p>{esc(x)}</p>" for x in pd["history"])

    return f"""{head_html(pd['title'], description, url, og, ld, og_type="article")}

  <main class="guide">
    <header class="intro">
      <p class="crumbs">{crumbs_html(crumbs)}</p>
      <h1>{esc(pd['h1'])}</h1>
      <p class="lede">{esc(pd['lede'])}</p>
      <dl class="facts">
        <div><dt>Dates</dt><dd>{esc(m['dates'])}</dd></div>
        <div><dt>Where</dt><dd>{esc(m['where'])}</dd></div>{neighbor("Before", k - 1)}{neighbor("After", k + 1)}
      </dl>
    </header>

    <section class="band">
      <h2>History</h2>
{history}
    </section>

    <section class="band">
      <h2>How to recognize it</h2>
      <p>{esc(m['look'])}</p>
      <p><strong>Key artists:</strong> {key_artists}.</p>
    </section>

    <section class="artist-works">
      <h2>{n} {esc(pd['works_label'])}</h2>
      <p class="era-intro">In date order, with who made each one and where it is today. Every one can be downloaded free as an iPhone or Mac wallpaper.</p>
      <div class="works-grid">
{cards}
      </div>
      <p class="no-ex">The {esc(pd['works_label'])} on this page are by {artists_line}.</p>
    </section>

    <section class="band">
      <h2>Questions</h2>
{faq_block(pd['faq'])}
    </section>

{DAILY_BAND}

    <section class="band">
      <h2>More art movements</h2>
      <ul class="related">
{related_html}
      </ul>
    </section>
  </main>

{FOOTER}"""


def write_periods(cat):
    """Writes art-movements/<slug>.html for each period page and returns their sitemap paths."""
    picks = {pd["slug"]: select_period_works(pd, cat) for pd in pe.PERIODS}
    ids = sorted({p["id"] for ws in picks.values() for p, _ in ws})
    with ThreadPoolExecutor(12) as pool:
        list(pool.map(lambda i: painting_thumb(cat[i]), ids))
    os.makedirs(os.path.join(ROOT, MOVEMENTS_SLUG), exist_ok=True)
    paths = []
    for pd in pe.PERIODS:
        with open(os.path.join(ROOT, MOVEMENTS_SLUG, pd["slug"] + ".html"), "w") as f:
            f.write(period_html(pd, cat, picks[pd["slug"]]))
        paths.append(f"{MOVEMENTS_SLUG}/{pd['slug']}")
    print(f"wrote {MOVEMENTS_SLUG}/ ({len(pe.PERIODS)} period pages, {sum(len(w) for w in picks.values())} works)")
    return paths


def write_artists_and_museums(cat):
    """Writes artists/ and museums/ and returns their sitemap paths."""
    picks = {a["slug"]: select_works(a, cat) for a in ar.ARTISTS}
    ids = {p["id"] for ws in picks.values() for p in ws}
    ids |= {i for pg in mu.PAGES.values() for i, _ in pg["highlights"]}
    with ThreadPoolExecutor(12) as pool:        # the first build fetches a few hundred display images
        list(pool.map(lambda i: painting_thumb(cat[i]), sorted(ids)))
    paths = []
    os.makedirs(os.path.join(ROOT, "artists"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "museums"), exist_ok=True)
    with open(os.path.join(ROOT, "artists", "index.html"), "w") as f:
        f.write(artists_index_html(cat, picks))
    paths.append("artists/")
    for a in ar.ARTISTS:
        with open(os.path.join(ROOT, "artists", a["slug"] + ".html"), "w") as f:
            f.write(artist_html(a, cat, picks[a["slug"]]))
        paths.append(f"artists/{a['slug']}")
    with open(os.path.join(ROOT, "museums", "index.html"), "w") as f:
        f.write(museums_index_html(cat))
    paths.append("museums/")
    by_slug = {m["slug"]: m for m in mu.MUSEUMS}
    for slug, pg in mu.PAGES.items():
        with open(os.path.join(ROOT, "museums", slug + ".html"), "w") as f:
            f.write(museum_html(by_slug[slug], pg, cat))
        paths.append(f"museums/{slug}")
    print(f"wrote artists/ ({len(ar.ARTISTS)} artists, {sum(len(w) for w in picks.values())} works) "
          f"and museums/ ({len(mu.PAGES)} pages)")
    return paths


def write_sitemap(slugs, extra=()):
    today = datetime.date.today().isoformat()
    urls = ["", *slugs, GUIDE_SLUG, MOVEMENTS_SLUG, *extra, "privacy", "terms"]
    body = "\n".join(f"  <url>\n    <loc>{SITE}/{u}</loc>\n    <lastmod>{today}</lastmod>\n  </url>" for u in urls)
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", default=DEFAULT_CATALOG)
    args = ap.parse_args()
    cat = load_catalog(args.catalog)
    missing = [i for pg in PAGES for i in pg["ids"] if i not in cat]
    missing += [e["id"] for _, _, es in fp.SECTIONS for e in es if e["id"] not in cat]
    missing += [x[0] for m in am.MOVEMENTS for x in m["ex"] if x[0] not in cat]
    missing += [i for a in ar.ARTISTS for i in a["must"] if i not in cat]
    missing += [i for pg in mu.PAGES.values() for i, _ in pg["highlights"] if i not in cat]
    missing += [i for pd in pe.PERIODS for i in pd["must"] if i not in cat]
    unknown = [pd["slug"] for pd in pe.PERIODS if pd["slug"] not in {m["slug"] for m in am.MOVEMENTS}]
    if unknown:
        sys.exit(f"Period pages with no movement in art_movements.py: {unknown}")
    if missing:
        sys.exit(f"Not in catalog: {missing}")
    for pg in PAGES:
        with open(os.path.join(ROOT, pg["slug"] + ".html"), "w") as f:
            f.write(page_html(pg, cat, PAGES))
        print("wrote", pg["slug"] + ".html")
    with open(os.path.join(ROOT, GUIDE_SLUG + ".html"), "w") as f:
        f.write(guide_html(cat))
    print("wrote", GUIDE_SLUG + ".html")
    with open(os.path.join(ROOT, MOVEMENTS_SLUG + ".html"), "w") as f:
        f.write(movements_html(cat))
    print("wrote", MOVEMENTS_SLUG + ".html")
    extra = write_artists_and_museums(cat)
    extra += write_periods(cat)
    write_sitemap([pg["slug"] for pg in PAGES], extra)
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
