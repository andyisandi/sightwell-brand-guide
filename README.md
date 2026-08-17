# Sightwell Studios — Brand Guideline

A single-page brand guideline site: colors, typography, logo, brand strategy, voice
and tone, grids, icons, and applications. Plus a "Machine" view that exports the whole
guideline as a `SKILL.md` for Claude.

**`index.html` is the site.** It is self-contained — the vector logo and the label
typeface are embedded — so you can open it directly or drop it on any host.

## Fonts

**Freight Text Pro (serif)** loads from **Adobe Fonts**, via this line already in the
`<head>`:

```html
<link rel="stylesheet" href="https://use.typekit.net/qcx2rwd.css">
```

Adobe Fonts kits are **domain-locked**, so you must allow the domain you publish on:

1. fonts.adobe.com → **My Adobe Fonts → Web Projects**
2. Open the **`qcx2rwd`** project → **Edit**
3. Under **Domains**, add your site's domain — e.g. `yourname.github.io`
   (and any custom domain, e.g. `brand.sightwellstudios.com`)
4. **Save**

Until that's done — and when previewing locally from `file://` — the serif falls back
to Georgia. This is expected; it switches to real Freight Text once live on an
allowed domain.

**Pragmatica Extended (labels, captions)** *is* available on Adobe Fonts — no license
purchase or self-hosted file needed. It just isn't in kit `qcx2rwd` yet:

1. fonts.adobe.com → **Web Projects** → open **`qcx2rwd`** → **Add font**
2. Search **Pragmatica Extended**, include **weights 400 and 500**
3. **Save**

The CSS already asks for `pragmatica-extended` first, so it takes over the moment it's
in the kit. Until then, labels fall back to **Archivo Expanded** (embedded in the page),
which is close enough that the layout doesn't shift.

## Publish on GitHub Pages

```bash
git init
git add .
git commit -m "Sightwell brand guideline site"
git branch -M main
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```

Then: repo **Settings → Pages → Source: Deploy from a branch** → `main` / `/ (root)` →
**Save**. The site goes live at `https://<username>/<repo>/` within a minute or two.
Finally, add that domain to the Adobe Fonts kit (see above).

## Editing

`index.html` is generated — don't edit it directly. Edit the source and rebuild:

```
src/page.html   # markup + CSS (the real source)
src/build.py    # embeds the label font, builds the logo symbols, wraps the document
assets/sightwell-logo.svg   # logo exported from Figma
```

```bash
python3 src/build.py     # regenerates index.html
```

Source of truth for the brand content is the Figma file **Sightwell x Claude**.

## Files

```
index.html                     the site (generated — this is what GitHub Pages serves)
README.md
assets/
  logo_cream_ember.svg         primary — cream + amber (also the source for the inline
                               sidebar/footer mark, recolored via currentColor)
  logo_ink_ember.svg           reversed — ink + amber
  logo_all ink.svg             single-color ink
  logo_all cream.svg           single-color cream
  header image.png             original hero photograph (source, not served)
  header.jpg                   optimized hero background used by the page (43KB)
  applications/                imagery pulled from Figma pages 16-19
fonts/                         optional: PragmaticaExtended-Medium.woff2
src/page.html                  source markup + CSS
src/build.py                   build script
```

### Logo downloads

The four tiles in **Logo & Usage** are clickable — each downloads its SVG with a clean
filename (e.g. `sightwell-logo-cream-amber.svg`). Downloads work when the page is served
over http(s) or opened locally; they are blocked inside sandboxed preview iframes.

### Hero background

The hero uses `assets/header.jpg` with a left-to-right charcoal gradient over it, so the
headline keeps contrast while the amber light stays visible on the right. The photo's dark
edge is exactly Ink `#222223`, so it blends into the sidebar. To swap the image, replace
`assets/header.jpg` (keep it wide — 1920px+ — and dark on the left).
