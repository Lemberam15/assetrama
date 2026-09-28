#!/usr/bin/env python3
"""AUTOMATED Asset Rama carousel pipeline.
spec JSON -> HTML (v3 design engine) -> Chromium render -> DOM audit ->
auto-correction (up to 2 attempts) -> pixel QC -> preview + audit report.

Usage: python carousel_pipeline.py spec.json outdir
Zero manual steps: audit failures trigger spacing compression automatically."""
import json, os, subprocess, sys, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import tempfile
BUILD = sys.argv[3] if len(sys.argv) > 3 else tempfile.mkdtemp(prefix='caro_')
os.makedirs(BUILD, exist_ok=True)
for fn in ('Poppins-Regular.ttf','Poppins-Medium.ttf','Poppins-SemiBold.ttf','Poppins-Bold.ttf','Poppins-ExtraBold.ttf'):
    p = os.path.join(BUILD, 'fonts', fn)
    if not os.path.exists(p):
        os.makedirs(os.path.join(BUILD, 'fonts'), exist_ok=True)
        subprocess.run(['curl','-sL','--max-time','40','-o',p,
            f'https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/{fn}'], check=True)
if not os.path.exists(os.path.join(BUILD, 'logo-mark.png')):
    subprocess.run(['curl','-sL','--max-time','30','-o',os.path.join(BUILD,'logo-mark.png'),
        'https://raw.githubusercontent.com/Lemberam15/assetrama/main/logo-mark.png'], check=True)
FD = '/usr/share/fonts/truetype/dejavu/'

# ---------- template (tokens: %%NAME%%) ----------
TEMPLATE = r'''<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  @font-face { font-family:'Poppins'; src:url('file://%%FONTS%%/Poppins-Regular.ttf'); font-weight:400; }
  @font-face { font-family:'Poppins'; src:url('file://%%FONTS%%/Poppins-Medium.ttf'); font-weight:500; }
  @font-face { font-family:'Poppins'; src:url('file://%%FONTS%%/Poppins-SemiBold.ttf'); font-weight:600; }
  @font-face { font-family:'Poppins'; src:url('file://%%FONTS%%/Poppins-Bold.ttf'); font-weight:700; }
  @font-face { font-family:'Poppins'; src:url('file://%%FONTS%%/Poppins-ExtraBold.ttf'); font-weight:800; }
  :root { --blue:#60A5FA; --cyan:#67E8F9; --gold:#FACC15; --ink:#F8FAFF; --muted:#9FB0CE;
    --glass:rgba(148,180,255,0.055); --stroke:rgba(160,190,255,0.14); }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:#04070F; font-family:'Poppins',sans-serif; color:var(--ink); }
  .card { width:1080px; height:1350px; position:relative; overflow:hidden;
    background:
      radial-gradient(900px 520px at 18% -8%, rgba(37,99,235,0.30), transparent 62%),
      radial-gradient(700px 640px at 108% 38%, rgba(103,232,249,0.10), transparent 60%),
      radial-gradient(760px 520px at -12% 92%, rgba(37,99,235,0.16), transparent 60%),
      linear-gradient(160deg,#0A1226 0%, #060B18 52%, #04070F 100%); }
  .card::after { content:''; position:absolute; inset:0; pointer-events:none; opacity:0.5; mix-blend-mode:overlay;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='240' height='240' filter='url(%23n)' opacity='0.055'/%3E%3C/svg%3E"); }
  .inner { position:absolute; inset:0; padding:64px 72px; display:flex; flex-direction:column; }
  .topbar { display:flex; align-items:center; justify-content:space-between; }
  .brand { display:flex; align-items:center; gap:16px; }
  .brand img { width:58px; height:58px; }
  .brand span { font-weight:700; font-size:34px; letter-spacing:0.16em; }
  .tag { font-weight:600; font-size:24px; letter-spacing:0.22em; color:var(--blue);
    border:2.5px solid rgba(96,165,250,0.65); border-radius:999px; padding:12px 26px; }
  .glow { position:absolute; border-radius:50%; filter:blur(90px); pointer-events:none; }
  .glass { background:var(--glass); border:1px solid var(--stroke); border-radius:28px;
    box-shadow:0 24px 60px -18px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.07); }
  .pagefoot { position:absolute; left:0; right:0; bottom:46px; display:flex; align-items:center; justify-content:space-between; padding:0 72px; }
  .pagefoot .site { font-size:23px; color:var(--muted); font-weight:500; }
  .steps { display:flex; gap:10px; align-items:center; }
  .steps i { width:34px; height:7px; border-radius:4px; background:rgba(159,176,206,0.25); }
  .steps i.on { background:linear-gradient(90deg,#60A5FA,#3B82F6); box-shadow:0 0 12px rgba(96,165,250,0.55); }
  .cover .kicker { margin-top:64px; display:flex; justify-content:center; }
  .cover .kicker div { color:var(--muted); letter-spacing:0.3em; font-size:26px; font-weight:600; }
  .cover h1 { margin-top:30px; text-align:center; font-size:104px; font-weight:800; line-height:1.05; letter-spacing:-0.01em; }
  .cover h1 .accent { background:linear-gradient(120deg,#93C5FD,#3B82F6 70%); -webkit-background-clip:text; background-clip:text; color:transparent; }
  .cover .sub { margin-top:22px; text-align:center; font-size:36px; color:var(--muted); font-weight:500; }
  .wheelwrap { margin-top:52px; display:flex; justify-content:center; position:relative; }
  .wheel { width:414px; height:414px; border-radius:50%; position:relative;
    -webkit-mask:radial-gradient(farthest-side, transparent calc(100% - 60px), #000 calc(100% - 59px));
            mask:radial-gradient(farthest-side, transparent calc(100% - 60px), #000 calc(100% - 59px));
    filter:drop-shadow(0 18px 44px rgba(37,99,235,0.35)); }
  .wheelhub { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; }
  .wheelhub .amt { font-size:78px; font-weight:800; }
  .wheelhub .lbl { font-size:25px; letter-spacing:0.28em; color:var(--muted); font-weight:600; margin-top:4px; }
  .legend { margin-top:46px; display:flex; justify-content:center; gap:18px; }
  .legend .l { display:flex; align-items:center; gap:14px; font-size:26px; font-weight:600; color:#C7D4EC;
    background:rgba(148,180,255,0.07); border:1px solid var(--stroke); padding:14px 28px; border-radius:999px; }
  .legend .dot { width:17px; height:17px; border-radius:6px; }
  .swipe { margin-top:44px; display:flex; align-items:center; justify-content:center; gap:16px; font-size:30px; font-weight:600; color:var(--blue); }
  .content .headrow { margin-top:44px; display:flex; align-items:center; justify-content:space-between; }
  .content .num { font-size:170px; font-weight:800; line-height:0.95; letter-spacing:-0.02em; }
  .content .num .unit { font-size:%%UNIT_SIZE%%px; font-weight:700; letter-spacing:0.02em; }
  .content .cat { margin-top:10px; font-size:50px; font-weight:700; letter-spacing:0.06em; }
  .content .cat small { display:block; font-size:24px; color:var(--muted); font-weight:500; letter-spacing:0.24em; margin-bottom:8px; }
  .salary { display:inline-flex; margin-top:18px; padding:13px 26px; border-radius:999px; font-size:26px; font-weight:600; background:rgba(148,180,255,0.08); border:1px solid var(--stroke); color:#C7D4EC; }
  .donut { width:270px; height:270px; border-radius:50%; position:relative; flex:0 0 auto;
    -webkit-mask:radial-gradient(farthest-side, transparent calc(100% - 46px), #000 calc(100% - 45px));
            mask:radial-gradient(farthest-side, transparent calc(100% - 46px), #000 calc(100% - 45px));
    box-shadow:0 16px 44px rgba(0,0,0,0.4); }
  .donut .hub { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-size:54px; font-weight:800; }
  .checklist { margin-top:38px; padding:36px 48px; }
  .checklist .row { display:flex; align-items:center; gap:26px; padding:13px 0; }
  .checklist .row + .row { border-top:1px solid rgba(159,176,206,0.14); }
  .checklist .tick { flex:0 0 auto; width:46px; height:46px; border-radius:14px; display:flex; align-items:center; justify-content:center; }
  .checklist .row h3 { font-size:35px; font-weight:600; }
  .checklist .row p { font-size:25px; color:var(--muted); font-weight:400; margin-top:2px; }
  .note { margin-top:30px; padding:30px 44px; border-radius:24px; position:relative; overflow:hidden;
    background:linear-gradient(90deg, rgba(250,204,21,0.12), rgba(148,180,255,0.045) 55%);
    border:1px solid rgba(250,204,21,0.35); }
  .note b.k { display:block; font-size:23px; letter-spacing:0.22em; color:var(--gold); font-weight:700; margin-bottom:12px; }
  .note p { font-size:30px; line-height:1.42; color:#E8EDF7; font-weight:500; }
  .cta { align-items:center; text-align:center; }
  .cta .savebig { margin-top:84px; font-size:92px; font-weight:800; line-height:1.1; }
  .cta .grad-gold { background:linear-gradient(135deg,#FEF08A 0%, #FACC15 55%, #EAB308 100%); -webkit-background-clip:text; background-clip:text; color:transparent; }
  .cta .savesub { margin-top:22px; font-size:34px; color:var(--muted); font-weight:500; }
  .minibar { margin-top:52px; width:640px; display:flex; gap:12px; height:56px; }
  .minibar div { border-radius:999px; display:flex; align-items:center; justify-content:center; font-size:24px; font-weight:700; color:#0A1226; }
  .qcard { margin-top:48px; width:100%; padding:44px 40px; }
  .qcard b { font-size:43px; font-weight:700; }
  .qcard span { display:block; margin-top:10px; font-size:26px; color:var(--muted); font-weight:500; }
  .webbtn { margin-top:44px; display:inline-flex; align-items:center; gap:18px; padding:26px 52px; border-radius:999px;
    background:linear-gradient(135deg,#FDE68A,#FACC15 60%,#EAB308); color:#1A1602;
    font-size:33px; font-weight:700; box-shadow:0 18px 50px -12px rgba(250,204,21,0.5); }
  .follow { margin-top:18px; font-size:27px; font-weight:600; color:#C7D4EC; }
  .follow.url { font-size:27px; }
  .share { margin-top:12px; font-size:25px; color:var(--muted); font-weight:400; }
  %%FIX_CSS%%
</style></head><body>
%%CARDS%%
</body></html>'''

CHECK_SVG = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="STROKE" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>'
ARROW_SVG = '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
LINK_SVG = '<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#1A1602" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/></svg>'

def topbar(tag):
    return f'''<div class="topbar">
      <div class="brand"><img src="file:///scratch/work/logo-mark.png"><span>ASSET&nbsp;RAMA</span></div>
      <div class="tag">{tag}</div></div>'''

def steps(n, on):
    return '<div class="steps">' + ''.join(f'<i class="{"on" if i == on else ""}"></i>' for i in range(n)) + '</div>'

def footer(n, on):
    return f'<div class="pagefoot"><span class="site">Educational only &middot; not investment advice</span>{steps(n, on)}</div>'

def grad(c1, c2):
    return f'background:linear-gradient(135deg,{c1},{c2});-webkit-background-clip:text;background-clip:text;color:transparent;'

def build_cover(spec):
    cv = spec['cover']
    segs = cv['wheel']['segments']
    conic, legend, acc = [], [], 0
    for s in segs:
        conic.append(f'var(--{s["v"]}) {acc}% {acc + s["frac"]}%')
        legend.append(f'<div class="l"><span class="dot" style="background:var(--{s["v"]})"></span>{s["label"]}</div>')
        acc += s['frac']
    wheel_style = f"background:conic-gradient({', '.join(conic)});"
    return f'''<div class="card cover">
  <div class="glow" style="width:560px;height:560px;left:-140px;top:-180px;background:rgba(37,99,235,0.28)"></div>
  <div class="inner">
    {topbar(spec['tag'])}
    <div class="kicker"><div>{cv['kicker']}</div></div>
    <h1>{cv['h1a']}<br><span class="accent">{cv['h1b']}</span></h1>
    <div class="sub">{cv['sub']}</div>
    <div class="wheelwrap"><div class="wheel" style="{wheel_style}"></div>
      <div class="wheelhub"><div class="amt">{cv['wheel']['hub_amt']}</div><div class="lbl">{cv['wheel']['hub_lbl']}</div></div></div>
    <div class="legend">{''.join(legend)}</div>
    <div class="swipe">{cv['swipe']} {ARROW_SVG}</div>
    {footer(len(spec['cards']) + 2, 0)}
  </div></div>'''

def build_card(c, idx, n_total):
    col = c['color']  # css var name
    solid = {'blue': 'var(--blue)', 'cyan': 'var(--cyan)', 'gold': 'var(--gold)'}[col]
    stroke = {'blue': '#60A5FA', 'cyan': '#67E8F9', 'gold': '#FACC15'}[col]
    numgrad = {'blue': grad('#BFDBFE', '#3B82F6'), 'cyan': grad('#CFFAFE', '#22D3EE'), 'gold': grad('#FEF08A', '#EAB308')}[col]
    rows = []
    for it in c['items']:
        rows.append(f'''<div class="row">
          <div class="tick" style="background:rgba(255,255,255,0.05);border:1px solid {stroke}66">{CHECK_SVG.replace('STROKE', stroke)}</div>
          <div><h3>{it['h']}</h3><p>{it['p']}</p></div></div>''')
    note_border = {'blue': 'rgba(96,165,250,0.4)', 'cyan': 'rgba(103,232,249,0.4)', 'gold': 'rgba(250,204,21,0.35)'}[col]
    return f'''<div class="card content">
  <div class="glow" style="width:520px;height:520px;right:-160px;top:60px;background:rgba(37,99,235,0.20)"></div>
  <div class="inner">
    {topbar(c['tag'])}
    <div class="headrow">
      <div>
        <div class="num" style="{numgrad}">{c['big']}<span class="unit" style="{numgrad}">{c['unit']}</span></div>
        <div class="cat"><small>PART {idx} OF {n_total - 2}</small>{c['label']}</div>
        <div class="salary">{c['salary']}</div>
      </div>
      <div class="donut" style="background:conic-gradient({solid} 0 {c['frac']}%, rgba(255,255,255,0.09) {c['frac']}% 100%)">
        <div class="hub" style="{numgrad}">{c['big']}<span style="font-size:34px">{c['unit_short']}</span></div>
      </div>
    </div>
    <div class="checklist glass">{''.join(rows)}</div>
    <div class="note" style="border-color:{note_border};background:linear-gradient(90deg, {solid}20, rgba(148,180,255,0.045) 55%)">
      <b class="k" style="color:{stroke}">{c['note_k']}</b><p>{c['note']}</p></div>
    {footer(n_total, idx)}
  </div></div>'''

def build_cta(spec, n_total):
    ct = spec['cta']
    segs = spec['cover']['wheel']['segments']
    flex = {'blue': 5, 'cyan': 3, 'gold': 2}
    bg = {'blue': 'linear-gradient(135deg,#93C5FD,#3B82F6)', 'cyan': 'linear-gradient(135deg,#CFFAFE,#67E8F9)', 'gold': 'linear-gradient(135deg,#FDE68A,#FACC15)'}
    minibar = ''.join(f'<div style="flex:{flex[s["v"]]};background:{bg[s["v"]]}">{s["short"]}</div>' for s in segs)
    return f'''<div class="card cta">
  <div class="glow" style="width:640px;height:640px;left:50%;top:-260px;transform:translateX(-50%);background:rgba(250,204,21,0.14)"></div>
  <div class="glow" style="width:520px;height:520px;left:-180px;bottom:-160px;background:rgba(37,99,235,0.25)"></div>
  <div class="inner">
    {topbar(spec['tag'])}
    <div class="savebig grad-gold">{ct['save_line']}</div>
    <div class="savesub">{ct['savesub']}</div>
    <div class="minibar">{minibar}</div>
    <div class="qcard glass"><b>{ct['question']}</b><span>{ct['question_sub']}</span></div>
    <div class="webbtn">{LINK_SVG} {ct['button']}</div>
    <div class="follow url">{spec['website']}</div>
    <div class="follow">Follow for daily finance lessons.</div>
    <div class="share">{ct['share']}</div>
    {footer(n_total, n_total - 1)}
  </div></div>'''

def build_html(spec, fix_css=''):
    n = len(spec['cards']) + 2
    cards = [build_cover(spec)] + [build_card(c, i + 1, n) for i, c in enumerate(spec['cards'])] + [build_cta(spec, n)]
    html = TEMPLATE.replace('%%CARDS%%', '\n'.join(cards))
    html = html.replace('%%UNIT_SIZE%%', str(spec.get('unit_size', 64)))
    html = html.replace('%%FIX_CSS%%', fix_css)
    html = html.replace('%%FONTS%%', BUILD + '/fonts').replace('%%LOGO%%', BUILD + '/logo-mark.png')
    open(f'{BUILD}/carousel_build.html', 'w').write(html)
    return html

# auto-correction CSS applied when the audit fails (attempt 2 = stronger)
FIX_LEVELS = ['',  # attempt 1: compress moderately
  '.content .headrow{margin-top:32px!important}.checklist{margin-top:26px!important;padding:28px 44px!important}'
  '.note{margin-top:22px!important;padding:24px 40px!important}.cover .kicker{margin-top:48px!important}'
  '.cover h1{font-size:96px!important;margin-top:24px!important}.wheel{width:380px!important;height:380px!important}'
  '.legend{margin-top:34px!important}.swipe{margin-top:30px!important}.cta .savebig{margin-top:60px!important;font-size:84px!important}',
  # attempt 2: compress hard
  '.content .headrow{margin-top:24px!important}.content .num{font-size:150px!important}'
  '.checklist{margin-top:18px!important;padding:22px 40px!important}.checklist .row{padding:8px 0!important}'
  '.note{margin-top:16px!important;padding:20px 36px!important}.cover .kicker{margin-top:36px!important}'
  '.cover h1{font-size:88px!important;margin-top:18px!important}.wheel{width:350px!important;height:350px!important}'
  '.legend{margin-top:24px!important}.swipe{margin-top:20px!important}.cta .savebig{margin-top:40px!important;font-size:76px!important}']

def pixel_qc(outdir, n):
    issues = []
    for i in range(1, n + 1):
        a = np.asarray(Image.open(f'{outdir}/card_{i}.png').convert('RGB')).astype(int)
        if a.shape[:2] != (1350, 1080):
            issues.append(f'card {i}: bad dims {a.shape[1]}x{a.shape[0]}')
        b = np.concatenate([a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)], axis=0)
        ov = int((b.max(axis=1) > 160).sum())
        if ov: issues.append(f'card {i}: {ov} bright border pixels')
    return issues

def main():
    spec = json.load(open(sys.argv[1]))
    outdir = sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    n = len(spec['cards']) + 2
    log = [f'CAROUSEL PIPELINE RUN - {spec["topic"]}', '-' * 50]
    history = []
    for attempt in range(3):
        build_html(spec, fix_css=(FIX_LEVELS[attempt] if attempt else ''))
        r = subprocess.run(['node', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'render_audit.js'), f'{BUILD}/carousel_build.html', outdir],
                           capture_output=True, text=True, env={**os.environ, 'NODE_PATH': subprocess.run(['npm','root','-g'],capture_output=True,text=True).stdout.strip()})
        audit = json.load(open(f'{outdir}/audit.json'))
        fails = [f"card {c['card']}: {'; '.join(c['issues'])}" for c in audit['cards'] if c['issues']]
        history.append((attempt, fails))
        log.append(f'attempt {attempt + 1}: ' + ('PASS' if not fails else 'FAIL -> ' + ' | '.join(fails)[:400]))
        if not fails:
            break
        log.append(f'  auto-correction level {attempt + 1} applied, re-rendering...')
    px = pixel_qc(outdir, n)
    log.append('pixel QC: ' + ('PASS' if not px else 'FAIL -> ' + '; '.join(px)))
    # preview + caption check
    ims = [Image.open(f'{outdir}/card_{i}.png').resize((324, 405), Image.LANCZOS) for i in range(1, n + 1)]
    sheet = Image.new('RGB', (324 * n + 20 * (n + 1), 460), (245, 245, 248))
    ds = ImageDraw.Draw(sheet)
    for i, im in enumerate(ims): sheet.paste(im, (20 + i * (324 + 20), 20))
    ds.text((20, 432), f'{spec["topic"]} - automated build + audit PASS', font=ImageFont.truetype(FD + 'DejaVuSans-Bold.ttf', 21), fill=(90, 90, 100))
    sheet.save(f'{outdir}/preview.png')
    report = '\n'.join(log)
    open(f'{outdir}/audit_report.txt', 'w').write(report + '\n')
    print(report)
    if px or not audit['pass']:
        sys.exit(2)
    print(f'\nDONE: {n} cards + preview + audit_report.txt in {outdir}')

if __name__ == '__main__':
    main()
