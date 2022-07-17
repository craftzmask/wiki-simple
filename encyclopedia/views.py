from django.contrib import messages
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

import random

import markdown2 as md

from . import util

class CreateNewPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        "placeholder": "Title"
    }))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={
        "placeholder": "Content",
        'rows': 80, 'cols':20
    }))
    
class EditPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        "placeholder": "Title",
        'readonly': True
    }))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={
        "placeholder": "Content",
        'rows': 80, 'cols':20
    }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def view_entry(request, title):
    content = util.get_entry(title)
    if content:
        return render(request, "encyclopedia/view_entry.html", {
            "title": title,
            "content": md.markdown(content)
        })
    else:
        return render(request, "encyclopedia/404.html")
    
def create_entry(request):
    if request.method == 'POST':
        form = CreateNewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if util.check_exist(title):
                messages.error(request, f"{title} is existed")   
            else:
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse(
                    "encyclopedia:view_entry",
                    kwargs={"title": title}
                ))
            
        return render(request, "encyclopedia/create_entry.html", {
            "form": form
        })
            
    return render(request, "encyclopedia/create_entry.html", {
        "form": CreateNewPageForm()
    })

def edit_entry(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse(
                "encyclopedia:view_entry",
                kwargs={"title": title}
            ))
    
    return render(request, "encyclopedia/edit_entry.html", {
        "title": title,
        "form": EditPageForm(initial={
            "title": title, "content": util.get_entry(title)
        })
    })

def search(request):
    q = request.GET["q"]
    
    matches = []
    for entry in util.list_entries():
        if q.casefold() in entry.casefold():
            matches.append(entry.casefold())
            
    if len(matches) == 1 and q == matches[0]:
        return HttpResponseRedirect(reverse(
            "encyclopedia:view_entry",
            kwargs={'title': q}
        ))
        
    return render(request, "encyclopedia/search_results.html", {
        "entries": matches
    })
    
def random_page(request):
    return HttpResponseRedirect(reverse(
        "encyclopedia:view_entry",
        kwargs={"title": random.choice(util.list_entries())}
    ))