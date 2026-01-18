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

-- User Credentials
CREATE TABLE user_credentials (
  email VARCHAR(255) PRIMARY KEY,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE
);
