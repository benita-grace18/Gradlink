from flask import Blueprint

mcs_bp = Blueprint(
    'mcs', __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/mcs'
)

from . import views  # noqa
