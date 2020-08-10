import base64
import json
import os
from struct import unpack
from typing import Tuple

import requests

GET_ID_URL = "https://api.mojang.com/users/profiles/minecraft/"
GET_BY_ID_URL = "https://sessionserver.mojang.com/session/minecraft/profile/"

template_116 = "/give {to} minecraft:player_head{{display:{{Name:\"{{\\\"text\\\":\\\"{name}\\\"}}\"}}, SkullOwner:{{Id:[I;{uuid0},{uuid1},{uuid2},{uuid3}],Properties:{{textures:[{{Value:\"{hash}\"}}]}}}}}} 1"
template113_115 = "/give {to} minecraft:player_head{{display:{{Name:\"{{\\\"text\\\":\\\"{name}\\\"}}\"}}, SkullOwner: {{Id: \"{uuid}\", Properties: {{textures: [{{Value: \"{hash}\"}}]}}}}}} 1"
legacy_template = "/give {to} skull 1 3 {{display:{{Name:\"{name}\"}}, SkullOwner: {{Id: \"{uuid}\", Properties: {{textures: [{{Value: \"{hash}\"}}]}}}}}}"


class Skin:
    """ Позволяет получить текстуру и ID по имени, 
        или имя и текстуру по ID.

        Если передан несуществующий ID или имя, бросит `ValueError`
        с JSON, который прилетел в ответ с сервера.

        Пример использования:

        ```
        skin = Skin("Notch")
        print(skin.get_uuid()) # UUID
        print(skin.get_name()) # Имя пользователя
        print(skin.get_url()) # Ссылка на скин
        print(skin.get_bytes()) # байты
        print(skin.get_hash()) # base64
        # Скачать скин в текущую директорию
        print(skin.download(os.getcwd())) 

        # Получить команды give для выдачи головы для
        # разных версий Minecraft:
        print(skin.give_head(to="@p", minecraft_version="1.16")) 
        print(skin.give_head(to="@p", minecraft_version="1.15")) 
        print(skin.give_head(to="@p", minecraft_version="1.12")) 
        # Команды аналогичны для версий 1.15, 1.14 и 1.13
        ```
        """

    def __init__(self, username_or_uuid: str):
        self.__id: str = None
        self.__name: str = None
        self.__bytes: bytes = None
        self.__response: dict = None

        # Это может быть UUID с дефисами. Удаляем их.
        username_or_uuid = username_or_uuid.replace("-", "")

        # 16 - максимальная длина ника, так что если передано больше,
        # считаем, что это ID
        if len(username_or_uuid) > 16:
            self.__id: str = username_or_uuid
        else:
            self.__name: str = username_or_uuid

        # При выдаче головы необходимо определить, был ли получен
        # скин по UUID, и если был, то назвать её UUID'ом, а не ником
        self.__get_by: str = username_or_uuid

    def __repr__(self):
        if self.__name is None:
            n = self.__id
        else:
            n = self.__name
        return "<Skin of "+n+">"

    def get_uuid(self) -> str:
        """ Возвращает ID скина

            Если объект был получен по имени пользователя, будет
            произведено обращение к серверу."""
        if self.__id is None:
            self.__load_id()
        return self.__id

    def __load_id(self):
        """ Чтобы получить скин, необходимо знать его ID.
            Если в объект было передано имя пользователя, а не ID,
            перед получением текстуры необходимо обратиться к серверу
            и узнать ID."""
        resp = requests.get(GET_ID_URL+self.__name).json()
        try:
            self.__id = resp["id"]
        except KeyError:
            raise ValueError(resp)

    def __load_full(self):
        """ Загрузка имени и текстуры, когда ID уже известен """
        resp = requests.get(GET_BY_ID_URL+self.get_uuid()).json()
        self.__name = resp["name"]

        datastr = base64.b64decode(resp["properties"][0]["value"]).decode()
        self.__response = json.loads(datastr)

    def get_name(self) -> str:
        """ Возвращает имя пользователя скина """
        if self.__name is None:
            self.__load_full()
        return self.__name

    def get_url(self) -> str:
        """ Возвращает ссылку на png картинку скина """
        if self.__response is None:
            self.__load_full()
        return self.__response["textures"]["SKIN"]["url"]

    def get_bytes(self) -> bytes:
        """ Возвращает байты png картинки скина """
        if self.__bytes is None:
            self.__bytes = requests.get(self.get_url()).content
        return self.__bytes

    def download(self, path: str) -> str:
        """ Скачивает png-картинку скина

            `path` - Папка для сохранения. Если пути не существует,
            необходимые папки будут созданы. По умолчанию файл сохраняется
            как имя_скина.png, но если путь заканчивается на `.png`, 
            то файл будет назван как последняя часть пути.

            Получившийся в итоге путь возвращается."""

        if not path.endswith(".png"):
            path = os.path.join(path, self.get_name()+".png")

        with open(path, "wb") as f:
            f.write(self.get_bytes())

        return path

    def get_hash(self) -> str:
        """ Возвращает хеш base64 данных скина

            (используется в командах `/give` и `/setblock`)"""
        return base64.b64encode(
            json.dumps(
                {"textures": {"SKIN": {"url": self.get_url()}}}).encode()
        ).decode()

    def get_numerical_uuid(self) -> Tuple[int]:
        """ Возвращает UUID скина в формате Minecraft 1.16 - в виде
            последовательности из 4 чисел"""
        uuid = self.get_uuid()
        return (unpack('>i', bytes.fromhex(uuid[x*8:(x+1)*8]))[0]
                for x in range(4))

    def get_hyphenated_uuid(self) -> str:
        """ Возвращает UUID скина в формате Minecraft ДО 1.16 -
            в виде строки шестнадцатеричных чисел, разделённых
            дефисом"""
        uuid = self.get_uuid()
        return uuid[:8] + "-" + uuid[8:12] + "-" + \
            uuid[12:16] + "-" + uuid[16:20] + "-" + uuid[20:]

    def give_head(self, to: str = "@p",
                  minecraft_version: str = "1.16") -> str:
        """ Генерирует """
        if minecraft_version.startswith("1.16"):
            return template_116.format(
                to=to,
                hash=self.get_hash(),
                name=self.__get_by,
                **{"uuid"+str(n): v
                   for n, v in enumerate(self.get_numerical_uuid())}
            )
        elif minecraft_version.startswith("1.15") \
                or minecraft_version.startswith("1.14") \
                or minecraft_version.startswith("1.13"):
            return template113_115.format(
                name=self.__get_by,
                to=to,
                uuid=self.get_hyphenated_uuid(),
                hash=self.get_hash())
        else:
            return legacy_template.format(
                name=self.__get_by,
                to=to,
                uuid=self.get_hyphenated_uuid(),
                hash=self.get_hash()
            )
