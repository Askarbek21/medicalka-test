import django_filters as filters 


class PostFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    content = filters.CharFilter(field_name='content', lookup_expr='icontains')
    created_at = filters.DateFromToRangeFilter(field_name='created_at')