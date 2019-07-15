local x = 'Lua'
print(string.lower(x))
print(string.upper(x))

print(string.gsub('aaaabbbccccdddaaa', 'a', 'A', 3))
print(string.gsub('aaaabbbccccdddaaa', 'a', 'A'))
print(string.find('aabbbccccdddaaa', 'aaa', 4))

-- 返回迭代器
for word in string.gmatch("Hello Lua user", "%a+")
do
    print(word)
end

-- 返回匹配的第一个参数
print(string.match("I have 2 questions for you.", "%d+ %a+"))

-- 数组
array = { 'aa', 'bb' }
print(array[-1]) --nil

for i = -2, 2 do
    array[i] = i * 2
end
print(array[-2], array[2]) -- -4      4


-- 多维数组
array = {}
for i = 1, 3 do
    array[i] = {}
    for j = 1, 3 do
        array[i][j] = i * j
    end
end
for i = 1, 3 do
    for j = 1, 3 do
        print(array[i][j])
    end
end

-- 无状态的迭代器
function iter(a, i)
    local v = a[i + 1]
    if v then
        return i + 1, v
    end
end

function ipairs2(a)
    return iter, a, 0
end

for k, v in ipairs2({ 1, 2, 3 }) do
    print(k, v)
end

for k, v in iter, { 1, 2, 3 }, 0 do
    print('iter' .. k, v)
end


--多状态的迭代器
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

-- 闭包

function Create(n)
    local function foo1()
        print(n)
    end
    local function foo2()
        n = n + 10
    end
    return foo1, foo2
end
-- n这个upvalue(即不是全局变量也不是局部变量)由内部函数fool与foo2共享
f1, f2 = Create(2015)
f1() --2015

f2()
f1() --2025

-- table
print(table.concat({ 'a', 'b', 'c', 'd', 4 }, '@@', 1, 5))
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