import os
from flask_mysqldb import MySQL
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

mysql = MySQL()

def init_db(app):
    """Initialize MySQL connection with Flask app"""
    # Get host - ensure it's not a port number
    host = os.getenv('DB_HOST') or os.getenv('MYSQL_HOST') or 'localhost'
    # Fix: If host is '3306' (common mistake), reset to localhost
    if host == '3306' or host.isdigit():
        host = 'localhost'
    
    app.config['MYSQL_HOST'] = host
    app.config['MYSQL_USER'] = os.getenv('DB_USER') or os.getenv('MYSQL_USER') or 'root'
    app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD') or os.getenv('MYSQL_PASSWORD') or ''
    app.config['MYSQL_DB'] = os.getenv('DB_NAME') or os.getenv('MYSQL_DB') or 'club_management'
    
    # Get port - ensure it's an integer
    port_str = os.getenv('DB_PORT') or os.getenv('MYSQL_PORT') or '3306'
    try:
        app.config['MYSQL_PORT'] = int(port_str)
    except ValueError:
        app.config['MYSQL_PORT'] = 3306
    
    mysql.init_app(app)
    return mysql

def get_db():
    """Get database connection"""
    return mysql.connection

def get_cursor():
    """Get database cursor"""
    return mysql.connection.cursor()

