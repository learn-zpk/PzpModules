// ts：类
(() => {
    interface IPerson {
        firstName: string
        lastName: string
    }

    class Person {
        firstName: string
        lastName: string
        fullName: string

        constructor(firstName: string, lastname: string) {
            this.firstName = firstName
            this.lastName = lastname
            this.fullName = firstName + '_' + lastname
        }
    }

    function showFullName(person: Person) {
        return person.fullName
    }

    const person = new Person('东方', '不败')
    console.log(showFullName(person))
})()