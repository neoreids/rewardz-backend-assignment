from django_filters import FilterSet, filters

from library.models import Books


class ListBookFilter(FilterSet):
    title = filters.CharFilter(field_name="title", method='search')
    author = filters.CharFilter(field_name="author", method='search')

    class Meta:
        model = Books
        fields = ["title", "author"]

    def search(self, queryset, field, value):
        lookup = "%s__icontains" % field
        return queryset.filter(**{lookup: value})
