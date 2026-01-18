from app.db import get_cursor


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
