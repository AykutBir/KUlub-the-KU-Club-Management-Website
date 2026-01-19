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

    @staticmethod
    def get_users_by_role(role):
        """Get users filtered by role"""
        cursor = get_cursor()
        try:
            cursor.execute(
                "SELECT user_id, name, email, role FROM users WHERE role = %s ORDER BY name",
                (role,)
            )
            rows = cursor.fetchall()
            return [
                {
                    'user_id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'role': row[3]
                }
                for row in rows
            ]
        except Exception as e:
            raise e
        finally:
            cursor.close()

    @staticmethod
    def count_users_by_role(role):
        """Count users by role"""
        cursor = get_cursor()
        try:
            cursor.execute(
                "SELECT COUNT(*) FROM users WHERE role = %s",
                (role,)
            )
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            raise e
        finally:
            cursor.close()

    @staticmethod
    def update_user_role(user_id, new_role):
        """Update user role"""
        db = get_db()
        cursor = get_cursor()
        try:
            cursor.execute(
                "UPDATE users SET role = %s WHERE user_id = %s",
                (new_role, user_id)
            )
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def search_users(role=None, name=None, club_name=None, page=1, per_page=5):
        """Search users with pagination. Returns users matching all provided criteria (AND logic)"""
        cursor = get_cursor()
        try:
            # Build WHERE clause conditions
            where_conditions = ["1=1"]
            params = []
            
            # Add filters
            if role:
                where_conditions.append("u.role = %s")
                params.append(role)
            
            if name:
                where_conditions.append("u.name LIKE %s")
                params.append(f"%{name}%")
            
            if club_name:
                where_conditions.append("(c_managed.name LIKE %s OR c_member.name LIKE %s)")
                params.append(f"%{club_name}%")
                params.append(f"%{club_name}%")
            
            where_clause = " AND ".join(where_conditions)
            
            # Build count query (separate from main query to avoid subquery issues)
            count_query = f"""
                SELECT COUNT(DISTINCT u.user_id)
                FROM users u
                LEFT JOIN clubs c_managed ON c_managed.admin_user_id = u.user_id
                LEFT JOIN club_members cm ON cm.user_id = u.user_id
                LEFT JOIN clubs c_member ON c_member.club_id = cm.club_id
                WHERE {where_clause}
            """
            cursor.execute(count_query, params)
            total_users = cursor.fetchone()[0]
            
            # Build main query with pagination
            base_query = f"""
                SELECT DISTINCT u.user_id, u.name, u.email, u.role,
                       COALESCE(c_managed.name, c_member.name, NULL) as club_name
                FROM users u
                LEFT JOIN clubs c_managed ON c_managed.admin_user_id = u.user_id
                LEFT JOIN club_members cm ON cm.user_id = u.user_id
                LEFT JOIN clubs c_member ON c_member.club_id = cm.club_id
                WHERE {where_clause}
                ORDER BY u.name
                LIMIT %s OFFSET %s
            """
            offset = (page - 1) * per_page
            params_with_pagination = params + [per_page, offset]
            
            cursor.execute(base_query, params_with_pagination)
            rows = cursor.fetchall()
            
            users = [
                {
                    'user_id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'role': row[3],
                    'club_name': row[4] if row[4] else None
                }
                for row in rows
            ]
            
            total_pages = (total_users + per_page - 1) // per_page if total_users > 0 else 0
            
            return {
                'users': users,
                'total_users': total_users,
                'total_pages': total_pages,
                'current_page': page
            }
        except Exception as e:
            raise e
        finally:
            cursor.close()