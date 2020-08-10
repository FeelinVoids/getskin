# getskin

Модуль Python, позволяющий работать с информацией о скине игрока Minecraft.  

Позволяет по нику/UUID получить UUID/ник, ссылку, скачать скин,
получить его base64 и выдать голову со скином.

Модуль можно как подключить в Python, так и работать через консольные команды.

## Установка

    

## Использование

Пример использования модуля с демонстрацией всех методов можно найти в [test.py](./test/test.py).

Результат его выполнения: [test.txt](./test/test.txt) и [скачанный в результате выполнения скин](./test/Notch.png).

## Консольные команды

Модуль можно вызвать с аргументами `--info`, `--download`, `--head` и `--hash`.
После первого аргумента должен быть ник или UUID, а далее - в зависимости от
команды.

### --info (--i)
Выводит имя, UUID и ссылку на скин.

    python -m getskin --info <ник или UUID>
    python -m getskin --info Notch
    python -m getskin --i Notch

Результат:

    Username: Notch
    UUID: 069a79f444e94726a5befca90e38aaf5
    Skin URL: http://textures.minecraft.net/texture/292009a4925b58f02c77dadc3ecef07ea4c7472f64e0fdc32ce5522489362680

### --download (--d)
Скачивает скин по пути `--path` (`--p`)
Если оставить параметр пути пустым, скин будет скачан в текущую
рабочую директорию.

В консоль будет напечатан итоговый путь.

    python -m getskin --download <ник или UUID> --path <путь>
    python -m getskin --download Notch --path /home/
    python -m getskin --d Notch --path /home/

### --head (--d)
Генерирует команду получения головы со скином.  

Параметр `--version` (`--v`) - версия майнкрафта. Может быть от `1.8` до `1.16`.
Метод получения голов с `1.8` до `1.13` одинаков.  
По умолчанию - `1.16`.

Параметр `--selector` (`--s`) - Кому выдавать голову.  
По умолчанию - `@p`.

    python -m getskin --head <ник или UUID> --selector <версия>
    python -m getskin --head Notch --selector @p --version 1.16
    python -m getskin --h Notch --s @p --v 1.16

Результат:

    /give @p minecraft:player_head{display:{Name:"{\"text\":\"Notch\"}"}, SkullOwner:{Id:[I;110787060,1156138790,-1514210135,238594805],Properties:{textures:[{Value:"eyJ0ZXh0dXJlcyI6IHsiU0tJTiI6IHsidXJsIjogImh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvMjkyMDA5YTQ5MjViNThmMDJjNzdkYWRjM2VjZWYwN2VhNGM3NDcyZjY0ZTBmZGMzMmNlNTUyMjQ4OTM2MjY4MCJ9fX0="}]}}} 1


### --hash
Выводит хеш base64 данных скина.  
(Такой используется в получении голов и установке блоков)

    python -m getskin --hash <ник или UUID>
    python -m getskin --hash Notch

Результат:

    eyJ0ZXh0dXJlcyI6IHsiU0tJTiI6IHsidXJsIjogImh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvMjkyMDA5YTQ5MjViNThmMDJjNzdkYWRjM2VjZWYwN2VhNGM3NDcyZjY0ZTBmZGMzMmNlNTUyMjQ4OTM2MjY4MCJ9fX0=