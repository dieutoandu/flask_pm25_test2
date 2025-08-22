import pymysql
import requests


table_str="""
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

insert_table="insert ignore into pm25(site,county,pm25,datacreationdate,itemunit)\
     values(%s,%s,%s,%s,%s)"



conn,cursor=None,None

def open_db():
    global conn,cursor

    try:
        conn=pymysql.connect(
            host="localhost",
            user="root",
            password="",
            port=3307,
            database="demo"
        )

        print(conn)
        cursor=conn.cursor()
        print("on pass !")
    except Exception as e :
        print(e)


def close_db():
    global conn , cursor
    if conn is not None:
        conn.close()
        print("close pass ")



def get_open_data():
    url='https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=540e2ca4-41e1-4186-8497-fdd67024ac44&limit=1000&sort=datacreationdate%20desc&format=JSON'
    resp=requests.get(url,verify=False)
    datas=resp.json()['records']
    values=[list(data.values()) for data in datas if list(data.values())[2]!='']
    return values


def write_sql():
    try:
        values=get_open_data()
        if len(values)==0:
            print('now not any data')
            return
        cursor.executemany(insert_table,values)
        conn.commit()
        print(f"insert data pass {len(values)}")
    except Exception as e :
        print(e)


open_db()
write_sql()
close_db()

