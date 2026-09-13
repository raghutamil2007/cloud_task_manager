CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE
);

INSERT INTO tasks (title, completed)
VALUES
('Learn Docker', false),
('Learn AWS EC2', false),
('Build CI/CD Pipeline', false);