from django.urls import path
from . import views  

urlpatterns = [
    path('task/', views.Tasklist, name="task-list"),
    path('newtask/', views.NewTask, name="new-task"), #C
    path('task/<int:id>', views.TaskView, name="task-view"), #R
    path('edit/<int:id>', views.EditTask, name="task-edit"), #U
    path('changestatus/<int:id>', views.ChangeStatus, name="change-status"), #U
    path('delete/<int:id>', views.DeleteTask, name='task-delete'), #D
]
