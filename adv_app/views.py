from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from .models import Adv, Reply, Author, Media
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
        context['content'] = Adv.objects.prefetch_related('media').values('media__content')
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

# class AdvInline():
#     form_class = AdvForm
#     model = Adv
#     template_name = "adv_create"
#     success_msg = 'Поздравляем! Ваше объявление опубликовано!'
#
#     def form_valid(self, form):
#         named_formsets = self.get_named_formsets()
#         if not all((x.is_valid() for x in named_formsets.values())):
#             return self.render_to_response(self.get_context_data(form=form))
#
#         self.object = form.save()
#         for every formset, attempt to find a specific formset save function
#         otherwise, just save.
#
#         for name, formset in named_formsets.items():
#             formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
#             if formset_save_func is not None:
#                 formset_save_func(formset)
#             else:
#                 formset.save()
#         return redirect('advs')

    # def formset_medias_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        # medias = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter
        # set in inlineformset_factory func
        # for obj in formset.deleted_objects:
        #     obj.delete()
        # for media in medias:
        #     media.adv = self.object
        #     media.save()

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
        return redirect('/')

    # def get_context_data(self, **kwargs):
    #     ctx = super(AdvCreate, self).get_context_data(**kwargs)
    #     ctx['named_formsets'] = self.get_named_formsets()
    #     return ctx

    # def get_named_formsets(self):
    #     if self.request.method == "GET":
    #         return {
    #             'medias': AddMediaFormSet(prefix='medias'),
    #         }
    #     else:
    #         return {
    #             'medias': AddMediaFormSet(self.request.POST or None, self.request.FILES or None, prefix='medias'),
    #         }

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

    # def get_context_data(self, **kwargs):
    #     ctx = super(AdvUpdate, self).get_context_data(**kwargs)
    #     ctx['named_formsets'] = self.get_named_formsets()
    #     return ctx
    #
    # def get_named_formsets(self):
    #     return {
    #         'medias': AddMediaFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object,
    #                                        prefix='medias'),
    #         }
class AdvDelete(LoginRequiredMixin, DeleteView,):
    # permission_required = ('adv_app.delete_adv',)
    model = Adv
    template_name = 'advdelete.html'
    success_url = reverse_lazy('advs')

class DetailReply(DetailView):
    model = Reply
