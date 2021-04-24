import json
import os
import struct
from base64 import b64decode, b64encode
from struct import unpack
from typing import IO, Optional, Tuple, Union

import requests

GET_UUID_URL = "https://api.mojang.com/users/profiles/minecraft/"
GET_BY_UUID_URL = "https://sessionserver.mojang.com/session/minecraft/profile/"

template_116 = "/give {to} minecraft:player_head{{display:{{Name:\"{{\\\"text\\\":\\\"{name}\\\"}}\"}}, SkullOwner:{{Id:[I;{uuid0},{uuid1},{uuid2},{uuid3}],Properties:{{textures:[{{Value:\"{hash}\"}}]}}}}}} 1"
template113_115 = "/give {to} minecraft:player_head{{display:{{Name:\"{{\\\"text\\\":\\\"{name}\\\"}}\"}}, SkullOwner: {{Id: \"{uuid}\", Properties: {{textures: [{{Value: \"{hash}\"}}]}}}}}} 1"
legacy_template = "/give {to} skull 1 3 {{display:{{Name:\"{name}\"}}, SkullOwner: {{Id: \"{uuid}\", Properties: {{textures: [{{Value: \"{hash}\"}}]}}}}}}"


class Skin:
    """ 
        Объект скина, получаемый по имени пользователя или uuid.
        Реализует функционал, позволяющий получать имя, uuid,
        base64, осуществлять проверку формата скина, и скачивать его.
    """

    def __init__(self, username: Optional[str] = None,
                 uuid: Optional[str] = None, base64: Optional[str] = None):
        self._uuid: str = uuid.replace("-", "") if uuid is not None else None
        self._username: str = username
        self._full = None

        if username == uuid == base64:
            raise ValueError("username == uuid == base64 ==", self._uuid)

        self._url: str = None
        if base64 is not None:
            data = json.loads(b64decode(base64).decode())
            self._url = data["textures"]["SKIN"]["url"]
            try:
                self._uuid = data["profileId"]
                self._username = data["profileName"]
            except:
                pass

        self.__bytes: bytes = None

    @classmethod
    def get(cls, data: str):
        if len(data) <= 16:
            return Skin.get_by_username(data)
        elif len(data) <= 32:
            return Skin.get_by_uuid(data)
        return Skin.get_by_base64(data)

    @classmethod
    def get_by_uuid(cls, uuid: str) -> "Skin":
        """ Получает объект по UUID """
        return cls(username=None, uuid=uuid, base64=None)

    @classmethod
    def get_by_username(cls, username: str) -> "Skin":
        """ Получает объект по имени пользователя """
        return cls(username=username, uuid=None, base64=None)

    @classmethod
    def get_by_base64(cls, base64: str) -> "Skin":
        """ Пытается получить скин по base64. Но обычно
            единственный случай, когда это может сработать -
            если хэш получен от API Mojang. """
        return cls(username=None, uuid=None, base64=base64)

    @staticmethod
    def resolve_username(username: str) -> str:
        """ Получает UUID игрока по нику путём обращения к API """
        return requests.get(GET_UUID_URL+username).json()["id"]

    @staticmethod
    def resolve_uuid(uuid: str) -> Tuple[str, str, str]:
        """ Принимает UUID, возвращает `("имя_пользователя",
            "base64", "url")` """
        uuid = uuid.replace("-", "")
        resp = requests.get(GET_BY_UUID_URL+uuid).json()
        b64 = resp["properties"][0]["value"]
        data = json.loads(b64decode(b64).decode())
        return (resp["name"], b64, data["textures"]["SKIN"]["url"])

    @staticmethod
    def _is_full_format(bytesfilelike: Union[bytes, IO]) -> bool:
        """ Позволяет определить формат скина.

            Скины бывают 2 форматов: неполные - меньше картинка меньше и
            не поддерживается второй слой, и полные - картинка
            квадратная """
        # https://stackoverflow.com/a/20380514
        if isinstance(bytesfilelike, bytes):
            head = bytesfilelike[:24]
        else:
            head = bytesfilelike.read(24)
        if len(head) != 24:
            return False
        check = struct.unpack('>i', head[4:8])[0]
        if check != 0x0d0a1a0a:
            return False
        width, height = struct.unpack('>ii', head[16:24])
        return height == 64

    @staticmethod
    def base64_to_url(b64: str) -> str:
        data = json.loads(b64decode(b64.encode()).decode())
        return data["textures"]["SKIN"]["url"]

    def is_full_format(self) -> bool:
        if self._full is None:
            self._full = Skin._is_full_format(self.get_bytes())
        return self._full

    def __repr__(self):
        if self._username is None:
            n = self._uuid
        else:
            n = self._username
        return "<Skin of "+n+">"

    def json(self):
        """ Возвращает все данные скина в формате словаря """
        return {
            "uuid": self.get_uuid(),
            "username": self.get_username(),
            "base64": self.get_base64(),
            "hyphenated_uuid": self.get_hyphenated_uuid(),
            "numerical_uuid": self.get_numerical_uuid(),
            "url": self.get_url(),
            "is_full_format": self.is_full_format()
        }

    @classmethod
    def from_json(self, json: dict) -> "Skin":
        """ Переводит dict, полученный методом .json() обратно
            в объект Skin """
        skin = Skin(username=json["username"], uuid=json["uuid"],
                    base64=json["base64"])
        skin._url = json["url"]
        skin._full = json["is_full_format"]
        return skin

    def get_uuid(self) -> str:
        """ Возвращает UUID скина

            Если объект был получен по имени пользователя, будет
            произведено обращение к API."""
        if self._uuid is None:
            self._uuid = self.resolve_username(self._username)
        return self._uuid

    def get_username(self) -> str:
        """ Возвращает имя пользователя скина """
        # Если имеем имя пользователя, можно вернуть его. Если не
        # имеем, значит по-любому имеем UUID. Загружаем.
        if self._username is None:
            self._username, _, self._url = self.resolve_uuid(self._uuid)
        return self._username

    def get_url(self) -> str:
        """ Возвращает ссылку на png картинку скина """
        if self._url is None:
            # В этом методе происходит обновление self._url
            uuid = self.get_uuid()
            self._username, _, self._url = self.resolve_uuid(uuid)
        return self._url

    def get_bytes(self) -> bytes:
        """ Возвращает байты png картинки скина

            Байты сохраняются в объекте для быстрого последующего
            доступа или скачивания картинки. """
        if self.__bytes is None:
            self.__bytes = requests.get(self.get_url()).content
        return self.__bytes

    def download(self, path: str = ".") -> str:
        """ Скачивает png-картинку скина

            `path` - Папка для сохранения. Если пути не существует,
            необходимые папки будут созданы. По умолчанию файл сохраняется
            как имя_скина.png, но если путь заканчивается на `.png`, 
            то файл будет назван как последняя часть пути.

            Получившийся в итоге путь возвращается."""

        # Прогрузим все данные сразу
        self.get_bytes()
        path = os.path.abspath(path)

        if not path.endswith(".png"):
            path = os.path.join(path, self.get_username()+".png")

        with open(path, "wb") as f:
            f.write(self.get_bytes())

        return path

    def get_base64(self) -> str:
        """ Возвращает хеш base64 данных скина

            (используется в командах `/give` и `/setblock`)"""
        return b64encode(
            json.dumps(
                {"textures": {"SKIN": {"url": self.get_url()}}}).encode()
        ).decode()

    def get_numerical_uuid(self) -> Tuple[int]:
        """ Возвращает UUID скина в формате Minecraft 1.16 - в виде
            последовательности из 4 чисел"""
        uuid = self.get_uuid()
        return tuple(unpack('>i', bytes.fromhex(uuid[x*8:(x+1)*8]))[0]
                     for x in range(4))

    def get_hyphenated_uuid(self) -> str:
        """ Возвращает UUID скина в формате Minecraft ДО 1.16 -
            в виде строки шестнадцатеричных чисел, разделённых
            дефисом"""
        uuid = self.get_uuid()
        return uuid[:8] + "-" + uuid[8:12] + "-" + \
            uuid[12:16] + "-" + uuid[16:20] + "-" + uuid[20:]

    def give_head(self, to: str = "@p",
                  minecraft_version: str = "1.16",
                  name: Optional[str] = None) -> str:
        """ Генерирует команду /give для получения головы со скином.

            `to` - Кому выдавать голову, по умолчанию `"@p"`

            `minecraft_version` - версия Minecraft, от неё зависит 
            команда.  
            Форматы команд разные в версиях:
                1.9 - 1.12
                1.13 - 1.15
                1.16 - ... 

            По умолчанию `"1.16"`"""
        self.get_url()  # Подгрузка данных, в т.ч. ника

        if name is None:
            name = self.get_username()
        if minecraft_version.startswith("1.16"):
            return template_116.format(
                to=to,
                hash=self.get_base64(),
                name=name,
                **{"uuid"+str(n): v
                   for n, v in enumerate(self.get_numerical_uuid())}
            )
        elif minecraft_version.startswith("1.15") \
                or minecraft_version.startswith("1.14") \
                or minecraft_version.startswith("1.13"):
            return template113_115.format(
                name=name,
                to=to,
                uuid=self.get_hyphenated_uuid(),
                hash=self.get_base64())
        else:
            return legacy_template.format(
                name=name,
                to=to,
                uuid=self.get_hyphenated_uuid(),
                hash=self.get_base64()
            )
