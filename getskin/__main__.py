import os
import sys
import argparse

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
group.add_argument("--head", "--h", help="Get /give command of head with skin")
group.add_argument("--download", "--d", help="Download the skin")
group.add_argument("--base64", "--b", help="Get base64 hash of skin")

parser.add_argument("--selector", "--s", required=False, default="@p")
parser.add_argument("--version", "--v", required=False, default="1.16")
parser.add_argument("--path", "--p", required=False, default=os.getcwd())


def main():
    def _print_info(name):
        skin = Skin(name)
        print(
            "Username: "+skin.get_name(),
            "UUID: "+skin.get_uuid(),
            "Skin URL: "+skin.get_url(),
            "base64: "+skin.get_hash(),
            "Head 1.16: "+skin.give_head(minecraft_version="1.16"),
            "Head 1.15: "+skin.give_head(minecraft_version="1.15"),
            "Head 1.12: "+skin.give_head(minecraft_version="1.12"),
            sep="\n\n"
        )

    if len(sys.argv) == 2 and not sys.argv[1].startswith("-"):
        _print_info(sys.argv[1])
        return

    args = parser.parse_args()

    if args.info is not None:
        _print_info(args.info)
    elif args.head is not None:
        print(Skin(args.head).give_head(args.selector, args.version))
    elif args.download is not None:
        print(Skin(args.download).download(args.path))
    elif args.base64 is not None:
        print(Skin(args.base64).get_hash())


if __name__ == "__main__":
    main()
