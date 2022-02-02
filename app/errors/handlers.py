from app import db
from flask import render_template
from app.errors import bp


@bp.app_errorhandler(403)
def not_found_error(error):
    """
    Function renders 403.html page back to user
    triggered if normal user tries to acceess a page in the admin bp
    """
    return render_template('errors/403.html'), 400


@bp.app_errorhandler(404)
def not_found_error(error):
    """
    Function renders 404.html page back to user
    """
    return render_template('errors/404.html'), 400


@bp.app_errorhandler(500)
def internal_error(error):
    """
    Function renders 404.html page back to user
    """
    # Ensure failed db session doesn't interfere with db access
    db.session.rollback()
    return render_template('errors/500.html'), 500
