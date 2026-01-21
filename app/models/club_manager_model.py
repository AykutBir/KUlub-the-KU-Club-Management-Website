from app.db import get_cursor, get_db


class ClubManager:
    """Model for club manager operations - all database queries for club administration."""

    
    # CLUB INFO & DASHBOARD
    
    #getting club info where user is also administrator.
    @staticmethod
    def get_admin_club(user_id):
        """Get the club managed by this admin user."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT club_id, name, foundation_date, budget, club_type, description
                FROM clubs
                WHERE admin_user_id = %s
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
                "foundation_date": row[2],
                "budget": float(row[3]) if row[3] else 0.0,
                "club_type": row[4],
                "description": row[5],
            }
        finally:
            cursor.close()
   # coubnt how many people joined this club 
    @staticmethod
    def get_member_count(club_id):
        """Get total member count for the club."""
        cursor = get_cursor()
        try:
            cursor.execute(
                "SELECT COUNT(*) FROM club_members WHERE club_id = %s",
                (club_id,),
            )
            row = cursor.fetchone()
            return row[0] if row else 0
        finally:
            cursor.close()
    #counting events that not ended yet
    @staticmethod
    def get_upcoming_events_count(club_id):
        """Get count of upcoming events (end_date >= today)."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT COUNT(*) FROM events
                WHERE club_id = %s AND end_date >= CURDATE()
                """,
                (club_id,),
            )
            row = cursor.fetchone()
            return row[0] if row else 0
        finally:
            cursor.close()
    #summing up all event attendance in past month
    @staticmethod
    def get_total_attendance_last_30_days(club_id):
        """Get total attendance in last 30 days."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT COUNT(i.user_id)
                FROM interacts_with i
                JOIN events e ON i.event_id = e.event_id
                WHERE e.club_id = %s
                  AND i.interaction_type = 'attended'
                  AND i.interaction_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                """,
                (club_id,),
            )
            row = cursor.fetchone()
            return row[0] if row else 0
        finally:
            cursor.close()
    # finding the event with highest attendance
    @staticmethod
    def get_most_popular_event(club_id):
        """Get the most popular event by attendance."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT e.name, COUNT(i.user_id) as attendance
                FROM events e
                LEFT JOIN interacts_with i ON e.event_id = i.event_id
                    AND i.interaction_type = 'attended'
                WHERE e.club_id = %s
                GROUP BY e.event_id, e.name
                ORDER BY attendance DESC
                LIMIT 1
                """,
                (club_id,),
            )
            row = cursor.fetchone()
            if not row:
                return {"name": "No events yet", "attendance": 0}
            return {"name": row[0], "attendance": row[1]}
        finally:
            cursor.close()

    # =============================================
    # MEMBERSHIP MANAGEMENT
    # =============================================
    # Getting all pending membership requests for the club.
    @staticmethod
    def get_pending_requests(club_id):
        """Get all pending membership requests for the club."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT mr.request_id, mr.user_id, u.name, u.email, mr.requested_at
                FROM membership_requests mr
                JOIN users u ON mr.user_id = u.user_id
                WHERE mr.club_id = %s AND mr.status = 'PENDING'
                ORDER BY mr.requested_at DESC
                """,
                (club_id,),
            )
            rows = cursor.fetchall()
            return [
                {
                    "request_id": row[0],
                    "user_id": row[1],
                    "name": row[2],
                    "email": row[3],
                    "requested_at": row[4],
                }
                for row in rows
            ]
        finally:
            cursor.close()
    # rejectinh a pending membership request
    @staticmethod
    def get_current_members(club_id):
        """Get all current members of the club."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT cm.user_id, u.name, u.email, cm.joined_at, cm.membership_title
                FROM club_members cm
                JOIN users u ON cm.user_id = u.user_id
                WHERE cm.club_id = %s
                ORDER BY cm.joined_at DESC
                """,
                (club_id,),
            )
            rows = cursor.fetchall()
            return [
                {
                    "user_id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "joined_at": row[3],
                    "membership_title": row[4] or "Member",
                }
                for row in rows
            ]
        finally:
            cursor.close()
# approving a pending membership request
    @staticmethod
    def approve_request(request_id, club_id):
        """Approve a membership request - add user to members and update request status."""
        cursor = get_cursor()
        db = get_db()
        try:
            # got request details
            cursor.execute(
                "SELECT user_id FROM membership_requests WHERE request_id = %s AND club_id = %s AND status = 'PENDING'",
                (request_id, club_id),
            )
            row = cursor.fetchone()
            if not row:
                return False, "Request not found or already processed"

            user_id = row[0]

            # ensure club exists and user is eligble to join
            cursor.execute(
                "SELECT club_type FROM clubs WHERE club_id = %s",
                (club_id,),
            )
            club_row = cursor.fetchone()
            if not club_row:
                return False, "Club not found"
            
            # Check whether if club is offical (replaces trigger trg_block_approve_if_member_or_official)
            if club_row[0] == 'OFFICIAL':
                return False, "Official clubs cannot approve membership requests."

            cursor.execute(
                "SELECT role FROM users WHERE user_id = %s",
                (user_id,),
            )
            role_row = cursor.fetchone()
            if not role_row:
                return False, "User not found"
            if role_row[0] != 'BASIC':
                return False, "Only basic users can become club members"

            # check if user is already a member of any club 
            cursor.execute(
                "SELECT club_id FROM club_members WHERE user_id = %s",
                (user_id,),
            )
            if cursor.fetchone():
                return False, "User is already a member of a club"

            # updating request status first before inserting into club_members
            cursor.execute(
                "UPDATE membership_requests SET status = 'APPROVED' WHERE request_id = %s",
                (request_id,),
            )

            # insert into club_members after updating request status
            cursor.execute(
                """
                INSERT INTO club_members (user_id, club_id, joined_at, membership_title)
                VALUES (%s, %s, NOW(), 'Member')
                """,
                (user_id, club_id),
            )

            db.commit()
            return True, "Request approved successfully"
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            cursor.close()
    #decline a pending membership request
    @staticmethod
    def decline_request(request_id, club_id):
        """Decline a membership request."""
        cursor = get_cursor()
        db = get_db()
        try:
            cursor.execute(
                """
                UPDATE membership_requests
                SET status = 'REJECTED'
                WHERE request_id = %s AND club_id = %s AND status = 'PENDING'
                """,
                (request_id, club_id),
            )
            if cursor.rowcount == 0:
                return False, "Request not found or already processed"
            db.commit()
            return True, "Request declined"
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            cursor.close()
    #remove sb from club's member list
    @staticmethod
    def kick_member(user_id, club_id):
        """Remove a member from the club."""
        cursor = get_cursor()
        db = get_db()
        try:
            cursor.execute(
                "DELETE FROM club_members WHERE user_id = %s AND club_id = %s",
                (user_id, club_id),
            )
            if cursor.rowcount == 0:
                return False, "Member not found"
            db.commit()
            return True, "Member removed successfully"
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            cursor.close()
    #changing a member's title
    @staticmethod
    def update_member_title(user_id, club_id, new_title):
        """Update a member's title."""
        cursor = get_cursor()
        db = get_db()
        try:
            cursor.execute(
                """
                UPDATE club_members
                SET membership_title = %s
                WHERE user_id = %s AND club_id = %s
                """,
                (new_title, user_id, club_id),
            )
            if cursor.rowcount == 0:
                return False, "Member not found"
            db.commit()
            return True, "Title updated successfully"
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            cursor.close()

    # EVENT MANAGEMENT
   
    #get locations where event can be held
    @staticmethod
    def get_venues():
        """Get all available venues."""
        cursor = get_cursor()
        try:
            cursor.execute("SELECT venue_id, name, capacity FROM venues ORDER BY name")
            rows = cursor.fetchall()
            return [
                {"venue_id": row[0], "name": row[1], "capacity": row[2]}
                for row in rows
            ]
        finally:
            cursor.close()
    #getting all events for the club
    @staticmethod
    def get_club_events(club_id):
        """Get all events for the club with attendance count."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT e.event_id, e.name, e.description, e.publish_date, e.end_date,
                       e.event_start_date, e.quota, e.category,
                       v.name as venue_name, v.capacity,
                       COUNT(CASE WHEN i.interaction_type = 'attended' THEN 1 END) as attendance_count
                FROM events e
                LEFT JOIN venues v ON e.venue_id = v.venue_id
                LEFT JOIN interacts_with i ON e.event_id = i.event_id
                WHERE e.club_id = %s
                GROUP BY e.event_id, e.name, e.description, e.publish_date, e.end_date,
                         e.event_start_date, e.quota, e.category, v.name, v.capacity
                ORDER BY e.event_start_date DESC
                """,
                (club_id,),
            )
            rows = cursor.fetchall()
            return [
                {
                    "event_id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "publish_date": row[3],
                    "end_date": row[4],
                    "event_start_date": row[5],
                    "quota": row[6],
                    "category": row[7],
                    "venue_name": row[8],
                    "venue_capacity": row[9],
                    "attendance_count": row[10],
                }
                for row in rows
            ]
        finally:
            cursor.close()
    #set a new event for the club
    @staticmethod
    def create_event(club_id, name, description, publish_date, end_date, venue_id, quota, event_start_date, category):
        """Create a new event for the club."""
        cursor = get_cursor()
        db = get_db()
        try:
            # validate quota against venue capacity
            cursor.execute("SELECT capacity FROM venues WHERE venue_id = %s", (venue_id,))
            venue = cursor.fetchone()
            if not venue:
                return False, "Venue not found"
            if quota > venue[0]:
                return False, f"Quota ({quota}) cannot exceed venue capacity ({venue[0]})"

            cursor.execute(
                """
                INSERT INTO events (club_id, name, description, publish_date, end_date, venue_id, quota, event_start_date, category)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (club_id, name, description, publish_date, end_date, venue_id, quota, event_start_date, category),
            )
            db.commit()
            return True, "Event created successfully"
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            cursor.close()
# removing an event from the club's event list
    @staticmethod
    def delete_event(event_id, club_id):
        """Delete an event (only if it belongs to the club)."""
        cursor = get_cursor()
        db = get_db()
        try:
            cursor.execute(
                "DELETE FROM events WHERE event_id = %s AND club_id = %s",
                (event_id, club_id),
            )
            if cursor.rowcount == 0:
                return False, "Event not found or not authorized"
            db.commit()
            return True, "Event deleted successfully"
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            cursor.close()

    # ANALYTICS - 7 ADVANCED QUERIES
    #break down of event performance with how many attended and saved
    @staticmethod
    def analytics_event_performance(club_id):
        """Query 1: Event Performance - GROUP BY + aggregate with CASE."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT e.event_id, e.name AS event_name,
                       COUNT(CASE WHEN i.interaction_type = 'attended' THEN 1 END) AS attended_count,
                       COUNT(CASE WHEN i.interaction_type = 'saved' THEN 1 END) AS saved_count
                FROM events e
                LEFT JOIN interacts_with i ON e.event_id = i.event_id
                WHERE e.club_id = %s
                GROUP BY e.event_id, e.name
                ORDER BY attended_count DESC
                """,
                (club_id,),
            )
            rows = cursor.fetchall()
            return [
                {
                    "event_id": row[0],
                    "event_name": row[1],
                    "attended_count": row[2],
                    "saved_count": row[3],
                }
                for row in rows
            ]
        finally:
            cursor.close()
    # find top 3 most attended events
    @staticmethod
    def analytics_top_3_events(club_id):
        """Query 2: Top 3 Most Attended Events - Nested Subquery."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT event_name, event_start_date, attendance_count
                FROM (
                    SELECT e.event_id, e.name AS event_name, e.event_start_date,
                           COUNT(i.user_id) AS attendance_count
                    FROM events e
                    LEFT JOIN interacts_with i ON e.event_id = i.event_id
                        AND i.interaction_type = 'attended'
                    WHERE e.club_id = %s
                    GROUP BY e.event_id, e.name, e.event_start_date
                ) AS event_stats
                ORDER BY attendance_count DESC
                LIMIT 3
                """,
                (club_id,),
            )
            rows = cursor.fetchall()
            return [
                {
                    "event_name": row[0],
                    "event_start_date": row[1],
                    "attendance_count": row[2],
                }
                for row in rows
            ]
        finally:
            cursor.close()
    #average turnout across all events
    @staticmethod
    def analytics_avg_attendance(club_id):
        """Query 3: Average Attendance per Event - Nested Aggregate."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT ROUND(AVG(attendance_count), 2) AS avg_attendance
                FROM (
                    SELECT COUNT(i.user_id) AS attendance_count
                    FROM events e
                    LEFT JOIN interacts_with i ON e.event_id = i.event_id
                        AND i.interaction_type = 'attended'
                    WHERE e.club_id = %s
                    GROUP BY e.event_id
                ) AS per_event
                """,
                (club_id,),
            )
            row = cursor.fetchone()
            return float(row[0]) if row and row[0] else 0.0
        finally:
            cursor.close()
    #events that filled more then half their capacity
    @staticmethod
    def analytics_quota_utilization(club_id):
        """Query 4: Events with >50% Quota Utilization - HAVING clause."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT e.name AS event_name, e.quota,
                       COUNT(i.user_id) AS attended,
                       ROUND((COUNT(i.user_id) / e.quota) * 100, 2) AS utilization_pct
                FROM events e
                LEFT JOIN interacts_with i ON e.event_id = i.event_id
                    AND i.interaction_type = 'attended'
                WHERE e.club_id = %s AND e.quota > 0
                GROUP BY e.event_id, e.name, e.quota
                HAVING COUNT(i.user_id) / e.quota > 0.5
                ORDER BY utilization_pct DESC
                """,
                (club_id,),
            )
            rows = cursor.fetchall()
            return [
                {
                    "event_name": row[0],
                    "quota": row[1],
                    "attended": row[2],
                    "utilization_pct": float(row[3]) if row[3] else 0.0,
                }
                for row in rows
            ]
        finally:
            cursor.close()
    #tracking attendence patterns weekly
    @staticmethod
    def analytics_weekly_trend(club_id):
        """Query 5: Weekly Attendance Trend - GROUP BY week."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT YEAR(e.event_start_date) AS yr,
                       WEEK(e.event_start_date) AS wk,
                       COUNT(i.user_id) AS total_attendance
                FROM events e
                JOIN interacts_with i ON e.event_id = i.event_id
                    AND i.interaction_type = 'attended'
                WHERE e.club_id = %s
                  AND e.event_start_date >= DATE_SUB(CURDATE(), INTERVAL 12 WEEK)
                GROUP BY YEAR(e.event_start_date), WEEK(e.event_start_date)
                ORDER BY yr, wk
                """,
                (club_id,),
            )
            rows = cursor.fetchall()
            return [
                {"year": row[0], "week": row[1], "total_attendance": row[2]}
                for row in rows
            ]
        finally:
            cursor.close()
    #floowers that actually attended events
    @staticmethod
    def analytics_follower_conversion(club_id):
        """Query 6: Follower to Attendee Conversion - Correlated Subquery."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT
                    (SELECT COUNT(*) FROM follows WHERE club_id = %s) AS total_followers,
                    COUNT(DISTINCT i.user_id) AS unique_attendees,
                    ROUND(
                        COUNT(DISTINCT i.user_id) * 100.0 /
                        NULLIF((SELECT COUNT(*) FROM follows WHERE club_id = %s), 0)
                    , 2) AS conversion_rate
                FROM interacts_with i
                JOIN events e ON i.event_id = e.event_id
                WHERE e.club_id = %s AND i.interaction_type = 'attended'
                """,
                (club_id, club_id, club_id),
            )
            row = cursor.fetchone()
            if not row:
                return {"total_followers": 0, "unique_attendees": 0, "conversion_rate": 0.0}
            return {
                "total_followers": row[0] or 0,
                "unique_attendees": row[1] or 0,
                "conversion_rate": float(row[2]) if row[2] else 0.0,
            }
        finally:
            cursor.close()
    #find members that never attended any event
    @staticmethod
    def analytics_inactive_members(club_id):
        """Query 7: Inactive Members - NOT EXISTS."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT u.user_id, u.name, cm.joined_at
                FROM club_members cm
                JOIN users u ON cm.user_id = u.user_id
                WHERE cm.club_id = %s
                  AND NOT EXISTS (
                      SELECT 1
                      FROM interacts_with i
                      JOIN events e ON i.event_id = e.event_id
                      WHERE i.user_id = cm.user_id
                        AND e.club_id = %s
                        AND i.interaction_type = 'attended'
                  )
                """,
                (club_id, club_id),
            )
            rows = cursor.fetchall()
            return [
                {"user_id": row[0], "name": row[1], "joined_at": row[2]}
                for row in rows
            ]
        finally:
            cursor.close()

    # BUDGET TRACKING
    # getting all budget transactions for the club
    @staticmethod
    def get_budget_transactions(club_id):
        """Get all budget transactions for the club."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT transaction_id, amount, transaction_date, transaction_type, description
                FROM budget_transactions
                WHERE club_id = %s
                ORDER BY transaction_date DESC
                """,
                (club_id,),
            )
            rows = cursor.fetchall()
            return [
                {
                    "transaction_id": row[0],
                    "amount": float(row[1]),
                    "transaction_date": row[2],
                    "transaction_type": row[3],
                    "description": row[4],
                }
                for row in rows
            ]
        finally:
            cursor.close()
    #recording a new budget transaction for the club
    @staticmethod
    def add_budget_transaction(club_id, amount, transaction_type, description):
        """Add a new budget transaction and update club balance."""
        cursor = get_cursor()
        db = get_db()
        try:
            # insert transaction
            cursor.execute(
                """
                INSERT INTO budget_transactions (club_id, amount, transaction_date, transaction_type, description)
                VALUES (%s, %s, CURDATE(), %s, %s)
                """,
                (club_id, amount, transaction_type, description),
            )

            # 
            #update club budget
            if transaction_type == 'INCOME':
                cursor.execute(
                    "UPDATE clubs SET budget = budget + %s WHERE club_id = %s",
                    (amount, club_id),
                )
            else:  # expense
                cursor.execute(
                    "UPDATE clubs SET budget = budget - %s WHERE club_id = %s",
                    (amount, club_id),
                )

            db.commit()
            return True, "Transaction added successfully"
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            cursor.close()
    #cartegorizing expenses in this month spending by description
    @staticmethod
    def get_monthly_expense_breakdown(club_id):
        """Get monthly expense breakdown by description."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT description, SUM(amount) as total_expense
                FROM budget_transactions
                WHERE club_id = %s AND transaction_type = 'EXPENSE'
                  AND transaction_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
                GROUP BY description
                ORDER BY total_expense DESC
                """,
                (club_id,),
            )
            rows = cursor.fetchall()
            return [
                {"description": row[0] or "Other", "total_expense": float(row[1])}
                for row in rows
            ]
        finally:
            cursor.close()
    # comparing income vs expense for the club
    @staticmethod
    def get_income_vs_expense(club_id):
        """Get total income vs expense for the club."""
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT
                    SUM(CASE WHEN transaction_type = 'INCOME' THEN amount ELSE 0 END) as total_income,
                    SUM(CASE WHEN transaction_type = 'EXPENSE' THEN amount ELSE 0 END) as total_expense
                FROM budget_transactions
                WHERE club_id = %s
                """,
                (club_id,),
            )
            row = cursor.fetchone()
            return {
                "total_income": float(row[0]) if row[0] else 0.0,
                "total_expense": float(row[1]) if row[1] else 0.0,
            }
        finally:
            cursor.close()
