[Project website](https://www.benamuwo.me/schrodingers_civ/) · [Research repository](https://github.com/RavenSeldon/schrodingers_civ)

# Launching beside the existing Flask blog

The package is ready for static hosting. Nothing has been published, pushed or changed on a server. The existing domain's server configuration and hosting arrangement have not been inspected. The intended public address is exactly **https://www.benamuwo.me/schrodingers_civ/**.

## Existing Flask application — confirmed local context

The existing repository is `https://github.com/RavenSeldon/beamu-blog.git`. Within that checkout the Flask application is under **`WebDev/Blog/`**. Its `Procfile` launches `gunicorn wsgi:app`, and `wsgi.py` calls the application factory. These facts were checked by reading the entry-point files and Git remote only; the app was not started or imported.

Both `benamuwo.me` and `www.benamuwo.me` belong to the existing site. The new publication's canonical URL remains **https://www.benamuwo.me/schrodingers_civ/**.

**Direct-static deployment boundary:** serve the publication's static files at the web-server / ingress layer, alongside the existing Flask upstream. Do not add Flask routes, modify the application factory or templates, put this package in the blog's uploads directory, restart Gunicorn, or run the application's deployment/startup scripts for this task. No database connection, SQL command, migration command, schema change or model change is needed. The database, migrations, models, configuration secrets and application files are outside this deployment.

This delivery changes only the separate static website package and its documentation. No files in the Flask repository were edited. Nginx is the proposed routing layer **if the current host uses it**; its actual deployed configuration is still unverified.

## Choose the serving layer

This guide describes direct static serving through Nginx, which bypasses Flask completely. The separately requested **`url.py` / `views.py` option** is documented in [FLASK-WIRING.md](FLASK-WIRING.md), with ready-to-copy blueprint files. Those examples have not been installed in WebDev. Choose one serving layer; adding the optional blueprint would require an operator-controlled application reload, while a direct-static content release does not. Neither option needs database, migration or model changes.

## 1. Build and inspect locally

Use Node 22 or newer. The lockfile pins the dependencies; the browser tools are development-only. The deployed site has no dependencies, services, API keys, cookies or database.

```sh
npm ci
npm run build
npm run check
npm run preview
```

Open http://127.0.0.1:4173/schrodingers_civ/. For the rendered suite, leave the preview running and use another terminal:

```sh
npx playwright install chromium
npm run test:browser
```

The complete deployable tree is `dist/`. Its contents, including directory names, must be placed **inside** the server's `/schrodingers_civ/` path. Do not serve the repository root or `handoff/`. Opening HTML via `file://` is not supported because the site intentionally uses the canonical base path.

## 2. Place the source in a separate website repository

Create a new GitHub repository when ready. Initialize the website folder itself only after checking that it is outside any parent Git working tree. Do not initialize inside the research repository, copy that working tree, or change its remote. Use `.gitignore` to exclude `handoff/`, temporary QA images, dependencies and release archives. Inspect `git diff --cached --stat` and `git diff --cached` before committing. The selected public publication assets are versioned under `src/`; the research history remains in its original repository.

This delivery does not create or push a remote. The source archive includes only the site, selected assets, reproducible scripts and documentation. Keep the local original PDFs in `src/originals/` as provenance, not in the web root.

## 3. Add a path on the existing domain

If a DigitalOcean Droplet uses Nginx in front of this Flask/Gunicorn app, add the **locations only** from `docs/nginx-location.conf` to the existing HTTPS server block. Adapt the filesystem path and the system MIME include path. Preserve the existing Flask proxy location (usually `location /`), Gunicorn upstream/socket, authentication behavior, certificates and every unrelated route. The static location handles only `/schrodingers_civ/`; it never forwards those requests to Flask, including missing static files. Check whether an earlier regex location or existing path handler conflicts; the `^~` location prevents unrelated extension handlers from intercepting these assets.

For the two hostnames:

- If one HTTPS server block already serves both `benamuwo.me` and `www.benamuwo.me`, add the static locations there. Both hosts may serve this path; the generated canonical URLs point to `www`. Do not change the blog's global hostname behavior.
- If the hosts use separate HTTPS server blocks, add the static locations to the `www` block. In the apex block, optionally add only the two path-scoped redirects in `docs/nginx-apex-location.conf`. They preserve the chapter path and query string while leaving every other apex URL under its existing Flask routing.
- Inspect for an existing server-wide `www` → apex redirect before deployment. It would conflict with the requested `www` canonical path. The operator must exempt only this static path from that redirect; do not blindly add a competing apex → `www` redirect or change redirects for the whole blog.

There is no new DNS record for `/schrodingers_civ/`: DNS selects hosts, not paths. If the existing host runs elsewhere, the path must be configured there or reverse-proxied there to a DigitalOcean origin. A new subdomain is a different URL and does not meet the requested canonical address.

Test the merged configuration with `sudo nginx -t`; reload only after it passes. This is an example, not a claim that the existing server was inspected or that its configuration accepts this snippet unchanged. Apply the first configuration addition during a normal managed deployment; later content updates need only switch the release symlink.

## 4. Upload, activate and roll back atomically

Example layout on a Linux Droplet:

```text
/srv/schrodingers-civ/
  releases/
    20260914-001/
      schrodingers_civ/
        index.html
        assets/
        audit/
        atlas/
        tale/
  current -> releases/20260914-001
```

Choose a unique release ID and substitute your SSH user and hostname. The following is a deployment procedure for the operator to run; it was not executed here.

```sh
# Local machine, after npm run build && npm run check:
release_id=20260914-001
ssh DEPLOY_USER@DROPLET_HOST "mkdir -p /srv/schrodingers-civ/releases/$release_id/schrodingers_civ"
rsync -av --checksum dist/ "DEPLOY_USER@DROPLET_HOST:/srv/schrodingers-civ/releases/$release_id/schrodingers_civ/"
```

On the server, check that the uploaded tree contains only public files and its asset hashes match `assets/source-manifest.json`. Check `nginx -t` if configuration was changed. Preserve the previous symlink target, then switch within the same filesystem:

```sh
cd /srv/schrodingers-civ
readlink current > previous-release.txt  # May be absent on the first release.
ln -s releases/20260914-001 current.next
mv -Tf current.next current
```

`mv -T` is the GNU/Linux command used on the Droplet, not macOS syntax. The `current.next` name must be unused. Retain old releases; do not delete them during activation. No Nginx reload is normally needed for a content-only symlink switch. If the existing host has `open_file_cache` enabled, disable it for this location or reload according to the host's normal practice so cached descriptors do not delay activation.

After activation, verify the actual HTTPS address, a direct paper URL, a late chapter URL, both PDFs, all three Markdown downloads, one SVG and one WebP. Verify `/schrodingers_civ` redirects to `/schrodingers_civ/`, nested missing routes return HTTP 404, and the root website still works.

```sh
curl -I https://www.benamuwo.me/schrodingers_civ/
curl -I https://www.benamuwo.me/schrodingers_civ/atlas/paper/
curl -I https://www.benamuwo.me/schrodingers_civ/tale/epilogue/
curl -I https://www.benamuwo.me/schrodingers_civ/assets/papers/audit.pdf
curl -I https://www.benamuwo.me/schrodingers_civ/not-a-real-route/
```

If the smoke checks fail, point `current.next` at the prior release recorded in `previous-release.txt` and atomically rename it over `current`. Revert a configuration change separately from the backed-up configuration, run `nginx -t`, and reload through the host's normal process. The root site must remain intact throughout. Rollback is a static-file symlink switch; it does not run Flask commands or database migrations.

## MIME types, caching and alternate origins

HTML must be `text/html`; JS `text/javascript` or `application/javascript`; CSS `text/css`; SVG `image/svg+xml`; WebP `image/webp`; PDFs `application/pdf`; Markdown `text/markdown`; CSV `text/csv`; ZIP `application/zip`. The example inherits the standard system types and adds Markdown. If that MIME file already defines Markdown, keep only one mapping.

The example deliberately uses `Cache-Control: no-cache` (store and revalidate) for stable filenames. Enable gzip or Brotli only through the existing host's configuration. Do not apply immutable year-long caching to mutable PDF or HTML names. The site does not install a service worker. A future release may fingerprint assets and grant only those fingerprints immutable caching.

If this Flask app is on managed hosting without editable Nginx, configure a separate static component/origin through that platform’s ingress routing, with `/schrodingers_civ/` assigned to the static component and existing routes kept on Flask. Inspect the actual platform first; a Flask `Procfile` alone does not establish the hosting provider. If Flask routing is explicitly selected instead, use the isolated blueprint instructions in `FLASK-WIRING.md`; do not modify existing blog handlers. DigitalOcean App Platform static hosting or Railway can provide an alternate origin. To retain the requested `www.benamuwo.me/schrodingers_civ/` address, the existing domain must route that path to the origin, with the prefix preserved or translated consistently. Uploading the site to an unrelated origin or changing DNS alone cannot route a path. A Droplet serving this path directly is the simplest option when the existing site already uses Nginx there.
