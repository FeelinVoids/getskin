import os
import sys
import argparse

from getskin.main import Skin

parser = argparse.ArgumentParser(
    description="""Allows you to work with  the player's skin information.
First argument is always skin username or UUID.

Examples:
    python -m getskin --info Notch
    python -m getskin --head Notch --s @p --v 1.15
    python -m getskin --download Notch --p /home/
    python -m getskin --hash Notch""",
    formatter_class=argparse.RawDescriptionHelpFormatter)

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("--info", "--i")
group.add_argument("--head", "--h")
group.add_argument("--download", "--d")
group.add_argument("--hash")

parser.add_argument("--selector", "--s", required=False, default="@p")
parser.add_argument("--version", "--v", required=False, default="1.16")
parser.add_argument("--path", "--p", required=False, default=os.getcwd())

args = parser.parse_args()

if args.info is not None:
    skin = Skin(args.info)
    print("Username:", skin.get_name())
    print("UUID:", skin.get_uuid())
    print("Skin URL:", skin.get_url())
elif args.head is not None:
    print(Skin(args.head).give_head(args.selector, args.version))
elif args.download is not None:
    print(Skin(args.download).download(args.path))
elif args.hash is not None:
    print(Skin(args.hash).get_hash())
