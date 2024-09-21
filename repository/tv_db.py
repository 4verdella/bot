import psycopg2
from config.config import Bot_config

cfg_db = Bot_config()

class PostgreSql_tv:
    def __init__(self):
        self.connect = psycopg2.connect(
            host=cfg_db.host,
            user=cfg_db.user,
            database=cfg_db.database,
            password=cfg_db.password
        )
        self.cursor = self.connect.cursor()

    def create_table(self):
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS tv_db(
                id SERIAL PRIMARY KEY,
                brand_name VARCHAR(255),
                product_url TEXT,
                product_image VARCHAR(255),
                product_price VARCHAR(40),
                configurations TEXT UNIQUE
            )""")
        self.connect.commit()

    def insert_data(self, *args):
        self.create_table()
        self.cursor.execute(f"""INSERT INTO tv_db (brand_name, product_url, product_image, product_price, configurations)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT(configurations) DO NOTHING""", args)
        self.connect.commit()

    def select_data(self):
        self.cursor.execute(f"""
            SELECT brand_name, product_url, product_image, product_price, configurations
            FROM tv_db
        """)
        return self.cursor.fetchall()



