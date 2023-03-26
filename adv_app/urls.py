from django.urls import path
from .views import AdvList, AdvDetail, AdvCreate, AdvUpdate, AdvDelete, Adv, LoginView
from personalpage.views import accept
from sign.views import GetCode

# CreateReplyFormView

urlpatterns = [
    path('', AdvList.as_view(), name = 'advs'),
    path('<int:pk>', (AdvDetail.as_view()), name = 'nadv'),
    path('create', (AdvCreate.as_view()), name = 'advcreate'),
    path('edit/<int:pk>', (AdvUpdate.as_view()), name = 'advedit'),
    path('delete/<int:pk>', AdvDelete.as_view(), name='advdelete'),
    path('code/<str:user>', GetCode.as_view(), name='code'),
    path('reply/accept/<int:pk>', accept, name = 'acceptit')

    # path('reply', CreateReplyFormView.as_view(), name='replycreate'),
]