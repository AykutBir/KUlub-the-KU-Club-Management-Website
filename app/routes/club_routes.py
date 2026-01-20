from flask import Blueprint, flash, redirect, request, session, url_for
from app.routes.auth import require_login
from app.models.club_model import Club

club_bp = Blueprint('clubs', __name__)


def _redirect_back():
    return redirect(request.referrer or url_for('dashboard.user_dashboard'))


@club_bp.route('/clubs/<int:club_id>/follow', methods=['POST'])
@require_login
def follow_club(club_id):
    role = session.get('role')
    if role == 'SYSTEM_ADMIN':
        flash('System admins cannot follow clubs.', 'error')
        return _redirect_back()

    club = Club.get_club_by_id(club_id)
    if not club:
        flash('Club not found.', 'error')
        return _redirect_back()

    try:
        Club.follow_club(session.get('user_id'), club_id)
        flash('Club followed successfully.', 'success')
    except Exception:
        flash('Unable to follow this club right now.', 'error')
    return _redirect_back()


@club_bp.route('/clubs/<int:club_id>/unfollow', methods=['POST'])
@require_login
def unfollow_club(club_id):
    role = session.get('role')
    if role == 'SYSTEM_ADMIN':
        flash('System admins cannot unfollow clubs.', 'error')
        return _redirect_back()

    club = Club.get_club_by_id(club_id)
    if not club:
        flash('Club not found.', 'error')
        return _redirect_back()

    try:
        Club.unfollow_club(session.get('user_id'), club_id)
        flash('Club unfollowed successfully.', 'success')
    except Exception:
        flash('Unable to unfollow this club right now.', 'error')
    return _redirect_back()


@club_bp.route('/clubs/<int:club_id>/request_membership', methods=['POST'])
@require_login
def request_membership(club_id):
    role = session.get('role')
    if role != 'BASIC':
        flash('Only basic users can request club membership.', 'error')
        return _redirect_back()

    club = Club.get_club_by_id(club_id)
    if not club:
        flash('Club not found.', 'error')
        return _redirect_back()

    success, message = Club.create_membership_request(session.get('user_id'), club_id)
    flash(message, 'success' if success else 'error')
    return _redirect_back()


@club_bp.route('/clubs/leave', methods=['POST'])
@require_login
def leave_club():
    role = session.get('role')
    if role != 'BASIC':
        flash('Only basic users can leave clubs.', 'error')
        return _redirect_back()

    user_id = session.get('user_id')
    success, message = Club.leave_club(user_id)
    flash(message, 'success' if success else 'error')
    return _redirect_back()