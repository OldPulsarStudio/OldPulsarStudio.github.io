#!/usr/bin/env python3
"""Build terms/index.html and privacy/index.html from expense_tracker docs."""

from pathlib import Path

from md_to_legal_html import convert

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT.parent / "expense_tracker" / "docs"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#020617">
  <title>{title} — OldPulsar Studio</title>
  <link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="../assets/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600&family=Syne:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <header class="site-header">
    <div class="container">
      <a class="brand" href="/">
        <img class="brand__mark" src="../assets/oldpulsar-mark.svg" alt="" width="32" height="32">
        <span>OldPulsar Studio</span>
      </a>
      <nav class="site-nav" aria-label="Main">
        <a href="/#projects">Projects</a>
        <a href="/#contact">Contact</a>
      </nav>
    </div>
  </header>

  <main class="page-legal">
    <div class="container legal">
      <div class="legal-body">
      {body}
      </div>
    </div>
  </main>

  <footer class="site-footer">
    <div class="container">
      <a class="site-footer__email" href="mailto:oldpulsarstudio@gmail.com">oldpulsarstudio@gmail.com</a>
      <nav class="site-footer__legal" aria-label="Legal">
        <a href="/terms">Terms</a>
        <a href="/privacy">Privacy</a>
      </nav>
      <p class="site-footer__copy">&copy; <span id="year"></span> OldPulsar Studio</p>
    </div>
  </footer>

  <script>
    document.getElementById("year").textContent = new Date().getFullYear();
  </script>
</body>
</html>
"""


def build(name: str, md_file: str, out_dir: str, title: str, description: str) -> None:
    md_path = DOCS / md_file
    body = convert(md_path.read_text(encoding="utf-8"))
    html = TEMPLATE.format(title=title, description=description, body=body)
    out_path = ROOT / out_dir / "index.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"Wrote {out_path}")


def main() -> None:
    build(
        "privacy",
        "artio-privacy-policy.md",
        "privacy",
        "Artio Privacy Policy",
        "Artio Privacy Policy — OldPulsar Studio",
    )
    build(
        "terms",
        "artio-terms-of-service.md",
        "terms",
        "Artio Terms of Service",
        "Artio Terms of Service — OldPulsar Studio",
    )


if __name__ == "__main__":
    main()
