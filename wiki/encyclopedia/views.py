from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import util
import markdown2
import random
mega_title = None #Global variable 
entry_list = [] #Contains list of all entries
lower_entry_list = [] #To do some computations,this list contains all entries in lower case
entries= util.list_entries()
for entry in entries:
    entry_list.append(entry)
    if type(entry)==str: #It takes care of any int type entry.It is done everywhere wherever there are type specific operations
        entry=entry.lower()
    lower_entry_list.append(entry)
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry_view(request, title):
    content1 = util.get_entry(title)
    content = markdown2.markdown(content1)
    global mega_title
    mega_title=title
    if content1 is not None:
        # If content was found, render it in a template or return it
        return render(request,"encyclopedia/info.html",{"content":content,"title":title})
    else:
        # If no content was found,error message is shown
        return HttpResponse("Page not found")
def search(request):
   query = request.GET.get('q')
   if type(query)==str:
       query = query.lower()
   content1= util.get_entry(title=query)
   query_list=list(query)
   match_entry=[]
   if content1 is None:
       for entry in entry_list: #It matches string provided in search section,with entries.Its accuracy can be varied
           if type(entry)==str:
             entry=entry.lower()
           entry=list(entry)
           counter=0
           for i in query_list:
               for j in entry:
                  if counter==3:#Increase this number for better accuracy.
                      entry = ''.join(entry)
                      if type(entry)==str:
                        entry=entry.capitalize()
                      match_entry.append(entry)
                  elif i==j:
                     counter +=1
       match_entry=set(match_entry)#Removes duplicates created from above loops
       match_entry=list(match_entry)#It contains successfully matched entries 
       return render(request,"encyclopedia/search.html",{
           "match_entry":match_entry
       })
   else:
       content=markdown2.markdown(content1)
       return render(request,"encyclopedia/info.html",{
           "content":content
       })
   
def new_page(request):
    return render(request,"encyclopedia/new_page.html",{})
def new_entry(request):
    content=request.GET.get('text_area')  
    title=request.GET.get('title_new') 
    if title is None:
        old_title=mega_title
        util.save_entry(old_title,content)
        content = markdown2.markdown(content)
        return render(request,"encyclopedia/info.html",{
            "content":content
        })
    check= util.title_check(title)
    if check==True:
        return HttpResponse('Entry already exists')
    if type(title)==str:
        title=title.capitalize()
    util.save_entry(title,content)
    content = markdown2.markdown(content)
    return render(request,"encyclopedia/info.html",{
        "content":content
    })
def edit_py(request):
    content= util.get_entry(mega_title) 
    return render(request,"encyclopedia/edit.html",{
        "content":content
    })
def random_page(request):
    x = ''.join(random.sample(entry_list,1))
    content = markdown2.markdown(util.get_entry(x))
    return render(request,"encyclopedia/info.html",{
        "content":content
    })