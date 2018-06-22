from django.shortcuts import render , get_object_or_404 
from django.http import HttpResponse , HttpResponseRedirect , Http404
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.db.models import Q


from .models import Blocktable, CommentTable
from .form import Blockform

def isLoginAndPermission(request):
    if(request.user.is_superuser):
        return {"id":request.session["_auth_user_id"], "isLogin" : True, "username" : request.user}
    if request.user.is_authenticated:
        return {"id":request.session["_auth_user_id"], "isLogin" : True, "username" : request.user}
    else :
        return {"isLogin" : False, "username" : ""}

def isWhiteSpaceOrEmpty(string):
    if string == "" :
        return True
    elif string.isspace():
        return True
    else:
        return False

def index(request):
    print(isLoginAndPermission(request))
    if(request.user.is_superuser):
        listBlock = Blocktable.objects.order_by('-date')

    elif request.user.is_authenticated:
        filterlist = Blocktable.objects.filter(Q(isPrivate=0) | Q(authId=request.session["_auth_user_id"]))
        listBlock = filterlist.order_by('-date')
    else:
        filterlist = Blocktable.objects.filter( isPrivate = 0)
        listBlock = filterlist.order_by('-date')

    return render(request,'index.html',{"listblock" : listBlock, "login" : isLoginAndPermission(request) })

def showBlockUsers(request, userid):
    
    filterlistBlock = Blocktable.objects.filter(authId=userid)
    listBlock = filterlistBlock.order_by('-date')


    return render(request,'listblockuser.html',{"listblock" : listBlock, "login" : isLoginAndPermission(request) })

def showBlock(request, blockid):

    filerlistComment = CommentTable.objects.filter(blockId=blockid)
    listComment = filerlistComment.order_by('-date')

    oneBlock = get_object_or_404(Blocktable, id=blockid)
    login = isLoginAndPermission(request)
    
    if((oneBlock.authId == isLoginAndPermission(request)["username"])or request.user.is_superuser):
        login["canEdit"] = True
    else:
        login["canEdit"] = False


    return render(request,'detailOneBlock.html',{"blockone" : oneBlock,"listComment":listComment , "login" : login })


def createBlockform(request):
    return render(request,'createBlockForm.html',{"login" : isLoginAndPermission(request)})

def creteBlock(request):
    if request.method  == "POST" :
        
        form = Blockform(request.POST)
        
        if(isWhiteSpaceOrEmpty(request.POST.get("title"))):
            return HttpResponseRedirect(reverse('blockapp:createblockform'))
        elif(isWhiteSpaceOrEmpty(request.POST.get("content"))):
            return HttpResponseRedirect(reverse('blockapp:createblockform'))
        if form.is_valid():
            
            obj = Blocktable()
            obj.title = form.cleaned_data['title']
            obj.content = form.cleaned_data['content']
            obj.isPrivate = int(request.POST.get("status"))
            obj.authId = request.user
            obj.save()
            return HttpResponseRedirect(reverse('blockapp:oneblock', args=(obj.id,)))
        return Http404("Error")
    else:        
        return Http404("Error")
    
def updateBlockForm(request, blockid):
    
    oneBlock = get_object_or_404(Blocktable, id=blockid)
    return render(request,'updateBlockForm.html',{"blockone" : oneBlock , "login" : isLoginAndPermission(request) })


def updateBlock(request, blockid):
    if request.method == "POST":
        obj = Blocktable.objects.get(id=blockid)
        print(blockid)
        obj.title = request.POST.get("title")
        obj.content = request.POST.get("content")
        obj.isPrivate = int(request.POST.get("status"))
        obj.save()

    return HttpResponseRedirect(reverse('blockapp:oneblock', args=(blockid,)))

def delete(request, blockid):
    block = get_object_or_404(Blocktable, id=blockid)
    block.delete()
    return HttpResponseRedirect(reverse('blockapp:index'))


def commetPost(request, blockid):
    blockone = Blocktable(pk=blockid)
    print(blockid)
    if request.method == "POST":
        obj = CommentTable()
        obj.content = request.POST.get("commentContent")
        obj.authId = isLoginAndPermission(request)["username"]
        obj.blockId = blockone
        obj.save()
    
    return HttpResponseRedirect(reverse('blockapp:oneblock', args=(blockid,)))

def searchListBlock(request):

    text = request.POST.get("search")
    if request.user.is_superuser :
        filterListBlockSearch = Blocktable.objects.filter(title__contains=text)
        listblockSearch = filterListBlockSearch.order_by('-date')

    elif isLoginAndPermission(request)["isLogin"] :
        filterListBlockSearch = Blocktable.objects.filter(title__contains=text)
        filterlist = filterListBlockSearch.filter(Q(isPrivate=0) | Q(authId=request.session["_auth_user_id"]))
        listblockSearch = filterlist.order_by('-date')

    else: 
        filterListBlockSearch = Blocktable.objects.filter(title__contains=text ,isPrivate= 0)
        listblockSearch = filterListBlockSearch.order_by('-date')

    return render(request,'searchList.html',{"searchname":text , "listBlock" : listblockSearch, "login" : isLoginAndPermission(request)})
