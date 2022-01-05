from django.urls import path
from qna import views

app_name = 'qna'

urlpatterns = [
    path('', views.index, name='index'),
    path('<context_id>/', views.his_sub, name='his_sub'),
]
