from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


def nb_news():
    # 用朴素贝叶斯算法对新闻分类
    # 1. 获取数据
    news = fetch_20newsgroups(data_home='data/')
    # 2. 划分数据集
    x_train, x_test, y_trian, y_test = train_test_split(news.data, news.target)
    # 3. 特征工程：tfidf
    transfer = TfidfVectorizer()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)
    # 4. 朴素贝叶斯预估器流程
    estimator = MultinomialNB()
    estimator.fit(x_train, y_trian)
    # 5. 模型评估
    ## 5.1 知己比对真实值和预测值
    y_predict = estimator.predict(x_test)
    print("真实值对比预测值：\n", y_test == y_predict)
    ## 5.2 计算准确率
    score = estimator.score(x_test, y_test)
    print("准确率：\n", score)
    return None


if __name__ == '__main__':
    nb_news()
