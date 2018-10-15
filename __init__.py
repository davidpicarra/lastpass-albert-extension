'''LastPass Vault search'''
import subprocess
import re
import os
from shutil import which
from albertv0 import *

__iid__ = 'PythonInterface/v0.1'
__prettyname__ = 'LastPass'
__version__ = '1.0'
__trigger__ = 'lp '
__author__ = 'David Piçarra'
__dependencies__ = ['lpass']

if not which('lpass'):
    raise Exception("`lpass` is not in $PATH.")

# ICON_PATH = iconLookup('dialog-password')
ICON_PATH = os.path.dirname(__file__)+"/lastpass.svg"

def handleQuery(query):
    """
    Handle query
     :param str query: Query
     :return list
    """
    if not query.isTriggered:
        return None

    stripped = query.string.strip()
    if stripped:
        try:
            lpass = subprocess.Popen(['lpass', 'ls', '--long'], stdout=subprocess.PIPE)
            try:
                output = subprocess.check_output(['grep', stripped], stdin=lpass.stdout)
            except subprocess.CalledProcessError as e:
                return Item(
                    id=__prettyname__,
                    icon=ICON_PATH,
                    text=__prettyname__,
                    subtext=f'No results found for {stripped}',
                    completion=query.rawString
                )
            items = []
            for line in output.splitlines():
                match = re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2} (.*) \[id: (\d*)\] \[username: (.*)\]', line.decode("utf-8"))
                items.append(Item(
                    id=__prettyname__,
                    icon=ICON_PATH,
                    text=match.group(1),
                    subtext=match.group(3),
                    completion=query.rawString,
                    actions=[
                        ProcAction("Copy password to clipboard", ["lpass", "show", "-cp", match.group(2)]),
                        ProcAction("Copy username to clipboard", ["lpass", "show", "-cu", match.group(2)]),
                        ProcAction("Copy notes to clipboard", ["lpass", "show", "-c", "--notes", match.group(2)])
                    ]
                ))

            return items

        except subprocess.CalledProcessError as e:
            return Item(
                id=__prettyname__,
                icon=ICON_PATH,
                text=f'Error: {str(e.output)}',
                subtext=str(e),
                completion=query.rawString,
                actions=[ClipAction('Copy password to clipboard', str(e))]
            )
        except Exception as e:
            return Item(
                id=__prettyname__,
                icon=ICON_PATH,
                text=f'Generic Exception: {str(e)}',
                subtext=str(e),
                completion=query.rawString,
                actions=[ClipAction('Copy password to clipboard', str(e))]
            )
    
    else:
        return Item(
            id=__prettyname__,
            icon=ICON_PATH,
            text=__prettyname__,
            subtext='Search the LastPass vault',
            completion=query.rawString,
        )
