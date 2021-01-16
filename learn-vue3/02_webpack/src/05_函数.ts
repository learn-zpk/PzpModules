(() => {
    // 函数
    // 函数的定义
    function add(x: number, y: number): number {
        return x + y
    }

    const add2 = function (x: number, y: number): number {
        return x + y
    }

    const add3: (x: number, y: number) => number = function (x: number, y: number): number {
        return x + y
    }
    // 可变参数及默认参数
    const getFullName = function (firstName: string = '张', lastName?: string): string {
        if (lastName) {
            return firstName + ' ' + lastName
        } else {
            return firstName
        }
    }

    console.log(getFullName('张', '三'))

    // 剩余参数
    function showMsg(str: string, ...args: string[]) {
        console.log(str)
        console.log(args)
    }

    showMsg('a', 'b', 'c', 'd')

    // 重载函数：函数名字相同，参数及个数不同

    // 泛型
    // function getArr(value: number, count: number): number[] {
    //     const arr: number[] = []
    //     for (let i = 0; i < count; i++) {
    //         arr.push(value)
    //     }
    //     return arr
    // }
    function getArr<T>(value: T, count: number): T[] {
        //const arr: T[] = []
        const arr: Array<T> = []
        for (let i = 0; i < count; i++) {
            arr.push(value)
        }
        return arr
    }

    const arr1 = getArr('100.123', 3)
    console.log(arr1)

    // 多个泛型参数的函数:大写字母
    function getMsg<T, V>(value1: T, value2: V): [T, V] {
        return [value1, value2]
    }

    const arr2 = getMsg<string, number>('jack', 100.23)
    console.log(arr2[0].split(''), arr2[1].toFixed(1))
})()