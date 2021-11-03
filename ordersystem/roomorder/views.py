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
        htmls+='<tr><td id="room{}">{}({})</td>'.format(room.id,room.caption,room.capacity)
        for time in time_choice:
            #判断单元格是否已经被预定
            flag=False
            status=0
            for book in book_list:
                if book.room.pk==room.pk and book.time_id==time[0] and (book.status==2 or (book.status==1 and request.user.username==book.user.username)):
                    flag=True
                    status=book.status
                    break
            if flag:
                #判断登陆人与预定人是否一致
                if request.user.username==book.user.username:
                    if status==1:#待审批
                        htmls+='<td class="myready danger item" room_id={} time_id={}>已申请，待审批</td>'.format(room.pk,time[0])
                    elif status==2:#通过审批
                        htmls += '<td class="mypass info item" room_id={} time_id={}>已占用</td>'.format(room.pk, time[0])
                else:
                    htmls+='<td class="otherpass success item" room_id={} time_id={}>已占用</td>'.format(room.pk,time[0])
            else:
                htmls+='<td class="item" room_id={} time_id={}></td>'.format(room.pk,time[0])
        htmls+="</tr>"
    return render(request,'index.html',{"time_choice":time_choice,"htmls":htmls,})

def book(request):
    if request.method == "POST":
        choose_date=request.POST.get("choose_date")
        #获取会议室时间段列表
        time_choice=models.Book.time_choice
        try:
            #向数据库修改会议室预定记录
            post_data=json.loads(request.POST.get("post_data"))
            print(post_data)
            if not post_data["room_id"]:
                #没有任何修改
                res={"status":2,"msg":""}
                return HttpResponse(json.dumps(res))
            user=request.user
            room_id=post_data["room_id"]
            time_id=post_data["time_id"]
            coursename=post_data["coursename"]
            teacher=post_data["teacher"]
            printel=post_data["printel"]
            bookertel=post_data["bookertel"]
            if request.POST.get("batch"):
            #添加新的预定信息
                models.Book.objects.create(user=user, room_id=room_id, time_id=time_id, date=choose_date,coursename=coursename,
                                           teacher=teacher,printel=printel,batch=True)
            else:
                models.Book.objects.create(user=user, room_id=room_id, time_id=time_id, date=choose_date,coursename=coursename,
                                           teacher=teacher, printel=printel)
            #删除旧预定信息
            # from django.db.models import Q
            # remove_book=Q()
            # for room_id, time_id_list in post_data["DEL"].items():
            #     temp = Q()
            #     for time_id in time_id_list:
            #         temp.children.append(("room_id", room_id))
            #         temp.children.append(("time_id", time_id))
            #         temp.children.append(("user_id", request.user.pk))
            #         temp.children.append(("date", choose_date))
            #         remove_book.add(temp, "OR")
            # if remove_book:
            #     models.Book.objects.filter(remove_book).delete()
            #     for time in post_data["DEL"][room_id]:
            #         models.Book.objects.filter(user=user,room_id=room_id,time_id=time,date=choose_date).delete()
            res={"status":1,"msg":''}
        except Exception as e:
            res={"status":0,"msg":str(e)}
            print(e)
        return HttpResponse(json.dumps(res))


def reg(request):
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        form_obj = forms.RegForm(request.POST)
        print(request.POST)
        avatar_img = request.FILES.get("avatar")
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

def detail(request):
    if request.method=="POST":
        user=request.user
        choose_date=request.POST.get("choose_date")
        post_data = json.loads(request.POST.get("post_data"))
        room_id=post_data["room_id"]
        time_id=post_data["time_id"]
        #获取详情信息
        destination=models.Book.objects.filter(date=choose_date,time_id=time_id)[0]
        if destination:
            print(destination.coursename)
    # 给前端返回详情信息
    res={"status":1,"msg":"","coursename":destination.coursename,"teacher":destination.teacher,
         "printel":destination.printel,"adminer":destination.adminer}
    return HttpResponse(json.dumps(res))

def acc_logout(request):
    logout(request)
    return redirect("/roomorder/login/")

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