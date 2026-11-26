"""Build the public site as plain HTML. No npm."""
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "src" / "content"
DATA = ROOT / "src" / "data"
OUT = ROOT

SCHOLAR = "https://scholar.google.com/citations?hl=en&user=Ba2uOMsAAAAJ"
LINKEDIN = "https://www.linkedin.com/in/marcelinus-adhiwibawa/"
ORCID = "https://orcid.org/0000-0002-2191-7411"
SCOPUS = "https://www.scopus.com/authid/detail.uri?authorId=56123256300"
GITHUB = "https://github.com/Alfasisurya"
EMAIL = "marcelinus.setya@gmail.com"
NAME = "Marcelinus Alfasisurya Setya Adhiwibawa"
FULL = f"{NAME}, M.Stat."
ROLE = "Multidisciplinary Data Scientist"
TAGLINE = "Statistical Science | Machine Learning | Computational Intelligence"

NAV = [
    ("about.html", "About"),
    ("expertise.html", "Expertise"),
    ("projects.html", "Research"),
    ("publications.html", "Publications"),
    ("showcases.html", "Showcases"),
    ("patents.html", "Patents"),
    ("explorations.html", "Explorations"),
    ("contact.html", "Contact"),
]


def esc(value):
    return html.escape(str(value), quote=True)


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    _, front, body = text.split("---", 2)
    data = {}
    key = None
    for line in front.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - "):
            data.setdefault(key, []).append(unquote(line[4:]))
            continue
        name, _, raw = line.partition(":")
        name, raw = name.strip(), raw.strip()
        key = name
        if raw == "":
            data[name] = []
        elif raw in ("true", "false"):
            data[name] = raw == "true"
        elif raw.isdigit():
            data[name] = int(raw)
        else:
            data[name] = unquote(raw)
    return data, body.strip()


def load(kind):
    folder = CONTENT / kind
    items = []
    for path in sorted(folder.glob("*.md")):
        meta, body = parse(path)
        meta["slug"] = path.stem
        meta["body"] = body
        items.append(meta)
    return items


def load_json(name):
    path = DATA / name
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def inline(text):
    text = esc(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def markdown(body, depth):
    prefix = "../" * depth
    lines = body.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            block = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i])
                i += 1
            out.append("<pre><code>" + esc("\n".join(block)) + "</code></pre>")
        elif line.startswith("<"):
            chunk = [line.replace('src="/', f'src="{prefix}')]
            i += 1
            while i < len(lines) and lines[i].startswith("<"):
                chunk.append(lines[i].replace('src="/', f'src="{prefix}'))
                i += 1
            out.append("\n".join(chunk))
            continue
        elif line.startswith("## "):
            out.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("# "):
            out.append(f"<h2>{inline(line[2:])}</h2>")
        elif line.startswith("> "):
            quote = [line[2:]]
            i += 1
            while i < len(lines) and lines[i].startswith("> "):
                quote.append(lines[i][2:])
                i += 1
            out.append("<blockquote><p>" + inline(" ".join(quote)) + "</p></blockquote>")
            continue
        elif line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append("<li>" + inline(lines[i][2:]) + "</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        elif line.strip() == "":
            pass
        else:
            para = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "-", ">", "`", "<")):
                para.append(lines[i])
                i += 1
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            continue
        i += 1
    return "\n".join(out)


def href(depth, target):
    return "../" * depth + target


def layout(title, description, depth, active, body):
    here = href(depth, "")
    links = []
    for target, label in NAV:
        current = ' aria-current="page"' if target == active else ""
        links.append(f'<a href="{href(depth, target)}"{current}>{label}</a>')
    page_title = FULL if title == FULL else f"{title} · {FULL}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(page_title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="author" content="{esc(FULL)}">
  <link rel="icon" href="{href(depth, "favicon.svg")}">
  <link rel="stylesheet" href="{href(depth, "css/site.css")}?v=8">
</head>
<body>
  <a class="skip" href="#content">Skip to content</a>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="{href(depth, "index.html")}" aria-label="Home">
        <span class="monogram" aria-hidden="true">MA</span>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false">Menu</button>
      <nav class="nav" aria-label="Primary">{"".join(links)}<button class="theme-btn" type="button">Theme</button></nav>
    </div>
  </header>
  <main id="content">{body}</main>
  <footer class="site-footer">
    <div class="wrap footer-inner">
      <nav class="footer-links" aria-label="Profiles">
        <a href="{SCHOLAR}">Google Scholar</a>
        <a href="{ORCID}">ORCID</a>
        <a href="{LINKEDIN}">LinkedIn</a>
        <a href="{GITHUB}">GitHub</a>
        <a href="{SCOPUS}">Scopus</a>
        <a href="{href(depth, "blog.html")}">Blog</a>
        <a href="{href(depth, "analysis.html")}">Analytical work</a>
      </nav>
      <p class="footer-note">© 2026 · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
  </footer>
  <script src="{href(depth, "js/site.js")}"></script>
</body>
</html>
"""


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def scholar_link(title):
    return "https://scholar.google.com/scholar?q=" + html.escape(f'"{title}" Adhiwibawa', quote=True)


def paper_links(item):
    links = []
    if item.get("url"):
        links.append((item["url"], "DOI" if item.get("doi") else "Paper"))
    elif item.get("doi"):
        links.append((f"https://doi.org/{item['doi']}", "DOI"))
    links.append((f'https://scholar.google.com/scholar?q={requests_quote(item["title"])}', "Google Scholar"))
    return links


def requests_quote(title):
    from urllib.parse import quote
    return quote(f'"{title}" Adhiwibawa')


MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def nice_date(value):
    match = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", str(value))
    if not match:
        return str(value)
    year, month, day = match.groups()
    return f"{int(day)} {MONTHS[int(month) - 1]} {year}"


def patent_link(item):
    url = item.get("url")
    if url and "pdki-indonesia" in url:
        return url, "PDKI record (DJKI)"
    if url and "/patent/" in url:
        return url, "Google Patents"
    return "https://patents.google.com/?q=" + requests_quote(item.get("number", item["title"])), "Search Google Patents"


def entry_list(items, depth, section):
    rows = []
    for item in items:
        page = href(depth, f"{section}/{item['slug']}/index.html")
        year = item.get("year") or item.get("period") or ""
        kicker = item.get("type") or item.get("category") or item.get("status") or item.get("jurisdiction") or ""
        if section == "blog":
            kicker = nice_date(item.get("date", ""))
        summary = item.get("summary") or item.get("venue") or ""
        extra = ""
        if section == "publications":
            bits = "".join(f'<a href="{esc(url)}">{esc(label)}</a>' for url, label in paper_links(item))
            extra = f'<p class="out-links">{bits}</p>'
        if section == "patents":
            url, label = patent_link(item)
            extra = f'<p class="out-links"><a href="{esc(url)}">{label}</a></p>'
        rows.append(
            f'<li data-item data-year="{esc(year)}" data-topics="{"|".join(esc(t) for t in item.get("domains") or item.get("topics") or [])}" '
            f'data-text="{esc((item["title"] + " " + summary).lower())}">'
            f'<div class="block-link"><span class="meta">{esc(kicker) if section == "blog" else esc(year) + "<br>" + esc(kicker)}</span>'
            f'<span><h3><a href="{page}">{esc(item["title"])}</a></h3><p>{esc(summary)}</p>{extra}</span></div></li>'
        )
    return '<ul class="entry-list">' + "".join(rows) + "</ul>"


def detail(item, depth, kicker, facts):
    fact_html = "".join(f"<li><span>{esc(label)}</span><span>{value}</span></li>" for label, value in facts if value)
    note = ""
    return f'''<article>
      <header class="page-head"><div class="wrap-narrow">
        <p class="kicker">{esc(kicker)}</p>
        <h1>{esc(item["title"])}</h1>
        <ul class="facts">{fact_html}</ul>
        {note}
      </div></header>
      <div class="wrap-narrow prose">{markdown(item["body"], depth)}</div>
    </article>'''


def sort_showcases(items):
    return sorted(
        items,
        key=lambda item: (0 if item.get("featured") else 1, -int(str(item.get("year") or 0) or 0), item.get("title", "")),
    )


def showcase_actions(item):
    actions = []
    demo = item.get("demoUrl") or ""
    if demo:
        external = demo.startswith("http://") or demo.startswith("https://")
        attrs = ' target="_blank" rel="noopener"' if external else ""
        label = "Open live demo" if external else "Open showcase"
        suffix = ' <span class="sr-only">(opens in a new tab)</span>' if external else ""
        actions.append(f'<a class="btn btn-primary" href="{esc(demo)}"{attrs}>{label}{suffix}</a>')
    if item.get("repoUrl"):
        actions.append(
            f'<a class="btn btn-secondary" href="{esc(item["repoUrl"])}" target="_blank" rel="noopener">'
            f'Source code <span class="sr-only">(opens in a new tab)</span></a>'
        )
    return "".join(actions)


def showcase_feature(item, depth=0):
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in (item.get("technologies") or []))
    image = ""
    if item.get("image"):
        image = (
            f'<img class="feature-img" src="{esc(href(depth, item["image"]))}" '
            f'alt="Screenshot of {esc(item["title"])}" width="960" height="600">'
        )
    meta = " · ".join(esc(bit) for bit in [item.get("status"), item.get("year")] if bit)
    return (
        f'<article class="feature">'
        f'<div class="feature-media">{image}</div>'
        f'<div class="feature-body">'
        f'<p class="meta">{meta}</p>'
        f'<h3>{esc(item["title"])}</h3>'
        f'<p>{esc(item.get("description", ""))}</p>'
        f'<div class="tag-row">{tags}</div>'
        f'<div class="action-row">{showcase_actions(item)}</div>'
        f'</div></article>'
    )


def showcase_cards(items, depth=0):
    ordered = sort_showcases(items)
    if not ordered:
        return ""
    first, rest = ordered[0], ordered[1:]
    html_out = showcase_feature(first, depth)
    if rest:
        cards = []
        for item in rest:
            tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in (item.get("technologies") or []))
            image = ""
            if item.get("image"):
                image = (
                    f'<img class="card-img" src="{esc(href(depth, item["image"]))}" '
                    f'alt="Screenshot of {esc(item["title"])}" loading="lazy" width="640" height="360">'
                )
            meta = " · ".join(esc(bit) for bit in [item.get("status"), item.get("year")] if bit)
            cards.append(
                f'<article class="card">{image}<div class="card-body">'
                f'<p class="meta">{meta}</p><h3>{esc(item["title"])}</h3>'
                f'<p>{esc(item.get("description", ""))}</p>'
                f'<div class="tag-row">{tags}</div>'
                f'<div class="action-row">{showcase_actions(item)}</div>'
                f'</div></article>'
            )
        html_out += '<div class="card-grid">' + "".join(cards) + "</div>"
    return html_out


def exploration_cards(items, detailed=False):
    cards = []
    for item in items:
        tags = "".join(f'<span class="tag">{esc(m)}</span>' for m in (item.get("methods") or []))
        question = f'<p>{esc(item.get("question", ""))}</p>' if detailed else ""
        cards.append(
            f'<article class="explore-card">'
            f'<p class="status">{esc(item.get("status", "Idea"))}</p>'
            f'<h3>{esc(item["title"])}</h3>'
            f'{question}'
            f'<div class="tag-row">{tags}</div>'
            f'</article>'
        )
    return '<div class="explore-grid">' + "".join(cards) + "</div>"


def compact_pubs(items):
    rows = []
    for item in items:
        link = item.get("url") or (f"https://doi.org/{item['doi']}" if item.get("doi") else "")
        doi = f' · <a href="{esc(link)}">DOI</a>' if link else ""
        rows.append(
            f'<li><span class="pub-year">{esc(item.get("year", ""))}</span>'
            f'<span><a class="pub-title" href="publications/{item["slug"]}/index.html">{esc(item["title"])}</a>'
            f'<span class="pub-venue">{esc(item.get("venue", ""))}{doi}</span></span></li>'
        )
    return '<ol class="pub-list">' + "".join(rows) + "</ol>"


def compact_patents(items):
    families = {}
    for item in items:
        families.setdefault(item["title"], []).append(item)
    rows = []
    for title, members in sorted(families.items(), key=lambda kv: -len(kv[1])):
        members.sort(key=lambda i: (0 if str(i.get("status", "")).startswith("Granted") else 1, i.get("number", "")))
        numbers = []
        for item in members:
            status = str(item.get("status", "")).split(" ")[0].rstrip(",")
            kind = "granted" if status == "Granted" else "filed"
            numbers.append(
                f'<a class="patent-no {kind}" href="patents/{item["slug"]}/index.html">'
                f'<span class="badge">{esc(status)}</span>{esc(item.get("number", ""))}</a>'
            )
        rows.append(f'<li class="patent-row"><p class="patent-title">{esc(title)}</p><div class="patent-nos">{"".join(numbers)}</div></li>')
    return '<ul class="patent-list">' + "".join(rows) + "</ul>"


def build():
    publications = sorted(load("publications"), key=lambda item: (-item.get("year", 0), item["title"]))
    projects = load("projects")
    analyses = load("analysis")
    patents = load("patents")
    posts = load("blog")
    showcases = load_json("showcases.json")
    explorations = load_json("explorations.json")
    for item in posts:
        item["year"] = str(item.get("date", ""))[:4]
    posts.sort(key=lambda item: str(item.get("date", "")), reverse=True)

    if (ROOT / "public" / "images").exists():
        shutil.copytree(ROOT / "public" / "images", ROOT / "images", dirs_exist_ok=True)
    if (ROOT / "public" / "favicon.svg").exists():
        shutil.copyfile(ROOT / "public" / "favicon.svg", ROOT / "favicon.svg")

    photo = "images/profile/foto_marcel.jpg"
    featured_projects = [item for item in projects if item.get("featured")]
    featured_papers = [item for item in publications if item.get("featured")]
    featured_analysis = [item for item in analyses if item.get("featured")]
    featured_showcases = [item for item in showcases if item.get("featured")] or showcases[:1]

    home = f'''
    <section class="hero"><div class="wrap hero-layout">
      <div class="hero-text">
        <p class="kicker">{esc(ROLE)}</p>
        <h1>{esc(NAME)}<span class="cred">, M.Stat.</span></h1>
        <p class="tagline">Statistical science · Machine learning · Computational intelligence</p>
        <p class="lede">I turn complex scientific data into knowledge people can act on. Trained in agricultural science and statistics, I work with field trials, spectra, plant images, satellite data, and sensors, and build the models and tools that help researchers and growers decide.</p>
        <div class="cta-row">
          <a class="btn btn-primary" href="projects.html">Explore my work</a>
          <a class="btn btn-secondary" href="showcases.html">Try a live demo</a>
        </div>
      </div>
      <figure class="hero-photo">
        <img class="portrait" src="{photo}" width="640" height="640" alt="Portrait photograph">
      </figure>
    </div>
    <div class="wrap">
      <dl class="stats">
        <div><dt>Years in applied research</dt><dd>15+</dd></div>
        <div><dt>Publications</dt><dd>{len(publications)}</dd></div>
        <div><dt>Citations</dt><dd>239</dd></div>
        <div><dt>h-index</dt><dd>7</dd></div>
        <div><dt>Granted patents</dt><dd>{sum(1 for p in patents if str(p.get("status", "")).startswith("Granted"))}</dd></div>
      </dl>
      <p class="stats-source">Citation figures from <a href="{SCHOLAR}">Google Scholar</a>, 22 November 2026.</p>
    </div></section>

    <section class="section"><div class="wrap">
      <div class="section-head">
        <p class="kicker">What I do</p>
        <h2>Two fields of depth, one set of methods</h2>
      </div>
      <div class="pillars">
        <article class="pillar">
          <p class="pillar-num">01</p>
          <h3>Life science &amp; environmental analytics</h3>
          <p>Agricultural data systems, plant imaging, remote sensing, drone mapping, and climate screening that support field decisions.</p>
        </article>
        <article class="pillar">
          <p class="pillar-num">02</p>
          <h3>Chemistry &amp; spectral intelligence</h3>
          <p>Chemometrics, NIR spectroscopy, pigment analysis, and low-cost optical sensors that turn spectra into measurements.</p>
        </article>
        <article class="pillar pillar-methods">
          <p class="pillar-num">03</p>
          <h3>Methods that work across fields</h3>
          <p>Forecasting and time-series modelling, statistical modelling and inference, multivariate analysis (PCA, PLSR), experimental design, machine learning, Python and R, geospatial pipelines, and sensor prototyping.</p>
        </article>
      </div>
      <p class="more"><a href="expertise.html">How the expertise is mapped →</a></p>
    </div></section>

    <section class="section"><div class="wrap">
      <div class="section-head">
        <p class="kicker">Research &amp; projects</p>
        <h2>Selected work</h2>
      </div>
      {entry_list(featured_projects, 0, "projects")}
      <p class="more"><a href="projects.html">All research and projects →</a></p>
    </div></section>

    <section class="section"><div class="wrap">
      <div class="section-head">
        <p class="kicker">Publications</p>
        <h2>Peer-reviewed research</h2>
      </div>
      {compact_pubs(featured_papers[:5])}
      <p class="more"><a href="publications.html">All {len(publications)} publications →</a></p>
    </div></section>

    <section class="section section-tint" id="live-showcases"><div class="wrap">
      <div class="section-head">
        <p class="kicker">Live demonstrations</p>
        <h2>From research to a working tool</h2>
      </div>
      {showcase_cards(showcases, 0)}
      <p class="more"><a href="showcases.html">All live showcases →</a></p>
    </div></section>

    <section class="section"><div class="wrap">
      <div class="section-head">
        <p class="kicker">Patents</p>
        <h2>Intellectual contributions</h2>
      </div>
      {compact_patents(patents)}
      <p class="more"><a href="patents.html">Patent details →</a></p>
    </div></section>

    <section class="section"><div class="wrap">
      <div class="section-head">
        <p class="kicker">Explorations</p>
        <h2>Where I am heading next</h2>
        <p class="intro">Areas I am studying, not yet established professional work.</p>
      </div>
      {exploration_cards(explorations)}
      <p class="more"><a href="explorations.html">Read the research questions →</a></p>
    </div></section>

    <section class="section contact-band"><div class="wrap contact-inner">
      <div>
        <p class="kicker">Contact</p>
        <h2>Let’s talk about data</h2>
        <p class="intro">Open to research collaboration and data science roles.</p>
      </div>
      <div class="cta-row">
        <a class="btn btn-primary" href="mailto:{EMAIL}">Email me</a>
        <a class="btn btn-secondary" href="{LINKEDIN}">LinkedIn</a>
      </div>
    </div></section>'''
    write(
        OUT / "index.html",
        layout(
            FULL,
            f"{FULL}, multidisciplinary data scientist working across statistical science, machine learning, and computational systems.",
            0,
            "index.html",
            home,
        ),
    )

    about = f'''<header class="page-head"><div class="wrap">
      <p class="kicker">About</p>
      <h1>From the field to the model</h1>
      <p class="lede">I started in plant protection on oil-palm plantations, moved into research on pigments, imaging, and low-cost sensors, and now build agricultural data systems for cocoa research at Mondelēz International.</p>
    </div></header>
    <section class="section"><div class="wrap prose-cols">
      <p>My foundation is agricultural science and statistics, both from Brawijaya University. That combination shapes how I work: I start from how the data were measured in the field or the lab, then choose the statistical or machine-learning method that answers the question honestly.</p>
      <p>Over the years I have combined statistical modelling, chemometrics, image analysis, remote sensing, and sensor prototyping to turn measurements into usable knowledge. The work has produced {len(publications)} papers, two granted patents, mobile tools such as the soybean leaf app Mata Daun, and the open Agronomic Intelligence platform.</p>
      <p>Next, I want to carry the same methods into other data-rich fields, such as finance, supply chains, measurement science, and food analytics. Those directions are listed separately under <a href="explorations.html">Explorations</a>.</p>
    </div></section>
    <section class="section"><div class="wrap">
      <h2>Career</h2>
      <ol class="timeline">
        <li><span class="meta">2021–present<br>Indonesia</span><div><h3>Agricultural Data System Scientist</h3><p class="org">Mondelēz International</p><ul><li>Agricultural data science and analytics for cocoa research.</li><li>Co-inventor of US Patent 12,444,511 on predicting cocoa-leaf nutrients from spectrometry data.</li></ul></div></li>
        <li><span class="meta">2012–2021<br>Malang, Indonesia</span><div><h3>Research Scientist</h3><p class="org">Ma Chung Research Center for Photosynthetic Pigments</p><ul><li>Research in bioimaging, chemometrics, natural pigments, and agricultural image analysis.</li><li>Built mobile applications that estimate plant nutrient status from leaf images, including the soybean application Mata Daun.</li><li>Applied CNN, ANFIS, and ANN models to species identification and pigment prediction.</li><li>Designed and fabricated low-cost multispectral sensors, photometers, and chlorophyll meters.</li></ul></div></li>
        <li><span class="meta">2010–2012<br>Indonesia</span><div><h3>Plant Monitoring and Advisory</h3><p class="org">PT Tintin Boyok Sawit Makmur (Barito Pacific Group)</p><ul><li>Field agronomic research and data-based monitoring for oil-palm plantations.</li></ul></div></li>
        <li><span class="meta">2009–2010<br>Indonesia</span><div><h3>Plantation Protection Staff</h3><p class="org">PT Astra Agro Lestari Tbk</p><ul><li>Pest and disease data analysis for oil palm.</li><li>Supported an e-learning system for plantation protection officers and the setup of the plant-protection laboratory at Kumai Research Center.</li></ul></div></li>
      </ol>
    </div></section>
    <section class="section"><div class="wrap">
      <h2>Education</h2>
      <ol class="timeline">
        <li><span class="meta">2016–2020</span><div><h3>Master of Statistics (M.Stat.)</h3><p class="org">Brawijaya University, Malang. GPA 3.60 / 4.00</p></div></li>
        <li><span class="meta">2003–2009</span><div><h3>Bachelor of Agriculture (S.P.), Plant Pest and Disease</h3><p class="org">Brawijaya University, Malang. GPA 3.35 / 4.00</p></div></li>
        <li><span class="meta">2007</span><div><h3>Harvard Summer School, Biodiversity of Borneo</h3><p class="org">CTFS Scholarship</p></div></li>
      </ol>
      <h2>Awards and grants</h2>
      <ul>
        <li>CTFS Harvard University Scholarship for the 2007 Harvard Summer School programme Biodiversity of Borneo.</li>
        <li>Asian Agri research grant for a biodiversity assessment, approximately USD 11,000.</li>
        <li>Insentif Sistem Inovasi Nasional (Insinas) grant, Ministry of Research and Technology, 2015, as team leader (USD 12,500).</li>
      </ul>
      <p>Languages: Indonesian (native) and English (professional working proficiency).</p>
    </div></section>'''
    write(OUT / "about.html", layout("About", f"Career and education of {FULL}", 0, "about.html", about))

    contact = f'''<header class="page-head"><div class="wrap">
      <p class="kicker">Contact</p><h1>Get in touch</h1>
      <p class="lede">For research collaboration or professional enquiries, email is the best way to reach me.</p>
    </div></header>
    <section class="section"><div class="wrap"><ul class="facts">
      <li><span>Location</span><span>Malang, Indonesia</span></li>
      <li><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li><span>Google Scholar</span><a href="{SCHOLAR}">scholar.google.com/citations?user=Ba2uOMsAAAAJ</a></li>
      <li><span>ORCID</span><a href="{ORCID}">0000-0002-2191-7411</a></li>
      <li><span>LinkedIn</span><a href="{LINKEDIN}">linkedin.com/in/marcelinus-adhiwibawa</a></li>
      <li><span>GitHub</span><a href="{GITHUB}">github.com/Alfasisurya</a></li>
      <li><span>Scopus</span><a href="{SCOPUS}">56123256300</a></li>
    </ul></div></section>'''
    write(OUT / "contact.html", layout("Contact", f"Contact {FULL}", 0, "contact.html", contact))

    def archive_page(filename, heading, kicker, lede, items, section, extra_after=""):
        years = sorted({str(item.get("year") or item.get("period")) for item in items}, reverse=True)
        topics = sorted({topic for item in items for topic in (item.get("domains") or item.get("topics") or [])})
        filters = (
            '<div class="filters" data-archive>'
            f'<label>Search<input data-filter-search type="search" placeholder="Search titles and summaries"></label>'
            '<label>Year<select data-filter-year><option value="all">All years</option>'
            + "".join(f'<option value="{esc(year)}">{esc(year)}</option>' for year in years)
            + '</select></label><label>Topic<select data-filter-topic><option value="all">All topics</option>'
            + "".join(f'<option value="{esc(topic)}">{esc(topic)}</option>' for topic in topics)
            + '</select></label></div><p class="meta"><span data-filter-count>'
            + str(len(items))
            + "</span> shown</p>"
        )
        body = (
            f'<header class="page-head"><div class="wrap"><p class="kicker">{kicker}</p><h1>{heading}</h1><p class="lede">{lede}</p></div></header>'
            f'<section class="section"><div class="wrap">{filters}{entry_list(items, 0, section)}<p data-filter-empty hidden>No matching items.</p></div></section>'
            + extra_after
        )
        write(OUT / filename, layout(heading, lede, 0, filename, body))

    showcases_after_pubs = f'''
    <section class="section section-tint" id="live-showcases"><div class="wrap">
      <div class="section-head">
        <p class="kicker">Live demonstrations</p>
        <h2>From research to a working tool</h2>
      </div>
      {showcase_cards(showcases, 0)}
      <p class="more"><a href="patents.html">Continue to patents →</a></p>
    </div></section>'''

    archive_page(
        "publications.html",
        "Publications",
        "Archive",
        f"{len(publications)} journal articles and conference papers, from 2013 to 2025. Each entry links to the DOI where available and to Google Scholar.",
        publications,
        "publications",
        extra_after=showcases_after_pubs,
    )
    archive_page("projects.html", "Research & Projects", "Research", "Research lines and tools, from leaf-image models and field instruments to geospatial screening.", projects, "projects")
    archive_page("analysis.html", "Analytical work", "Library", "Exploratory analyses and working studies. These have not been peer reviewed.", analyses, "analysis")
    archive_page("blog.html", "Blog", "Writing", "Articles about projects I am working on or have finished, and other public work.", posts, "blog")

    expertise = f'''<header class="page-head"><div class="wrap">
      <p class="kicker">Expertise</p>
      <h1>Depth, methods, and direction</h1>
      <p class="lede">Two domains where my work is established, the methods that connect them, and the fields I am exploring next.</p>
    </div></header>
    <section class="section"><div class="wrap">
      <div class="section-head">
        <p class="kicker">Established</p>
        <h2>Backed by roles, publications, and patents</h2>
      </div>
      <div class="pillars pillars-2">
        <article class="pillar">
          <p class="pillar-num">01</p>
          <h3>Life science &amp; environmental analytics</h3>
          <ul>
            <li>Agricultural data science and digital agronomy</li>
            <li>Plant imaging and field monitoring</li>
            <li>Remote sensing, geospatial analytics, and drone photogrammetry</li>
            <li>Climate and environmental analytics for agricultural decisions</li>
          </ul>
          <p class="evidence">Mondelēz agricultural data systems · Ma Chung research · Agronomic Intelligence · remote-sensing papers</p>
        </article>
        <article class="pillar">
          <p class="pillar-num">02</p>
          <h3>Chemistry &amp; spectral intelligence</h3>
          <ul>
            <li>Chemometrics and multivariate calibration</li>
            <li>NIR spectroscopy and spectral data analysis</li>
            <li>Optical and multispectral sensor prototyping</li>
            <li>Predictive models for chemical and biological measurements</li>
          </ul>
          <p class="evidence">US Patent 12,444,511 · pigment and chemometrics papers · low-cost field instruments</p>
        </article>
      </div>
    </div></section>
    <section class="section"><div class="wrap">
      <div class="section-head">
        <p class="kicker">Transferable</p>
        <h2>Methods that work across fields</h2>
      </div>
      <div class="chip-row">
        <span class="chip">Forecasting and time-series modelling</span>
        <span class="chip">Statistical modelling and inference</span>
        <span class="chip">Regression and multivariate analysis</span>
        <span class="chip">PCA and PLSR</span>
        <span class="chip">Experimental design and validation</span>
        <span class="chip">Machine learning and predictive analytics</span>
        <span class="chip">Python and R</span>
        <span class="chip">Data processing and visualisation</span>
        <span class="chip">Geospatial data pipelines</span>
        <span class="chip">Sensor and data-system prototyping</span>
      </div>
    </div></section>
    <section class="section section-tint"><div class="wrap">
      <div class="section-head">
        <p class="kicker">Emerging</p>
        <h2>Fields I am exploring</h2>
        <p class="intro">Study directions, not yet established professional work.</p>
      </div>
      {exploration_cards(explorations)}
      <p class="more"><a href="explorations.html">Read the research questions →</a></p>
    </div></section>'''
    write(OUT / "expertise.html", layout("Expertise", "Established expertise, transferable methods, and emerging research interests.", 0, "expertise.html", expertise))

    showcases_page = f'''<header class="page-head"><div class="wrap">
      <p class="kicker">Showcases</p>
      <h1>Live demonstrations</h1>
      <p class="lede">Research turned into tools you can open and use in the browser.</p>
    </div></header>
    <section class="section"><div class="wrap">
      {showcase_cards(showcases, 0)}
      <p class="more"><a href="projects.html">The research behind it →</a></p>
    </div></section>'''
    write(
        OUT / "showcases.html",
        layout(
            "Live Showcases",
            "Live demonstrations and project showcases, starting with Agronomic Intelligence.",
            0,
            "showcases.html",
            showcases_page,
        ),
    )

    explorations_page = f'''<header class="page-head"><div class="wrap">
      <p class="kicker">Explorations</p>
      <h1>Where I am heading next</h1>
      <p class="lede">Questions I am studying in fields beyond my established work. Each is marked as an idea or as something I am actively learning; none is presented as completed professional experience.</p>
    </div></header>
    <section class="section"><div class="wrap">
      {exploration_cards(explorations, detailed=True)}
    </div></section>'''
    write(
        OUT / "explorations.html",
        layout(
            "Explorations",
            "Emerging research interests in finance, supply chain, psychometrics, and food analytics.",
            0,
            "explorations.html",
            explorations_page,
        ),
    )

    patent_rows = entry_list(patents, 0, "patents")
    patents_body = f'''<header class="page-head"><div class="wrap"><p class="kicker">Patents</p><h1>Intellectual contributions</h1>
      <p class="lede">Granted patents and published applications on cocoa-leaf nutrient prediction from spectrometry and image-based screening of drought-tolerant soybean. Legal status follows the public records linked from each entry.</p>
    </div></header><section class="section"><div class="wrap">{patent_rows}</div></section>'''
    write(OUT / "patents.html", layout("Patents", "Patents and patent applications.", 0, "patents.html", patents_body))

    for item in publications:
        facts = [
            ("Authors", esc(", ".join(item.get("authors") or []))),
            ("Venue", esc(item.get("venue", ""))),
        ]
        if item.get("citation"):
            facts.append(("Citation", esc(item["citation"])))
        if item.get("doi"):
            facts.append(("DOI", f'<a href="{esc(item.get("url") or "https://doi.org/" + item["doi"])}">{esc(item["doi"])}</a>'))
        facts.append(("Scholar", f'<a href="https://scholar.google.com/scholar?q={requests_quote(item["title"])}">Search this title on Google Scholar</a>'))
        body = detail(item, 2, f'{item.get("year")} · {item.get("type")}', facts)
        write(OUT / "publications" / item["slug"] / "index.html", layout(item["title"], item.get("summary", ""), 2, "publications.html", body))

    for item in projects:
        facts = [
            ("Period", esc(item.get("period", ""))),
            ("Status", esc(item.get("status", ""))),
            ("Role", esc(item.get("role", ""))),
            ("Organization", esc(item.get("organization", ""))),
        ]
        if item.get("stack"):
            facts.append(("Tools", esc(", ".join(item["stack"]))))
        if item.get("demo"):
            facts.append(("Live tool", f'<a href="{esc(item["demo"])}">{esc(item["demo"].split("://", 1)[-1].rstrip("/"))}</a>'))
        if item.get("repo"):
            facts.append(("Source code", f'<a href="{esc(item["repo"])}">{esc(item["repo"].split("://", 1)[-1])}</a>'))
        body = detail(item, 2, " · ".join(item.get("domains") or []), facts)
        write(OUT / "projects" / item["slug"] / "index.html", layout(item["title"], item.get("summary", ""), 2, "projects.html", body))

    for item in analyses:
        facts = [
            ("Date", esc(item.get("date", ""))),
            ("Question", esc(item.get("question", ""))),
            ("Status", "Exploratory, not peer reviewed"),
        ]
        body = detail(item, 2, f'Exploratory · {item.get("category", "")}', facts)
        write(OUT / "analysis" / item["slug"] / "index.html", layout(item["title"], item.get("summary", ""), 2, "analysis.html", body))

    for item in patents:
        url, label = patent_link(item)
        facts = [
            ("Number", esc(item.get("number", ""))),
            ("Inventors", esc(", ".join(item.get("inventors") or []))),
            ("Filed", esc(item.get("filed", ""))),
            ("Published", esc(item.get("published", ""))),
            ("Owner", esc(item.get("owner", ""))),
            ("Field", esc(item.get("field", ""))),
            ("Record", f'<a href="{esc(url)}">{label}</a>'),
        ]
        body = detail(item, 2, f'{item.get("jurisdiction")} · {item.get("status")}', facts)
        write(OUT / "patents" / item["slug"] / "index.html", layout(item["title"], item.get("summary", ""), 2, "patents.html", body))

    for item in posts:
        facts = [("Published", esc(nice_date(item.get("date", ""))))]
        if item.get("topics"):
            facts.append(("Topics", esc(", ".join(item["topics"]))))
        body = detail(item, 2, "Blog", facts)
        body = body.replace("</article>", '<div class="wrap-narrow"><p class="back-link"><a href="../../blog.html">← All blog posts</a></p></div></article>')
        write(OUT / "blog" / item["slug"] / "index.html", layout(item["title"], item.get("summary", ""), 2, "blog.html", body))

    print(
        f"pages written: {len(publications)} papers, {len(projects)} projects, "
        f"{len(patents)} patents, {len(showcases)} showcases, {len(explorations)} explorations"
    )


if __name__ == "__main__":
    build()
