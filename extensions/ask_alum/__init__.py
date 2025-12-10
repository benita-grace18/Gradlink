from flask import Blueprint

ask_bp = Blueprint('ask_alum', __name__,
                   template_folder='templates',
                   static_folder='static',
                   url_prefix='/ask')

from . import views  # noqa
