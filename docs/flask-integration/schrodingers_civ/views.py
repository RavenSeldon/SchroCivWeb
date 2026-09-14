"""Serve a separately deployed public tree; never import the blog or its models."""
import os
from pathlib import Path

from flask import Response, redirect, request, send_from_directory, url_for

DEFAULT_ROOT = "/srv/schrodingers-civ/current/schrodingers_civ"
MIME_TYPES = {
    ".html": "text/html", ".css": "text/css", ".js": "text/javascript",
    ".svg": "image/svg+xml", ".webp": "image/webp", ".png": "image/png",
    ".pdf": "application/pdf", ".md": "text/markdown", ".csv": "text/csv",
    ".json": "application/json", ".xml": "application/xml", ".zip": "application/zip",
}


def _headers(response):
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


def _missing(root):
    file = root / "404.html"
    if file.is_file() and file.resolve().is_relative_to(root):
        response = send_from_directory(str(root), "404.html", mimetype="text/html")
        response.status_code = 404
        return _headers(response)
    return _headers(Response("Publication page not found.\n", status=404, mimetype="text/plain"))


def publication(asset_path=""):
    # Resolve the release symlink once per request, so a release switch is atomic.
    root = Path(os.environ.get("SCHRODINGERS_CIV_ROOT", DEFAULT_ROOT)).resolve()
    if not root.is_dir():
        return _headers(Response("Publication files are not installed.\n", status=503,
                                 mimetype="text/plain"))
    candidate = (root / asset_path).resolve()
    if not candidate.is_relative_to(root):
        return _missing(root)
    if candidate.is_dir():
        if not request.path.endswith("/"):
            target = (url_for("schrodingers_civ.file", asset_path=asset_path + "/")
                      if asset_path else url_for("schrodingers_civ.index"))
            if request.query_string:
                target += "?" + request.query_string.decode("latin-1")
            return redirect(target, code=308)
        candidate = (candidate / "index.html").resolve()
        if not candidate.is_relative_to(root):
            return _missing(root)
    if not candidate.is_file():
        return _missing(root)
    return _headers(send_from_directory(
        str(root), str(candidate.relative_to(root)),
        mimetype=MIME_TYPES.get(candidate.suffix.lower(), "application/octet-stream"),
        conditional=True,
    ))
