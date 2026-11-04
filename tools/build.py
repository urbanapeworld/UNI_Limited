#!/usr/bin/env python3
"""Generate every HTML page, sitemap.xml and robots.txt into ../public.

Edit content here, then run:  python3 tools/build.py
Commit the generated files in public/ too: Cloudflare serves public/ as-is.
Needs Python 3.8+ and Pillow (for image sizes, to prevent layout shift).
"""
import datetime, html, json, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public")
SITE = "https://uniprofiles.in"          # canonical domain: change here only
ASSET_V = "3"                            # bump to bust CSS/JS caches
TODAY = datetime.date.today().isoformat()

PHONE, PHONE2 = "+91 94375 57166", "+91 82490 10494"
TEL = "+919437557166"
EMAIL, EMAIL2 = "uniprofiles@uniprofiles.in", "sushant.hota@uniprofiles.in"
ADDR_SHORT = "Plot 2045/P, Village Jharbeda, Rajgangpur, Dist. Sundargarh, Odisha 770070"
ADDR_LONG = ("Plot 2045/P, Khata 174, Village Jharbeda, near Dalmia College, SH-10, "
             "Rajgangpur, Dist. Sundargarh, Odisha 770070, India")
e = html.escape

# ---------------------------------------------------------------- images
_dims = {}
def dims(name):
    if name not in _dims:
        with Image.open(os.path.join(PUB, "img", name + ".jpg")) as im:
            _dims[name] = im.size
    return _dims[name]

def img(name, alt, lazy=True, cls="", style=""):
    w, h = dims(name)
    a = [f'src="/img/{name}.jpg"', f'alt="{e(alt)}"', f'width="{w}"', f'height="{h}"']
    if lazy: a.append('loading="lazy" decoding="async"')
    if cls: a.append(f'class="{cls}"')
    if style: a.append(f'style="{style}"')
    return "<img " + " ".join(a) + ">"

def figs(items):
    return '<div class="figs">' + "".join(
        f"<figure>{img(n, c)}<figcaption>{e(c)}</figcaption></figure>" for n, c in items) + "</div>"

# ---------------------------------------------------------------- data
PRODUCTS = [
  dict(slug="boiler-conveyor-structures", name="Boiler & Conveyor Structures", short="Boiler & conveyor structures",
       icon="i-beam", card="buckstay-cob", card_alt="Painted buck stays for a coke oven battery",
       title="Boiler Structures, Buck Stays & Conveyor Galleries | Uni Profiles, Odisha",
       desc="Buck stays, columns, beams, bracings, auto-weld beams and conveyor galleries fabricated at Rajgangpur, Odisha for BHEL, Thermax and steel-plant projects.",
       h1="Boiler Structures, Buck Stays & Conveyor Galleries",
       lede="Buck stays, columns, beams, bracings and conveyor structures for utility boilers, coke-oven batteries and raw-material handling systems.",
       teaser="Buck stays, columns, beams, bracings and conveyor galleries for utility boilers, coke-oven batteries and material handling."),
  dict(slug="steel-stacks-chimneys", name="Steel Stacks & Chimneys", short="Stacks & chimneys",
       icon="i-stack", card="stack-shell-1", card_alt="Flanged steel stack shell ready for dispatch",
       title="Steel Stack & Chimney Fabrication | Uni Profiles, Rajgangpur, Odisha",
       desc="Self-supporting steel stacks and chimneys in rolled, flanged shells for refineries including IOCL and BORL. Fabricated, blasted, painted and dispatched from Rajgangpur, Odisha.",
       h1="Steel Stack & Chimney Fabrication",
       lede="Self-supporting steel stacks in rolled shells with flanged joints, fabricated, blasted, painted and banded for dispatch to refinery and plant sites.",
       teaser="Self-supporting steel stacks in rolled shells with flanged joints, platforms and ladders, painted and banded for dispatch."),
  dict(slug="fired-heater-non-pressure-parts", name="Fired Heater Non-Pressure Parts", short="Fired heater parts",
       icon="i-flame", card="heater-trial", card_alt="Fired heater casing in trial assembly at the works",
       title="Fired Heater Casings & Non-Pressure Parts | Uni Profiles, Odisha",
       desc="Radiant and convection casings, structural frames and ducting for refinery fired heaters, trial-assembled at our Rajgangpur works before dispatch.",
       h1="Fired Heater Casings & Non-Pressure Parts",
       lede="Radiant and convection casings, structural frames and ducting for refinery fired heaters, trial-assembled in the shop before they are shipped.",
       teaser="Radiant and convection casings, structural frames and ducting, trial-assembled at the works before shipment."),
  dict(slug="silos-hoppers-ducts", name="Silos, Hoppers & Ducts", short="Silos, hoppers & ducts",
       icon="i-funnel", card="ntpc-silo", card_alt="Stiffened steel silo cone in fabrication for an NTPC project through BHEL",
       title="Silos, Hoppers, Flue Ducts & Gas Mains | Uni Profiles, Odisha",
       desc="Silo cones, bunkers, crusher hoppers, flanged flue ducts and gas collecting mains in stiffened plate, fabricated at Rajgangpur for NTPC, BHEL and steel-plant projects.",
       h1="Silos, Hoppers, Flue Ducts & Gas Mains",
       lede="Plate-work in stiffened steel: silo cones and bunkers, crusher hoppers, large flanged flue ducts and coke-oven gas collecting mains.",
       teaser="Silo cones and bunkers for NTPC projects through BHEL, crusher hoppers, large flanged flue ducts and gas collecting mains."),
  dict(slug="non-pressurised-tanks", name="Non-Pressurised Tanks", short="Tanks",
       icon="i-tank", card="tank-shop", card_alt="Large non-pressurised tank with internal grid in the fabrication bay",
       title="Non-Pressurised Tank & Process Vessel Fabrication | Uni Profiles, Odisha",
       desc="Non-pressurised process tanks with internals, overhead and drainage tanks and stiffened rectangular bath tanks, fabricated at Rajgangpur, Odisha.",
       h1="Non-Pressurised Tanks & Process Vessels",
       lede="Large process vessels with internals, overhead and drainage tanks, and stiffened rectangular bath tanks, built to the client's drawing.",
       teaser="Large process vessels with internals, overhead and drainage tanks, and stiffened rectangular bath tanks."),
  dict(slug="bridge-girders-built-up-sections", name="Bridge Girders & Built-up Sections", short="Bridge girders",
       icon="i-bridge", card="truss-girder", card_alt="Steel through-truss bridge girder in trial assembly in the works yard",
       title="RDSO-Approved Steel Bridge Girders & H-Beams | Uni Profiles, Odisha",
       desc="RDSO-approved open web, plate and composite steel girders (Parts A & B, 3,600 MT a year), ROB girders, and H-beams and built-up sections from an automated beam line.",
       h1="RDSO-Approved Bridge Girders & Built-up Sections",
       lede="Open web, plate and composite steel girders on the RDSO approved list, road-over-bridge spans, and H-beams and built-up sections from our automated beam line.",
       teaser="RDSO-approved open web, plate and composite girders, trial-assembled in our yard, plus H-beams and built-up sections."),
]
PBY = {p["slug"]: p for p in PRODUCTS}

INDUSTRIES = [
  dict(slug="refineries", t="Refineries & Petrochemicals", c="IOCL, BORL",
       prod=["steel-stacks-chimneys", "fired-heater-non-pressure-parts"],
       im=[("stack-bongaigaon","IOCL Bongaigaon · stack shell 3"),("stack-shell-1","IOCL · stack shell 1"),("stack-iocl","IOCL · stack base and shell segments"),("chimney-borl","BORL · chimney after erection"),("heater-trial","Fired heater · shop trial assembly"),("heater-erection","Fired heater · erection at site"),("fired-heater-duct","Large duct assembly, painted")]),
  dict(slug="steel-plants", t="Steel Plants & Coke Ovens", c="SAIL RSP via BEC Bhilai",
       prod=["boiler-conveyor-structures", "silos-hoppers-ducts", "non-pressurised-tanks"],
       im=[("buckstay-cob","Buck stays · Coke Oven Battery 3"),("gas-main","Gas collecting main · coke ovens"),("drainage-tank","Drainage tank · COB 3")]),
  dict(slug="power", t="Power & Boilers", c="BHEL, Thermax",
       prod=["boiler-conveyor-structures", "silos-hoppers-ducts"],
       im=[("ntpc-silo","BHEL for NTPC · silo cone in fabrication"),("buckstay-bhel","BHEL Trichy · buck stay"),("duct-flange","Flanged duct with internal bracing"),("tube-module","Tube bank in fabricated casing"),("shell-trailer","Painted cylindrical casings")]),
  dict(slug="railways-bridges", t="Railways & Bridges", c="RDSO girders and ROB spans",
       prod=["bridge-girders-built-up-sections"],
       im=[("rdso-girder-site","RDSO plate girder span · erected at site"),("truss-girder","Through-truss girder · trial assembly in the yard"),("rob-assembly","Rawatsons Engineers · ROB girder control assembly"),("beam-yard","Built-up sections in the bay")]),
  dict(slug="mining-material-handling", t="Mining & Material Handling", c="BHEL ISG and others",
       prod=["boiler-conveyor-structures", "silos-hoppers-ducts"],
       im=[("conveyor-gallery","BHEL ISG · conveyor gallery"),("crusher-hopper","Crusher hopper"),("hopper-pyramid","Pyramid crusher hopper"),("crusher-stand","Crusher stand")]),
  dict(slug="tanks-aerospace", t="Aerospace & Industrial Tanks", c="Process tanks, Tata Aerospace Systems, L&T ECC",
       prod=["non-pressurised-tanks"],
       im=[("tank-shop","Non-pressurised tank with internals · in the bay"),("bath-tank","Tata Aerospace Systems (SECO) · bath tank"),("overhead-tank","L&T ECC Kansbahal · overhead tank")]),
  dict(slug="dispatch-erection", t="Dispatch & Site Erection", c="Across projects",
       prod=["steel-stacks-chimneys"],
       im=[("crane-lift","Three-crane tandem lift onto trailer"),("chimney-site","Chimney · two segments erected"),("stack-shell-b","Stack shell · stiffened base flange"),("shipment","Assemblies wrapped for transport")]),
]
IBY = {i["slug"]: i for i in INDUSTRIES}

CLIENTS = [("BHEL","Trichy & Bengaluru"),("SAIL","Rourkela Steel Plant"),("Thermax","Pune"),("L&T ECC","Kansbahal"),("Tata Projects","EPC"),("GE Power","India"),("thyssenkrupp","Industries India"),("MECON","Limited"),("Hindalco","Hirakud"),("BEC","Bhilai"),("Tenova","Chennai"),("Fives Stein","Kolkata"),("Rawatsons","Kolkata"),("Zetwerk","Bengaluru"),("Mogli Labs","India")]

TESTIMONIALS = [
  ("Bhilai Engineering Corporation","Engineering & Steel Plant Equipment","Confirmed purchases of more than 4,000 tons of complex structures over five years, including ducts, buck stays, stacks and gas mains, and rated our quality and delivery as exemplary."),
  ("BHEL, Tiruchirappalli","Power & Boilers","Certified our general fabrication, ducts, buck stays, auto-weld beams, bracings and columns since 2012, with performance recorded as good on quality and delivery schedule."),
  ("Thermax Limited","Boiler & Heater Division","Appreciated our execution of columns, beams, girders, buck stays, ducting and heater casings across several projects, with special thanks for keeping their schedule and quality."),
  ("BHEL Industrial Systems Group","Material Handling","Confirmed our fabrication and supply of RMHS structures, including trestles, gallery and junction house, for the Nagarnar steel plant project, with good quality and delivery."),
]

APPROVALS = [
  ("RDSO","Open web, composite and other steel plate girders, Parts A and B. 3,600 MT a year.","CBS/G/Reg/Uni Profiles"),
  ("NTPC","Welded technological and building structures, single pieces up to about 10 T. Also approved for auto-weld beams and bracings.","01/7010-602/UNI PROFILES"),
  ("SAIL, Rourkela Steel Plant","Registered manufacturer for heavy structural fabrication.","Vendor code 1000090842"),
  ("BHEL, Trichy","General fabrication, ducts, buck stays, auto-weld beams and columns since 2012.","Vendor code 14548"),
  ("ISO 9001:2015","Fabrication and machining of equipment, spares, technological structures and H-beams.","Certificate 23DQKX25"),
  ("MSME & Factory Licence","Udyam-registered small manufacturer. Factory licence SG 661, Odisha.","UDYAM-OD-30-0000302"),
]

TPI = ["MECON Ltd","Centre for Engineering and Technology, SAIL","Lloyd's","TÜV Rheinland","TÜV Nord","Inspectorate","Bureau Veritas India (BVIL)","Tata Projects Ltd (Inspection Division)","IRClass","Quest"]

MACHINES = [  # from the 2024 company profile
  ("CNC profile cutting machine with plasma source","Primo Automation","4 m × 15 m","1"),
  ("Beam assembly machine","Primo Automation","2 m H × 1 m","1"),
  ("H-beam straightening machine","Primo Automation","Up to 80 mm","1"),
  ("EOT crane","N K Engineers","20 MT","2"),
  ("EOT crane","N K Engineers","5 MT","1"),
  ("Mobile (hydra) crane","Escorts","12 MT","2"),
  ("SAW welding machine","Lincoln Electric DC-1000","0–1,000 A","1"),
  ("SAW welding machine","D&H Sécheron SAW 1250","0–1,250 A","1"),
  ("Hydraulic power press","Simpletec Automatics","600 MT","1"),
  ("Plate bending (rolling) machine","Maharshi Industries","25 mm × 2,500 mm","1"),
  ("Multi-axis CNC drilling machine","Kotec, Korea","Up to Ø40 mm","1"),
  ("Pillar drilling machine","Royal","Up to Ø36 mm","1"),
  ("Core / magnetic drilling machines","Ralli Wolf, FEIN, Positron","Ø25–60 mm","14"),
  ("Plasma cutting machine","D&H Sécheron","125 A","1"),
  ("Pug cutting machines","ESAB, D&H, Koike","—","13"),
  ("MIG welding machines","Panasonic YD-400 KR2","0–400 A","17"),
  ("ARC welding machines","Panasonic, WARPP","0–400 A","11"),
  ("ARC welding machines","WARPP, Megatronic, Memco","0–250 A","10"),
  ("Electrode baking oven (mother oven)","Multispan MDC-2901","0–400 °C","1"),
  ("Flux baking ovens","Multispan, Swastik","Ambient–300 °C","2"),
  ("Portable electrode ovens","Thermocut, Memco","0–200 °C","6"),
  ("Screw air compressor","ELGI","40 HP","1"),
  ("Reciprocating air compressors","Indo-Air, Prime","3 HP","3"),
  ("Shot blasting equipment","Kulmech","8–10 mm nozzle","1"),
  ("Angle grinders","Bosch, DeWalt","—","30"),
  ("DG set","Cummins","125 kVA","1"),
]

# ---------------------------------------------------------------- chrome
ICONS = open(os.path.join(ROOT, "tools", "icons.svg")).read()

def nav(cur):
    """cur is the top-level section key; returns desktop + mobile nav."""
    def top(key, href, label, sub=None):
        on = ' aria-current="page"' if cur == key else ""
        chev = ' <svg class="ic chev"><use href="#i-chev"/></svg>' if sub else ""
        s = f'<li><a href="{href}"{on}>{label}{chev}</a>'
        if sub:
            s += '<ul class="drop">' + "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in sub) + "</ul>"
        return s + "</li>"
    about = [("/about/","Who We Are"),("/facility/","Manufacturing Facility"),("/about/#quality","Quality &amp; Inspection"),("/approvals/","Approvals &amp; Certificates")]
    prods = [(f"/products/{p['slug']}/", e(p["name"])) for p in PRODUCTS]
    projs = [(f"/projects/#{i['slug']}", e(i["t"])) for i in INDUSTRIES]
    clients = [("/clients/","Our Clients"),("/clients/#testimonials","Client Testimonials")]
    desk = ('<ul class="menu">' + top("about","/about/","About Us",about) + top("products","/products/","Products",prods)
            + top("projects","/projects/","Projects",projs) + top("clients","/clients/","Clients",clients)
            + top("approvals","/approvals/","Approvals") + top("contact","/contact/","Contact Us") + "</ul>")
    mob = ('<a href="/about/">About Us</a><a class="subl" href="/facility/">Manufacturing Facility</a><a class="subl" href="/approvals/">Approvals &amp; Certificates</a>'
           '<a href="/products/">Products</a>' + "".join(f'<a class="subl" href="{h}">{l}</a>' for h, l in prods)
           + '<a href="/projects/">Projects</a><a href="/clients/">Clients</a><a href="/contact/">Contact Us</a>')
    return desk, mob

ORG = {
  "@type": "Organization", "@id": SITE + "/#org", "name": "Uni Profiles Pvt. Ltd.", "alternateName": "Uni Profiles",
  "url": SITE + "/", "logo": SITE + "/img/logo.png", "email": EMAIL, "telephone": TEL, "foundingDate": "2009",
  "description": "Heavy steel and alloy-steel fabrication works at Rajgangpur, Odisha: boiler structures, stacks, fired-heater casings, ducts, tanks and RDSO-approved bridge girders.",
  "address": {"@type": "PostalAddress", "streetAddress": "Plot 2045/P, Village Jharbeda, SH-10", "addressLocality": "Rajgangpur",
              "addressRegion": "Odisha", "postalCode": "770070", "addressCountry": "IN"},
  "contactPoint": {"@type": "ContactPoint", "telephone": TEL, "email": EMAIL2, "contactType": "sales", "areaServed": "IN"},
  "hasCredential": [{"@type": "EducationalOccupationalCredential", "name": "ISO 9001:2015"}],
}

def page(path, title, desc, body, cur="", crumbs=None, og_img="stack-bongaigaon", extra_ld=None, home=False):
    url = SITE + path
    graph = [ORG]
    if home:
        graph.append({"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "Uni Profiles", "publisher": {"@id": SITE + "/#org"}})
    if crumbs:
        items = [("Home", "/")] + crumbs
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": n + 1, "name": nm, "item": SITE + h} for n, (nm, h) in enumerate(items)]})
    if extra_ld: graph += extra_ld
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    desk, mob = nav(cur)
    doc = f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Uni Profiles Pvt. Ltd.">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/{og_img}.jpg">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/img/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/site.css?v={ASSET_V}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
{ICONS}
<div class="topbar">
  <div class="container">
    <span class="tag">Manufacturers of heavy steel structures, stacks, ducts and plate girders</span>
    <div class="info">
      <a href="tel:{TEL}"><span><svg class="ic"><use href="#i-phone"/></svg>{PHONE}</span></a>
      <a href="mailto:{EMAIL}"><span><svg class="ic"><use href="#i-mail"/></svg>{EMAIL}</span></a>
    </div>
  </div>
</div>
<header class="header">
  <div class="container">
    <a class="logo" href="/" aria-label="Uni Profiles home"><img src="/img/logo.png" alt="" width="42" height="42"><div><b>Uni Profiles</b><small>PVT. LTD. · SINCE 2009</small></div></a>
    <nav aria-label="Main">{desk}</nav>
    <button class="burger" type="button" id="burger" aria-expanded="false" aria-controls="mnav" aria-label="Open menu"><svg class="ic"><use href="#i-menu"/></svg></button>
  </div>
  <nav class="mnav" id="mnav" aria-label="Mobile" hidden>{mob}</nav>
</header>
<main id="top">
{body}
</main>
<footer>
  <div class="container fgrid">
    <div class="fbrand">
      <a class="logo" href="/"><img src="/img/logo.png" alt="" width="42" height="42"><div><b>Uni Profiles</b><small>PVT. LTD.</small></div></a>
      <p><b style="color:var(--ink)">Uni Profiles Pvt. Ltd.</b> fabricates heavy steel equipment and boiler auxiliary structures at Rajgangpur, Odisha, for India's power, steel, refinery and railway sectors.</p>
    </div>
    <div><h4>Products</h4><ul class="ql">{"".join(f'<li><a href="/products/{p["slug"]}/">{e(p["name"])}</a></li>' for p in PRODUCTS)}</ul></div>
    <div><h4>Company</h4><ul class="ql"><li><a href="/about/">Who We Are</a></li><li><a href="/facility/">Facility</a></li><li><a href="/projects/">Projects</a></li><li><a href="/clients/">Clients</a></li><li><a href="/approvals/">Approvals</a></li><li><a href="/contact/">Contact Us</a></li></ul>
      <ul class="ct" style="margin-top:22px">
        <li><svg class="ic"><use href="#i-phone"/></svg><a href="tel:{TEL}">{PHONE}</a></li>
        <li><svg class="ic"><use href="#i-mail"/></svg><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><svg class="ic"><use href="#i-pin"/></svg><span><b>Works:</b> {e(ADDR_LONG)}</span></li>
      </ul></div>
  </div>
  <div class="copy-bar">Copyright © {datetime.date.today().year} <span>Uni Profiles Pvt. Ltd.</span> All rights reserved.</div>
</footer>
<div class="side" aria-label="Quick actions">
  <a href="/contact/"><svg class="ic"><use href="#i-edit"/></svg>Enquiry</a>
  <a href="/projects/"><svg class="ic"><use href="#i-eye"/></svg>Projects</a>
  <a href="/approvals/"><svg class="ic"><use href="#i-shield"/></svg>Approvals</a>
</div>
<a class="wa" href="https://wa.me/919437557166" target="_blank" rel="noopener" aria-label="Chat on WhatsApp"><svg viewBox="0 0 24 24"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3ZM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 1 1 12 21.8Zm0-21.6A11.8 11.8 0 0 0 1.8 17.9L.1 24l6.3-1.6A11.8 11.8 0 1 0 12 .2Z"/></svg></a>
<script src="/assets/site.js?v={ASSET_V}" defer></script>
</body>
</html>
"""
    out = os.path.join(PUB, path.strip("/"), "index.html") if path != "/" else os.path.join(PUB, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    PAGES.append(path)

PAGES = []

def banner(h1, lede, crumbs, bg):
    items = [("Home", "/")] + crumbs
    li = "".join(f'<li><a href="{h}">{e(n)}</a></li>' if k < len(items) - 1 else f'<li aria-current="page">{e(n)}</li>'
                 for k, (n, h) in enumerate(items))
    return (f'<section class="pagehead">{img(bg, "", lazy=False)}<div class="container">'
            f'<nav aria-label="Breadcrumb"><ol class="crumbs">{li}</ol></nav><h1>{e(h1)}</h1><p>{lede}</p></div></section>')

def cta(text="Send us your drawings for a quote.", sub="Scope, tonnage and delivery point are enough to start.", product=None):
    href = "/contact/" + (f"?product={e(product)}" if product else "")
    return (f'<section class="cta"><div class="container"><div><h2>{text}</h2><p>{sub}</p></div>'
            f'<a class="btn light" href="{href}">Send Enquiry <i>↗</i></a></div></section>')

def prod_cards(exclude=None, head=True):
    cards = "".join(
        f'<a class="prod" href="/products/{p["slug"]}/">{img(p["card"], p["card_alt"])}<div class="body">'
        f'<span class="no"><svg class="ic"><use href="#{p["icon"]}"/></svg></span><h3>{e(p["name"])}</h3>'
        f'<p>{e(p["teaser"])}</p><span class="more">Details →</span></div></a>'
        for p in PRODUCTS if p["slug"] != exclude)
    return f'<div class="prods">{cards}</div>'

def cert_cards(items=APPROVALS):
    return '<div class="certs">' + "".join(
        f'<div class="cert"><span class="ico"><svg class="ic"><use href="#i-shield"/></svg></span><div><h3>{e(t)}</h3><p>{e(d)}</p><small>{e(r)}</small></div></div>'
        for t, d, r in items) + "</div>"

def client_tiles():
    return "".join(f'<div class="lg"><b>{e(a)}</b><small>{e(b)}</small></div>' for a, b in CLIENTS)

def testimonial_cards():
    return "".join(f'<article class="tcard"><svg class="ic q"><use href="#i-quote"/></svg><h3>{e(a)}</h3><span class="ind">{e(b)}</span><p>{e(c)}</p></article>'
                   for a, b, c in TESTIMONIALS)

# ---------------------------------------------------------------- pages
def home():
    rail = "".join(
        f'<a class="pcard" href="/projects/#{i["slug"]}"><div class="im">{img(i["im"][0][0], i["im"][0][1])}<span class="eye"><svg class="ic"><use href="#i-eye"/></svg></span></div>'
        f'<div class="body"><h3>{e(i["t"])}</h3><p class="meta">{e(i["c"])} · {len(i["im"])} photos</p><span class="go">View projects →</span></div></a>'
        for i in INDUSTRIES)
    body = f"""
  <section class="hero" aria-roledescription="carousel" aria-label="Highlights">
    <div class="slide on">
      {img("stack-bongaigaon","Banded steel stack shell on a trailer leaving the works",lazy=False)}
      <div class="cap"><div class="container"><div><span class="kick">Heavy Steel Fabrication · Odisha</span><h1>Heavy steel fabrication in Rajgangpur, Odisha.</h1><p>Stacks, ducts, fired-heater casings, boiler structures and RDSO-approved plate girders for India's refineries, steel plants, power stations and railways.</p><a class="btn" href="/contact/">Send Enquiry <i>↗</i></a></div></div></div>
    </div>
    <div class="slide">
      {img("shop-bays","Inside the fabrication bays with yellow EOT cranes")}
      <div class="cap"><div class="container"><div><span class="kick">Manufacturing Facility</span><h2>Two 96 m bays under 20 MT cranes.</h2><p>A five-acre works with CNC cutting, SAW welding, a 600 MT press and its own blasting and painting booth.</p><a class="btn" href="/facility/">Our Facility <i>↗</i></a></div></div></div>
    </div>
    <div class="slide">
      {img("heater-erection","Fired heater casing under erection at a refinery site")}
      <div class="cap"><div class="container"><div><span class="kick">Fired Heaters</span><h2>Trial-assembled at the shop, erected at site.</h2><p>Non-pressure parts for refinery heaters, built to client drawings under third-party inspection.</p><a class="btn" href="/products/fired-heater-non-pressure-parts/">Fired Heater Parts <i>↗</i></a></div></div></div>
    </div>
    <div class="slide">
      {img("rdso-girder-site","Steel plate girder span erected on bearings over a river, fabricated under RDSO approval",style="object-position:50% 40%")}
      <div class="cap"><div class="container"><div><span class="kick">RDSO Approved</span><h2>Plate and composite girders for bridges.</h2><p>On the RDSO approved list for steel plate girders, registered for 3,600 MT a year.</p><a class="btn" href="/products/bridge-girders-built-up-sections/">Bridge Girders <i>↗</i></a></div></div></div>
    </div>
    <div class="hero-ctl"><div class="container">
      <div class="dots" id="hero-dots"></div>
      <div class="arrows"><button type="button" id="h-prev" aria-label="Previous slide">‹</button><button type="button" id="h-next" aria-label="Next slide">›</button></div>
    </div></div>
  </section>

  <div class="marquee" aria-hidden="true"><div class="track" id="track"><span>Buck Stays</span><span>Steel Stacks</span><span>Fired Heater Casings</span><span>Flue Ducts</span><span>Crusher Hoppers</span><span>Plate Girders</span><span>Conveyor Galleries</span><span>Gas Collecting Mains</span><span>Non-Pressurised Tanks</span><span>Auto-Weld Beams</span></div></div>

  <section class="section">
    <div class="container about">
      <div class="collage">
        {img("shop-bays","Fabrication bay with overhead cranes and rolled shells",cls="main")}
        {img("cnc-cutting","CNC plasma and flame profile cutting machine",cls="inset")}
        <div class="ribbon"><b>17+</b><span>Years in<br>production</span></div>
      </div>
      <div>
        <span class="sub-title">About Our Company</span>
        <h2 class="title">Heavy Fabrication for India's Core Industries</h2>
        <p class="lead">Uni Profiles Pvt. Ltd., incorporated in 2009, runs a steel and alloy-steel fabrication works at Rajgangpur, Odisha, 40 km from Rourkela. We make heavy steel equipment and boiler auxiliary structures for BHEL, SAIL, Thermax, L&amp;T, Tata Projects and other leading engineering companies, with an annual capacity of 6,000 MT.</p>
        <a class="btn" href="/about/">Who We Are <i>↗</i></a>
      </div>
    </div>
  </section>

  <section class="section tint">
    <div class="container">
      <div class="head"><span class="sub-title">Products</span><h2 class="title">Fabricated to Your Drawing. Delivered to Your Schedule.</h2></div>
      {prod_cards()}
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="head center"><span class="sub-title">Projects</span><h2 class="title">Our Work, by Industry</h2></div>
      <div class="rail" id="prail">{rail}</div>
      <div class="rail-dots" id="pdots"></div>
    </div>
  </section>

  <section class="section tint" style="padding-block:80px">
    <div class="container">
      <div class="counters">
        <div class="cbox"><svg class="ic"><use href="#i-crane"/></svg><b>6,000+</b><span>MT annual capacity</span></div>
        <div class="cbox"><svg class="ic"><use href="#i-ruler"/></svg><b>96 m</b><span>Bay length, two bays</span></div>
        <div class="cbox"><svg class="ic"><use href="#i-users"/></svg><b>15+</b><span>Major industrial clients</span></div>
        <div class="cbox"><svg class="ic"><use href="#i-search"/></svg><b>10</b><span>Third-party inspection agencies</span></div>
        <div class="cbox"><svg class="ic"><use href="#i-cal"/></svg><b>2009</b><span>In production since</span></div>
      </div>
    </div>
  </section>

  <section class="section" style="padding-bottom:72px">
    <div class="container"><div class="head center"><span class="sub-title">Clients</span><h2 class="title">Our Esteemed Clients</h2></div></div>
    <div class="logos"><div class="lt" id="logos">{client_tiles()}</div></div>
    <div class="container center" style="margin-top:36px"><a class="btn" href="/clients/">Clients &amp; Testimonials <i>↗</i></a></div>
  </section>

  <section class="section tint">
    <div class="container">
      <div class="head center"><span class="sub-title">Approvals &amp; Certificates</span><h2 class="title">Registered With India's Leading Buyers</h2></div>
      {cert_cards(APPROVALS[:3])}
      <div class="center" style="margin-top:36px"><a class="btn" href="/approvals/">All Approvals <i>↗</i></a></div>
    </div>
  </section>
{cta()}"""
    page("/", "Uni Profiles Pvt. Ltd. | Heavy Steel Fabrication in Rajgangpur, Odisha",
         "Heavy steel and alloy-steel fabrication works at Rajgangpur, Odisha, near Rourkela. Boiler structures, steel stacks, fired-heater casings, ducts, tanks and RDSO-approved bridge girders. 6,000 MT a year.",
         body, home=True)

def about():
    body = banner("About Uni Profiles", "A steel and alloy-steel fabrication works at Rajgangpur, Odisha, making heavy equipment and boiler auxiliary structures since 2009.",
                  [("About Us", "/about/")], "shop-bays") + f"""
  <section class="section">
    <div class="container split">
      <div class="prose">
        <h2>Who we are</h2>
        <p>Uni Profiles Pvt. Ltd. is a Rourkela-based engineering group, incorporated in 2009, that operates a steel and alloy-steel fabrication unit at Rajgangpur in Sundargarh district, Odisha. The works is 40 km from Rourkela and 70 km from Jharsuguda airport.</p>
        <p>We fabricate heavy steel equipment and boiler auxiliary structures to client drawings, for EPC contractors and plant owners in power, steel, refining, railways and material handling. Our capacity is <strong>6,000 MT a year</strong>.</p>
        <h2>What we specialise in</h2>
        <ul>
          {"".join(f'<li><a href="/products/{p["slug"]}/"><strong>{e(p["name"])}</strong></a>: {e(p["teaser"][0].lower() + p["teaser"][1:])}</li>' for p in PRODUCTS)}
        </ul>
        <h2>Where we are</h2>
        <p>The works stands on five acres off SH-10 at Village Jharbeda, Rajgangpur, with 44,000 sq ft under roof in two 17 × 96 m bays and an open yard for trial assembly and trailer loading. <a href="/facility/">See the full facility and machinery list →</a></p>

        <h2 id="quality">Quality and inspection</h2>
        <p>We are certified to <strong>ISO 9001:2015</strong>. Inspection starts at material inward and continues as stage inspection through cutting, fit-up, welding, blasting and painting to the finished piece. Our QA/QC team includes certified NDT personnel and certified blasting and painting inspectors, works with calibrated instruments, and is sent for training through authorised organisations, including a painters' training programme run by Berger Paints at Bhilai.</p>
        <h3>Checks at the blasting and painting area</h3>
        <ul>
          <li>Blotter test for compressed-air quality</li>
          <li>Substrate dust contamination: adhesive tape test</li>
          <li>Soluble salt contamination: Bresle kit</li>
          <li>Calibrated wet- and dry-film thickness gauges</li>
          <li>Coating adhesion: cross-hatch cutter</li>
          <li>Calibrated surface profile gauge and roughness comparator</li>
          <li>Calibrated temperature and relative humidity meter</li>
        </ul>
        <h3>Third-party inspection</h3>
        <p>Beyond our customers' own inspectors, our work has been inspected by these agencies on behalf of clients:</p>
        <ul class="chips">{"".join(f"<li><span>{e(t)}</span></li>" for t in TPI)}</ul>
      </div>
      <aside class="aside">
        {img("duct-flange","Flanged duct under inspection in the shop")}
        <div class="box"><h3>At a glance</h3><ul>
          <li>Incorporated 2009</li><li>6,000 MT a year</li><li>5 acres, 44,000 sq ft covered</li><li>2 × 20 MT + 1 × 5 MT EOT cranes</li><li>ISO 9001:2015</li><li>RDSO, NTPC, SAIL RSP, BHEL approved</li></ul></div>
        <div class="box"><h3>Next</h3><ul><li><a href="/facility/">Facility &amp; machinery</a></li><li><a href="/approvals/">Approvals &amp; certificates</a></li><li><a href="/projects/">Projects by industry</a></li><li><a href="/clients/">Clients &amp; testimonials</a></li></ul></div>
      </aside>
    </div>
  </section>
{cta()}"""
    page("/about/", "About Us | Uni Profiles Pvt. Ltd., Heavy Steel Fabricators, Odisha",
         "Uni Profiles Pvt. Ltd., incorporated 2009, fabricates heavy steel equipment and boiler auxiliary structures at Rajgangpur, Odisha. ISO 9001:2015, stage inspection, 10 third-party inspection agencies.",
         body, cur="about", crumbs=[("About Us", "/about/")], og_img="shop-bays")

def facility():
    rows = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td><td>{e(d)}</td></tr>" for a, b, c, d in MACHINES)
    body = banner("Manufacturing Facility & Machinery", "Five acres at Rajgangpur, two 96 m bays under 20 MT cranes, an automated H-beam line and an in-house blasting and painting booth.",
                  [("About Us", "/about/"), ("Facility", "/facility/")], "shop-bays") + f"""
  <section class="section">
    <div class="container fac">
      <div>
        <span class="sub-title">Land &amp; Infrastructure</span>
        <h2 class="title">Built for Long, Heavy Pieces</h2>
        <p style="margin-top:16px">Both bays run 96 metres end to end under 20 MT cranes, so stack shells and girders move from cutting bed to paint booth without leaving the hook. We keep adding machines as orders demand.</p>
        <ul class="mlist">
          <li>Site area <span>5 acres</span></li>
          <li>Covered shed <span>44,000 sq ft</span></li>
          <li>Bays <span>2 × 17 × 96 m</span></li>
          <li>EOT cranes <span>2 × 20 MT, 1 × 5 MT</span></li>
          <li>Mobile cranes <span>2 × 12 MT</span></li>
          <li>CNC profile cutting <span>4 × 15 m</span></li>
          <li>Hydraulic press <span>600 MT</span></li>
          <li>Plate rolling <span>25 × 2,500 mm</span></li>
          <li>SAW welding <span>1,000 + 1,250 A</span></li>
          <li>MIG / ARC sets <span>17 / 21</span></li>
          <li>CNC drilling <span>Ø40 mm</span></li>
          <li>Power / DG <span>200 / 125 kVA</span></li>
        </ul>
      </div>
      <div class="fac-imgs">
        {img("shell-welding","Welder on a large rolled shell beside the CNC cutting bed")}
        {img("cnc-drill","Kotec CNC multi-axis drilling machine")}
        {img("cnc-cutting","CNC plasma and flame profile cutting machine")}
      </div>
    </div>
  </section>

  <section class="section tint">
    <div class="container split">
      <div class="prose">
        <h2>H-beam and built-up section line</h2>
        <p>For H-beams and built-up sections we run a complete line: CNC plasma and flame cutting of flanges and webs, an automated beam assembly machine (up to 2 m deep and 1 m wide), submerged-arc welding, and a hydraulic straightening machine that corrects flange distortion up to 80 mm thick. The same line feeds <a href="/products/boiler-conveyor-structures/">boiler structures and auto-weld beams</a> and <a href="/products/bridge-girders-built-up-sections/">plate girders</a>.</p>
        <h2>Plate forming</h2>
        <p>A plate bending (rolling) machine takes plate up to 25 mm thick and 2,500 mm wide for stack shells, casings and cylindrical tanks, and a 600 MT hydraulic press handles pressing and forming work.</p>
        <h2>Blasting and painting</h2>
        <p>Surface preparation and coating are done in-house, so pieces leave the works ready for erection.</p>
        <ul>
          <li>Blasting booth 12 × 6 × 5 m, Kulmech blasting hopper</li>
          <li>40 HP ELGI screw compressor at 7.5 kg/cm²; 8–10 mm nozzles at 7 kg/cm²</li>
          <li>Media: sand, copper slag, shot and grit</li>
          <li>Airless spray for paints up to 60% volume solids, pneumatic paint stirrer, and conventional spray on a 3 HP compressor</li>
        </ul>
        <p>Coating checks at this stage are listed under <a href="/about/#quality">quality and inspection</a>.</p>
      </div>
      <aside class="aside">
        {img("crane-lift","Three-crane tandem lift loading a fabricated piece onto a trailer")}
        <div class="box"><h3>Power</h3><ul><li>200 kVA connected load</li><li>125 kVA Cummins DG back-up</li></ul></div>
      </aside>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="head"><span class="sub-title">Plant &amp; Machinery</span><h2 class="title">Full Machinery List</h2></div>
      <div class="tbl-wrap"><table class="spec">
        <thead><tr><th>Machine</th><th>Make / model</th><th>Capacity</th><th>Nos.</th></tr></thead>
        <tbody>{rows}</tbody>
      </table></div>
    </div>
  </section>
{cta()}"""
    page("/facility/", "Fabrication Facility & Plant Machinery | Uni Profiles, Rajgangpur, Odisha",
         "5-acre fabrication works at Rajgangpur, Odisha: two 17 × 96 m bays, 2 × 20 MT EOT cranes, CNC cutting, H-beam line, SAW welding, 600 MT press, plate rolling and in-house blasting and painting.",
         body, cur="about", crumbs=[("About Us", "/about/"), ("Facility", "/facility/")], og_img="shop-bays")

def approvals():
    body = banner("Approvals & Certificates", "Registered with the railways' standards body, India's largest power producer, its largest steel maker and its largest boiler manufacturer.",
                  [("Approvals", "/approvals/")], "rdso-girder-site") + f"""
  <section class="section">
    <div class="container">
      {cert_cards()}
    </div>
  </section>
  <section class="section tint">
    <div class="container split">
      <div class="prose">
        <h2>What these approvals cover</h2>
        <p><strong>RDSO</strong> registration puts us on the approved list for open web, composite and steel plate girders under Parts A and B, at a registered capacity of 3,600 MT a year. See <a href="/products/bridge-girders-built-up-sections/">bridge girders</a>.</p>
        <p><strong>NTPC</strong> approval covers welded technological and building structures, auto-weld beams and bracings. We have also built silo cones for NTPC projects through BHEL. See <a href="/products/silos-hoppers-ducts/">silos, hoppers and ducts</a>.</p>
        <p><strong>SAIL, Rourkela Steel Plant</strong> lists us as a registered manufacturer for heavy structural fabrication, and <strong>BHEL Trichy</strong> has bought general fabrication, ducts, buck stays, auto-weld beams and columns from us since 2012. See <a href="/products/boiler-conveyor-structures/">boiler and conveyor structures</a>.</p>
        <p>Our quality system is certified to <strong>ISO 9001:2015</strong> for fabrication and machining of equipment, spares, technological structures and H-beams. <a href="/about/#quality">How we inspect →</a></p>
      </div>
      <aside class="aside"><div class="box"><h3>Need a copy?</h3><ul><li>Certificates and registration letters are available on request for vendor registration.</li><li><a href="/contact/">Ask for documents →</a></li></ul></div></aside>
    </div>
  </section>
{cta()}"""
    page("/approvals/", "Approvals: RDSO, NTPC, SAIL RSP, BHEL, ISO 9001:2015 | Uni Profiles",
         "Uni Profiles is RDSO-approved for steel plate and composite girders (3,600 MT/yr), NTPC-approved for technological structures, a registered SAIL RSP and BHEL Trichy vendor, and ISO 9001:2015 certified.",
         body, cur="approvals", crumbs=[("Approvals", "/approvals/")], og_img="rdso-girder-site")

def projects():
    blocks = "".join(
        f'<div class="ind-block" id="{i["slug"]}"><h2>{e(i["t"])}</h2><p class="meta">{e(i["c"])} · Related: '
        + ", ".join(f'<a href="/products/{s}/" style="color:var(--steel)">{e(PBY[s]["name"])}</a>' for s in i["prod"])
        + f'</p>{figs(i["im"])}</div>' for i in INDUSTRIES)
    jump = "".join(f'<li><a href="#{i["slug"]}">{e(i["t"])}</a></li>' for i in INDUSTRIES)
    body = banner("Projects", "Stacks, heater casings, buck stays, silos, girders and tanks we have fabricated, grouped by the industry they went to.",
                  [("Projects", "/projects/")], "crane-lift") + f"""
  <section class="section">
    <div class="container">
      <ul class="chips" style="margin-bottom:40px">{jump}</ul>
      {blocks}
    </div>
  </section>
{cta()}"""
    page("/projects/", "Projects: Refineries, Steel Plants, Power, Railways | Uni Profiles, Odisha",
         "Photographs of stacks for IOCL and BORL, coke-oven buck stays for SAIL RSP, silo cones for NTPC through BHEL, RDSO girders, crusher hoppers and process tanks fabricated by Uni Profiles.",
         body, cur="projects", crumbs=[("Projects", "/projects/")], og_img="crane-lift")

def clients():
    body = banner("Clients & Testimonials", "Power, steel, refinery, railway and EPC companies that buy fabrication from our Rajgangpur works.",
                  [("Clients", "/clients/")], "conveyor-gallery") + f"""
  <section class="section">
    <div class="container">
      <div class="head"><span class="sub-title">Clients</span><h2 class="title">Our Esteemed Clients</h2></div>
      <div class="lgrid">{client_tiles()}</div>
    </div>
  </section>
  <section class="section tint" id="testimonials" style="scroll-margin-top:84px">
    <div class="container">
      <div class="head"><span class="sub-title">Testimonials</span><h2 class="title">What Our Clients Say</h2></div>
      <div class="trail" id="trail">{testimonial_cards()}</div>
      <div class="rail-dots" id="tdots"></div>
    </div>
  </section>
{cta()}"""
    page("/clients/", "Clients & Testimonials | BHEL, SAIL, Thermax, L&T | Uni Profiles",
         "Uni Profiles fabricates for BHEL, SAIL Rourkela Steel Plant, Thermax, L&T ECC, Tata Projects, GE Power, thyssenkrupp, MECON, Hindalco and others. Read what BEC Bhilai, BHEL and Thermax say.",
         body, cur="clients", crumbs=[("Clients", "/clients/")], og_img="conveyor-gallery")

def contact():
    opts = "".join(f"<option>{e(p['name'])}</option>" for p in PRODUCTS) + "<option>Other</option>"
    body = banner("Contact Us", "Send your drawings, tonnage and delivery point. We reply with a quote.", [("Contact", "/contact/")], "shipment") + f"""
  <section class="section">
    <div class="container">
      <div class="enq">
        <div class="enq-info">
          <span class="sub-title" style="color:#fff">Get In Touch</span>
          <h2>Send us your drawings for a quote.</h2>
          <div class="row"><span class="ico"><svg class="ic"><use href="#i-phone"/></svg></span><div><b>Works · Sushant Kumar Hota</b><span><a href="tel:{TEL}">{PHONE}</a><br><a href="tel:+918249010494">{PHONE2}</a></span></div></div>
          <div class="row"><span class="ico"><svg class="ic"><use href="#i-mail"/></svg></span><div><b>Email</b><span><a href="mailto:{EMAIL2}">{EMAIL2}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></span></div></div>
          <div class="row"><span class="ico"><svg class="ic"><use href="#i-pin"/></svg></span><div><b>Works</b><span>{e(ADDR_SHORT)}<br><a href="https://www.google.com/maps/search/?api=1&amp;query=Uni+Profiles+Rajgangpur" target="_blank" rel="noopener" style="text-decoration:underline">Open in Google Maps</a></span></div></div>
          <div class="row"><span class="ico"><svg class="ic"><use href="#i-crane"/></svg></span><div><b>Getting here</b><span>40 km from Rourkela, 70 km from Jharsuguda airport</span></div></div>
        </div>
        <form class="enq-form" id="enq" novalidate>
          <h3>Enquiry Form</h3>
          <div><label for="e-name">Name</label><input id="e-name" name="name" autocomplete="name" required></div>
          <div><label for="e-co">Company</label><input id="e-co" name="company" autocomplete="organization"></div>
          <div><label for="e-ph">Phone</label><input id="e-ph" name="phone" type="tel" autocomplete="tel"></div>
          <div><label for="e-prod">Product</label><select id="e-prod" name="product">{opts}</select></div>
          <div class="full"><label for="e-msg">Scope, tonnage and delivery point</label><textarea id="e-msg" name="message" required></textarea></div>
          <div class="full"><button class="btn" type="submit">Prepare Email <i>↗</i></button></div>
          <p class="status" id="e-status" aria-live="polite"></p>
        </form>
      </div>
    </div>
  </section>"""
    page("/contact/", "Contact Uni Profiles | Steel Fabrication Enquiries, Rajgangpur, Odisha",
         "Send fabrication enquiries to Uni Profiles Pvt. Ltd., Plot 2045/P, Village Jharbeda, Rajgangpur, Odisha 770070. Call +91 94375 57166 or email sushant.hota@uniprofiles.in.",
         body, cur="contact", crumbs=[("Contact", "/contact/")], og_img="shipment")

def products_hub():
    body = banner("Products", "Heavy plate and structural fabrication to the client's drawing, in six product families.", [("Products", "/products/")], "beam-yard") + f"""
  <section class="section tint">
    <div class="container">{prod_cards()}</div>
  </section>
{cta()}"""
    page("/products/", "Products: Boiler Structures, Stacks, Heater Casings, Girders | Uni Profiles",
         "Six product families from Uni Profiles, Rajgangpur, Odisha: boiler and conveyor structures, steel stacks, fired-heater non-pressure parts, silos, hoppers and ducts, tanks, and RDSO bridge girders.",
         body, cur="products", crumbs=[("Products", "/products/")], og_img="beam-yard")

# Per-product body copy: only facts from the company profile, approvals and client letters.
PRODUCT_BODY = {
"boiler-conveyor-structures": dict(
  gallery=[("buckstay-cob","Buck stays for Coke Oven Battery 3, SAIL RSP, via BEC Bhilai"),("buckstay-bhel","Buck stay for BHEL Trichy"),("conveyor-gallery","Conveyor gallery for BHEL ISG"),("beam-yard","Built-up sections in the bay")],
  approvals=["NTPC","BHEL, Trichy","SAIL, Rourkela Steel Plant"],
  html="""
<h2>What we fabricate</h2>
<ul>
<li><strong>Buck stays</strong> for utility boilers and coke-oven batteries</li>
<li><strong>Columns, beams, girders and bracings</strong> for boiler and technological structures</li>
<li><strong>Auto-weld beams</strong> from our automated H-beam line</li>
<li><strong>Conveyor galleries, trestles and junction houses</strong> for raw-material handling systems</li>
</ul>
<h2>How we build them</h2>
<p>Flanges and webs are cut on a 4 × 15 m CNC plasma and flame profile cutter, fitted on an automated beam assembly machine (up to 2 m deep), welded on 1,000 A and 1,250 A submerged-arc machines, and straightened on a hydraulic flange straightener rated to 80 mm. Connection holes are drilled on a Kotec multi-axis CNC drill. Two 96 m bays under 20 MT EOT cranes let long members move through every stage without re-handling. <a href="/facility/">Full facility →</a></p>
<h2>Where they have gone</h2>
<p><strong>BHEL Trichy</strong> has bought general fabrication, ducts, buck stays, auto-weld beams, bracings and columns from us since 2012. <strong>Thermax</strong> has recorded our execution of columns, beams, girders and buck stays across several projects. For <strong>SAIL Rourkela Steel Plant</strong>, through Bhilai Engineering Corporation, we built buck stays for Coke Oven Battery 3. For <strong>BHEL Industrial Systems Group</strong> we fabricated and supplied RMHS trestles, galleries and a junction house for the Nagarnar steel plant project.</p>
<p>We are approved by <strong>NTPC</strong> for welded technological and building structures, auto-weld beams and bracings.</p>
"""),
"steel-stacks-chimneys": dict(
  gallery=[("stack-bongaigaon","IOCL Bongaigaon · stack shell 3 leaving the works"),("stack-iocl","IOCL · stack base and shell segments"),("chimney-borl","BORL · chimney after erection"),("chimney-site","Chimney · two segments erected"),("stack-shell-b","Stack shell · stiffened base flange"),("crane-lift","Three-crane tandem lift onto trailer")],
  approvals=["ISO 9001:2015","SAIL, Rourkela Steel Plant"],
  html="""
<h2>What we fabricate</h2>
<ul>
<li><strong>Self-supporting steel stacks</strong> in rolled shell segments with flanged joints</li>
<li><strong>Chimneys</strong> for refinery and process plants, with stiffened base flanges</li>
<li><strong>Platforms and ladders</strong> fabricated with the shells</li>
</ul>
<h2>How we build them</h2>
<p>Shell plates are profile-cut on CNC and rolled on our plate bending machine (up to 25 mm thick and 2,500 mm wide), then longitudinal and circumferential seams are welded and flanges fitted for bolted joints at site. Each segment is blasted in our 12 × 6 × 5 m booth, painted with airless spray, checked for film thickness and adhesion, then banded and loaded onto trailers, using a tandem lift for the heaviest shells.</p>
<h2>Where they have gone</h2>
<p>We have fabricated stack shells for <strong>IOCL</strong>, including the Bongaigaon refinery, and a chimney for <strong>BORL</strong> that has since been erected at site. Stacks were also part of more than 4,000 tons of complex structures supplied to <strong>Bhilai Engineering Corporation</strong> over five years.</p>
"""),
"fired-heater-non-pressure-parts": dict(
  gallery=[("heater-trial","Fired heater casing · trial assembly at the works"),("heater-erection","Fired heater · erection at a refinery site"),("fired-heater-duct","Large heater duct assembly, painted"),("tube-module","Tube bank in fabricated casing")],
  approvals=["ISO 9001:2015"],
  html="""
<h2>What we fabricate</h2>
<ul>
<li><strong>Radiant and convection section casings</strong></li>
<li><strong>Structural frames</strong> supporting the heater</li>
<li><strong>Ducting</strong> for heater sections</li>
<li><strong>Casings around tube banks</strong></li>
</ul>
<h2>How we build them</h2>
<p>Heater casings are built to the client's drawings and <strong>trial-assembled in the shop</strong> before dispatch, so fit-up problems are found in Rajgangpur rather than on a refinery site. Sections are then blasted, painted and shipped for erection. Stage inspection runs from material inward to dispatch, and the work is open to the client's third-party inspector at every stage.</p>
<h2>Where they have gone</h2>
<p><strong>Thermax</strong>, through its boiler and heater division, has recorded our execution of ducting and heater casings across several projects, with thanks for holding schedule and quality. Our refinery work, including heaters now erected at site, is shown under <a href="/projects/#refineries">refinery projects</a>.</p>
"""),
"silos-hoppers-ducts": dict(
  gallery=[("ntpc-silo","Silo cone with radial gussets · BHEL for NTPC"),("crusher-hopper","Crusher hopper in stiffened plate"),("hopper-pyramid","Pyramid crusher hopper"),("crusher-stand","Crusher stand"),("duct-flange","Flanged duct with internal bracing"),("gas-main","Gas collecting main · coke ovens")],
  approvals=["NTPC","BHEL, Trichy"],
  html="""
<h2>What we fabricate</h2>
<ul>
<li><strong>Silo cones and bunkers</strong> with radial gussets and stiffeners</li>
<li><strong>Crusher hoppers</strong>, including pyramid hoppers, and <strong>crusher stands</strong></li>
<li><strong>Flue and gas ducts</strong>: large flanged sections with internal bracing</li>
<li><strong>Gas collecting mains</strong> for coke-oven batteries</li>
<li><strong>Chutes</strong> for material handling</li>
</ul>
<h2>How we build them</h2>
<p>This is heavy plate-work. Plates are CNC-cut, rolled or pressed (600 MT hydraulic press), and assembled with stiffeners in bays long enough to build large duct sections and cones in one piece. Flange faces and internal bracing are checked before blasting and painting, and pieces are sized for road transport to site.</p>
<h2>Where they have gone</h2>
<p>We have built silo cones for <strong>NTPC</strong> projects through <strong>BHEL</strong>, and ducts for <strong>BHEL Trichy</strong> since 2012. Ducts and gas mains were part of more than 4,000 tons of structures supplied to <strong>Bhilai Engineering Corporation</strong>, including a gas collecting main for Coke Oven Battery 3 at SAIL Rourkela Steel Plant.</p>
"""),
"non-pressurised-tanks": dict(
  gallery=[("tank-shop","Non-pressurised tank with internals in the bay"),("bath-tank","Bath tank for Tata Aerospace Systems (SECO)"),("overhead-tank","Overhead tank for L&T ECC, Kansbahal"),("drainage-tank","Drainage tank for Coke Oven Battery 3")],
  approvals=["ISO 9001:2015"],
  html="""
<h2>What we fabricate</h2>
<ul>
<li><strong>Process vessels and tanks with internals</strong>, such as internal grids and flanged openings</li>
<li><strong>Overhead tanks</strong> with their support structures</li>
<li><strong>Drainage tanks</strong> for steel-plant service</li>
<li><strong>Stiffened rectangular bath tanks</strong> for industrial process lines</li>
</ul>
<h2>How we build them</h2>
<p>Cylindrical shells are rolled on our plate bending machine and handled on rollers in the bay for seam welding; rectangular tanks are built up from stiffened plate panels. Internals and nozzles are fitted before blasting and painting, so the tank leaves the works complete.</p>
<h2>Where they have gone</h2>
<p>We have built a bath tank for <strong>Tata Aerospace Systems</strong> (through SECO), an overhead tank for <strong>L&amp;T ECC</strong> at Kansbahal, and a drainage tank for Coke Oven Battery 3 at <strong>SAIL Rourkela Steel Plant</strong>.</p>
"""),
"bridge-girders-built-up-sections": dict(
  gallery=[("rdso-girder-site","RDSO plate girder span erected on bearings"),("truss-girder","Through-truss girder · trial assembly in the yard"),("rob-assembly","ROB girder control assembly for Rawatsons Engineers"),("beam-yard","Built-up sections in the bay")],
  approvals=["RDSO","NTPC","ISO 9001:2015"],
  html="""
<h2>What we fabricate</h2>
<ul>
<li><strong>Steel plate girders</strong> for railway bridges, under RDSO approval</li>
<li><strong>Composite girders</strong></li>
<li><strong>Open web (through-truss) girders</strong>, trial-assembled in our yard</li>
<li><strong>Road-over-bridge (ROB) girders</strong></li>
<li><strong>H-beams and built-up sections</strong> from our automated beam line</li>
</ul>
<h2>RDSO approval</h2>
<p>Uni Profiles is on the RDSO approved list for open web, composite and other steel plate girders under <strong>Parts A and B</strong>, at a registered capacity of <strong>3,600 MT a year</strong>. <a href="/approvals/">All approvals →</a></p>
<h2>How we build them</h2>
<p>Flanges and webs are CNC-cut and assembled on the beam line, welded by submerged arc, and straightened before stiffeners and splice plates are fitted. Open web girders are <strong>control-assembled in our yard</strong> to check camber, alignment and hole match before dispatch.</p>
<h2>Where they have gone</h2>
<p>Our plate girders have been erected on bridge bearings at site, and we have control-assembled road-over-bridge girders for <strong>Rawatsons Engineers</strong>, Kolkata. See <a href="/projects/#railways-bridges">railway and bridge projects</a>.</p>
"""),
}

def product_page(p):
    b = PRODUCT_BODY[p["slug"]]
    rel_ind = [i for i in INDUSTRIES if p["slug"] in i["prod"]]
    appr = [a for a in APPROVALS if a[0] in b["approvals"]]
    others = [q for q in PRODUCTS if q["slug"] != p["slug"]]
    body = banner(p["h1"], e(p["lede"]), [("Products", "/products/"), (p["name"], f"/products/{p['slug']}/")], p["card"]) + f"""
  <section class="section">
    <div class="container split">
      <div class="prose">{b["html"]}
        <h2>Photographs</h2>
        {figs(b["gallery"])}
      </div>
      <aside class="aside">
        <div class="box"><h3>Relevant approvals</h3><ul>{"".join(f'<li><strong>{e(t)}</strong>: {e(d)}</li>' for t, d, r in appr)}<li><a href="/approvals/">All approvals →</a></li></ul></div>
        <div class="box"><h3>Industries</h3><ul>{"".join(f'<li><a href="/projects/#{i["slug"]}">{e(i["t"])}</a></li>' for i in rel_ind)}</ul></div>
        <div class="box"><h3>Other products</h3><ul>{"".join(f'<li><a href="/products/{q["slug"]}/">{e(q["name"])}</a></li>' for q in others)}</ul></div>
        <a class="btn" href="/contact/?product={e(p['name'])}">Enquire About This <i>↗</i></a>
      </aside>
    </div>
  </section>
{cta(sub="Send drawings, tonnage and delivery point for " + e(p['short'].lower()) + ".", product=p['name'])}"""
    service = {"@type": "Service", "name": p["name"], "serviceType": "Steel fabrication", "description": p["desc"],
               "provider": {"@id": SITE + "/#org"}, "areaServed": {"@type": "Country", "name": "India"},
               "url": f"{SITE}/products/{p['slug']}/"}
    page(f"/products/{p['slug']}/", p["title"], p["desc"], body, cur="products",
         crumbs=[("Products", "/products/"), (p["name"], f"/products/{p['slug']}/")], og_img=p["card"], extra_ld=[service])

def sitemap():
    pri = lambda u: "1.0" if u == "/" else ("0.9" if u.startswith("/products/") else "0.7")
    urls = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{pri(u)}</priority></url>" for u in PAGES)
    with open(os.path.join(PUB, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    with open(os.path.join(PUB, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")

if __name__ == "__main__":
    home(); about(); facility(); approvals(); products_hub()
    for p in PRODUCTS: product_page(p)
    projects(); clients(); contact(); sitemap()
    print(f"built {len(PAGES)} pages")
