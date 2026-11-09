#!/usr/bin/env python3
"""Asset Rama site QC. Run from the repo root:  python3 scripts/site_qc.py

Checks, in one pass:
  1. tag balance on every .html page
  2. every internal href/src resolves to a real file
  3. sitemap.xml lists every page, and every sitemap URL is a real file
  4. robots.txt still allows crawling and points at the sitemap
  5. every application/ld+json block parses
  6. inline <script> blocks pass `node --check` (skipped if node is absent)

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
        if subprocess.run(['which', 'node'], capture_output=True).returncode == 0:
            check_scripts(p)
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
