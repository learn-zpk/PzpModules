import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

if __name__ == '__main__':
    # 1. 加载数据集
    data = pd.read_csv('data/FBlocation/train.csv')
    # 2. 预处理数据
    # 2.1 缩小数据范围
    data = data.query("x < 2.5 & x>2 & y < 1.5 & y > 1.0")
    # 2.2 处理时间特征
    time_val = pd.to_datetime(data['time'], unit='s')
    date = pd.DatetimeIndex(time_val)
    data['day'] = date.day
    data['weekday'] = date.weekday
    data['hour'] = date.hour
    # 2.3 过滤签到地点少的数据
    place_count = data.groupby('place_id').count()['row_id']
    data = data[data['place_id'].isin(place_count[place_count > 3].index.values)]

    # 2.4 筛选目标值和特征值
    x = data[["x", "y", "accuracy", "day", "weekday", "hour"]]
    y = data[["place_id"]]

    # 2.5 数据集划分
    x_train, x_test, y_train, y_test = train_test_split(x, y)

    # 3. 特征工程：标准化
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    # 用训练集的平均值和标准差对测试集特征工程处理
    x_test = transfer.transform(x_test)
    # 4. KNN算法预估器
    estimator = KNeighborsClassifier(n_neighbors=3)
    # 加入网格搜索与交叉验证
    estimator = GridSearchCV(estimator, param_grid={'n_neighbors': [3, 4, 5, 6, 7, 8, 9, 10]}, cv=10)

    estimator.fit(x_train, y_train)
    # 5. 模型评估
    ## 5.1 知己比对真实值和预测值
    y_predict = estimator.predict(x_test)
    print("真实值对比预测值：\n", y_test == y_predict)
    ## 5.2 计算准确率
    score = estimator.score(x_test, y_test)
    print("准确率：\n", score)

    print("最佳参数：\n", estimator.best_params_)
    print("最佳结果：\n", estimator.best_score_)
    print("最佳评估器：\n", estimator.best_estimator_)
    print("交叉验证结果：\n", estimator.cv_results_)