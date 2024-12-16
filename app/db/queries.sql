-- Таблица для топ-100 репозиториев
CREATE TABLE IF NOT EXISTS top100 (
    repo VARCHAR(255),
    owner VARCHAR(255),
    position_cur INT,
    position_prev INT,
    stars INT,
    watchers INT,
    forks INT,
    open_issues INT,
    language VARCHAR(255)
);

-- Таблица для активности
CREATE TABLE IF NOT EXISTS activity (
    date DATE,
    repo VARCHAR(255),
    owner VARCHAR(255),
    commits INT,
    authors TEXT[]
);