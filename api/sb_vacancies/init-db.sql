-- init-db-clean.sql (только таблицы без тестовых данных)

-- 1. Таблица категорий
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 2. Таблица подкатегорий
CREATE TABLE IF NOT EXISTS subcategories (
    id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- 3. Таблица вакансий
CREATE TABLE IF NOT EXISTS vacancies (
    id SERIAL PRIMARY KEY,
    subcategory_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    employment_type VARCHAR(50),
    experience_required VARCHAR(50),
    schedule VARCHAR(100),
    salary_from DECIMAL(10, 2),
    salary_to DECIMAL(10, 2),
    salary_period VARCHAR(20),
    company_name VARCHAR(200),
    requirements TEXT,
    responsibilities TEXT,
    benefits TEXT,
    views_count VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (subcategory_id) REFERENCES subcategories(id) ON DELETE CASCADE
);

-- Базовые индексы
CREATE INDEX IF NOT EXISTS idx_categories_name ON categories(name);
CREATE INDEX IF NOT EXISTS idx_subcategories_category_id ON subcategories(category_id);
CREATE INDEX IF NOT EXISTS idx_subcategories_name ON subcategories(name);
CREATE INDEX IF NOT EXISTS idx_vacancies_subcategory_id ON vacancies(subcategory_id);
CREATE INDEX IF NOT EXISTS idx_vacancies_title ON vacancies(title);
CREATE INDEX IF NOT EXISTS idx_vacancies_created_at ON vacancies(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_vacancies_company_name ON vacancies(company_name);