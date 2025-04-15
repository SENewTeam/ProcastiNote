from django.urls import path
from  comments import views

urlpatterns = [
    path('create/', views.createComment),
    path('getAllComment/',views.get_all_paper),
    path('getComment/<paper_id>/', views.get_comments_for_paper),
    path('updateComment/<comment_id>/', views.update_comment),
    path('deleteComment/<comment_id>/', views.delete_comment),
]
