-- =============================================
-- MIGRATION SCRIPT: Remove Database Triggers
-- =============================================
-- This script removes all 4 triggers from the database.
-- The validation logic has been moved to application code.
-- Run this script on existing databases to remove triggers.
-- =============================================

USE club_management;

-- Drop Trigger 1: Prevent saving events that user is attending
DROP TRIGGER IF EXISTS trg_block_save_if_attending;

-- Drop Trigger 2: Prevent attending events that user has saved
DROP TRIGGER IF EXISTS trg_block_attend_if_saved;

-- Drop Trigger 3: Block membership requests for official clubs and enforce single membership
DROP TRIGGER IF EXISTS trg_block_official_membership_request;

-- Drop Trigger 4: Validate approval of membership requests
DROP TRIGGER IF EXISTS trg_block_approve_if_member_or_official;

-- =============================================
-- Migration Complete
-- =============================================
-- All triggers have been removed. Validation is now handled
-- in the application code:
-- - Event.save_event() checks if user is attending
-- - Event.attend_event() checks if user has saved
-- - Club.create_membership_request() validates membership requests
-- - ClubManager.approve_request() validates approval requests
-- =============================================




