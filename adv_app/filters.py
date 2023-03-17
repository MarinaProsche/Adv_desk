from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter
from .models import Adv
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