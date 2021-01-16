(() => {
    // 类
    // 类的类型可以通过接口实现
    interface IFly {
        fly()
    }

    interface ISwim {
        swim()
    }

    // 类可以实现多个接口  implements
    class Person implements IFly, ISwim {
        fly() {
            console.log('我能飞')
        }

        swim() {
            console.log('我不会游泳')
        }
    }

    const person = new Person()
    person.fly()

    //接口还可以继承其他的接口 extends
    interface IFlyAndSwim extends IFly, ISwim {
    }

    class Person2 {
        name: string
        age: number
        gender: string

        constructor(name: string, age: number, gender: string = '男') {
            this.name = name
            this.age = age
            this.gender = gender
        }

        sayHi(str: string) {
            console.log(`hi,${str},${this.name},${this.age},${this.gender}`)
        }
    }

    const person2 = new Person2('xxx', 11)
    person2.sayHi('lala')

    // 类继承：extends
    class Student extends Person2 {
        constructor(name: string, age: number, gender: string) {
            super(name, age, gender);
        }

        sayHi() {
            // 调用父类的方法
            super.sayHi('student');
        }
    }

    const student = new Student('xxx', 11, '女')
    student.sayHi()


    class Animal {
        name: string

        constructor(name: string) {
            this.name = name
        }

        run(distance: number = 0) {
            console.log(`${distance},${this.name}`)
        }
    }

    class Dog extends Animal {
        constructor(name: string) {
            super(name);
        }

        run(distance: number = 0) {
            console.log(`dog: ${distance},${this.name}`)
        }
    }

    class Pig extends Animal {
        constructor(name: string) {
            super(name);
        }

        run(distance: number = 0) {
            console.log(`pig: ${distance},${this.name}`)
        }
    }

    const ani: Animal = new Animal('动物')
    ani.run(111)
    const dog: Dog = new Animal('狗')
    dog.run(222)
    const pig: Pig = new Animal('猪')
    pig.run(333)

    // 多态：使用父类的类型创建子类对象
    const dog1: Animal = new Animal('狗')
    dog1.run(222)
    const pig1: Pig = new Animal('猪')
    pig1.run(333)

    function showRun(ani: Animal) {
        ani.run()
    }

    showRun(dog1)
    showRun(pig1)

    // 类修饰符：public、protected、private，默认是public
    // private: 只有当前类的方法可访问
    // protected：当前类及子类可访问

    // readonly修饰的类属性不能随意修改，构造函数中可以修改
    class Person4 {
        // name:string
        // 构造函数中的参数使用readonly后，该属性就变成一个只读类成员属性
        constructor(readonly name: string = 'xxx') {
            this.name = name
        }

        // 构造函数中的参数使用protected/public/private后，该属性就变成一个protected/public/private的类成员属性
        // constructor(protected name: string = 'xxx') {
        //     this.name = name
        // }
    }

    const person4: Person4 = new Person4('xx')
    // person4.name='xxxx'
    console.log(person4.name)

    // 存取器: get set
    class Person5 {
        firstName: string
        lastName: string

        constructor(firstName: string, lastName: string) {
            this.firstName = firstName
            this.lastName = lastName
        }

        get fullName() {
            return this.firstName + ' ' + this.lastName
        }

        set fullName(fullname: string) {
            [this.firstName, this.lastName] = fullname.split(' ')
        }
    }

    const person5 = new Person5('张', '三')
    console.log(person5.fullName)
    person5.fullName = '李 四'
    console.log(person5.fullName)

    // 静态属性及静态方法：static

    // 抽象类abstract: 包含抽象方法、也可以包含实例方法
    abstract class AbstractAnimal {
        abstract eat()
        sayHi(){
            console.log('xxx')
        }
    }


})()
