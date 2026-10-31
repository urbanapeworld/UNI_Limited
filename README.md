# Uni Profiles — company website

Static, single-page website for **Uni Profiles Pvt. Ltd.**, a heavy steel fabrication works at Rajgangpur, Odisha.

## Structure

```
index.html   the whole site (HTML, CSS and JS in one file)
img/         project and facility photos, plus logo.png
```

No build step and no dependencies. The only external request is the Inter font from Google Fonts. Apple devices use the system SF Pro font instead.

## Run locally

Open `index.html` in a browser, or serve the folder:

```
python3 -m http.server 8000
```

## Deploy

Any static host works. Point it at the repository root:

- **GitHub Pages:** Settings → Pages → deploy from branch `main`, folder `/ (root)`.
- **Netlify, Vercel or Cloudflare Pages:** import the repo with no build command and `/` as the publish directory.

## Before going live

- **Approvals:** confirm the validity of the ISO 9001, factory licence, SAIL RSP and RDSO approvals. Several dates in the 2024 company profile have passed.
- **Photos:** replace the images in `img/` with higher-resolution ones. The current images were extracted from the PDF profile and are 300–1,000 px wide. Keep the same filenames, or update the `src` paths in `index.html`.
