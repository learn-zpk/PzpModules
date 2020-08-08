from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler


def knn_iris():
    # 1. 获取数据
    iris = load_iris()
    # 2. 划分分数据集：训练集、测试集
    x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, random_state=3)
    # 3. 特征工程：标准化
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    # 用训练集的平均值和标准差对测试集特征工程处理
    x_test = transfer.transform(x_test)
    # 4. KNN算法预估器
    estimator = KNeighborsClassifier(n_neighbors=3)
    estimator.fit(x_train, y_train)
    # 5. 模型评估
    ## 5.1 知己比对真实值和预测值
    y_predict = estimator.predict(x_test)
    print("真实值对比预测值：\n", y_test == y_predict)
    ## 5.2 计算准确率
    score = estimator.score(x_test, y_test)
    print("准确率：\n", score)


def knn_iris_gridsearch_cv():
    # 1. 获取数据
    iris = load_iris()
    # 2. 划分分数据集：训练集、测试集
    x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, random_state=22)
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


if __name__ == '__main__':
    # 1. 使用KNN算法预测鸢尾花分类
    # knn_iris()
    # 2. 使用KNN算法预测鸢尾花分类: 网格搜索、交叉验证
    knn_iris_gridsearch_cv()
