import jieba
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from scipy.stats import pearsonr


def datasets_demo():
    # 获取数据集
    iris = load_iris()
    print("鸢尾花数据集：\n", iris)
    print('查看数据集描述：\n', iris['DESCR'])
    print('查看特征值信息：\n', iris.feature_names)

    # 数据集划分
    x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=22)
    print(x_train.shape)


def dict_demo():
    # 字典特征提取
    data = [{'city': '上海', 'temperature': 100}, {'city': '北京', 'temperature': 60}, {'city': '深圳', 'temperature': 80}]
    transfer = DictVectorizer(sparse=False)
    data_new = transfer.fit_transform(data)
    print("特征提取结果:\n", data_new)

    print("特征名称:\n", transfer.get_feature_names())
    return None


def text_count_demo():
    data = ['life is short,i like python like', 'list is too long,i dislike python']
    transfer = CountVectorizer()
    data_new = transfer.fit_transform(data)

    print("特征提取结果:\n", data_new.toarray())

    print("特征名称:\n", transfer.get_feature_names())
    return None


def ch_count_demo():
    data = ['我爱北京天安门', '天安门上太阳升']
    transfer = CountVectorizer()
    data_new = transfer.fit_transform(data)

    print("特征提取结果:\n", data_new.toarray())

    print("特征名称:\n", transfer.get_feature_names())
    return None


def cut_word(text):
    return " ".join(list(jieba.cut(text)))


def ch_count_demo2():
    # 中文需要借助分词：jieba等
    data = [cut_word(_) for _ in ['我爱北京天安门', '天安门上太阳升']]
    transfer = CountVectorizer(stop_words=['北京'])
    data_new = transfer.fit_transform(data)

    print("特征提取结果:\n", data_new.toarray())

    print("特征名称:\n", transfer.get_feature_names())
    return None


def tfidf_demo():
    # 用tfidf方法进行文本特征处理
    data = [cut_word(_) for _ in ["今天很残酷,明天更残酷，后天很美好，但大部分人都死在明天晚上。所以每个人不要放弃今天",
                                  '我们看到的从很远星系来的光是在几百万年之前发出的，这样当我们看到宇宙时，我们是在看它的过去',
                                  '如果只用一种方式去了解某样事物，你就不会真正了解它。了解事物真正含义的秘密取决于如何将其与我们所了解的事物相联系。']]
    transfer = TfidfVectorizer(stop_words=['一种'])
    data_new = transfer.fit_transform(data)

    print("特征提取结果:\n", data_new.toarray())

    print("特征名称:\n", transfer.get_feature_names())
    return None


def minmax_demo():
    # 归一化
    data = pd.read_csv('data/dating.txt')
    print("data:\n", data)
    data = data.iloc[:, :3]
    # feature_range可指定范围，默认[0,1]
    transfer = MinMaxScaler()
    data_new = transfer.fit_transform(data)
    print("归一化结果:\n", data_new)

    return None


def standard_demo():
    # 标准化
    data = pd.read_csv('data/dating.txt')
    print("data:\n", data)
    data = data.iloc[:, :3]
    transfer = StandardScaler()
    data_new = transfer.fit_transform(data)
    print("标准化结果:\n", data_new)

    return None


def variance_demo():
    # 过滤低方差特征
    data = pd.read_csv('data/factor_returns.csv')
    data = data.iloc[:, 1:-2]
    print('data.shape:\n', data.shape)
    transfer = VarianceThreshold(threshold=1)
    data_new = transfer.fit_transform(data)
    # 计算相关系数
    r = pearsonr(data['pe_ratio'], data['pb_ratio'])
    print('相关系数:\n', r)
    print("data_new:\n", data_new, data_new.shape)


def pca_demo():
    # pca降维
    data = [[2, 8, 4, 5], [6, 3, 0, 8], [5, 4, 9, 1]]
    # transfer = PCA(n_components=2)
    transfer = PCA(n_components=0.95)
    data_new = transfer.fit_transform(data)
    print("data_new:\n", data_new, data_new.shape)
    return None


if __name__ == '__main__':
    # datasets_demo()
    # 2. 字典特征提取
    # dict_demo()
    # 3. 文本特征提取：统计
    # text_count_demo()
    # 4. 中文文本特征提取
    # ch_count_demo()
    # 5. 中文文本特征提取,分词
    # ch_count_demo2()
    # 6. tfidf文本特征提取
    # tfidf_demo()
    # 7. 归一化
    # minmax_demo()
    # 8. 标准化
    # standard_demo()
    # 9. 低方差特征过滤
    # variance_demo()
    # 10. PCA降维
    pca_demo()
