from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter, DateRangeFilter
from .models import Adv, Reply
from django.forms import DateInput

class AdvFilter(FilterSet):
    Tag = ModelMultipleChoiceFilter(
        field_name = 'category',
        queryset = Adv.objects.all().values('category_name'),
        label = 'выберите категорию',
        conjoined = False,
    )

    TimeAdding = DateFilter(
        'date_adv',
        lookup_expr='gt',
        label='опубликовано до',
        widget=DateInput(
            attrs={
                'type': 'date'
            }
        )
    )

    class Meta:
        model = Adv
        fields = {
           'head_adv': ['icontains'],
        }


class UserAdvFilter(FilterSet):
    date_replay = DateRangeFilter()

    def __init__(self, *args, **kwargs):
        super(UserAdvFilter, self).__init__(*args, **kwargs)
        self.filters['text_reply'].queryset = Adv.objects.filter(author_id=kwargs['request'])

    class Meta:
        model = Reply
        fields = ('text_reply', 'date_replay',)