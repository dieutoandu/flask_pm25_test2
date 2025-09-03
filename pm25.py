import pymysql
import requests


table_str = """
create table if not exists pm25(
id int auto_increment primary key ,
site varchar(25),
county varchar(50),
pm25 int,
datacreationdate datetime,
itemunit varchar(20),
unique key site_time (site,datacreationdate)
)
"""

insert_table = "insert ignore into pm25(site,county,pm25,datacreationdate,itemunit)\
     values(%s,%s,%s,%s,%s)"


conn, cursor = None, None


def open_db():
    global conn, cursor

    try:
        conn = pymysql.connect(
            host="mysql-123fc510-dieutoandu2001-006a.i.aivencloud.com",
            user="avnadmin",
            password="AVNS_xvnQ_Gy9nuH3FKXe8Hg",
            port=18217,
            database="defaultdb",
        )

        print(conn)
        cursor = conn.cursor()
        print("on pass !")
    except Exception as e:
        print(e)


def close_db():
    global conn, cursor
    if conn is not None:
        conn.close()
        print("close pass ")


def get_open_data():
    url = "https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=540e2ca4-41e1-4186-8497-fdd67024ac44&limit=1000&sort=datacreationdate%20desc&format=JSON"
    resp = requests.get(url, verify=False)
    datas = resp.json()["records"]
    values = [list(data.values()) for data in datas if list(data.values())[2] != ""]
    return values


def write_sql():

    try:
        values = get_open_data()
        if len(values) == 0:
            print("now not any data")
            return
        values = cursor.executemany(values, (insert_table,))
        conn.commit()
        print(f"insert data pass {len(values)}")
        return values
    except Exception as e:
        print(e)
    return 0


def get_mysql_data():

    try:
        open_db()

        sqlstr = (
            "select site,county,pm25,datacreationdate,itemunit "
            "from pm25 "
            "where datacreationdate=(select max(datacreationdate) from pm25);"
        )
        cursor.execute(sqlstr)
        datas = cursor.fetchall()

        return datas
    except Exception as e:
        print(e)
    finally:
        close_db()

    return None


def get_avg_pm25():

    try:
        open_db()

        sqlstr = """
            select county,round(avg(pm25),2) from pm25 group by county;
            """
        cursor.execute(sqlstr)
        datas = cursor.fetchall()

        return datas
    except Exception as e:
        print(e)
    finally:
        close_db()

    return None


def write_data_to_mysql():

    try:
        open_db()
        datas = write_sql()
        print("update pass")
        return len(datas)
    except Exception as e:
        print(e)
        print("update not pass ")
    finally:
        close_db()
    return 0


def get_pm25_by_county(county):
    try:
        open_db()

        sqlstr = """
        select site,pm25,datacreationdate from pm25 
        where county = %s 
        and datacreationdate=(select max(datacreationdate) from pm25);

        """
        cursor.execute(sqlstr, (county,))
        datas = cursor.fetchall()

        return datas
    except Exception as e:
        print(e)
    finally:
        close_db()

    return None


if __name__ == "__main__":
    print(get_pm25_by_county("臺北市"))
