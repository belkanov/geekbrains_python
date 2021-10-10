"""
    *(вместо 6) Добавить возможность редактирования данных при помощи отдельного скрипта: передаём ему номер записи и новое значение.
    При этом файл не должен читаться целиком — обязательное требование.
    Предусмотреть ситуацию, когда пользователь вводит номер записи, которой не существует.
"""
from sys import argv, exit
from os import linesep


def rewrite_data(file, old_data, new_data, start_cursor):
    """
    Этот алгоритм ни разу не эффективен для массовой замены (тогда надо делать поиск неполных данных во время чтения чанка).
    Писался под конкретную задачу разовой замены с условием отсутствия чтения всего файла целиком.

    Так же на текущий момент обучения мы не рассматривали работу с файловой системой - можно было бы писать в новый файл, а потом сделать переименование.
    Алгоритм был бы проще, но затратней в плане дискового пространства: надо как минимум иметь столько же свободного места как и первоначальный файл,
    а если файл большой - могут возникнуть сложности вплоть до отсутствия возможности создать новый файл (не влезет)

    ветку if data_len_diff > 0 можно сделать похожей на elif data_len_diff < 0, только работать надо будет с конца

    В общем много всяких "если"..

    Опираясь на комменты ниже при наших обьемах данных, можно разово прочитать блок в 10 мб (chunk = file.read(10 * 1024 * 1024))
    сделать реплейс и записать - все будет ок. При этом технически файл целиком читаться не будет (мы как минимум прочитаем первую строчку отдельно),
    что таки будет соответствовать условиям задачи =)
    Если же данных будет больше чем на 1 блок (блк 10мб - файл 20мб), то тут важно учитывать смещеные данных при записи блоками.
    Я для себя решил проработать этот момент сведя блок к 10 байтам
    С размером блока связаны ограничения в макс. длину заменяемой инфы:
    Для 10 байт это 123,4567 (8 символов + 2 управляющих \r\n если речь про utf8 и винду)
    По хорошему длину блока, конечно, надо выбирать не меньше длины заменяемой инфы, но у нас тут учеба и "тесты", а не продакшн и боль =)
    """
    chunk_len = 10
    is_end_line = False if bytes(linesep, 'utf8') in old_data else True  # если в найденной линии нет переноса строки - это конец файла
    new_data = bytes((new_data + linesep) if not is_end_line else new_data, 'utf8')
    data_len_diff = len(new_data) - len(old_data)
    file.seek(start_cursor)
    chunk = file.read(chunk_len)
    file.seek(start_cursor)
    if data_len_diff > 0:  # если замена больше старых данных
        tmp_data = chunk[-data_len_diff:]  # сохраняем лишние (вылезают за chunk_len) данные
        chunk = chunk[:chunk_len - data_len_diff]  # обрезаем их
        file.write(chunk.replace(old_data, new_data, 1))  # меняем инфу
        while True:
            cur_cursor = file.tell()
            chunk = file.read(chunk_len)
            if not chunk:
                break
            chunk = tmp_data + chunk  # добавляем данные от прошлого chunk
            tmp_data = chunk[-data_len_diff:]  # сохраняем новые лишние
            file.seek(cur_cursor)
            file.write(chunk[:chunk_len] if len(chunk) > chunk_len else chunk)  # обрезаем лишнее и записываем
    elif data_len_diff < 0:  # если замена меньше старых данных
        file.write(chunk.replace(old_data, new_data, 1))  # меняем инфу + записываем
        if is_end_line:
            file.truncate()  # если мы пишем в конец файла - сразу обрезаем остатки
        else:
            file.seek(-data_len_diff, 1)  # сдвигаем курсор вперед, чтобы он был в ровень с длиной чанка
            while True:
                cur_cursor = file.tell()
                chunk = file.read(chunk_len)  #
                if not chunk:
                    # тут мы можем попасть в ситуацию, когда после вставки мы окажемся прямо в конце файла
                    file.seek(file.tell() + data_len_diff)  # поэтому сдвигаем курсор назад
                    file.truncate()  # и обрезаем файл
                    break
                next_cursor = file.tell()  # сохраняем позицию начала след. чанка
                file.seek(cur_cursor + data_len_diff)  # просто сдвигаем текущий чанк на разницу при замене данных
                file.write(chunk)
                if len(chunk) < chunk_len:
                    file.truncate()  # обрезаем файл
                file.seek(next_cursor)  # и идем к следующему, который так же сдвинем.
    else:  # если новая инфа по длинне такая же как и старая
        file.write(chunk.replace(old_data, new_data, 1))  # меняем инфу


def edit_data(*args):
    if len(args) != 3:
        print('Указано неверное количество параметров.')
        return 1
    line_to_change = int(args[1]) - 1
    if line_to_change < 0:
        print('Номер строки должен быть >= 1')
        return 1
    with open('bakery.csv', 'br+') as f:
        # f.tell() не работает в итерациях, поэтому так
        line_idx = 0
        while True:
            cursor_to_start_cur_line = f.tell()
            # можно конечно считать не построчно, а искать '\n' с нужным индексом в блоке по несколько десятков/сотен МБ
            # подозреваю, что такой вариант будет работать бодрее на больших файлах
            # но в рамках нашей задачи, можно условиться, что будет одна запись в день (вряд ли сумму продаж будут писать каждую минуту или каждый час)
            # тогда БД за год будет всего 3.5кБ (10 строчек ~ 0.1кБ), а за 100 лет - 350кБ
            # поэтому я решил сделать так
            cur_line = f.readline()
            if not cur_line:
                break
            if line_idx == line_to_change:
                return rewrite_data(f, cur_line, args[2], cursor_to_start_cur_line)
            line_idx += 1

    print(f'Указанной строки ({args[1]}) не найдено в файле.')
    return 1


if __name__ == '__main__':
    exit(edit_data(*argv))