from django.urls import path
from .views import AdvList, AdvDetail, AdvCreate

urlpatterns = [
    path('', AdvList.as_view(), name = 'advs'),
    path('<int:pk>', (AdvDetail.as_view()), name = 'nadv'),
    path('create', (AdvCreate.as_view()), name = 'advcreate')
]