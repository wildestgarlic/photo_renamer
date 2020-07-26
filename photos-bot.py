#!/usr/bin/env python3
import getpass
import os
import time
from datetime import datetime
from PIL import Image

user = getpass.getuser()

folder_track = rf'/home/{user}/Pictures/Date_to_name/'
folder_delivery = rf'/home/{user}/Pictures/Renamed_photo/'

reset = '\033[0m'
italic = '\x1B[3m'
blue = '\033[0;34m'
bold = '\033[1m'


def rename():
    """Переименовывает фотографии на дату создания"""
    counter = 1  # счётчик для одноминутных кадров
    for image_name in os.listdir(folder_track):
        extension = image_name.split(".")[-1].lower()
        # проверка на присутсвие расширения
        if "." not in image_name:
            continue  # поработать над подпаками здесь
        elif extension == 'png'\
                or extension == 'tif'\
                or extension == 'jpg'\
                or extension == 'svg':

            full_date = created_date(image_name)
            new_name = full_date + f"-{counter:0>4}." + extension  # преффикс до 4с в счётчике

            print(f'{bold}{image_name:30} - {new_name:>45}{reset}')  # посмотреть за преименованиями

            os.rename(folder_track + image_name, folder_delivery + new_name)
            counter += 1
            if counter == 10000:
                counter = 1
    time.sleep(0.1)  # слишком быстрая скорость сбивает счётчик


def created_date(filename):
    """Ищет верную дату создания фотографии и
    возвращает её в формате гггг-мм-дд_чч-мм или через ':' вместо '-' """
    os.chdir(folder_track)
    try:
        create_time = Image.open(filename)._getexif()[36867]
    except:  # отсутсвие пунката метадаты, добавить ошибку
        create_time = os.path.getmtime(filename)
        create_time = datetime.fromtimestamp(create_time)

    create_time = str(create_time).replace(' ', '_')[:19]
    return create_time


def ready():
    """Спрашивает, начинать ли действовать"""
    start = input('[y]es or [n]o?\n')
    if start.lower().startswith('y'):
        return True
    return False


def main():
    try:
        # os.mkdirs(folder_track, folder_delivery)  # для других пользователей
        print(f'{blue}Запускаюсь..{reset} ')
        time.sleep(1)  # lol

        print(f'Фотографии будут переименованы и перемещены\n'
              f'\tотсюда {italic}{folder_track}{reset}\n'
              f'\tсюда   {italic}{folder_delivery}{reset}')

        if ready():
            rename()
    except FileNotFoundError:
        print("Файл не найден")
    except KeyboardInterrupt:
        print(' Остановка через Ctrl + C')
    finally:
        print(f'{blue}Завершено.{reset}')


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
