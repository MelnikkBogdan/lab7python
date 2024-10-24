import psycopg2

# Параметри підключення
connection = psycopg2.connect(
    dbname='library',
    user='user',
    password='password',
    host='localhost',
    port='5432'
)

cursor = connection.cursor()

# SQL для створення таблиць
create_books_table = '''
CREATE TABLE books (
    inventory_number VARCHAR(10) PRIMARY KEY,
    author TEXT,
    title TEXT,
    section VARCHAR(50),
    publication_year INT,
    page_count INT,
    price NUMERIC(10, 2),
    type VARCHAR(50),  -- Значення 'book', 'manual', 'periodical'
    copies INT,
    max_borrow_period INT
);
'''

create_readers_table = '''
CREATE TABLE readers (
    id SERIAL PRIMARY KEY,
    ticket_number VARCHAR(50) UNIQUE,
    last_name TEXT,
    first_name TEXT,
    phone_number VARCHAR(15),
    address TEXT,
    course INT CHECK (course BETWEEN 1 AND 4),
    group_number VARCHAR(10)
);
'''

create_issues_table = '''
CREATE TABLE issues (
    id SERIAL PRIMARY KEY,
    issue_date DATE NOT NULL,
    reader_ticket_number VARCHAR(50) REFERENCES readers(ticket_number),
    book_inventory_number VARCHAR(10) REFERENCES books(inventory_number),
    return_date DATE
);
'''

# Виконання запитів на створення таблиць
cursor.execute(create_books_table)
cursor.execute(create_readers_table)
cursor.execute(create_issues_table)

# Додавання даних
books_data = [
    ('001', 'Author 1', 'Title 1', 'technical', 2002, 100, 29.99, 'book', 5, 30),
    ('002', 'Author 2', 'Title 2', 'fiction', 2003, 150, 19.99, 'manual', 3, 14),
    ('003', 'Author 3', 'Title 3', 'economic', 2004, 200, 24.99, 'periodical', 10, 21),
    ('004', 'Author 4', 'Title 4', 'technical', 2005, 300, 15.99, 'book', 7, 14),
    ('005', 'Author 5', 'Title 5', 'fiction', 2001, 350, 9.99, 'manual', 2, 10),
    ('006', 'Author 6', 'Title 6', 'economic', 2000, 400, 29.99, 'book', 1, 30),
    ('007', 'Author 7', 'Title 7', 'technical', 1999, 100, 19.99, 'periodical', 0, 0),
    ('008', 'Author 8', 'Title 8', 'fiction', 1998, 150, 24.99, 'book', 4, 14),
    ('009', 'Author 9', 'Title 9', 'economic', 1997, 200, 14.99, 'manual', 6, 21),
    ('010', 'Author 10', 'Title 10', 'technical', 1996, 250, 5.99, 'periodical', 8, 30),
    ('011', 'Author 11', 'Title 11', 'fiction', 1995, 300, 35.99, 'book', 2, 14),
    ('012', 'Author 12', 'Title 12', 'economic', 1994, 150, 9.99, 'manual', 3, 10),
    ('013', 'Author 13', 'Title 13', 'technical', 2002, 200, 29.99, 'periodical', 5, 21),
    ('014', 'Author 14', 'Title 14', 'fiction', 2003, 180, 19.99, 'book', 4, 30)
]

readers_data = [
    ('T001', 'Ivanov', 'Ivan', '+380123456789', 'Address 1', 1, 'Group 1'),
    ('T002', 'Petrov', 'Petr', '+380987654321', 'Address 2', 2, 'Group 2'),
    ('T003', 'Sidorov', 'Sidr', '+380123456780', 'Address 3', 3, 'Group 3'),
    ('T004', 'Koval', 'Kostiantyn', '+380123456781', 'Address 4', 4, 'Group 1'),
    ('T005', 'Shevchenko', 'Taras', '+380123456782', 'Address 5', 1, 'Group 2'),
    ('T006', 'Khmara', 'Oles', '+380123456783', 'Address 6', 2, 'Group 3'),
    ('T007', 'Bohdan', 'Bohdan', '+380123456784', 'Address 7', 3, 'Group 1'),
    ('T008', 'Ivchenko', 'Mykola', '+380123456785', 'Address 8', 4, 'Group 2'),
    ('T009', 'Melnyk', 'Vasyl', '+380123456786', 'Address 9', 1, 'Group 3')
]

issues_data = [
    ('2024-01-01', 'T001', '001'),
    ('2024-02-01', 'T002', '002'),
    ('2024-03-01', 'T003', '003'),
    ('2024-04-01', 'T004', '004'),
    ('2024-05-01', 'T005', '005'),
    ('2024-06-01', 'T006', '006'),
    ('2024-07-01', 'T007', '007'),
    ('2024-08-01', 'T008', '008'),
    ('2024-09-01', 'T009', '009'),
    ('2024-10-01', 'T001', '010'),
    ('2024-11-01', 'T002', '011')
]

# Вставка даних у таблицю books
for book in books_data:
    cursor.execute('''
    INSERT INTO books (inventory_number, author, title, section, publication_year, page_count, price, type, copies, max_borrow_period)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', book)
    
# Вставка даних у таблицю readers
for reader in readers_data:
    cursor.execute('''
    INSERT INTO readers (ticket_number, last_name, first_name, phone_number, address, course, group_number)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', reader)

# Вставка даних у таблицю issues
for issue in issues_data:
    cursor.execute('''
    INSERT INTO issues (issue_date, reader_ticket_number, book_inventory_number)
    VALUES (%s, %s, %s)
    ''', issue)

# Підтвердження змін
connection.commit()

# Закриття з'єднання
cursor.close()
connection.close()
