"""Build the public site as plain HTML. No npm."""
import html
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "src" / "content"
OUT = ROOT

SCHOLAR = "https://scholar.google.com/citations?hl=en&user=Ba2uOMsAAAAJ"
LINKEDIN = "https://www.linkedin.com/in/marcelinus-adhiwibawa/"
ORCID = "https://orcid.org/0000-0002-2191-7411"
SCOPUS = "https://www.scopus.com/authid/detail.uri?authorId=56123256300"
EMAIL = "marcelinus.setya@gmail.com"
NAME = "Marcelinus Alfasisurya Setya Adhiwibawa"
FULL = f"{NAME}, M.Stat."

NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("projects.html", "Research"),
    ("analysis.html", "Analytical Work"),
    ("publications.html", "Publications"),
    ("patents.html", "Patents"),
    ("notes.html", "Notes"),
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
  <link rel="stylesheet" href="{href(depth, "css/site.css")}?v=4">
</head>
<body>
  <a class="skip" href="#content">Skip to content</a>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="{href(depth, "index.html")}">
        <span class="brand-name">{esc(FULL)}</span>
        <span class="brand-role">Applied Scientist</span>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false">Menu</button>
      <nav class="nav" aria-label="Primary">{"".join(links)}<button class="theme-btn" type="button">Theme</button></nav>
    </div>
  </header>
  <main id="content">{body}</main>
  <footer class="site-footer">
    <div class="wrap">
      <p class="name">{esc(FULL)}</p>
      <p>Applied Scientist · AI, Geospatial &amp; Intelligent Systems</p>
      <p>
        <a href="{SCHOLAR}">Google Scholar</a> ·
        <a href="{ORCID}">ORCID 0000-0002-2191-7411</a> ·
        <a href="{LINKEDIN}">LinkedIn</a> ·
        <a href="{SCOPUS}">Scopus 56123256300</a> ·
        <a href="mailto:{EMAIL}">{EMAIL}</a>
      </p>
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


def entry_list(items, depth, section):
    rows = []
    for item in items:
        page = href(depth, f"{section}/{item['slug']}/index.html")
        year = item.get("year") or item.get("period") or ""
        kicker = item.get("type") or item.get("category") or item.get("status") or item.get("jurisdiction") or "Note"
        summary = item.get("summary") or item.get("venue") or ""
        extra = ""
        if section == "publications":
            bits = "".join(f'<a href="{esc(url)}">{esc(label)}</a>' for url, label in paper_links(item))
            extra = f'<p class="out-links">{bits}</p>'
        if section == "patents":
            url = item.get("url") or "https://patents.google.com/?q=" + requests_quote(item.get("number", item["title"]))
            label = "Google Patents" if item.get("url") and "/patent/" in item["url"] else "Search Google Patents"
            extra = f'<p class="out-links"><a href="{esc(url)}">{label}</a></p>'
        rows.append(
            f'<li data-item data-year="{esc(year)}" data-topics="{"|".join(esc(t) for t in item.get("domains") or item.get("topics") or [])}" '
            f'data-text="{esc((item["title"] + " " + summary).lower())}">'
            f'<div class="block-link"><span class="meta">{esc(year)}<br>{esc(kicker)}</span>'
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


def build():
    publications = sorted(load("publications"), key=lambda item: (-item.get("year", 0), item["title"]))
    projects = load("projects")
    analyses = load("analysis")
    patents = load("patents")
    notes = load("articles")

    if (ROOT / "public" / "images").exists():
        shutil.copytree(ROOT / "public" / "images", ROOT / "images", dirs_exist_ok=True)
    if (ROOT / "public" / "favicon.svg").exists():
        shutil.copyfile(ROOT / "public" / "favicon.svg", ROOT / "favicon.svg")

    photo = "images/profile/foto_marcel.jpg"
    featured_projects = [item for item in projects if item.get("featured")]
    featured_papers = [item for item in publications if item.get("featured")]
    featured_analysis = [item for item in analyses if item.get("featured")]
    featured_patent = next((item for item in patents if item.get("featured")), patents[0])

    home = f'''
    <section class="hero"><div class="wrap hero-layout">
      <img class="portrait" src="{photo}" width="640" height="640" alt="Portrait of {esc(NAME)}">
      <div>
        <p class="kicker">Applied Scientist</p>
        <h1>{esc(NAME)}<span class="cred">, M.Stat.</span></h1>
        <p class="position">AI, Geospatial &amp; Intelligent Systems</p>
        <p class="lede">I work where field science, data, and instruments meet. My research spans agricultural data science, geospatial analysis, spectroscopy, and applied machine learning, from leaf-image models and low-cost sensors to satellite analysis and a granted US patent.</p>
        <ul class="link-row">
          <li><a href="{SCHOLAR}">Google Scholar</a></li>
          <li><a href="{ORCID}">ORCID</a></li>
          <li><a href="{LINKEDIN}">LinkedIn</a></li>
          <li><a href="{SCOPUS}">Scopus</a></li>
          <li><a href="mailto:{EMAIL}">Email</a></li>
        </ul>
      </div>
    </div></section>
    <section class="section"><div class="wrap">
      <p class="kicker">Publication record</p>
      <h2>Citations and impact</h2>
      <p class="intro">My work has been cited 239 times on Google Scholar, with an h-index of 7 and an i10-index of 7. Since 2021 it has received 182 citations.</p>
      <table class="record">
        <thead><tr><th>Metric</th><th>All</th><th>Since 2021</th></tr></thead>
        <tbody>
          <tr><th>Citations</th><td>239</td><td>182</td></tr>
          <tr><th>h-index</th><td>7</td><td>6</td></tr>
          <tr><th>i10-index</th><td>7</td><td>3</td></tr>
        </tbody>
        <caption>Source: <a href="{SCHOLAR}">Google Scholar</a>, as of 22 November 2026.</caption>
      </table>
    </div></section>
    <section class="section"><div class="wrap">
      <p class="kicker">Expertise</p>
      <h2>Areas of work</h2>
      <div class="expertise">
        <div><h3>Agricultural data science</h3><p>Designing field data collection, cleaning, and reporting for agricultural research and plantations.</p></div>
        <div><h3>Geospatial analytics and remote sensing</h3><p>Spatial analysis, satellite imagery, and map-based screening tools such as Agronomic Intelligence.</p></div>
        <div><h3>Artificial intelligence</h3><p>CNN, ANN, and ANFIS models for plant images and spectral data.</p></div>
        <div><h3>Chemometrics and spectroscopy</h3><p>Pigment analysis, chemometric modelling, and NIR spectrometry for cocoa-leaf nutrients.</p></div>
        <div><h3>IoT and embedded systems</h3><p>Low-cost multispectral sensors, photometers, and chlorophyll meters built with Arduino, ESP32, and Raspberry Pi.</p></div>
        <div><h3>Statistical modelling</h3><p>Multivariate statistics, spatial interpolation, and classification.</p></div>
      </div>
    </div></section>
    <section class="section"><div class="wrap">
      <p class="kicker">Selected work</p><h2>Research and projects</h2>
      {entry_list(featured_projects, 0, "projects")}
      <p><a href="projects.html">All research and projects</a></p>
    </div></section>
    <section class="section"><div class="wrap">
      <p class="kicker">Analytical work</p><h2>Exploratory analyses</h2>
      <p class="intro">Working analyses that have not been peer reviewed.</p>
      {entry_list(featured_analysis, 0, "analysis")}
      <p><a href="analysis.html">All analytical work</a></p>
    </div></section>
    <section class="section"><div class="wrap">
      <p class="kicker">Papers</p><h2>Selected publications</h2>
      {entry_list(featured_papers, 0, "publications")}
      <p><a href="publications.html">All publications</a></p>
    </div></section>
    <section class="section"><div class="wrap">
      <p class="kicker">Patent</p>
      <h2>{esc(featured_patent.get("number", ""))}</h2>
      <p class="intro">{esc(featured_patent["title"])}</p>
      <p>United States patent, granted 14 October 2025. Assigned to {esc(featured_patent.get("owner", ""))}.</p>
      <p><a href="patents/{featured_patent["slug"]}/index.html">Patent details</a> · <a href="{esc(featured_patent.get("url", SCHOLAR))}">Google Patents</a></p>
    </div></section>'''
    write(OUT / "index.html", layout(FULL, f"{FULL}, applied scientist working on AI, geospatial analysis, and intelligent systems for agriculture.", 0, "index.html", home))

    about = f'''<header class="page-head"><div class="wrap">
      <div class="about-head">
        <img class="portrait" src="{photo}" width="640" height="640" alt="Portrait of {esc(NAME)}">
        <div>
          <p class="kicker">About</p>
          <h1>{esc(FULL)}</h1>
          <p class="position">Applied Scientist · AI, Geospatial &amp; Intelligent Systems</p>
        </div>
      </div>
      <p class="lede">{esc(NAME)} is an applied scientist in Malang, Indonesia. He holds an M.Stat. from Brawijaya University and a bachelor’s degree in plant pest and disease from the same university. Since 2021 he has worked as an Agricultural Data System Scientist at Mondelēz International. From 2012 to 2021 he was a research scientist at the Ma Chung Research Center for Photosynthetic Pigments.</p>
    </div></header>
    <section class="section"><div class="wrap">
      <h2>Profile</h2>
      <p>His work connects agricultural experiments with the data systems behind them: study design, data cleaning, spatial analysis, spectra, images, and the instruments that collect them. He applies machine learning to concrete agricultural problems, using CNN, ANN, and ANFIS models on leaf images, satellite pixels, and spectra.</p>
      <p>He has published more than 25 peer-reviewed papers and conference proceedings, cited 239 times on Google Scholar (h-index 7). He is a co-inventor of <a href="patents/us-12444511/index.html">US Patent 12,444,511</a> on predicting cocoa-leaf nutrients from spectrometry data.</p>
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
      <p class="kicker">Contact</p><h1>{esc(FULL)}</h1>
      <p class="lede">For research collaboration or professional enquiries, email is the best way to reach me.</p>
    </div></header>
    <section class="section"><div class="wrap"><ul class="facts">
      <li><span>Location</span><span>Malang, Indonesia</span></li>
      <li><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li><span>Google Scholar</span><a href="{SCHOLAR}">scholar.google.com/citations?user=Ba2uOMsAAAAJ</a></li>
      <li><span>ORCID</span><a href="{ORCID}">0000-0002-2191-7411</a></li>
      <li><span>LinkedIn</span><a href="{LINKEDIN}">linkedin.com/in/marcelinus-adhiwibawa</a></li>
      <li><span>Scopus</span><a href="{SCOPUS}">56123256300</a></li>
    </ul></div></section>'''
    write(OUT / "contact.html", layout("Contact", f"Contact {FULL}", 0, "contact.html", contact))

    def archive_page(filename, heading, kicker, lede, items, section):
        years = sorted({str(item.get("year") or item.get("period")) for item in items}, reverse=True)
        topics = sorted({topic for item in items for topic in (item.get("domains") or item.get("topics") or [])})
        filters = (
            '<div class="filters" data-archive>'
            f'<label>Search<input data-filter-search type="search" placeholder="Title, author, method"></label>'
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
        )
        write(OUT / filename, layout(heading, lede, 0, filename, body))

    archive_page(
        "publications.html",
        "Publications",
        "Archive",
        f"{len(publications)} journal articles and conference papers, from 2013 to 2025. Each entry links to the DOI where available and to Google Scholar.",
        publications,
        "publications",
    )
    archive_page("projects.html", "Projects", "Research", "Research lines and tools, from leaf-image models and field instruments to geospatial screening.", projects, "projects")
    archive_page("analysis.html", "Analytical work", "Library", "Exploratory analyses and working studies. These have not been peer reviewed.", analyses, "analysis")
    archive_page("notes.html", "Technical notes", "Notes", "Short write-ups on methods and the rules behind the tools.", notes, "articles")

    patent_rows = entry_list(patents, 0, "patents")
    patents_body = f'''<header class="page-head"><div class="wrap"><p class="kicker">Innovation</p><h1>Patents</h1>
      <p class="lede">Granted patents and published applications, covering cocoa-leaf nutrient prediction from spectrometry and image-based screening of drought-tolerant soybean.</p>
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
        url = item.get("url") or "https://patents.google.com/?q=" + requests_quote(item.get("number", ""))
        label = "Google Patents" if item.get("url") and "/patent/" in item["url"] else "Search Google Patents"
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

    for item in notes:
        facts = [("Date", esc(item.get("date", "")))]
        body = detail(item, 2, "Note", facts)
        write(OUT / "articles" / item["slug"] / "index.html", layout(item["title"], item.get("summary", ""), 2, "notes.html", body))

    print(f"pages written: {len(publications)} papers, {len(projects)} projects, {len(patents)} patents")


if __name__ == "__main__":
    build()
