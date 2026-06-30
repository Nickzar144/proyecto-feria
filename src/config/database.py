import mysql.connector
from mysql.connector import pooling


class Database:
    """
    Gestiona un pool de conexiones persistentes hacia MySQL 8.0+
    usando mysql-connector-python.
    """
    _pool = None

    _CONFIG = {
        "pool_name": "movishare_pool",
        "pool_size": 5,
        "host": "localhost",
        "database": "movishare_db",
        "user": "root",
        "password": "Lacontraes132",
        "charset": "utf8mb4",
        "collation": "utf8mb4_general_ci",
        "autocommit": False
    }

    @classmethod
    def initialize_pool(cls):
        if cls._pool is None:
            cls._pool = pooling.MySQLConnectionPool(**cls._CONFIG)

    @classmethod
    def get_connection(cls):
        if cls._pool is None:
            cls.initialize_pool()
        return cls._pool.get_connection()

    @classmethod
    def close_pool(cls):
        if cls._pool is not None:
            cls._pool = None

    @classmethod
    def execute_query(cls, query, params=None, fetch_one=False, fetch_all=False):
        """
        Ejecuta una consulta parametrizada. Si no es SELECT, hace commit.
        Retorna None, un dict o una lista de dicts según flags.
        """
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            result = None
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                result = None

            if not query.strip().upper().startswith("SELECT"):
                conn.commit()
                # Si fue INSERT, devolver lastrowid cuando no hay fetch
                if query.strip().upper().startswith("INSERT") and not (fetch_one or fetch_all):
                    result = cursor.lastrowid

            return result
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def execute_many(cls, query, params_list):
        """Ejecuta una consulta con múltiples conjuntos de parámetros."""
        conn = cls.get_connection()
        cursor = conn.cursor()
        try:
            cursor.executemany(query, params_list)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
