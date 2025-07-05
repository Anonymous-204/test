/* ===========================================================
   MENU/FORMS – ẨN HIỆN TOÀN CỤC
=========================================================== */
// ─── Phần tử DOM ───────────────────────────────────────────
const toggleFriends   = document.getElementById("toggle-friends");
const friendsList     = document.getElementById("friends-list");

const toggleAddFriend = document.getElementById("toggle-addfriend");
const addFriendForm   = document.getElementById("add-friend-form");

const memberBtn       = document.getElementById("member-button");
const memberDropdown  = document.getElementById("member-dropdown");

const accountBtn      = document.getElementById("account");
const accountDropdown = document.getElementById("dropdown-menu");

const assignBtn       = document.getElementById("show-form-task");
const assignFormWrap  = document.getElementById("assignForm");

// ─── Hàm ẩn tất cả menu/form ──────────────────────────────
function hideAll() {
  friendsList?.classList.add("hidden");
  addFriendForm?.classList.add("hidden");
  memberDropdown?.classList.add("hidden");
  accountDropdown?.classList.add("hidden");
  if (assignFormWrap) assignFormWrap.style.display = "none";
}

// ─── Toggle helpers (ẩn hết trước khi bật cái mới) ────────
function makeToggle(btn, panel, isBlock = false) {
  btn?.addEventListener("click", (e) => {
    e.preventDefault();
    hideAll();
    if (panel) {
      if (isBlock) {
        panel.style.display = "block";
      } else {
        panel.classList.toggle("hidden");
      }
    }
    e.stopPropagation();      // giữ menu khi bấm chính nút
  });
}

// Bạn bè & Thêm bạn
makeToggle(toggleFriends, friendsList);
makeToggle(toggleAddFriend, addFriendForm);

// Thành viên & Tài khoản
makeToggle(memberBtn,  memberDropdown);
makeToggle(accountBtn, accountDropdown);

// Giao việc
makeToggle(assignBtn, assignFormWrap, true);

// ─── Ẩn tất cả khi click ngoài khu menu/form ──────────────
document.addEventListener("click", function (e) {
  // Nếu click vào các vùng "cho phép" => không ẩn
  if (
    toggleFriends?.contains(e.target) || friendsList?.contains(e.target) ||
    toggleAddFriend?.contains(e.target) || addFriendForm?.contains(e.target) ||
    memberBtn?.contains(e.target) || memberDropdown?.contains(e.target) ||
    accountBtn?.contains(e.target) || accountDropdown?.contains(e.target) ||
    assignBtn?.contains(e.target) || assignFormWrap?.contains(e.target)
  ) {
    return; // giữ nguyên nếu click vùng hợp lệ
  }

  // Nếu không thì ẩn tất cả
  hideAll();
});


/* ===========================================================
   FRIEND REQUEST  |  ADD TASK (fetch + CSRF)
=========================================================== */
// Gửi yêu cầu kết bạn
document.getElementById("friend-form")?.addEventListener("submit", function (e) {
  e.preventDefault();
  fetch("/send-friend-request/", {
    method: "POST",
    headers: { "X-CSRFToken": getCookie("csrftoken") },
    body: new FormData(this)
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("friend-message").innerText = data.message || data.error;
    this.reset();
  });
});

// Gửi task mới
document.getElementById("assign-form")?.addEventListener("submit", async function (e) {
  e.preventDefault();
  const res = await fetch("/add-task/", {
    method: "POST",
    headers: { "X-CSRFToken": getCookie("csrftoken") },
    body: new FormData(this)
  });
  const data = await res.json();
  if (data.error) return alert("Lỗi: " + data.error);

  const card = document.createElement("div");
  card.className = "task-card";
  card.innerHTML = `
    <strong>${data.content}</strong><br>
    Người nhận: ${data.assignee}<br>
    Deadline&nbsp;: ${data.deadline}`;
  document.getElementById("sent-tasks").appendChild(card);
  this.reset();
  hideAll();                          // ẩn form sau khi gửi
});

// Lấy CSRF Django
function getCookie(name) {
  return document.cookie
    .split(";")
    .map(c => c.trim())
    .find(c => c.startsWith(name + "="))
    ?.split("=")[1] ?? "";
}
// công việc

function completeTask(taskId) {
  fetch(`/complete-task/${taskId}/`, {
    method: "POST",
    headers: { "X-CSRFToken": getCookie("csrftoken") }
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      const card = document.getElementById(`task-${taskId}`);
      if (card) card.remove();
    } else {
      alert(data.error || "Có lỗi khi hoàn thành công việc.");
    }
  });
}

function deleteTask(taskId) {
  fetch(`/delete-task/${taskId}/`, {
    method: "POST",
    headers: { "X-CSRFToken": getCookie("csrftoken") }
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      const card = document.getElementById(`task-${taskId}`);
      if (card) card.remove();
    } else {
      alert(data.error || "Không thể xoá công việc.");
    }
  });
}
