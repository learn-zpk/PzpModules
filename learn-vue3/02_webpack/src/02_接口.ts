(() => {
    // 接口
    // 只读属性 readonly
    // 可选属性 ?
    interface IPerson {
        readonly id: number
        name: string
        age: number
        sex?: string
    }

    const person: IPerson = {
        id: 1,
        name: 'zzz',
        age: 20,
        // sex: '男'
    }
    console.log(person.sex)
})()