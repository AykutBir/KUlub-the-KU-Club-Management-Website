from flask import Blueprint, request, jsonify, session
from app.routes.auth import require_login, require_role
from app.models.user_model import User
from app.models.club_model import Club
from app.models.event_model import Event
from app.db import get_db, get_cursor
from datetime import datetime
import bcrypt

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/users/create', methods=['POST'])
@require_login
@require_role('SYSTEM_ADMIN')
def create_user():
    """Create a new user (admin-only)"""
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Invalid request payload'
            }), 400
        
        firstName = data.get('firstName', '').strip()
        lastName = data.get('lastName', '').strip()
        email = data.get('email', '').strip()
        birthdate = data.get('birthdate', '').strip()
        password = data.get('password', '')

        # Validate required fields
        if not firstName:
            return jsonify({
                'success': False,
                'message': 'First name is required',
                'field': 'FirstName'
            }), 400

        if not lastName:
            return jsonify({
                'success': False,
                'message': 'Last name is required',
                'field': 'LastName'
            }), 400

        if not email:
            return jsonify({
                'success': False,
                'message': 'Email is required',
                'field': 'Email'
            }), 400

        # Validate KU email format
        if not email.endswith('@ku.edu.tr'):
            return jsonify({
                'success': False,
                'message': 'Please use a valid KU Mail address (@ku.edu.tr)',
                'field': 'Email'
            }), 400

        if not birthdate:
            return jsonify({
                'success': False,
                'message': 'Birthdate is required',
                'field': 'Birthdate'
            }), 400

        # Validate date format (YYYY-MM-DD)
        try:
            datetime.strptime(birthdate, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Invalid date format. Please use YYYY-MM-DD format',
                'field': 'Birthdate'
            }), 400

        if not password or len(password) < 8:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 8 characters',
                'field': 'Password'
            }), 400

        # Check if email already exists
        existing_user = User.get_user_by_email(email)
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'Email already registered',
                'field': 'Email'
            }), 400

        # Create new user
        try:
            user = User.create_user(firstName, lastName, email, birthdate, password)
            return jsonify({
                'success': True,
                'message': 'User created successfully',
                'data': user
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'An error occurred during user creation. Please try again.'
            }), 500

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred during user creation'
        }), 500

@admin_bp.route('/admin/users/search', methods=['POST'])
@require_login
@require_role('SYSTEM_ADMIN')
def search_users():
    """Search users with pagination"""
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Invalid request payload'
            }), 400
        
        # Handle None/null values properly
        role_val = data.get('role')
        role = role_val.strip() if role_val and isinstance(role_val, str) else None
        
        name_val = data.get('name')
        name = name_val.strip() if name_val and isinstance(name_val, str) else None
        
        club_name_val = data.get('club_name')
        club_name = club_name_val.strip() if club_name_val and isinstance(club_name_val, str) else None
        
        page = int(data.get('page', 1))
        
        if page < 1:
            page = 1
        
        result = User.search_users(role=role, name=name, club_name=club_name, page=page, per_page=5)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred during search'
        }), 500

@admin_bp.route('/admin/users/promote-club-admin', methods=['POST'])
@require_login
@require_role('SYSTEM_ADMIN')
def promote_club_admin():
    """Promote a basic user to club admin"""
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Invalid request payload'
            }), 400
        
        user_id = data.get('user_id')
        club_id = data.get('club_id')
        
        if not user_id or not club_id:
            return jsonify({
                'success': False,
                'message': 'User ID and Club ID are required'
            }), 400
        
        # Verify user exists and has role 'BASIC'
        user = User.get_user_by_id(user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        if user['role'] != 'BASIC':
            return jsonify({
                'success': False,
                'message': 'User must have BASIC role to be promoted to club admin'
            }), 400
        
        # Verify club exists
        club = Club.get_club_by_id(club_id)
        if not club:
            return jsonify({
                'success': False,
                'message': 'Club not found'
            }), 404
        
        # Check if club already has an admin
        if club['admin_user_id'] is not None:
            return jsonify({
                'success': False,
                'message': 'This club already has a manager. Please revoke the existing manager first.'
            }), 400
        
        # Update club admin and user role in transaction
        db = get_db()
        cursor = get_cursor()
        try:
            # Set club admin
            cursor.execute(
                "UPDATE clubs SET admin_user_id = %s WHERE club_id = %s",
                (user_id, club_id)
            )
            # Update user role
            cursor.execute(
                "UPDATE users SET role = 'CLUB_ADMIN' WHERE user_id = %s",
                (user_id,)
            )
            db.commit()
            
            return jsonify({
                'success': True,
                'message': 'User promoted to club admin successfully'
            }), 200
        except Exception as e:
            db.rollback()
            return jsonify({
                'success': False,
                'message': 'An error occurred during promotion'
            }), 500
        finally:
            cursor.close()
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred during promotion'
        }), 500

@admin_bp.route('/admin/users/revoke-club-admin', methods=['POST'])
@require_login
@require_role('SYSTEM_ADMIN')
def revoke_club_admin():
    """Revoke club admin status"""
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Invalid request payload'
            }), 400
        
        club_id = data.get('club_id')
        user_id = data.get('user_id')
        
        if not club_id or not user_id:
            return jsonify({
                'success': False,
                'message': 'Club ID and User ID are required'
            }), 400
        
        # Verify club exists
        club = Club.get_club_by_id(club_id)
        if not club:
            return jsonify({
                'success': False,
                'message': 'Club not found'
            }), 404
        
        # Verify user is the club's admin
        if club['admin_user_id'] != user_id:
            return jsonify({
                'success': False,
                'message': 'User is not the admin of this club'
            }), 400
        
        # Update in transaction
        db = get_db()
        cursor = get_cursor()
        try:
            # Remove club admin
            cursor.execute(
                "UPDATE clubs SET admin_user_id = NULL WHERE club_id = %s",
                (club_id,)
            )
            # Update user role to BASIC
            cursor.execute(
                "UPDATE users SET role = 'BASIC' WHERE user_id = %s",
                (user_id,)
            )
            db.commit()
            
            return jsonify({
                'success': True,
                'message': 'Club admin revoked successfully'
            }), 200
        except Exception as e:
            db.rollback()
            return jsonify({
                'success': False,
                'message': 'An error occurred during revocation'
            }), 500
        finally:
            cursor.close()
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred during revocation'
        }), 500

@admin_bp.route('/admin/users/promote-system-admin', methods=['POST'])
@require_login
@require_role('SYSTEM_ADMIN')
def promote_system_admin():
    """Promote a user to system admin"""
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Invalid request payload'
            }), 400
        
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'User ID is required'
            }), 400
        
        # Verify user exists
        user = User.get_user_by_id(user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Verify user has role 'BASIC' or 'CLUB_ADMIN'
        if user['role'] not in ['BASIC', 'CLUB_ADMIN']:
            return jsonify({
                'success': False,
                'message': 'User must have BASIC or CLUB_ADMIN role to be promoted to system admin'
            }), 400
        
        # Count current system admins
        current_count = User.count_users_by_role('SYSTEM_ADMIN')
        if current_count >= 4:
            return jsonify({
                'success': False,
                'message': f'Cannot promote: System must have 2-4 system administrators. Current count: {current_count}'
            }), 400
        
        # If promoting CLUB_ADMIN, first revoke their club admin status
        db = get_db()
        cursor = get_cursor()
        try:
            if user['role'] == 'CLUB_ADMIN':
                # Find the club they manage
                cursor.execute(
                    "SELECT club_id FROM clubs WHERE admin_user_id = %s",
                    (user_id,)
                )
                club_result = cursor.fetchone()
                if club_result:
                    club_id = club_result[0]
                    cursor.execute(
                        "UPDATE clubs SET admin_user_id = NULL WHERE club_id = %s",
                        (club_id,)
                    )
            
            # Update user role to SYSTEM_ADMIN
            cursor.execute(
                "UPDATE users SET role = 'SYSTEM_ADMIN' WHERE user_id = %s",
                (user_id,)
            )
            db.commit()
            
            return jsonify({
                'success': True,
                'message': 'User promoted to system admin successfully'
            }), 200
        except Exception as e:
            db.rollback()
            return jsonify({
                'success': False,
                'message': 'An error occurred during promotion'
            }), 500
        finally:
            cursor.close()
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred during promotion'
        }), 500

@admin_bp.route('/admin/users/revoke-system-admin', methods=['POST'])
@require_login
@require_role('SYSTEM_ADMIN')
def revoke_system_admin():
    """Revoke system admin status"""
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Invalid request payload'
            }), 400
        
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'User ID is required'
            }), 400
        
        # Verify user exists and has role 'SYSTEM_ADMIN'
        user = User.get_user_by_id(user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        if user['role'] != 'SYSTEM_ADMIN':
            return jsonify({
                'success': False,
                'message': 'User is not a system admin'
            }), 400
        
        # Prevent revoking the current logged-in admin
        current_user_id = session.get('user_id')
        if user_id == current_user_id:
            return jsonify({
                'success': False,
                'message': 'You cannot revoke your own system admin privileges.'
            }), 400
        
        # Count current system admins
        current_count = User.count_users_by_role('SYSTEM_ADMIN')
        if current_count <= 2:
            return jsonify({
                'success': False,
                'message': f'Cannot revoke: System must have 2-4 system administrators. Current count: {current_count}'
            }), 400
        
        # Update user role to BASIC
        try:
            User.update_user_role(user_id, 'BASIC')
            return jsonify({
                'success': True,
                'message': 'System admin revoked successfully'
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'An error occurred during revocation'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred during revocation'
        }), 500

@admin_bp.route('/admin/clubs', methods=['GET'])
@require_login
@require_role('SYSTEM_ADMIN')
def get_clubs():
    """Get all clubs with admin status"""
    try:
        clubs = Club.get_clubs_with_admin_status()
        return jsonify({
            'success': True,
            'data': clubs
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching clubs'
        }), 500

@admin_bp.route('/admin/clubs/<int:club_id>/admins', methods=['GET'])
@require_login
@require_role('SYSTEM_ADMIN')
def get_club_admins(club_id):
    """Get club admin for a given club"""
    try:
        admin = Club.get_club_admin(club_id)
        if admin:
            return jsonify({
                'success': True,
                'data': admin
            }), 200
        else:
            return jsonify({
                'success': True,
                'data': None,
                'message': 'This club has no admin'
            }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching club admin'
        }), 500

@admin_bp.route('/admin/users/basic', methods=['GET'])
@require_login
@require_role('SYSTEM_ADMIN')
def get_basic_users():
    """Get all basic users"""
    try:
        users = User.get_users_by_role('BASIC')
        return jsonify({
            'success': True,
            'data': users
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching users'
        }), 500

@admin_bp.route('/admin/clubs/create', methods=['POST'])
@require_login
@require_role('SYSTEM_ADMIN')
def create_club():
    """Create a new club with optional admin assignment and initial budget"""
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Invalid request payload'
            }), 400
        
        name = data.get('name', '').strip()
        foundation_date = data.get('foundation_date', '').strip()
        club_type = data.get('club_type', '').strip()
        admin_user_id = data.get('admin_user_id')
        initial_budget = data.get('initial_budget', 0)
        
        # Validate required fields
        if not name:
            return jsonify({
                'success': False,
                'message': 'Club name is required'
            }), 400
        
        if not foundation_date:
            return jsonify({
                'success': False,
                'message': 'Foundation date is required'
            }), 400
        
        # Validate date format
        try:
            datetime.strptime(foundation_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Invalid date format. Please use YYYY-MM-DD format'
            }), 400
        
        if club_type not in ['STANDARD', 'OFFICIAL']:
            return jsonify({
                'success': False,
                'message': 'Club type must be STANDARD or OFFICIAL'
            }), 400
        
        if not admin_user_id:
            return jsonify({
                'success': False,
                'message': 'Club admin is required'
            }), 400
        
        try:
            admin_user_id = int(admin_user_id)
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'message': 'Invalid admin user ID'
            }), 400
        
        # Verify user exists and has BASIC role
        user = User.get_user_by_id(admin_user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        if user['role'] != 'BASIC':
            return jsonify({
                'success': False,
                'message': 'User must have BASIC role to be assigned as club admin'
            }), 400
        
        # Validate initial budget
        try:
            initial_budget = float(initial_budget) if initial_budget else 0.0
            if initial_budget < 0:
                return jsonify({
                    'success': False,
                    'message': 'Initial budget must be non-negative'
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'message': 'Invalid initial budget value'
            }), 400
        
        # Create club
        try:
            club = Club.create_club(name, foundation_date, club_type, admin_user_id, initial_budget)
            return jsonify({
                'success': True,
                'message': 'Club created successfully',
                'data': club
            }), 200
        except Exception as e:
            # Check for duplicate name error
            if 'Duplicate entry' in str(e) or 'UNIQUE constraint' in str(e):
                return jsonify({
                    'success': False,
                    'message': 'A club with this name already exists'
                }), 400
            return jsonify({
                'success': False,
                'message': 'An error occurred during club creation'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred during club creation'
        }), 500

@admin_bp.route('/admin/budget/summary', methods=['GET'])
@require_login
@require_role('SYSTEM_ADMIN')
def get_budget_summary():
    """Get budget summary for all clubs"""
    try:
        summary = Club.get_budget_summary()
        return jsonify({
            'success': True,
            'data': summary
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching budget summary'
        }), 500

@admin_bp.route('/admin/budget/allocate', methods=['POST'])
@require_login
@require_role('SYSTEM_ADMIN')
def allocate_budget():
    """Allocate budget to a club"""
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Invalid request payload'
            }), 400
        
        club_id = data.get('club_id')
        amount = data.get('amount')
        description = data.get('description', '').strip()
        
        if not club_id:
            return jsonify({
                'success': False,
                'message': 'Club ID is required'
            }), 400
        
        try:
            club_id = int(club_id)
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'message': 'Invalid club ID'
            }), 400
        
        if not amount:
            return jsonify({
                'success': False,
                'message': 'Amount is required'
            }), 400
        
        try:
            amount = float(amount)
            if amount <= 0:
                return jsonify({
                    'success': False,
                    'message': 'Amount must be greater than 0'
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'message': 'Invalid amount value'
            }), 400
        
        # Verify club exists
        club = Club.get_club_by_id(club_id)
        if not club:
            return jsonify({
                'success': False,
                'message': 'Club not found'
            }), 404
        
        # Allocate budget
        try:
            Club.allocate_budget(club_id, amount, description or None)
            return jsonify({
                'success': True,
                'message': 'Budget allocated successfully'
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'An error occurred during budget allocation'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred during budget allocation'
        }), 500

@admin_bp.route('/admin/events/upcoming', methods=['GET'])
@require_login
@require_role('SYSTEM_ADMIN')
def get_upcoming_events():
    """Get paginated upcoming events (10 per page)"""
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
        
        result = Event.get_upcoming_events_paginated(page=page, per_page=10)
        return jsonify({
            'success': True,
            'data': result
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching events'
        }), 500

@admin_bp.route('/admin/events/<int:event_id>', methods=['GET'])
@require_login
@require_role('SYSTEM_ADMIN')
def get_event(event_id):
    """Get full event details for editing"""
    try:
        event = Event.get_event_by_id(event_id)
        if not event:
            return jsonify({
                'success': False,
                'message': 'Event not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': event
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching event'
        }), 500

@admin_bp.route('/admin/venues', methods=['GET'])
@require_login
@require_role('SYSTEM_ADMIN')
def get_venues():
    """Get all venues for dropdown"""
    try:
        venues = Event.get_all_venues()
        return jsonify({
            'success': True,
            'data': venues
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching venues'
        }), 500

@admin_bp.route('/admin/clubs/all', methods=['GET'])
@require_login
@require_role('SYSTEM_ADMIN')
def get_all_clubs():
    """Get all clubs for dropdown"""
    try:
        clubs = Club.get_all_clubs()
        return jsonify({
            'success': True,
            'data': clubs
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching clubs'
        }), 500

@admin_bp.route('/admin/events/<int:event_id>', methods=['PUT'])
@require_login
@require_role('SYSTEM_ADMIN')
def update_event(event_id):
    """Update event (validate that event_id and publish_date are not changed)"""
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Invalid request payload'
            }), 400
        
        # Verify event exists and is not deleted
        event = Event.get_event_by_id(event_id)
        if not event:
            return jsonify({
                'success': False,
                'message': 'Event not found'
            }), 404
        
        # Validate that event_id and publish_date are not being changed
        if 'event_id' in data and int(data.get('event_id')) != event_id:
            return jsonify({
                'success': False,
                'message': 'Event ID cannot be changed'
            }), 400
        
        if 'publish_date' in data and data.get('publish_date') != str(event['publish_date']):
            return jsonify({
                'success': False,
                'message': 'Publish date cannot be changed'
            }), 400
        
        # Get update fields
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        end_date = data.get('end_date', '').strip()
        venue_id = data.get('venue_id')
        club_id = data.get('club_id')
        modification_description = data.get('modification_description', '').strip()
        
        # Validate required fields
        if not name:
            return jsonify({
                'success': False,
                'message': 'Event name is required'
            }), 400
        
        if not description:
            return jsonify({
                'success': False,
                'message': 'Event description is required'
            }), 400
        
        if not end_date:
            return jsonify({
                'success': False,
                'message': 'End date is required'
            }), 400
        
        # Validate date format
        try:
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Invalid date format. Please use YYYY-MM-DD format'
            }), 400
        
        if not venue_id:
            return jsonify({
                'success': False,
                'message': 'Venue is required'
            }), 400
        
        try:
            venue_id = int(venue_id)
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'message': 'Invalid venue ID'
            }), 400
        
        if not club_id:
            return jsonify({
                'success': False,
                'message': 'Club is required'
            }), 400
        
        try:
            club_id = int(club_id)
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'message': 'Invalid club ID'
            }), 400
        
        # Verify venue exists
        venues = Event.get_all_venues()
        if not any(v['venue_id'] == venue_id for v in venues):
            return jsonify({
                'success': False,
                'message': 'Venue not found'
            }), 404
        
        # Verify club exists
        club = Club.get_club_by_id(club_id)
        if not club:
            return jsonify({
                'success': False,
                'message': 'Club not found'
            }), 404
        
        # Update event
        try:
            success = Event.update_event(event_id, name, description, end_date, venue_id, club_id)
            if not success:
                return jsonify({
                    'success': False,
                    'message': 'Failed to update event'
                }), 500
            
            # Record modification
            user_id = session.get('user_id')
            if user_id:
                Event.record_modification(
                    event_id,
                    'UPDATE',
                    modification_description if modification_description else None,
                    user_id
                )
            
            return jsonify({
                'success': True,
                'message': 'Event updated successfully'
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'An error occurred during event update'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred during event update'
        }), 500

@admin_bp.route('/admin/events/<int:event_id>', methods=['DELETE'])
@require_login
@require_role('SYSTEM_ADMIN')
def delete_event(event_id):
    """Soft delete event and record in EVENT-MODIFICATION"""
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        modification_description = data.get('description', '').strip() if data else ''
        
        # Verify event exists and is not already deleted
        event = Event.get_event_by_id(event_id)
        if not event:
            return jsonify({
                'success': False,
                'message': 'Event not found'
            }), 404
        
        # Soft delete event
        try:
            success = Event.delete_event(event_id)
            if not success:
                return jsonify({
                    'success': False,
                    'message': 'Failed to delete event'
                }), 500
            
            # Record modification
            user_id = session.get('user_id')
            if user_id:
                Event.record_modification(
                    event_id,
                    'DELETE',
                    modification_description if modification_description else None,
                    user_id
                )
            
            return jsonify({
                'success': True,
                'message': 'Event deleted successfully'
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'An error occurred during event deletion'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred during event deletion'
        }), 500

@admin_bp.route('/admin/events/finished', methods=['GET'])
@require_login
@require_role('SYSTEM_ADMIN')
def get_finished_events():
    """Get paginated finished events (10 per page)"""
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
        
        result = Event.get_finished_events_paginated(page=page, per_page=10)
        return jsonify({
            'success': True,
            'data': result
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching finished events'
        }), 500

@admin_bp.route('/admin/events/modifications', methods=['GET'])
@require_login
@require_role('SYSTEM_ADMIN')
def get_event_modifications():
    """Get paginated event modifications (10 per page)"""
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
        
        result = Event.get_event_modifications_paginated(page=page, per_page=10)
        return jsonify({
            'success': True,
            'data': result
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching event modifications'
        }), 500