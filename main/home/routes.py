import sys
from . import db
from flask import (
    Flask, render_template,
    request, redirect, url_for,
    abort, flash, jsonify,
    make_response,
    Blueprint
)
from datetime import datetime as dt
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy

# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates'
)

@home_bp.route('/', methods=['GET'])
def home():
    """Homepage."""

    return render_template(
        'index.html',
        title='Flask Blueprint Demo',
        description='Demonstration of Flask blueprints in action.',
        template='home-template'
    )
