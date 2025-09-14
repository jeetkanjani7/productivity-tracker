-- Migration to add goal_date column to settings table
-- Run this in your Supabase SQL editor

-- Add goal_date column to settings table
ALTER TABLE settings ADD COLUMN IF NOT EXISTS goal_date DATE DEFAULT '2025-12-31';

-- Update existing records to have a default goal date if they don't have one
UPDATE settings SET goal_date = '2025-12-31' WHERE goal_date IS NULL;
