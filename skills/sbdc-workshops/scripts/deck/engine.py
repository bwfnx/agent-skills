# SBDC Workshops deck engine: Maryland SBDC design system, fixed 16:9 stage, click-by-click reveal,
# worksheet QR checkpoints, presenter window (P), print-to-PDF.
# A class file calls setup(form_url), then `from engine import *`, adds slides, calls render().
import base64, html, io, pathlib
import qrcode, qrcode.image.svg

HERE = pathlib.Path(__file__).parent
SIGNUP_URL = "https://mdsbdc.ecenterdirect.com/signup"
SIGNUP_LABEL = "mdsbdc.ecenterdirect.com/signup"
LOGO = base64.b64encode((HERE / "logo-reverse-900.png").read_bytes()).decode()
VIEWPORT_BASE = (HERE / "viewport-base.css").read_text()
FORM_URL = FORM_LABEL = QR_FORM = ""


def qr(url):
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=2)
    buf = io.BytesIO(); img.save(buf)
    svg = buf.getvalue().decode()
    return svg[svg.index("<svg"):]


QR_SIGNUP = qr(SIGNUP_URL)
SLIDES = []


def setup(form_url, form_label="Link is in the Zoom chat"):
    """Call first, then `from engine import *` so QR_FORM / FORM_LABEL are bound in the class file."""
    global FORM_URL, FORM_LABEL, QR_FORM
    FORM_URL, FORM_LABEL, QR_FORM = form_url, form_label, qr(form_url)


def slide(kind, body, notes, eyebrow="", title="", label=""):
    head = ""
    if eyebrow:
        head += f'<p class="eyebrow r">{eyebrow}</p>'
    if title:
        head += f'<h2 class="r">{title}</h2><div class="rule r"></div>'
    SLIDES.append((kind, head + body, notes, html.unescape(label or title or eyebrow)))


def section(num, title, notes):
    slide("dark section", f'''
      <div class="sec-num r">{num}</div>
      <h1 class="r">{title}</h1>
      <div class="band r"></div>''', notes, title="")
    SLIDES[-1] = (*SLIDES[-1][:3], title)


def checkpoint(qs, title, blurb, notes):
    slide("dark checkpoint", f'''
      <div class="cp-grid">
        <div>
          <p class="eyebrow light r">Worksheet checkpoint &middot; {qs}</p>
          <h1 class="r">{title}</h1>
          <p class="lead r">{blurb}</p>
          <p class="url r">{FORM_LABEL}</p>
        </div>
        <div class="qr-card r">{QR_FORM}<span>Lost the tab? Scan again.</span></div>
      </div>''', notes)
    SLIDES[-1] = (*SLIDES[-1][:3], f"Checkpoint {qs}")


def bullets(items, cls=""):
    return f'<ul class="list {cls}">' + "".join(f'<li class="r">{i}</li>' for i in items) + "</ul>"



# ============================ RENDER ============================

CSS = r"""
/* === THEME: Maryland SBDC design system tokens (colors.css / typography.css / spacing.css) === */
:root{
  --sbdc-red:#d11142; --sbdc-blue:#002d62; --sbdc-gray:#adafb2;
  --red-50:#fceef2; --red-100:#f8d3dd; --red-200:#f0a3b7; --red-600:#b00d38; --red-700:#8c0a2c;
  --blue-50:#e8eef5; --blue-100:#c6d4e6; --blue-200:#8ea9cc; --blue-300:#4f7aad; --blue-400:#1f5290;
  --blue-600:#002752; --blue-700:#001e40; --blue-800:#00162e; --blue-900:#000d1c;
  --n-50:#f7f8f9; --n-100:#eef0f2; --n-200:#e2e4e7; --n-300:#cdd0d4; --n-500:#8b8e92; --n-600:#6a6d71; --n-800:#313438;
  --success:#1f7a4d; --gold:#c9821a;
  --font-display:'Archivo','Helvetica Neue',Arial,sans-serif;
  --font-body:Arial,'Helvetica Neue',Helvetica,sans-serif;
  --ease:cubic-bezier(0.22,0.61,0.36,1);
  --stage-bg:#000d1c; --slide-bg:#ffffff;
}
*{margin:0;padding:0;box-sizing:border-box}
"""

CSS += VIEWPORT_BASE

CSS += r"""
/* === SLIDE FRAME: 120px side margins, blue footer band with page number === */
.slide{font-family:var(--font-body);color:var(--n-800)}
.frame{position:absolute;inset:88px 120px 150px 120px}
.foot{position:absolute;left:0;right:0;bottom:0;height:72px;background:var(--sbdc-blue);display:flex;align-items:center;justify-content:space-between;padding:0 120px;color:#fff;font:700 20px/1 var(--font-display);letter-spacing:.12em;text-transform:uppercase}
.foot .pg{color:var(--blue-200);font-variant-numeric:tabular-nums}
.foot .band-mini{background:var(--sbdc-red);padding:8px 14px}
.dark .foot{display:none}

/* === TYPE: heavy Archivo display, red eyebrow + 4px accent rule (SectionHeader motif) === */
.eyebrow{font:700 24px/1.2 var(--font-display);letter-spacing:.12em;text-transform:uppercase;color:var(--sbdc-red);margin-bottom:18px}
.eyebrow.light{color:var(--red-200)}
h2{font:900 76px/1.05 var(--font-display);letter-spacing:-.02em;color:var(--sbdc-blue)}
.rule{width:96px;height:6px;background:var(--sbdc-red);margin:26px 0 48px}
h3{font:800 40px/1.15 var(--font-display);color:var(--sbdc-blue);letter-spacing:-.01em}
.list{list-style:none;display:flex;flex-direction:column;gap:22px;font-size:34px;line-height:1.35}
.list li{padding-left:40px;position:relative}
.list li::before{content:"";position:absolute;left:0;top:.5em;width:16px;height:16px;background:var(--sbdc-red)}
.list.checks li::before{width:22px;height:12px;background:none;border:solid var(--success);border-width:0 0 5px 5px;transform:rotate(-45deg);top:.3em}
.takeaway{position:absolute;bottom:0;left:0;font:800 38px/1.2 var(--font-display);color:var(--sbdc-blue);border-left:8px solid var(--sbdc-red);padding:6px 0 6px 28px}
.statement{font:800 52px/1.2 var(--font-display);color:var(--sbdc-blue);letter-spacing:-.01em}
.statement em{font-style:normal;color:var(--sbdc-red)}
.statement.center{position:absolute;bottom:0;left:0;right:0;text-align:center;font-size:46px}
.fine{font-size:24px;line-height:1.45;color:var(--n-600);margin-top:22px}
.card{background:#fff;border:1px solid var(--n-200);border-top:6px solid var(--sbdc-blue);border-radius:10px;padding:40px 44px;box-shadow:0 4px 12px rgba(0,45,98,.10),0 2px 4px rgba(0,45,98,.06)}
.card.accent{border-top-color:var(--sbdc-red);background:var(--red-50)}
.card-k{font:700 22px/1.2 var(--font-display);letter-spacing:.12em;text-transform:uppercase;color:var(--n-600);margin-bottom:22px}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:start}
.cols2.wide-left{grid-template-columns:1.25fr 1fr}
.cols2.wide-right{grid-template-columns:1fr 1.1fr;align-items:center}

/* === DARK SLIDES: title, sections, checkpoints, close — navy ground, red MARYLAND band === */
.dark{--slide-bg:var(--blue-800);background:radial-gradient(ellipse at 85% 10%,rgba(31,82,144,.55),transparent 55%),linear-gradient(160deg,var(--sbdc-blue),var(--blue-800) 70%);color:#fff}
.dark h1{font:900 124px/1.0 var(--font-display);letter-spacing:-.025em;color:#fff}
.band{width:360px;height:22px;background:var(--sbdc-red);margin:40px 0}
.logo{position:absolute;top:80px;left:120px;width:300px}
.title .frame{inset:0}
.title-grid{position:absolute;left:120px;right:120px;bottom:120px;display:grid;grid-template-columns:1fr 340px;gap:80px;align-items:end}
.byline{font:600 34px/1.45 var(--font-display);color:var(--blue-100)}
.byline.small{font:500 24px/1.4 var(--font-body);color:var(--blue-200);margin-top:22px}
.qr-card{background:#fff;border-radius:10px;padding:22px;display:flex;flex-direction:column;align-items:center;gap:12px;box-shadow:0 12px 28px rgba(0,0,0,.35)}
.qr-card svg{width:100%;height:auto;display:block}
.qr-card svg path{fill:var(--blue-800)}
.qr-card span{font:800 20px/1.2 var(--font-display);color:var(--sbdc-blue);text-align:center;letter-spacing:.02em}
.close .title-grid{bottom:210px}
.sba{position:absolute;left:120px;right:120px;bottom:56px;font-size:17px;line-height:1.45;color:var(--blue-200)}
.section .frame{display:flex;flex-direction:column;justify-content:center;inset:0 120px}
.sec-num{font:700 30px/1 var(--font-display);letter-spacing:.2em;text-transform:uppercase;color:var(--red-200);margin-bottom:30px}
.section h1{max-width:1500px}
.checkpoint .frame{inset:0 120px;display:flex;align-items:center}
.cp-grid{display:grid;grid-template-columns:1fr 420px;gap:110px;align-items:center;width:100%}
.checkpoint h1{font-size:104px}
.lead{font:500 36px/1.45 var(--font-body);color:var(--blue-100);margin-top:36px;max-width:1100px}
.url{font:800 34px/1 var(--font-display);color:#fff;margin-top:44px;letter-spacing:.01em}
.url.ink{color:var(--sbdc-blue)}

/* === SCAN SLIDE === */
.scan-grid{display:grid;grid-template-columns:1fr 520px;gap:110px;align-items:start}
.steps{list-style:none;counter-reset:s;display:flex;flex-direction:column;gap:30px}
.steps li{counter-increment:s;font-size:36px;line-height:1.35;padding-left:86px;position:relative}
.steps li::before{content:counter(s);position:absolute;left:0;top:-4px;width:58px;height:58px;background:var(--sbdc-red);color:#fff;font:900 32px/58px var(--font-display);text-align:center}
.steps b{color:var(--sbdc-blue)}
.qr-card.big{border:2px solid var(--n-200);box-shadow:0 12px 28px rgba(0,45,98,.14);margin-top:-80px}

/* === AGENDA === */
.agenda{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:28px 80px}
.agenda li{font:700 40px/1.2 var(--font-display);color:var(--sbdc-blue);display:flex;gap:28px;align-items:baseline;border-bottom:1px solid var(--n-200);padding-bottom:24px}
.agenda span{font-size:28px;color:var(--sbdc-red);letter-spacing:.08em}

/* === TIERS (where to look) === */
.tiers{display:flex;flex-direction:column;align-items:center;gap:14px}
.tier{display:grid;grid-template-columns:380px 1fr 150px;gap:30px;align-items:center;padding:30px 44px;color:#fff;font-size:28px;line-height:1.3}
.tier b{font:900 44px/1 var(--font-display)}
.tier em{font:800 30px/1 var(--font-display);font-style:normal;text-align:right;color:var(--red-100)}
.t1{width:72%;background:var(--sbdc-blue)} .t2{width:86%;background:var(--blue-400)} .t3{width:100%;background:var(--blue-300)}
.t1 em{font-size:26px}
.also{margin-top:40px;font-size:28px;line-height:1.45;background:var(--n-50);border-left:6px solid var(--sbdc-red);padding:22px 30px}
.also b{color:var(--sbdc-blue)}
.buy{display:grid;grid-template-columns:230px 1fr;gap:22px 24px;font-size:28px;line-height:1.4}
.buy dt{font:800 30px/1.3 var(--font-display);color:var(--sbdc-blue)}
.big-line{font:900 64px/1.05 var(--font-display);color:var(--sbdc-red);margin-bottom:22px}
.card.accent p:not(.card-k):not(.big-line){font-size:30px;line-height:1.45}

/* === COMPARE TABLE === */
.compare{width:100%;border-collapse:collapse;font-size:32px}
.compare th{font:800 34px/1 var(--font-display);color:#fff;background:var(--sbdc-blue);text-align:left;padding:24px 30px}
.compare th:first-child{background:none}
.compare td{padding:22px 30px;border-bottom:1px solid var(--n-200)}
.compare td:first-child{font:800 30px/1 var(--font-display);color:var(--sbdc-blue);width:300px}

/* === STRATEGY STAIRS === */
.stairs{display:grid;grid-template-columns:1fr 1fr 1fr;gap:32px;align-items:end;height:520px}
.step{padding:36px 36px 40px;color:#fff;display:flex;flex-direction:column;gap:16px}
.step h3{color:#fff;font-size:44px}
.step p{font-size:26px;line-height:1.4}
.step-n{font:700 20px/1 var(--font-display)!important;letter-spacing:.14em;text-transform:uppercase;opacity:.8}
.s1{height:62%;background:var(--sbdc-red)} .s2{height:100%;background:var(--sbdc-blue)} .s3{height:78%;background:var(--blue-300);border:4px dashed var(--blue-100)}
.chips{display:flex;flex-wrap:wrap;gap:16px;margin-top:48px}
.chips span{font:900 34px/1 var(--font-display);color:var(--sbdc-blue);border:3px solid var(--sbdc-blue);padding:16px 24px;border-radius:3px}

/* === 36-MONTH TIMELINE === */
.timeline{position:relative;height:330px;margin-top:10px}
.tl-bar{display:grid;grid-template-columns:1fr 1fr 1fr;height:150px;margin-right:150px}
.tl-seg{padding:26px 30px;color:#fff;display:flex;flex-direction:column;justify-content:space-between}
.tl-seg b{font:800 34px/1.1 var(--font-display)} .tl-seg span{font-size:24px;opacity:.85}
.tl-seg.a{background:var(--blue-300)} .tl-seg.b{background:var(--blue-400)} .tl-seg.c{background:var(--sbdc-blue)}
.tl-rfp{position:absolute;top:150px;height:40px;left:calc((100% - 150px) * 0.8);border-left:6px solid var(--sbdc-red)}
.tl-rfp span{position:absolute;top:40px;left:-6px;background:var(--sbdc-red);color:#fff;font:900 30px/1.1 var(--font-display);padding:16px 22px;white-space:nowrap}
.tl-rfp small{font:500 20px/1 var(--font-body)}
.tl-award{position:absolute;right:0;top:0;width:150px;height:150px;background:var(--success);color:#fff;font:900 32px/150px var(--font-display);text-align:center}

/* === STAT + CURVE === */
.stat-n{font:900 300px/0.9 var(--font-display);color:var(--sbdc-red);letter-spacing:-.04em}
.stat-l{font:800 44px/1.2 var(--font-display);color:var(--sbdc-blue);margin-top:24px;max-width:680px}
.curve{display:flex;flex-direction:column;gap:16px;margin-bottom:44px}
.curve div{display:grid;grid-template-columns:220px 1fr 200px;align-items:center;gap:20px;font-size:26px}
.curve b{font:800 26px/1 var(--font-display);color:var(--sbdc-blue)}
.curve span{height:34px;background:var(--sbdc-blue);display:block}
.curve em{font-style:normal;color:var(--n-600)}

/* === CAPABILITY STATEMENT MOCK === */
.cs{border:2px solid var(--sbdc-blue);border-radius:6px;overflow:hidden}
.cs-h{background:var(--sbdc-blue);color:#fff;font:800 28px/1 var(--font-display);padding:22px 26px}
.cs-r{display:grid;grid-template-columns:1fr 1fr}
.cs-r span{padding:30px 26px;font:700 26px/1.2 var(--font-display);color:var(--sbdc-blue);border-top:1px solid var(--n-200)}
.cs-r span:first-child{border-right:1px solid var(--n-200)}

/* === SIX PHASES === */
.phases{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-top:40px}
.ph{height:300px;padding:34px 28px;color:#fff;font:800 32px/1.15 var(--font-display);display:flex;flex-direction:column;gap:22px;clip-path:polygon(0 0,88% 0,100% 50%,88% 100%,0 100%,12% 50%)}
.ph:first-child{clip-path:polygon(0 0,88% 0,100% 50%,88% 100%,0 100%)}
.ph{padding-left:48px;padding-right:44px}
.ph span{font-size:64px;font-weight:900;opacity:.9}
.ph.pre{background:var(--sbdc-blue)} .ph.post{background:var(--sbdc-red)}
.ph-legend{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:34px}
.ph-legend span{font:800 30px/1 var(--font-display);padding-top:22px;border-top:8px solid}
.ph-legend .pre{color:var(--sbdc-blue);border-color:var(--sbdc-blue)} .ph-legend .post{color:var(--sbdc-red);border-color:var(--sbdc-red)}
.phase-tag{position:absolute;right:0;top:-40px;font:900 260px/1 var(--font-display);color:var(--blue-50);z-index:-1}
.phase-tag.post{color:var(--red-50)}
.funnel{display:flex;flex-direction:column;align-items:center;gap:10px;margin-top:10px}
.funnel div{color:#fff;font:800 30px/1 var(--font-display);padding:34px 0;text-align:center}
.funnel div:nth-child(1){width:100%;background:var(--blue-300)} .funnel div:nth-child(2){width:78%;background:var(--sbdc-red)} .funnel div:nth-child(3){width:52%;background:var(--sbdc-blue)}
.roles{display:flex;flex-direction:column;gap:12px}
.roles div{display:grid;grid-template-columns:340px 1fr;align-items:center;padding:18px 24px;background:var(--blue-50);border-left:6px solid var(--sbdc-blue);font-size:25px}
.roles b{font:800 27px/1.2 var(--font-display);color:var(--sbdc-blue)}
.keyouts .ko{font:900 46px/1 var(--font-display);color:#fff;background:var(--sbdc-red);padding:30px 34px;margin-bottom:14px}

/* === COLOR TEAM FLOW === */
.colorflow{display:flex;align-items:stretch;gap:0;margin-top:40px}
.colorflow i{width:34px;flex:0 0 34px;background:linear-gradient(90deg,transparent 45%,var(--n-300) 45% 55%,transparent 55%) center/100% 6px no-repeat;display:block}
.cf{flex:1;min-height:250px;padding:28px 22px;font:900 34px/1.1 var(--font-display);display:flex;flex-direction:column;gap:14px;justify-content:center;text-align:center}
.cf small{font:500 21px/1.35 var(--font-body)}
.cf.write{background:var(--n-100);color:var(--sbdc-blue);flex:.7}
.cf.pink{background:var(--red-200);color:var(--red-700)} .cf.red{background:var(--sbdc-red);color:#fff} .cf.gold{background:var(--gold);color:#fff}
.cf.submit{background:var(--sbdc-blue);color:#fff;flex:.8}

.callout{background:var(--sbdc-red);color:#fff;padding:70px 60px}
.callout p{font:900 80px/1.02 var(--font-display);letter-spacing:-.02em}
.callout span{display:block;font:800 44px/1 var(--font-display);margin-top:24px;color:var(--red-100)}

/* === FOUR C's, GO/NO-GO, SPLIT, TILES === */
.four{display:grid;grid-template-columns:1fr 1fr;gap:28px}
.four div{border:2px solid var(--n-200);border-top:8px solid var(--sbdc-blue);padding:34px 40px;display:flex;flex-direction:column;gap:14px}
.four b{font:900 50px/1 var(--font-display);color:var(--sbdc-blue)}
.four b::first-letter{color:var(--sbdc-red)}
.four span{font-size:29px;line-height:1.4}
.gng{display:grid;grid-template-columns:1fr 1fr;gap:44px}
.gng>div{padding:40px 46px}
.gng h3{margin-bottom:28px;font-size:46px}
.gng .list{font-size:30px;gap:18px}
.no{background:var(--red-50);border-top:8px solid var(--sbdc-red)} .no h3{color:var(--red-700)}
.go{background:#e9f4ee;border-top:8px solid var(--success)} .go h3{color:var(--success)}
.go .list li::before{background:var(--success)}
.split{display:grid;grid-template-columns:1fr 120px 1fr;height:470px}
.half{padding:60px;color:#fff;display:flex;flex-direction:column;justify-content:flex-end;gap:14px}
.half p{font:700 24px/1 var(--font-display);letter-spacing:.14em;text-transform:uppercase;opacity:.8}
.half h3{color:#fff;font-size:104px;font-weight:900;letter-spacing:-.02em}
.half span{font-size:32px}
.cap{background:var(--sbdc-blue)} .prop{background:var(--sbdc-red)}
.divider{position:relative;background:linear-gradient(90deg,var(--sbdc-blue) 50%,var(--sbdc-red) 50%)}
.divider span{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:#fff;color:var(--sbdc-blue);font:900 34px/1 var(--font-display);padding:26px 18px;border:4px solid var(--sbdc-blue)}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.tiles div{border:1px solid var(--n-200);border-top:6px solid var(--sbdc-red);padding:34px 36px 38px;font-size:26px;line-height:1.4;color:var(--n-600);min-height:250px;box-shadow:0 1px 3px rgba(0,45,98,.08)}
.tiles span{font:900 60px/1 var(--font-display);color:var(--blue-100);display:block;margin-bottom:10px}
.tiles b{display:block;font:800 36px/1.15 var(--font-display);color:var(--sbdc-blue);margin-bottom:10px}
.next-h{font-size:52px;margin-bottom:34px}
.submit-card{background:var(--sbdc-blue);color:#fff;padding:44px 48px;position:relative;min-height:540px}
.submit-card h3{color:#fff;font-size:50px;max-width:560px}
.submit-card p:not(.eyebrow){font-size:28px;line-height:1.45;color:var(--blue-100);margin-top:22px;max-width:430px}
.mini-qr{position:absolute;right:40px;bottom:40px;width:200px;background:#fff;padding:12px;border-radius:6px}
.mini-qr svg{width:100%;height:auto;display:block} .mini-qr svg path{fill:var(--blue-800)}

/* === MOTION: quick fade + rise, 60ms stagger (design system: 120–320ms, no bounce) === */
.r{opacity:0;transform:translateY(18px);transition:opacity 320ms var(--ease),transform 320ms var(--ease)}
.slide.visible .r{opacity:1;transform:none}
.slide.visible .r:nth-child(2){transition-delay:60ms} .slide.visible .r:nth-child(3){transition-delay:120ms}
.slide.visible .r:nth-child(4){transition-delay:180ms} .slide.visible .r:nth-child(5){transition-delay:240ms}
.slide.visible .r:nth-child(6){transition-delay:300ms} .slide.visible .r:nth-child(7){transition-delay:360ms}
@media print{.r{opacity:1!important;transform:none!important}}

/* === PROGRESSIVE REVEAL: .f elements wait for the next click; .on shows them (JS assigns both) === */
.slide .f:not(.on){opacity:0!important;transform:translateY(14px)!important}
.slide.visible .f.on{transition-delay:0s!important}
@media print{.slide .f:not(.on),.slide .f.on{opacity:1!important;transform:none!important}}
@page{size:1920px 1080px;margin:0}
@media print{.progress,.hint{display:none!important}}

/* === PRESENTATION CHROME (outside the stage) === */
.progress{position:fixed;left:0;top:0;height:4px;background:var(--sbdc-red);z-index:1000;transition:width 200ms var(--ease)}
.hint{position:fixed;right:16px;bottom:12px;font:600 13px/1 var(--font-display);color:rgba(255,255,255,.35);z-index:1000;letter-spacing:.04em}
"""

JS = r"""
/* === SLIDE CONTROLLER: arrows/space/PageUp/PageDown/Home/End, click, swipe, wheel.
       F = fullscreen. P = presenter window with notes, timer, next slide (share only the deck window in Zoom). === */
class Deck{
  constructor(){
    this.slides=[...document.querySelectorAll('.slide')];
    this.stage=document.getElementById('deckStage');
    this.bar=document.getElementById('progress');
    this.i=Math.min(parseInt(location.hash.slice(1)||'1',10)-1||0,this.slides.length-1);
    this.t0=null; this.pw=null; this.k=0;
    // Progressive reveal: every leaf matching STEPS on a light slide becomes one click. Dark slides and the scan slide show at once.
    const STEPS='.list>li,.tier,.also,.step,.four>div,.tiles>div,.ph,.ph-legend,.roles>div,.funnel>div,.colorflow>.cf,.gng>div,.half,.tl-seg,.tl-rfp,.tl-award,.takeaway,.statement,.stat,.curve>div,.agenda>li,.compare tbody tr,.ko,.callout,.chips,.cols2>*,.capstmt,.submit-card';
    this.frags=this.slides.map(s=>{
      if(s.classList.contains('dark')||s.classList.contains('scan'))return [];
      const c=[...s.querySelector('.frame').querySelectorAll(STEPS)];
      const leaves=c.filter(el=>!c.some(o=>o!==el&&el.contains(o)));
      leaves.forEach(el=>el.classList.add('f'));
      return leaves;
    });
    const fit=()=>{const f=Math.min(innerWidth/1920,innerHeight/1080);
      this.stage.style.transform=`translate(${(innerWidth-1920*f)/2}px,${(innerHeight-1080*f)/2}px) scale(${f})`;};
    fit(); addEventListener('resize',fit);
    addEventListener('keydown',e=>this.key(e));
    let x0=null; addEventListener('touchstart',e=>x0=e.touches[0].clientX,{passive:true});
    addEventListener('touchend',e=>{if(x0===null)return;const dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>40)(dx<0?this.next():this.prev());x0=null;});
    let lock=0; addEventListener('wheel',e=>{const n=Date.now();if(n-lock<600||Math.abs(e.deltaY)<20)return;lock=n;e.deltaY>0?this.next():this.prev();},{passive:true});
    this.show();
  }
  key(e){
    const k=e.key;
    if(['ArrowRight','ArrowDown',' ','PageDown','Enter'].includes(k)){e.preventDefault();this.next();}
    else if(['ArrowLeft','ArrowUp','PageUp','Backspace'].includes(k)){e.preventDefault();this.prev();}
    else if(k==='Home')this.go(0); else if(k==='End')this.go(this.slides.length-1);
    else if(k==='f'||k==='F'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();}
    else if(k==='p'||k==='P')this.presenter();
  }
  next(){const fr=this.frags[this.i];if(this.k<fr.length){fr[this.k++].classList.add('on');this.renderPresenter();}else if(this.i<this.slides.length-1)this.go(this.i+1);}
  prev(){if(this.i>0)this.go(this.i-1,true);}  // going back lands on the fully built slide
  go(n,full=false){this.i=Math.max(0,Math.min(n,this.slides.length-1));const fr=this.frags[this.i];this.k=full?fr.length:0;fr.forEach((el,j)=>el.classList.toggle('on',j<this.k));this.show();}
  show(){
    this.slides.forEach((s,j)=>{s.classList.toggle('active',j===this.i);s.classList.toggle('visible',j===this.i);});
    this.bar.style.width=((this.i+1)/this.slides.length*100)+'%';
    history.replaceState(null,'','#'+(this.i+1));
    this.renderPresenter();
  }
  presenter(){
    if(this.pw&&!this.pw.closed){this.pw.focus();return;}
    this.pw=open('','sbdc-presenter','width=960,height=720');
    if(!this.pw)return;
    this.t0=this.t0||Date.now();
    const d=this.pw.document;
    d.title='Presenter notes';
    d.body.style.cssText='margin:0;font:22px/1.5 Arial,sans-serif;background:#00162e;color:#fff;padding:28px 34px';
    d.body.innerHTML='<div id="h" style="font:700 16px Archivo,Arial;letter-spacing:.1em;text-transform:uppercase;color:#8ea9cc;display:flex;justify-content:space-between"><span id="n"></span><span id="t"></span></div><h2 id="ti" style="font:800 34px/1.15 Arial;margin:14px 0 18px"></h2><div id="no" style="font-size:26px;line-height:1.55"></div><p id="nx" style="margin-top:28px;color:#8ea9cc;font-size:18px"></p><p style="color:#4f7aad;font-size:14px;margin-top:24px">Arrow keys work here too.</p>';
    d.addEventListener('keydown',e=>this.key(e));
    setInterval(()=>{if(this.pw.closed)return;const s=Math.floor((Date.now()-this.t0)/1000);this.pw.document.getElementById('t').textContent=Math.floor(s/60)+':'+String(s%60).padStart(2,'0')+' elapsed';},1000);
    this.renderPresenter();
  }
  renderPresenter(){
    if(!this.pw||this.pw.closed)return;
    const d=this.pw.document,s=this.slides[this.i],nx=this.slides[this.i+1];
    const fr=this.frags[this.i];d.getElementById('n').textContent='Slide '+(this.i+1)+' of '+this.slides.length+(fr.length?' · step '+this.k+' of '+fr.length:'');
    d.getElementById('ti').textContent=s.dataset.title;
    d.getElementById('no').textContent=s.querySelector('.notes').textContent;
    d.getElementById('nx').textContent=nx?'Next: '+nx.dataset.title:'Last slide';
  }
}
new Deck();
"""

def render(out, title, footer):
    """Write the single-file deck. footer = text in the blue band, e.g. "Session 2 &middot; Team Roles"."""
    parts = []
    n = len(SLIDES)
    for i, (kind, body, notes, label) in enumerate(SLIDES, 1):
        foot = f'<div class="foot"><span class="band-mini">Maryland SBDC</span><span>{footer}</span><span class="pg">{i:02d} / {n:02d}</span></div>'
        parts.append(
            f'<section class="slide {kind}" data-title="{html.escape(label)}" aria-label="Slide {i}: {html.escape(label)}">\n'
            f'  <div class="frame">{body}</div>{foot}\n'
            f'  <aside class="notes" hidden>{html.escape(notes)}</aside>\n'
            f'  <!-- NOTES: {html.escape(notes)} -->\n</section>')
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800;900&display=swap">
<style>{CSS}</style>
</head>
<body>
<div class="progress" id="progress"></div>
<div class="deck-viewport">
<main class="deck-stage" id="deckStage">
{chr(10).join(parts)}
</main>
</div>
<div class="hint">&larr; &rarr; move &middot; F fullscreen &middot; P notes</div>
<script>{JS}</script>
</body>
</html>"""
    pathlib.Path(out).write_text(doc, encoding="utf-8")
    print(f"{pathlib.Path(out).name}: {n} slides, {len(doc)//1024} KB, form -> {FORM_URL}")
