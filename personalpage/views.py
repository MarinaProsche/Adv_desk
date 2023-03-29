from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.models import User

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import TemplateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from adv_app.models import Adv, Reply


class LoginView(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'personalpage.html'
    context_object_name = "personal_adv"
    ordering = '-date_replay'

class AcceptReplyView(LoginRequiredMixin, TemplateView):
    template_name = 'accept_reply.html'

    def get_context_data(self, **kwargs):
        id = self.kwargs.get('pk')
        reply = Reply.objects.get(pk=id)
        email = User.objects.get(id=reply.author_id)
        send_mail(
            subject=f'Ваш отклик принят!',
            message=f'Ваш отклик: {reply.text_reply} {self.request.user} принят!',
            from_email='marinaprosche@yandex.ru',
            recipient_list=[email.email],
        )
        reply.accept_reply()

class DeleteReplyView(LoginRequiredMixin, DeleteView):
    template_name = 'delete_reply.html'
    queryset = Reply.objects.all()
    context_object_name = 'reply'
    success_url = reverse_lazy('personal')

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'account/password_change_form.html'

def password_success(request):
    return render(request, 'account/password_change_done.html')