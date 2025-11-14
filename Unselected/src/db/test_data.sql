-- Clear existing data
DELETE FROM subtasks;
DELETE FROM tasks;

-- 1) Research Paper (in progress)
INSERT INTO tasks (title, description, due_date, created_at, completed)
VALUES ('Research Paper', 'Finalize literature review and analysis section', '2025-11-20', strftime('%s','2025-08-02 10:30:00'), 0);
INSERT INTO subtasks (task_id, title, done) VALUES
  (1,'Literature review',1),
  (1,'Data analysis',0),
  (1,'Conclusion draft',0);

-- 2) Gym Routine (completed)
INSERT INTO tasks (title, description, due_date, created_at, completed)
VALUES ('Gym Routine', 'Leg day and cardio training', '2025-11-10', strftime('%s','2025-07-15 08:00:00'), 0);
INSERT INTO subtasks (task_id, title, done) VALUES
  (2,'Squats',1),
  (2,'Lunges',1),
  (2,'Cardio',1);

-- 3) Grocery Shopping (completed - no subtasks)
INSERT INTO tasks (title, description, due_date, created_at, completed)
VALUES ('Grocery Shopping', 'Buy essentials for the week', '2025-11-09', strftime('%s','2025-09-01 12:15:00'), 1);

-- 4) Project Deployment (in progress)
INSERT INTO tasks (title, description, due_date, created_at, completed)
VALUES ('Project Deployment', 'Deploy latest FastAPI microservice architecture', '2025-11-22', strftime('%s','2025-10-01 09:45:00'), 0);
INSERT INTO subtasks (task_id, title, done) VALUES
  (4,'Prepare Dockerfile',1),
  (4,'Test endpoints',0),
  (4,'Push to server',0);

-- 5) Vacation Planning (completed)
INSERT INTO tasks (title, description, due_date, created_at, completed)
VALUES ('Vacation Planning', 'Book flights and hotel for December trip', '2025-12-01', strftime('%s','2025-09-20 18:20:00'), 0);
INSERT INTO subtasks (task_id, title, done) VALUES
  (5,'Book flights',1),
  (5,'Reserve hotel',1),
  (5,'Plan itinerary',1);

-- 6) Code Review (in progress)
INSERT INTO tasks (title, description, due_date, created_at, completed)
VALUES ('Code Review', 'Review PRs for the data pipeline project', '2025-11-11', strftime('%s','2025-10-05 15:10:00'), 0);
INSERT INTO subtasks (task_id, title, done) VALUES
  (6,'Review ETL scripts',1),
  (6,'Check model performance',0),
  (6,'Write feedback',0);

-- 7) Dentist Appointment (completed - no subtasks)
INSERT INTO tasks (title, description, due_date, created_at, completed)
VALUES ('Dentist Appointment', 'Routine cleaning and x-rays', '2025-11-15', strftime('%s','2025-08-15 11:40:00'), 1);

-- 8) Write Blog Post (in progress)
INSERT INTO tasks (title, description, due_date, created_at, completed)
VALUES ('Write Blog Post', 'Draft technical blog about Python microservices', '2025-11-18', strftime('%s','2025-10-25 17:25:00'), 0);
INSERT INTO subtasks (task_id, title, done) VALUES
  (8,'Outline topics',1),
  (8,'Write intro',0),
  (8,'Edit post',0);
