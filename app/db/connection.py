from psycopg2 import pool
from fastapi import Depends

db_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn="dbname=github user=postgres password=postgres host=localhost"
)

def get_db_connection():
    conn = db_pool.getconn()
    try:
        yield conn
    finally:
        db_pool.putconn(conn)