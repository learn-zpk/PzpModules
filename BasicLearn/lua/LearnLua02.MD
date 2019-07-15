[toc]

## 字符串
- 基本格式
     - 单引号: `'"lua"'`
     - 双引号: `"'lua'"`
     - [[]]:`[["lua"'lua']]`
     
- 操作
     - string.gsub(str,findstr,replacestr,num): num为替换的次数，默认全部替换,返回包括新的字符串以及替换的次数
     - string.find(str,substr,[start,[end]]): 获取substr出现的具体位置(起始与结束为止)，不存在返回nil，下标从1开始
     - string.gmatch(str, pattern): 返回一个在字符串 str 找到的下一个符合 pattern 描述的子串，没找到返回nil
     - string.match(str, pattern, init): 返回符合 pattern 描述的第一个子串，没找到返回nil

```lua
print(string.gsub('aaaabbbcc','a','A',3)) --AAAabbbcc      3
print(string.gsub('aaaabbbcc','a','A')) --AAAabbbcc      4 
print(string.find('aabbbccccdddaaa','aaa',4)) --13      15
for word in string.gmatch("Hello Lua user", "%a+")
do
    print(word)
end
```

## 数组
- 数组默认的索引值是1，可以指定0或者负数的索引
```lua
array={'aa','bb'}
print(array[-1]) --nil

for i= -2, 2 do
    array[i] = i *2
end
print(array[-2],array[2]) -- -4      4
```

## 迭代器
- 无状态迭代器: 迭代函数都是用两个变量（状态常量和控制变量）的值作为参数被调用,一个无状态的迭代器只利用这两个值可以获取下一个元素
```lua
function iter(a, i)
    local v = a[i + 1]
    --print(i)
    if v then
        return i + 1, v
    end
end

function ipairs(a)
    return iter, a, 0
end
-- 第二个参数一直递增
for k, v in ipairs({ 1, 2, 3 }) do
    print(k, v)
end


```
-- 多状态的迭代器: 使用闭包实现
```lua
function elemIterator(data)
    local index = 0
    local count = #data

    return function()
        index = index + 1
        if index <= count then
            return data[index]
        end
    end
end

for elem in elemIterator({ 1, 2, 3 })
do
    print(elem)
end
print(index)
for elem in elemIterator({ 4, 6, 8, 10 })
do
    print(elem)
end
print(index)
```

## 闭包
```lua
function Create(n)
   local function foo1()
      print(n)
   end
   local function foo2()
      n = n + 10
   end
   return foo1,foo2
end
-- n这个upvalue(即不是全局变量也不是局部变量)由内部函数fool与foo2共享

f1,f2 = Create(2015)
f1() --2015

f2()
f1() --2025
```

## table
- table.concat(table,[,sep[,start,[,end]]]): 拼接table中的数组部分，sep为拼接符
- table.insert(table, [pos,] value): (数组部分)指定的数组位置插入数据
- table.remove(table [, pos]): 删除数组部分中一个元素
```lua
print(table.concat({ 'a','b','c','d',4}, '@@',1,5)) --a@@b@@c@@d@@4
xx = { a = 1, 4, b = 2, c = 3, 5 }
table.insert(xx, 2, 1)
for k, v in ipairs(xx) do
    print(k .. v)
end
--[[
14
21
35
--]]
table.remove(xx, 2)
for k, v in ipairs(xx) do
    print(k .. v)
end
--[[
14
35
--]]
```