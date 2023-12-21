from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .forms import *
from django.http import Http404, HttpResponseForbidden
from EasyCook.models import *
from django.urls import reverse
from .forms import RecipeForm, InstructionsForm
from .models import Review
from .models import Recette
from django.contrib import messages
from .forms import LoginForm
import urllib
from django.conf import settings
import json
import urllib.parse
import urllib.request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import urllib.error
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext as _
from django.core.mail import EmailMessage
from django.utils.translation import activate
from .models import SiteLanguage


@login_required(login_url='EasyCook:Login')
def switch_language(request, language_code):
    # Assurez-vous que la langue est valide
    if language_code in ['fr', 'en']:
        # Enregistrez ou mettez à jour la langue pour l'ensemble de l'application
        site_language, created = SiteLanguage.objects.get_or_create(pk=1)
        site_language.language = language_code
        site_language.save()

        # Activez la langue pour la session actuelle
        activate(language_code)

    # Redirigez l'utilisateur vers la page précédente
    return redirect(request.META.get('HTTP_REFERER', 'EasyCook:Accueil'))


def Accueil(request):
    all_recipes = Recette.objects.all()

    for recipe in all_recipes:
        reviews = Review.objects.filter(nom_recette=recipe)
        if reviews.exists():
            moyenne_notes = sum(review.note for review in reviews) / len(reviews)
            recipe.popularite = round(moyenne_notes)
        else:
            recipe.popularite = 0

    popular_recipes = sorted(all_recipes, key=lambda x: x.popularite, reverse=True)[:5]
    context = {'popular_recipes': popular_recipes}
    return render(request, 'EasyCook/Accueil.html', context)

def Login(request):
    if request.user.is_authenticated:
        messages.success(request, _('Vous êtes déjà connecté.'))
        return redirect('EasyCook:Accueil')

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response', None)

            if not recaptcha_response:
                messages.error(request, _('Veuillez remplir le captcha.'))
                return render(request, 'EasyCook/Login.html', {'form': form})

            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue sur EasyCook, {user.username}.')
                return redirect('EasyCook:Accueil')

            else:
                messages.error(request, _('Identifiant ou mot de passe incorrect.'))

    return render(request, 'EasyCook/Login.html', {'form': form})

def Register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('EasyCook:Accueil')

    return render(request, 'EasyCook/Register.html', context={'form': form})

@login_required(login_url = '/EasyCook/Login')
def Logout(request):
    logout(request)
    messages.success(request, _('Vous avez été déconnecté avec succès.'))
    return redirect('EasyCook:Accueil')

def Recipes(request):
    recipes = Recette.objects.all().order_by('nom_recette')
    page = request.GET.get('page',1)
    paginator= Paginator (recipes, 10)

    try:
        recipes = paginator.page(page)
    except PageNotAnInteger:
        recipes = paginator.page(1)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)

    return render(request, 'EasyCook/Recipes.html', {'recipes': recipes })

def generatePdf(request, nom_recette):
    recette = Recette.objects.get(pk=nom_recette)
    ingredients = recette.nom_ingredient.all()
    texte_instruction = recette.texte_instruction
    origine = recette.service.origine if recette.service else None
    nom_service = recette.service.nom_service if recette.service else None

    context = {'Descr_recipe': recette,'Ingredients': ingredients,'texte_instruction': texte_instruction,'Service': nom_service,'Origine': origine}

    template_path = 'EasyCook/generatePdf.html'
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='EasyCook/pdf')
    response['Content-Disposition'] = f'filename="{recette.nom_recette}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error while creating PDF: %s' % pisa_status.err, status=500)

    return response

@login_required(login_url='EasyCook:Login')
def send_email_with_pdf(request, nom_recette):
    recette = Recette.objects.get(pk=nom_recette)

    pdf_response = generatePdf(request, nom_recette)
    pdf_data = pdf_response.content

    subject = f"Recette: {recette.nom_recette}"
    message = "Veuillez trouver ci-joint le fichier PDF de la recette."
    from_email = "EasyCookforuser@gmail.com"

    to_email = request.user.email

    email = EmailMessage(subject, message, from_email, [to_email])
    email.attach(f"{recette.nom_recette}.pdf", pdf_data, 'EasyCook/pdf')
    email.send()

    return HttpResponse("Email sent successfully.")

@login_required(login_url='EasyCook:Login')
def Evaluations_recipe(request, nom_recette):
    recette = get_object_or_404(Recette, nom_recette=nom_recette)

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.nom_recette = recette
            review.username = request.user
            review.save()

            nom_recette = recette.nom_recette

            url = reverse('EasyCook:Descr_recipe', kwargs={'nom_recette': nom_recette})
            return redirect(url)

    else:
        form = ReviewForm()

    evaluations = Review.objects.filter(nom_recette=recette)
    return render(request, 'EasyCook/Evaluations_recipe.html', {'form': form, 'evaluations': evaluations})

def Descr_recipe(request, nom_recette):
    try:
        recipe = get_object_or_404(Recette, nom_recette=nom_recette)
        ingredients = recipe.nom_ingredient.all()
        reviews = Review.objects.filter(nom_recette=recipe)
        texte_instruction = recipe.texte_instruction
        origine = recipe.service.origine if recipe.service else None
        nom_service = recipe.service.nom_service if recipe.service else None

    except Recette.DoesNotExist:
        raise Http404(_("Cette recette n'existe pas"))

    except Recette.DoesNotExist:
        raise Http404(_("Cette recette n'existe pas"))

    if reviews.exists():
        moyenne_notes = sum(review.note for review in reviews) / len(reviews)
        recipe.popularite = round(moyenne_notes)
        moyenne_notes = round(moyenne_notes, 2)
    else:
        recipe.popularite = 0
        moyenne_notes = 0

    context = {'Descr_recipe': recipe, 'Evaluation': reviews, 'moyenne_notes': moyenne_notes,
               'Ingredients': ingredients, 'texte_instruction': texte_instruction, 'Service': nom_service, 'Origine': origine}
    return render(request, 'EasyCook/Descr_recipe.html', context)

def Popular_recipe(request):
    all_recipes = Recette.objects.all()

    for recipe in all_recipes:
        reviews = Review.objects.filter(nom_recette=recipe)
        if reviews.exists():
            moyenne_notes = sum(review.note for review in reviews) / len(reviews)
            recipe.popularite = round(moyenne_notes)
        else:
            recipe.popularite = 0

    popular_recipes = sorted(all_recipes, key=lambda x: x.popularite, reverse=True)[:5]

    form = PopularRecipeFilterForm(request.GET)
    origine = form.cleaned_data['origine'] if form.is_valid() else 'all'
    nom_service = form.cleaned_data['nom_service'] if form.is_valid() else 'all'

    if origine == 'all' and nom_service == 'all':
        filtered_recipes = popular_recipes
    else:
        filtered_recipes = []
        for recipe in popular_recipes:
            if (
                (origine == 'all' or (recipe.service and recipe.service.origine == origine))
                and
                (nom_service == 'all' or (recipe.service and recipe.service.nom_service == nom_service))
            ):
                filtered_recipes.append(recipe)

    page = request.GET.get('page', 1)
    paginator = Paginator(filtered_recipes, 10)

    try:
        filtered_recipes = paginator.page(page)
    except PageNotAnInteger:
        filtered_recipes = paginator.page(1)
    except EmptyPage:
        filtered_recipes = paginator.page(paginator.num_pages)

    context = {'popular_recipes': filtered_recipes, 'form': form}
    return render(request, 'EasyCook/Popular_recipe.html', context)

@login_required(login_url='EasyCook:Login')
def Fridge(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to access this page.")

    frigo, created = Frigo.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = FrigoForm(request.POST, instance=frigo)
        if form.is_valid():
            ingredients_selected = form.cleaned_data.get('ingredients_dispo')
            frigo.ingredients_dispo.clear()

            request.session['selected_ingredients'] = [ingredient.nom_ingredient for ingredient in ingredients_selected]

            return redirect('EasyCook:SearchRecipes')

    else:
        form = FrigoForm(instance=frigo)
        print("Form errors:", form.errors)
    return render(request, 'EasyCook/Fridge.html', {'form': form})

def SearchRecipes(request):
    selected_ingredients = request.session.get('selected_ingredients', [])
    recipes = Recette.objects.filter(nom_ingredient__in=selected_ingredients).distinct()

    page = request.GET.get('page', 1)
    paginator = Paginator(recipes, 10)  # 10 recettes par page

    try:
        recipes = paginator.page(page)
    except PageNotAnInteger:
        recipes = paginator.page(1)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)

    return render(request, 'EasyCook/SearchRecipes.html', {'recipes': recipes})

@login_required(login_url='EasyCook:Login')
def Share_recipe_step1(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        form2 = RecipeForm2(request.POST)

        if form.is_valid() and form2.is_valid():
            recipe = form.save(commit=False)

            recipe.user = request.user
            recipe.save()

            ingredients_selected = form.cleaned_data['nom_ingredient']
            recipe.nom_ingredient.set(ingredients_selected)

            origine = form2.cleaned_data['origine']
            service = form2.cleaned_data['nom_service']

            service_recipe = Service.objects.create(nom_recette=recipe, origine=origine, nom_service=service)
            service_recipe.save()
            recipe.service = service_recipe
            recipe.save()
            request.session['nom_recette'] = recipe.nom_recette

            return redirect('EasyCook:Share_recipe_step2')

    else:
        form = RecipeForm()
        form2 = RecipeForm2()

    return render(request, 'EasyCook/Share_recipe_step1.html', {'form': form, 'form2': form2})

def Share_recipe_step2(request):
    nom_recette = request.session.get('nom_recette', None)

    if nom_recette is None:
        messages.error(request, _('Erreur lors de la récupération de la recette.'))
        return redirect('EasyCook:Accueil')

    recette_instance = get_object_or_404(Recette, nom_recette=nom_recette)

    form = InstructionsForm(request.POST, request.FILES, initial={'nom_recette': recette_instance.nom_recette})

    if request.method == 'POST':
        print(f"POST data: {request.POST}")
        if form.is_valid():

            messages.success(request, _('Recette partagée avec succès!'))
            return redirect('EasyCook:Recipes')

    return render(request, 'EasyCook/Share_recipe_step2.html', {'instructions_form': form})

def Error404(request, exception):
    return render(request, 'Accueil/404.html', status=400)

def Error500(request, *args, **argv):
    return render(request, 'Accueil/500.html', status=500)

def à_Propos(request):
    return render(request, "EasyCook/a_Propos.html")
