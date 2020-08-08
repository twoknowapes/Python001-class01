##### 类的创建
* 类：一群有着相同属性和函数的对象的集合
* 对象：集合中的一个事物
* 属性：对象的某个静态特征
* 函数：对象的某个动态能力
##### 四大特性
###### 封装
###### 抽象
* 接口协议
1. 不能包含属性
2. 只能声明方法且不能包含代码实现
3. 类实现必须实现接口中声明的所有方法
* 抽象基类
1. 不允许被实例化而只能被继承
2. 可以包含属性和方法
3. 子类继承必须实现抽象类中的所有抽象方法
* 实践原则：基于接口而非实现编程
1. 函数的命名不能暴露任何实现细节
2. 封装具体的实现细节
3. 为实现类定义抽象的接口
###### 继承
* 继承优缺
* 实践原则：多用组合少用继承
###### 多态
#### 迭代生成
##### 容器
##### 可迭代对象
```
def is_iterable(param):
    """
    1. 自定义判断一个对象是否可迭代；
    2. isinstance(obj, iterable)。
    """
    try:
        iter(param)
        return True
    except TypeError:
        return False

params = [
    1234,
    '1234,',
    [1, 2, 3, 4],
    (1, 2, 3, 4),
    {1: 2, 2: 2, 3: 3, 4: 4},
    set([1, 2, 3, 4])
]

for param in params:
    print('{} is iterable: {}'.format(param, is_iterable(param)))
    
########## 输出 ##########

1234 is iterable: False
1234, is iterable: True
[1, 2, 3, 4] is iterable: True
(1, 2, 3, 4) is iterable: True
{1: 2, 2: 2, 3: 3, 4: 4} is iterable: True
{1, 2, 3, 4} is iterable: True
```
##### 迭代器：从集合中取出元素
```
import os
import psutil

def show_memory_info(hint):
    pid = os.getgid()
    p = psutil.Process(pid)

    info = p.memory_full_info()
    memory = info.uss / 1024. / 1024
    print('{} memory used: {} MB'.format(hint, memory))

def test_iterator():
    show_memory_info('initing iterator')
    list_1 = [i for i in range(100000000)]
    show_memory_info('after iterator initiated')
    print(sum(list_1))
    show_memory_info('after sum called')

def test_generator():
    show_memory_info('initing generator')
    list_2 = [i for i in range(100000000)]
    show_memory_info('after generator initiated')
    print(sum(list_2))
    show_memory_info('after sum called')


%time print(test_iterator())
%time print(test_generator())
```
##### 生成器：用于凭空生成元素
```
def gen_AB():
    print('start')
    yield 'A'
    print('continue')
    yield 'B'
    print('end')
    
    
for c in gen_AB():
    print('-->', c)
    
########## 输出 ##########

start
--> A
continue
--> B
end
```
```
def add(n, i):
    retunr n + 1
    
def test():
    for i in range(4):
        yield i
        
        
g = test()

for n in [1, 10, 5]:
    g = (add(n, i) for i in g)
   
print(list(g)) # [15, 16, 17, 18]
'''
n = 1 -> 生成器表达式尚未执行
n = 10 -> 生成器表达式尚未执行
n = 5 -> 生成器表达式开始执行
g = (add(n, i) == (15, 16, 17, 18)
    for i in (add(n, i) == (11, 12, 13, 14)
        for i in (add(n, i) == (6, 7, 8, 9)
            for i in test()))) == (0, 1, 2, 3)
'''
```