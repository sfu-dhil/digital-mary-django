from functools import reduce
from operator import or_

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormMixin, ModelFormMixin
from django.db.models import F, Q
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.contrib import messages

from .models import Item
from .forms import ItemSearchForm
from digital_mary_challenges.forms import ChallengeForm

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_search_form'] = ItemSearchForm()
        return context

class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'label': 'About', 'url': reverse('about')},
        ]
        return context

class ItemsView(ListView):
    paginate_by = 24
    model = Item
    template_name = 'items.html'
    ordering = ['earliest_creation', 'latest_creation', 'name']

    def get_queryset(self):
        queryset = super().get_queryset() \
            .filter(is_public=True) \
            .prefetch_related('images', 'remote_images')

        form = ItemSearchForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data

            if data.get('q'):
                query = reduce(or_, [SearchQuery(data.get('q'), config=language, search_type='websearch') for language in ['english', 'arabic']])
                queryset = queryset \
                    .filter(search_vector=query) \
                    .annotate(rank=SearchRank(F('search_vector'), query) * 100) \
                    .order_by('-rank', *self.get_ordering())

            if data.get('category'):
                queryset = queryset.filter(categories=data.get('category'))
            if data.get('culture'):
                queryset = queryset.filter(cultures=data.get('culture'))
            if data.get('inscription_style'):
                queryset = queryset.filter(inscription_style=data.get('inscription_style'))
            if data.get('language'):
                queryset = queryset.filter(languages=data.get('language'))
            if data.get('location'):
                queryset = queryset.filter(Q(findspot=data.get('location')) | Q(provenance=data.get('location')) | Q(provenience=data.get('location')))
            if data.get('technique'):
                queryset = queryset.filter(techniques=data.get('technique'))
            if data.get('period'):
                queryset = queryset.filter(
                    (Q(earliest_creation__lte=data.get('period')) | Q(earliest_creation__isnull=True)) &
                    (Q(latest_creation__gte=data.get('period')) | Q(latest_creation__isnull=True)) &
                    ~(Q(earliest_creation__isnull=True) | Q(latest_creation__isnull=True))
                )
            if data.get('material'):
                queryset = queryset.filter(materials=data.get('material'))
            if data.get('subject'):
                queryset = queryset.filter(subjects=data.get('subject'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'label': 'Items', 'url': reverse('items')},
        ]
        context['item_search_form'] = ItemSearchForm(self.request.GET)
        return context


class ItemView(FormMixin, DetailView):
    model = Item
    template_name = 'item.html'
    form_class = ChallengeForm

    def get_queryset(self):
        return super().get_queryset() \
            .filter(is_public=True) \
            .prefetch_related('images', 'remote_images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'label': 'Items', 'url': reverse('items')},
            {'label': self.object.name, 'url': reverse('item', kwargs={'pk': self.object.pk})},
        ]
        return context

    def get_success_url(self):
        return reverse('item', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.item = self.get_object()
            challenge.save()
            messages.success(request, f'Challenge successfully sent.')
            if len(settings.EMAIL_CHALLENGE_RECIPIENTS) > 0:
                for email_recipient in settings.EMAIL_CHALLENGE_RECIPIENTS:
                    send_mail(
                        subject=f'Digital Mary Challenge for: {self.object.name}',
                        message=render_to_string(
                            'emails/new_challenge.html',
                            request=request,
                            context={'object': challenge, 'site': get_current_site(request)}
                        ),
                        from_email=None,
                        recipient_list=[email_recipient],
                    )
            return self.form_valid(form)
        else:
            messages.error(request, 'Please correct the challenge errors below.')
            return self.form_invalid(form)
