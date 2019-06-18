[toc]

## 数据类型
### 简单描述

|数据类型|描述|
|---|---|
|nil|无效值,条件表达式中相当于false|
|boolean||
|number|双精度实浮点数|
|string|双引号、单引号都可以表示|
|function|由C或lua编写的函数|
|userdata|任意存储在变量中的C数据结构|
|thread|执行的独立线路，用于执行协同程序|
|table|一个"关联数组"（associative arrays），数组的索引可以是数字、字符串或表类型|

### nil其他用处
- 对于全局变量和 table，赋值nil等同于删除
```lua
tab1 = { key1 = "val1", key2 = "val2", "val3" }
for k, v in pairs(tab1) do
    print(k .. " - " .. v)
end

tab1.key1 = nil
for k, v in pairs(tab1) do
    print(k .. " - " .. v)
end

--- 输出没有key1
```
- nil 作比较时应该加上双引号
- 条件表达式中nil类似于false(nil不等于false)

### number
- 默认双精度(double)类型
- 默认类型可以在luaconf.h中修改

### string
- 字符串连接用` .. `
- 取长度用`#xxx`
```lua
a='hello '
b='world!'
print(a .. b)
print(#(a .. b))
```

### table
- 数组的索引可以是数字或者是字符串
- 默认初始索引从1开始
```lua
b={a=1,2,c=3,4,d=5}
for k,v in pairs(b) do
   print(k .. '--' .. v)
end
```
- for paris先从数字索引输出，再输出字符串索引
- table 不会固定长度大小，有新数据添加时 table 长度会自动增长，没初始的 table 都是 nil。
- Table的组成: 
    1) 哈希表存储key-value键值对，哈希表冲突时通过链表组织冲突元素
    2) 数组存储非key-value数据
- ipairs从索引1开始遍历，不能断开，断开终止遍历
- pairs随机遍历，但一定会遍历整个表，遍历完成则终止
```lua
print('test pairs and ipairs')
local t = {
    [1] = 1,
    2,
    [3] = 3,
    4,
    [5] = 5,
    [6] = 6,
    [a]=7
}

for k, v in ipairs(t) do
    print("ipairs  " .. k .."-" .. v)
end

for k, v in pairs(t) do
    print("pairs  " .. k .."-" .. v)
end
--[[
    1. 根据元素类别分别存进哈希表、数组
        哈希表：{ [1]=1，[3]=3，[5]=5，[6]=6 }； 
        数组：{ 2，4 } 
    2. 将数组中的元素存入哈希表
        [1]=2与[2]=4
        [1] 冲突，重新赋值，最终得到{ [1]=2，[2]=4，[3]=3，[5]=5，[6]=6 }
    3. 
--]]

```
### function
- anonymous function
- 可以作为参数

### thread
- 协同程序（coroutine)
- ...

### userdata
- ...

## 变量
- 三种类型: 全局变量、局部变量、表中的域
- 默认全是全局变量、语句块或函数里的也是，显示声明local则为局部变量
- 变量默认是为nil
- 全局变量默认保存在`_G`这个table中
```lua
c='1'
print(_G['c'])
```
- 赋值时变量个数与值个数不一致时: 值少补nil，值多丢弃
```lua
a,b,c=1
print(a,b,c) --- 1 nil nil
a,b,c=1,2,3,4,5,6
print(a,b,c) --- 1 2 3
```

## 循环
|类型|描述|
|---|---|
|while|条件为true，重复执行|
|for|重复次数由for语句控制|
|repeat...util|重复执行直到条件为真为止|
|嵌套循环|上述三种组合|

```lua
while(i>10)
do
    i=i+1
    print("while"..i)
end 

for i=10,1,-1
do
    print("for"..i)
end 
```

## 流程控制
```lua
a = 0
if (a == 0) then
    print("a为0")
elseif(a==1) then
    print("a为1")
else
    print("a不为0或1")
end
```

## 函数
```
optional_function_scope function function_name( argument1, argument2, argument3..., argumentn)
    function_body
    return result_params_comma_separated
end
```
- optional_function_scope: 默认为全局变量，显示声明local则为局部函数
- result_params_comma_separated: 可以返回多个值，以逗号隔开

- 可变参数，用`...`表示,获取可变参数个数`select('#', ...)`或`#{...}`
```lua
function average(...)
    local result = 0
    print(...)
    for k, v in ipairs({ ... }) do
        result = result + v
    end
    -- return result / #{...}
    return result / select('#', ...)
end

print("平均值为" .. average(6, 7, 8, 2, 5, 4, 3))
```
