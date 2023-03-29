from django.urls import path
from .views import AdvList, AdvDetail, AdvCreate, AdvUpdate, AdvDelete, Adv, LoginView
from personalpage.views import AcceptReplyView, DeleteReplyView, PasswordsChangeView, password_success

from sign.views import GetCode
from django.contrib.staticfiles.urls import static
from adv_project import settings
from django.contrib.auth.forms import PasswordChangeForm

urlpatterns = [
    path('', AdvList.as_view(), name = 'advs'),
    path('<int:pk>', (AdvDetail.as_view()), name = 'nadv'),
    path('create', (AdvCreate.as_view()), name = 'advcreate'),
    path('edit/<int:pk>', AdvUpdate.as_view(), name = 'advedit'),
    path('delete/<int:pk>', AdvDelete.as_view(), name='advdelete'),
    path('code/<str:user>', GetCode.as_view(), name='code'),
    path('accept/<int:pk>', AcceptReplyView.as_view(), name='reply_accept'),
    path('deletereply/<int:pk>', DeleteReplyView.as_view(), name='reply_delete'),
    path('password_change/', PasswordsChangeView.as_view(), name='password_change'),
    path('password_change/done/', password_success, name='password_change_done'),
]