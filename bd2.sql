-- 1. ТАБЛИЦА ПОЛЬЗОВАТЕЛИ
CREATE TABLE users (
    login VARCHAR(30) NOT NULL,
    parol VARCHAR(255) NOT NULL
);
-- 2. ТАБЛИЦА ПОЛ 
CREATE TABLE pol (
    id_pol SERIAL PRIMARY KEY,
    nazvanie VARCHAR(10) NOT NULL
);

-- 3. ТАБЛИЦА ДОЛЖНОСТИ 
CREATE TABLE dolzhnosti (
    id_dolzhnosti SERIAL PRIMARY KEY,
    nazvanie_dolzhnosti VARCHAR(50) NOT NULL,
    zarplata DECIMAL(10, 2)
);

-- 4. ТАБЛИЦА ПОДРАЗДЕЛЕНИЯ 
CREATE TABLE podrazdeleniya (
    id_podrazdeleniya SERIAL PRIMARY KEY,
    nazvanie_podrazdeleniya VARCHAR(50) NOT NULL,
    kod_podrazdeleniya VARCHAR(10),
    data_sozdaniya TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. ТАБЛИЦА ПОМЕЩЕНИЯ 
CREATE TABLE pomeshcheniya (
    id_pomeshcheniya SERIAL PRIMARY KEY,
    nomer_pomeshcheniya VARCHAR(50) NOT NULL,
    id_podrazdeleniya INTEGER NOT NULL,
    vmestimost INTEGER NOT NULL
);

-- 6. ТАБЛИЦА СОТРУДНИКИ 
CREATE TABLE sotrudniki (
    id_sotrudnika SERIAL PRIMARY KEY,
    fio VARCHAR(70) NOT NULL,
    id_podrazdeleniya INTEGER NOT NULL,
    id_pomeshcheniya INTEGER,
    id_dolzhnosti INTEGER NOT NULL,
    data_rozhdenia DATE,
    id_pol INTEGER NOT NULL,
    telefon VARCHAR(15),
    pochta VARCHAR(30)
);

-- 7. ТАБЛИЦА ИСТОРИЯ ДОЛЖНОСТЕЙ
CREATE TABLE istoriya_dolzhnostey (
    id_zapisi SERIAL PRIMARY KEY,
    id_sotrudnika INTEGER NOT NULL,
    staraya_dolzhnost VARCHAR(50),
    novaya_dolzhnost VARCHAR(50),
    data_smeny TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. ТАБЛИЦА ПРОЕКТЫ 
CREATE TABLE proekty (
    id_proekta SERIAL PRIMARY KEY,
    nazvanie VARCHAR(50) NOT NULL,
    id_podrazdeleniya INTEGER
);


-- 1. ПОЛЬЗОВАТЕЛИ

INSERT INTO users (login, parol) VALUES 
('admin', 'admin123'),
('ivanov', '123456'),
('petrova', 'password');


-- 2. ПОЛ

INSERT INTO pol (nazvanie) VALUES 
('Мужской'),
('Женский');

-- 3. ДОЛЖНОСТИ

INSERT INTO dolzhnosti (nazvanie_dolzhnosti, zarplata) VALUES 
('Генеральный директор', 200000.00),
('Заместитель директора', 150000.00),
('Финансовый директор', 160000.00),
('Начальник IT-отдела', 120000.00),
('Начальник бухгалтерии', 110000.00),
('Начальник отдела кадров', 100000.00),
('Начальник отдела продаж', 110000.00),
('Старший инженер', 90000.00),
('Инженер', 70000.00),
('Младший инженер', 55000.00),
('Главный бухгалтер', 95000.00),
('Бухгалтер', 65000.00),
('Экономист', 60000.00),
('HR-менеджер', 70000.00),
('Менеджер по продажам', 75000.00),
('Торговый представитель', 60000.00),
('Маркетолог', 65000.00),
('Администратор', 50000.00),
('Секретарь', 45000.00),
('Курьер', 35000.00),
('Стажер', 30000.00),
('Охранник', 40000.00),
('Уборщик', 30000.00);


-- 4. ПОДРАЗДЕЛЕНИЯ

INSERT INTO podrazdeleniya (nazvanie_podrazdeleniya, kod_podrazdeleniya) VALUES 
('Руководство', 'RUK'),
('IT-отдел', 'IT'),
('Бухгалтерия', 'BUX'),
('Отдел кадров', 'HR'),
('Отдел продаж', 'SALES'),
('Отдел маркетинга', 'MRK'),
('Производственный отдел', 'PROD'),
('Отдел логистики', 'LOG'),
('Склад', 'SKL'),
('Административный отдел', 'ADM'),
('Юридический отдел', 'LAW'),
('Отдел разработки', 'DEV'),
('Отдел тестирования', 'QA'),
('Техническая поддержка', 'SUP'),
('Отдел закупок', 'PUR');

-- 5. ПОМЕЩЕНИЯ

INSERT INTO pomeshcheniya (nomer_pomeshcheniya, id_podrazdeleniya, vmestimost) VALUES 
('101', 1, 1), ('102', 1, 2), ('103', 1, 2),
('201', 2, 12), ('202', 2, 8), ('203', 2, 6), ('204', 2, 4),
('205', 11, 5), ('206', 12, 10), ('207', 13, 8), ('208', 14, 6),
('301', 3, 8), ('302', 3, 4), ('303', 3, 2),
('401', 4, 6), ('402', 4, 3),
('501', 5, 15), ('502', 5, 6),
('503', 6, 8), ('504', 6, 4),
('601', 7, 10), ('602', 7, 6),
('603', 8, 8), ('604', 8, 4),
('701', 9, 6), ('702', 9, 3),
('801', 10, 5), ('802', 10, 3),
('901', 15, 6), ('902', 15, 3),
('1001', 12, 8), ('1002', 13, 6), ('1003', 14, 8), ('1004', 14, 4),
('1005', 15, 6), ('1006', 15, 4), ('1007', 2, 4), ('1008', 3, 4),
('1009', 5, 6), ('1010', 7, 4), ('1011', 8, 4);


-- 6. СОТРУДНИКИ 

INSERT INTO sotrudniki (fio, id_podrazdeleniya, id_pomeshcheniya, id_dolzhnosti, data_rozhdenia, id_pol, telefon, pochta) VALUES 
('Иванов Петр Сергеевич', 1, 1, 1, '1975-03-12', 1, '+79161234567', 'ivanov@company.ru'),
('Смирнова Анна Владимировна', 1, 2, 2, '1980-07-25', 2, '+79167654321', 'smirnova@company.ru'),
('Кузнецов Андрей Михайлович', 1, 3, 3, '1978-11-03', 1, '+79168889900', 'kuznetsov@company.ru'),
('Козлов Алексей Иванович', 2, 4, 4, '1985-11-03', 1, '+79165554433', 'kozlov@company.ru'),
('Петрова Мария Дмитриевна', 2, 4, 8, '1990-02-14', 2, '+79167778899', 'petrova@company.ru'),
('Сидоров Денис Андреевич', 2, 4, 9, '1992-09-30', 1, '+79162345678', 'sidorov@company.ru'),
('Ковалева Татьяна Алексеевна', 2, 4, 9, '1994-03-15', 2, '+79168901234', 'kovaleva@company.ru'),
('Морозов Дмитрий Игоревич', 2, 4, 9, '1991-10-11', 1, '+79169012345', 'morozov@company.ru'),
('Федорова Ольга Павловна', 3, 13, 5, '1988-12-05', 2, '+79163456789', 'fedorova@company.ru'),
('Орлова Людмила Викторовна', 3, 13, 11, '1986-05-19', 2, '+79170123456', 'orlova@company.ru'),
('Михайлова Елена Игоревна', 3, 13, 12, '1990-08-14', 2, '+79175678901', 'mihailova@company.ru'),
('Николаев Игорь Васильевич', 4, 16, 6, '1983-04-22', 1, '+79164567890', 'nikolaev@company.ru'),
('Зайцева Марина Олеговна', 4, 16, 14, '1996-11-15', 2, '+79175678901', 'zaitseva@company.ru'),
('Алексеев Михаил Петрович', 5, 18, 7, '1987-08-09', 1, '+79166789012', 'alekseev@company.ru'),
('Новиков Александр Дмитриевич', 5, 18, 16, '1995-02-28', 1, '+79174567890', 'novikov@company.ru'),
('Тихомиров Владислав Андреевич', 6, 20, 18, '1988-09-05', 1, '+79203456789', 'tihomirov@company.ru'),
('Васильева Екатерина Сергеевна', 7, 22, 9, '1991-06-18', 2, '+79165678901', 'vasileva@company.ru'),
('Комаров Владимир Петрович', 8, 24, 19, '1986-03-14', 1, '+79187890123', 'komarov@company.ru'),
('Павлов Сергей Николаевич', 9, 26, 20, '1993-01-27', 1, '+79167890123', 'pavlov@company.ru'),
('Морозова Елена Александровна', 10, 28, 19, '1985-12-03', 2, '+79201234567', 'morozova@company.ru'),
('Лебедев Александр Игоревич', 11, 30, 19, '1984-07-10', 1, '+79204567890', 'lebedev@company.ru'),
('Тихонов Андрей Викторович', 12, 31, 8, '1987-08-19', 1, '+79206789012', 'tihonov_a@company.ru'),
('Носков Владимир Петрович', 13, 32, 9, '1989-05-12', 1, '+79211234567', 'noskov@company.ru'),
('Логинов Алексей Сергеевич', 14, 33, 9, '1990-07-03', 1, '+79215678901', 'loginov@company.ru'),
('Гаврилов Игорь Владимирович', 15, 35, 19, '1986-06-19', 1, '+79221234567', 'gavrilov@company.ru'),
('Безместный Антон Юрьевич', 2, NULL, 22, '1999-05-10', 1, '+79179998877', 'bezmestny@company.ru'),
('Свободная Екатерина Максимовна', 3, NULL, 22, '2000-09-25', 2, '+79178887766', 'svobodnaya@company.ru'),
('Новобранец Дмитрий Алексеевич', 4, NULL, 22, '2001-03-15', 1, '+79177776655', 'novobranec@company.ru');


-- 7. ИСТОРИЯ ДОЛЖНОСТЕЙ

INSERT INTO istoriya_dolzhnostey (id_sotrudnika, staraya_dolzhnost, novaya_dolzhnost, data_smeny) VALUES 
(4, 'Старший инженер', 'Начальник IT-отдела', '2022-06-15 10:00:00'),
(5, 'Инженер', 'Старший инженер', '2021-09-10 14:30:00'),
(6, 'Младший инженер', 'Инженер', '2022-03-05 09:15:00'),
(9, 'Бухгалтер', 'Главный бухгалтер', '2023-01-15 13:00:00');

-- 8. ПРОЕКТЫ

INSERT INTO proekty (nazvanie, id_podrazdeleniya) VALUES 
('Внедрение ERP-системы', 2),
('Автоматизация бухгалтерии', 3),
('Программа обучения персонала', 4),
('Расширение рынка сбыта', 5),
('Рекламная кампания 2024', 6),
('Модернизация производства', 7),
('Реновация офиса', NULL);


-- 1. Подразделения с количеством сотрудников
SELECT 
    p.nazvanie_podrazdeleniya,
    COUNT(s.id_sotrudnika) AS sotrudnikov
FROM podrazdeleniya p
LEFT JOIN sotrudniki s USING(id_podrazdeleniya)
GROUP BY p.id_podrazdeleniya, p.nazvanie_podrazdeleniya
ORDER BY sotrudnikov DESC;

-- 2. Сотрудники в помещениях вместимостью больше 5 человек
SELECT 
    s.fio,
    s.id_podrazdeleniya,
    pm.nomer_pomeshcheniya,
    pm.vmestimost
FROM sotrudniki s
JOIN pomeshcheniya pm ON s.id_pomeshcheniya = pm.id_pomeshcheniya
WHERE pm.vmestimost > 5
ORDER BY pm.vmestimost DESC, s.fio;

-- 3. Начальники и их подчиненные
SELECT 
    s.fio AS nachalnik,
    d.nazvanie_dolzhnosti AS dolzhnost,
    p.nazvanie_podrazdeleniya AS podrazdelenie,
    COUNT(s2.id_sotrudnika) - 1 AS podchinennykh  
FROM sotrudniki s
JOIN dolzhnosti d USING(id_dolzhnosti)
JOIN podrazdeleniya p USING(id_podrazdeleniya)
JOIN sotrudniki s2 USING(id_podrazdeleniya)
WHERE d.nazvanie_dolzhnosti LIKE ANY(ARRAY['%директор%', 'Начальник%'])
GROUP BY s.id_sotrudnika, s.fio, d.nazvanie_dolzhnosti, p.nazvanie_podrazdeleniya
ORDER BY podchinennykh DESC;

-- 4. Сотрудники без рабочего места
SELECT 
    s.fio,
    p.nazvanie_podrazdeleniya,
    d.nazvanie_dolzhnosti
FROM sotrudniki s
JOIN podrazdeleniya p USING(id_podrazdeleniya)
JOIN dolzhnosti d USING(id_dolzhnosti)
WHERE s.id_pomeshcheniya IS NULL
ORDER BY p.nazvanie_podrazdeleniya, s.fio;

-- 5. Топ-3 самых загруженных помещений
SELECT 
    pm.nomer_pomeshcheniya,
    p.nazvanie_podrazdeleniya,
    COUNT(s.id_sotrudnika) AS zanyato
FROM pomeshcheniya pm
JOIN podrazdeleniya p ON pm.id_podrazdeleniya = p.id_podrazdeleniya
LEFT JOIN sotrudniki s ON pm.id_pomeshcheniya = s.id_pomeshcheniya
GROUP BY pm.id_pomeshcheniya, pm.nomer_pomeshcheniya, p.nazvanie_podrazdeleniya 
HAVING COUNT(s.id_sotrudnika) > 0
ORDER BY zanyato DESC
LIMIT 3;
