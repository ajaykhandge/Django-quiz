 
from django.urls import path
from users import views as users_views
from django.contrib.auth import views as auth_views
from .views import index,welcome,quiz,quiz_question,check_question,thanks,leaderboard,forbidden


urlpatterns = [
    path('index/',index,name="index"),
    path('welcome/',welcome,name='welcome'),
    path('leaderboard/<str:quiz_name>',leaderboard,name='leaderboard'),
    path('thanks/',thanks,name='thanks'),
    path('quiz/',quiz,name='quiz'),
     path('forbidden/',forbidden,name='forbidden'),
    path('ajax/quiz/',quiz_question,name='quiz_questions'),
    path('ajax/quiz/check_ans',check_question,name='check_questions'),
    
    
]   