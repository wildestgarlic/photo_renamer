#!/usr/bin/env python3
import os
import sys
from datetime import datetime

from PIL import Image


class Renamer:
    image_extensions = ["png", "tiff", "jpg", "jpeg", "svg", "webp", "ico"]

    def __init__(self):
        self.work_dir = os.path.abspath(os.curdir)
        self.folder_to = os.path.join(self.work_dir, "to")

    def rename(self):
        """ Переименование на дату создания
            Фомата гггг-мм-дд_чч-мм
        """
        for name in os.listdir(self.work_dir):

            _, extension = os.path.splitext(name)
            extension = extension.replace(".", "")
            if extension.lower() not in self.image_extensions:
                continue

            new_name = self._rename_file(name, extension)
            print(f"{name:45} - {new_name:>45}")

    def _rename_file(self, name: str, extension: str) -> str:
        suffix = ""
        creation_date = self.get_date_of_creation(name)

        new_name = self._build_name(creation_date, suffix, extension)
        out = os.path.join(self.work_dir, name)
        to = os.path.join(self.folder_to, new_name)

        additional_number = 1
        while os.path.exists(to):
            suffix = str(additional_number)
            new_name = self._build_name(creation_date, suffix, extension)
            to = os.path.join(self.folder_to, new_name)
            additional_number += 1

        os.rename(out, to)

        return new_name

    @staticmethod
    def _build_name(creation_date: str, suffix: str, extension: str) -> str:
        if suffix:
            return f'{creation_date}_{suffix}.{extension}'
        return f'{creation_date}.{extension}'

    def get_date_of_creation(self, name) -> str:
        """ Ищет дату создания фотографии и
            возвращает её в формате гггг-мм-дд_чч-мм
        """
        file = os.path.join(self.work_dir, name)

        creation_time = self._creation_time_from_pil(file)
        if not creation_time:  # отсутсвие пунката метадаты
            creation_time = self._creation_time_from_os_path(file)

        creation_time_string = str(creation_time).replace(" ", "_").replace(":", "_")

        return creation_time_string

    @staticmethod
    def _creation_time_from_pil(file):
        image = Image.open(file)
        exif = image.getexif()
        creation_time = exif.get(36867)
        return creation_time

    @staticmethod
    def _creation_time_from_os_path(file):
        timestamp = os.path.getmtime(file)
        creation_time = datetime.fromtimestamp(timestamp)
        return creation_time

    def create_folder(self):
        """ todo: path from console args
        """
        try:
            if not os.path.exists(self.folder_to):
                os.makedirs(self.folder_to)
        except OSError:
            print("Ошибка при создании папок")
            raise


def main():
    renamer = Renamer()

    try:
        renamer.create_folder()
        renamer.rename()

    except FileNotFoundError:
        raise Exception("Файл не найден")
    except KeyboardInterrupt:
        sys.exit()
    finally:
        print(f"Успешно завершено")


if __name__ == "__main__":
    # while True:
    main()
