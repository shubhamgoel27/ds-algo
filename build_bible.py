#!/usr/bin/env python3
"""Build concept-bible.html — a tabbed DSA reference from the concept-notes/*.md files.

Layout: sidebar-nav-docs · Mode: annotated-schematic (Tufte) · Voice: manifesto ·
Device: annotation-callout-layer. Self-contained single HTML file.
"""
import os, re, html, json

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.join(HERE, "concept-notes")
OUT = os.path.join(HERE, "concept-bible.html")

# (slug, display title, short tab label, group)
CONCEPTS = [
    ("arrays-hashing", "Arrays & Hashing", "Arrays & Hashing", "Linear scans"),
    ("two-pointers", "Two Pointers", "Two Pointers", "Linear scans"),
    ("sliding-window", "Sliding Window", "Sliding Window", "Linear scans"),
    ("stack", "Stack", "Stack", "Linear scans"),
    ("binary-search", "Binary Search", "Binary Search", "Search & sort"),
    ("linked-list", "Linked List", "Linked List", "Pointers"),
    ("trees", "Trees (BFS + DFS)", "Trees", "Recursion & trees"),
    ("tries", "Tries (Prefix Trees)", "Tries", "Recursion & trees"),
    ("heap", "Heap / Priority Queue", "Heap / PQ", "Ordered structures"),
    ("backtracking", "Backtracking", "Backtracking", "Recursion & trees"),
    ("graphs", "Graphs", "Graphs", "Graphs"),
    ("advanced-graphs", "Advanced Graphs / Union-Find", "Adv. Graphs / UF", "Graphs"),
    ("dp-1d", "Dynamic Programming — 1D", "DP · 1D", "Dynamic programming"),
    ("dp-2d", "Dynamic Programming — 2D", "DP · 2D", "Dynamic programming"),
    ("greedy", "Greedy", "Greedy", "Optimization"),
    ("intervals", "Intervals", "Intervals", "Optimization"),
    ("bit-math", "Bit Manipulation & Math", "Bit / Math", "Math"),
    ("design", "Design", "Design", "Ordered structures"),
]

# section header → css kind (the two "hook" sections pop)
SECTION_KIND = {
    "the engine in one sentence": "engine",
    "the one question that unlocks it": "unlock",
}

PY_KW = {"def","return","if","elif","else","for","while","in","not","and","or","is",
         "None","True","False","class","import","from","as","lambda","with","yield",
         "break","continue","pass","global","nonlocal","try","except","finally","raise",
         "assert","del","await","async"}
PY_BUILTIN = {"len","range","max","min","sum","sorted","set","dict","list","tuple","int",
              "str","float","map","filter","enumerate","zip","abs","print","deque","heapq",
              "heappush","heappop","heappushpop","heapify","defaultdict","Counter","bisect",
              "float","ord","chr","reversed","any","all","next","iter"}


def highlight_py(code):
    """Tokenizer-based Python highlighter -> safe escaped HTML spans."""
    out = []
    i, n = 0, len(code)
    while i < n:
        c = code[i]
        if c == "#":  # comment to EOL
            j = code.find("\n", i)
            j = n if j == -1 else j
            out.append(f'<span class="cm">{html.escape(code[i:j])}</span>')
            i = j
        elif c in "\"'":  # string
            q = c
            j = i + 1
            while j < n and code[j] != q:
                if code[j] == "\\":
                    j += 1
                j += 1
            j = min(j + 1, n)
            out.append(f'<span class="st">{html.escape(code[i:j])}</span>')
            i = j
        elif c.isdigit():
            j = i
            while j < n and (code[j].isdigit() or code[j] in ".xXa-fA-F_"):
                j += 1
            out.append(f'<span class="nu">{html.escape(code[i:j])}</span>')
            i = j
        elif c.isalpha() or c == "_":
            j = i
            while j < n and (code[j].isalnum() or code[j] == "_"):
                j += 1
            word = code[i:j]
            esc = html.escape(word)
            if word in PY_KW:
                out.append(f'<span class="kw">{esc}</span>')
            elif word in PY_BUILTIN:
                out.append(f'<span class="bi">{esc}</span>')
            else:
                out.append(esc)
            i = j
        else:
            out.append(html.escape(c))
            i += 1
    return "".join(out)


def inline(text):
    """Inline markdown -> HTML. Operates with escaping built in."""
    # protect inline code first
    spans = []
    def stash(m):
        spans.append(m.group(1))
        return f"\x00{len(spans)-1}\x00"
    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    def unstash(m):
        return f'<code>{html.escape(spans[int(m.group(1))])}</code>'
    text = re.sub(r"\x00(\d+)\x00", unstash, text)
    return text


TYPE_GLYPH = {  # tiny schematic SVG motif per visual type (annotated-schematic line-art)
    "flow": '<polyline points="8,30 52,30" /><polyline points="44,24 52,30 44,36"/><rect x="60" y="18" width="48" height="24" rx="2"/><polyline points="116,30 160,30"/><polyline points="152,24 160,30 152,36"/>',
    "tree": '<line x1="84" y1="14" x2="50" y2="44"/><line x1="84" y1="14" x2="118" y2="44"/><circle cx="84" cy="14" r="7"/><circle cx="50" cy="48" r="7"/><circle cx="118" cy="48" r="7"/>',
    "pointer-walk": '<line x1="20" y1="40" x2="160" y2="40"/><g class="cells"></g><polyline points="30,18 30,32"/><text x="26" y="14">L</text><polyline points="150,18 150,32"/><text x="146" y="14">R</text>',
    "grid-animation": '<rect x="40" y="14" width="14" height="14"/><rect x="56" y="14" width="14" height="14" class="hot"/><rect x="72" y="14" width="14" height="14"/><rect x="40" y="30" width="14" height="14" class="hot"/><rect x="56" y="30" width="14" height="14"/><rect x="72" y="30" width="14" height="14"/>',
    "state-machine": '<circle cx="36" cy="30" r="12"/><circle cx="100" cy="30" r="12"/><circle cx="160" cy="30" r="12"/><line x1="48" y1="30" x2="88" y2="30"/><polyline points="80,24 88,30 80,36"/><line x1="112" y1="30" x2="148" y2="30"/><polyline points="140,24 148,30 140,36"/>',
    "before-after": '<rect x="14" y="14" width="56" height="32" rx="2"/><text x="30" y="34">before</text><polyline points="84,30 116,30"/><polyline points="108,24 116,30 108,36"/><rect x="126" y="14" width="56" height="32" rx="2" class="hot"/><text x="142" y="34">after</text>',
    "bar-steps": '<rect x="20" y="34" width="10" height="12"/><rect x="36" y="26" width="10" height="20"/><rect x="52" y="18" width="10" height="28" class="hot"/><rect x="68" y="28" width="10" height="18"/><rect x="84" y="22" width="10" height="24"/>',
    "table-heatmap": '<rect x="40" y="12" width="16" height="16"/><rect x="58" y="12" width="16" height="16" class="hot"/><rect x="76" y="12" width="16" height="16"/><rect x="40" y="30" width="16" height="16" class="hot"/><rect x="58" y="30" width="16" height="16"/><rect x="76" y="30" width="16" height="16" class="hot"/>',
}
TYPE_GLYPH["default"] = TYPE_GLYPH["flow"]


def render_visual(spec_text):
    fields = {}
    for line in spec_text.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fields[k.strip().lower()] = v.strip()
    vtype = fields.get("type", "default").split()[0] if fields.get("type") else "default"
    glyph = TYPE_GLYPH.get(vtype, TYPE_GLYPH["default"])
    title = inline(fields.get("title", "Figure"))
    shows = inline(fields.get("shows", ""))
    elements = inline(fields.get("elements", ""))
    return f'''<figure class="viz">
  <div class="viz-head"><span class="pin">FIG</span><span class="viz-title">{title}</span><span class="viz-type">{html.escape(vtype)}</span></div>
  <svg class="viz-svg" viewBox="0 0 196 58" role="img" aria-label="{html.escape(fields.get('title','figure'))}">{glyph}</svg>
  <figcaption>{shows}</figcaption>
  <p class="viz-el"><span class="viz-el-label">draws</span> {elements}</p>
</figure>'''


def md_to_html(md):
    lines = md.split("\n")
    out = []
    i = 0
    cur_section_open = False

    def close_section():
        nonlocal cur_section_open
        if cur_section_open:
            out.append("</div>")
            cur_section_open = False

    # skip the leading H1 (handled by panel header)
    while i < len(lines) and not lines[i].startswith("# "):
        i += 1
    i += 1

    list_buf = []
    list_type = None

    def flush_list():
        nonlocal list_buf, list_type
        if list_buf:
            tag = "ol" if list_type == "ol" else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in list_buf) + f"</{tag}>")
            list_buf = []
            list_type = None

    while i < len(lines):
        line = lines[i]

        # fenced code
        m = re.match(r"^```(\w*)", line)
        if m:
            flush_list()
            lang = m.group(1)
            j = i + 1
            body = []
            while j < len(lines) and not lines[j].startswith("```"):
                body.append(lines[j])
                j += 1
            code = "\n".join(body)
            if lang == "visual":
                out.append(render_visual(code))
            elif lang == "python":
                out.append(f'<pre class="code"><code>{highlight_py(code)}</code></pre>')
            else:
                out.append(f'<pre class="trace"><code>{html.escape(code)}</code></pre>')
            i = j + 1
            continue

        # table
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|?\s*$", lines[i + 1]):
            flush_list()
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                rows.append([c.strip() for c in lines[j].strip().strip("|").split("|")])
                j += 1
            thead = "".join(f"<th>{inline(c)}</th>" for c in header)
            tbody = ""
            for r in rows:
                tds = "".join(f"<td>{inline(c)}</td>" for c in r)
                tbody += f"<tr>{tds}</tr>"
            out.append(f'<div class="tablewrap"><table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></div>')
            i = j
            continue

        # headings
        if line.startswith("## "):
            flush_list()
            close_section()
            title = line[3:].strip()
            kind = SECTION_KIND.get(title.lower(), "default")
            out.append(f'<div class="section section--{kind}">')
            cur_section_open = True
            out.append(f'<h2>{inline(title)}</h2>')
            i += 1
            continue
        if line.startswith("### "):
            flush_list()
            out.append(f'<h3>{inline(line[4:].strip())}</h3>')
            i += 1
            continue

        # blockquote
        if line.startswith(">"):
            flush_list()
            out.append(f'<blockquote>{inline(line.lstrip("> ").rstrip())}</blockquote>')
            i += 1
            continue

        # lists
        ulm = re.match(r"^[-*]\s+(.*)", line)
        olm = re.match(r"^\d+\.\s+(.*)", line)
        if ulm:
            if list_type == "ol":
                flush_list()
            list_type = "ul"
            list_buf.append(ulm.group(1))
            i += 1
            continue
        if olm:
            if list_type == "ul":
                flush_list()
            list_type = "ol"
            list_buf.append(olm.group(1))
            i += 1
            continue

        # blank
        if not line.strip():
            flush_list()
            i += 1
            continue

        # paragraph (gather until blank / block)
        para = [line]
        j = i + 1
        while j < len(lines) and lines[j].strip() and not re.match(r"^(```|\||#|>|[-*]\s|\d+\.\s)", lines[j]):
            para.append(lines[j])
            j += 1
        flush_list()
        out.append(f"<p>{inline(' '.join(para))}</p>")
        i = j

    flush_list()
    close_section()
    return "\n".join(out)


def main():
    panels = []
    nav_groups = {}
    for slug, title, label, group in CONCEPTS:
        with open(os.path.join(NOTES, slug + ".md")) as f:
            md = f.read()
        body = md_to_html(md)
        idx = len(panels) + 1
        panels.append(f'''<section class="panel" id="panel-{slug}" data-slug="{slug}" hidden>
  <div class="panel-rule"><span class="panel-num">{idx:02d}</span><h1>{html.escape(title)}</h1></div>
  {body}
</section>''')
        nav_groups.setdefault(group, []).append((slug, label, idx))

    nav = []
    for group, items in nav_groups.items():
        nav.append(f'<div class="nav-group"><span class="nav-group-label">{html.escape(group)}</span>')
        for slug, label, idx in items:
            nav.append(f'<button class="nav-item" data-target="{slug}"><span class="nav-num">{idx:02d}</span>{html.escape(label)}</button>')
        nav.append("</div>")
    nav_html = "\n".join(nav)

    html_doc = TEMPLATE.replace("{{NAV}}", nav_html).replace("{{PANELS}}", "\n".join(panels)).replace("{{COUNT}}", str(len(CONCEPTS)))
    with open(OUT, "w") as f:
        f.write(html_doc)
    print(f"wrote {OUT} — {len(CONCEPTS)} concepts, {len(html_doc)} bytes")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DSA Concept Bible</title>
<meta name="artifold:intent" content="Tabbed interview-prep reference of 18 algorithm patterns with rendered figures">
<meta name="artifold:tool" content="claude">
<meta name="artifold:prompt" content="Generate notes/explanations for all main LC concepts as a /craft report with a tab per concept and helper visuals">
<meta name="artifold:layout-archetype" content="sidebar-nav-docs">
<meta name="artifold:design-mode" content="annotated-schematic">
<meta name="artifold:voice-register" content="manifesto">
<meta name="artifold:signature-device" content="annotation-callout-layer">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{
  --paper:#faf8f2; --paper-2:#f3f0e6; --ink:#1f1d1a; --ink-soft:#54514a; --ink-faint:#8b8678;
  --red:#d6261f; --red-soft:#f4ddd9; --blue:#2f5d7c; --rule:#ddd6c6; --rule-2:#e7e1d2;
  --grid:#ece6d6; --good:#3f7a4b; --warn:#b06a16; --hard:#b3261e;
  --font-head:"Newsreader",Georgia,serif; --font-body:"Inter",system-ui,sans-serif;
  --font-mono:"JetBrains Mono",ui-monospace,Menlo,monospace;
  --sp:8px; --maxw:74ch; --shadow:0 1px 0 var(--rule), 0 8px 24px -16px rgba(40,34,20,.45);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--font-body);
  font-size:16.5px;line-height:1.62;-webkit-font-smoothing:antialiased;
  background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);
  background-size:26px 26px;background-position:-1px -1px;}
.app{display:grid;grid-template-columns:268px minmax(0,1fr);min-height:100vh}

/* ---- sidebar ---- */
.side{position:sticky;top:0;height:100vh;overflow-y:auto;border-right:1px solid var(--rule);
  background:rgba(247,244,235,.86);backdrop-filter:blur(3px);padding:22px 16px 40px}
.brand{padding:6px 8px 14px;border-bottom:1px dashed var(--rule);margin-bottom:14px}
.brand .kicker{font-family:var(--font-mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--red);font-weight:700}
.brand h2{font-family:var(--font-head);font-weight:600;font-size:24px;line-height:1.04;letter-spacing:-.02em;margin:6px 0 2px}
.brand p{margin:0;font-size:11.5px;color:var(--ink-faint);font-family:var(--font-mono)}
.nav-group{margin:14px 0 4px}
.nav-group-label{display:block;font-family:var(--font-mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-faint);padding:0 8px 4px}
.nav-item{display:flex;gap:9px;align-items:baseline;width:100%;text-align:left;border:0;background:none;
  font-family:var(--font-body);font-size:13.5px;color:var(--ink-soft);padding:6px 8px;border-radius:5px;cursor:pointer;line-height:1.2}
.nav-item:hover{background:var(--paper-2);color:var(--ink)}
.nav-item .nav-num{font-family:var(--font-mono);font-size:10.5px;color:var(--ink-faint);min-width:17px}
.nav-item.active{background:var(--ink);color:var(--paper)}
.nav-item.active .nav-num{color:var(--red-soft)}
.nav-item:focus-visible{outline:2px solid var(--red);outline-offset:2px}

/* ---- main ---- */
.main{padding:0}
.topbar{position:sticky;top:0;z-index:5;display:flex;align-items:center;gap:14px;
  padding:11px 40px;border-bottom:1px solid var(--rule);background:rgba(250,248,242,.9);backdrop-filter:blur(4px)}
.topbar .crumb{font-family:var(--font-mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-faint)}
.topbar .crumb b{color:var(--red)}
.progress{flex:1;display:flex;gap:3px;align-items:center;max-width:340px}
.progress i{flex:1;height:3px;background:var(--rule);border-radius:2px}
.progress i.on{background:var(--ink)}
.progress i.here{background:var(--red)}
.wrap{max-width:920px;margin:0 auto;padding:30px 40px 120px}
.panel{animation:fade .35s ease}
@keyframes fade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}

.panel-rule{display:flex;align-items:flex-end;gap:14px;border-bottom:2px solid var(--ink);padding-bottom:10px;margin-bottom:8px}
.panel-num{font-family:var(--font-mono);font-size:13px;color:var(--red);font-weight:700;letter-spacing:.06em;padding-bottom:3px}
.panel h1{font-family:var(--font-head);font-weight:600;font-size:clamp(30px,4vw,42px);line-height:1.02;letter-spacing:-.025em;margin:0}

.section{margin:30px 0;padding-left:18px;border-left:1px solid var(--rule-2);position:relative}
.section h2{font-family:var(--font-head);font-weight:600;font-size:22px;letter-spacing:-.01em;margin:0 0 8px;color:var(--ink)}
.section h2::before{content:"";position:absolute;left:-4.5px;top:6px;width:8px;height:8px;background:var(--paper);border:2px solid var(--ink);border-radius:50%}
h3{font-family:var(--font-body);font-weight:700;font-size:14px;letter-spacing:.01em;margin:20px 0 6px}
p{margin:10px 0;max-width:var(--maxw)}
strong{font-weight:700;color:var(--ink)}
em{font-style:italic}
a{color:var(--blue);text-decoration:underline;text-underline-offset:2px}
ul,ol{margin:10px 0;padding-left:22px;max-width:var(--maxw)}
li{margin:5px 0}
li::marker{color:var(--red)}
code{font-family:var(--font-mono);font-size:.86em;background:var(--paper-2);border:1px solid var(--rule-2);
  border-radius:3px;padding:.05em .35em;color:#7a2018}
blockquote{margin:14px 0;padding:8px 16px;border-left:3px solid var(--red);background:var(--red-soft);
  border-radius:0 4px 4px 0;color:#5a201c;max-width:var(--maxw);font-size:15px}
blockquote p{margin:0}

/* hook sections pop */
.section--engine,.section--unlock{border-left:0;padding:0;margin:24px 0}
.section--engine{margin-top:14px}
.section--engine h2,.section--unlock h2{font-size:11px;font-family:var(--font-mono);letter-spacing:.16em;
  text-transform:uppercase;color:var(--ink-faint);margin-bottom:6px}
.section--engine h2::before,.section--unlock h2::before{display:none}
.section--engine p{font-family:var(--font-head);font-size:23px;line-height:1.34;font-weight:400;color:var(--ink);max-width:40ch}
.section--engine strong{font-weight:600}
.section--unlock{background:var(--ink);color:var(--paper);border-radius:8px;padding:18px 22px;box-shadow:var(--shadow)}
.section--unlock h2{color:var(--red-soft)}
.section--unlock p{color:var(--paper);max-width:54ch}
.section--unlock strong{color:#fff;background:linear-gradient(transparent 62%, rgba(214,38,31,.55) 62%)}
.section--unlock code{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.18);color:#ffd9d3}

/* code + traces */
pre{margin:14px 0;overflow-x:auto;border-radius:6px;font-family:var(--font-mono);font-size:13px;line-height:1.55}
pre.code{background:#1c1b18;color:#e9e4d6;padding:14px 16px;border:1px solid #000;box-shadow:var(--shadow)}
pre.code code{background:none;border:0;padding:0;color:inherit;font-size:13px}
pre.code .kw{color:#ff9a8c;font-weight:500}
pre.code .bi{color:#9fc7e6}
pre.code .st{color:#cfe3a8}
pre.code .nu{color:#e6c07b}
pre.code .cm{color:#867f6c;font-style:italic}
pre.trace{background:var(--paper-2);color:var(--ink-soft);padding:13px 16px;border:1px solid var(--rule);
  background-image:linear-gradient(var(--grid) 1px,transparent 1px);background-size:100% 21px;background-position:0 13px}
pre.trace code{background:none;border:0;padding:0;color:inherit}

/* tables */
.tablewrap{margin:16px 0;overflow-x:auto;border:1px solid var(--rule);border-radius:6px;box-shadow:var(--shadow)}
table{border-collapse:collapse;width:100%;font-size:14px;background:var(--paper)}
thead th{background:var(--ink);color:var(--paper);text-align:left;padding:8px 12px;font-weight:600;
  font-family:var(--font-body);font-size:12px;letter-spacing:.02em;position:sticky}
tbody td{padding:8px 12px;border-top:1px solid var(--rule-2);vertical-align:top}
tbody tr:nth-child(even){background:var(--paper-2)}
tbody td:first-child{font-family:var(--font-mono);font-size:12px;color:var(--red);white-space:nowrap;font-weight:500}
table code{font-size:.8em}

/* figures (annotation-callout-layer device) */
.viz{margin:18px 0;border:1px solid var(--rule);border-radius:7px;background:var(--paper);
  padding:14px 16px 12px;position:relative;box-shadow:var(--shadow)}
.viz-head{display:flex;align-items:center;gap:9px;margin-bottom:8px}
.pin{font-family:var(--font-mono);font-size:9px;font-weight:700;letter-spacing:.1em;color:var(--paper);
  background:var(--red);padding:2px 6px;border-radius:10px}
.viz-title{font-family:var(--font-body);font-weight:700;font-size:13.5px}
.viz-type{margin-left:auto;font-family:var(--font-mono);font-size:10px;color:var(--ink-faint);text-transform:uppercase;letter-spacing:.08em}
.viz-svg{display:block;width:100%;max-width:360px;height:auto;margin:4px auto 8px}
.viz-svg line,.viz-svg polyline,.viz-svg rect,.viz-svg circle{fill:none;stroke:var(--ink);stroke-width:1.6}
.viz-svg rect{fill:var(--paper-2)}
.viz-svg circle{fill:var(--paper)}
.viz-svg .hot{fill:var(--red-soft);stroke:var(--red)}
.viz-svg text{font-family:var(--font-mono);font-size:9px;fill:var(--red);stroke:none}
.viz figcaption{font-size:13.5px;color:var(--ink);font-weight:500;margin:2px 0 6px}
.viz-el{font-size:12px;color:var(--ink-soft);margin:0;border-top:1px dashed var(--rule);padding-top:7px;max-width:none}
.viz-el-label{font-family:var(--font-mono);font-size:9.5px;text-transform:uppercase;letter-spacing:.1em;color:var(--red);margin-right:6px}

@media (max-width:880px){
  .app{grid-template-columns:1fr}
  .side{position:fixed;z-index:20;transform:translateX(-100%);transition:transform .25s;width:268px;box-shadow:var(--shadow)}
  .side.open{transform:none}
  .menu-btn{display:inline-flex}
  .wrap{padding:24px 20px 100px}
  .topbar{padding:10px 20px}
  body{background-size:22px 22px}
}
.menu-btn{display:none;border:1px solid var(--rule);background:var(--paper);border-radius:5px;
  font-family:var(--font-mono);font-size:12px;padding:5px 9px;cursor:pointer}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;scroll-behavior:auto}}
</style>
</head>
<body>
<div class="app">
  <aside class="side" id="side">
    <div class="brand">
      <span class="kicker">Active Recall × Patterns</span>
      <h2>DSA Concept Bible</h2>
      <p>{{COUNT}} patterns · the unlock for each</p>
    </div>
    <nav id="nav">
      {{NAV}}
    </nav>
  </aside>
  <main class="main">
    <div class="topbar">
      <button class="menu-btn" id="menuBtn" aria-label="Toggle navigation">≡ menu</button>
      <span class="crumb">Pattern <b id="crumbNum">01</b> / {{COUNT}} · <span id="crumbName">Arrays &amp; Hashing</span></span>
      <div class="progress" id="progress" aria-hidden="true"></div>
    </div>
    <div class="wrap" id="wrap">
      {{PANELS}}
    </div>
  </main>
</div>
<script>
(function(){
  const panels=[...document.querySelectorAll('.panel')];
  const items=[...document.querySelectorAll('.nav-item')];
  const prog=document.getElementById('progress');
  const crumbNum=document.getElementById('crumbNum'), crumbName=document.getElementById('crumbName');
  const side=document.getElementById('side');
  panels.forEach((_,k)=>{const b=document.createElement('i');prog.appendChild(b);});
  const bars=[...prog.children];
  function show(slug,push){
    let idx=0;
    panels.forEach((p,k)=>{const on=p.dataset.slug===slug;p.hidden=!on;if(on)idx=k;});
    items.forEach(it=>it.classList.toggle('active',it.dataset.target===slug));
    bars.forEach((b,k)=>{b.className=k<idx?'on':(k===idx?'here':'');});
    const it=items.find(x=>x.dataset.target===slug);
    crumbNum.textContent=String(idx+1).padStart(2,'0');
    crumbName.textContent=it?it.textContent.replace(/^\d+/,'').trim():'';
    side.classList.remove('open');
    document.getElementById('wrap').scrollTo?.(0,0);
    window.scrollTo(0,0);
    if(push)history.replaceState(null,'',' #'+slug);
  }
  items.forEach(it=>it.addEventListener('click',()=>show(it.dataset.target,true)));
  document.getElementById('menuBtn').addEventListener('click',()=>side.classList.toggle('open'));
  document.addEventListener('keydown',e=>{
    if(e.key!=='ArrowLeft'&&e.key!=='ArrowRight')return;
    const cur=panels.findIndex(p=>!p.hidden);
    let n=cur+(e.key==='ArrowRight'?1:-1);
    if(n>=0&&n<panels.length)show(panels[n].dataset.slug,true);
  });
  const start=(location.hash||'').replace('#','');
  show(panels.some(p=>p.dataset.slug===start)?start:panels[0].dataset.slug,false);
})();
</script>
</body>
</html>"""


if __name__ == "__main__":
    main()
