from typing import IO
from waba.settings import Folder, File, Group  # Validator
from waba.tools import Validator
from waba.activity import OnStart

moduleFolder = Folder()  # folder name will be specified by plugin name at attaching

options = File(moduleFolder, {
    "amogus": "sus",
}, ext="json")


@Validator  # checks arguments and provides only once that asked
def validator(filename: str, obj: IO) -> bool:
    if filename.endswith(".json"):
        return obj.readline().startswith("sus")


devices = Group(Folder(moduleFolder, "devices"), validator=validator)


@OnStart
async def setup():
    ...
