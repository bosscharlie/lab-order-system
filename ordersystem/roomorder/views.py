from django.shortcuts import render
from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from . import models
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
            res["msg"]="/index/"
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