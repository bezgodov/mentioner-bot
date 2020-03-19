from typing import List, Dict, Callable

from handlers.addmembers import AddMembers
from handlers.addteam import AddTeam
from handlers.getteams import GetTeams
from handlers.mention import Mention
from handlers.removeteam import RemoveTeam
from handlers.renameteam import RenameTeam

def make_handler(handler: Callable, name: str, hint: str) -> Dict:
    return {
        "name": name,
        "handler": handler,
        "hint": hint
    }

handlers = [
    make_handler(AddTeam, 'addteam', 'Add a team'),
    make_handler(AddMembers, 'addmembers', 'Add members to a team'),
    make_handler(GetTeams, 'getteams', 'Get all teams in a chat'),
    make_handler(Mention, 'mention', 'Mention a team'),
    make_handler(RemoveTeam, 'removeteam', 'Remove a team'),
    make_handler(RenameTeam, 'renameteam', 'Rename a team'),
]
