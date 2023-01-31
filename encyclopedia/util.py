import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    returns False.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
#        default_storage.delete(filename) - default string, changed for one below as per spec:
        return False
    default_storage.save(filename, ContentFile(content))
    return True # this line is added

def edit_entry(title, content):
    """
    Edits an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def conver(title):
#    with open(title, 'r', encoding='utf-8') as inp:
#        sp = inp.readlines()
    full = get_entry(title)
    sp = full.splitlines(True)
    full = ''
    for i, line in enumerate(sp):
        if line.count('*') >= 4:
            line = line.replace(' **', ' <b>')
            line = line.replace('** ', '</b> ')
            line = line.replace('**.', '</b>.')
            line = line.replace('**', '<b>')
        cnt = line.count('](')
        if cnt >= 1:
            for j in range(cnt):
                lix = line.index('(')
                rix = line.index(')')
                lnk = '<a href="' + line[lix + 1:rix] + '">'
                line = line.replace('[', lnk, 1)
                lix = line.index('(')
                rix = line.index(')')
                lnk2 = ']' + line[lix: rix + 1]
                line = line.replace(lnk2, '</a>', 1)        
        if line[0] in '-*+':
            line = '<li>' + line[1:-1] + '</li>'
            if sp[i - 1][0] not in '-*+':
                line = '<ul>' + line
            if sp[i + 1][0] not in '-*+':
                line = line + '</ul>'
        if line[0] == '#':
            if line[1] == '#':
                if line[2] == '#':
                    if line[3] == '#':
                        if line[4] == '#':
                            if line[5] == '#':
                                line = '<h6>' + line[6:] + '</h6>'
                            line = '<h5>' + line[5:] + '</h5>'
                        line = '<h4>' + line[4:] + '</h4>'
                    line = '<h3>' + line[3:] + '</h3>'
                line = '<h2>' + line[2:] + '</h2>'
            line = '<h1>' + line[1:] + '</h1>'
        full += line + '\n'
#    with open('HTM.html', 'w', encoding='utf-8') as otp:
#        print(full, file=otp)
    return full