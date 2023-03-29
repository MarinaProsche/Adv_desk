from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from .models import Adv, Reply
from .forms import AdvForm, CreateReplyForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from .filters import AdvFilter
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.core.mail import send_mail
from django.contrib.auth.models import User


class AdvList(ListView):
    model = Adv
    ordering = '-date_adv'
    template_name = 'adv.html'
    context_object_name = 'adv'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdvFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class CustomSuccessMessageMixin:
    # короткие сообщения пользователю - на данный момент используется только при отправлении комментария
    @property
    def success_msg(self):
        return False
    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)
    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)

class AdvDetail(CustomSuccessMessageMixin, FormMixin, DetailView):
    # permission_required = ('adv_app.add_reply',)
    model = Adv
    template_name = 'nadv.html'
    context_object_name = 'nadv' # n по логике с номером
    form_class = CreateReplyForm
    success_msg = 'Комментарий успешно создан, ожидайте модерации'

    def get_success_url(self):
        return reverse_lazy('nadv', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.adv = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        user = User.objects.get(username=self.object.adv.author)
        send_mail(
            subject=f'Новый отклик!',
            message=f'{user}, здравствуйте! У вас новый отклик на статью "{self.object.adv.head_adv}"',
            from_email='marinaprosche@yandex.ru',
            recipient_list=[user.email],
        )

        return super().form_valid(form)

class AdvCreate(CustomSuccessMessageMixin, LoginRequiredMixin, CreateView):
    # permission_required = ('adv_app.add_adv')
    form_class = AdvForm
    model = Adv
    template_name = 'adv_create.html'
    success_url = reverse_lazy('advs')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AdvForm()
        return context

    def form_valid(self, form):
        adv = form.save(commit=False)
        form.instance.author = self.request.user
        return super().form_valid(form)

class AdvUpdate(CustomSuccessMessageMixin, LoginRequiredMixin, UpdateView):
    # permission_required = ('adv_app.change_adv',)
    form_class = AdvForm
    model = Adv
    template_name = 'adv_create.html'
    success_url = reverse_lazy('advs')
    # success_msg = 'Ваше объявление отредактировано!'

class AdvDelete(LoginRequiredMixin, DeleteView,):
    # permission_required = ('adv_app.delete_adv',)
    model = Adv
    template_name = 'advdelete.html'
    success_url = reverse_lazy('advs')
