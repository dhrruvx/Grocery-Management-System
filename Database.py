from re import L
from typing import final
from Config import Config
import logging
import mysql.connector as MySQL_conn
from datetime import date, datetime, timedelta

class Database:
    def __init__(self, filename="db_config.env") -> None:
        config = Config(filename)
        params = config.get_configurations()
        self.host = params.get("DB", "host")
        self.user = params.get("DB", "user")
        self.password = params.get("DB", "password")
        self.database = params.get("DB", "database")

    def connect_noDB(self):
        conn = MySQL_conn.connect(
            host= self.host,
            user=self.user,
            password=self.password
        )

        return conn

    def connect(self):
        conn = MySQL_conn.connect(
            host= self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        return conn

    def create(self, table_name, attributes):

        SQL = f""" CREATE TABLE {table_name} (
            )"""

    def create_tables(self, queries):
        
        for sql in queries:
            try:
                conn = self.connect()
                cursor = conn.cursor()
                print(f"EXECUTING QUERY:  {sql}")
                cursor.execute(sql)
                table_name = sql.split()[2]
                print(f"TABLE {table_name} Created successfully")
                print("QUERY SUCCESSFUL..")
            except Exception as e:
                print(f"EXCEPTION OCCOURED: {e}")
            finally:
                cursor.close()
                conn.close()
    
    def run_query(self, SQL):
        results=None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(SQL)
            results = cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
            if(results is not None):
                return results

    def retrieve(self, table_name, clause=""):
        results = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            SQL = f"SELECT * FROM {table_name} {clause}"
            cursor.execute(SQL)
            results = cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
            if(results is not None):
                return results


    def insert(self, table_name, *values, **k_values):
        """
            values: tuple of data to be inserted
            k_values : dict
        """
        SQL = ""
        vals = None
        value_length = len(values)
        v_str = "%s," * value_length
        v_str = f"({v_str[:len(v_str)-1]})"

        k_value_length = len(k_values)
        k_v_str = "%s," * k_value_length
        k_v_str = f"({k_v_str[:len(k_v_str)-1]})"

        results = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            if(value_length == 0):
                params = str(tuple(k_values.keys()))
                cols = ""
                vals = tuple(k_values.values())
                print(f"values: {vals}")
                for i in params:
                    if(i == "'"):
                        continue
                    else:
                        cols = cols + i

                print(f"COLS: {cols}")
                if(cols[len(cols)-2] == "," ):
                    cols = cols[:len(cols)-2] + ")" 
                    print(f"{cols}")

                SQL = f"INSERT INTO {table_name} {cols} VALUES {k_v_str}"
                print("EXECUTING SQL: ", SQL, vals)
                cursor.execute(SQL, vals)
                conn.commit()
                print("Query SUCCESS")

            elif(k_value_length == 0):
                vals = values
                SQL = f"INSERT INTO {table_name} VALUES {v_str}"
                print("EXECUTING SQL: ", SQL, vals)
                cursor.execute(SQL, values)
                conn.commit()
        
        except Exception as e:
            print(f"EXCEPTION OCCOURED: {e}")
        finally:
            cursor.close()
            conn.close()
            if(results is not None):
                return results

    def update(self, table_name, id, **kw_cols):
        """
            id: 'user_id=001' string
            **kw_cols: key argument for the attributes
        """
        k_value_length = len(kw_cols)
        k_v_str = "%s," * k_value_length
        k_v_str = f"({k_v_str[:len(k_v_str)-1]})"

        params = ""
        for k in kw_cols.keys():
            params = params + k + "=%s,"
        
        rev_param = params[::-1]
        index = rev_param.find(",")
        params = rev_param[index+1:][::-1]

        try:
            conn = self.connect()
            cursor = conn.cursor()
            SQL = f"UPDATE {table_name} SET {params} WHERE {id}"
            vals = vals = tuple(kw_cols.values())

            print("EXECUTING SQL: ", SQL, vals)
            cursor.execute(SQL, vals)
            conn.commit()
            print("Query SUCCESS")

        except Exception as e:
            print(f"EXCEPTION OCCOURED: {e}")
        finally:
            cursor.close()
            conn.close()

    def delete(self, table_name, clause=""):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            SQL = f"DELETE FROM {table_name} WHERE {clause}"

            print("EXECUTING SQL: ", SQL)
            cursor.execute(SQL)
            conn.commit()
            print("Query SUCCESS")
        except Exception as e:
            print(f"EXCEPTION OCCURED: {e}")
        finally:
            cursor.close()
            conn.close()

        print(SQL)


# DELETE FROM products WHERE product_id=3476

db = Database()
#db.update("products", "product_id=3001", unit_price=37, availibility=54)
#db.update("products",id =f"product_id=3001", availibility=61 - 3)

#db.delete("products", "product_id=35677 AND cate=535")6