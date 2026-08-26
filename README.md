# our-agency.co.uk — static clone

A self-contained static copy of <https://our-agency.co.uk> (a WordPress site fronted by
NitroPack and a Cloudflare/openresty bot filter), captured on 2026-08-26.

Everything the site needs is in `site/` — 127 pages and 799 assets, with no requests to the
original domain or its CDN at runtime.

## Running it

The clone uses root-relative URLs (`/wp-content/...`, `/services/branding/`), so it has to be
served over HTTP; opening `site/index.html` via `file://` will not resolve them.

```sh
python3 serve.py          # http://127.0.0.1:8000  (pass a port to override)
```

Any static file server works as long as it maps a directory request to its `index.html`:

```sh
npx serve site
```

## Deployment

`vercel.json` serves `site/` as the deployment root, so the clone's root-relative URLs resolve.
It also sets `X-Robots-Tag: noindex, nofollow` on every response: this is a byte-level copy of a
live business's site, and letting search engines index it would put a duplicate of Our Agency's
pages and branding into results under someone else's domain. Remove that header block if the
deployment is ever meant to be indexed.

## What is in `site/`

| Path | Contents |
| --- | --- |
| `index.html`, `contact/`, `studio/`, `services/…`, `project/…` | 127 page directories, each an `index.html` |
| `wp-content/` | Theme CSS/JS, uploads, and the WebP-Express image variants |
| `combinedCss/`, `externalFontFace/` | NitroPack's combined stylesheets |
| `wp-includes/` | WordPress core scripts the theme depends on |
| `_fonts/`, `_cdn/` | Google Fonts files, and the Typekit fonts NitroPack proxies |

Pages are copies of the **original server HTML**, not snapshots of the rendered DOM. That
distinction matters: NitroPack's loader only runs against the markup it shipped, and replaying a
post-JavaScript snapshot makes it abort before it loads the theme's JavaScript. Keeping the
original markup means the clone boots the same 11 scripts the live site does, so lazy-loading,
scroll animations and the rest of the theme behave as they do in production.

## Deliberate differences from the live site

- **Third-party tracking is removed.** Google Tag Manager / gtag, Facebook, HubSpot and
  NitroPack's telemetry beacon are stripped so that browsing the clone does not report traffic to
  the original site's analytics. The `<script>` elements are left in place but disarmed, because
  NitroPack looks them up by id and throws if they are missing.
- **Absolute URLs were rewritten to root-relative paths.** Links between captured pages, images,
  stylesheets, fonts and scripts all point inside `site/`. URLs that were never captured — the
  WordPress REST API (`/wp-json/…`), RSS feeds, `xmlrpc.php`, and genuinely external hosts such as
  Instagram, Vimeo and Google Maps — were left absolute and still point at the internet.
- **Server-side features do not work.** The contact form, search, and the Cloudflare Turnstile
  widget need the live WordPress backend; they render but submit nowhere.
- **The Complianz cookie banner is removed.** Its markup ships in the HTML, but the stylesheet
  that makes it a small corner popup is generated per banner by WordPress
  (`wp-content/uploads/complianz/css/banner-1-optin.css`) and is only ever referenced through a
  `banner-{banner_id}-{type}.css` template that the plugin fills in at runtime — so no literal URL
  pointed at it and it was never captured. Unstyled, it rendered as a full-width block. With the
  tracking scripts stripped there is also nothing left for it to gate, so `build.js` drops the
  banner, its "manage consent" tab and its config script.

## How it was captured

The origin sits behind a bot filter that answers non-browser clients with a "One moment,
please..." interstitial, so `curl` and `wget` cannot read the site — the challenge is tied to the
client's TLS fingerprint, and a captured session cookie does not transfer. The capture therefore
ran entirely through headless Chromium:

1. `crawl.js` — walk the site from the homepage, recording page URLs and every asset response.
2. `rawcrawl.js` — re-fetch each discovered page and keep the raw server HTML.
3. `fetch2.js` / `refetch.js` — pull the assets NitroPack lazy-loads, which never appear as
   network requests during an ordinary page load.
4. `build.js` — rewrite URLs, remove trackers, and assemble `site/`.

Those scripts are working tools rather than part of the deliverable, so they are not checked in;
`site/` is the artifact.

## Provenance

All content, images and branding belong to Our Agency. This is an unmodified copy of a public
website, kept for reference; it is not authorised for republication.
