import os
import sys

import getskin

dirpath = os.path.dirname(os.path.abspath(__file__))


def test_object(skin, filename):
    testpath = os.path.join(dirpath, "test_results")
    if not os.path.exists(testpath):
        os.makedirs(testpath)
    path = os.path.join(testpath, filename+".txt")
    file = open(path, "w", encoding="utf-8")
    default_stdout = sys.stdout
    sys.stdout = file

    b64 = skin.get_base64()

    print("is_full_format:", skin.is_full_format())
    print()
    print("json:", skin.json())
    print()
    print("get_uuid:", skin.get_uuid())
    print()
    print("get_username:", skin.get_username())
    print()
    print("get_url:", skin.get_url())
    print()
    print("get_base64:", b64)
    print()
    print("get_numerical_uuid:", skin.get_numerical_uuid())
    print()
    print("get_hyphenated_uuid:", skin.get_hyphenated_uuid())
    print()
    print("give_head (1.16):", skin.give_head(
          to="@p", minecraft_version="1.16"))
    print()
    print("give_head (1.15):", skin.give_head(
          to="@p", minecraft_version="1.15"))
    print()
    print("give_head (1.12):", skin.give_head(
          to="@p", minecraft_version="1.12"))
    print()
    print("get_bytes length:", len(skin.get_bytes()))
    print()
    print("download:", skin.download(os.path.join(testpath, filename+".png")))

    print("Skin.base64_to_url:", getskin.Skin.base64_to_url(b64))

    file.close()
    sys.stdout = default_stdout


test_object(getskin.Skin("Notch"), "__init__")

test_object(getskin.Skin.get_by_uuid("3bea3a289e9b409c84d8a5bcc52299bb"),
            "get_by_uuid")

test_object(getskin.Skin.get_by_username("FeelinVoids_"), "get_by_username")
