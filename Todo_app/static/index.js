function deleteArchivedTask(taskId) {
  fetch(`/delete-archived-task/${taskId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    }
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
