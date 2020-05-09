from pymysql import *
import psycopg2

def sql_update(sql):
    # 创建connection连接
    conn = connect(host='i.mysql1.qa.daling.com', port=7940, database='sbc_account_dev', user='daling_app_rw',
                   password='1234@Daling', charset='utf8')
    # 获取cursor对象
    cs1 = conn.cursor()
    # 执行sql语句
    cs1.execute(sql)

    # 提交之前的操作，如果之前已经执行多次的execute，那么就都进行提交
    conn.commit()

    # 关闭cursor对象
    cs1.close()
    # 关闭connection对象
    conn.close()



def pgsql_update(sql):
    conn = psycopg2.connect(database="sbc_order_db", user="daling_app_rw",
                            password="1234@Daling", host="i.pgsql1.qa.daling.com",
                            port="5410")
    # 获取cursor对象
    cs1 = conn.cursor()
    # 执行sql语句
    cs1.execute(sql)
    # # 查询结果转化为数组格式
    rows = cs1.fetchall()
    res = rows[0][0]
    return res

    # 提交之前的操作，如果之前已经执行多次的execute，那么就都进行提交
    #conn.commit()

    # 关闭cursor对象
    cs1.close()
if __name__ == "__main__":
    sql_1 = "update t_account set active_money = 10000 where user_id = '{}'".format(844354)
    print(sql_update(sql_1))

    sql = "select order_status from t_sale_order where so_no = '001934315381758789'"
    r = pgsql_update(sql)
    print(r)