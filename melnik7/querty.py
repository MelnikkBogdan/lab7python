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

# Запит для отримання всіх книг, виданих після 2001 року, відсортованих за назвою
cursor.execute('''
SELECT title FROM books 
WHERE publication_year > 2001 
ORDER BY title;
''')
books_after_2001 = cursor.fetchall()
print("Books published after 2001:")
for book in books_after_2001:
    print(book[0])  # Виводимо тільки назви книг

# Запит для підрахунку кількості книг кожного виду
cursor.execute('''
SELECT type, COUNT(*) FROM books 
GROUP BY type;
''')
book_counts = cursor.fetchall()
print("\nCount of each book type:")
for book_type, count in book_counts:
    print(f"{book_type}: {count}")

# Запит для отримання читачів, які брали посібники
cursor.execute('''
SELECT DISTINCT r.last_name 
FROM readers r
JOIN issues i ON r.ticket_number = i.reader_ticket_number
JOIN books b ON i.book_inventory_number = b.inventory_number
WHERE b.type = 'manual'
ORDER BY r.last_name;
''')
readers_of_manuals = cursor.fetchall()
print("\nReaders who borrowed manuals:")
for reader in readers_of_manuals:
    print(reader[0])

section = 'fiction'  # Приклад параметра
cursor.execute('''
SELECT * FROM books 
WHERE section = %s;
''', (section,))
books_in_section = cursor.fetchall()
print(f"\nBooks in section '{section}':")
for book in books_in_section:
    print(book)

cursor.execute('''
SELECT b.title, i.issue_date, (i.issue_date + INTERVAL '1 day' * b.max_borrow_period) AS return_date
FROM issues i
JOIN books b ON i.book_inventory_number = b.inventory_number;
''')
return_dates = cursor.fetchall()
print("\nReturn dates for borrowed books:")
for title, issue_date, return_date in return_dates:
    print(f"{title} - Issue Date: {issue_date}, Return Date: {return_date}")

cursor.execute('''
SELECT section, type, COUNT(*) 
FROM books 
GROUP BY section, type;
''')
counts_by_section_and_type = cursor.fetchall()
print("\nCount of books, manuals, and periodicals in each section:")
for section, book_type, count in counts_by_section_and_type:
    print(f"{section} - {book_type}: {count}")


# Функція для виведення структури та даних таблиці
def print_table(cursor, table_name):
    cursor.execute(f'SELECT * FROM {table_name};')
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]

    print(f"\nTable: {table_name}")
    print(f"{' | '.join(col_names)}")
    print("-" * (len(col_names) * 10))
    for row in rows:
        print(f"{' | '.join(map(str, row))}")


# Виведення всіх таблиць
tables = ['books', 'readers', 'issues']
for table in tables:
    print_table(cursor, table)

# Закриття з'єднання
cursor.close()
connection.close()
