-- init-db.sql
-- Инициализация базы данных для сервиса sb_services
-- Создан на основе миграции Alembic dc3fba90ce81

-- Сначала удаляем существующие таблицы в правильном порядке (если они есть)
DROP TABLE IF EXISTS se_services CASCADE;
DROP TABLE IF EXISTS subcategories CASCADE;
DROP TABLE IF EXISTS categories CASCADE;

-- Таблица categories (категории услуг)
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE categories IS 'Основные категории услуг';
COMMENT ON COLUMN categories.id IS 'Уникальный идентификатор категории';
COMMENT ON COLUMN categories.name IS 'Название категории (уникальное)';
COMMENT ON COLUMN categories.description IS 'Описание категории (уникальное)';
COMMENT ON COLUMN categories.created_at IS 'Дата и время создания записи';
COMMENT ON COLUMN categories.updated_at IS 'Дата и время последнего обновления';

-- Таблица subcategories (подкатегории услуг)
CREATE TABLE subcategories (
    id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    -- Внешний ключ на таблицу categories
    CONSTRAINT fk_subcategories_category
        FOREIGN KEY (category_id)
        REFERENCES categories(id)
        ON DELETE CASCADE
);

COMMENT ON TABLE subcategories IS 'Подкатегории услуг, принадлежащие категориям';
COMMENT ON COLUMN subcategories.id IS 'Уникальный идентификатор подкатегории';
COMMENT ON COLUMN subcategories.category_id IS 'Ссылка на родительскую категорию';
COMMENT ON COLUMN subcategories.name IS 'Название подкатегории';
COMMENT ON COLUMN subcategories.description IS 'Описание подкатегории';
COMMENT ON COLUMN subcategories.created_at IS 'Дата и время создания записи';
COMMENT ON COLUMN subcategories.updated_at IS 'Дата и время последнего обновления';

-- Индекс для ускорения поиска подкатегорий по категории
CREATE INDEX idx_subcategories_category_id ON subcategories(category_id);

-- Таблица se_services (услуги/сервисы)
CREATE TABLE se_services (
    id SERIAL PRIMARY KEY,
    subcategory_id INTEGER NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2),
    currency VARCHAR(3) NOT NULL,
    status VARCHAR(20) NOT NULL,
    views_count INTEGER NOT NULL DEFAULT 0,
    location VARCHAR(200),
    experience_years INTEGER,
    portfolio_url VARCHAR(500),
    availability VARCHAR(100),
    min_duration_hours INTEGER,
    max_duration_hours INTEGER,
    has_guarantee BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    -- Внешний ключ на таблицу subcategories
    CONSTRAINT fk_se_services_subcategory
        FOREIGN KEY (subcategory_id)
        REFERENCES subcategories(id)
        ON DELETE CASCADE
);

COMMENT ON TABLE se_services IS 'Конкретные услуги/сервисы';
COMMENT ON COLUMN se_services.id IS 'Уникальный идентификатор услуги';
COMMENT ON COLUMN se_services.subcategory_id IS 'Ссылка на подкатегорию';
COMMENT ON COLUMN se_services.name IS 'Название услуги';
COMMENT ON COLUMN se_services.description IS 'Подробное описание услуги';
COMMENT ON COLUMN se_services.price IS 'Цена услуги (точность: 10 цифр, 2 после запятой)';
COMMENT ON COLUMN se_services.currency IS 'Валюта (3 символа, например: USD, EUR, BYN, RUB)';
COMMENT ON COLUMN se_services.status IS 'Статус услуги (active, inactive, draft и т.д.)';
COMMENT ON COLUMN se_services.views_count IS 'Количество просмотров услуги';
COMMENT ON COLUMN se_services.location IS 'Местоположение (город, страна)';
COMMENT ON COLUMN se_services.experience_years IS 'Опыт работы в годах';
COMMENT ON COLUMN se_services.portfolio_url IS 'Ссылка на портфолио';
COMMENT ON COLUMN se_services.availability IS 'Доступность (available, busy, on_vacation и т.д.)';
COMMENT ON COLUMN se_services.min_duration_hours IS 'Минимальная продолжительность работы (часы)';
COMMENT ON COLUMN se_services.max_duration_hours IS 'Максимальная продолжительность работы (часы)';
COMMENT ON COLUMN se_services.has_guarantee IS 'Флаг наличия гарантии на услугу';
COMMENT ON COLUMN se_services.created_at IS 'Дата и время создания записи';
COMMENT ON COLUMN se_services.updated_at IS 'Дата и время последнего обновления';

-- Индексы для улучшения производительности
CREATE INDEX idx_se_services_subcategory_id ON se_services(subcategory_id);
CREATE INDEX idx_se_services_status ON se_services(status);
CREATE INDEX idx_se_services_price ON se_services(price);
CREATE INDEX idx_se_services_created_at ON se_services(created_at);

-- Функция для автоматического обновления поля updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггеры для автоматического обновления поля updated_at при изменении записей

-- Для таблицы categories
CREATE TRIGGER trg_categories_updated_at
    BEFORE UPDATE ON categories
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Для таблицы subcategories
CREATE TRIGGER trg_subcategories_updated_at
    BEFORE UPDATE ON subcategories
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Для таблицы se_services
CREATE TRIGGER trg_se_services_updated_at
    BEFORE UPDATE ON se_services
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Вставка тестовых данных (опционально)
-- Раскомментируйте, если нужны тестовые данные при инициализации

/*
INSERT INTO categories (name, description) VALUES
    ('Дизайн', 'Услуги по дизайну'),
    ('Разработка', 'Услуги разработки программного обеспечения'),
    ('Маркетинг', 'Маркетинговые и рекламные услуги'),
    ('Консультации', 'Консультационные услуги'),
    ('Образование', 'Образовательные услуги и обучение');

INSERT INTO subcategories (category_id, name, description) VALUES
    (1, 'Веб-дизайн', 'Дизайн веб-сайтов и интерфейсов'),
    (1, 'Графический дизайн', 'Дизайн логотипов, брендинг'),
    (2, 'Веб-разработка', 'Создание веб-сайтов и приложений'),
    (2, 'Мобильная разработка', 'Разработка мобильных приложений'),
    (3, 'SEO-оптимизация', 'Поисковая оптимизация сайтов');

INSERT INTO se_services (subcategory_id, name, description, price, currency, status, location) VALUES
    (1, 'Дизайн лендинга', 'Создание современного дизайна одностраничного сайта', 500.00, 'BYN', 'active', 'Минск'),
    (3, 'Разработка интернет-магазина', 'Полный цикл разработки интернет-магазина на Django', 2000.00, 'USD', 'active', 'Удаленно'),
    (5, 'SEO-аудит сайта', 'Полный анализ сайта и рекомендации по SEO', 300.00, 'EUR', 'active', 'Удаленно');
*/

-- Сообщение об успешном завершении
DO $$
BEGIN
    RAISE NOTICE 'База данных успешно инициализирована';
    RAISE NOTICE 'Созданы таблицы: categories, subcategories, se_services';
    RAISE NOTICE 'Созданы индексы и триггеры для автоматического обновления updated_at';
END $$;