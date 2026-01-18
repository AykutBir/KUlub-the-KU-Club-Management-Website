from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.routes.auth import require_login, require_role
from app.models.club_manager_model import ClubManager

club_manager_bp = Blueprint('club_manager', __name__)


def get_admin_club_or_error():
    """Helper to get the admin's club or return error response."""
    user_id = session.get('user_id')
    club = ClubManager.get_admin_club(user_id)
    if not club:
        return None, ("You are not assigned to manage any club.", 403)
    return club, None


# =============================================
# DASHBOARD
# =============================================

@club_manager_bp.route('/clubmgr')
@require_login
@require_role('CLUB_ADMIN')
def dashboard():
    """Club Manager Dashboard with KPIs."""
    club, error = get_admin_club_or_error()
    if error:
        return error

    # Get KPI data
    member_count = ClubManager.get_member_count(club['club_id'])
    upcoming_events = ClubManager.get_upcoming_events_count(club['club_id'])
    attendance_30d = ClubManager.get_total_attendance_last_30_days(club['club_id'])
    popular_event = ClubManager.get_most_popular_event(club['club_id'])

    return render_template(
        'club_manager/dashboard.html',
        club=club,
        member_count=member_count,
        upcoming_events=upcoming_events,
        attendance_30d=attendance_30d,
        popular_event=popular_event,
        user_name=session.get('name'),
        active_page='dashboard'
    )


# =============================================
# MEMBERSHIP MANAGEMENT
# =============================================

@club_manager_bp.route('/clubmgr/members')
@require_login
@require_role('CLUB_ADMIN')
def members():
    """Membership management page."""
    club, error = get_admin_club_or_error()
    if error:
        return error

    pending_requests = ClubManager.get_pending_requests(club['club_id'])
    current_members = ClubManager.get_current_members(club['club_id'])

    return render_template(
        'club_manager/members.html',
        club=club,
        pending_requests=pending_requests,
        current_members=current_members,
        user_name=session.get('name'),
        active_page='members'
    )


@club_manager_bp.route('/clubmgr/members/approve', methods=['POST'])
@require_login
@require_role('CLUB_ADMIN')
def approve_request():
    """Approve a membership request."""
    club, error = get_admin_club_or_error()
    if error:
        return jsonify({'success': False, 'message': error[0]}), error[1]

    request_id = request.form.get('request_id')
    if not request_id:
        return jsonify({'success': False, 'message': 'Request ID is required'}), 400

    success, message = ClubManager.approve_request(request_id, club['club_id'])
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400


@club_manager_bp.route('/clubmgr/members/decline', methods=['POST'])
@require_login
@require_role('CLUB_ADMIN')
def decline_request():
    """Decline a membership request."""
    club, error = get_admin_club_or_error()
    if error:
        return jsonify({'success': False, 'message': error[0]}), error[1]

    request_id = request.form.get('request_id')
    if not request_id:
        return jsonify({'success': False, 'message': 'Request ID is required'}), 400

    success, message = ClubManager.decline_request(request_id, club['club_id'])
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400


@club_manager_bp.route('/clubmgr/members/kick', methods=['POST'])
@require_login
@require_role('CLUB_ADMIN')
def kick_member():
    """Remove a member from the club."""
    club, error = get_admin_club_or_error()
    if error:
        return jsonify({'success': False, 'message': error[0]}), error[1]

    user_id = request.form.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'User ID is required'}), 400

    success, message = ClubManager.kick_member(user_id, club['club_id'])
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400


@club_manager_bp.route('/clubmgr/members/update-title', methods=['POST'])
@require_login
@require_role('CLUB_ADMIN')
def update_title():
    """Update a member's title."""
    club, error = get_admin_club_or_error()
    if error:
        return jsonify({'success': False, 'message': error[0]}), error[1]

    user_id = request.form.get('user_id')
    new_title = request.form.get('title')

    if not user_id or not new_title:
        return jsonify({'success': False, 'message': 'User ID and title are required'}), 400

    success, message = ClubManager.update_member_title(user_id, club['club_id'], new_title)
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400


# =============================================
# EVENT MANAGEMENT
# =============================================

@club_manager_bp.route('/clubmgr/events')
@require_login
@require_role('CLUB_ADMIN')
def events():
    """Event management page."""
    club, error = get_admin_club_or_error()
    if error:
        return error

    club_events = ClubManager.get_club_events(club['club_id'])
    venues = ClubManager.get_venues()

    return render_template(
        'club_manager/events.html',
        club=club,
        events=club_events,
        venues=venues,
        user_name=session.get('name'),
        active_page='events'
    )


@club_manager_bp.route('/clubmgr/events/create', methods=['POST'])
@require_login
@require_role('CLUB_ADMIN')
def create_event():
    """Create a new event."""
    club, error = get_admin_club_or_error()
    if error:
        return jsonify({'success': False, 'message': error[0]}), error[1]

    name = request.form.get('name')
    description = request.form.get('description')
    publish_date = request.form.get('publish_date')
    end_date = request.form.get('end_date')
    event_start_date = request.form.get('event_start_date')
    venue_id = request.form.get('venue_id')
    quota = request.form.get('quota')
    category = request.form.get('category')

    # Validation
    if not all([name, description, publish_date, end_date, venue_id, quota]):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400

    try:
        quota = int(quota)
        venue_id = int(venue_id)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid quota or venue'}), 400

    success, message = ClubManager.create_event(
        club['club_id'], name, description, publish_date, end_date,
        venue_id, quota, event_start_date, category
    )

    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400


@club_manager_bp.route('/clubmgr/events/delete', methods=['POST'])
@require_login
@require_role('CLUB_ADMIN')
def delete_event():
    """Delete an event."""
    club, error = get_admin_club_or_error()
    if error:
        return jsonify({'success': False, 'message': error[0]}), error[1]

    event_id = request.form.get('event_id')
    if not event_id:
        return jsonify({'success': False, 'message': 'Event ID is required'}), 400

    success, message = ClubManager.delete_event(event_id, club['club_id'])
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400


# =============================================
# ANALYTICS
# =============================================

@club_manager_bp.route('/clubmgr/analytics')
@require_login
@require_role('CLUB_ADMIN')
def analytics():
    """Analytics page with 7 advanced queries."""
    club, error = get_admin_club_or_error()
    if error:
        return error

    club_id = club['club_id']

    # Execute all 7 analytics queries
    event_performance = ClubManager.analytics_event_performance(club_id)
    top_3_events = ClubManager.analytics_top_3_events(club_id)
    avg_attendance = ClubManager.analytics_avg_attendance(club_id)
    quota_utilization = ClubManager.analytics_quota_utilization(club_id)
    weekly_trend = ClubManager.analytics_weekly_trend(club_id)
    follower_conversion = ClubManager.analytics_follower_conversion(club_id)
    inactive_members = ClubManager.analytics_inactive_members(club_id)

    return render_template(
        'club_manager/analytics.html',
        club=club,
        event_performance=event_performance,
        top_3_events=top_3_events,
        avg_attendance=avg_attendance,
        quota_utilization=quota_utilization,
        weekly_trend=weekly_trend,
        follower_conversion=follower_conversion,
        inactive_members=inactive_members,
        user_name=session.get('name'),
        active_page='analytics'
    )


# =============================================
# BUDGET TRACKING
# =============================================

@club_manager_bp.route('/clubmgr/budget')
@require_login
@require_role('CLUB_ADMIN')
def budget():
    """Budget tracking page."""
    club, error = get_admin_club_or_error()
    if error:
        return error

    transactions = ClubManager.get_budget_transactions(club['club_id'])
    monthly_breakdown = ClubManager.get_monthly_expense_breakdown(club['club_id'])
    income_vs_expense = ClubManager.get_income_vs_expense(club['club_id'])

    return render_template(
        'club_manager/budget.html',
        club=club,
        transactions=transactions,
        monthly_breakdown=monthly_breakdown,
        income_vs_expense=income_vs_expense,
        user_name=session.get('name'),
        active_page='budget'
    )


@club_manager_bp.route('/clubmgr/budget/add', methods=['POST'])
@require_login
@require_role('CLUB_ADMIN')
def add_transaction():
    """Add a new budget transaction."""
    club, error = get_admin_club_or_error()
    if error:
        return jsonify({'success': False, 'message': error[0]}), error[1]

    amount = request.form.get('amount')
    transaction_type = request.form.get('transaction_type')
    description = request.form.get('description')

    if not all([amount, transaction_type]):
        return jsonify({'success': False, 'message': 'Amount and type are required'}), 400

    if transaction_type not in ['INCOME', 'EXPENSE']:
        return jsonify({'success': False, 'message': 'Invalid transaction type'}), 400

    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({'success': False, 'message': 'Amount must be positive'}), 400
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid amount'}), 400

    success, message = ClubManager.add_budget_transaction(
        club['club_id'], amount, transaction_type, description
    )

    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400
