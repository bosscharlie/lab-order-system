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