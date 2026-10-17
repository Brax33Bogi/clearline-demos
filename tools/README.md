# tools/polish

Re-renders every demo page in this repo from the facts already on it.

```
python3 -m tools.polish            # every site
python3 -m tools.polish some-slug  # one site
```

Run from the repo root. Photos are never touched. Running it twice gives the
same bytes, because each rendered page carries its facts in a
`<script type="application/json" id="cl-facts">` block that the next run reads.

What it does, in order:

- `extract.py` pulls the business name, phone, Google rating and review count,
  address, place id, photo credit line and photo list off the page. Nothing
  else on the finished page is a fact about the business.
- `trades.py` works out the trade from the business name first and the old
  Google category second, so a plumber is a plumber even when Google filed it
  under heating and air. It carries the service list, headline, response
  promise, trust points and FAQ for 25 trades, and the towns around the
  business's own city for the service area.
- `looks.py` holds eight visual systems (type, radius, hero, services and
  gallery layouts) and a palette per trade. None of them is Clearline's brand:
  the page wears the prospect's trade. The only Clearline pieces are the
  preview strip and the credit line, copied from `brand/demo-site-chrome.html`
  in the engine repo.
- `render.py` writes the page: one H1 with service and city, phone and quote
  form above the fold, USP bar, services, real photos, trust, Google rating
  with links to read and leave reviews, service area with map and directions,
  six FAQs, full quote form with a thank-you state, privacy and terms, sticky
  call and text bar on phones, LocalBusiness JSON-LD and Open Graph tags.

The quote form posts to the same Supabase `demo_inquiries` table as before,
with the same columns.

These pages were produced by Engine V1, which is retired, so nothing
overwrites them. The live engine (`engine-v2` in `Brax33Bogi/clearline-engine`)
renders its own demos with `stations/demo-template.js`; if that template should
pick up any of this, port it there rather than pointing it at this tool.
