# Uni Profiles — company website

Static website for **Uni Profiles Pvt. Ltd.**, a heavy steel fabrication works at Rajgangpur, Odisha. It is deployed to **Cloudflare Workers as static assets**. There is no build step and no server code.

## Structure

```
public/                      what Cloudflare serves (generated HTML is committed)
  index.html                 home
  about/ facility/ approvals/ projects/ clients/ contact/
  products/                  hub + one page per product family (6)
  assets/site.css, site.js   shared styles and behaviour
  sitemap.xml, robots.txt    generated
  404.html, _headers, img/
tools/build.py               generates every page, sitemap and robots.txt
tools/icons.svg              icon sprite included in each page
```

### Editing content

All copy, products, projects, clients and approvals live in `tools/build.py`. Edit there, then run:

```
pip install pillow          # once
python3 tools/build.py      # rewrites the pages in public/
```

Commit both `tools/` and `public/`. Do not hand-edit generated HTML: the next build overwrites it.

The canonical domain is the `SITE` constant at the top of `build.py` (used in canonical tags, sitemap and schema). After CSS/JS changes, bump `ASSET_V`.

### After going live

1. Google Search Console: add the domain property, submit `/sitemap.xml`.
2. Add a Google Business Profile for the works address, with the website set to the home page.

All commands go through `npm run`. Wrangler is installed locally from `package.json`, so you never need `npx` or a global install.

## Commands

```
npm install        # once, installs the pinned wrangler
npm run dev        # local server at http://localhost:8787
npm run check      # dry-run deploy: validates config and assets, uploads nothing
npm run deploy     # publish to Cloudflare
```

Node 20 or newer is required (`.nvmrc` pins 22).

## Deploy option A: from your machine

1. `npm install`
2. `npm run deploy`. The first run opens a browser to log in to Cloudflare.
3. The site goes live at `https://uni-profiles.<your-subdomain>.workers.dev`.

## Deploy option B: automatic on every push (recommended)

1. In the Cloudflare dashboard, go to **Workers & Pages → Create → Import a repository**.
2. Pick `urbanapeworld/UNI_Limited`, branch `main`.
3. Set the build settings:
   - **Build command:** `npm install`
   - **Deploy command:** `npm run deploy`
   - **Root directory:** `/`
4. Save and deploy. Every push to `main` now redeploys automatically.

Cloudflare prefills the deploy command as `npx wrangler deploy`. Replace it with `npm run deploy` so the build uses the wrangler version pinned in `package.json`.

## Custom domain

In the Worker's **Settings → Domains & Routes → Add → Custom domain**, enter `uniprofiles.net` and `www.uniprofiles.net`. The domain's DNS must be on Cloudflare. If it is with another registrar, add the domain to Cloudflare first and change the nameservers there.

## Before going live

- **Approvals:** confirm the validity of the ISO 9001, factory licence, SAIL RSP and RDSO approvals. Several dates in the 2024 company profile have passed.
- **Photos:** replace the images in `public/img/` with higher-resolution ones. The current images were extracted from the PDF profile and are 300–1,000 px wide. Keep the same filenames, or update the `src` paths in `public/index.html`.
