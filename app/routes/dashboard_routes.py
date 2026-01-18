from flask import Blueprint, render_template, session, redirect, url_for
from app.routes.auth import require_login, require_role
from app.models.user_model import User
from app.models.club_model import Club
from app.models.event_model import Event

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/user')
@require_login
@require_role('BASIC')
def user_dashboard():
    """Basic user dashboard"""
    user_id = session.get('user_id')
    # Load profile data for the header and profile panel
    user = User.get_user_profile(user_id)
    if not user:
        return redirect(url_for('auth.login_page'))

    # Use first name for the greeting
    first_name = user.get('name', 'User').split(' ')[0]
    # Gather discovery, membership, and event data for the dashboard sections
    clubs = Club.get_all_clubs()
    user_club = Club.get_user_club(user_id)
    membership_requests = Club.get_membership_requests_for_user(user_id)
    membership_status_by_club = {
        request['club_id']: request['status'] for request in membership_requests
    }

    events = Event.get_upcoming_events()

    # TODO: Replace with saved/attended event lookups once tables exist.
    saved_event_ids = set()
    attending_event_ids = set()

    return render_template(
        'basic_dashboard.html',
        user=user,
        first_name=first_name,
        clubs=clubs,
        user_club=user_club,
        membership_requests=membership_requests,
        membership_status_by_club=membership_status_by_club,
        events=events,
        saved_event_ids=saved_event_ids,
        attending_event_ids=attending_event_ids,
    )

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
