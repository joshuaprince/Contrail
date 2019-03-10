from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PriceView(TemplateView):
    template_name = "price.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CompareView(TemplateView):
    template_name = "compare.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
