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

def friends_view(request):
    return render(request, "friends.html")

def index_view(request):
    if not request.user.is_authenticated:
        return redirect('/login/')  # Chưa login thì đẩy về login

    return render(request, "index.html", {
        "user": request.user  # Gửi thông tin người dùng vào template
    })

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



# @login_required(login_url="/login/")
# def index_view(request):
#     """Trang chủ: hiển thị task + xử lý form giao việc."""
#     if request.method == "POST":
#         assignee_username = request.POST.get("assignee").strip()
#         content           = request.POST.get("content").strip()
#         deadline          = request.POST.get("deadline")

#         # Tìm người nhận
#         try:
#             assignee = User.objects.get(username=assignee_username)
#             Task.objects.create(
#                 assigner=request.user,
#                 assignee=assignee,
#                 content=content,
#                 deadline=deadline
#             )
#             messages.success(request, f"Đã giao việc cho {assignee_username}.")
#         except User.DoesNotExist:
#             messages.error(request, "Không tìm thấy người nhận.")

#         # 🡒 PRG‑pattern: redirect để tránh gửi lại form khi reload
#         return redirect("index")              # tên urlpattern Trang chủ

#     # --- GET: hiển thị task đang hoạt động ---
#     tasks_i_receive = Task.objects.filter(assignee=request.user, is_done=False)
#     tasks_i_assign  = Task.objects.filter(assigner=request.user, is_done=False)

#     return render(
#         request,
#         "index.html",
#         {
#             "tasks_i_receive": tasks_i_receive,
#             "tasks_i_assign":  tasks_i_assign,
#         },
#     )

@require_POST
@login_required
def add_task_view(request):
    assignee_username = request.POST.get("assignee", "").strip()
    content           = request.POST.get("content", "").strip()
    deadline          = request.POST.get("deadline")

    if not (assignee_username and content and deadline):
        return JsonResponse({"error": "Thiếu thông tin."}, status=400)

    try:
        assignee = User.objects.get(username=assignee_username)
    except User.DoesNotExist:
        return JsonResponse({"error": "Người nhận không tồn tại."}, status=404)

    task = Task.objects.create(
        assigner=request.user,
        assignee=assignee,
        content=content,
        deadline=deadline
    )

    return JsonResponse({
        "content": task.content,
        "assignee": task.assignee.username,
        "deadline": task.deadline.strftime("%Y-%m-%d")
    })









# from .models import FriendRequest

# @require_POST
# @login_required
# def send_friend_request(request):
#     to_username = request.POST.get("username", "").strip()
#     if not to_username:
#         return JsonResponse({"error": "Thiếu tên người dùng."}, status=400)

#     # Không tự gửi cho chính mình
#     if to_username == request.user.username:
#         return JsonResponse({"error": "Không thể kết bạn với chính mình."}, status=400)

#     try:
#         to_user = User.objects.get(username=to_username)
#     except User.DoesNotExist:
#         return JsonResponse({"error": "Người dùng không tồn tại."}, status=404)

#     # Đã là bạn?
#     if to_user.profile in request.user.profile.friends.all():
#         return JsonResponse({"error": "Đã là bạn bè."}, status=400)

#     # Đã có request chờ?
#     fr, created = FriendRequest.objects.get_or_create(
#         sender   = request.user,
#         receiver = to_user,
#         defaults = {"status": FriendRequest.PENDING}
#     )
#     if not created:
#         if fr.status == FriendRequest.PENDING:
#             return JsonResponse({"error": "Đã gửi yêu cầu, đang chờ."}, status=400)
#         # nếu đã reject trước thì cho phép tạo mới
#         fr.status = FriendRequest.PENDING
#         fr.save()

#     return JsonResponse({"message": "Đã gửi lời mời kết bạn."})

# @require_POST
# @login_required
# def respond_friend_request(request):
#     fr_id  = request.POST.get("id")
#     action = request.POST.get("action")  # "accept" / "reject"
#     try:
#         fr = FriendRequest.objects.get(id=fr_id, receiver=request.user, status=FriendRequest.PENDING)
#     except FriendRequest.DoesNotExist:
#         return JsonResponse({"error": "Yêu cầu không hợp lệ."}, status=404)

#     if action == "accept":
#         fr.accept()
#         return JsonResponse({"message": "Đã chấp nhận."})
#     elif action == "reject":
#         fr.reject()
#         return JsonResponse({"message": "Đã từ chối."})
#     return JsonResponse({"error": "Hành động không hợp lệ."}, status=400)

# @login_required
# def friends_page(request):
#     pending_in  = FriendRequest.objects.filter(receiver=request.user, status=FriendRequest.PENDING)
#     pending_out = FriendRequest.objects.filter(sender=request.user, status=FriendRequest.PENDING)
#     friends     = request.user.profile.friends.all()
#     return render(request, "friends.html", {
#         "pending_in":  pending_in,
#         "pending_out": pending_out,
#         "friends":     friends,
#     })
