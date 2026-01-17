from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from app.models.user_model import User

auth_bp = Blueprint('auth', __name__)

def get_current_user():
    """Retrieve current logged-in user from session"""
    if 'user_id' in session:
        return {
            'user_id': session.get('user_id'),
            'email': session.get('email'),
            'name': session.get('name'),
            'role': session.get('role')
        }
    return None

def require_login(f):
    """Decorator to protect routes that require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return decorated_function

def require_role(role):
    """Decorator to protect routes that require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('auth.login_page'))
            if session.get('role') != role:
                return jsonify({'success': False, 'message': 'Unauthorized access'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route('/login', methods=['GET'])
def login_page():
    """Render the login/signup page"""
    return render_template('auth.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    """Handle login submission"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email and password are required',
                'field': 'Email'
            }), 400

        # Authenticate user
        user = User.authenticate_user(email, password)
        
        if user:
            # Store user info in session
            session['user_id'] = user['user_id']
            session['email'] = user['email']
            session['name'] = user['name']
            session['role'] = user['role']
            
            # Determine redirect URL based on role
            if user['role'] == 'BASIC':
                redirect_url = '/user'
            elif user['role'] == 'CLUB_ADMIN':
                redirect_url = '/clubmgr'
            elif user['role'] == 'SYSTEM_ADMIN':
                redirect_url = '/admin'
            else:
                redirect_url = '/user'
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'redirect': redirect_url,
                'user': user
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password',
                'field': 'Email'
            }), 401

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred during login',
            'field': None
        }), 500

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """Handle sign-up submission"""
    try:
        data = request.get_json()
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
            from datetime import datetime
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
            
            # Auto-login: store in session
            session['user_id'] = user['user_id']
            session['email'] = user['email']
            session['name'] = user['name']
            session['role'] = user['role']
            
            # Redirect to user dashboard (BASIC role)
            return jsonify({
                'success': True,
                'message': 'Registration successful',
                'redirect': '/user',
                'user': user
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'An error occurred during registration. Please try again.',
                'field': None
            }), 500

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred during registration',
            'field': None
        }), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Handle logout"""
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Logged out successfully',
        'redirect': '/login'
    }), 200
