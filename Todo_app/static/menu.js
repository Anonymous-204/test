// ===========================
// TOGGLE FORM & DROPDOWN
// ===========================

// DOM elements
const assignBtn       = document.getElementById("show-form-task");
const assignFormWrap  = document.getElementById("assignForm");
const accountBtn      = document.getElementById("account");
const accountDropdown = document.getElementById("dropdown-menu");

// Ẩn tất cả menu/form hiện tại
function hideAll() {
  if (assignFormWrap) assignFormWrap.style.display = "none";
  accountDropdown?.classList.add("hidden");
}

// Toggle đơn giản
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
    e.stopPropagation();
  });
}

// Kích hoạt toggle cho các thành phần
makeToggle(assignBtn, assignFormWrap, true);
makeToggle(accountBtn, accountDropdown);

// Ẩn form nếu click ra ngoài
document.addEventListener("click", function (e) {
  if (
    assignBtn?.contains(e.target) || assignFormWrap?.contains(e.target) ||
    accountBtn?.contains(e.target) || accountDropdown?.contains(e.target)
  ) {
    return;
  }
  hideAll();
});


// ===========================
// FORM GIAO VIỆC (AJAX)
// ===========================

document.getElementById("assign-form")?.addEventListener("submit", async function (e) {
  e.preventDefault();
  const res = await fetch("/add-task/", {
    method: "POST",
    headers: { "X-CSRFToken": getCookie("csrftoken") },
    body: new FormData(this)
  });
  const data = await res.json();
  if (data.error) return alert("Lỗi: " + data.error);

  // Nếu có vùng hiển thị task thì thêm vào
  const container = document.getElementById("sent-tasks");
  if (container) {
    const card = document.createElement("div");
    card.className = "task-card";
    card.innerHTML = `
      <strong>${data.content}</strong><br>
      Người nhận: ${data.assignee}<br>
      Deadline&nbsp;: ${data.deadline}`;
    container.appendChild(card);
  }

  this.reset();
  hideAll();
});


// Lấy CSRF Token từ cookie
function getCookie(name) {
  return document.cookie
    .split(";")
    .map(c => c.trim())
    .find(c => c.startsWith(name + "="))
    ?.split("=")[1] ?? "";
}

// Hoàn thành công việc
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

// Xoá công việc chưa hoàn thành
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

// Xoá công việc đã hoàn thành (trong archive)
function deleteArchivedTask(taskId) {
  fetch(`/delete-archived-task/${taskId}/`, {
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

async function logout(event) {
  // ✅ Chặn hành vi mặc định của thẻ <a href="#"> (cuộn lên đầu trang)
  if (event) event.preventDefault();

  try {
    const response = await fetch("/api/logout/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
    });

    const data = await response.json();

    if (response.ok && data.success) {
      localStorage.clear();
      sessionStorage.clear();
      alert("🚪 Đăng xuất thành công!");
      window.location.href = "/login/";
    } else {
      alert("❌ Lỗi đăng xuất: " + (data.message || "Không rõ nguyên nhân"));
    }
  } catch (err) {
    alert("⚠️ Lỗi kết nối khi đăng xuất: " + err.message);
  }
}
