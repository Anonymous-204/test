
# Create your models here.
# models.py
# from django.db import models
# from django.contrib.auth.models import User

# class Task(models.Model):
#     assigner   = models.ForeignKey(User, related_name="tasks_assigned", on_delete=models.CASCADE)
#     assignee   = models.ForeignKey(User, related_name="tasks_received", on_delete=models.CASCADE)
#     content    = models.TextField()
#     deadline   = models.DateField()
#     is_done    = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.content[:30]}… → {self.assignee.username}"


from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    assigner = models.ForeignKey(User, related_name="tasks_assigned", on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name="tasks_received", on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    deadline = models.DateField()
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content} ({self.assigner.username} → {self.assignee.username})"
