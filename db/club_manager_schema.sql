-- =============================================
-- CLUB MANAGER SCHEMA ADDITIONS
-- Run after main clubmanagement.sql
-- =============================================

USE club_management;

-- Interacts_with: tracks user save/attend for events
DROP TABLE IF EXISTS interacts_with;
CREATE TABLE interacts_with (
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    interaction_type ENUM('saved', 'attended') NOT NULL,
    interaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, event_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

-- Follows: tracks users following clubs
DROP TABLE IF EXISTS follows;
CREATE TABLE follows (
    user_id INT NOT NULL,
    club_id INT NOT NULL,
    follow_start_date DATE NOT NULL,
    PRIMARY KEY (user_id, club_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (club_id) REFERENCES clubs(club_id) ON DELETE CASCADE
);

-- Add missing columns to events table
-- Check if columns exist before adding (MySQL 8.0+)
SET @dbname = 'club_management';
SET @tablename = 'events';

-- Add quota column if not exists
SET @columnname = 'quota';
SET @preparedStatement = (SELECT IF(
  (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
   WHERE TABLE_SCHEMA = @dbname AND TABLE_NAME = @tablename AND COLUMN_NAME = @columnname) > 0,
  'SELECT 1',
  'ALTER TABLE events ADD COLUMN quota INT DEFAULT 50'
));
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

-- Add event_start_date column if not exists
SET @columnname = 'event_start_date';
SET @preparedStatement = (SELECT IF(
  (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
   WHERE TABLE_SCHEMA = @dbname AND TABLE_NAME = @tablename AND COLUMN_NAME = @columnname) > 0,
  'SELECT 1',
  'ALTER TABLE events ADD COLUMN event_start_date DATETIME'
));
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

-- Add category column if not exists
SET @columnname = 'category';
SET @preparedStatement = (SELECT IF(
  (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
   WHERE TABLE_SCHEMA = @dbname AND TABLE_NAME = @tablename AND COLUMN_NAME = @columnname) > 0,
  'SELECT 1',
  'ALTER TABLE events ADD COLUMN category VARCHAR(50)'
));
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

-- Add membership_title to club_members if not exists
SET @tablename = 'club_members';
SET @columnname = 'membership_title';
SET @preparedStatement = (SELECT IF(
  (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
   WHERE TABLE_SCHEMA = @dbname AND TABLE_NAME = @tablename AND COLUMN_NAME = @columnname) > 0,
  'SELECT 1',
  'ALTER TABLE club_members ADD COLUMN membership_title VARCHAR(50) DEFAULT ''Member'''
));
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

-- Add description column to clubs if not exists
SET @tablename = 'clubs';
SET @columnname = 'description';
SET @preparedStatement = (SELECT IF(
  (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
   WHERE TABLE_SCHEMA = @dbname AND TABLE_NAME = @tablename AND COLUMN_NAME = @columnname) > 0,
  'SELECT 1',
  'ALTER TABLE clubs ADD COLUMN description TEXT'
));
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;
