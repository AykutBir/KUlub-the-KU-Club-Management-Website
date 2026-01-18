from app.db import get_cursor


class Event:
    @staticmethod
    def get_upcoming_events():
        """Fetch upcoming events for the feed."""
        cursor = get_cursor()
        try:
            # Join clubs and venues so each event card has full context
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
                ORDER BY e.publish_date ASC
                """
            )
            rows = cursor.fetchall()
            return [
                {
                    "event_id": row[0],
                    "name": row[1],
                    "publish_date": row[2],
                    "end_date": row[3],
                    "club_name": row[4],
                    "venue_name": row[5],
                    "capacity": row[6],
                }
                for row in rows
            ]
        finally:
            cursor.close()
