from app.db import get_db, get_cursor
from datetime import date


class Club:
    @staticmethod
    def get_all_clubs():
        """Fetch all clubs for discovery."""
        cursor = get_cursor()
        try:
            # Pull the core fields needed for the club cards
            cursor.execute(
                """
                SELECT club_id, name, club_type, foundation_date
                FROM clubs
                ORDER BY name
                """
            )
            rows = cursor.fetchall()
            return [
                {
                    "club_id": row[0],
                    "name": row[1],
                    "club_type": row[2],
                    "foundation_date": row[3],
                }
                for row in rows
            ]
        finally:
            cursor.close()

    @staticmethod
    def get_user_club(user_id):
        """Return the user's current club membership, if any."""
        cursor = get_cursor()
        try:
            # Join memberships to clubs to get the user's club details
            cursor.execute(
                """
                SELECT c.club_id, c.name, c.club_type, c.foundation_date
                FROM club_members cm
                JOIN clubs c ON c.club_id = cm.club_id
                WHERE cm.user_id = %s
                LIMIT 1
                """,
                (user_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            return {
                "club_id": row[0],
                "name": row[1],
                "club_type": row[2],
                "foundation_date": row[3],
            }
        finally:
            cursor.close()

    @staticmethod
    def get_membership_requests_for_user(user_id):
        """Fetch membership requests for the user."""
        cursor = get_cursor()
        try:
            # Include club names so the dashboard can show request status
            cursor.execute(
                """
                SELECT mr.club_id, mr.status, mr.requested_at, c.name
                FROM membership_requests mr
                JOIN clubs c ON c.club_id = mr.club_id
                WHERE mr.user_id = %s
                ORDER BY mr.requested_at DESC
                """,
                (user_id,),
            )
            rows = cursor.fetchall()
            return [
                {
                    "club_id": row[0],
                    "status": row[1],
                    "requested_at": row[2],
                    "club_name": row[3],
                }
                for row in rows
            ]
        finally:
            cursor.close()

    @staticmethod
    def get_pending_request_for_user(user_id):
        """Check if the user already has a pending membership request."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT request_id, club_id
                FROM membership_requests
                WHERE user_id = %s AND status = 'PENDING'
                LIMIT 1
                """,
                (user_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            return {"request_id": row[0], "club_id": row[1]}
        finally:
            cursor.close()

    @staticmethod
    def create_membership_request(user_id, club_id):
        """Create a membership request if the user is eligible."""
        db = get_db()
        cursor = get_cursor()
        try:
            # Block if user already belongs to a club
            cursor.execute(
                "SELECT 1 FROM club_members WHERE user_id = %s LIMIT 1",
                (user_id,),
            )
            if cursor.fetchone():
                return False, "You are already a member of a club."

            # Block if user already has a pending request
            cursor.execute(
                """
                SELECT 1 FROM membership_requests
                WHERE user_id = %s AND status = 'PENDING'
                LIMIT 1
                """,
                (user_id,),
            )
            if cursor.fetchone():
                return False, "You already have a pending membership request."

            # Block requests for OFFICIAL clubs
            cursor.execute(
                "SELECT club_type FROM clubs WHERE club_id = %s",
                (club_id,),
            )
            club = cursor.fetchone()
            if not club:
                return False, "Club not found."
            if club[0] == 'OFFICIAL':
                return False, "Official clubs do not accept membership requests."

            cursor.execute(
                """
                INSERT INTO membership_requests (user_id, club_id)
                VALUES (%s, %s)
                """,
                (user_id, club_id),
            )
            db.commit()
            return True, "Membership request sent."
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            cursor.close()

    @staticmethod
    def leave_club(user_id):
        """Allow a user to leave their club membership."""
        db = get_db()
        cursor = get_cursor()
        try:
            # Check if user is a member of a club and get the club_id
            cursor.execute(
                "SELECT club_id FROM club_members WHERE user_id = %s LIMIT 1",
                (user_id,),
            )
            membership = cursor.fetchone()
            if not membership:
                return False, "You are not a member of any club."

            club_id = membership[0]

            # Delete the membership record
            cursor.execute(
                "DELETE FROM club_members WHERE user_id = %s",
                (user_id,),
            )
            if cursor.rowcount == 0:
                return False, "Unable to leave club."

            # Update the membership request status to REJECTED
            cursor.execute(
                """
                UPDATE membership_requests
                SET status = 'REJECTED'
                WHERE user_id = %s AND club_id = %s AND status = 'APPROVED'
                """,
                (user_id, club_id),
            )
            
            db.commit()
            return True, "You have successfully left the club."
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            cursor.close()

    @staticmethod
    def follow_club(user_id, club_id):
        """Follow a club."""
        db = get_db()
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                INSERT INTO club_followers (user_id, club_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE followed_at = followed_at
                """,
                (user_id, club_id),
            )
            db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def unfollow_club(user_id, club_id):
        """Unfollow a club."""
        db = get_db()
        cursor = get_cursor()
        try:
            cursor.execute(
                "DELETE FROM club_followers WHERE user_id = %s AND club_id = %s",
                (user_id, club_id),
            )
            db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def is_following(user_id, club_id):
        """Check if the user is following a club."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT 1
                FROM club_followers
                WHERE user_id = %s AND club_id = %s
                LIMIT 1
                """,
                (user_id, club_id),
            )
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    @staticmethod
    def get_followed_clubs(user_id):
        """Get clubs followed by the user."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT c.club_id, c.name, c.club_type, c.foundation_date, cf.followed_at
                FROM club_followers cf
                JOIN clubs c ON c.club_id = cf.club_id
                WHERE cf.user_id = %s
                ORDER BY cf.followed_at DESC
                """,
                (user_id,),
            )
            rows = cursor.fetchall()
            return [
                {
                    "club_id": row[0],
                    "name": row[1],
                    "club_type": row[2],
                    "foundation_date": row[3],
                    "followed_at": row[4],
                }
                for row in rows
            ]
        finally:
            cursor.close()

    @staticmethod
    def get_club_admin(club_id):
        """Get admin user for a club"""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT u.user_id, u.name, u.email, u.role
                FROM clubs c
                JOIN users u ON u.user_id = c.admin_user_id
                WHERE c.club_id = %s AND c.admin_user_id IS NOT NULL
                """,
                (club_id,)
            )
            result = cursor.fetchone()
            if result:
                return {
                    'user_id': result[0],
                    'name': result[1],
                    'email': result[2],
                    'role': result[3]
                }
            return None
        except Exception as e:
            raise e
        finally:
            cursor.close()

    @staticmethod
    def set_club_admin(club_id, user_id):
        """Assign admin to club"""
        db = get_db()
        cursor = get_cursor()
        try:
            cursor.execute(
                "UPDATE clubs SET admin_user_id = %s WHERE club_id = %s",
                (user_id, club_id)
            )
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def remove_club_admin(club_id):
        """Remove admin from club"""
        db = get_db()
        cursor = get_cursor()
        try:
            cursor.execute(
                "UPDATE clubs SET admin_user_id = NULL WHERE club_id = %s",
                (club_id,)
            )
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def get_clubs_with_admin_status():
        """Get all clubs with admin status"""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT c.club_id, c.name, c.admin_user_id, 
                       CASE WHEN c.admin_user_id IS NOT NULL THEN u.name ELSE NULL END as admin_name
                FROM clubs c
                LEFT JOIN users u ON u.user_id = c.admin_user_id
                ORDER BY c.name
                """
            )
            rows = cursor.fetchall()
            return [
                {
                    'club_id': row[0],
                    'name': row[1],
                    'admin_user_id': row[2],
                    'admin_name': row[3]
                }
                for row in rows
            ]
        except Exception as e:
            raise e
        finally:
            cursor.close()

    @staticmethod
    def get_club_by_id(club_id):
        """Get club by ID"""
        cursor = get_cursor()
        try:
            cursor.execute(
                "SELECT club_id, name, club_type, admin_user_id FROM clubs WHERE club_id = %s",
                (club_id,)
            )
            result = cursor.fetchone()
            if result:
                return {
                    'club_id': result[0],
                    'name': result[1],
                    'club_type': result[2],
                    'admin_user_id': result[3]
                }
            return None
        except Exception as e:
            raise e
        finally:
            cursor.close()

    @staticmethod
    def create_club(name, foundation_date, club_type, admin_user_id=None, initial_budget=0):
        """Create a new club with optional admin assignment and initial budget"""
        db = get_db()
        cursor = get_cursor()
        try:
            # Insert new club
            cursor.execute(
                """
                INSERT INTO clubs (name, foundation_date, club_type, budget, admin_user_id)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (name, foundation_date, club_type, initial_budget, admin_user_id)
            )
            club_id = cursor.lastrowid
            
            # If admin_user_id provided, assign admin and update user role
            if admin_user_id:
                cursor.execute(
                    "UPDATE clubs SET admin_user_id = %s WHERE club_id = %s",
                    (admin_user_id, club_id)
                )
                cursor.execute(
                    "UPDATE users SET role = 'CLUB_ADMIN' WHERE user_id = %s",
                    (admin_user_id,)
                )
            
            # If initial_budget > 0, create initial INCOME transaction
            if initial_budget > 0:
                cursor.execute(
                    """
                    INSERT INTO budget_transactions (club_id, amount, transaction_date, transaction_type, description)
                    VALUES (%s, %s, %s, 'INCOME', %s)
                    """,
                    (club_id, initial_budget, date.today(), f'Initial budget allocation for {name}')
                )
            
            db.commit()
            
            return {
                'club_id': club_id,
                'name': name,
                'foundation_date': foundation_date,
                'club_type': club_type,
                'budget': initial_budget,
                'admin_user_id': admin_user_id
            }
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def get_budget_summary():
        """Get budget summary for all clubs with aggregated transaction data"""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT 
                    c.club_id,
                    c.name,
                    c.budget as current_budget,
                    COALESCE(SUM(CASE WHEN bt.transaction_type = 'EXPENSE' THEN bt.amount ELSE 0 END), 0) as total_spent,
                    COALESCE(SUM(CASE WHEN bt.transaction_type = 'INCOME' THEN bt.amount ELSE 0 END), 0) as total_earned
                FROM clubs c
                LEFT JOIN budget_transactions bt ON bt.club_id = c.club_id
                GROUP BY c.club_id, c.name, c.budget
                ORDER BY c.name
                """
            )
            rows = cursor.fetchall()
            return [
                {
                    'club_id': row[0],
                    'name': row[1],
                    'current_budget': float(row[2]) if row[2] else 0.0,
                    'total_spent': float(row[3]) if row[3] else 0.0,
                    'total_earned': float(row[4]) if row[4] else 0.0
                }
                for row in rows
            ]
        except Exception as e:
            raise e
        finally:
            cursor.close()

    @staticmethod
    def allocate_budget(club_id, amount, description=None):
        """Allocate budget to a club by creating INCOME transaction and updating club budget"""
        db = get_db()
        cursor = get_cursor()
        try:
            # Insert INCOME transaction
            cursor.execute(
                """
                INSERT INTO budget_transactions (club_id, amount, transaction_date, transaction_type, description)
                VALUES (%s, %s, %s, 'INCOME', %s)
                """,
                (club_id, amount, date.today(), description or 'Budget allocation')
            )
            
            # Update club budget
            cursor.execute(
                "UPDATE clubs SET budget = budget + %s WHERE club_id = %s",
                (amount, club_id)
            )
            
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
