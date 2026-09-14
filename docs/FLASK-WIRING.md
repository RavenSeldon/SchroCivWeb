[Project website](https://www.benamuwo.me/schrodingers_civ/) · [Research repository](https://github.com/RavenSeldon/shrodingers_civ.git)

# Optional Flask wiring: url.py and views.py

These are **instructions and example files only**. Nothing has been added to the WebDev repository or the live server. The database, migrations, models, blog favicon and existing routes remain untouched.

## What exists today

Read-only inspection confirmed the `beamu-blog` remote and the Flask app at `/Users/theda/PycharmProjects/PythonProject/WebDev/Blog/`. Its entry point is `gunicorn wsgi:app`. Blueprints are registered inside `register_blueprints(app)` in `app/routes/__init__.py`. No existing `url.py` or `views.py` files were found in the app; this is Flask blueprint routing, not a Django URL configuration.

To use the names you requested without rewriting existing modules, the supplied examples form a **new, isolated blueprint**:

```text
WebDev/Blog/app/routes/schrodingers_civ/
  __init__.py
  url.py       # registers only /schrodingers_civ and its descendants
  views.py     # serves public files from a separate static release directory
```

The three ready-to-copy files are under `docs/flask-integration/schrodingers_civ/` in this website package. They use Flask and the Python standard library; Python 3.9+ is needed for `Path.is_relative_to`. No database or model library is used by this blueprint.

## Complete Python change inventory

| Target in WebDev/Blog | Action |
| --- | --- |
| `app/routes/schrodingers_civ/__init__.py` | New package marker; included in this delivery |
| `app/routes/schrodingers_civ/url.py` | New blueprint and all publication URL rules; included |
| `app/routes/schrodingers_civ/views.py` | New static-file handler, redirects, MIME types and publication errors; included |
| `app/routes/__init__.py` | Add the blueprint import and registration; exact patch included |
| `app/__init__.py` | No change needed: the existing factory already calls `register_blueprints(app)` |
| `wsgi.py` | No change needed: it already loads that factory |
| Existing blog route modules, models, migrations and database configuration | No changes |

This is the complete wiring set for the inspected Flask structure. No additional Python dependency or database-backed model is required. The examples are implemented and tested in isolation; installation into the existing app remains an operator action.

## Wiring to apply later

1. Install the built `dist/` tree as `/srv/schrodingers-civ/current/schrodingers_civ/`, using the release-directory and symlink procedure in `DEPLOYMENT.md`. Keep the files separate from the blog's uploads and database directories. The application process needs read access to this public tree only.
2. Copy the three example files into the new directory shown above. Do not replace an existing route file, `url.py`, or `views.py`.
3. Inside the **existing** `register_blueprints(app)` function, add only these two lines, alongside the existing registrations:

```python
from app.routes.schrodingers_civ.url import schrodingers_civ_bp
app.register_blueprint(schrodingers_civ_bp)
```

An exact two-line registration patch against the inspected file is included at `docs/flask-integration/register-blueprint.patch`. It has not been applied. Keep every existing import and registration unchanged. This example does not require changes to `app/__init__.py`, `wsgi.py`, models, migrations, or database settings.

4. If the static release lives elsewhere, configure the single environment variable `SCHRODINGERS_CIV_ROOT` to its absolute directory. Do not copy, edit or disclose the app's existing secrets. For a separate local test, that path may point to this website's `dist/` directory.
5. The operator must load the new blueprint through the host's normal code reload process. Unlike direct Nginx static serving, adding a Flask blueprint requires a reload of the application workers. This package does **not** run that reload. Do not run a deployment wrapper that includes migration commands. Existing application startup hooks may have their own behavior; inspect those separately before an operator initiates a reload. The isolated tests for these examples do not import or start the blog.

Requests to the prefix reach `publication()` in `views.py`. It sends existing files, redirects directory URLs to a trailing slash, and returns the publication's own HTTP 404 page for missing files. Missing installation returns 503. It rejects traversal and file symlinks that escape the selected public release. MIME types and cache revalidation are explicit. It does not render Flask templates, query the database, read models, authenticate users, or intercept the blog's root route.

Global middleware and application-wide request hooks still apply to any Flask blueprint. This package has not inspected or changed them; the view's lack of database calls does not certify that the rest of the existing application never accesses its database during a request. If the requirement is that publication requests must bypass Flask entirely, use the Nginx option in `DEPLOYMENT.md` instead.

## Hostnames and the favicon

The same blueprint works behind both `benamuwo.me` and `www.benamuwo.me`. The site's canonical address remains `https://www.benamuwo.me/schrodingers_civ/`. Do not change global hostname redirects. Verify that an existing `www` → apex redirect does not conflict with this path; the guide covers path-only routing for the two hosts.

The Maitrism Seal favicon is referenced by these static pages as `/schrodingers_civ/assets/favicon.svg`. **Do not replace `/favicon.ico`, the blog's templates, or its static favicon.** The seal also replaces only the publication landing-page hero image. All chapter artwork remains intact.

Choose one serving owner: if the Nginx `^~ /schrodingers_civ/` location is installed, it handles this path before Gunicorn and the blueprint is unnecessary. If Flask is the chosen owner, leave the existing proxy to Gunicorn in place and do not add the competing Nginx static location.

## Check and undo

After an operator applies the integration, check the landing page, a direct chapter URL, paper reader, SVG favicon, PDF/Markdown downloads, a missing route and trailing-slash redirects. Verify the ordinary blog homepage still works. No database command belongs in these checks.

To remove the optional Python integration, remove only its two registration lines and the new blueprint directory, then follow the normal operator-controlled worker reload. To roll back static content, restore the previous publication release symlink. Neither operation requires a schema change or migration.
