from abc import ABCMeta, abstractmethod


class Zoo(object):

    def __init__(self, name):
        self.animals = []
        self.zoo_name = name

    def add_animals(self, animal):
        if animal in self.animals:
            return self.animals[animal]
        else:
            self.animals.append(animal)
            self.__dict__[type(animal).__name__] = animal


class Animals(metaclass=ABCMeta):
    size = {
        '小型': 1,
        '中型': 2,
        '大型': 3
    }
    is_meat = {
        '食肉': True,
        '食草': False,
        '杂食': False
    }
    is_fierce = {
        '凶猛': True,
        '温顺': False
    }

    @abstractmethod
    def __init__(self, size, is_meat, is_fierce):
        self.size = size
        self.is_meat = is_meat
        self.is_fierce = is_fierce

        if self.size != '1' and self.is_meat == True and self.is_fierce == True:
            self.is_fierce_animal = True
        else:
            self.is_fierce_animal = False


class Cat(Animals):
    sound = '喵喵喵'

    def __init__(self, name, size, is_meat, is_fierce):
        super(Cat, self).__init__(size, is_meat, is_fierce)
        self.name = name
        self.is_suitable_pet = 'YES'


if __name__ == '__main__':
    z = Zoo('时间动物园')

    cat = Cat('大花猫', '食肉', '小型', '凶猛')
    print(f'Cat sounding: "{Cat.sound}')
    print(f'cat is pet: {cat.is_fierce_animal}')
    print(f'cat is beast: {cat.is_fierce_animal}')

    z.add_animals(cat)
    has_cat = getattr(z, 'Cat')
    print(f'zoo has cat: {bool(has_cat)}')
