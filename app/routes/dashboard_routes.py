from flask import Blueprint, render_template, session, redirect, url_for
from app.routes.auth import require_login, require_role
from app.models.user_model import User
from app.models.club_model import Club
from app.models.event_model import Event
from app.db import get_cursor

dashboard_bp = Blueprint('dashboard', __name__)

def _redirect_for_role():
    role = session.get('role')
    if role == 'CLUB_ADMIN':
        return redirect(url_for('club_manager.dashboard'))
    if role == 'SYSTEM_ADMIN':
        return redirect(url_for('dashboard.admin_dashboard'))
    return redirect(url_for('auth.login_page'))

def _get_basic_user_or_redirect():
    user_id = session.get('user_id')
    user = User.get_user_profile(user_id)
    if not user:
        return None, redirect(url_for('auth.login_page'))
    if user.get('role') != 'BASIC':
        return None, _redirect_for_role()
    return user, None

@dashboard_bp.route('/user')
@require_login
@require_role('BASIC')
def user_dashboard():
    """Basic user dashboard"""
    return redirect(url_for('dashboard.basic_discover'))

@dashboard_bp.route('/basic/discover')
@require_login
def basic_discover():
    user, redirect_response = _get_basic_user_or_redirect()
    if redirect_response:
        return redirect_response

    user_id = user['user_id']
    first_name = user.get('name', 'User').split(' ')[0]
    clubs = Club.get_all_clubs()
    user_club = Club.get_user_club(user_id)
    membership_requests = Club.get_membership_requests_for_user(user_id)
    membership_status_by_club = {
        request['club_id']: request['status'] for request in membership_requests
    }
    followed_clubs = Club.get_followed_clubs(user_id)
    followed_club_ids = {club['club_id'] for club in followed_clubs}

    return render_template(
        'basic/discover.html',
        active_page='discover',
        user=user,
        first_name=first_name,
        clubs=clubs,
        user_club=user_club,
        membership_requests=membership_requests,
        membership_status_by_club=membership_status_by_club,
        followed_clubs=followed_clubs,
        followed_club_ids=followed_club_ids,
    )

@dashboard_bp.route('/basic/followed')
@require_login
def basic_followed():
    user, redirect_response = _get_basic_user_or_redirect()
    if redirect_response:
        return redirect_response

    user_id = user['user_id']
    first_name = user.get('name', 'User').split(' ')[0]
    followed_clubs = Club.get_followed_clubs(user_id)

    return render_template(
        'basic/followed.html',
        active_page='followed',
        user=user,
        first_name=first_name,
        followed_clubs=followed_clubs,
    )

@dashboard_bp.route('/basic/feed')
@require_login
def basic_feed():
    user, redirect_response = _get_basic_user_or_redirect()
    if redirect_response:
        return redirect_response

    user_id = user['user_id']
    first_name = user.get('name', 'User').split(' ')[0]
    followed_clubs = Club.get_followed_clubs(user_id)
    followed_club_ids = {club['club_id'] for club in followed_clubs}
    events = Event.get_upcoming_events()
    if followed_club_ids:
        events = [event for event in events if event.get('club_id') in followed_club_ids]
    saved_events = Event.get_user_saved_events(user_id)
    attended_events = Event.get_user_attended_events(user_id)
    saved_event_ids = {event['event_id'] for event in saved_events}
    attending_event_ids = {event['event_id'] for event in attended_events}

    return render_template(
        'basic/feed.html',
        active_page='feed',
        user=user,
        first_name=first_name,
        events=events,
        followed_clubs=followed_clubs,
        saved_event_ids=saved_event_ids,
        attending_event_ids=attending_event_ids,
    )

@dashboard_bp.route('/basic/my-club')
@require_login
def basic_my_club():
    user, redirect_response = _get_basic_user_or_redirect()
    if redirect_response:
        return redirect_response

    user_id = user['user_id']
    first_name = user.get('name', 'User').split(' ')[0]
    user_club = Club.get_user_club(user_id)
    membership_requests = Club.get_membership_requests_for_user(user_id)

    return render_template(
        'basic/my_club.html',
        active_page='my_club',
        user=user,
        first_name=first_name,
        user_club=user_club,
        membership_requests=membership_requests,
    )

@dashboard_bp.route('/basic/my-events')
@require_login
def basic_my_events():
    user, redirect_response = _get_basic_user_or_redirect()
    if redirect_response:
        return redirect_response

    user_id = user['user_id']
    first_name = user.get('name', 'User').split(' ')[0]
    saved_events = Event.get_user_saved_events(user_id)
    attended_events = Event.get_user_attended_events(user_id)

    return render_template(
        'basic/my_events.html',
        active_page='my_events',
        user=user,
        first_name=first_name,
        saved_events=saved_events,
        attended_events=attended_events,
    )

@dashboard_bp.route('/basic/profile')
@require_login
def basic_profile():
    user, redirect_response = _get_basic_user_or_redirect()
    if redirect_response:
        return redirect_response

    first_name = user.get('name', 'User').split(' ')[0]

    return render_template(
        'basic/profile.html',
        active_page='profile',
        user=user,
        first_name=first_name,
    )

    # Legacy route redirects to the new Basic pages.

@dashboard_bp.route('/admin')
@require_login
@require_role('SYSTEM_ADMIN')
def admin_dashboard():
    """System admin dashboard"""
    user_id = session.get('user_id')
    user = User.get_user_profile(user_id)
    if not user:
        return redirect(url_for('auth.login_page'))

    first_name = user.get('name', 'User').split(' ')[0]
    
    # Execute database queries for overview statistics
    cursor = get_cursor()
    try:
        # Total Users (all three types)
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        # Active Clubs
        cursor.execute("SELECT COUNT(*) FROM clubs")
        active_clubs = cursor.fetchone()[0]
        
        # Upcoming Events (events where end_date >= today, excluding overdue events)
        cursor.execute("SELECT COUNT(*) FROM events WHERE end_date >= CURDATE()")
        upcoming_events = cursor.fetchone()[0]
        
        # Club Membered Basic Users
        cursor.execute("""
            SELECT COUNT(DISTINCT cm.user_id) 
            FROM club_members cm 
            JOIN users u ON cm.user_id = u.user_id 
            WHERE u.role = 'BASIC'
        """)
        club_membered_users = cursor.fetchone()[0]
        
        # Non-member Basic Users (for comparison)
        cursor.execute("""
            SELECT COUNT(*) 
            FROM users 
            WHERE role = 'BASIC' 
            AND user_id NOT IN (SELECT user_id FROM club_members)
        """)
        non_member_users = cursor.fetchone()[0]
        
    except Exception as e:
        # Set default values on error
        total_users = 0
        active_clubs = 0
        upcoming_events = 0
        club_membered_users = 0
        non_member_users = 0
    finally:
        cursor.close()
    
    return render_template(
        'admin_dashboard.html',
        first_name=first_name,
        total_users=total_users,
        active_clubs=active_clubs,
        upcoming_events=upcoming_events,
        club_membered_users=club_membered_users,
        non_member_users=non_member_users
    )
