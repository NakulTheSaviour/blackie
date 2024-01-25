from faker import Faker
import mysql.connector
from mysql.connector import Error

# Connect to MySQL
try:
    connection = mysql.connector.connect(
        host='localhost',
        database='nakuldb1',
        user='root',
        password='nakul'
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # Create a table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Player (
            UID VARCHAR(255) NOT NULL,
            Name VARCHAR(255) NOT NULL,
            Score INT NOT NULL,
            Country CHAR(2) NOT NULL,
            TimeStamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (UID)
        );
        """
        cursor.execute(create_table_query)

        # Use Faker to generate and insert data
        fake = Faker()
        insert_query = "INSERT INTO Player (UID, Name, Score, Country, TimeStamp) VALUES (%s, %s, %s, %s, %s);"
        data = [(fake.uuid4(), fake.name(), fake.random_int(min=1, max=100), fake.country_code(), fake.date_time_this_decade()) for _ in range(10000)]

        cursor.executemany(insert_query, data)

        # Commit changes
        connection.commit()
        print("Data inserted successfully")

except Error as e:
    print(f"Error: {e}")

finally:
    # Close connection
    if connection.is_connected():
        cursor.close()
        connection.close()
