from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz


def decision_iris():
    iris = load_iris()
    x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, random_state=22)
    estimator = DecisionTreeClassifier(criterion='entropy')
    estimator.fit(x_train, y_train)
    y_predict = estimator.predict(x_test)
    print("真实值对比预测值：\n", y_test == y_predict)

    score = estimator.score(x_test, y_test)
    print("准确率：\n", score)
    # 导出决策树
    export_graphviz(estimator, out_file='./data/tree.dot', feature_names=iris.feature_names)
    return None


if __name__ == '__main__':
    decision_iris()
