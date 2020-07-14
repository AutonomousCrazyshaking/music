from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage

class cPaginator(Paginator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def page(self, number):
        try:
            pages = super().page(number)
        except PageNotAnInteger:
            pages = super().page(1)
        except EmptyPage:
            pages = super().page(super().num_pages)
        return pages