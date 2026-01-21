-- =============================================
-- SAMPLE DATA FOR CLUB MANAGEMENT SYSTEM
-- Run after clubmanagement.sql and club_manager_schema.sql
-- =============================================

USE club_management;

-- Clear existing data (in correct order due to foreign keys)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE event_modifications;
TRUNCATE TABLE interacts_with;
TRUNCATE TABLE event_attendance;
TRUNCATE TABLE event_saves;
TRUNCATE TABLE follows;
TRUNCATE TABLE club_followers;
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
-- VENUES (8 venues)
-- =============================================
INSERT INTO venues (venue_id, name, capacity) VALUES
(1, 'Main Auditorium', 500),
(2, 'Conference Room A', 50),
(3, 'Student Center Hall', 200),
(4, 'Outdoor Amphitheater', 300),
(5, 'Library Seminar Room', 30),
(6, 'Sports Complex Hall', 400),
(7, 'Engineering Building Room 101', 80),
(8, 'Arts Center Gallery', 150);

-- =============================================
-- USERS (24 users: 1 system admin, 6 club admins, 17 basic users)
-- =============================================
INSERT INTO users (user_id, name, email, birthdate, role, created_at) VALUES
-- System Administrator
(1, 'Admin User', 'admin@ku.edu.tr', '1995-01-01', 'SYSTEM_ADMIN', '2024-01-01'),
-- Club Administrators
(2, 'Ali Yilmaz', 'ali.yilmaz@ku.edu.tr', '1998-03-15', 'CLUB_ADMIN', '2024-01-10'),
(3, 'Ayse Demir', 'ayse.demir@ku.edu.tr', '1999-07-22', 'CLUB_ADMIN', '2024-01-12'),
(4, 'Mehmet Kaya', 'mehmet.kaya@ku.edu.tr', '1997-11-08', 'CLUB_ADMIN', '2024-01-15'),
(15, 'Fatma Yildirim', 'fatma.yildirim@ku.edu.tr', '1998-05-10', 'CLUB_ADMIN', '2024-01-20'),
(16, 'Mustafa Ozkan', 'mustafa.ozkan@ku.edu.tr', '1996-09-18', 'CLUB_ADMIN', '2024-01-25'),
(17, 'Seda Karaca', 'seda.karaca@ku.edu.tr', '1999-12-05', 'CLUB_ADMIN', '2024-02-01'),
-- Basic Users
(5, 'Zeynep Ozturk', 'zeynep.ozturk@ku.edu.tr', '2000-02-14', 'BASIC', '2024-02-01'),
(6, 'Can Aksoy', 'can.aksoy@ku.edu.tr', '2001-05-20', 'BASIC', '2024-02-05'),
(7, 'Elif Sahin', 'elif.sahin@ku.edu.tr', '2000-08-30', 'BASIC', '2024-02-10'),
(8, 'Burak Celik', 'burak.celik@ku.edu.tr', '1999-12-03', 'BASIC', '2024-02-15'),
(9, 'Selin Yildiz', 'selin.yildiz@ku.edu.tr', '2001-04-18', 'BASIC', '2024-02-20'),
(10, 'Emre Aydin', 'emre.aydin@ku.edu.tr', '2000-09-25', 'BASIC', '2024-03-01'),
(11, 'Deniz Arslan', 'deniz.arslan@ku.edu.tr', '1998-06-12', 'BASIC', '2024-03-05'),
(12, 'Ipek Korkmaz', 'ipek.korkmaz@ku.edu.tr', '2001-01-28', 'BASIC', '2024-03-10'),
(13, 'Omer Dogan', 'omer.dogan@ku.edu.tr', '1999-10-07', 'BASIC', '2024-03-15'),
(14, 'Melis Tekin', 'melis.tekin@ku.edu.tr', '2000-07-19', 'BASIC', '2024-03-20'),
(18, 'Cem Ates', 'cem.ates@ku.edu.tr', '2001-03-22', 'BASIC', '2024-04-01'),
(19, 'Gizem Bulut', 'gizem.bulut@ku.edu.tr', '2000-06-14', 'BASIC', '2024-04-05'),
(20, 'Kaan Yucel', 'kaan.yucel@ku.edu.tr', '1999-11-30', 'BASIC', '2024-04-10'),
(21, 'Leyla Cetin', 'leyla.cetin@ku.edu.tr', '2001-08-17', 'BASIC', '2024-04-15'),
(22, 'Onur Koc', 'onur.koc@ku.edu.tr', '2000-01-25', 'BASIC', '2024-04-20'),
(23, 'Pinar Yilmaz', 'pinar.yilmaz@ku.edu.tr', '1998-04-08', 'BASIC', '2024-05-01'),
(24, 'Riza Demir', 'riza.demir@ku.edu.tr', '2001-10-12', 'BASIC', '2024-05-05');

-- =============================================
-- USER CREDENTIALS (password: 'password123' for all)
-- Hash generated with bcrypt
-- =============================================
INSERT INTO user_credentials (email, password_hash) VALUES
('admin@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
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
('melis.tekin@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('fatma.yildirim@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('mustafa.ozkan@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('seda.karaca@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('cem.ates@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('gizem.bulut@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('kaan.yucel@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('leyla.cetin@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('onur.koc@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('pinar.yilmaz@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC'),
('riza.demir@ku.edu.tr', '$2b$12$Uz17KCEkYuOsOLgkZrQ.1O1SF97fgcPrPFkMobob7LcCORXL4IqOC');

-- =============================================
-- CLUBS (6 clubs with admins)
-- =============================================
INSERT INTO clubs (club_id, name, foundation_date, budget, club_type, admin_user_id, description) VALUES
(1, 'Computer Science Society', '2020-09-01', 15000.00, 'OFFICIAL', 2, 'A community for CS enthusiasts to learn, share, and grow together through workshops, hackathons, and tech talks.'),
(2, 'Photography Club', '2021-03-15', 8500.00, 'STANDARD', 3, 'Capturing moments and memories. Join us for photo walks, exhibitions, and photography workshops.'),
(3, 'Debate Society', '2019-10-20', 12000.00, 'OFFICIAL', 4, 'Sharpen your critical thinking and public speaking skills through competitive debates and discussions.'),
(4, 'Music Society', '2022-01-10', 11000.00, 'STANDARD', 15, 'Express yourself through music. Join our band, choir, or solo performances. Open to all skill levels.'),
(5, 'Sports Club', '2020-05-20', 18000.00, 'OFFICIAL', 16, 'Stay active and competitive. We organize tournaments, training sessions, and inter-university competitions.'),
(6, 'Art & Design Club', '2021-09-15', 9500.00, 'STANDARD', 17, 'Unleash your creativity through various art forms. Workshops, exhibitions, and collaborative projects await.');

-- =============================================
-- CLUB MEMBERS (distributed across clubs)
-- Note: Schema allows only one club membership per user (user_id is PRIMARY KEY)
-- =============================================
INSERT INTO club_members (user_id, club_id, joined_at, membership_title) VALUES
-- CS Society members
(5, 1, '2024-02-15', 'Member'),
(6, 1, '2024-02-20', 'Treasurer'),
(7, 1, '2024-03-01', 'Board Member'),
(18, 1, '2024-04-10', 'Member'),
(19, 1, '2024-05-01', 'Secretary'),
-- Photography Club members
(8, 2, '2024-02-25', 'Member'),
(9, 2, '2024-03-05', 'Member'),
(20, 2, '2024-04-15', 'Member'),
(21, 2, '2024-05-10', 'Event Coordinator'),
-- Debate Society members
(10, 3, '2024-03-10', 'Vice President'),
(11, 3, '2024-03-15', 'Member'),
(22, 3, '2024-04-20', 'Member'),
(23, 3, '2024-05-15', 'Treasurer'),
-- Music Society members
(12, 4, '2024-04-10', 'Member'),
(24, 4, '2024-05-20', 'Member'),
-- Sports Club members
(13, 5, '2024-04-05', 'Member'),
(14, 5, '2024-04-15', 'Member');
-- Note: Users 5, 6, 7, 8, 9, 11, 18, 19, 20, 21 already have memberships in other clubs
-- The schema only allows one club membership per user (user_id is PRIMARY KEY)

-- =============================================
-- MEMBERSHIP REQUESTS (mix of statuses with complex scenarios)
-- =============================================
INSERT INTO membership_requests (request_id, user_id, club_id, status, requested_at) VALUES
-- Pending requests
(1, 12, 1, 'PENDING', '2024-12-01'),
(2, 13, 1, 'PENDING', '2024-12-05'),
(3, 14, 2, 'PENDING', '2024-12-10'),
(9, 18, 2, 'PENDING', '2024-12-15'),
(10, 19, 3, 'PENDING', '2024-12-20'),
(11, 20, 4, 'PENDING', '2024-12-25'),
(12, 21, 5, 'PENDING', '2024-12-28'),
-- Approved requests (these users are now members)
(4, 5, 1, 'APPROVED', '2024-02-14'),
(5, 6, 1, 'APPROVED', '2024-02-19'),
(6, 8, 2, 'APPROVED', '2024-02-24'),
(13, 5, 4, 'APPROVED', '2024-03-19'),
(14, 7, 4, 'APPROVED', '2024-03-30'),
(15, 18, 1, 'APPROVED', '2024-04-09'),
(16, 18, 4, 'APPROVED', '2024-04-30'),
(17, 6, 5, 'APPROVED', '2024-03-24'),
(18, 8, 6, 'APPROVED', '2024-03-30'),
(19, 9, 6, 'APPROVED', '2024-04-09'),
(20, 11, 6, 'APPROVED', '2024-04-19'),
-- Rejected requests
(7, 12, 2, 'REJECTED', '2024-11-20'),
(8, 13, 3, 'REJECTED', '2024-11-25'),
(21, 14, 1, 'REJECTED', '2024-10-15'),
(22, 15, 2, 'REJECTED', '2024-10-20'),
(23, 16, 3, 'REJECTED', '2024-10-25'),
(24, 17, 4, 'REJECTED', '2024-11-01');

-- =============================================
-- EVENTS (30 events across clubs including past/overdue events)
-- =============================================
INSERT INTO events (event_id, club_id, name, description, publish_date, end_date, venue_id, quota, event_start_date, category) VALUES
-- CS Society Events (including past events)
(1, 1, 'Introduction to Machine Learning', 'Learn the basics of ML with hands-on examples using Python and scikit-learn.', '2024-11-01', '2024-12-15', 2, 45, '2024-12-15 14:00:00', 'Workshop'),
(2, 1, 'Hackathon 2024', 'Annual 24-hour coding competition with exciting prizes and networking opportunities.', '2024-11-15', '2025-01-20', 1, 200, '2025-01-20 09:00:00', 'Competition'),
(3, 1, 'Tech Talk: Cloud Computing', 'Industry expert discusses the future of cloud technologies and career opportunities.', '2024-12-01', '2025-01-10', 3, 150, '2025-01-10 15:00:00', 'Seminar'),
(4, 1, 'Python Workshop for Beginners', 'Start your programming journey with Python fundamentals.', '2024-10-15', '2024-11-20', 5, 25, '2024-11-20 10:00:00', 'Workshop'),
(13, 1, 'Web Development Bootcamp 2023', 'Intensive 3-day bootcamp covering HTML, CSS, JavaScript, and React.', '2023-08-01', '2023-09-15', 1, 100, '2023-09-15 09:00:00', 'Workshop'),
(14, 1, 'Data Science Conference', 'Annual conference featuring talks on AI, machine learning, and data analytics.', '2023-10-01', '2023-11-10', 1, 300, '2023-11-10 10:00:00', 'Conference'),
(15, 1, 'Git & GitHub Workshop', 'Learn version control and collaboration tools essential for software development.', '2024-09-01', '2024-10-05', 2, 40, '2024-10-05 14:00:00', 'Workshop'),
(16, 1, 'Cybersecurity Seminar', 'Expert talks on network security, ethical hacking, and protecting digital assets.', '2024-08-15', '2024-09-20', 3, 120, '2024-09-20 15:00:00', 'Seminar'),
-- Photography Club Events (including past events)
(5, 2, 'Night Photography Walk', 'Explore the city at night and capture stunning urban photographs.', '2024-11-10', '2024-12-20', 4, 30, '2024-12-20 19:00:00', 'Activity'),
(6, 2, 'Portrait Photography Masterclass', 'Learn professional portrait techniques from award-winning photographer.', '2024-12-05', '2025-01-15', 2, 20, '2025-01-15 13:00:00', 'Workshop'),
(7, 2, 'Annual Photo Exhibition', 'Showcase your best work at our yearly exhibition open to all students.', '2024-11-20', '2025-02-01', 3, 100, '2025-02-01 11:00:00', 'Exhibition'),
(8, 2, 'Landscape Photography Trip', 'Weekend trip to capture beautiful mountain landscapes.', '2024-10-01', '2024-11-15', 4, 15, '2024-11-15 07:00:00', 'Trip'),
(17, 2, 'Street Photography Workshop', 'Learn to capture candid moments and urban life through street photography.', '2023-11-01', '2023-12-10', 8, 25, '2023-12-10 10:00:00', 'Workshop'),
(18, 2, 'Nature Photography Expedition', 'Full-day trip to national park for wildlife and nature photography.', '2024-05-01', '2024-06-15', 4, 20, '2024-06-15 06:00:00', 'Trip'),
(19, 2, 'Studio Lighting Techniques', 'Master professional studio lighting setups for portrait photography.', '2024-07-10', '2024-08-20', 7, 15, '2024-08-20 13:00:00', 'Workshop'),
(20, 2, 'Photo Editing with Lightroom', 'Comprehensive workshop on post-processing and photo editing techniques.', '2024-09-15', '2024-10-25', 2, 30, '2024-10-25 14:00:00', 'Workshop'),
-- Debate Society Events (including past events)
(9, 3, 'Mock UN Conference', 'Simulate United Nations debates on current global issues.', '2024-11-25', '2025-01-25', 1, 100, '2025-01-25 09:00:00', 'Competition'),
(10, 3, 'Public Speaking Workshop', 'Improve your presentation skills with practical exercises and feedback.', '2024-12-10', '2025-01-05', 2, 35, '2025-01-05 14:00:00', 'Workshop'),
(11, 3, 'Inter-University Debate Tournament', 'Compete against debate teams from other universities.', '2024-11-01', '2025-02-10', 1, 80, '2025-02-10 10:00:00', 'Competition'),
(12, 3, 'Critical Thinking Seminar', 'Develop analytical skills essential for effective argumentation.', '2024-10-20', '2024-12-01', 5, 28, '2024-12-01 15:00:00', 'Seminar'),
(21, 3, 'Parliamentary Debate Championship', 'Annual championship tournament with multiple rounds and elimination stages.', '2023-09-15', '2023-10-20', 1, 150, '2023-10-20 09:00:00', 'Competition'),
(22, 3, 'Rhetoric and Persuasion Workshop', 'Learn the art of persuasive speaking and effective communication.', '2024-06-01', '2024-07-10', 2, 40, '2024-07-10 14:00:00', 'Workshop'),
(23, 3, 'Ethics in Argumentation', 'Explore ethical considerations in debate and argumentation practices.', '2024-08-20', '2024-09-25', 5, 30, '2024-09-25 15:00:00', 'Seminar'),
-- Music Society Events (new club)
(24, 4, 'Spring Concert 2024', 'Annual spring concert featuring performances from all music groups.', '2024-02-01', '2024-04-15', 1, 400, '2024-04-15 19:00:00', 'Concert'),
(25, 4, 'Jazz Night', 'Evening of jazz performances by student musicians and guest artists.', '2024-05-10', '2024-06-20', 3, 180, '2024-06-20 20:00:00', 'Concert'),
(26, 4, 'Music Theory Workshop', 'Learn music theory fundamentals for beginners and intermediate musicians.', '2024-09-01', '2024-10-10', 2, 35, '2024-10-10 16:00:00', 'Workshop'),
(27, 4, 'Open Mic Night', 'Showcase your talent at our monthly open mic event. All genres welcome.', '2024-11-01', '2024-12-18', 3, 50, '2024-12-18 19:30:00', 'Activity'),
(28, 4, 'Choir Rehearsal Series', 'Join our choir for weekly rehearsals leading up to the winter concert.', '2024-10-01', '2024-12-20', 7, 60, '2024-12-20 18:00:00', 'Rehearsal'),
-- Sports Club Events (new club)
(29, 5, 'Basketball Tournament', 'Inter-club basketball tournament with teams from all clubs.', '2024-03-01', '2024-04-20', 6, 200, '2024-04-20 10:00:00', 'Competition'),
(30, 5, 'Fitness Bootcamp', 'Intensive fitness training sessions for all fitness levels.', '2024-07-15', '2024-08-30', 6, 80, '2024-08-30 08:00:00', 'Training'),
(31, 5, 'Soccer League Finals', 'Championship match for the semester soccer league.', '2024-11-10', '2024-12-22', 6, 300, '2024-12-22 15:00:00', 'Competition'),
(32, 5, 'Yoga & Meditation Session', 'Relaxing yoga session followed by guided meditation.', '2024-09-20', '2024-11-05', 7, 40, '2024-11-05 17:00:00', 'Activity'),
-- Art & Design Club Events (new club)
(33, 6, 'Art Exhibition Opening', 'Opening night for our semester art exhibition featuring student works.', '2024-04-01', '2024-05-25', 8, 120, '2024-05-25 18:00:00', 'Exhibition'),
(34, 6, 'Digital Art Workshop', 'Learn digital art techniques using Photoshop and Illustrator.', '2024-08-01', '2024-09-15', 7, 25, '2024-09-15 13:00:00', 'Workshop'),
(35, 6, 'Sculpture Making Class', 'Hands-on workshop on creating sculptures with various materials.', '2024-10-15', '2024-11-28', 7, 20, '2024-11-28 14:00:00', 'Workshop'),
(36, 6, 'Art History Lecture Series', 'Monthly lectures on art history from ancient to modern times.', '2024-09-01', '2024-12-15', 2, 45, '2024-12-15 16:00:00', 'Lecture');

-- =============================================
-- INTERACTS_WITH (event interactions - saves and attends with complex relationships)
-- =============================================
INSERT INTO interacts_with (user_id, event_id, interaction_type, interaction_date) VALUES
-- CS Society event interactions
(5, 1, 'attended', '2024-12-15 14:30:00'),
(6, 1, 'attended', '2024-12-15 14:30:00'),
(7, 1, 'attended', '2024-12-15 14:30:00'),
(8, 1, 'saved', '2024-12-10 09:00:00'),
(18, 1, 'attended', '2024-12-15 14:30:00'),
(19, 1, 'saved', '2024-12-12 10:00:00'),
(5, 2, 'saved', '2024-12-01 10:00:00'),
(6, 2, 'attended', '2025-01-20 09:30:00'),
(7, 2, 'attended', '2025-01-20 09:30:00'),
(9, 2, 'saved', '2024-12-20 15:00:00'),
(18, 2, 'saved', '2024-12-25 11:00:00'),
(5, 3, 'saved', '2024-12-15 11:00:00'),
(6, 4, 'attended', '2024-11-20 10:30:00'),
(7, 4, 'attended', '2024-11-20 10:30:00'),
(12, 4, 'attended', '2024-11-20 10:30:00'),
-- Past CS Society events
(5, 13, 'attended', '2023-09-15 09:30:00'),
(6, 13, 'attended', '2023-09-15 09:30:00'),
(7, 13, 'attended', '2023-09-15 09:30:00'),
(8, 13, 'attended', '2023-09-15 09:30:00'),
(5, 14, 'attended', '2023-11-10 10:30:00'),
(6, 14, 'attended', '2023-11-10 10:30:00'),
(7, 14, 'saved', '2023-10-15 14:00:00'),
(6, 15, 'attended', '2024-10-05 14:30:00'),
(7, 15, 'attended', '2024-10-05 14:30:00'),
(18, 15, 'attended', '2024-10-05 14:30:00'),
(5, 16, 'attended', '2024-09-20 15:30:00'),
(6, 16, 'saved', '2024-08-25 10:00:00'),
-- Photography Club event interactions
(8, 5, 'attended', '2024-12-20 19:30:00'),
(9, 5, 'attended', '2024-12-20 19:30:00'),
(5, 5, 'saved', '2024-12-18 08:00:00'),
(20, 5, 'attended', '2024-12-20 19:30:00'),
(21, 5, 'saved', '2024-12-19 09:00:00'),
(8, 6, 'saved', '2025-01-10 12:00:00'),
(9, 6, 'attended', '2025-01-15 13:30:00'),
(20, 6, 'attended', '2025-01-15 13:30:00'),
(10, 7, 'saved', '2025-01-20 09:00:00'),
(8, 8, 'attended', '2024-11-15 07:30:00'),
(9, 8, 'attended', '2024-11-15 07:30:00'),
-- Past Photography Club events
(8, 17, 'attended', '2023-12-10 10:30:00'),
(9, 17, 'attended', '2023-12-10 10:30:00'),
(8, 18, 'attended', '2024-06-15 06:30:00'),
(9, 18, 'attended', '2024-06-15 06:30:00'),
(20, 18, 'attended', '2024-06-15 06:30:00'),
(8, 19, 'attended', '2024-08-20 13:30:00'),
(9, 19, 'saved', '2024-07-20 11:00:00'),
(8, 20, 'attended', '2024-10-25 14:30:00'),
(9, 20, 'attended', '2024-10-25 14:30:00'),
(21, 20, 'attended', '2024-10-25 14:30:00'),
-- Debate Society event interactions
(10, 9, 'attended', '2025-01-25 09:30:00'),
(11, 9, 'attended', '2025-01-25 09:30:00'),
(12, 9, 'saved', '2025-01-20 14:00:00'),
(22, 9, 'saved', '2025-01-22 10:00:00'),
(23, 9, 'attended', '2025-01-25 09:30:00'),
(10, 10, 'attended', '2025-01-05 14:30:00'),
(11, 10, 'attended', '2025-01-05 14:30:00'),
(13, 10, 'saved', '2024-12-28 16:00:00'),
(22, 10, 'attended', '2025-01-05 14:30:00'),
(10, 11, 'saved', '2025-01-15 11:00:00'),
(11, 12, 'attended', '2024-12-01 15:30:00'),
(10, 12, 'attended', '2024-12-01 15:30:00'),
(22, 12, 'attended', '2024-12-01 15:30:00'),
-- Past Debate Society events
(10, 21, 'attended', '2023-10-20 09:30:00'),
(11, 21, 'attended', '2023-10-20 09:30:00'),
(12, 21, 'attended', '2023-10-20 09:30:00'),
(10, 22, 'attended', '2024-07-10 14:30:00'),
(11, 22, 'attended', '2024-07-10 14:30:00'),
(22, 22, 'attended', '2024-07-10 14:30:00'),
(10, 23, 'attended', '2024-09-25 15:30:00'),
(11, 23, 'saved', '2024-08-30 12:00:00'),
-- Music Society event interactions
(5, 24, 'attended', '2024-04-15 19:30:00'),
(7, 24, 'attended', '2024-04-15 19:30:00'),
(12, 24, 'attended', '2024-04-15 19:30:00'),
(18, 24, 'attended', '2024-04-15 19:30:00'),
(24, 24, 'attended', '2024-04-15 19:30:00'),
(5, 25, 'attended', '2024-06-20 20:30:00'),
(7, 25, 'attended', '2024-06-20 20:30:00'),
(12, 25, 'saved', '2024-05-25 14:00:00'),
(5, 26, 'attended', '2024-10-10 16:30:00'),
(7, 26, 'attended', '2024-10-10 16:30:00'),
(18, 26, 'attended', '2024-10-10 16:30:00'),
(5, 27, 'saved', '2024-12-10 10:00:00'),
(7, 27, 'saved', '2024-12-12 11:00:00'),
(12, 27, 'attended', '2024-12-18 19:45:00'),
(5, 28, 'attended', '2024-12-20 18:30:00'),
(7, 28, 'attended', '2024-12-20 18:30:00'),
(18, 28, 'attended', '2024-12-20 18:30:00'),
(24, 28, 'attended', '2024-12-20 18:30:00'),
-- Sports Club event interactions
(6, 29, 'attended', '2024-04-20 10:30:00'),
(13, 29, 'attended', '2024-04-20 10:30:00'),
(14, 29, 'attended', '2024-04-20 10:30:00'),
(19, 29, 'attended', '2024-04-20 10:30:00'),
(20, 29, 'attended', '2024-04-20 10:30:00'),
(6, 30, 'attended', '2024-08-30 08:30:00'),
(13, 30, 'attended', '2024-08-30 08:30:00'),
(14, 30, 'attended', '2024-08-30 08:30:00'),
(19, 30, 'saved', '2024-07-25 09:00:00'),
(6, 31, 'attended', '2024-12-22 15:30:00'),
(13, 31, 'attended', '2024-12-22 15:30:00'),
(14, 31, 'attended', '2024-12-22 15:30:00'),
(19, 31, 'attended', '2024-12-22 15:30:00'),
(20, 31, 'attended', '2024-12-22 15:30:00'),
(6, 32, 'attended', '2024-11-05 17:30:00'),
(13, 32, 'attended', '2024-11-05 17:30:00'),
(14, 32, 'saved', '2024-10-01 10:00:00'),
-- Art & Design Club event interactions
(8, 33, 'attended', '2024-05-25 18:30:00'),
(9, 33, 'attended', '2024-05-25 18:30:00'),
(11, 33, 'attended', '2024-05-25 18:30:00'),
(21, 33, 'attended', '2024-05-25 18:30:00'),
(8, 34, 'attended', '2024-09-15 13:30:00'),
(9, 34, 'attended', '2024-09-15 13:30:00'),
(11, 34, 'saved', '2024-08-15 11:00:00'),
(8, 35, 'saved', '2024-11-20 10:00:00'),
(9, 35, 'attended', '2024-11-28 14:30:00'),
(11, 35, 'attended', '2024-11-28 14:30:00'),
(21, 35, 'attended', '2024-11-28 14:30:00'),
(8, 36, 'attended', '2024-12-15 16:30:00'),
(9, 36, 'attended', '2024-12-15 16:30:00'),
(11, 36, 'saved', '2024-11-25 12:00:00');

-- =============================================
-- FOLLOWS (users following clubs with complex cross-club relationships)
-- =============================================
INSERT INTO follows (user_id, club_id, follow_start_date) VALUES
-- Users following CS Society
(5, 1, '2024-02-01'),
(6, 1, '2024-02-03'),
(7, 1, '2024-02-10'),
(8, 1, '2024-03-01'),
(12, 1, '2024-11-01'),
(13, 1, '2024-11-15'),
(18, 1, '2024-04-05'),
(19, 1, '2024-04-28'),
(20, 1, '2024-05-15'),
-- Users following Photography Club
(8, 2, '2024-02-20'),
(9, 2, '2024-02-25'),
(5, 2, '2024-03-15'),
(14, 2, '2024-12-01'),
(20, 2, '2024-04-10'),
(21, 2, '2024-05-05'),
(22, 2, '2024-05-20'),
-- Users following Debate Society
(10, 3, '2024-03-01'),
(11, 3, '2024-03-10'),
(12, 3, '2024-04-01'),
(13, 3, '2024-04-15'),
(14, 3, '2024-05-01'),
(22, 3, '2024-04-15'),
(23, 3, '2024-05-10'),
(24, 3, '2024-05-25'),
-- Users following Music Society
(5, 4, '2024-03-15'),
(7, 4, '2024-03-25'),
(12, 4, '2024-04-05'),
(18, 4, '2024-04-25'),
(24, 4, '2024-05-15'),
(6, 4, '2024-06-01'),
(8, 4, '2024-06-10'),
(13, 4, '2024-06-20'),
-- Users following Sports Club
(6, 5, '2024-03-20'),
(13, 5, '2024-04-01'),
(14, 5, '2024-04-10'),
(19, 5, '2024-05-01'),
(20, 5, '2024-05-05'),
(5, 5, '2024-05-15'),
(7, 5, '2024-05-20'),
(21, 5, '2024-05-25'),
-- Users following Art & Design Club
(8, 6, '2024-03-25'),
(9, 6, '2024-04-05'),
(11, 6, '2024-04-15'),
(21, 6, '2024-05-10'),
(5, 6, '2024-05-20'),
(12, 6, '2024-05-25'),
(14, 6, '2024-06-01'),
(18, 6, '2024-06-05');

-- =============================================
-- BUDGET TRANSACTIONS (45 transactions across all clubs)
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
(25, 1, 1500.00, '2023-08-15', 'INCOME', 'Web Development Bootcamp fees'),
(26, 1, 2500.00, '2023-10-01', 'INCOME', 'Data Science Conference sponsorships'),
(27, 1, 800.00, '2023-09-01', 'EXPENSE', 'Bootcamp venue and equipment'),
(28, 1, 1200.00, '2023-11-05', 'EXPENSE', 'Conference speaker fees'),
(29, 1, 400.00, '2024-09-25', 'EXPENSE', 'Git workshop materials'),
(30, 1, 600.00, '2024-08-20', 'EXPENSE', 'Cybersecurity seminar venue'),
-- Photography Club transactions
(8, 2, 3000.00, '2024-09-01', 'INCOME', 'University funding allocation'),
(9, 2, 1500.00, '2024-09-20', 'INCOME', 'Equipment rental revenue'),
(10, 2, 2000.00, '2024-10-10', 'EXPENSE', 'New camera equipment'),
(11, 2, 400.00, '2024-11-01', 'EXPENSE', 'Exhibition printing costs'),
(12, 2, 600.00, '2024-11-20', 'EXPENSE', 'Transportation for photo trip'),
(13, 2, 1000.00, '2024-12-05', 'INCOME', 'Workshop registration fees'),
(31, 2, 800.00, '2023-11-15', 'INCOME', 'Street Photography Workshop fees'),
(32, 2, 500.00, '2023-12-05', 'EXPENSE', 'Workshop instructor fee'),
(33, 2, 1200.00, '2024-05-20', 'INCOME', 'Nature Photography Trip fees'),
(34, 2, 800.00, '2024-06-10', 'EXPENSE', 'Transportation and accommodation'),
(35, 2, 600.00, '2024-08-05', 'EXPENSE', 'Studio lighting equipment rental'),
(36, 2, 400.00, '2024-10-20', 'EXPENSE', 'Lightroom workshop software licenses'),
-- Debate Society transactions
(14, 3, 4000.00, '2024-09-01', 'INCOME', 'University funding allocation'),
(15, 3, 2500.00, '2024-09-25', 'INCOME', 'Tournament sponsorship'),
(16, 3, 1000.00, '2024-10-15', 'EXPENSE', 'Tournament venue booking'),
(17, 3, 500.00, '2024-11-01', 'EXPENSE', 'Judge honorariums'),
(18, 3, 300.00, '2024-11-20', 'EXPENSE', 'Printing and materials'),
(19, 3, 1500.00, '2024-12-01', 'INCOME', 'Mock UN registration fees'),
(20, 3, 700.00, '2024-12-10', 'EXPENSE', 'Catering for workshop'),
(37, 3, 3000.00, '2023-09-20', 'INCOME', 'Parliamentary Debate Championship fees'),
(38, 3, 1500.00, '2023-10-15', 'EXPENSE', 'Championship venue and judges'),
(39, 3, 450.00, '2024-07-05', 'EXPENSE', 'Rhetoric workshop materials'),
(40, 3, 350.00, '2024-09-20', 'EXPENSE', 'Ethics seminar speaker fee'),
-- Music Society transactions
(41, 4, 4000.00, '2024-09-01', 'INCOME', 'University funding allocation'),
(42, 4, 2500.00, '2024-03-20', 'INCOME', 'Spring Concert ticket sales'),
(43, 4, 1200.00, '2024-04-10', 'EXPENSE', 'Concert venue and sound equipment'),
(44, 4, 1800.00, '2024-05-25', 'INCOME', 'Jazz Night ticket sales'),
(45, 4, 900.00, '2024-06-15', 'EXPENSE', 'Jazz Night venue and musicians'),
(46, 4, 500.00, '2024-09-15', 'EXPENSE', 'Music Theory Workshop materials'),
(47, 4, 600.00, '2024-12-10', 'INCOME', 'Open Mic Night entry fees'),
(48, 4, 300.00, '2024-12-15', 'EXPENSE', 'Open Mic equipment rental'),
-- Sports Club transactions
(49, 5, 6000.00, '2024-09-01', 'INCOME', 'University funding allocation'),
(50, 5, 2000.00, '2024-03-15', 'INCOME', 'Basketball Tournament registration fees'),
(51, 5, 1200.00, '2024-04-15', 'EXPENSE', 'Tournament equipment and referees'),
(52, 5, 1500.00, '2024-07-20', 'INCOME', 'Fitness Bootcamp registration fees'),
(53, 5, 800.00, '2024-08-25', 'EXPENSE', 'Bootcamp trainer fees'),
(54, 5, 2500.00, '2024-11-25', 'INCOME', 'Soccer League Finals ticket sales'),
(55, 5, 1000.00, '2024-12-18', 'EXPENSE', 'Finals venue and equipment'),
(56, 5, 400.00, '2024-10-30', 'EXPENSE', 'Yoga session instructor fee'),
-- Art & Design Club transactions
(57, 6, 3500.00, '2024-09-01', 'INCOME', 'University funding allocation'),
(58, 6, 1500.00, '2024-04-20', 'INCOME', 'Art Exhibition entry fees'),
(59, 6, 800.00, '2024-05-20', 'EXPENSE', 'Exhibition space and materials'),
(60, 6, 600.00, '2024-08-15', 'EXPENSE', 'Digital Art Workshop software licenses'),
(61, 6, 500.00, '2024-10-25', 'EXPENSE', 'Sculpture Making Class materials'),
(62, 6, 400.00, '2024-11-20', 'EXPENSE', 'Art History Lecture Series speaker fees'),
(63, 6, 800.00, '2024-12-01', 'INCOME', 'Workshop registration fees');

-- =============================================
-- CLUB_FOLLOWERS (legacy table - users following clubs)
-- =============================================
INSERT INTO club_followers (user_id, club_id, followed_at) VALUES
-- Users following CS Society
(5, 1, '2024-02-01 10:00:00'),
(6, 1, '2024-02-03 14:30:00'),
(7, 1, '2024-02-10 09:15:00'),
(8, 1, '2024-03-01 16:45:00'),
(18, 1, '2024-04-05 11:00:00'),
(19, 1, '2024-04-28 14:20:00'),
-- Users following Photography Club
(8, 2, '2024-02-20 11:20:00'),
(9, 2, '2024-02-25 13:10:00'),
(5, 2, '2024-03-15 10:30:00'),
(20, 2, '2024-04-10 09:45:00'),
(21, 2, '2024-05-05 15:30:00'),
-- Users following Debate Society
(10, 3, '2024-03-01 15:00:00'),
(11, 3, '2024-03-10 12:00:00'),
(12, 3, '2024-04-01 09:30:00'),
(22, 3, '2024-04-15 13:15:00'),
(23, 3, '2024-05-10 10:45:00'),
-- Users following Music Society
(5, 4, '2024-03-15 14:00:00'),
(7, 4, '2024-03-25 11:30:00'),
(12, 4, '2024-04-05 16:20:00'),
-- Users following Sports Club
(6, 5, '2024-03-20 09:00:00'),
(13, 5, '2024-04-01 13:45:00'),
(14, 5, '2024-04-10 10:15:00'),
-- Users following Art & Design Club
(8, 6, '2024-03-25 15:30:00'),
(9, 6, '2024-04-05 11:00:00'),
(11, 6, '2024-04-15 14:20:00');

-- =============================================
-- EVENT_SAVES (users saving events for later with complex patterns)
-- =============================================
INSERT INTO event_saves (user_id, event_id, saved_at) VALUES
-- CS Society event saves
(8, 1, '2024-12-10 09:00:00'),
(5, 2, '2024-12-01 10:00:00'),
(9, 2, '2024-12-20 15:00:00'),
(5, 3, '2024-12-15 11:00:00'),
(19, 1, '2024-12-12 10:00:00'),
(18, 2, '2024-12-25 11:00:00'),
(6, 16, '2024-08-25 10:00:00'),
(7, 14, '2023-10-15 14:00:00'),
-- Photography Club event saves
(5, 5, '2024-12-18 08:00:00'),
(8, 6, '2025-01-10 12:00:00'),
(10, 7, '2025-01-20 09:00:00'),
(21, 5, '2024-12-19 09:00:00'),
(9, 19, '2024-07-20 11:00:00'),
-- Debate Society event saves
(12, 9, '2025-01-20 14:00:00'),
(13, 10, '2024-12-28 16:00:00'),
(10, 11, '2025-01-15 11:00:00'),
(22, 9, '2025-01-22 10:00:00'),
(11, 23, '2024-08-30 12:00:00'),
-- Music Society event saves
(12, 25, '2024-05-25 14:00:00'),
(5, 27, '2024-12-10 10:00:00'),
(7, 27, '2024-12-12 11:00:00'),
-- Sports Club event saves
(19, 30, '2024-07-25 09:00:00'),
(14, 32, '2024-10-01 10:00:00'),
-- Art & Design Club event saves
(8, 35, '2024-11-20 10:00:00'),
(11, 34, '2024-08-15 11:00:00'),
(11, 36, '2024-11-25 12:00:00');

-- =============================================
-- EVENT_ATTENDANCE (users attending events including past events)
-- =============================================
INSERT INTO event_attendance (user_id, event_id, attended_at) VALUES
-- CS Society event attendance
(5, 1, '2024-12-15 14:30:00'),
(6, 1, '2024-12-15 14:30:00'),
(7, 1, '2024-12-15 14:30:00'),
(18, 1, '2024-12-15 14:30:00'),
(6, 2, '2025-01-20 09:30:00'),
(7, 2, '2025-01-20 09:30:00'),
(6, 4, '2024-11-20 10:30:00'),
(7, 4, '2024-11-20 10:30:00'),
(12, 4, '2024-11-20 10:30:00'),
-- Past CS Society events
(5, 13, '2023-09-15 09:30:00'),
(6, 13, '2023-09-15 09:30:00'),
(7, 13, '2023-09-15 09:30:00'),
(8, 13, '2023-09-15 09:30:00'),
(5, 14, '2023-11-10 10:30:00'),
(6, 14, '2023-11-10 10:30:00'),
(6, 15, '2024-10-05 14:30:00'),
(7, 15, '2024-10-05 14:30:00'),
(18, 15, '2024-10-05 14:30:00'),
(5, 16, '2024-09-20 15:30:00'),
-- Photography Club event attendance
(8, 5, '2024-12-20 19:30:00'),
(9, 5, '2024-12-20 19:30:00'),
(20, 5, '2024-12-20 19:30:00'),
(9, 6, '2025-01-15 13:30:00'),
(20, 6, '2025-01-15 13:30:00'),
(8, 8, '2024-11-15 07:30:00'),
(9, 8, '2024-11-15 07:30:00'),
-- Past Photography Club events
(8, 17, '2023-12-10 10:30:00'),
(9, 17, '2023-12-10 10:30:00'),
(8, 18, '2024-06-15 06:30:00'),
(9, 18, '2024-06-15 06:30:00'),
(20, 18, '2024-06-15 06:30:00'),
(8, 19, '2024-08-20 13:30:00'),
(8, 20, '2024-10-25 14:30:00'),
(9, 20, '2024-10-25 14:30:00'),
(21, 20, '2024-10-25 14:30:00'),
-- Debate Society event attendance
(10, 9, '2025-01-25 09:30:00'),
(11, 9, '2025-01-25 09:30:00'),
(23, 9, '2025-01-25 09:30:00'),
(10, 10, '2025-01-05 14:30:00'),
(11, 10, '2025-01-05 14:30:00'),
(22, 10, '2025-01-05 14:30:00'),
(11, 12, '2024-12-01 15:30:00'),
(10, 12, '2024-12-01 15:30:00'),
(22, 12, '2024-12-01 15:30:00'),
-- Past Debate Society events
(10, 21, '2023-10-20 09:30:00'),
(11, 21, '2023-10-20 09:30:00'),
(12, 21, '2023-10-20 09:30:00'),
(10, 22, '2024-07-10 14:30:00'),
(11, 22, '2024-07-10 14:30:00'),
(22, 22, '2024-07-10 14:30:00'),
(10, 23, '2024-09-25 15:30:00'),
-- Music Society event attendance
(5, 24, '2024-04-15 19:30:00'),
(7, 24, '2024-04-15 19:30:00'),
(12, 24, '2024-04-15 19:30:00'),
(18, 24, '2024-04-15 19:30:00'),
(24, 24, '2024-04-15 19:30:00'),
(5, 25, '2024-06-20 20:30:00'),
(7, 25, '2024-06-20 20:30:00'),
(5, 26, '2024-10-10 16:30:00'),
(7, 26, '2024-10-10 16:30:00'),
(18, 26, '2024-10-10 16:30:00'),
(12, 27, '2024-12-18 19:45:00'),
(5, 28, '2024-12-20 18:30:00'),
(7, 28, '2024-12-20 18:30:00'),
(18, 28, '2024-12-20 18:30:00'),
(24, 28, '2024-12-20 18:30:00'),
-- Sports Club event attendance
(6, 29, '2024-04-20 10:30:00'),
(13, 29, '2024-04-20 10:30:00'),
(14, 29, '2024-04-20 10:30:00'),
(19, 29, '2024-04-20 10:30:00'),
(20, 29, '2024-04-20 10:30:00'),
(6, 30, '2024-08-30 08:30:00'),
(13, 30, '2024-08-30 08:30:00'),
(14, 30, '2024-08-30 08:30:00'),
(6, 31, '2024-12-22 15:30:00'),
(13, 31, '2024-12-22 15:30:00'),
(14, 31, '2024-12-22 15:30:00'),
(19, 31, '2024-12-22 15:30:00'),
(20, 31, '2024-12-22 15:30:00'),
(6, 32, '2024-11-05 17:30:00'),
(13, 32, '2024-11-05 17:30:00'),
-- Art & Design Club event attendance
(8, 33, '2024-05-25 18:30:00'),
(9, 33, '2024-05-25 18:30:00'),
(11, 33, '2024-05-25 18:30:00'),
(21, 33, '2024-05-25 18:30:00'),
(8, 34, '2024-09-15 13:30:00'),
(9, 34, '2024-09-15 13:30:00'),
(9, 35, '2024-11-28 14:30:00'),
(11, 35, '2024-11-28 14:30:00'),
(21, 35, '2024-11-28 14:30:00'),
(8, 36, '2024-12-15 16:30:00'),
(9, 36, '2024-12-15 16:30:00');

-- =============================================
-- EVENT_MODIFICATIONS (audit trail for event changes)
-- =============================================
INSERT INTO event_modifications (modification_id, event_id, modification_type, modification_date, description, modified_by_user_id) VALUES
-- Event updates
(1, 1, 'UPDATE', '2024-11-05 10:00:00', 'Updated event description and added more details about ML topics', 2),
(2, 2, 'UPDATE', '2024-11-20 14:30:00', 'Changed venue capacity and updated prize information', 2),
(3, 5, 'UPDATE', '2024-11-15 09:00:00', 'Updated meeting location and time for night photography walk', 3),
(4, 9, 'UPDATE', '2024-12-01 11:00:00', 'Added new debate topics and updated schedule', 4),
(7, 13, 'UPDATE', '2023-08-20 14:00:00', 'Updated bootcamp schedule and added new topics', 2),
(8, 14, 'UPDATE', '2023-10-15 10:00:00', 'Added new speakers and updated conference agenda', 2),
(9, 17, 'UPDATE', '2023-11-25 11:00:00', 'Changed workshop location to outdoor venue', 3),
(10, 24, 'UPDATE', '2024-03-20 15:00:00', 'Updated concert program and added new performers', 15),
(11, 29, 'UPDATE', '2024-03-25 09:00:00', 'Adjusted tournament schedule and bracket', 16),
(12, 33, 'UPDATE', '2024-04-20 16:00:00', 'Extended exhibition dates and added new artworks', 17),
-- Event deletions (soft deletes)
(5, 4, 'DELETE', '2024-11-25 16:00:00', 'Event cancelled due to low registration', 2),
(6, 8, 'DELETE', '2024-11-10 13:00:00', 'Trip postponed to next semester', 3),
(13, 18, 'DELETE', '2024-06-10 10:00:00', 'Trip cancelled due to weather conditions', 3),
(14, 32, 'DELETE', '2024-11-01 12:00:00', 'Yoga session cancelled, instructor unavailable', 16);
