import pandas as pd
from sklearn.decomposition import PCA

if __name__ == '__main__':
    # 1. 获取数据
    aisles = pd.read_csv('data/instacart/aisles.csv')
    order_products = pd.read_csv('data/instacart/order_products__prior.csv')
    orders = pd.read_csv('data/instacart/orders.csv')
    products = pd.read_csv('data/instacart/products.csv')
    # 2. 合并表
    tmp1 = pd.merge(aisles, products, on=['aisle_id', 'aisle_id'])
    tmp2 = pd.merge(order_products, tmp1, on=['product_id', 'product_id'])
    tmp3 = pd.merge(orders, tmp2, on=['order_id', 'order_id'])

    table = pd.crosstab(tmp3['user_id'], tmp3['aisle'])
    # 3. 找到user_id和aisle之间的关系
    transfer = PCA(n_components=0.95)
    data_new = transfer.fit_transform(table)
    print(data_new.shape)
