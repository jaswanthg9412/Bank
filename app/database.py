import psycopg2


def get_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="bank_management",
        user="postgres",
        password= "tiger" ,
        port="5432"
    )

    return connection


def create_account(name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO accounts (name)
        VALUES (%s)
        RETURNING account_number;
        """,
        (name,)
    )

    account_number = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return account_number


def get_accounts():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT account_number, name, balance FROM accounts"
    )

    accounts = cursor.fetchall()

    cursor.close()
    connection.close()

    return accounts


def deposit_money(account_number, amount):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE accounts
        SET balance = balance + %s
        WHERE account_number = %s
        RETURNING name, balance;
        """,
        (amount, account_number)
    )

    account = cursor.fetchone()

    if account is None:
        connection.rollback()
        cursor.close()
        connection.close()
        return None

    name, balance = account

    cursor.execute(
        """
        INSERT INTO transactions
        (account_number, transaction_type, amount)
        VALUES (%s, %s, %s);
        """,
        (account_number, "Deposit", amount)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return name, balance


def withdraw_money(account_number, amount):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE accounts
        SET balance = balance - %s
        WHERE account_number = %s
          AND balance >= %s
        RETURNING name, balance;
        """,
        (amount, account_number, amount)
    )

    account = cursor.fetchone()

    if account is None:
        connection.rollback()

        cursor.execute(
            "SELECT 1 FROM accounts WHERE account_number = %s",
            (account_number,)
        )
        exists = cursor.fetchone()

        cursor.close()
        connection.close()

        if exists is None:
            return "not_found"

        return "insufficient_balance"

    name, balance = account

    cursor.execute(
        """
        INSERT INTO transactions
        (account_number, transaction_type, amount)
        VALUES (%s, %s, %s);
        """,
        (account_number, "Withdrawal", amount)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return name, balance


def get_transaction_history(account_number):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT transaction_type, amount, transaction_date
        FROM transactions
        WHERE account_number = %s
        ORDER BY transaction_id;
        """,
        (account_number,)
    )

    transactions = cursor.fetchall()

    cursor.close()
    connection.close()

    return transactions