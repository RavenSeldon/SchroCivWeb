"""URL registration for the static publication only."""
from flask import Blueprint
from .views import publication

schrodingers_civ_bp = Blueprint(
    "schrodingers_civ", __name__, url_prefix="/schrodingers_civ"
)
schrodingers_civ_bp.add_url_rule(
    "", endpoint="without_slash", view_func=publication, defaults={"asset_path": ""}
)
schrodingers_civ_bp.add_url_rule(
    "/", endpoint="index", view_func=publication, defaults={"asset_path": ""}
)
schrodingers_civ_bp.add_url_rule(
    "/<path:asset_path>", endpoint="file", view_func=publication
)
