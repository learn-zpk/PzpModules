import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score


def kmeans_demo():
    # 数据处理
    aisles = pd.read_csv('../01/data/instacart/aisles.csv')
    order_products = pd.read_csv('../01/data/instacart/order_products__prior.csv')
    orders = pd.read_csv('../01/data/instacart/orders.csv')
    products = pd.read_csv('../01/data/instacart/products.csv')

    tmp1 = pd.merge(aisles, products, on=['aisle_id', 'aisle_id'])
    tmp2 = pd.merge(order_products, tmp1, on=['product_id', 'product_id'])
    tmp3 = pd.merge(orders, tmp2, on=['order_id', 'order_id'])

    table = pd.crosstab(tmp3['user_id'], tmp3['aisle'])

    # 特征降维
    transfer = PCA(n_components=0.95)
    data_new = transfer.fit_transform(table)
    # KMeans聚类
    estimator = KMeans(n_clusters=3)
    estimator.fit(data_new)
    y_predict = estimator.predict(data_new)
    # print(y_predict[0:100])
    # 评估
    print("轮廓系统：\n", silhouette_score(data_new, y_predict))
    return None


if __name__ == '__main__':
    kmeans_demo()
