from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext as _

class SiteLanguage(models.Model):
    language = models.CharField(max_length=2, choices=[('fr', 'French'), ('en', 'English')], default='fr')

    def __str__(self):
        return str(self.language)

class Frigo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients_dispo = models.ManyToManyField('Ingredients', verbose_name=_('ingredients_dispo'))

    def __str__(self):
        return str(self.id_frigo)

class Ingredients(models.Model):
    nom_ingredient = models.CharField(max_length=50, primary_key=True, verbose_name=_('Nom_ingrédient'))
    unite = models.CharField(max_length=50, verbose_name=_('Unité'))

    def __str__(self):
        return self.nom_ingredient

class RecetteIngredients(models.Model):
    nom_recette = models.ForeignKey("Recette", on_delete=models.CASCADE, verbose_name=_('Nom de la recette'))
    nom_ingredient = models.ForeignKey("Ingredients", on_delete=models.CASCADE, verbose_name=_('Ingredients'))

    def __str__(self):
        return f"{self.nom_recette} - {self.nom_ingredient}"

class Photo_plat(models.Model):
    id_photo = models.AutoField(max_length=100,primary_key=True)
    chemin_photo = models.ImageField(upload_to='media/photo_plat')
    id_service = models.ForeignKey('Service', on_delete=models.CASCADE)
    id_review = models.ForeignKey('Review', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_photo)

class Review(models.Model):
    nom_recette = models.ForeignKey('Recette', on_delete=models.CASCADE, verbose_name=_('Nom de la recette')) # J'ai retirer LE ManyToMany
    id_review = models.AutoField(max_length=100, primary_key=True, verbose_name=_('ID de la revue'))
    commentaire = models.CharField(max_length=200, verbose_name=_('Commentaire'))
    class Note(models.IntegerChoices):
        Zero = 0, '0'
        Un = 1, '1'
        Deux = 2, '2'
        Trois = 3, '3'
        Quatre = 4, '4'
        Cinq = 5, '5'

    note = models.IntegerField(choices=Note.choices, verbose_name=_('Note'))

    def __str__(self):
        return f"{self.id_review} - Note: {self.note}"

class Service(models.Model):
    id_service = models.AutoField(max_length=100, primary_key=True, verbose_name=_('ID du service'))
    nom_recette = models.ForeignKey('Recette', on_delete=models.CASCADE, related_name='service_recette', unique=True, verbose_name=_('Nom de la recette'))

    class ServiceType(models.TextChoices):
        ENTREE = 'Entrée', _('Entrée')
        PLAT = 'Plat', _('Plat')
        DESSERT = 'Dessert', _('Dessert')

    nom_service = models.CharField(max_length=10, choices=ServiceType.choices)

    class Origine(models.TextChoices):
        AFGHANISTAN = 'Afghanistan', _('Afghanistan')
        AFRIQUE_DU_SUD = 'Afrique du Sud', _('Afrique du Sud')
        ALGERIE = 'Algérie', _('Algérie')
        ALLEMAGNE = 'Allemagne', _('Allemagne')
        ANGLETERRE = 'Angleterre', _('Angleterre')
        ARGENTINE = 'Argentine', _('Argentine')
        AUSTRALIE = 'Australie', _('Australie')
        AUTRICHE = 'Autriche', _('Autriche')
        BELGIQUE = 'Belgique', _('Belgique')
        BRESIL = 'Brésil', _('Brésil')
        CANADA = 'Canada', _('Canada')
        CHILI = 'Chili', _('Chili')
        CHINE = 'Chine', _('Chine')
        COLOMBIE = 'Colombie', _('Colombie')
        COREE_DU_SUD = 'Corée du Sud', _('Corée du Sud')
        CUBA = 'Cuba', _('Cuba')
        DANEMARK = 'Danemark', _('Danemark')
        EGYPTE = 'Égypte', _('Égypte')
        ESPAGNE = 'Espagne', _('Espagne')
        ETATS_UNIS = 'États-Unis', _('États-Unis')
        FINLANDE = 'Finlande', _('Finlande')
        FRANCE = 'France', _('France')
        GRECE = 'Grèce', _('Grèce')
        HONGRIE = 'Hongrie', _('Hongrie')
        INDE = 'Inde', _('Inde')
        INDONESIE = 'Indonésie', _('Indonésie')
        IRAN = 'Iran', _('Iran')
        IRLANDE = 'Irlande', _('Irlande')
        ITALIE = 'Italie', _('Italie')
        JAPON = 'Japon', _('Japon')
        LIBAN = 'Liban', _('Liban')
        MALAISIE = 'Malaisie', _('Malaisie')
        MAROC = 'Maroc', _('Maroc')
        MEXIQUE = 'Mexique', _('Mexique')
        NORVEGE = 'Norvège', _('Norvège')
        PAYS_BAS = 'Pays-Bas', _('Pays-Bas')
        PEROU = 'Pérou', _('Pérou')
        POLOGNE = 'Pologne', _('Pologne')
        PORTUGAL = 'Portugal', _('Portugal')
        REPUBLIQUE_TCHEQUE = 'République Tchèque', _('République Tchèque')
        ROUMANIE = 'Roumanie', _('Roumanie')
        RUSSIE = 'Russie', _('Russie')
        SENEGAL = 'Sénégal', _('Sénégal')
        SUEDE = 'Suède', _('Suède')
        SUISSE = 'Suisse', _('Suisse')
        TUNISIE = 'Tunisie', _('Tunisie')
        TURQUIE = 'Turquie', _('Turquie')
        UKRAINE = 'Ukraine', _('Ukraine')
        VENEZUELA = 'Venezuela', _('Venezuela')
        VIETNAM = 'Vietnam', _('Vietnam')

    origine = models.CharField(max_length=20, choices=Origine.choices)

    def __str__(self):
        return f"{self.id_service} - {self.origine} - {self.nom_service}"

class Recette(models.Model):
    nom_recette = models.CharField(max_length=100, primary_key=True,  verbose_name=_('Nom de la recette'))
    nom_ingredient = models.ManyToManyField('Ingredients', verbose_name=_('Ingredients'))
    temps_preparation = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    temps_cuisson = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='photo_plat/')
    date_creation = models.DateTimeField(auto_now_add=True)
    texte_instruction = models.TextField()
    service = models.OneToOneField('Service', on_delete=models.CASCADE, related_name='recette', null=True, blank=True)

    def __str__(self):
        return self.nom_recette

