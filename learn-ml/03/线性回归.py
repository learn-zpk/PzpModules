from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression, SGDRegressor, Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def linear_regression():
    boston = load_boston()
    x_train, x_test, y_train, y_test = train_test_split(boston.data, boston.target, random_state=22)
    # 无量纲化
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)
    # 模型训练
    estimator = LinearRegression(fit_intercept=True)
    estimator.fit(x_train, y_train)
    # 模型参数
    print("权重系数：\n", estimator.coef_)
    print("偏置：\n", estimator.intercept_)
    # 模型评估
    print("正规方程-均方误差: \n", mean_squared_error(y_test, estimator.predict(x_test)))
    return None


def sgd_regression():
    boston = load_boston()
    x_train, x_test, y_train, y_test = train_test_split(boston.data, boston.target, random_state=22)
    # 无量纲化
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)

    estimator = SGDRegressor(learning_rate="constant", eta0=0.01, max_iter=10000)
    estimator.fit(x_train, y_train)
    print("权重系数：\n", estimator.coef_)
    print("偏置：\n", estimator.intercept_)
    # 模型评估
    print("梯度下降-均方误差: \n", mean_squared_error(y_test, estimator.predict(x_test)))

    return None


def ridge_regression():
    # 岭回归，L2正则化
    boston = load_boston()
    x_train, x_test, y_train, y_test = train_test_split(boston.data, boston.target, random_state=22)
    # 无量纲化
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)

    estimator = Ridge(alpha=0.5, max_iter=10000)
    estimator.fit(x_train, y_train)
    print("权重系数：\n", estimator.coef_)
    print("偏置：\n", estimator.intercept_)
    # 模型评估
    y_predict = estimator.predict(x_test)
    print("预测结果：\n", y_predict - y_test)
    print("岭回归-均方误差: \n", mean_squared_error(y_test, y_predict))

    return None


if __name__ == '__main__':
    # 正规方程
    linear_regression()
    # 随机梯度下降
    sgd_regression()
    # 岭回归
    ridge_regression()
