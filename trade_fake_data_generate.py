import pymysql
import random
from faker import Faker

# Initialize Faker instance
faker = Faker()

# Configuration
num_records = 900
spareparts_id_range = (5, 73)
created_by_id_range = (1, 2)

# Database connection details
db_config = {
    "host": "localhost",      # Replace with your host (e.g., "127.0.0.1" or a remote IP)
    "user": "root",  # Replace with your MySQL username
    "password": "pass",  # Replace with your MySQL password
    "database": "SparePartsDB",  # Replace with your database name
    "port": 3306              # Default MySQL port
}

# Connect to the MySQL database
connection = pymysql.connect(**db_config)
cursor = connection.cursor()


# Insert records
for _ in range(num_records):
    quantity = random.randint(-100, 100)
    other = "/"
    trade_time = faker.date_time_between(start_date="-3y", end_date="now").strftime('%Y-%m-%d %H:%M:%S')
    spareparts_id_id = random.randint(*spareparts_id_range)
    created_by_id = random.randint(*created_by_id_range)

    # Execute the insert query
    insert_query = """
    INSERT INTO app01_trade (spareparts_id_id, created_by_id, trade_time, other, quantity)
    VALUES (%s, %s, %s, %s, %s);
    """
    cursor.execute(insert_query, (spareparts_id_id, created_by_id, trade_time, other, quantity))

# Commit changes and close the connection
connection.commit()
connection.close()

print(f"Inserted {num_records} records into the MySQL database '{db_config['database']}'.")
