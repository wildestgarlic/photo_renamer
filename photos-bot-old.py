import getpass
import os
from platform import platform
import time
from datetime import datetime

from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

"""Запускать, когда нужно работать с уже подготовленными файлами,
    вместо того, чтобы постоянно следить за изменениями."""


class Handler(FileSystemEventHandler):
    """Следит за изменением файлов в папке и следует инструкциям"""

    def on_modified(self, event):
        counter = 1  # счётчик для одноминутных кадров
        for image_name in os.listdir(folder_track):
            full_date = self.created_date(image_name)
            # проверка на присутсвие расширения
            if "." not in image_name:
                continue  # поработать над подпаками здесь
            else:
                extension = image_name.split(".")[-1]
                new_name = full_date + f"-{counter:0>4}." + extension  # преффикс до 4с в счётчике
            print(f'{image_name:30} - {new_name:>45}')  # посмотреть за преименованиями
            os.rename(folder_track + image_name, folder_dest + new_name)
            counter += 1
            if counter == 10000:
                counter = 1
        time.sleep(0.07)  # слишком быстрая скорость сбивает счётчик

    def created_date(self, filename):
        """Ищет верную дату создания фотографии и
        возвращает её в формате гггг-мм-дд_чч-мм или через ':' вместо '-' """
        os.chdir(folder_track)
        try:
            create_time = Image.open(filename)._getexif()[36867]
        except:
            create_time = os.path.getmtime(filename)
            create_time = datetime.fromtimestamp(create_time)

        create_time = str(create_time).replace(' ', '_')
        create_time = create_time[:19]
        return create_time

    def other_files(self, filename):
        #  if "." not in filename
        pass  # сортировать не фото и не папки в отдельную папку "others"

user = getpass.getuser()

if platform().startswith("Linux"):
    folder_track = rf'/home/{user}/Pictures/Date_to_name/'
    folder_dest = rf'/home/{user}/Pictures/Renamed_photo/'

elif platform().startswith("Windows"):
    folder_track = rf'C:\Users\{user}\Изображения\Дата_в_имя\\' or rf'C:\Users\{user}\Pictures\Date_to_name\\'
    folder_dest = rf'C:\Users\{user}\Изображения\Отсортированные_фото\\' or rf'C:\Users\{user}\Изображения\Sorted_photo\\'
else:
    print('bb')
    raise SystemError

def main():
    # Запуск всего на отслеживание
    handle = Handler()
    observer = Observer()
    observer.schedule(handle, folder_track, recursive=True) #recursive=True для работы в подпапках
    observer.start()

    try:
        print("Работаю..")
        while True:
            time.sleep(300)
    except KeyboardInterrupt:
        print("Остановливаю по заросу с клавиатуры.")
        observer.stop()
        observer.join()
    except FileNotFoundError:
        print("Файл не найден")
    finally:
        print("Остановлен.")


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
