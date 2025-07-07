from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from core.models import Task

def login_view(request):
    return render(request, "login.html")

def register_view(request):
    return render(request, "register.html")

@login_required
def friends_view(request):
    all_users = User.objects.all().order_by("username")

    friends_info = []
    for user in all_users:
        num_assigned = Task.objects.filter(assigner=user, is_completed=False).count()
        num_received = Task.objects.filter(assignee=user, is_completed=False).count()

        friends_info.append({
            "user": user,
            "num_assigned": num_assigned,
            "num_received": num_received,
        })

    return render(request, "friends.html", {
        "friends": friends_info,
        "user": request.user
    })

@login_required
def archive_view(request):
    tasks_assigned = Task.objects.filter(assigner=request.user, is_completed=True)
    tasks_received = Task.objects.filter(assignee=request.user, is_completed=True)
    return render(request, "archive.html", {
        "tasks_assigned": tasks_assigned,
        "tasks_received": tasks_received
    })

# hàm đăng ký
@csrf_exempt
def register_api(request): 
    print("=== ĐÃ VÀO HÀM register_api ===")
    if request.method == "POST":
        try:
            body_unicode = request.body.decode('utf-8')
            print("📦 Raw body:", body_unicode)
            data = json.loads(body_unicode)
            print("✅ Parsed JSON:", data)

            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            if not all([username, email, password]):
                return JsonResponse({"message": "Thiếu thông tin"}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"message": "Username đã tồn tại."}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "Email đã được sử dụng."}, status=400)

            User.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({"message": "Đăng ký thành công."})
        except Exception as e:
            print("❌ Lỗi trong register_api:", str(e))
            return JsonResponse({"message": "Lỗi xử lý dữ liệu."}, status=500)

    return JsonResponse({"message": "Chỉ chấp nhận POST."}, status=405)

# hàm đăng nhập
@csrf_exempt
def login_api(request):
    if request.method == "POST":
        try:
            body_unicode = request.body.decode('utf-8')
            print("📦 Raw body:", body_unicode)
            data = json.loads(body_unicode)
            print("✅ Parsed JSON:", data)

            email = data.get("email")
            password = data.get("password")

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({"message": "Email không tồn tại."}, status=400)

            user_auth = authenticate(username=user.username, password=password)

            if user_auth is not None:
                auth_login(request, user_auth)
                return JsonResponse({"message": "Đăng nhập thành công."})
            else:
                return JsonResponse({"message": "Mật khẩu không đúng."}, status=400)

        except Exception as e:
            print("❌ Lỗi trong login_api:", str(e))
            return JsonResponse({"message": "Lỗi xử lý dữ liệu."}, status=500)

    return JsonResponse({"message": "Chỉ chấp nhận POST."}, status=405)


# hàm giao việc

@csrf_exempt
@login_required
def add_task_view(request):
    if request.method == 'POST':
        assignee_username = request.POST.get('assignee')
        content = request.POST.get('content')
        deadline = request.POST.get('deadline')

        try:
            assignee = User.objects.get(username=assignee_username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Người nhận không tồn tại'}, status=400)

        task = Task.objects.create(
            assigner=request.user,
            assignee=assignee,
            content=content,
            deadline=deadline
        )

        return JsonResponse({
            'content': task.content,
            'assignee': task.assignee.username,
            'deadline': task.deadline.strftime('%Y-%m-%d')
        })

    return JsonResponse({'error': 'Yêu cầu không hợp lệ'}, status=400)


# nút bấm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Task

@login_required
def index_view(request):
    tasks_i_assign = Task.objects.filter(assigner=request.user, is_completed=False).order_by('-created_at')
    tasks_i_receive = Task.objects.filter(assignee=request.user, is_completed=False).order_by('-created_at')

    return render(request, "lobby.html", {
        "user": request.user,
        "tasks_i_assign": tasks_i_assign,
        "tasks_i_receive": tasks_i_receive
    })

@login_required
def archive_view(request):
    tasks_assigned = Task.objects.filter(assigner=request.user, is_completed=True)
    tasks_received = Task.objects.filter(assignee=request.user, is_completed=True)
    return render(request, "archive.html", {
        "tasks_assigned": tasks_assigned,
        "tasks_received": tasks_received
    })
# xoá/hoàn thành công việc
@login_required
def complete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user != task.assignee:
        return JsonResponse({'error': 'Không có quyền hoàn thành'}, status=403)

    task.is_completed = True
    task.save()
    return JsonResponse({'success': True})

@login_required
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user != task.assigner:
        return JsonResponse({'error': 'Không có quyền xoá'}, status=403)

    task.delete()
    return JsonResponse({'success': True})
# xoá trong archive
@login_required
@require_POST
def delete_archived_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, is_completed=True)
        if task.assigner != request.user and task.assignee != request.user:
            return JsonResponse({'success': False, 'error': 'Bạn không có quyền xoá task này.'}, status=403)

        task.delete()
        return JsonResponse({'success': True})
    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Không tìm thấy task.'}, status=404)

