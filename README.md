# OldPulsarStudio.github.io

Official website for **OldPulsar Studio** — landing page and hosted legal pages for our apps.

## Structure

| File | Purpose |
|------|---------|
| `index.html` | Studio landing page |
| `style.css` | Shared styles |
| `terms/index.html` | Terms of service at `/terms` (paste content into `<main>`) |
| `privacy/index.html` | Privacy policy at `/privacy` (paste content into `<main>`) |
| `assets/` | Brand SVGs (OldPulsar mark, Artio icon, favicon) |

## Local preview

```bash
cd OldPulsarStudio.github.io
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080).

## Deploy (GitHub Pages)

1. Push this repo to GitHub (`OldPulsarStudio/OldPulsarStudio.github.io`).
2. **Settings → Pages → Build and deployment**
3. Source: **Deploy from a branch**
4. Branch: `main` / **/ (root)**
5. Save — the site will be live at `https://oldpulsarstudio.github.io/`

## Legal pages (English + Spanish)

Content is generated from the Artio policy files in the expense tracker repo:

- `../expense_tracker/policy_terms/artio-privacy-policy-v2.md`
- `../expense_tracker/policy_terms/artio-terms-of-service-v2.md`

After editing those files, rebuild the site pages:

```bash
cd OldPulsarStudio.github.io/scripts
python3 build-legal-pages.py
```

Published at `/privacy` and `/terms`.
