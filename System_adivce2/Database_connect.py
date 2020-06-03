import pymysql

def Connect_sql():
    conn = pymysql.connect(host="localhost", port=3306, user='root', password="bottle152")
    cur = conn.cursor()  # 生成游标对象
    return conn, cur

def Close_sql(conn,cur):
    cur.close()
    conn.close()
    return