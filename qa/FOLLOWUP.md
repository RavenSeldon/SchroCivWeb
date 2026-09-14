[Project website](https://www.benamuwo.me/schrodingers_civ/) · [Research repository](https://github.com/RavenSeldon/schrodingers_civ)

# Scoped follow-up: seal, favicon and Flask integration instructions

The only presentation changes are the landing hero (supplied Maitrism Seal SVG, contained without cropping/recolouring) and the publication-scoped favicon (same SVG bytes). All 31 other HTML documents and all 23 chapter images match their pre-change hashes. The main benamuwo.me favicon and all Flask application files remain untouched.

The landing was rendered at 360×800 and 1440×1000: image loaded, no page overflow, correct contain sizing and zero axe WCAG A/AA violations. The favicon HTTP response was 200 and matched the supplied SVG bytes. Evidence: `landing-update.json`, `screenshots/landing-seal-360.png`, `screenshots/landing-seal-1440.png`.

The complete optional Flask integration consists of three new Python example files and a two-line registration patch. It has NOT been installed into WebDev. The inspected factory and WSGI entry point already support the existing blueprint registry; they require no changes. See `docs/FLASK-WIRING.md` for the full Python change inventory and deployment/rollback instructions.

The example blueprint passed isolated Flask test-client checks for all 31 routes and 46 asset hashes, GET/HEAD, root route preservation, both hostnames, query-preserving trailing-slash redirects, publication 404s, path/symlink escape rejection and a missing-installation 503. The test uses a new minimal Flask app and imports none of the blog's code. No database, migration, model, application start or live request is involved.

The direct Nginx option bypasses Flask entirely. The optional Python option is explicitly distinguished: the blueprint has no database calls, but existing application-wide startup/request hooks have not been audited, and loading new Python routes would require the operator's normal app reload. No reload was performed.

Current static checks: 1,857 local links, 46 asset hashes, all 23 chapters. The static output is about 4.25 MB because the exact SVG is present as both hero and favicon. Original full-suite QA remains recorded separately; it was not unnecessarily repeated for this bounded change.
