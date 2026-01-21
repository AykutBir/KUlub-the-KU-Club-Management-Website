CREATE DATABASE IF NOT EXISTS club_management;
USE club_management;

-- Users: User information
CREATE TABLE users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  birthdate DATE NOT NULL,
  role ENUM('BASIC','CLUB_ADMIN','SYSTEM_ADMIN') NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Credentials: Password hashes for authentication
CREATE TABLE user_credentials (
  email VARCHAR(255) PRIMARY KEY,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE
);

-- Venues: Event locations
CREATE TABLE venues (
  venue_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL UNIQUE,
  capacity INT NOT NULL
);

-- Clubs: Club information + club admin assignment
CREATE TABLE clubs (
  club_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL UNIQUE,
  foundation_date DATE NOT NULL,
  budget DECIMAL(12,2) NOT NULL DEFAULT 0.00,
  club_type ENUM('STANDARD','OFFICIAL') NOT NULL DEFAULT 'STANDARD',
  admin_user_id INT NULL,
  description TEXT,
  FOREIGN KEY (admin_user_id) REFERENCES users(user_id)
);

-- Budget Transactions: Track club income and expenses
CREATE TABLE budget_transactions (
  transaction_id INT AUTO_INCREMENT PRIMARY KEY,
  club_id INT NOT NULL,
  amount DECIMAL(12,2) NOT NULL,
  transaction_date DATE NOT NULL,
  transaction_type ENUM('INCOME','EXPENSE') NOT NULL,
  description VARCHAR(255),
  FOREIGN KEY (club_id) REFERENCES clubs(club_id)
);

-- Club Members: User membership in clubs
CREATE TABLE club_members (
  user_id INT PRIMARY KEY,
  club_id INT NOT NULL,
  joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  membership_title VARCHAR(50) DEFAULT 'Member',
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (club_id) REFERENCES clubs(club_id)
);

-- Membership Requests: Pending membership applications
CREATE TABLE membership_requests (
  request_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  club_id INT NOT NULL,
  status ENUM('PENDING','APPROVED','REJECTED') NOT NULL DEFAULT 'PENDING',
  requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uniq_request (user_id, club_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (club_id) REFERENCES clubs(club_id)
);

-- Follows: Users following clubs
CREATE TABLE follows (
  user_id INT NOT NULL,
  club_id INT NOT NULL,
  follow_start_date DATE NOT NULL,
  PRIMARY KEY (user_id, club_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (club_id) REFERENCES clubs(club_id) ON DELETE CASCADE
);

-- Events: Club events with full details
CREATE TABLE events (
  event_id INT AUTO_INCREMENT PRIMARY KEY,
  club_id INT NOT NULL,
  name VARCHAR(150) NOT NULL,
  description TEXT NOT NULL,
  publish_date DATE NOT NULL,
  end_date DATE NOT NULL,
  venue_id INT NOT NULL,
  deleted BOOLEAN DEFAULT FALSE,
  quota INT DEFAULT 50,
  event_start_date DATETIME,
  category VARCHAR(50),
  FOREIGN KEY (club_id) REFERENCES clubs(club_id),
  FOREIGN KEY (venue_id) REFERENCES venues(venue_id)
);

-- Event Saves: Users saving events for later
CREATE TABLE event_saves (
  user_id INT NOT NULL,
  event_id INT NOT NULL,
  saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, event_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

-- Event Attendance: Users attending events
CREATE TABLE event_attendance (
  user_id INT NOT NULL,
  event_id INT NOT NULL,
  attended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, event_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

-- Interacts With: Alternative table for event interactions
CREATE TABLE interacts_with (
  user_id INT NOT NULL,
  event_id INT NOT NULL,
  interaction_type ENUM('saved', 'attended') NOT NULL,
  interaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, event_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

-- Event Modifications: Audit trail for event changes
CREATE TABLE event_modifications (
  modification_id INT AUTO_INCREMENT PRIMARY KEY,
  event_id INT NOT NULL,
  modification_type ENUM('UPDATE', 'DELETE') NOT NULL,
  modification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  description TEXT NULL,
  modified_by_user_id INT NOT NULL,
  FOREIGN KEY (event_id) REFERENCES events(event_id),
  FOREIGN KEY (modified_by_user_id) REFERENCES users(user_id)
);




