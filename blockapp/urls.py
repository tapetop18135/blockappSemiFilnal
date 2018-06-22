from django.urls import path
from . import views
app_name = 'blockapp'
urlpatterns = [
    path('', views.index, name="index"),
    path('<int:blockid>/', views.showBlock, name="oneblock"),
    path('user/<int:userid>/', views.showBlockUsers, name="listblockuser"),

    path('serachList/', views.searchListBlock, name="searchlistblock"),
    path('serachList/<str:searchtext>', views.showSearchlist, name="showSearchlist"),

    path('<int:blockid>/comment', views.commetPost, name="commentPost"),

    path('createblockform/', views.createBlockform, name="createblockform"),
    path('createblock/', views.creteBlock, name="createblock"),

    path('<int:blockid>/updateblockform', views.updateBlockForm, name="updateblockform"),    
    path('<int:blockid>/updateblock', views.updateBlock, name="updateblock"),
    
    path('<int:blockid>/delete', views.delete, name="deleteblock"),
]