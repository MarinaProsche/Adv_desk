from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Adv, Reply, Author, Media
from django.shortcuts import redirect
from .forms import AdvForm, AddMediaFormSet
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import AdvFilter

class AdvList(ListView):
    model = Adv
    ordering = 'date_adv'
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

class AdvDetail(DetailView):
    model = Adv
    template_name = 'nadv.html'
    context_object_name = 'nadv' # n по логике с номером


class AdvInline():
    form_class = AdvForm
    model = Adv
    template_name = "adv_create"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()
        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('advs')

    def formset_medias_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        medias = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for media in medias:
            media.adv = self.object
            media.save()

class AdvCreate(LoginRequiredMixin, AdvInline, CreateView):
    # permission_required = ('adv_app.add_post')
    form_class = AdvForm
    model = Adv
    template_name = 'adv_create.html'

    def get_form_kwargs(self):
        kwargs = super(AdvCreate, self).get_form_kwargs()
        kwargs['author'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(AdvCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'medias': AddMediaFormSet(prefix='medias'),
            }
        else:
            return {
                'medias': AddMediaFormSet(self.request.POST or None, self.request.FILES or None, prefix='medias'),
            }

class AdvUpdate(AdvInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(AdvUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'medias': AddMediaFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object,
                                           prefix='medias'),
            }

    # def form_valid(self, form):
    #     form.instance.author = Adv.objects.filter(author__user=self.request.user)
    #     return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = AdvForm()
    #     return context
    #
    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         author = form.save(commit=False)
    #         author.author = self.request.user
    #         author.save()
    #     return redirect('/')

    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     path = self.request.META['PATH_INFO']
    #     post = form.save()
        # send_post_for_subscribers_celery.delay(post.pk)
        # return super().form_valid(form)
