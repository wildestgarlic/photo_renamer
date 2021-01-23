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


def rename_photos():
    """Переименовывает фотографии на дату создания"""
    counter = 1  # счётчик для одноминутных кадров
    for image_name in os.listdir(folder_track):
        image_extensions = ["png", "tiff", "jpg", "jpeg", "svg", "webp", "ico"]
        extension = image_name.split(".")[-1].lower()
        if "." not in image_name:
            continue  # поработать над подпаками здесь
        elif extension in image_extensions:
            full_date = get_created_date(image_name)
            new_name = full_date + f"-{counter:0>4}." + extension  # преффикс до 4 нулей в счётчике

            print(f'{bold}{image_name:30} - {new_name:>45}{reset}')  # лог преименований
            os.rename(folder_track + image_name, folder_delivery + new_name)
            counter += 1
            if counter == 10000:
                counter = 1
    time.sleep(0.1)  # слишком быстрая скорость сбивает счётчик

def get_created_date(filename):
    """Ищет верную дату создания фотографии и
    возвращает её в формате гггг-мм-дд_чч-мм или через ':' вместо '-' """
    os.chdir(folder_track)
    try:
        create_time = Image.open(filename)._getexif()[36867]
    except:  # отсутсвие пунката метадаты
        create_time = os.path.getmtime(filename)
        create_time = datetime.fromtimestamp(create_time)

    create_time_string = str(create_time).replace(' ', '_')[:19]
    return create_time_string

def ready():
    """Спрашивает, начинать ли действовать"""
    start = input('[y]es or [n]o?\n')
    while True:
        if start.lower().startswith('y'):
            return True
        elif start.lower().startswith('n'):
            return False

def create_dirs_if_not_exists():
    try:
        if not folder_track:
                os.makedirs(folder_track)
        if not folder_delivery:
            os.makedirs(folder_delivery)
    except:
        print("Ошибка в создании папок")

def main():
    create_dirs_if_not_exists()
    try:
        print(f'Фотографии будут переименованы и перемещены\n'
              f'\t отсюда {italic}{folder_track}{reset}\n'
              f'\t сюда   {italic}{folder_delivery}{reset}')

        time.sleep(2)
        if ready():
            rename_photos()

    except FileNotFoundError:
        print("Файл не найден")
    except KeyboardInterrupt:
        print("Остановка через Ctrl + C")
    finally:
        print(f'{blue}Успешно завершено{reset}')


if __name__ == '__main__':
    main()
