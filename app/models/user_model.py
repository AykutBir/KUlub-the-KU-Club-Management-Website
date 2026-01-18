import bcrypt
from app.db import get_db, get_cursor

class User:
    @staticmethod
    def create_user(first_name, last_name, email, birthdate, password):
        """Create a new user with hashed password"""
        db = get_db()
        cursor = get_cursor()
        
        try:
            # Concatenate first and last name
            full_name = first_name + " " + last_name
            
            # Hash password using bcrypt
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            password_hash_str = password_hash.decode('utf-8')
            
            # Insert user into users table
            insert_user_query = "INSERT INTO users (name, email, birthdate, role) VALUES ('" + full_name.replace("'", "''") + "', '" + email.replace("'", "''") + "', '" + birthdate.replace("'", "''") + "', 'BASIC')"
            cursor.execute(insert_user_query)
            
            # Insert password hash into user_credentials table
            insert_cred_query = "INSERT INTO user_credentials (email, password_hash) VALUES ('" + email.replace("'", "''") + "', '" + password_hash_str.replace("'", "''") + "')"
            cursor.execute(insert_cred_query)
            
            # Commit transaction
            db.commit()
            
            # Get the created user
            user_id = cursor.lastrowid
            return {
                'user_id': user_id,
                'name': full_name,
                'email': email,
                'role': 'BASIC'
            }
        except Exception as e:
            # Rollback on error
            db.rollback()
            raise e
        finally:
            cursor.close()
    
    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user by email and password"""
        cursor = get_cursor()
        
        try:
            # Join users and user_credentials tables
            query = "SELECT u.user_id, u.name, u.email, u.role, uc.password_hash FROM users u JOIN user_credentials uc ON u.email = uc.email WHERE u.email = '" + email.replace("'", "''") + "'"
            cursor.execute(query)
            result = cursor.fetchone()
            
            if result:
                user_id, name, user_email, role, stored_hash = result
                
                # Verify password
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                    return {
                        'user_id': user_id,
                        'name': name,
                        'email': user_email,
                        'role': role
                    }
            
            return None
        except Exception as e:
            raise e
        finally:
            cursor.close()
    
    @staticmethod
    def get_user_by_email(email):
        """Retrieve user by email"""
        cursor = get_cursor()
        
        try:
            query = "SELECT user_id, name, email, role FROM users WHERE email = '" + email.replace("'", "''") + "'"
            cursor.execute(query)
            result = cursor.fetchone()
            
            if result:
                user_id, name, user_email, role = result
                return {
                    'user_id': user_id,
                    'name': name,
                    'email': user_email,
                    'role': role
                }
            
            return None
        except Exception as e:
            raise e
        finally:
            cursor.close()
    
    @staticmethod
    def get_user_by_id(user_id):
        """Retrieve user by ID"""
        cursor = get_cursor()
        
        try:
            query = "SELECT user_id, name, email, role FROM users WHERE user_id = " + str(user_id)
            cursor.execute(query)
            result = cursor.fetchone()
            
            if result:
                uid, name, email, role = result
                return {
                    'user_id': uid,
                    'name': name,
                    'email': email,
                    'role': role
                }
            
            return None
        except Exception as e:
            raise e
        finally:
            cursor.close()

    @staticmethod
    def get_user_profile(user_id):
        """Retrieve user profile fields for dashboard."""
        cursor = get_cursor()

        try:
            # Fetch the profile fields used in the dashboard's profile section
            cursor.execute(
                "SELECT user_id, name, email, birthdate, role FROM users WHERE user_id = %s",
                (user_id,),
            )
            result = cursor.fetchone()

            if result:
                uid, name, email, birthdate, role = result
                return {
                    'user_id': uid,
                    'name': name,
                    'email': email,
                    'birthdate': birthdate,
                    'role': role
                }

            return None
        except Exception as e:
            raise e
        finally:
            cursor.close()
