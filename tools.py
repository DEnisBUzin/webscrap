import os
import datetime


# HW №1

def logger_HW_1(old_function):

    def new_function(*args, **kwargs):
        with open("main.log", "a", encoding="utf-8") as f:
            time_now = datetime.datetime.now()
            result = old_function(*args, **kwargs)
            f.writelines(f"{time_now} вызвана функция {old_function.__name__} c аргументами: {args}, {kwargs}."
                         f" Возвращаемое значение: {result}\n")
            return result

    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger_HW_1
    def hello_world():
        return 'Hello World'

    @logger_HW_1
    def summator(a, b=0):
        return a + b

    @logger_HW_1
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


# HW №2

def logger_HW_2(path):

    def __logger(old_function):

        def new_function(*args, **kwargs):
            with open(path, "a", encoding="utf-8") as f:
                time_now = datetime.datetime.now()
                result = old_function(*args, **kwargs)
                f.writelines(f"{time_now} вызвана функция {old_function.__name__} c аргументами: {args}, {kwargs}."
                             f" Возвращаемое значение: {result}\n")
            return result

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger_HW_2(path)
        def hello_world():
            return 'Hello World'

        @logger_HW_2(path)
        def summator(a, b=0):
            return a + b

        @logger_HW_2(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()
    test_2()