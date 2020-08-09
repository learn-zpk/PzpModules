import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def logistic_regression():
    # 读取数据
    data = pd.read_csv(
        './data/breast-cancer-wisconsin.data',
        names=['Sample code number', 'Clump Thickness', 'Uniformity of Cell Size', 'Uniformity of Cell Shape',
               'Marginal Adhesion', 'Single Epithelial Cell Size', 'Bare Nuclei', 'Bland Chromatin',
               'Normal Nucleoli', 'Mitoses', 'Class']
    )
    # 缺失值处理
    data.replace(to_replace="?", value=np.nan, inplace=True)
    data.dropna(inplace=True)
    # 划分数据集
    x = data.iloc[:, 1:-1]
    y = data["Class"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=22)
    # 特征工程
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)

    # 模型训练
    estimator = LogisticRegression()
    estimator.fit(x_train, y_train)

    print("权重系数：\n", estimator.coef_)
    print("偏置：\n", estimator.intercept_)

    # 模型评估
    y_predict = estimator.predict(x_test)
    print("预测结果：\n", y_predict)
    print("真实值对比预测值：\n", y_test == y_predict)
    score = estimator.score(x_test, y_test)
    print("准确率：\n", score)

    # 精确率、召回率、F1因子
    report = classification_report(y_test, y_predict, labels=[2, 4], target_names=["良性", "劣性"])
    print("精确率、召回率、F1因子指标：\n", report)
    # AUC
    y_true = np.where(y_test > 3, 1, 0)
    print("AUC指标：", roc_auc_score(y_true, y_predict))

    # 保存模型
    joblib.dump(estimator, './data/model.pkl')
    return None


def load_model():
    estimator = joblib.load('./data/model.pkl')
    print(estimator.coef_)
    print(estimator.intercept_)


if __name__ == '__main__':
    # logistic_regression()
    load_model()
