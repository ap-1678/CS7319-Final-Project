PRAGMA foreign_keys = ON;

-- Wipe & reset AUTOINCREMENT counters
DELETE FROM subtasks;
DELETE FROM tasks;
DELETE FROM sqlite_sequence WHERE name IN ('tasks','subtasks');

-- 1) Write report (in progress)
INSERT INTO tasks (title, description, due_date, created_at, completed)
VALUES ('Write report', 'Methods section for CS7319', '2025-11-15', strftime('%s','2025-09-05 10:45:00'), 0);
WITH t AS (SELECT last_insert_rowid() AS tid)
INSERT INTO subtasks (task_id, title, done)
SELECT tid, 'Outline', 0 FROM t
UNION ALL SELECT tid, 'Draft', 0 FROM t
UNION ALL SELECT tid, 'Edit', 0 FROM t;

-- 2) Grocery run (completed, no subtasks)
INSERT INTO tasks (title, description, due_date, created_at, completed)
VALUES ('Grocery run', 'Milk, eggs, coffee', '2025-11-10', strftime('%s','2025-09-10 13:00:00'), 1);

-- 3) Build UI (in progress)
INSERT INTO tasks (title, description, due_date, created_at, completed)
VALUES ('Build UI', 'Navbar + Search box + Results', '2025-11-20', strftime('%s','2025-09-15 09:30:00'), 0);
WITH t AS (SELECT last_insert_rowid() AS tid)
INSERT INTO subtasks (task_id, title, done)
SELECT tid, 'Navbar', 1 FROM t
UNION ALL SELECT tid, 'Search box', 0 FROM t
UNION ALL SELECT tid, 'Results list', 0 FROM t;

-- 4) Gym session (completed via subtasks)
INSERT INTO tasks (title, description, due_date, created_at, completed)
VALUES ('Gym session', 'Leg day routine', NULL, strftime('%s','2025-09-22 07:15:00'), 0);
WITH t AS (SELECT last_insert_rowid() AS tid)
INSERT INTO subtasks (task_id, title, done)
SELECT tid, 'Squats', 1 FROM t
UNION ALL SELECT tid, 'Leg press', 1 FROM t;

-- 5) Presentation prep (in progress)
INSERT INTO tasks (title, description, due_date, created_at, completed)
VALUES ('Presentation prep', 'Slides for final project', '2025-11-25', strftime('%s','2025-10-01 16:00:00'), 0);
WITH t AS (SELECT last_insert_rowid() AS tid)
INSERT INTO subtasks (task_id, title, done)
SELECT tid, 'Slide design', 1 FROM t
UNION ALL SELECT tid, 'Practice', 0 FROM t;

-- 6) Dentist appointment (completed, no subtasks)
INSERT INTO tasks (title, description, due_date, created_at, completed)
VALUES ('Dentist appointment', 'Routine cleaning and x-rays', '2025-11-12', strftime('%s','2025-08-28 14:20:00'), 1);

-- 7) Blog article (in progress)
INSERT INTO tasks (title, description, due_date, created_at, completed)
VALUES ('Blog article', 'Draft technical post about FastAPI microservices', '2025-11-18', strftime('%s','2025-10-05 18:00:00'), 0);
WITH t AS (SELECT last_insert_rowid() AS tid)
INSERT INTO subtasks (task_id, title, done)
SELECT tid, 'Outline', 1 FROM t
UNION ALL SELECT tid, 'Write draft', 0 FROM t
UNION ALL SELECT tid, 'Review', 0 FROM t;

-- 8) Backup system test (completed, no subtasks)
INSERT INTO tasks (title, description, due_date, created_at, completed)
VALUES ('Backup system test', 'Verify automated nightly backups', '2025-11-09', strftime('%s','2025-10-10 11:45:00'), 1);
