from django.shortcuts import render
# from django import forms
import markdown2
import random
from django.utils.safestring import mark_safe

from . import util


def index(request):
    msp = []
    for ent in util.list_entries():
        # lnkent = mark_safe('<a href="entries/' + ent + '.md">' + ent + '</a>') #first tried to do
        # real path, but djungo needed one more path in urls... Still not sure what is required
        # in task - wike/title, or just title
        # lnkent = mark_safe('<a href="' + ent + '">' + ent + '</a>') #second version - without wiki
        lnkent = mark_safe('<a href="wiki/' + ent + '">' + ent + '</a>')  # finally decided to do with wiki,
        # as all pages have links wiki/
        msp.append(lnkent)
    return render(request, "encyclopedia/index.html", {
        # "entries": util.list_entries() #this is initial line, no links at index page
        "entries": msp
    })


def article(request, name):
    if name in util.list_entries():
        # cont = mark_safe(util.conver(name)) #this is my own converter markdown to html,
        # before I've discovered markdown2
        pth = 'entries/' + name + '.md'
        cont = mark_safe(markdown2.markdown_path(pth))
        lnkent = mark_safe('<a href="../edit/' + name + '">' + 'Edit page' + '</a>')
        return render(request, "encyclopedia/article.html", {"name": [name, cont, lnkent]})
    else:
        cont = '- this page was not found '
        return render(request, "encyclopedia/noarticle.html", {"name": [name, cont]})


def search(request):
    # return article(request, request.GET.get('q')) used this, and it worked, with search working as in view.article
    name = request.GET.get('q')
    if name in util.list_entries():
        pth = 'entries/' + name + '.md'
        cont = mark_safe(markdown2.markdown_path(pth))
        lnkent = mark_safe('<a href="../edit/' + name + '">' + 'Edit page' + '</a>')
        return render(request, "encyclopedia/article.html", {"name": [name, cont, lnkent]})
    else:
        msp = []
        for ent in util.list_entries():
            if name in ent:
                lnkent = mark_safe('<a href="wiki/' + ent + '">' + ent + '</a>')
                msp.append(lnkent)
        return render(request, "encyclopedia/index.html", {"entries": msp})


def newp(request):
    return render(request, "encyclopedia/newpage.html")


def save(request):
    name = request.POST.get('entry')
    cont = request.POST.get('content')
    if not util.save_entry(name, cont):
        cont1 = '- this entry already exists'
        return render(request, "encyclopedia/noarticle.html", {"name": [name, cont1]})
    pth = 'entries/' + name + '.md'
    cont = mark_safe(markdown2.markdown_path(pth))
    lnkent = mark_safe('<a href="../edit/' + name + '">' + 'Edit page' + '</a>')
    return render(request, "encyclopedia/article.html", {"name": [name, cont, lnkent]})


def edit(request, name):
    contmrk = util.get_entry(name)
    return render(request, "encyclopedia/edit.html", {"name": [name, contmrk]})


def edsave(request):
    name = request.POST.get('entry')
    cont = request.POST.get('content')
    util.edit_entry(name, cont)
    pth = 'entries/' + name + '.md'
    cont = mark_safe(markdown2.markdown_path(pth))
    lnkent = mark_safe('<a href="../edit/' + name + '">' + 'Edit page' + '</a>')
    return render(request, "encyclopedia/article.html", {"name": [name, cont, lnkent]})


def rand(request):
    name = random.choice(util.list_entries())
    return article(request, name)
