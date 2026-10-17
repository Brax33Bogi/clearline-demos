"""Render one demo page from its facts.

Layout and copy vary by trade and by look (looks.py). Facts never vary:
they are whatever extract.py found on the page already published.
"""
from __future__ import annotations

import html
import json
import re

from .looks import LOOKS, PALETTES
from .trades import TRADES, TRUST, detect_trade, faqs, service_areas

SITE = "https://sites.clearlineweb.net"

SCHEMA_TYPE = {
    "hvac": "HVACBusiness", "refrigeration": "HVACBusiness", "ducts": "HVACBusiness",
    "plumbing": "Plumber", "electrical": "Electrician", "roofing": "RoofingContractor",
    "construction": "GeneralContractor", "handyman": "GeneralContractor",
    "auto": "AutoRepair", "autoelectric": "AutoRepair", "oilchange": "AutoRepair", "autoglass": "AutoRepair",
    "hardware": "HardwareStore", "nursery": "GardenStore", "repairshop": "Store",
    "appliance": "HomeAndConstructionBusiness",
}


def esc(s) -> str:
    return html.escape(str(s), quote=True)


# The c mark from brand/demo-site-chrome.html. Artwork, never redrawn.
_MARK_PATH = ("M303 -14Q231 -14 172.5 16.0Q114 46 80.0 103.0Q46 160 46 241V255Q46 336 80.0 393.0Q114 450 172.5 480.0"
              "Q231 510 303 510Q374 510 425.0 485.0Q476 460 507.5 416.5Q539 373 549 318L427 292Q423 322 409.0 346.0"
              "Q395 370 369.5 384.0Q344 398 306 398Q268 398 237.5 381.5Q207 365 189.5 332.5Q172 300 172 253V243"
              "Q172 196 189.5 163.5Q207 131 237.5 114.5Q268 98 306 98Q363 98 392.5 127.5Q422 157 430 205L552 176"
              "Q539 123 507.5 79.5Q476 36 425.0 11.0Q374 -14 303 -14Z")


def _mark(size: int, mask_id: str, color: str = "currentColor") -> str:
    return (f'<svg width="{size}" height="{size}" viewBox="46 -510 506 524" aria-hidden="true" style="display:block;flex:none;color:{color}">'
            f'<mask id="{mask_id}" maskUnits="userSpaceOnUse" x="46" y="-510" width="506" height="524">'
            f'<rect x="46" y="-510" width="506" height="524" fill="#fff"/><rect x="46" y="-309.75" width="506" height="31.5" fill="#000"/></mask>'
            f'<g mask="url(#{mask_id})" fill="currentColor"><g transform="scale(1 -1)"><path d="{_MARK_PATH}"/></g></g></svg>')


def strip(name: str) -> str:
    return f'''<div class="cl-strip" role="note" style="background:#0E1014;color:#F4F1E8;font-family:'Manrope',-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif;font-size:14px;line-height:1.45;">
  <div style="max-width:1240px;margin:0 auto;padding:12px 20px;display:flex;align-items:center;gap:14px;flex-wrap:wrap;">
    <span style="display:inline-flex;align-items:center;gap:8px;font-family:'Space Grotesk','Helvetica Neue',Helvetica,Arial,sans-serif;font-weight:600;font-size:10px;letter-spacing:0.16em;text-transform:uppercase;color:#F4F1E8;white-space:nowrap;">
      {_mark(16, "clStripCut", "#F4F1E8")}
      Preview
    </span>
    <span style="color:rgba(244,241,232,0.8);flex:1 1 320px;min-width:0;">
      A first draft of what <b style="color:#F4F1E8;font-weight:600;">{esc(name)}</b> could look like, built by Clearline. Not their live site. Nothing here is published.
    </span>
    <a href="tel:+15599189067" style="font-family:'Space Grotesk','Helvetica Neue',Helvetica,Arial,sans-serif;font-weight:600;font-size:13px;color:#7A89FF;text-decoration:none;white-space:nowrap;padding:8px 0;margin:-8px 0;">Questions: 559-918-9067</a>
  </div>
</div>'''


def credit(name: str) -> str:
    subj = html.escape("About the site you built for " + name).replace(" ", "%20")
    return f'''<div class="cl-credit" style="margin-top:28px;padding-top:18px;border-top:1px solid rgba(244,241,232,0.16);display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;font-family:'Manrope',-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif;font-size:13px;color:rgba(244,241,232,0.55);">
  <span style="display:inline-flex;align-items:center;gap:10px;">
    {_mark(14, "clCreditCut", "#F4F1E8")}
    <span>Preview built by <a href="https://clearlinebuilds.com" style="color:#F4F1E8;text-decoration:none;font-weight:600;">Clearline</a>, a custom systems studio in Clovis, California. Want it live? <a href="mailto:braxton@clearlinebuilds.com?subject={subj}" style="color:#F4F1E8;text-decoration:underline;text-underline-offset:3px;">Email Braxton</a>.</span>
  </span>
  <a href="tel:+15599189067" style="color:#7A89FF;text-decoration:none;font-family:'Space Grotesk','Helvetica Neue',Helvetica,Arial,sans-serif;font-weight:600;padding:8px 0;margin:-8px 0;">559-918-9067</a>
</div>'''


CSS = r"""
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-padding-top:84px}
body{margin:0;font-family:var(--fb),system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;font-size:17px;line-height:1.6;color:var(--ink);background:#fff;-webkit-font-smoothing:antialiased}
img{display:block;max-width:100%;height:auto}
a{color:inherit}
h1,h2,h3,h4{margin:0;font-family:var(--fd),Georgia,serif;font-weight:var(--dw);letter-spacing:var(--dls);line-height:var(--dlh);text-wrap:balance}
h1{font-size:clamp(2.35rem,5.4vw,4.3rem);text-transform:var(--dtt)}
h2{font-size:clamp(1.8rem,3.3vw,2.7rem);text-transform:var(--dtt)}
h3{font-size:1.2rem;letter-spacing:-.015em}
p{margin:0}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
.kicker{display:block;margin:0 0 14px;font-weight:700;color:var(--a)}
.kicker.upper{font-size:12.5px;letter-spacing:.14em;text-transform:uppercase}
.kicker.small{font-family:var(--fd);font-style:italic;font-weight:500;font-size:1.05rem;letter-spacing:0}
.lead{font-size:1.1rem;color:var(--mut);max-width:62ch}
.sec{padding:88px 0}
.sec-h{max-width:680px;margin-bottom:44px}
.sec-h h2{margin-bottom:14px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:52px;padding:0 26px;border-radius:var(--rc);font-weight:700;font-size:1rem;text-decoration:none;border:0;cursor:pointer;font-family:inherit;line-height:1.1;transition:transform .15s ease,background-color .15s ease,color .15s ease}
.btn:active{transform:translateY(1px)}
.btn-p{background:var(--a);color:var(--on-a)}
.btn-p:hover{background:var(--a2);color:#fff}
.btn-ink{background:var(--ink);color:#fff}
.btn-ink:hover{background:var(--a)}
.btn-ghost{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.55)}
.btn-ghost:hover{background:rgba(255,255,255,.12)}
.btn-line{background:transparent;color:var(--ink);border:1.5px solid rgba(0,0,0,.18)}
.btn-line:hover{border-color:var(--ink)}
.btn svg{width:18px;height:18px;flex:none}
:focus-visible{outline:3px solid var(--a);outline-offset:3px}
.hair{border:0;border-top:1px solid rgba(0,0,0,.1);margin:0}

/* header */
.hdr{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.92);backdrop-filter:saturate(1.4) blur(12px);-webkit-backdrop-filter:saturate(1.4) blur(12px);border-bottom:1px solid rgba(0,0,0,.08)}
.hdr .wrap{display:flex;align-items:center;justify-content:space-between;gap:18px;height:76px}
.brand{min-width:0;text-decoration:none}
.brand b{display:block;font-family:var(--fd);font-weight:var(--dw);font-size:1.3rem;letter-spacing:var(--dls);line-height:1.1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-transform:var(--dtt)}
.brand span{display:block;font-size:11.5px;font-weight:600;letter-spacing:.11em;text-transform:uppercase;color:var(--mut);margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.nav{display:flex;gap:26px;font-size:15px;font-weight:600}
.nav a{text-decoration:none;color:var(--mut)}
.nav a:hover{color:var(--ink)}
.hdr-cta{display:flex;gap:10px;align-items:center;flex:none}
.hdr-cta .btn{min-height:46px;padding:0 18px;font-size:15px}
.hdr .call-sm{display:none}

/* hero shared */
.hero{position:relative;color:#fff;background:var(--ink);overflow:hidden}
.hero .bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.42}
.hero .sh{position:absolute;inset:0;background:linear-gradient(100deg,rgba(0,0,0,.82) 0%,rgba(0,0,0,.6) 50%,rgba(0,0,0,.25) 100%)}
.hero .wrap{position:relative}
.eyebrow{display:inline-flex;align-items:center;gap:9px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.24);border-radius:999px;padding:7px 15px 7px 11px;font-size:13.5px;font-weight:600;margin-bottom:24px}
.eyebrow .dot{width:9px;height:9px;border-radius:50%;background:#45c989;box-shadow:0 0 0 4px rgba(69,201,137,.25)}
.hero h1 small{display:block;font-size:.42em;font-weight:600;letter-spacing:.02em;margin-top:16px;opacity:.85;font-family:var(--fb);text-transform:none;line-height:1.3}
.hero .sub{font-size:1.15rem;line-height:1.55;color:rgba(255,255,255,.86);margin:22px 0 28px;max-width:58ch}
.cta{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:22px}
.rate{display:inline-flex;align-items:center;gap:10px;font-size:15px;font-weight:600}
.stars{display:inline-flex;gap:2px;font-size:17px;line-height:1;color:#ffc233}
.stars .off{color:rgba(255,255,255,.3)}
.rate.dark .stars .off{color:rgba(0,0,0,.18)}
.rate a{color:inherit;text-decoration:none;opacity:.8}
.rate a:hover{opacity:1;text-decoration:underline}

/* hero: split */
.hero-split .inner{display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:center;padding:84px 0 80px}
.qcard{background:#fff;color:var(--ink);border-radius:var(--rk);padding:28px;box-shadow:0 30px 70px rgba(0,0,0,.35)}
.qcard h3{font-size:1.35rem;margin-bottom:4px}
.qcard .qs{font-size:14.5px;color:var(--mut);margin-bottom:18px}
.qcard .or{text-align:center;font-size:14px;color:var(--mut);margin-top:14px}
.qcard .or a{font-weight:700;color:var(--a);text-decoration:none}

/* hero: cover */
.hero-cover .inner{min-height:min(82vh,760px);display:flex;flex-direction:column;justify-content:flex-end;padding:120px 0 64px}
.hero-cover .sh{background:linear-gradient(to top,rgba(0,0,0,.88) 0%,rgba(0,0,0,.55) 45%,rgba(0,0,0,.15) 100%)}
.hero-cover .bg{opacity:.75}
.hero-cover h1{max-width:18ch}
.hero-cover .badge{position:absolute;top:28px;right:24px;background:rgba(255,255,255,.95);color:var(--ink);border-radius:var(--rk);padding:14px 18px;display:flex;align-items:center;gap:12px;box-shadow:0 14px 40px rgba(0,0,0,.3)}
.hero-cover .badge b{font-family:var(--fd);font-size:1.7rem;line-height:1;font-weight:var(--dw)}
.hero-cover .badge span{font-size:12.5px;line-height:1.3;color:var(--mut)}

/* hero: paper */
.hero-paper{background:var(--wash);color:var(--ink)}
.hero-paper .inner{display:grid;grid-template-columns:1.05fr .95fr;gap:64px;align-items:center;padding:76px 0 88px}
.hero-paper .eyebrow{background:#fff;border-color:rgba(0,0,0,.1);color:var(--ink)}
.hero-paper .sub{color:var(--mut)}
.hero-paper .frame{position:relative;border-radius:var(--rk);overflow:visible}
.hero-paper .frame img{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:var(--rk);position:relative;box-shadow:0 30px 60px rgba(0,0,0,.18)}
.hero-paper .frame::before{content:"";position:absolute;inset:auto -18px -18px auto;width:62%;height:62%;background:var(--a);border-radius:var(--rk);opacity:.9}
.hero-paper .frame .tag{position:absolute;left:-14px;bottom:28px;background:#fff;border-radius:var(--rk);padding:12px 16px;box-shadow:0 12px 36px rgba(0,0,0,.16);font-size:14px;font-weight:600;display:flex;gap:10px;align-items:center}
.hero-paper .frame .tag .stars .off{color:rgba(0,0,0,.18)}
.hero-paper .btn-ghost{color:var(--ink);border-color:rgba(0,0,0,.22)}
.hero-paper .btn-ghost:hover{background:rgba(0,0,0,.05)}

/* quote band (cover and paper heroes) */
.qband{background:#fff;border-bottom:1px solid rgba(0,0,0,.08)}
.qband .wrap{display:grid;grid-template-columns:auto 1fr;gap:28px;align-items:center;padding:22px 24px}
.qband h3{font-size:1.1rem}
.qband p{font-size:14px;color:var(--mut)}
.qband form{display:grid;grid-template-columns:1fr 1fr 1.2fr auto;gap:10px}
.qband input,.qband select{margin:0}
.qband .btn{min-height:50px}
.qband .sent{text-align:left;padding:4px 0}

/* usp */
.usp{background:var(--a);color:var(--on-a)}
.usp .wrap{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;padding-top:20px;padding-bottom:20px}
.usp div{display:flex;align-items:center;gap:10px;justify-content:center;font-size:15px;font-weight:700;text-align:center}
.usp svg{width:18px;height:18px;flex:none}

/* services */
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.card{border:1px solid rgba(0,0,0,.09);border-radius:var(--rk);padding:30px 26px;background:#fff;transition:border-color .15s,transform .15s}
.card:hover{border-color:var(--a);transform:translateY(-2px)}
.card .ic{width:44px;height:44px;border-radius:calc(var(--rk) * .6);background:var(--wash);color:var(--a);display:flex;align-items:center;justify-content:center;font-family:var(--fd);font-weight:var(--dw);font-size:1.1rem;margin-bottom:18px}
.card h3{margin-bottom:8px}
.card p{color:var(--mut);font-size:15.5px}
.rows{display:grid;grid-template-columns:1fr 1fr;gap:0 48px;border-top:1px solid rgba(0,0,0,.12)}
.rows>div{display:grid;grid-template-columns:52px 1fr;gap:14px;padding:26px 0;border-bottom:1px solid rgba(0,0,0,.12)}
.rows .n{font-family:var(--fd);font-weight:var(--dw);font-size:1.5rem;color:var(--a);line-height:1}
.rows h3{margin-bottom:6px}
.rows p{color:var(--mut);font-size:15.5px}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:4px}
.tiles div{background:var(--wash);padding:30px 26px 34px;border-left:4px solid var(--a);border-radius:var(--rk)}
.tiles h3{margin-bottom:8px}
.tiles p{color:var(--mut);font-size:15.5px}

/* gallery */
.gal{display:grid;gap:14px}
.gal img{width:100%;height:100%;object-fit:cover;border-radius:var(--rk);background:var(--wash)}
.gal-bento{grid-template-columns:repeat(3,1fr);grid-auto-rows:250px}
.gal-bento .big{grid-column:span 2;grid-row:span 2}
.gal-strip{grid-template-columns:repeat(3,1fr)}
.gal-strip img{aspect-ratio:4/3}
.gal-columns{display:block;column-count:3;column-gap:14px}
.gal-columns img{break-inside:avoid;margin-bottom:14px}
.gal-note{margin-top:18px;font-size:14px;color:var(--mut)}

/* band */
.band{position:relative;color:#fff;background:var(--ink)}
.band img{width:100%;height:min(46vh,440px);object-fit:cover;opacity:.75}
.band .sh{position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.8),rgba(0,0,0,0) 70%)}
.band .wrap{position:absolute;left:0;right:0;bottom:36px}
.band h2{color:#fff;margin-bottom:8px}
.band p{color:rgba(255,255,255,.8);max-width:52ch}

/* trust */
.why{background:var(--wash)}
.tg{display:grid;grid-template-columns:repeat(4,1fr);gap:28px}
.tg h3{font-size:1.05rem;margin-bottom:8px;padding-left:14px;border-left:3px solid var(--a)}
.tg p{color:var(--mut);font-size:15px;padding-left:17px}

/* reviews */
.rv{display:grid;grid-template-columns:auto 1fr;gap:56px;align-items:center}
.rv .big{display:flex;align-items:baseline;gap:14px}
.rv .num{font-family:var(--fd);font-weight:var(--dw);font-size:clamp(4.5rem,9vw,7rem);line-height:.9;letter-spacing:-.04em}
.rv .of{font-size:1rem;color:var(--mut)}
.rv .stars{font-size:26px;margin:14px 0 8px}
.rv .stars .off{color:rgba(0,0,0,.15)}
.rv .cnt{font-weight:700}
.rv .lead{margin-bottom:22px}
.rv .links{display:flex;gap:12px;flex-wrap:wrap}

/* area + map */
.area{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start}
.towns{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 18px;padding:0;list-style:none}
.towns li{background:var(--wash);border-radius:var(--rc);padding:9px 14px;font-size:14.5px;font-weight:600}
.towns li.home{background:var(--a);color:var(--on-a)}
.map{border-radius:var(--rk);overflow:hidden;border:1px solid rgba(0,0,0,.1);height:340px;background:var(--wash)}
.map iframe{width:100%;height:100%;border:0;display:block}
.addr{font-size:15.5px;color:var(--mut);line-height:1.7}
.addr a{color:var(--a);font-weight:700;text-decoration:none}
.addr a:hover{text-decoration:underline}

/* faq */
.faq details{border-bottom:1px solid rgba(0,0,0,.12);padding:22px 0}
.faq details:first-of-type{border-top:1px solid rgba(0,0,0,.12)}
.faq summary{font-family:var(--fd);font-weight:var(--dw);letter-spacing:var(--dls);font-size:1.15rem;cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:20px;align-items:center}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--a);font-size:1.6rem;font-weight:400;line-height:1;flex:none;transition:transform .2s}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq details p{color:var(--mut);margin-top:12px;font-size:1rem;max-width:78ch}

/* quote */
.quote{background:var(--ink);color:#fff}
.quote .qg{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start}
.quote .kicker{color:rgba(255,255,255,.7)}
.quote .lead{color:rgba(255,255,255,.75)}
.quote .nap{margin-top:28px;font-size:1rem;line-height:1.9}
.quote .nap a.ph{font-family:var(--fd);font-weight:var(--dw);font-size:2rem;color:#fff;text-decoration:none;letter-spacing:var(--dls);display:inline-block;line-height:1.1;margin-bottom:8px}
.quote .nap a{color:#fff}
form{background:#fff;border-radius:var(--rk);padding:30px;color:var(--ink)}
label{display:block;font-size:13.5px;font-weight:700;margin-bottom:6px}
input,select,textarea{width:100%;border:1.5px solid rgba(0,0,0,.16);border-radius:var(--rc);padding:13px 14px;font:inherit;font-size:16px;margin-bottom:14px;background:#fbfbfc;color:var(--ink);min-height:50px}
select{appearance:none;-webkit-appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23555' stroke-width='2.5'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 14px center;padding-right:38px}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--a);box-shadow:0 0 0 3px color-mix(in srgb,var(--a) 22%,transparent)}
textarea{min-height:104px;resize:vertical}
form .btn{width:100%}
.fine{font-size:13px;color:var(--mut);margin-top:12px;text-align:center}
.note{font-size:14px;margin-top:10px;min-height:1.2em}
.note.err{color:#b4413a}
.sent{display:none;text-align:center;padding:30px 10px}
.sent .ck{width:58px;height:58px;border-radius:50%;background:var(--a);color:var(--on-a);font-size:28px;display:flex;align-items:center;justify-content:center;margin:0 auto 16px}
.sent h3{margin-bottom:8px}
.sent p{color:var(--mut)}
.is-sent .qf{display:none}.is-sent .sent{display:block}
.qband .is-sent{padding:0}

/* footer */
footer{background:#0b0f13;color:#9aa6b2;padding:60px 0 36px;font-size:14.5px}
.fg{display:grid;grid-template-columns:1.6fr 1fr 1fr;gap:40px;padding-bottom:34px;border-bottom:1px solid #1b2229}
footer h4{color:#fff;font-size:15px;margin-bottom:14px;font-family:var(--fb);letter-spacing:0}
footer .fn{color:#fff;font-family:var(--fd);font-weight:var(--dw);font-size:1.25rem;letter-spacing:var(--dls);margin-bottom:10px;text-transform:var(--dtt)}
footer a{text-decoration:none;color:#c6d0d9}
footer a:hover{color:#fff}
footer .col a{display:block;margin-bottom:9px}
.legal details{border-bottom:1px solid #1b2229;padding:16px 0}
.legal summary{font-size:15px;font-weight:700;color:#c6d0d9;cursor:pointer;list-style:none}
.legal summary::-webkit-details-marker{display:none}
.legal p{color:#9aa6b2;font-size:14px;line-height:1.7;margin-top:10px;max-width:90ch}
.fb{padding-top:22px;display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;font-size:13.5px}

/* sticky mobile bar */
.bar{display:none}

@media(prefers-reduced-motion:no-preference){
  .rise{animation:rise .7s cubic-bezier(.2,.7,.2,1) both}
  .rise:nth-child(2){animation-delay:.06s}.rise:nth-child(3){animation-delay:.12s}.rise:nth-child(4){animation-delay:.18s}.rise:nth-child(5){animation-delay:.24s}
  @keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
}

@media(max-width:1000px){
  .nav{display:none}
  .grid3,.tiles{grid-template-columns:1fr 1fr}
  .tg{grid-template-columns:1fr 1fr}
  .hero-split .inner{grid-template-columns:1fr;gap:34px;padding:60px 0 56px}
  .hero-paper .inner{grid-template-columns:1fr;gap:40px;padding:56px 0 64px}
  .hero-paper .frame{margin-right:18px}
  .qband form{grid-template-columns:1fr 1fr}
  .qband .wrap{grid-template-columns:1fr;gap:16px}
  .rv,.area,.quote .qg{grid-template-columns:1fr;gap:34px}
  .gal-columns{column-count:2}
}
@media(max-width:640px){
  body{font-size:16px;padding-bottom:72px}
  .wrap{padding:0 16px}
  .sec{padding:58px 0}
  .sec-h{margin-bottom:30px}
  .hdr .wrap{height:66px}
  .hdr-cta .btn-line,.hdr-cta .desk{display:none}
  .hdr .call-sm{display:inline-flex}
  .hero .sub{font-size:1.02rem}
  .hero-cover .inner{min-height:0;padding:96px 0 44px}
  .hero-cover .badge{top:16px;right:16px;padding:10px 12px}
  .hero-cover .badge b{font-size:1.3rem}
  .cta .btn{flex:1 1 100%}
  .qcard{padding:22px}
  .usp .wrap{grid-template-columns:1fr 1fr;gap:12px 10px}
  .usp div{justify-content:flex-start;text-align:left;font-size:14px}
  .grid3,.tiles,.rows,.tg{grid-template-columns:1fr}
  .rows{gap:0}
  .gal{gap:8px}
  .gal-bento{grid-template-columns:1fr 1fr;grid-auto-rows:140px}
  .gal-strip{grid-template-columns:1fr 1fr}
  .gal-columns{column-count:2;column-gap:8px}
  .gal-columns img{margin-bottom:8px}
  .band img{height:300px}
  .band .wrap{bottom:22px}
  .rv .num{font-size:4.5rem}
  .map{height:260px}
  form{padding:22px}
  .fg{grid-template-columns:1fr;gap:26px}
  .bar{display:grid;grid-template-columns:1fr 1fr;position:fixed;bottom:0;left:0;right:0;z-index:60;box-shadow:0 -6px 24px rgba(0,0,0,.22);padding-bottom:env(safe-area-inset-bottom,0);background:var(--ink)}
  .bar a{display:flex;align-items:center;justify-content:center;gap:8px;min-height:60px;font-weight:800;font-size:16px;text-decoration:none;color:#fff}
  .bar a svg{width:18px;height:18px}
  .bar .c{background:var(--a);color:var(--on-a)}
}
"""

ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.9 2z"/></svg>'
ICON_MSG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
ICON_CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'


def stars(rating: float, off_cls: str = "off") -> str:
    out = []
    for i in range(5):
        on = rating >= i + 0.75
        half = not on and rating >= i + 0.25
        out.append(f'<span class="{"" if on else ("half" if half else off_cls)}">{"★" if on or half else "☆"}</span>')
    return '<span class="stars" aria-hidden="true">' + "".join(out) + "</span>"


def _split_address(addr: str) -> tuple[str, str, str]:
    m = re.search(r"^(.*?),\s*([^,]+?),\s*CA\s*(\d{5})?", addr)
    if not m:
        return addr, "", ""
    street = m.group(1).strip()
    city = re.sub(r"^City of\s+", "", m.group(2).strip())
    return street, city, (m.group(3) or "")


def pick_photos(photos: list, hero_kind: str):
    """Hero wants a landscape photo (a portrait one for the paper frame). The
    band wants the widest of what is left. The gallery is the rest."""
    if not photos:
        return None, None, []
    rest = list(photos)
    want_portrait = hero_kind == "paper"
    def ratio(p):
        return p["w"] / max(p["h"], 1)
    cands = [p for p in rest if (ratio(p) < 0.95) == want_portrait] or rest
    hero = cands[0]
    rest.remove(hero)
    band = None
    if len(rest) >= 5:
        band = max(rest, key=ratio)
        rest.remove(band)
    return hero, band, rest[:6]


def quote_form(d: dict, services: list, compact: bool = False) -> str:
    opts = "".join(f"<option>{esc(s)}</option>" for s, _ in services) + "<option>Something else</option>"
    if compact:
        return f'''<div class="qwrap">
<form class="qf" data-cl-form novalidate style="padding:0;background:none;border-radius:0">
  <input name="name" placeholder="Your name" autocomplete="name" aria-label="Your name" required>
  <input name="phone" type="tel" placeholder="Phone number" autocomplete="tel" aria-label="Phone number" required>
  <select name="service" aria-label="What do you need">{opts}</select>
  <button class="btn btn-p" type="submit">Send it</button>
  <p class="note" aria-live="polite" style="grid-column:1/-1;margin:0"></p>
</form>
<div class="sent" aria-live="polite"><h3>Got it, thank you</h3><p>Somebody from {esc(d["short_name"])} will call you back.</p></div>
</div>'''
    return f'''<div class="qwrap">
<form class="qf" data-cl-form novalidate>
  <h3>Get a free quote</h3>
  <p class="qs">Takes 20 seconds. Somebody calls you back.</p>
  <input name="name" placeholder="Your name" autocomplete="name" aria-label="Your name" required>
  <input name="phone" type="tel" placeholder="Phone number" autocomplete="tel" aria-label="Phone number" required>
  <select name="service" aria-label="What do you need">{opts}</select>
  <button class="btn btn-p" type="submit">Send it</button>
  <p class="note" aria-live="polite"></p>
  <p class="or">or call <a href="tel:+1{d["tel"]}">{esc(d["phone"])}</a></p>
</form>
<div class="sent" aria-live="polite"><div class="ck">{ICON_CHECK}</div><h3>Got it, thank you</h3><p>We have your number. Somebody from {esc(d["short_name"])} will call you back. If it is urgent, call {esc(d["phone"])}.</p></div>
</div>'''


def render(d: dict) -> str:
    key = detect_trade(d["name"], d["category"])
    t = TRADES[key]
    look = LOOKS[t["look"]]
    a, a2, ink, wash, on_a = PALETTES[key]
    name, short = d["name"], d.get("short_name") or d["name"]
    city = d["city"]
    phone, tel = d["phone"], d["tel"]
    label, verb = t["label"], t["verb"]
    rating, reviews = d.get("rating"), d.get("reviews") or 0
    photos = d["photos"]
    hero, band, gallery = pick_photos(photos, LOOKS[t["look"]]["hero"])
    services = t["services"]
    areas = service_areas(city, d["target_city"])
    street, _, zipc = _split_address(d["address"])
    url = f"{SITE}/{d['slug']}/"
    maps_q = html.escape(f"{name} {d['address']}", quote=True).replace(" ", "+")
    place = d["place_id"]
    gmaps = f"https://www.google.com/maps/place/?q=place_id:{place}"
    directions = f"https://www.google.com/maps/dir/?api=1&destination={maps_q}&destination_place_id={place}"
    read_reviews = f"https://search.google.com/local/reviews?placeid={place}"
    write_review = f"https://search.google.com/local/writereview?placeid={place}"
    h1_svc = f"{label} in {city}"
    title = f"{label} in {city} | {name}"
    desc = f"{name} provides {verb} in {city} and the surrounding Central Valley. {t['promise']}. Call {phone}."
    kick = f'kicker {"upper" if look["kicker"] == "upper" else "small"}'

    jsonld = {
        "@context": "https://schema.org",
        "@type": SCHEMA_TYPE.get(key, "HomeAndConstructionBusiness"),
        "name": name, "telephone": phone, "url": url,
        "address": {"@type": "PostalAddress", "streetAddress": street, "addressLocality": city, "addressRegion": "CA", "postalCode": zipc, "addressCountry": "US"},
        "areaServed": [city] + areas,
        "sameAs": [gmaps],
    }
    if hero:
        jsonld["image"] = f"{SITE}/{d['slug']}/{hero['file']}"
    if rating:
        jsonld["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": rating, "reviewCount": reviews, "bestRating": 5}

    rating_line = ""
    if rating:
        rating_line = (f'<p class="rate"><span class="num">{stars(rating)}</span> <b>{rating:g}</b> '
                       f'<a href="{read_reviews}" target="_blank" rel="noopener">from {reviews:,} Google reviews</a></p>')

    # ----- hero -----
    hero_img = (f'<img class="bg" src="{hero["file"]}" alt="" width="{hero["w"]}" height="{hero["h"]}" fetchpriority="high" decoding="async">' if hero else "")
    h1 = f'<h1 class="rise">{esc(t["hook"])}<small>{esc(h1_svc)}</small></h1>'
    ctas = (f'<div class="cta rise"><a class="btn btn-p" href="tel:+1{tel}">{ICON_PHONE} Call {esc(phone)}</a>'
            f'<a class="btn btn-ghost" href="#quote">Request a free quote</a></div>')
    eyebrow = f'<p class="eyebrow rise"><span class="dot"></span> {esc(t["promise"])}</p>'
    sub = f'<p class="sub rise">{esc(t["sub"])}</p>'

    if look["hero"] == "split":
        hero_html = f'''<section class="hero hero-split" aria-label="Introduction">
  {hero_img}<div class="sh"></div>
  <div class="wrap"><div class="inner">
    <div>{eyebrow}{h1}{sub}{ctas}{rating_line}</div>
    <div class="qcard">{quote_form(d, services)}</div>
  </div></div>
</section>'''
        qband = ""
    elif look["hero"] == "cover":
        badge = (f'<div class="badge" aria-label="Google rating"><b>{rating:g}</b><span>{stars(rating)}<br>{reviews:,} Google reviews</span></div>' if rating else "")
        hero_html = f'''<section class="hero hero-cover" aria-label="Introduction">
  {hero_img}<div class="sh"></div>{badge}
  <div class="wrap"><div class="inner">{eyebrow}{h1}{sub}{ctas}{rating_line}</div></div>
</section>'''
        qband = f'''<section class="qband" aria-label="Quick quote"><div class="wrap">
  <div><h3>Get a free quote</h3><p>Takes 20 seconds. Somebody calls you back.</p></div>
  {quote_form(d, services, compact=True)}
</div></section>'''
    else:  # paper
        tag = (f'<div class="tag">{stars(rating)} <span>{rating:g} on Google</span></div>' if rating else "")
        frame = (f'<div class="frame rise"><img src="{hero["file"]}" alt="{esc(name)}, {esc(verb)} in {esc(city)}" width="{hero["w"]}" height="{hero["h"]}" fetchpriority="high" decoding="async">{tag}</div>' if hero else "")
        hero_html = f'''<section class="hero hero-paper" aria-label="Introduction">
  <div class="wrap"><div class="inner">
    <div>{eyebrow}{h1}{sub}{ctas}{rating_line.replace('class="rate"', 'class="rate dark"') if rating else ""}</div>
    {frame}
  </div></div>
</section>'''
        qband = f'''<section class="qband" aria-label="Quick quote"><div class="wrap">
  <div><h3>Get a free quote</h3><p>Takes 20 seconds. Somebody calls you back.</p></div>
  {quote_form(d, services, compact=True)}
</div></section>'''

    # ----- usp -----
    trust = TRUST[t["kind"]]
    usp_items = [trust[0][0], f"Serving {city} and nearby", (f"{rating:g} stars from {reviews:,} reviews" if rating else "Locally owned"), trust[1][0]]
    usp = '<section class="usp" aria-label="At a glance"><div class="wrap">' + "".join(f"<div>{ICON_CHECK}<span>{esc(x)}</span></div>" for x in usp_items) + "</div></section>"

    # ----- services -----
    if look["services"] == "cards":
        sv = '<div class="grid3">' + "".join(f'<div class="card"><div class="ic">{i+1}</div><h3>{esc(s)}</h3><p>{esc(b)}</p></div>' for i, (s, b) in enumerate(services)) + "</div>"
    elif look["services"] == "rows":
        sv = '<div class="rows">' + "".join(f'<div><span class="n">{i+1:02d}</span><div><h3>{esc(s)}</h3><p>{esc(b)}</p></div></div>' for i, (s, b) in enumerate(services)) + "</div>"
    else:
        sv = '<div class="tiles">' + "".join(f'<div><h3>{esc(s)}</h3><p>{esc(b)}</p></div>' for s, b in services) + "</div>"
    services_html = f'''<section class="sec" id="services"><div class="wrap">
  <div class="sec-h"><span class="{kick}">What we do</span><h2>{esc(label)} services in {esc(city)}</h2>
  <p class="lead">Every job gets the same thing: somebody who shows up when they said, explains what you are paying for, and cleans up after.</p></div>
  {sv}
</div></section>'''

    # ----- gallery -----
    gal_html = ""
    if len(gallery) >= 2:
        g = look["gallery"] if len(gallery) >= 4 else "strip"
        imgs = []
        for i, p in enumerate(gallery):
            cls = ' class="big"' if (g == "bento" and i == 0) else ""
            alt = f"{name}, {verb} in {city}, photo {i + 1}"
            img = f'<img src="{p["file"]}" alt="{esc(alt)}" width="{p["w"]}" height="{p["h"]}" loading="lazy" decoding="async">'
            imgs.append(f"<div{cls}>{img}</div>" if g == "bento" else img)
        gal_html = f'''<section class="sec" id="work" style="padding-top:0"><div class="wrap">
  <div class="sec-h"><span class="{kick}">Our work</span><h2>Recent jobs</h2>
  <p class="lead">Real photographs from real jobs. No stock images of somebody else's work.</p></div>
  <div class="gal gal-{g}">{"".join(imgs)}</div>
  <p class="gal-note">Photos: {esc(d["credits"] or name)}, via Google.</p>
</div></section>'''

    band_html = ""
    if band:
        band_html = f'''<section class="band" aria-label="On the job">
  <img src="{band["file"]}" alt="{esc(name)} on a job in {esc(city)}" width="{band["w"]}" height="{band["h"]}" loading="lazy" decoding="async"><div class="sh"></div>
  <div class="wrap"><h2>Local crew, not a call center</h2><p>You talk to the person doing the work. Same number every time.</p></div>
</section>'''

    # ----- trust -----
    why = f'''<section class="sec why" id="why"><div class="wrap">
  <div class="sec-h"><span class="{kick}">Why people call us</span><h2>What you can count on</h2></div>
  <div class="tg">{"".join(f"<div><h3>{esc(h)}</h3><p>{esc(b)}</p></div>" for h, b in trust)}</div>
</div></section>'''

    # ----- reviews -----
    rev = ""
    if rating:
        rev = f'''<section class="sec" id="reviews"><div class="wrap">
  <div class="rv">
    <div><div class="big"><span class="num">{rating:g}</span><span class="of">out of 5</span></div>{stars(rating)}<p class="cnt">{reviews:,} Google reviews</p></div>
    <div><span class="{kick}">Reviews</span><h2>What neighbors in {esc(city)} say</h2>
    <p class="lead" style="margin-top:14px">The rating is live on our Google profile. Read every review there, unedited, nothing cherry picked.</p>
    <div class="links"><a class="btn btn-ink" href="{read_reviews}" target="_blank" rel="noopener">Read the reviews on Google</a><a class="btn btn-line" href="{write_review}" target="_blank" rel="noopener">Leave a review</a></div></div>
  </div>
</div></section>'''

    # ----- area -----
    towns = f'<li class="home">{esc(city)}</li>' + "".join(f"<li>{esc(x)}</li>" for x in areas)
    area = f'''<section class="sec why" id="area"><div class="wrap">
  <div class="area">
    <div><span class="{kick}">Where we work</span><h2>{esc(city)} and the towns around it</h2>
      <ul class="towns">{towns}</ul>
      <p class="addr">Not sure if you are in range? Call <a href="tel:+1{tel}">{esc(phone)}</a> and ask. It is a short conversation.</p>
      <p class="addr" style="margin-top:18px">{esc(d["address"])}<br><a href="{directions}" target="_blank" rel="noopener">Get directions</a> &middot; <a href="{gmaps}" target="_blank" rel="noopener">Google profile</a></p>
    </div>
    <div class="map"><iframe src="https://maps.google.com/maps?q={maps_q}&z=13&output=embed" loading="lazy" title="Map to {esc(name)}" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
  </div>
</div></section>'''

    # ----- faq -----
    faq_items = faqs(t["kind"], city, phone, t["promise"], label)
    faq = f'''<section class="sec faq" id="faq"><div class="wrap">
  <div class="sec-h"><span class="{kick}">Questions</span><h2>The things people ask first</h2></div>
  {"".join(f"<details><summary>{esc(q)}</summary><p>{esc(a_)}</p></details>" for q, a_ in faq_items)}
</div></section>'''

    # ----- quote -----
    opts = "".join(f"<option>{esc(s)}</option>" for s, _ in services) + "<option>Something else</option>"
    quote = f'''<section class="sec quote" id="quote"><div class="wrap"><div class="qg">
  <div><span class="{kick}">Get in touch</span><h2>Tell us what you need</h2>
    <p class="lead" style="margin-top:14px">Fill this out and somebody calls you back. Or skip it and call, that is faster.</p>
    <div class="nap"><a class="ph" href="tel:+1{tel}">{esc(phone)}</a><br>{esc(d["address"])}<br><a href="{directions}" target="_blank" rel="noopener">Get directions</a></div>
  </div>
  <div class="qwrap">
  <form class="qf" data-cl-form novalidate>
    <label for="q-name">Your name</label><input id="q-name" name="name" placeholder="First and last" autocomplete="name" required>
    <label for="q-phone">Phone</label><input id="q-phone" name="phone" type="tel" placeholder="(559) 555-0134" autocomplete="tel" required>
    <label for="q-svc">What do you need?</label><select id="q-svc" name="service">{opts}</select>
    <label for="q-msg">Anything we should know</label><textarea id="q-msg" name="message" placeholder="Address, timing, what is going on"></textarea>
    <button class="btn btn-p" type="submit">Request my free quote</button>
    <p class="note" aria-live="polite"></p>
    <p class="fine">No obligation. Your number is not shared with anyone.</p>
  </form>
  <div class="sent" aria-live="polite" style="background:#fff;border-radius:var(--rk);padding:56px 30px;color:var(--ink)"><div class="ck">{ICON_CHECK}</div><h3>Got it, thank you</h3><p>Your request is in. Somebody from {esc(short)} will call you back. If it is urgent, call {esc(phone)}.</p></div>
  </div>
</div></div></section>'''

    # ----- footer -----
    footer = f'''<footer><div class="wrap">
  <div class="fg">
    <div><div class="fn">{esc(short)}</div><p style="max-width:36ch">{esc(label)} in {esc(city)} and the surrounding area. {esc(trust[0][0])}. {esc(trust[1][0])}.</p>
      <p style="margin-top:14px"><a href="tel:+1{tel}">{esc(phone)}</a><br>{esc(d["address"])}</p></div>
    <div class="col"><h4>Services</h4>{"".join(f'<a href="#services">{esc(s)}</a>' for s, _ in services[:5])}</div>
    <div class="col"><h4>Company</h4><a href="#work">Our work</a><a href="#reviews">Reviews</a><a href="#area">Service area</a><a href="#faq">FAQ</a><a href="#quote">Contact</a><a href="#privacy">Privacy policy</a></div>
  </div>
  <div class="legal" id="privacy">
    <details><summary>Privacy policy</summary><p>We collect only what you type into the quote form: your name, your phone number, the service you need and any notes you add. We use it to call you back about your job and nothing else. We do not sell it, rent it, or share it with any other company. If you want your information deleted, call {esc(phone)} and ask, and it is gone the same day.</p></details>
    <details id="terms"><summary>Terms of service</summary><p>Quotes are free and carry no obligation. A quote is valid for 30 days unless it says otherwise on the document. Work begins only after you approve the written price. Workmanship is guaranteed; manufacturer warranties on materials pass through to you at the terms the manufacturer sets. Prices can change if the job turns out to be different from what was visible at the walk-through, and if that happens we stop and tell you before doing the extra work.</p></details>
  </div>
  <div class="fb"><div>&copy; 2026 {esc(name)}. All rights reserved.</div><div>Photos: {esc(d["credits"] or name)}, via Google.</div></div>
  {credit(name)}
</div></footer>'''

    facts = {k: v for k, v in d.items() if k != "slug"}
    js = f'''<script>
(function(){{
  var SB='https://fusyxkmgzretrkcyyacs.supabase.co/rest/v1/demo_inquiries';
  var KEY='sb_publishable_jVR6cac6c3caVuBRgN1Blw_lkB_h5Ta';
  var PLACE={json.dumps(place)}, BIZ={json.dumps(name)};
  document.querySelectorAll('form[data-cl-form]').forEach(function(f){{
    var note=f.querySelector('.note'), btn=f.querySelector('button'), label=btn.textContent;
    f.addEventListener('submit',function(e){{
      e.preventDefault();
      var n=(f.elements.name.value||'').trim(), p=(f.elements.phone.value||'').trim();
      var s=f.elements.service?f.elements.service.value:'', m=f.elements.message?f.elements.message.value.trim():'';
      if(!n||!p){{note.textContent='Name and phone, then we can reach you.';note.className='note err';return;}}
      note.textContent='';note.className='note';btn.disabled=true;btn.textContent='Sending...';
      fetch(SB,{{method:'POST',headers:{{'apikey':KEY,'Content-Type':'application/json','Prefer':'return=minimal'}},
        body:JSON.stringify({{place_id:PLACE,business:BIZ,name:n,phone:p,message:(s?'['+s+'] ':'')+m}})}})
      .then(function(r){{if(!r.ok)throw new Error(r.status);var w=f.closest('.qwrap');w.classList.add('is-sent');w.querySelector('.sent').setAttribute('tabindex','-1');w.querySelector('.sent').focus();}})
      .catch(function(){{btn.disabled=false;btn.textContent=label;note.textContent='That did not go through. Please call {esc(phone)} instead.';note.className='note err';}});
    }});
  }});
}})();
</script>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="{ink}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(t["promise"])}. Call {esc(phone)}.">
<meta property="og:url" content="{url}">
{f'<meta property="og:image" content="{SITE}/{d["slug"]}/{hero["file"]}">' if hero else ""}
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='{a.replace("#", "%23")}'/%3E%3Ctext x='32' y='43' font-family='Arial,Helvetica,sans-serif' font-weight='700' font-size='34' fill='{on_a.replace("#", "%23")}' text-anchor='middle'%3E{esc(short[:1].upper())}%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family={look["fonts"]}&display=swap" rel="stylesheet">
{f'<link rel="preload" as="image" href="{hero["file"]}" fetchpriority="high">' if hero else ""}
<script type="application/ld+json">{json.dumps(jsonld)}</script>
<script type="application/json" id="cl-facts">{json.dumps(facts, ensure_ascii=False)}</script>
<style>
:root{{--a:{a};--a2:{a2};--ink:{ink};--wash:{wash};--on-a:{on_a};--mut:#5b6670;--fd:{look["display"]};--fb:{look["body"]};--dw:{look["dw"]};--dls:{look["dls"]};--dtt:{look["dtt"]};--dlh:{look["dlh"]};--rc:{look["rc"]};--rk:{look["rk"]}}}
{CSS}
</style>
</head>
<body class="look-{t["look"]} trade-{key}">
{strip(name)}
<a href="#main" class="btn btn-ink" style="position:absolute;left:-9999px;top:8px;z-index:100" onfocus="this.style.left='8px'" onblur="this.style.left='-9999px'">Skip to content</a>

<header class="hdr"><div class="wrap">
  <a class="brand" href="#main"><b>{esc(short)}</b><span>{esc(label)} &middot; {esc(city)}, CA</span></a>
  <nav class="nav" aria-label="Sections"><a href="#services">Services</a><a href="#work">Our work</a><a href="#reviews">Reviews</a><a href="#faq">FAQ</a><a href="#quote">Contact</a></nav>
  <div class="hdr-cta">
    <a class="btn btn-line" href="tel:+1{tel}">{ICON_PHONE} {esc(phone)}</a>
    <a class="btn btn-p call-sm" href="tel:+1{tel}" aria-label="Call {esc(phone)}">{ICON_PHONE} Call</a>
    <a class="btn btn-p desk" href="#quote">Get a quote</a>
  </div>
</div></header>

<main id="main">
{hero_html}
{qband}
{usp}
{services_html}
{gal_html}
{band_html}
{why}
{rev}
{area}
{faq}
{quote}
</main>
{footer}

<div class="bar" aria-label="Call or text"><a class="c" href="tel:+1{tel}">{ICON_PHONE} Call now</a><a href="sms:+1{tel}">{ICON_MSG} Text us</a></div>
{js}
</body>
</html>
'''
