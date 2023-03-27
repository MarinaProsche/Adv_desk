from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from .models import Adv, Reply, Author
from .forms import AdvForm, CreateReplyForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from .filters import AdvFilter
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin


class AdvList(ListView):
    model = Adv
    ordering = '-date_adv'
    template_name = 'adv.html'
    context_object_name = 'adv'
    # paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdvFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        # context['content'] = Adv.objects.prefetch_related('media').values('media__content')
        # context['current_time'] = timezone.localtime(timezone.now())
        # context['timezones'] = pytz.common_timezones
        return context

class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False
    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)
    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)

class AdvDetail(CustomSuccessMessageMixin, LoginRequiredMixin, FormMixin, DetailView):
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
        return super().form_valid(form)

class AdvCreate(CustomSuccessMessageMixin, LoginRequiredMixin, CreateView):
    # permission_required = ('adv_app.add_adv')
    form_class = AdvForm
    model = Adv
    template_name = 'adv_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AdvForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.author = self.request.user
            author.save()
        return redirect('/advs/')


class AdvUpdate(CustomSuccessMessageMixin, LoginRequiredMixin, UpdateView):
    # permission_required = ('adv_app.change_adv',)
    form_class = AdvForm
    model = Adv
    template_name = 'adv_create.html'
    success_url = reverse_lazy('nadv')
    success_msg = 'Ваше объявление отредактировано!'

    def get_form_kwargs(self):
        kwargs = super(AdvUpdate, self).get_form_kwargs()
        kwargs['author'] = self.request.user
        return kwargs

class AdvDelete(LoginRequiredMixin, DeleteView,):
    # permission_required = ('adv_app.delete_adv',)
    model = Adv
    template_name = 'advdelete.html'
    success_url = reverse_lazy('advs')

class DetailReply(DetailView):
    model = Reply

# def image_upload_view(request):
#     """Process images uploaded by users"""
#     if request.method == 'POST':
#         form = AdvForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             Get the current instance object to display in the template
#             content = form.instance
#             return render(request, 'adv_create.html', {'form': form, 'content': content})
#     else:
#         form = AdvForm()
#     return render(request, 'adv_create.html', {'form': form})
