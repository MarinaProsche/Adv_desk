from django_filters import FilterSet, AllValuesFilter, CharFilter, ModelMultipleChoiceFilter, DateFilter, ModelChoiceFilter, DateRangeFilter, ChoiceFilter
from .models import Adv, Reply, CATEGORY_NAME
from django.forms import DateInput

class AdvFilter(FilterSet):
    text_adv = CharFilter(field_name='head_adv', lookup_expr='icontains', label='Поиск')
    category_name = ChoiceFilter(choices=CATEGORY_NAME, label = 'Выберите категорию', empty_label = 'все категории')


    TimeAdding = DateFilter(
        'date_adv',
        lookup_expr='gt',
        label='Опубликовано до',
        widget=DateInput(
            attrs={
                'type': 'date'
            }
        )
    )
