# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is Yinghao Sun's academic personal website, hosted via GitHub Pages at `sunyinghao-uestc.github.io`. It is based on the [Jon Barron academic website template](https://jonbarron.info/). The site is a pure static HTML/CSS site with no build system, package manager, or tests.

## Repository structure

- `index.html` — Main page (~4700 lines). Single-page academic profile with research publications, each entry is a table row with thumbnail images, paper info, and BibTeX citation data.
- `stylesheet.css` — Global styles (Lato font, link colors, paper title formatting, image hover effects).
- `CNAME` — Custom domain for GitHub Pages.
- `data/` — BibTeX files (`.bib`), CV PDF, bio text, and a BibTeX style file (`.bst`).
- `images/` — Publication thumbnails, profile photo, favicon, and MP4 video previews.
- `mipnerf/`, `mipnerf360/`, `zipnerf/` — Individual project pages for research papers. Each has its own `index.html`, `css/`, `js/`, and `img/` directories.

## How the main page works

Each publication in `index.html` is a `<tr>` with:
- A thumbnail column using a two-image hover effect (before/after images with CSS opacity transition controlled by inline `onmouseover`/`onmouseout` JavaScript functions).
- A text column with paper title, authors, venue, links (arXiv, project page, code, video, etc.), and a hidden BibTeX `<pre>` block that is shown/hidden via inline JS.

The `highlight` CSS class (`background-color: #ffffd0`) is used to mark featured papers.

## Development

No build step — edit files directly and serve statically:

```bash
# Local preview
python3 -m http.server 8000
# Then open http://localhost:8000
```

Push to the `master` branch to deploy via GitHub Pages.

## Customizing from the template

The site still contains Jon Barron's content (name, bio, photo, publications, social links). To complete the personalization, search for "Jon Barron" and "jonbarron" throughout `index.html` and replace with Yinghao Sun's information. Also update:
- `CNAME` if using a custom domain
- `data/` files (CV PDF, bio, BibTeX files)
- Profile photo in `images/`
- The `<title>` and `<meta name="author">` tags

## Publication entry pattern

When adding a new paper to `index.html`, follow the existing row pattern:
1. Copy an existing `<tr>` block
2. Update the unique function names for the hover effect (e.g., `vbanana_start`/`vbanana_stop`)
3. Update image paths, paper title, author list, venue, and links
4. Add the BibTeX citation in the hidden `<pre>` block
5. Add the `.bib` file in `data/`
