import requests
from requests.exceptions import Timeout

DEFAULT_CONN_TIMEOUT = 5
DEFAULT_READ_TIMEOUT = 5


def get_response(url, params=None, headers=None):
    result = None
    timeouts = DEFAULT_CONN_TIMEOUT, DEFAULT_READ_TIMEOUT

    try:
        response = requests.get(url,
                                params=params,
                                headers=headers,
                                timeout=timeouts)
    except Timeout as e:  # не стал углубляться в разные таймауты
        print('GET timeout =(\n'
              'Try again!')
    else:
        if response.ok:
            result = response
        else:
            print(f"Response isn't OK ({response.status_code})")

    return result


def save_to_file(response, filename=None):
    filename = filename or 'default_filename.json'
    with open(filename, 'wb') as f:
        f.write(response.content)


def f1():
    """
    Посмотреть документацию к API GitHub,
    разобраться как вывести список репозиториев для конкретного пользователя,
    сохранить JSON-вывод в файле *.json.
    """

    user_name = 'user_name'
    url = f'https://api.github.com/users/{user_name}/repos'
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    response = get_response(url, headers=headers)
    if response:
        save_to_file(response, 'github_response.json')
        for repo in response.json():
            print(repo['name'])


def f2():
    """
    Изучить список открытых API
    (https://www.programmableweb.com/category/all/apis).
    Найти среди них любое, требующее авторизацию (любого типа).
    Выполнить запросы к нему, пройдя авторизацию.
    Ответ сервера записать в файл.
    """

    youtube_api_key = 'api_key_from_google'

    # общая инфа про канал
    api_type = 'channels'
    params = {
        'id': 'UC_x5XG1OV2P6uZZ5FSM9Ttw',  # Google Developers
        'part': 'snippet,contentDetails,statistics',
        'key': youtube_api_key,
    }
    headers = {
        'Accept': 'application/json'
    }
    url = f'https://youtube.googleapis.com/youtube/v3/{api_type}'
    response = get_response(url, params=params, headers=headers)
    if response:
        save_to_file(response, 'youtube_response.json')


if __name__ == '__main__':
    f1()
    f2()
