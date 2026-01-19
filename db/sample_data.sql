-- =============================================
-- SAMPLE DATA FOR CLUB MANAGEMENT SYSTEM
-- Run after clubmanagement.sql and club_manager_schema.sql
-- =============================================

USE club_management;

-- Clear existing data (in correct order due to foreign keys)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE interacts_with;
TRUNCATE TABLE follows;
TRUNCATE TABLE budget_transactions;
TRUNCATE TABLE membership_requests;
TRUNCATE TABLE club_members;
TRUNCATE TABLE events;
TRUNCATE TABLE clubs;
TRUNCATE TABLE venues;
TRUNCATE TABLE user_credentials;
TRUNCATE TABLE users;
SET FOREIGN_KEY_CHECKS = 1;

-- =============================================
-- VENUES (5 venues)
-- =============================================
INSERT INTO venues (venue_id, name, capacity) VALUES
(1, 'Main Auditorium', 500),
(2, 'Conference Room A', 50),
(3, 'Student Center Hall', 200),
(4, 'Outdoor Amphitheater', 300),
(5, 'Library Seminar Room', 30);

-- =============================================
-- USERS (13 users: 3 club admins, 10 basic users)
-- =============================================
INSERT INTO users (user_id, name, email, birthdate, role, created_at) VALUES
-- Club Administrators
(1, 'Ali Yilmaz', 'ali.yilmaz@ku.edu.tr', '1998-03-15', 'CLUB_ADMIN', '2024-01-10'),
(2, 'Ayse Demir', 'ayse.demir@ku.edu.tr', '1999-07-22', 'CLUB_ADMIN', '2024-01-12'),
(3, 'Mehmet Kaya', 'mehmet.kaya@ku.edu.tr', '1997-11-08', 'CLUB_ADMIN', '2024-01-15'),
-- Basic Users
(4, 'Zeynep Ozturk', 'zeynep.ozturk@ku.edu.tr', '2000-02-14', 'BASIC', '2024-02-01'),
(5, 'Can Aksoy', 'can.aksoy@ku.edu.tr', '2001-05-20', 'BASIC', '2024-02-05'),
(6, 'Elif Sahin', 'elif.sahin@ku.edu.tr', '2000-08-30', 'BASIC', '2024-02-10'),
(7, 'Burak Celik', 'burak.celik@ku.edu.tr', '1999-12-03', 'BASIC', '2024-02-15'),
(8, 'Selin Yildiz', 'selin.yildiz@ku.edu.tr', '2001-04-18', 'BASIC', '2024-02-20'),
(9, 'Emre Aydin', 'emre.aydin@ku.edu.tr', '2000-09-25', 'BASIC', '2024-03-01'),
(10, 'Deniz Arslan', 'deniz.arslan@ku.edu.tr', '1998-06-12', 'BASIC', '2024-03-05'),
(11, 'Ipek Korkmaz', 'ipek.korkmaz@ku.edu.tr', '2001-01-28', 'BASIC', '2024-03-10'),
(12, 'Omer Dogan', 'omer.dogan@ku.edu.tr', '1999-10-07', 'BASIC', '2024-03-15'),
(13, 'Melis Tekin', 'melis.tekin@ku.edu.tr', '2000-07-19', 'BASIC', '2024-03-20');

-- =============================================
-- USER CREDENTIALS (password: 'password123' for all)
-- Hash generated with bcrypt
-- =============================================
INSERT INTO user_credentials (email, password_hash) VALUES
('ali.yilmaz@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('ayse.demir@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('mehmet.kaya@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('zeynep.ozturk@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('can.aksoy@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('elif.sahin@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('burak.celik@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('selin.yildiz@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('emre.aydin@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('deniz.arslan@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('ipek.korkmaz@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('omer.dogan@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('melis.tekin@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC');

-- =============================================
-- CLUBS (3 clubs with admins)
-- =============================================
INSERT INTO clubs (club_id, name, foundation_date, budget, club_type, admin_user_id, description) VALUES
(1, 'Computer Science Society', '2020-09-01', 15000.00, 'OFFICIAL', 1, 'A community for CS enthusiasts to learn, share, and grow together through workshops, hackathons, and tech talks.'),
(2, 'Photography Club', '2021-03-15', 8500.00, 'STANDARD', 2, 'Capturing moments and memories. Join us for photo walks, exhibitions, and photography workshops.'),
(3, 'Debate Society', '2019-10-20', 12000.00, 'OFFICIAL', 3, 'Sharpen your critical thinking and public speaking skills through competitive debates and discussions.');

-- =============================================
-- CLUB MEMBERS (distributed across clubs)
-- =============================================
INSERT INTO club_members (user_id, club_id, joined_at, membership_title) VALUES
-- CS Society members
(4, 1, '2024-02-15', 'Member'),
(5, 1, '2024-02-20', 'Treasurer'),
(6, 1, '2024-03-01', 'Board Member'),
-- Photography Club members
(7, 2, '2024-02-25', 'Member'),
(8, 2, '2024-03-05', 'Member'),
-- Debate Society members
(9, 3, '2024-03-10', 'Vice President'),
(10, 3, '2024-03-15', 'Member');

-- =============================================
-- MEMBERSHIP REQUESTS (mix of statuses)
-- =============================================
INSERT INTO membership_requests (request_id, user_id, club_id, status, requested_at) VALUES
-- Pending requests
(1, 11, 1, 'PENDING', '2024-12-01'),
(2, 12, 1, 'PENDING', '2024-12-05'),
(3, 13, 2, 'PENDING', '2024-12-10'),
-- Approved requests (these users are now members)
(4, 4, 1, 'APPROVED', '2024-02-14'),
(5, 5, 1, 'APPROVED', '2024-02-19'),
(6, 7, 2, 'APPROVED', '2024-02-24'),
-- Rejected requests
(7, 11, 2, 'REJECTED', '2024-11-20'),
(8, 12, 3, 'REJECTED', '2024-11-25');

-- =============================================
-- EVENTS (12 events across clubs)
-- =============================================
INSERT INTO events (event_id, club_id, name, description, publish_date, end_date, venue_id, quota, event_start_date, category) VALUES
-- CS Society Events
(1, 1, 'Introduction to Machine Learning', 'Learn the basics of ML with hands-on examples using Python and scikit-learn.', '2024-11-01', '2024-12-15', 2, 45, '2024-12-15 14:00:00', 'Workshop'),
(2, 1, 'Hackathon 2024', 'Annual 24-hour coding competition with exciting prizes and networking opportunities.', '2024-11-15', '2025-01-20', 1, 200, '2025-01-20 09:00:00', 'Competition'),
(3, 1, 'Tech Talk: Cloud Computing', 'Industry expert discusses the future of cloud technologies and career opportunities.', '2024-12-01', '2025-01-10', 3, 150, '2025-01-10 15:00:00', 'Seminar'),
(4, 1, 'Python Workshop for Beginners', 'Start your programming journey with Python fundamentals.', '2024-10-15', '2024-11-20', 5, 25, '2024-11-20 10:00:00', 'Workshop'),
-- Photography Club Events
(5, 2, 'Night Photography Walk', 'Explore the city at night and capture stunning urban photographs.', '2024-11-10', '2024-12-20', 4, 30, '2024-12-20 19:00:00', 'Activity'),
(6, 2, 'Portrait Photography Masterclass', 'Learn professional portrait techniques from award-winning photographer.', '2024-12-05', '2025-01-15', 2, 20, '2025-01-15 13:00:00', 'Workshop'),
(7, 2, 'Annual Photo Exhibition', 'Showcase your best work at our yearly exhibition open to all students.', '2024-11-20', '2025-02-01', 3, 100, '2025-02-01 11:00:00', 'Exhibition'),
(8, 2, 'Landscape Photography Trip', 'Weekend trip to capture beautiful mountain landscapes.', '2024-10-01', '2024-11-15', 4, 15, '2024-11-15 07:00:00', 'Trip'),
-- Debate Society Events
(9, 3, 'Mock UN Conference', 'Simulate United Nations debates on current global issues.', '2024-11-25', '2025-01-25', 1, 100, '2025-01-25 09:00:00', 'Competition'),
(10, 3, 'Public Speaking Workshop', 'Improve your presentation skills with practical exercises and feedback.', '2024-12-10', '2025-01-05', 2, 35, '2025-01-05 14:00:00', 'Workshop'),
(11, 3, 'Inter-University Debate Tournament', 'Compete against debate teams from other universities.', '2024-11-01', '2025-02-10', 1, 80, '2025-02-10 10:00:00', 'Competition'),
(12, 3, 'Critical Thinking Seminar', 'Develop analytical skills essential for effective argumentation.', '2024-10-20', '2024-12-01', 5, 28, '2024-12-01 15:00:00', 'Seminar');

-- =============================================
-- INTERACTS_WITH (event interactions - saves and attends)
-- =============================================
INSERT INTO interacts_with (user_id, event_id, interaction_type, interaction_date) VALUES
-- CS Society event interactions
(4, 1, 'attended', '2024-12-15 14:30:00'),
(5, 1, 'attended', '2024-12-15 14:30:00'),
(6, 1, 'attended', '2024-12-15 14:30:00'),
(7, 1, 'saved', '2024-12-10 09:00:00'),
(4, 2, 'saved', '2024-12-01 10:00:00'),
(5, 2, 'attended', '2025-01-20 09:30:00'),
(6, 2, 'attended', '2025-01-20 09:30:00'),
(8, 2, 'saved', '2024-12-20 15:00:00'),
(4, 3, 'saved', '2024-12-15 11:00:00'),
(5, 4, 'attended', '2024-11-20 10:30:00'),
(6, 4, 'attended', '2024-11-20 10:30:00'),
(11, 4, 'attended', '2024-11-20 10:30:00'),
-- Photography Club event interactions
(7, 5, 'attended', '2024-12-20 19:30:00'),
(8, 5, 'attended', '2024-12-20 19:30:00'),
(4, 5, 'saved', '2024-12-18 08:00:00'),
(7, 6, 'saved', '2025-01-10 12:00:00'),
(8, 6, 'attended', '2025-01-15 13:30:00'),
(9, 7, 'saved', '2025-01-20 09:00:00'),
(7, 8, 'attended', '2024-11-15 07:30:00'),
(8, 8, 'attended', '2024-11-15 07:30:00'),
-- Debate Society event interactions
(9, 9, 'attended', '2025-01-25 09:30:00'),
(10, 9, 'attended', '2025-01-25 09:30:00'),
(11, 9, 'saved', '2025-01-20 14:00:00'),
(9, 10, 'attended', '2025-01-05 14:30:00'),
(10, 10, 'attended', '2025-01-05 14:30:00'),
(12, 10, 'saved', '2024-12-28 16:00:00'),
(9, 11, 'saved', '2025-01-15 11:00:00'),
(10, 12, 'attended', '2024-12-01 15:30:00'),
(9, 12, 'attended', '2024-12-01 15:30:00');

-- =============================================
-- FOLLOWS (users following clubs)
-- =============================================
INSERT INTO follows (user_id, club_id, follow_start_date) VALUES
-- Users following CS Society
(4, 1, '2024-02-01'),
(5, 1, '2024-02-03'),
(6, 1, '2024-02-10'),
(7, 1, '2024-03-01'),
(11, 1, '2024-11-01'),
(12, 1, '2024-11-15'),
-- Users following Photography Club
(7, 2, '2024-02-20'),
(8, 2, '2024-02-25'),
(4, 2, '2024-03-15'),
(13, 2, '2024-12-01'),
-- Users following Debate Society
(9, 3, '2024-03-01'),
(10, 3, '2024-03-10'),
(11, 3, '2024-04-01'),
(12, 3, '2024-04-15'),
(13, 3, '2024-05-01');

-- =============================================
-- BUDGET TRANSACTIONS (20 transactions)
-- =============================================
INSERT INTO budget_transactions (transaction_id, club_id, amount, transaction_date, transaction_type, description) VALUES
-- CS Society transactions
(1, 1, 5000.00, '2024-09-01', 'INCOME', 'University funding allocation'),
(2, 1, 2000.00, '2024-09-15', 'INCOME', 'Sponsorship from TechCorp'),
(3, 1, 500.00, '2024-10-01', 'EXPENSE', 'Workshop materials and supplies'),
(4, 1, 1200.00, '2024-10-20', 'EXPENSE', 'Hackathon prizes'),
(5, 1, 300.00, '2024-11-05', 'EXPENSE', 'Speaker honorarium'),
(6, 1, 3000.00, '2024-11-15', 'INCOME', 'Hackathon registration fees'),
(7, 1, 800.00, '2024-12-01', 'EXPENSE', 'Catering for tech talk'),
-- Photography Club transactions
(8, 2, 3000.00, '2024-09-01', 'INCOME', 'University funding allocation'),
(9, 2, 1500.00, '2024-09-20', 'INCOME', 'Equipment rental revenue'),
(10, 2, 2000.00, '2024-10-10', 'EXPENSE', 'New camera equipment'),
(11, 2, 400.00, '2024-11-01', 'EXPENSE', 'Exhibition printing costs'),
(12, 2, 600.00, '2024-11-20', 'EXPENSE', 'Transportation for photo trip'),
(13, 2, 1000.00, '2024-12-05', 'INCOME', 'Workshop registration fees'),
-- Debate Society transactions
(14, 3, 4000.00, '2024-09-01', 'INCOME', 'University funding allocation'),
(15, 3, 2500.00, '2024-09-25', 'INCOME', 'Tournament sponsorship'),
(16, 3, 1000.00, '2024-10-15', 'EXPENSE', 'Tournament venue booking'),
(17, 3, 500.00, '2024-11-01', 'EXPENSE', 'Judge honorariums'),
(18, 3, 300.00, '2024-11-20', 'EXPENSE', 'Printing and materials'),
(19, 3, 1500.00, '2024-12-01', 'INCOME', 'Mock UN registration fees'),
(20, 3, 700.00, '2024-12-10', 'EXPENSE', 'Catering for workshop');
