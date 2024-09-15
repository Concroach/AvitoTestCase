CREATE TABLE employee (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TYPE organization_type AS ENUM (
    'IE',  -- Индивидуальный предприниматель
    'LLC', -- ООО (Общество с ограниченной ответственностью)
    'JSC'  -- АО (Акционерное общество)
);

CREATE TABLE organization (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    type organization_type,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE organization_responsible (
    id SERIAL PRIMARY KEY,
    organization_id INT REFERENCES organization(id) ON DELETE CASCADE,
    user_id INT REFERENCES employee(id) ON DELETE CASCADE
);

CREATE TABLE tender (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    service_type VARCHAR(100) NOT NULL,  -- Тип услуги (например, Construction)
    status VARCHAR(50) NOT NULL,         -- Статусы тендера (CREATED, PUBLISHED, CLOSED и т.д.)
    version INT DEFAULT 1,               -- Версия тендера
    organization_id INT REFERENCES organization(id) ON DELETE CASCADE,
    creator_username VARCHAR(50) REFERENCES employee(username) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bid (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL,         -- Статусы предложений (CREATED, PUBLISHED, CANCELED и т.д.)
    version INT DEFAULT 1,               -- Версия предложения
    tender_id INT REFERENCES tender(id) ON DELETE CASCADE,
    organization_id INT REFERENCES organization(id) ON DELETE CASCADE,
    creator_username VARCHAR(50) REFERENCES employee(username) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE review (
    id SERIAL PRIMARY KEY,
    bid_id INT REFERENCES bid(id) ON DELETE CASCADE,
    author_username VARCHAR(50) REFERENCES employee(username) ON DELETE CASCADE,
    content TEXT NOT NULL,  -- Текст отзыва
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Заполенние базы данных для тестов
-- Пользователь
INSERT INTO employee (username, first_name, last_name) VALUES ('user1', 'John', 'Doe');

-- Организация
INSERT INTO organization (name, description, type) VALUES ('TechCorp', 'IT Company', 'LLC');

-- Ответственный за организацию
INSERT INTO organization_responsible (organization_id, user_id) VALUES (1, 1);

-- Тендер
INSERT INTO tender (name, description, service_type, status, organization_id, creator_username) 
VALUES ('Тендер 1', 'Описание тендера', 'Construction', 'CREATED', 1, 'user1');

-- Предложение
INSERT INTO bid (name, description, status, tender_id, organization_id, creator_username) 
VALUES ('Предложение 1', 'Описание предложения', 'CREATED', 1, 1, 'user1');

-- Отзыв
INSERT INTO review (bid_id, author_username, content) 
VALUES (1, 'user1', 'Отличное предложение!');
