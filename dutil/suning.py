import requests

def be_suning(id,shopdb):
    try:
        shopdb.query("SELECT prod_id FROM t_good_suning WHERE prod_id = {}".format(id))[0].prod_id
        hc()
    except :
        print("商品不是苏宁商品，设置为苏宁商品")
        try:
            sku = shopdb.query("SELECT sku FROM t_good_shelf WHERE id ={}".format(id)).first().sku
            sql = "INSERT INTO t_good_suning VALUES (nextval('seq_t_good_suning_id'),'"+id+"','"+sku+"',NULL,'000000000121359927','1','0.0000',NULL,now() :: TIMESTAMP (0) WITHOUT TIME ZONE,'-1','车载纸巾');"
            shopdb.query(sql)
            hc()
        except :
            print("id对应的商品不存在")

def hc():
    url = 'http://atxc.beta.daling.com/suning/redis/recover/suningProd'
    requests.get(url=url)

def de_suning(id,shopdb):
    try:
        shopdb.query("SELECT prod_id FROM t_good_suning WHERE prod_id = {}".format(id))[0].prod_id
        print("商品为苏宁商品，设置为普通商品")
        try:
            r = shopdb.query("DELETE FROM t_good_suning WHERE prod_id = {}".format(id))
            print(r)
            hc()
        except :
            print("删除失败")
    except :
        hc()
