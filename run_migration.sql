-- Run this in your Supabase SQL editor to add goal_date column

-- Add goal_date column to settings table
ALTER TABLE settings ADD COLUMN IF NOT EXISTS goal_date DATE DEFAULT '2025-12-31';

-- Update existing records to have a default goal date if they don't have one
UPDATE settings SET goal_date = '2025-12-31' WHERE goal_date IS NULL;

-- Verify the column was added
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'settings' AND column_name = 'goal_date';
