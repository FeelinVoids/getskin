import getskin
import os
import sys


# Результат выполнения этого скрипта запишем в файл test.txt
dirpath = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(dirpath, "test.txt")
file = open(path, "w", encoding="utf-8")

default_stdout = sys.stdout
sys.stdout = file

# Получаем объект скина, с которым будем работать.
# Вместо ника может быть UUID.
skin = getskin.Skin("Notch")

# Демонстрация всех методов:
print(
    # Возвращает UUID в 3-х разных форматах:
    # - Слитно
    # - В виде массива из 4-х чисел
    # - Разделённый дефисами
    # Подробнее здесь:
    # https://minecraft.gamepedia.com/Universally_unique_identifier
    skin.get_uuid(),
    list(skin.get_numerical_uuid()),
    skin.get_hyphenated_uuid(),

    # Возвращает имя пользователя
    skin.get_name(),

    # Возвращает ссылку на png файл
    skin.get_url(),

    # Скачивает и возвращает байты файла
    skin.get_bytes(),

    # Скачивает файл в переданную первым параметром директорию
    skin.download(dirpath),

    # Возвращает base64 данных скина
    skin.get_hash(),

    # Получение команды /give для разных версий
    skin.give_head(to="@p", minecraft_version="1.16"),
    skin.give_head(to="@p", minecraft_version="1.15"),
    skin.give_head(to="@p", minecraft_version="1.12"),

    sep="\n\n\n"
)

file.close()
sys.stdout = default_stdout

print("Test result:", path)
