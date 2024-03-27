from Database import Database

def check_credentials(username, password):
    db = Database()
    con = db.connect()

    login_flag = False
    user = None
    user_type = None
    user_id = None
    try:
        cursor = con.cursor()
        sql = "SELECT * FROM users WHERE username=%s AND password=%s LIMIT 1"
        vals = (username, password)
        cursor.execute(sql, vals)
        results = cursor.fetchall()
        row_count = cursor.rowcount
        #print(results)
        if(row_count == 1):
            login_flag = True
            for row in results:
                user = row[1]
                user_id = row[0]
                if(row[5] == 1):
                    user_type = "admin"
                else:
                    user_type = "customer"
        else:
            pass
    except Exception as e:
        print(f"EXCEPTION OCCOURED: {e}")
    finally:
        cursor.close()
        con.close()
        return (login_flag, user, user_type, user_id)