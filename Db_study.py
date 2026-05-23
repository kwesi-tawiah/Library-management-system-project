import sqlite3

# The "with" statement automatically handles
# closing the connection safely.

with sqlite3.connect("company.db") as conn:

    # Creates a cursor object
    cursor = conn.cursor()

    # CREATE TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees(

        id integer primary key autoincrement,
        name text not null,
        department text,
        salary integer

    )
    """)

    # INSERT ONE ROW
    cursor.execute("""

    INSERT INTO employees(name, department, salary)
    VALUES(?, ?, ?)

    """, ("Chris", "Engineering", 5000))

    # INSERT MANY ROWS
    workers = [

        ("Alice", "HR", 3000),
        ("John", "Finance", 4500),
        ("Mike", "Engineering", 7000)

    ]

    cursor.executemany("""

    INSERT INTO employees(name, department, salary)
    VALUES(?, ?, ?)

    """, workers)

    # SAVE CHANGES
    conn.commit()

    # lastrowid
    print("Last inserted row id:",
          cursor.lastrowid)

    # SELECT
    cursor.execute("""

    SELECT * FROM employees

    """)

    # fetchall()
    all_workers = cursor.fetchall()

    print("\nALL EMPLOYEES")
    for worker in all_workers:
        print(worker)

    # WHERE
    cursor.execute("""

    SELECT * FROM employees
    WHERE department = ?

    """, ("Engineering",))

    engineers = cursor.fetchall()

    print("\nENGINEERS")
    for engineer in engineers:
        print(engineer)

    # fetchone()
    cursor.execute("""

    SELECT * FROM employees

    """)

    first_person = cursor.fetchone()

    print("\nFIRST PERSON")
    print(first_person)

    # fetchmany()
    cursor.execute("""

    SELECT * FROM employees

    """)

    two_people = cursor.fetchmany(2)

    print("\nTWO PEOPLE")
    print(two_people)

    # ORDER BY
    cursor.execute("""

    SELECT * FROM employees
    ORDER BY salary DESC

    """)

    sorted_workers = cursor.fetchall()

    print("\nSORTED BY SALARY")
    for worker in sorted_workers:
        print(worker)

    # LIMIT
    cursor.execute("""

    SELECT * FROM employees
    LIMIT 2

    """)

    limited = cursor.fetchall()

    print("\nLIMITED RESULTS")
    print(limited)

    # UPDATE
    cursor.execute("""

    UPDATE employees
    SET salary = ?
    WHERE name = ?

    """, (9000, "Chris"))

    conn.commit()

    # DELETE
    cursor.execute("""

    DELETE FROM employees
    WHERE name = ?

    """, ("Alice",))

    conn.commit()

    # rollback()
    try:

        cursor.execute("""

        INSERT INTO employees(name, department, salary)
        VALUES(?, ?, ?)

        """, ("David", "Management", 10000))

        # Force an error
        x = 10 / 0

        conn.commit()

    except Exception as error:

        print("\nERROR OCCURRED")
        print(error)

        # Undo uncommitted changes
        conn.rollback()

    # FINAL DATA
    cursor.execute("""

    SELECT * FROM employees

    """)

    final_workers = cursor.fetchall()

    print("\nFINAL DATABASE")
    for worker in final_workers:
        print(worker)
