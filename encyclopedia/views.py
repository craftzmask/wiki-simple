from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_entry(request, title):
    content = util.get_entry(title)
    if content:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
    else:
        return render(request, "encyclopedia/404.html")
    
def search(request):
    q = request.GET["q"]
    
    matches = []
    for entry in util.list_entries():
        if q.casefold() in entry.casefold():
            matches.append(entry.casefold())
            
    if len(matches) == 1 and q == matches[0]:
        return HttpResponseRedirect(reverse(
            "encyclopedia:get_entry",
            kwargs={'title': q}
        ))
        
    return render(request, "encyclopedia/search_results.html", {
        "entries": matches
    })
    