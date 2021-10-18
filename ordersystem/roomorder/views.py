from django.shortcuts import render
from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
import json
import datetime

def acc_login(request):
    if request.method=="POST":
        print(request.POST)
        res={"status":0,"msg":""}
        username=request.POST.get("username")
        password=request.POST.get("pwd")
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            res["msg"]="/roomorder/index/"
        else:
            #登陆认证失败
            res["status"]=1
            res["msg"]="登陆认证失败，请检查用户名及密码是否正确"
        return JsonResponse(res)
    return render(request,'login.html')


#@login_required(login_url="/login/")
def index(request):
    date=datetime.datetime.now().date()
    #没有指定日期default当天日期
    book_date=request.GET.get("book_date",date)
    #获取会议室时间段列表
    time_choice=models.Book.time_choice
    #获取会议室列表
    room_list=models.Room.objects.all()
    #获取会议室预定信息
    book_list=models.Book.objects.filter(date=book_date)
    htmls=''
    for room in room_list:
        htmls+='<tr><td>{}({})</td>'.format(room.caption,room.capacity)
        for time in time_choice:
            #判断单元格是否已经被预定
            flag=False
            for book in book_list:
                if book.room.pk==room.pk and book.time_id==time[0]:
                    flag=True
                    break
            if flag:
                #判断登陆人与预定人是否一致
                if request.user.username==book.user.username:
                    htmls+='<td class="info item" room_id={} time_id={}>{}</td>'.format(room.pk,time[0],book.user.username)
                else:
                    htmls+='<td class="success item" room_id={} time_id={}>{}</td>'.format(room.pk,time[0],book.user.username)
            else:
                htmls+='<td class="item" room_id={} time_id={}></td>'.format(room.pk,time[0])
        htmls+="</tr>"
    return render(request,'index.html',{"time_choice":time_choice,"htmls":htmls,})

def book(request):
    if request.method == "POST":
        print(request.POST)
        choose_date=request.POST.get("choose_date")
        #获取会议室时间段列表
        time_choice=models.Book.time_choice
        try:
            #向数据库修改会议室预定记录
            post_data=json.loads(request.POST.get("post_data"))
            if not post_data["ADD"] and not post_data["DEL"]:
                #没有任何修改
                res={"status":2,"msg":""}
                return HttpResponse(json.dumps(res))
            user=request.user
            #添加新的预定信息
            book_list=[]
            for room_id,time_id_list in post_data["ADD"].items():
                for time_id in time_id_list:
                    book_obj=models.Book(user=user, room_id=room_id, time_id=time_id, date=choose_date)
                    book_list.append(book_obj)
            models.Book.objects.bulk_create(book_list)
            #删除旧预定信息
            from django.db.models import Q
            remove_book=Q()
            for room_id, time_id_list in post_data["DEL"].items():
                temp = Q()
                for time_id in time_id_list:
                    temp.children.append(("room_id", room_id))
                    temp.children.append(("time_id", time_id))
                    temp.children.append(("user_id", request.user.pk))
                    temp.children.append(("date", choose_date))
                    remove_book.add(temp, "OR")
            if remove_book:
                models.Book.objects.filter(remove_book).delete()
                for time in post_data["DEL"][room_id]:
                    models.Book.objects.filter(user=user,room_id=room_id,time_id=time,date=choose_date).delete()
            res={"status":1,"msg":''}
        except Exception as e:
            res={"status":0,"msg":str(e)}
        return HttpResponse(json.dumps(res))


def reg(request):
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        form_obj = forms.RegForm(request.POST)
        # print('request.POST'.center(80, '#'))
        print(request.POST)
        # print('request.POST'.center(80, '#'))
        avatar_img = request.FILES.get("avatar")
        # print(avatar_img)
        print(form_obj.is_valid())
        # 帮我做校验
        if form_obj.is_valid():
            # 校验通过，去数据库创建一个新的用户
            form_obj.cleaned_data.pop("re_password")
            print(form_obj.cleaned_data)
            try:
                models.UserInfo.objects.create_user(**form_obj.cleaned_data)
            except Exception as e:
                print(e)
            ret["msg"] = "/roomorder/login/"
            return JsonResponse(ret)
        else:
            print(form_obj.errors)
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            print(ret)
            print("=" * 120)
            return JsonResponse(ret)
            # 生成一个form对象
    form_obj = forms.RegForm()
    print(form_obj.fields)
    return render(request,'reg.html',{"form_obj": form_obj})

def acc_logout(request):
    logout(request)
    return redirect("/login/")

def check_username_exist(request):
    username=request.GET.get("username")
    res={"status":0,"msg":""}
    print(models.UserInfo.objects.filter(username=username))
    if models.UserInfo.objects.filter(username=username):
        res = {"status": 1, "msg": ""}
    return HttpResponse(json.dumps(res))
#
# def home(request):
#