// 1. 可利用tsc 1.ts编译此文件为1.js
(() => {
    function sayHi(str: string) {
        return 'say hi ' + str
    }

    let text = 'ok'
    // let text = [1, 2, 3]
    console.log(sayHi(text))
})()
// 2. ts是强类型语法，ide会智能提示类型错误等信息