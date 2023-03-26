from django.shortcuts import render, redirect


from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from adv_app.models import Adv, Reply
from adv_app.filters import UserAdvFilter

class LoginView(LoginRequiredMixin, ListView):
    model = Adv
    template_name = 'personalpage.html'
    context_object_name = "personal_adv"


def accept(request, **kwargs):
    pass


    # author = request.user
    # advs = Adv.objects.filter(author = author)   #получаем все объявления этого автора
    # for item in advs: #для каждого объявления в объявлениях
    #     replys = item.reply.all() #получаем все комментарии к каждому объявлению
    #     for n in replys:
    #         id = n.id
    #         reply = Reply.objects.get(id=id)
    #         reply.accept_reply()
    #         return redirect('/')






