import django_filters
from e_commerce.models import Product


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {'name': ['contains', ],
                  'category': ['exact', ]}
