// 基础类型
(() => {
    // 布尔类型：boolean
    let flag: boolean = true;
    console.log(flag)
    // 数值类型: number
    let a1: number = 10;
    let a2: number = 0b1010;
    let a3: number = 0o12;
    let a4: number = 0x0a;
    console.log(a1, a2, a3, a4)
    // 字符串类型: string
    let str1: string = '我是个大垃圾'
    console.log(str1)
    // 字符串和数字拼接
    let str2 = str1 + a1;
    console.log(str2)

    // ts中变量定义是什么类型，只能赋值这个类型值

    // undefined和null都可以作为其他类型的子类型,strict模式要为false
    a2 = undefined
    a2 = null

    console.log(a2)

    // 数组类型：[]、Array<>
    let arr1: number[] = [10, 20, 30]
    let arr2: Array<number> = [100, 200, 300]

    // 元组类型：在定义数组的时候，数据的个数和类型一开始已经限定了
    let tuple1: [string, number, boolean] = ['张三', 100, true]

    // 枚举类型: 元组默认从0开始,也可以自定义数字
    enum Color {
        red = 10,
        green,
        blue
    }

    let color: Color = Color.green;
    console.log(color)

    // any: 当一个数组中存储多个数据，个数不确定、类型不确定可以用到
    let any1: any = 100;
    console.log(any1)
    any1 = 'any'
    console.log(any1)

    let arrAny: any[] = [100, '1131', true]

    // void: 函数声明的时候在函数后面用:void
    function showMsg(): void {
        console.log('测试void')
    }

    console.log(showMsg())

    // object类型
    function getObj(obj: object): object {
        console.log(obj)
        return {
            name: 'zzz',
            age: 222
        }
    }

    console.log(getObj({'aaa': 122}))

    // 联合类型: |
    // 类型断言: <类型>以及as 类型，告知编译器不要检测类型
    function getStringLength(str: number | string): number {
        if ((str as string).length) {
            return (str as string).length
        } else {
            return str.toString().length
        }
        // if ((<string>str).length) {
        //     return (<string>str).length
        // } else {
        //     return str.toString().length
        // }
    }

    console.log(getStringLength(123))
})()