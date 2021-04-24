import argparse
import os
import sys
import json

from getskin.__version__ import __version__
from getskin.main import Skin

parser = argparse.ArgumentParser(
    description="""Allows you to work with the player's skin information.
First argument is always skin username or UUID.

Examples:
    # Simple:
    getskin Notch

    # Advanced:
    getskin --info Notch
    getskin --head Notch --s @p --v 1.15
    getskin --download Notch --p /home/
    getskin --base64 Notch""",
    formatter_class=argparse.RawDescriptionHelpFormatter)

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("--info", "--i", help="Get username, UUID and skin URL")
group.add_argument("--json", "--j", help="Get skin info as JSON")
group.add_argument("--head", "--h", help="Get /give command of head with skin")
group.add_argument("--download", "--d", help="Download the skin")
group.add_argument("--base64", "--b", help="Get base64 hash of skin")
group.add_argument("--version", "--v", help="Get version of getskin",
                   action="store_true")

parser.add_argument("--selector", "--s", required=False, default="@p")
parser.add_argument("--mc", required=False, default="1.16")
parser.add_argument("--path", "--p", required=False, default=os.getcwd())


def main():
    def _print_info(name):
        skin = Skin.get(name)
        print(
            "Username: "+skin.get_username(),
            "UUID: "+skin.get_uuid(),
            "Skin URL: "+skin.get_url(),
            "base64: "+skin.get_base64(),
            "Head 1.16: "+skin.give_head(minecraft_version="1.16"),
            "Head 1.15: "+skin.give_head(minecraft_version="1.15"),
            "Head 1.12: "+skin.give_head(minecraft_version="1.12"),
            sep="\n\n"
        )

    if len(sys.argv) == 2 and not sys.argv[1].startswith("-"):
        if len(sys.argv[1]) < 32:
            _print_info(sys.argv[1])
        else:
            print(Skin.base64_to_url(sys.argv[1]))
        return

    args = parser.parse_args()

    if args.info is not None:
        _print_info(args.info)
    elif args.head is not None:
        print(Skin.get(args.head).give_head(args.selector, args.mc))
    elif args.json is not None:
        print(json.dumps(Skin.get(args.json).json(), indent=4,
                         ensure_ascii=False,
                         sort_keys=True))
    elif args.download is not None:
        print(Skin.get(args.download).download(args.path))
    elif args.base64 is not None:
        print(Skin.get(args.base64).get_base64())
    elif args.version is not None:
        print(__version__)


if __name__ == "__main__":
    main()
