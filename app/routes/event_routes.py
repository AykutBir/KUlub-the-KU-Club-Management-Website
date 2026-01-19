from flask import Blueprint, flash, redirect, request, session, url_for
from app.routes.auth import require_login
from app.models.event_model import Event

event_bp = Blueprint('events', __name__)


def _redirect_back():
    return redirect(request.referrer or url_for('dashboard.user_dashboard'))


def _validate_event_access(event_id):
    event = Event.get_event_by_id(event_id)
    if not event:
        flash('Event not found.', 'error')
        return None
    return event


@event_bp.route('/events/<int:event_id>/save', methods=['POST'])
@require_login
def save_event(event_id):
    role = session.get('role')
    if role == 'SYSTEM_ADMIN':
        flash('System admins cannot save events.', 'error')
        return _redirect_back()

    if not _validate_event_access(event_id):
        return _redirect_back()

    user_id = session.get('user_id')
    if Event.is_attending(user_id, event_id):
        flash('You are already attending this event. Cancel attendance first.', 'error')
        return _redirect_back()

    try:
        Event.save_event(user_id, event_id)
        flash('Event saved.', 'success')
    except Exception:
        flash('Unable to save this event right now.', 'error')
    return _redirect_back()


@event_bp.route('/events/<int:event_id>/unsave', methods=['POST'])
@require_login
def unsave_event(event_id):
    role = session.get('role')
    if role == 'SYSTEM_ADMIN':
        flash('System admins cannot unsave events.', 'error')
        return _redirect_back()

    if not _validate_event_access(event_id):
        return _redirect_back()

    try:
        Event.unsave_event(session.get('user_id'), event_id)
        flash('Event unsaved.', 'success')
    except Exception:
        flash('Unable to unsave this event right now.', 'error')
    return _redirect_back()


@event_bp.route('/events/<int:event_id>/attend', methods=['POST'])
@require_login
def attend_event(event_id):
    role = session.get('role')
    if role == 'SYSTEM_ADMIN':
        flash('System admins cannot attend events.', 'error')
        return _redirect_back()

    if not _validate_event_access(event_id):
        return _redirect_back()

    user_id = session.get('user_id')
    if Event.has_saved(user_id, event_id):
        flash('You saved this event. Unsave it before attending.', 'error')
        return _redirect_back()

    try:
        Event.attend_event(user_id, event_id)
        flash('You are now attending this event.', 'success')
    except Exception:
        flash('Unable to attend this event right now.', 'error')
    return _redirect_back()


@event_bp.route('/events/<int:event_id>/cancel_attendance', methods=['POST'])
@require_login
def cancel_attendance(event_id):
    role = session.get('role')
    if role == 'SYSTEM_ADMIN':
        flash('System admins cannot cancel attendance.', 'error')
        return _redirect_back()

    if not _validate_event_access(event_id):
        return _redirect_back()

    try:
        Event.cancel_attendance(session.get('user_id'), event_id)
        flash('Attendance canceled.', 'success')
    except Exception:
        flash('Unable to cancel attendance right now.', 'error')
    return _redirect_back()
