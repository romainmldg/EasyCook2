from django import forms
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django_recaptcha.fields import ReCaptchaField


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField()

class RecipeForm(forms.ModelForm):
    nom_ingredient = forms.ModelMultipleChoiceField(
        queryset=Ingredients.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Recette
        fields = ['nom_recette', 'temps_preparation', 'temps_cuisson', 'nom_ingredient', 'image', 'texte_instruction']

class RecipeForm2(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['origine', 'nom_service']
        origine = forms.ChoiceField(choices=Service.Origine.choices, widget=forms.Select)
        nom_service = forms.ChoiceField(choices=Service.ServiceType.choices, widget=forms.Select)

class InstructionsForm(forms.ModelForm):
    class Meta:
        model = Recette
        fields = []

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['commentaire', 'note']
        note = forms.ChoiceField(choices=Review.Note.choices, widget=forms.RadioSelect)

class FrigoForm(forms.ModelForm):
    class Meta:
        model = Frigo
        fields = ['ingredients_dispo']
        widgets = {'ingredients_dispo': forms.CheckboxSelectMultiple}

class PopularRecipeFilterForm(forms.Form):
    origine = forms.ChoiceField(
        choices=[('all', 'Choisir l\'origine')] + list(Service.Origine.choices),
        required=False
    )

    nom_service = forms.ChoiceField(
        choices=[('all', 'Choisir le type de recette')] + list(Service.ServiceType.choices),
        required=False
    )