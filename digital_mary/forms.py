from django import forms
from django_select2.forms import Select2Widget

from .models import Category, Culture, InscriptionStyle, Language, \
    Location, Technique, Item, Material, Subject

class ItemSearchForm(forms.Form):
    q = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'search',
            'placeholder': 'Search...',
            'class': 'form-control',
        }),
        required=False,
    )
    category = forms.ModelChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
            'data-placeholder': 'Category',
        }),
        queryset=Category.objects.order_by('label').all(),
        required=False,
    )
    culture = forms.ModelChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
            'data-placeholder': 'Culture',
        }),
        queryset=Culture.objects.order_by('label').all(),
        required=False,
    )
    inscription_style = forms.ModelChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
            'data-placeholder': 'Inscription style',
        }),
        queryset=InscriptionStyle.objects.order_by('label').all(),
        required=False,
    )
    language = forms.ModelChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
            'data-placeholder': 'Language',
        }),
        queryset=Language.objects.order_by('label').all(),
        required=False,
    )
    technique = forms.ModelChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
            'data-placeholder': 'Technique',
        }),
        queryset=Technique.objects.order_by('label').all(),
        required=False,
    )
    period = forms.ChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
            'data-placeholder': 'Period',
        }),
        choices=Item.Periods,
        required=False,
    )
    material = forms.ModelChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
            'data-placeholder': 'Material',
        }),
        queryset=Material.objects.order_by('label').all(),
        required=False,
    )
    subject = forms.ModelChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
            'data-placeholder': 'Subject',
        }),
        queryset=Subject.objects.order_by('label').all(),
        required=False,
    )
    location = forms.ModelChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
            'data-placeholder': 'Location',
        }),
        queryset=Location.objects.order_by('label').all(),
        required=False,
    )