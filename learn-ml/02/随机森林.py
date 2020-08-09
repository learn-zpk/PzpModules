from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import GridSearchCV, train_test_split
import pandas as pd


def random_forest():
    # 1. 获取数据
    titanic = pd.read_csv('./data/titanic.csv')
    x = titanic[['pclass', 'age', 'sex']]
    y = titanic['survived']
    # print(x.head(5))
    # 2. 数据处理
    x["age"].fillna(x["age"].mean(), inplace=True)
    x = x.to_dict(orient="records")
    # 3. 划分数据集
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=22)
    # 5. 特征工程:字典特征抽取
    transfer = DictVectorizer()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)

    estimator = RandomForestClassifier()
    param_dict = {
        'n_estimators': [120, 200, 300, 500, 800, 1200],
        'max_depth': [5, 7, 9, 11, 13, 15]
    }
    estimator = GridSearchCV(estimator, param_grid=param_dict, cv=3)
    estimator.fit(x_train, y_train)
    y_predict = estimator.predict(x_test)
    print("真实值对比预测值：\n", y_test == y_predict)

    score = estimator.score(x_test, y_test)
    print("准确率：\n", score)
    return None


if __name__ == '__main__':
    random_forest()
