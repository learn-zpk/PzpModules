class AbstractIpExtract():
    def __init__(self):
        self.free_list = []

    def extract(self, **kwargs):
        raise NotImplementedError("<< extract ip list from url_list >> not implemented")

    def save(self):
        # 保存免费ip列表
        pass
        print(self.free_list)
