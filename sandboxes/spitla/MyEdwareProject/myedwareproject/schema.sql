CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(100) NOT NULL,
    closed BOOL NOT NULL
);

INSERT OR IGNORE INTO tasks (id, name, closed) VALUES (1, 'Start learning Pyramid', 0);
INSERT OR IGNORE INTO tasks (id, name, closed) VALUES (2, 'Do quick tutorial', 0);
INSERT OR IGNORE INTO tasks (id, name, closed) VALUES (3, 'Have some beer!', 0);
