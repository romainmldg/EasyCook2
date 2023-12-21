from django.urls import path
from . import views


app_name = 'EasyCook'
urlpatterns = [

    path('Login/', views.Login, name='Login'),
    path('Register/', views.Register, name='Register'),
    path('Logout/', views.Logout, name='Logout'),
    path('Accueil/', views.Accueil,name = 'Accueil'),
    path('Recipes/', views.Recipes,name = 'Recipes'),
    path('Evaluations_recipe/<str:nom_recette>/', views.Evaluations_recipe, name='Evaluations_recipe'),
    path('Descr_recipe/<str:nom_recette>/', views.Descr_recipe, name='Descr_recipe'),
    path('Fridge/', views.Fridge,name = 'Fridge'),
    path('Share_recipe/step1/', views.Share_recipe_step1, name='Share_recipe_step1'),
    path('Share_recipe/step2/', views.Share_recipe_step2, name='Share_recipe_step2'),
    path('Popular_recipe/', views.Popular_recipe,name = 'Popular_recipe'),
    path('recette/<str:nom_recette>/pdf/', views.generatePdf, name='generate_pdf'),
    path('Error404/', views.Error404, name='404'),
    path('Error500/', views.Error500, name='500'),
    path('à_Propos/', views.à_Propos, name='à_Propos'),
    path('SearchRecipes/', views.SearchRecipes, name='SearchRecipes'),
    path('send_email_with_pdf/<str:nom_recette>/', views.send_email_with_pdf, name='send_email_with_pdf'),
    path('switch_language/<str:language_code>/', views.switch_language, name='switch_language')
]