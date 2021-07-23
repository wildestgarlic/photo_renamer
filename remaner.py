#!/usr/bin/env python3
import getpass
import os
import random
import sys
from datetime import datetime

from PIL import Image


class Renamer:
    def __init__(self):
        self.work_dir = os.path.realpath(__file__)
        self.folder_from = os.path.join(self.work_dir, "from")
        self.folder_to = os.path.join(self.work_dir, "to")
        self.user = getpass.getuser()
        self.image_extensions = ["png", "tiff", "jpg", "jpeg", "svg", "webp", "ico"]

    def rename(self):
        """
        Переименовывает фотографии на дату создания
        """
        for name in os.listdir(self.folder_from):

            _, extension = os.path.splitext(name)
            if extension.lower() not in self.image_extensions:
                continue

            new_name = self._rename_file(name, extension)
            print(f"{name:45} - {new_name:>45}")

    def _rename_file(self, name: str, extension: str) -> str:
        creation_date = self.get_date_of_creation(name)
        r = random.randint(1, 9999)
        new_name = creation_date + f"-{r:0>4}." + extension

        out = os.path.join(self.folder_from + name)
        to = os.path.join(self.folder_from + new_name)
        os.rename(out, to)

        return new_name

    @staticmethod
    def get_date_of_creation(file):
        """
        Ищет верную дату создания фотографии и
        возвращает её в формате гггг-мм-дд_чч-мм
        """
        create_time = Image.open(file)._getexif()[36867]  # noqa
        if not create_time:  # отсутсвие пунката метадаты
            timestamp = os.path.getmtime(file)
            create_time = datetime.fromtimestamp(timestamp)

        create_time_string = str(create_time).replace(" ", "_").replace(":", "_")[:19]

        return create_time_string

    def create_dirs_if_not_exists(self):
        try:
            if not os.path.exists(self.folder_from):
                os.makedirs(self.folder_from)
            if not os.path.exists(self.folder_to):
                os.makedirs(self.folder_to)
        except OSError:
            print("Ошибка при создании папок")
            raise


def main():
    renamer = Renamer()

    try:
        renamer.create_dirs_if_not_exists()
        renamer.rename()

    except FileNotFoundError:
        raise Exception("Файл не найден")
    except KeyboardInterrupt:
        sys.exit()
    finally:
        print(f"Успешно завершено")


if __name__ == "__main__":
    while True:
        main()
