#!/usr/bin/env python3
"""Asset Rama site QC. Run from the repo root:  python3 scripts/site_qc.py

Checks, in one pass:
  1. tag balance on every .html page
  2. every internal href/src resolves to a real file
  3. sitemap.xml lists every page, and every sitemap URL is a real file
  4. robots.txt still allows crawling and points at the sitemap
  5. every application/ld+json block parses
  6. inline <script> blocks pass `node --check` (skipped if node is absent)
  7. no duplicate id="" in any page
  8. lessons.html and search.html: the visible "N lessons" / "N pages" count text,
     the number of cards and (on lessons.html) the ItemList all agree, every
     ListItem carries both url and name, and the ItemList order follows the DOM

Exit code 0 = all clear, 1 = at least one failure. No network access, no writes.
"""
import json
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://lemberam15.github.io/assetrama'
VOID = {'br', 'img', 'meta', 'link', 'input', 'hr', 'source', 'area', 'base',
        'col', 'embed', 'param', 'track', 'wbr'}
SKIP = {'404.html'}          # 404 is served at arbitrary paths, so it is not sitemapped
fails, notes = [], []


def pages():
    out = []
    for p in ROOT.rglob('*.html'):
        rel = p.relative_to(ROOT)
        if rel.name.startswith('google') or '.git' in rel.parts:
            continue
        out.append(p)
    return sorted(out)


class Balance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.err = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        elif any(t == tag for t, _ in self.stack):
            self.err.append('line %d: </%s> closes a still-open <%s>'
                            % (self.getpos()[0], tag, self.stack[-1][0]))
            while self.stack and self.stack.pop()[0] != tag:
                pass
        else:
            self.err.append('line %d: stray </%s>' % (self.getpos()[0], tag))


def check_tags(p):
    b = Balance()
    b.feed(p.read_text())
    for e in b.err:
        fails.append('%s: %s' % (p.relative_to(ROOT), e))
    for t, line in b.stack:
        fails.append('%s: <%s> opened at line %d never closed' % (p.relative_to(ROOT), t, line))


LINK = re.compile(r'(?:href|src)="([^"]+)"')


def check_links(p):
    for raw in LINK.findall(p.read_text()):
        u = raw.strip()
        if not u or u.startswith(('#', 'mailto:', 'tel:', 'data:', 'javascript:')):
            continue
        rootrel = False
        if u.startswith(SITE):
            u = u[len(SITE):].lstrip('/') or 'index.html'
            rootrel = True
        elif urlparse(u).scheme or u.startswith('//'):
            continue                      # external
        u = unquote(u.split('#')[0].split('?')[0])
        if not u:
            continue
        target = ((ROOT if rootrel else p.parent) / u).resolve()
        if not target.exists():
            fails.append('%s: dead link %s' % (p.relative_to(ROOT), raw))


ID = re.compile(r'\sid="([^"]+)"')


def check_dup_ids(p):
    seen = {}
    for m in ID.finditer(p.read_text()):
        seen[m.group(1)] = seen.get(m.group(1), 0) + 1
    for k, v in seen.items():
        if v > 1:
            fails.append('%s: id="%s" is used %d times' % (p.relative_to(ROOT), k, v))


CARD = re.compile(r'<a class="card [^"]*" data-cat="[a-z]+" href="([^"]+)">\s*'
                  r'<div class="art".*?<h2>(.*?)</h2>', re.S)
COUNT = re.compile(r'<p class="count" id="count">(\d+)\s+(\w+)</p>')
ITEMLIST = re.compile(r'<script type="application/ld\+json">(\{"@context": "https://schema.org", '
                      r'"@type": "ItemList".*?)</script>', re.S)


def check_index(page, with_itemlist=False):
    """The card list, the visible count text and (on lessons.html) the ItemList are
    three hand-maintained copies of one fact. Assert they agree before a commit."""
    p = ROOT / page
    if not p.exists():
        fails.append('%s missing' % page)
        return
    text = p.read_text()
    cards = CARD.findall(text)
    m = COUNT.search(text)
    if not m:
        fails.append('%s: no <p class="count" id="count"> line' % page)
        return
    stated = int(m.group(1))
    if stated != len(cards):
        fails.append('%s: count text says %d %s but %d cards render'
                     % (page, stated, m.group(2), len(cards)))
    if with_itemlist:
        block = ITEMLIST.search(text)
        if not block:
            fails.append('%s: no ItemList JSON-LD' % page)
            return
        data = json.loads(block.group(1))
        items = data.get('itemListElement', [])
        if data.get('numberOfItems') != len(items):
            fails.append('%s: ItemList numberOfItems %s but %d items'
                         % (page, data.get('numberOfItems'), len(items)))
        if len(items) != len(cards):
            fails.append('%s: ItemList has %d items but %d cards render'
                         % (page, len(items), len(cards)))
        for i, it in enumerate(items, 1):
            if not it.get('url') or not it.get('name'):
                fails.append('%s: ItemList position %d is missing url or name' % (page, i))
            if it.get('position') != i:
                fails.append('%s: ItemList position %d is numbered %s'
                             % (page, i, it.get('position')))
        want = [c[0].rsplit('/', 1)[-1] for c in cards]
        got = [(it.get('url') or '').rsplit('/', 1)[-1] for it in items]
        if want != got:
            bad = next(i for i, (a, b) in enumerate(zip(want, got)) if a != b) if len(want) == len(got) else 0
            fails.append('%s: ItemList order does not follow the cards (first difference at card %d: %s vs %s)'
                         % (page, bad + 1, want[bad] if want else '?', got[bad] if got else '?'))
    notes.append('%s: %d cards, count text agrees' % (page, len(cards)))


def check_sitemap(all_pages):
    sm = ROOT / 'sitemap.xml'
    if not sm.exists():
        fails.append('sitemap.xml missing')
        return
    text = sm.read_text()
    locs = re.findall(r'<loc>([^<]+)</loc>', text)
    listed = set()
    for loc in locs:
        rel = loc.replace(SITE, '').lstrip('/') or 'index.html'
        listed.add(rel)
        if not (ROOT / rel).exists():
            fails.append('sitemap.xml: %s does not exist' % rel)
    for p in all_pages:
        rel = str(p.relative_to(ROOT))
        if p.name in SKIP or p.name.startswith('google'):
            continue
        if rel not in listed:
            fails.append('sitemap.xml: %s is not listed' % rel)
    notes.append('sitemap: %d urls, %d pages on disk' % (len(locs), len(all_pages)))


def check_robots():
    rb = ROOT / 'robots.txt'
    if not rb.exists():
        fails.append('robots.txt missing')
        return
    t = rb.read_text()
    if 'Sitemap:' not in t or 'sitemap.xml' not in t:
        fails.append('robots.txt: no Sitemap line')
    if re.search(r'^Disallow:\s*/\s*$', t, re.M):
        fails.append('robots.txt: disallows the whole site')


LD = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
SCRIPT = re.compile(r'<script(?![^>]*\bsrc=)(?![^>]*ld\+json)[^>]*>(.*?)</script>', re.S)


def check_jsonld(p):
    for n, block in enumerate(LD.findall(p.read_text()), 1):
        try:
            json.loads(block)
        except Exception as e:
            fails.append('%s: JSON-LD block %d does not parse (%s)'
                         % (p.relative_to(ROOT), n, e))


def check_scripts(p):
    for n, code in enumerate(SCRIPT.findall(p.read_text()), 1):
        if not code.strip():
            continue
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as fh:
            fh.write(code)
            tmp = fh.name
        r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
        Path(tmp).unlink()
        if r.returncode:
            first = (r.stderr.strip().splitlines() or ['?'])[0]
            fails.append('%s: inline script %d fails node --check (%s)'
                         % (p.relative_to(ROOT), n, first))


def main():
    all_pages = pages()
    for p in all_pages:
        check_tags(p)
        check_links(p)
        check_jsonld(p)
        check_dup_ids(p)
        if subprocess.run(['which', 'node'], capture_output=True).returncode == 0:
            check_scripts(p)
    check_index('lessons.html', with_itemlist=True)
    check_index('search.html')
    check_sitemap(all_pages)
    check_robots()

    notes.insert(0, 'pages checked: %d' % len(all_pages))
    for n in notes:
        print('  ' + n)
    if fails:
        print('\nFAIL (%d)' % len(fails))
        for f in fails:
            print('  - ' + f)
        return 1
    print('\nPASS — tag balance, links, sitemap, robots, JSON-LD and inline scripts all clean.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
