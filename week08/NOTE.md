#### 对象解析
##### [对象操作](https://www.jianshu.com/p/5cf2aebdf7c5)
###### 比较
* '=='：比较对象之间的值是否相等
* 'is'：比较对象身份标识是否相等
###### 赋值
* 不可变对象的赋值 -> 直接传递对象本身
1. 在缓存范围内
2. 不在缓存范围
* 可变对象的赋值 -> 传递这个对象的引用
###### 切片
* 对”不可变对象的子元素“的操作不会影响另一对象
* 对“可变对象的子元素“的操作会影响另一对象
###### 拷贝
* 浅拷贝：原对象中子对象的引用
1. 对不可变对象进行浅拷贝 -> 相当于深拷贝（即赋值）
2. 对可变对象进行浅拷贝 -> 相当于完全切片
* 深拷贝：递归地拷贝原对象中的每一个子对象
1. 不可变对象的深拷贝
2. 可变对象的深拷贝
##### 垃圾回收
###### 计数引用：充分非必要
###### 循环引用：不可达判定
###### 内存泄漏
#### 类的初探
#### 函数对象
##### 一等函数
###### 定义函数
* 简单定义
```
def fib(n):
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a + b
    return result


f = fib(100)
print(f) # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
```
* 四个原则
1. 函数设计要尽量短小且嵌套层次不宜过深
2. 函数声明应该做到合理、简单、易用
3. 函数参数设计应该考虑向下兼容
4. 一个函数只做一件事以保证函数粒度的一致性
* 位置参数
1. 必须按正确的顺序传递到函数中
2. 调用时的数量和位置必须和定义时一致
###### 参数传递
* 赋值传递
1. C++
1.1 值传递：拷贝参数的值-原变量和新变量之间互相独立
1.2 引用传递：把参数的引用传给新的变量-指向同一块内存地址
2. Python：赋值传递：让新变量与原变量指向相同的对象
```
def my_func1(b):
  b = 2

a = 1
my_func1(a)
a # 1
```
```
def my_func2(b):
  b = 2
  return b

a = 1
a = my_func2(a)
a # 2
```
```
def my_func3(l2):
  l2.append(4)

l1 = [1, 2, 3]
my_func3(l1)
l1 # [1, 2, 3, 4]
```
```
def my_func4(l2):
  l2 = l2 + [4]

l1 = [1, 2, 3]
my_func4(l1)
l1 # [1, 2, 3]
```
```
def my_func5(l2):
  l2 = l2 + [4]
  return l2

l1 = [1, 2, 3]
l1 = my_func5(l1)
l1 # [1, 2, 3, 4]
```
* 默认参数
1. 默认参数在定义函数时定义
2. 调用时如果没有传递参数则会使用默认参数
3. 默认参数只会执行一次（在默认值为可变对象时很重要）
```
def default_argument(a, b=[]):
    b.append(a)
    return b


print(default_argument(1)) # [1]
print(default_argument(2)) # [1, 2]
```
* 关键字参数
1. 使用形参来确定输入的参数值且必须跟在位置参数后
1.1 \*arg：把多出的位置参数转化为元组
1.2 \*\*kwarg：把关键字参数转化为字典
2. 调用时以 kwarg=value 的形式来指定
2.1 * 解包元组
2.2 ** 解包字典
```
def keyword_arguments(a, *b, **c):
    print(a)
    print(b)
    print(c.keys())


keyword_arguments(a=1, b=2, c=3)

########## 输出 ##########

1
()
dict_keys(['b', 'c'])
```
```
def argument_lists(a, b, c):
    print(a)
    print(b)
    print(c)


dic = {'a': 1, 'b': 2, 'c': 3}
argument_lists(**dic)

########## 输出 ##########

1
2
3
```
* 特殊参数
1. 位置或关键字参数
2. / 之前参数只能是位置参数
3. \* 之后参数只能是关键字参数
```
def special_parameters(*, a):
    print(a)


special_parameters(a=1)

########## 输出 ##########

1
```
###### 高阶函数
* lambda 表达式
```
def make_incrementor(n):
    return lambda x: x + n


f = make_incrementor(42)
print(f(0))
print(f(1))
```
###### 函数内省
###### 函数注解
```
def f(ham: str, eggs: str = 'eggs') -> str:
    print('Annotations:', f.__annotations__)
    print('Arguments:', ham, eggs)
    return ham + ' and ' + eggs


f('spam')
```
###### [内置函数](https://docs.python.org/3.10/library/functions.html)
##### 设计模式
##### 装饰器和闭包
###### 命名空间
* 命名空间：一个从名字到对象的映射
* 作用域：一个命名空间可直接访问的文本区域
1. 局部作用域：最先搜索的最内部作用域包含局部名称
2. 嵌套作用域：最近封闭作用域开始搜索的任何封闭函数的作用域
3. 全局作用域：倒数第二个作用域包含当前模块的全局名称
4. 内置作用域：最外面的作用域（最后搜索）包含内置名称的命名空间
```
def scope_test():
    def do_local():
        spam = 'local spam'

    def do_nonlocal():
        nonlocal spam
        spam = 'nonlocal spam'

    def do_global():
        global spam
        spam = 'globla spam'

    spam = 'test spam'
    do_local()
    print('After local assignment:', spam)
    do_nonlocal()
    print('After nonlocal assignment:', spam)
    do_global()
    print('After global assignment:', spam)


scope_test()
print('In global scope:', spam)
```
###### 把函数赋予变量
###### 函数当作参数传入另一个函数中
###### 在函数里定义函数
###### 函数返回值也可以是函数对象（闭包）
###### 装饰器
* 简单的装饰器
* 带参的装饰器
* 自定义参数
* 内置装饰器
* 类装饰器
* 嵌套装饰器
* metaclass：超越变形特性