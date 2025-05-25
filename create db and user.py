import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'ac_users'
DB_USER = 'ac_user'
DB_PASSWORD = '172003'
DB_HOST = 'localhost'

def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8mb4'")
        print(f"Db {DB_NAME} created.")
    except mysql.connector.Error as err:
        print(f"Failed creating db: {err}")

def create_user(cursor):
    try:
        cursor.execute(f"CREATE USER IF NOT EXISTS '{DB_USER}'@'{DB_HOST}' IDENTIFIED BY '{DB_PASSWORD}'")
        print(f"User {DB_USER} created or exists")
    except mysql.connector.Error as err:
        print(f"Failed creating user: {err}")

def grant_privileges(cursor):
    try:
        cursor.execute(f"GRANT ALL PRIVILEGES ON {DB_NAME}.* TO '{DB_USER}'@'{DB_HOST}'")
        cursor.execute("FLUSH PRIVILEGES")
        print(f"Granted privileges to user {DB_USER} on database {DB_NAME}.")
    except mysql.connector.Error as err:
        print(f"Failed granting privileges: {err}")

def main():
    try:
        cnx = mysql.connector.connect(user='aureldb', password='passac2025', host=DB_HOST)
        cursor = cnx.cursor()

        try:
            cursor.execute(f"USE {DB_NAME}")
            print(f"Db {DB_NAME} already exists")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(cursor)
            else:
                print(err)
                return

        create_user(cursor)
        grant_privileges(cursor)

        cursor.close()
        cnx.close()
        print("Setup completed successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == '__main__':
    main()
