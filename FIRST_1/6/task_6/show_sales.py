from sys import argv, exit


def show_data(*args):
    if len(args) > 3:
        print('Указано слишком много параметров.')
        return 1
    # про проверку входный данных на данном этапе речи не было, так что считаем,
    # что у нас идеальный пользователь, который не вводит всякую дичь =)
    start_line = 0 if len(args) < 2 else int(args[1])-1
    end_line = None if len(args) < 3 else int(args[2])-1
    with open('bakery.csv', encoding='utf8') as f:
        for idx, line in enumerate(f):
            if start_line <= idx and (end_line is None or idx <= end_line):
                print(line.strip())
    return 0


if __name__ == '__main__':
    exit(show_data(*argv))
