import django_filters
from django_filters import DateFilter, CharFilter
from .models import Expert, Office

class ExpertFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name="timestamp", lookup_expr='gte')
    # end_date = DateFilter(field_name="timestamp", lookup_expr='lte')
    # note = CharFilter(field_name='note', lookup_expr='icontains')

    class Meta:
        model = Expert
        fields = ['practices', 'city', 'country']
        # fields = '__all__'