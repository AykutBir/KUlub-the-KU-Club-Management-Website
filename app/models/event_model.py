from app.db import get_cursor, get_db


class Event:
    @staticmethod
    def get_upcoming_events():
        cursor = get_cursor()
        try:
            # Join clubs and venues so each event card has full context
            cursor.execute(
                """
                SELECT e.event_id,
                       e.club_id,
                       e.name,
                       e.publish_date,
                       e.end_date,
                       c.name AS club_name,
                       v.name AS venue_name,
                       v.capacity
                FROM events e
                JOIN clubs c ON c.club_id = e.club_id
                JOIN venues v ON v.venue_id = e.venue_id
                WHERE e.end_date >= CURDATE()
                  AND e.deleted = FALSE
                ORDER BY e.publish_date ASC
                """
            )
            rows = cursor.fetchall()
            return [
                {"event_id": row[0],"club_id": row[1],
                "name": row[2],"publish_date": row[3],
                "end_date": row[4],"club_name": row[5],
                "venue_name": row[6],"capacity": row[7],
                } for row in rows
            ]
        finally:
            cursor.close()

    @staticmethod
    def get_upcoming_events_paginated(page=1, per_page=10):
        cursor = get_cursor()
        try:
            # Count total events (excluding deleted)
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM events e
                WHERE e.end_date >= CURDATE()
                  AND e.deleted = FALSE
                """)
            total_events = cursor.fetchone()[0]
            
            # Calculate offset
            offset = (page - 1) * per_page
            
            # Fetch paginated events
            cursor.execute(
                """
                SELECT e.event_id,
                       e.name,
                       e.publish_date,
                       e.end_date,
                       c.name AS club_name,
                       v.name AS venue_name,
                       v.capacity
                FROM events e
                JOIN clubs c ON c.club_id = e.club_id
                JOIN venues v ON v.venue_id = e.venue_id
                WHERE e.end_date >= CURDATE()
                  AND e.deleted = FALSE
                ORDER BY e.publish_date ASC
                LIMIT %s OFFSET %s
                """,
                (per_page, offset)
            )
            rows = cursor.fetchall()
            
            events = [
                {
                "event_id": row[0],"name": row[1],
                "publish_date": row[2],"end_date": row[3],
                "club_name": row[4],"venue_name": row[5],
                "capacity": row[6],
                }for row in rows]
            
            total_pages = (total_events + per_page - 1) // per_page if total_events > 0 else 0
            
            return {
                "events": events,"total_events": total_events,
                "total_pages": total_pages,"current_page": page}
        finally:
            cursor.close()

    @staticmethod
    def get_event_by_id(event_id):
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT e.event_id,
                       e.club_id,
                       e.name,
                       e.description,
                       e.publish_date,
                       e.end_date,
                       e.venue_id,
                       c.name AS club_name,
                       v.name AS venue_name
                FROM events e
                JOIN clubs c ON c.club_id = e.club_id
                JOIN venues v ON v.venue_id = e.venue_id
                WHERE e.event_id = %s
                  AND e.deleted = FALSE
                """,
                (event_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            
            return {
                "event_id": row[0],"club_id": row[1],"name": row[2],"description": row[3],"publish_date": row[4],"end_date": row[5],"venue_id": row[6],"club_name": row[7],"venue_name": row[8],}
        finally:
            cursor.close()

    @staticmethod
    def update_event(event_id, name, description, end_date, venue_id, club_id):
        db = get_db()
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                UPDATE events
                SET name = %s,
                    description = %s,
                    end_date = %s,
                    venue_id = %s,
                    club_id = %s
                WHERE event_id = %s
                  AND deleted = FALSE
                """,
                (name, description, end_date, venue_id, club_id, event_id)
            )
            db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def delete_event(event_id):
        db = get_db()
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                UPDATE events
                SET deleted = TRUE
                WHERE event_id = %s
                """,
                (event_id,)
            )
            db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def record_modification(event_id, modification_type, description, user_id):
        db = get_db()
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                INSERT INTO event_modifications 
                (event_id, modification_type, description, modified_by_user_id)
                VALUES (%s, %s, %s, %s)
                """,
                (event_id, modification_type, description if description else None, user_id)
            )
            db.commit()
            return cursor.lastrowid
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def get_all_venues():
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT venue_id, name, capacity
                FROM venues
                ORDER BY name
                """
            )
            rows = cursor.fetchall()
            return [{"venue_id": row[0],"name": row[1],"capacity": row[2],} for row in rows]
        finally:
            cursor.close()

    @staticmethod
    def get_finished_events_paginated(page=1, per_page=10):
        cursor = get_cursor()
        try:
            # Count total finished events (excluding deleted)
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM events e
                WHERE e.end_date < CURDATE()
                  AND e.deleted = FALSE
                """
            )
            total_events = cursor.fetchone()[0]
            
            # Calculate offset
            offset = (page - 1) * per_page
            
            # Fetch paginated finished events
            cursor.execute(
                """
                SELECT e.event_id,
                       e.name,
                       e.publish_date,
                       e.end_date,
                       c.name AS club_name,
                       v.name AS venue_name
                FROM events e
                JOIN clubs c ON c.club_id = e.club_id
                JOIN venues v ON v.venue_id = e.venue_id
                WHERE e.end_date < CURDATE()
                  AND e.deleted = FALSE
                ORDER BY e.end_date DESC
                LIMIT %s OFFSET %s
                """,
                (per_page, offset)
            )
            rows = cursor.fetchall()
            
            events = [
                {"event_id": row[0],"name": row[1],"publish_date": row[2],
                "end_date": row[3],"club_name": row[4],"venue_name": row[5],}for row in rows]
            
            total_pages = (total_events + per_page - 1) // per_page if total_events > 0 else 0
            
            return {"events": events,"total_events": total_events,"total_pages": total_pages,"current_page": page}
        finally:
            cursor.close()

    @staticmethod
    def get_event_modifications_paginated(page=1, per_page=10):
        cursor = get_cursor()
        try:
            # Count total modifications
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM event_modifications em
                """
            )
            total_modifications = cursor.fetchone()[0]
            
            # Calculate offset
            offset = (page - 1) * per_page
            
            # Fetch paginated modifications
            cursor.execute(
                """
                SELECT em.modification_id,
                       em.event_id,
                       em.modification_type,
                       em.modification_date,
                       em.description,
                       e.name AS event_name,
                       c.name AS club_name,
                       u.name AS admin_name
                FROM event_modifications em
                JOIN events e ON e.event_id = em.event_id
                JOIN clubs c ON c.club_id = e.club_id
                JOIN users u ON u.user_id = em.modified_by_user_id
                ORDER BY em.modification_date DESC
                LIMIT %s OFFSET %s
                """,
                (per_page, offset)
            )
            rows = cursor.fetchall()
            
            modifications = [
                {"modification_id": row[0],"event_id": row[1],
                "modification_type": row[2],"modification_date": row[3],
                "description": row[4] if row[4] else None,"event_name": row[5],
                "club_name": row[6],"admin_name": row[7],}for row in rows]
            
            total_pages = (total_modifications + per_page - 1) // per_page if total_modifications > 0 else 0
            
            return {
                "modifications": modifications,"total_modifications": total_modifications,
                "total_pages": total_pages,"current_page": page}
        finally:
            cursor.close()

    @staticmethod
    def save_event(user_id, event_id):
        db = get_db()
        cursor = get_cursor()
        try:
            # Check if user is already attending this event (replaces trigger trg_block_save_if_attending)
            cursor.execute(
                """
                SELECT 1 FROM event_attendance
                WHERE user_id = %s AND event_id = %s
                LIMIT 1
                """,
                (user_id, event_id),
            )
            if cursor.fetchone():
                raise ValueError('Cannot save an event you are attending.')
            
            cursor.execute(
                """
                INSERT INTO event_saves (user_id, event_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE saved_at = saved_at
                """,
                (user_id, event_id),
            )
            db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def unsave_event(user_id, event_id):
        db = get_db()
        cursor = get_cursor()
        try:
            cursor.execute(
                "DELETE FROM event_saves WHERE user_id = %s AND event_id = %s",
                (user_id, event_id),
            )
            db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def attend_event(user_id, event_id):
        db = get_db()
        cursor = get_cursor()
        try:
            # Check if user has saved this event (replaces trigger trg_block_attend_if_saved)
            cursor.execute(
                """
                SELECT 1 FROM event_saves
                WHERE user_id = %s AND event_id = %s
                LIMIT 1
                """,
                (user_id, event_id),
            )
            if cursor.fetchone():
                raise ValueError('Cannot attend an event you have saved.')
            
            cursor.execute(
                """
                INSERT INTO event_attendance (user_id, event_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE attended_at = attended_at
                """,
                (user_id, event_id),
            )
            db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def cancel_attendance(user_id, event_id):
        db = get_db()
        cursor = get_cursor()
        try:
            cursor.execute(
                "DELETE FROM event_attendance WHERE user_id = %s AND event_id = %s",
                (user_id, event_id),
            )
            db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def has_saved(user_id, event_id):
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT 1
                FROM event_saves
                WHERE user_id = %s AND event_id = %s
                LIMIT 1
                """,
                (user_id, event_id),
            )
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    @staticmethod
    def is_attending(user_id, event_id):
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT 1
                FROM event_attendance
                WHERE user_id = %s AND event_id = %s
                LIMIT 1
                """,
                (user_id, event_id),
            )
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    @staticmethod
    def get_user_saved_events(user_id):
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT e.event_id,
                       e.name,
                       e.publish_date,
                       e.end_date,
                       c.name AS club_name,
                       v.name AS venue_name,
                       v.capacity
                FROM event_saves es
                JOIN events e ON e.event_id = es.event_id
                JOIN clubs c ON c.club_id = e.club_id
                JOIN venues v ON v.venue_id = e.venue_id
                WHERE es.user_id = %s
                  AND e.deleted = FALSE
                ORDER BY es.saved_at DESC
                """,
                (user_id,),
            )
            rows = cursor.fetchall()
            return [
                {"event_id": row[0],"name": row[1],
                "publish_date": row[2],"end_date": row[3],
                "club_name": row[4],"venue_name": row[5],
                "capacity": row[6],}for row in rows]
        finally:
            cursor.close()

    @staticmethod
    def get_user_attended_events(user_id):
        cursor = get_cursor()
        try:
            cursor.execute(
                """
                SELECT e.event_id,
                       e.name,
                       e.publish_date,
                       e.end_date,
                       c.name AS club_name,
                       v.name AS venue_name,
                       v.capacity
                FROM event_attendance ea
                JOIN events e ON e.event_id = ea.event_id
                JOIN clubs c ON c.club_id = e.club_id
                JOIN venues v ON v.venue_id = e.venue_id
                WHERE ea.user_id = %s
                  AND e.deleted = FALSE
                ORDER BY ea.attended_at DESC
                """,
                (user_id,),
            )
            rows = cursor.fetchall()
            return [
                {"event_id": row[0],"name": row[1],"publish_date": row[2],
                "end_date": row[3],"club_name": row[4],"venue_name": row[5],
                "capacity": row[6],
                }for row in rows]
        finally:
            cursor.close()
