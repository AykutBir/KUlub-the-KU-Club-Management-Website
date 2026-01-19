CREATE DATABASE club_management;
USE club_management;
-- Users
CREATE TABLE users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  birthdate DATE NOT NULL,
  role ENUM('BASIC','CLUB_ADMIN','SYSTEM_ADMIN') NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Venues (must come before events)
CREATE TABLE venues (
  venue_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL UNIQUE,
  capacity INT NOT NULL
);

-- Clubs
CREATE TABLE clubs (
  club_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL UNIQUE,
  foundation_date DATE NOT NULL,
  budget DECIMAL(12,2) NOT NULL DEFAULT 0.00,
  club_type ENUM('STANDARD','OFFICIAL') NOT NULL DEFAULT 'STANDARD',
  admin_user_id INT NULL,
  FOREIGN KEY (admin_user_id) REFERENCES users(user_id)
);

-- Events
CREATE TABLE events (
  event_id INT AUTO_INCREMENT PRIMARY KEY,
  club_id INT NOT NULL,
  name VARCHAR(150) NOT NULL,
  description TEXT NOT NULL,
  publish_date DATE NOT NULL,
  end_date DATE NOT NULL,
  venue_id INT NOT NULL,
  deleted BOOLEAN DEFAULT FALSE,
  FOREIGN KEY (club_id) REFERENCES clubs(club_id),
  FOREIGN KEY (venue_id) REFERENCES venues(venue_id)
);

-- Budget Transactions
CREATE TABLE budget_transactions (
  transaction_id INT AUTO_INCREMENT PRIMARY KEY,
  club_id INT NOT NULL,
  amount DECIMAL(12,2) NOT NULL,
  transaction_date DATE NOT NULL,
  transaction_type ENUM('INCOME','EXPENSE') NOT NULL,
  description VARCHAR(255),
  FOREIGN KEY (club_id) REFERENCES clubs(club_id)
);

-- Memberships
CREATE TABLE club_members (
  user_id INT PRIMARY KEY,
  club_id INT NOT NULL,
  joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (club_id) REFERENCES clubs(club_id)
);

-- Membership Requests
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

-- Club Followers
CREATE TABLE club_followers (
  user_id INT NOT NULL,
  club_id INT NOT NULL,
  followed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, club_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (club_id) REFERENCES clubs(club_id) ON DELETE CASCADE
);

-- Event Saves
CREATE TABLE event_saves (
  user_id INT NOT NULL,
  event_id INT NOT NULL,
  saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, event_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

-- Event Attendance
CREATE TABLE event_attendance (
  user_id INT NOT NULL,
  event_id INT NOT NULL,
  attended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, event_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

-- User Credentials
CREATE TABLE user_credentials (
  email VARCHAR(255) PRIMARY KEY,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE
);

-- Enforce mutual exclusivity between event_saves and event_attendance
--due to our rule: Event Interaction: A user can either save an event or attend an event, but never both.
DELIMITER $$
CREATE TRIGGER trg_block_save_if_attending
BEFORE INSERT ON event_saves
FOR EACH ROW
BEGIN
  IF EXISTS (
    SELECT 1 FROM event_attendance
    WHERE user_id = NEW.user_id AND event_id = NEW.event_id
  ) THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Cannot save an event you are attending.';
  END IF;
END$$

CREATE TRIGGER trg_block_attend_if_saved
BEFORE INSERT ON event_attendance
FOR EACH ROW
BEGIN
  IF EXISTS (
    SELECT 1 FROM event_saves
    WHERE user_id = NEW.user_id AND event_id = NEW.event_id
  ) THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Cannot attend an event you have saved.';
  END IF;
END$$

--Membership Limit: A basic user can be a member of only one club at a time.
-- Official clubs Limit: no membership requests
CREATE TRIGGER trg_block_official_membership_request
BEFORE INSERT ON membership_requests
FOR EACH ROW
BEGIN
  IF EXISTS (
    SELECT 1 FROM clubs
    WHERE club_id = NEW.club_id AND club_type = 'OFFICIAL'
  ) THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Official clubs do not accept membership requests.';
  END IF;

  IF EXISTS (
    SELECT 1 FROM club_members
    WHERE user_id = NEW.user_id
  ) THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'User is already a member of a club.';
  END IF;

  IF EXISTS (
    SELECT 1 FROM membership_requests
    WHERE user_id = NEW.user_id AND status = 'PENDING'
  ) THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'User already has a pending membership request.';
  END IF;
END$$

CREATE TRIGGER trg_block_approve_if_member_or_official
BEFORE UPDATE ON membership_requests
FOR EACH ROW
BEGIN
  IF NEW.status = 'APPROVED' AND OLD.status <> 'APPROVED' THEN
    IF EXISTS (
      SELECT 1 FROM club_members
      WHERE user_id = NEW.user_id
    ) THEN
      SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'User is already a member of a club.';
    END IF;

    IF EXISTS (
      SELECT 1 FROM clubs
      WHERE club_id = NEW.club_id AND club_type = 'OFFICIAL'
    ) THEN
      SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Official clubs cannot approve membership requests.';
    END IF;
  END IF;
END$$
DELIMITER ;


-- Event Modifications
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
