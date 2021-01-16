(() => {
    // 函数类型
    interface ISearchFunc {
        //定义一个调用签名
        (source: string, subString: string): boolean
    }

    const searchString: ISearchFunc = function (source: string, subString: string): boolean {
        return source.search(subString) >= -1
    }

    console.log(searchString('1222', '22'))
})()