from flask import Blueprint
from app.routes.auth import require_login, require_role

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/user')
@require_login
@require_role('BASIC')
def user_dashboard():
    """Basic user dashboard"""
    return "user"

@dashboard_bp.route('/clubmgr')
@require_login
@require_role('CLUB_ADMIN')
def clubmgr_dashboard():
    """Club admin dashboard"""
    return "clubmgr"

@dashboard_bp.route('/admin')
@require_login
@require_role('SYSTEM_ADMIN')
def admin_dashboard():
    """System admin dashboard"""
    return "admin"

