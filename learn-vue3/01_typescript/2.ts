// ts：类
(() => {
    interface IPerson {
        firstName: string
        lastName: string
        sayHi: () => string
    }

    function showFullName(person: IPerson) {
        return person.firstName + '_' + person.lastName
    }

    const person: IPerson = {
        firstName: '东方',
        lastName: '不败',
        sayHi: (): string => {
            return "Hi there"
        }
    }
    console.log(showFullName(person))
    console.log(person.sayHi())
})()