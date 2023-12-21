from django.core.management.base import BaseCommand
from EasyCook.models import Ingredients
import random

class Command(BaseCommand):
    help = 'Ajoute automatiquement une liste d\'ingrédients à la base de données.'

    def handle(self, *args, **options):
        nom_ingredients = [
            'Ail', 'Amandes', 'Anchois', 'Aubergines', 'Aubergines grillées', 'Baileys', 'Basilic', 'Beurre',
            'Betteraves', 'Bières',
            'Brie', 'Boulgour', 'Brocoli', 'Bœuf', 'Cacao en poudre', 'Camembert', 'Canard', 'Cannelle', 'Carciofi',
            'Carottes', 'Caviar',
            'Cèpes', 'Champagne', 'Champignons', 'Chèvre', 'Chia', 'Chocolat au lait', 'Chocolat blanc',
            'Chocolat fondu', 'Chocolat noir', 'Ciboulette',
            'Cognac', 'Concombre', 'Coriandre', 'Coulis de tomate', 'Courgettes', 'Crème aigre', 'Crème de menthe',
            'Crème épaisse', 'Crème fraîche', 'Crevettes',
            'Cumin', 'Curaçao', 'Curry', 'Câpres', 'Côtes de porc', 'Cœur de palmier', 'Côtelettes d\'agneau',
            'Côtelettes de veau', 'Côtelettes de porc', 'Côtelettes de poulet',
            'Dinde', 'Emmental', 'Endives', 'Entrecôte', 'Escargots', 'Espadon', 'Essence de vanille',
            'Extrait d\'amande', 'Extrait de citron', 'Extrait de vanille', 'Farine',
            'Farro', 'Faux-filet', 'Feta', 'Fraises', 'Framboises', 'Fromage blanc', 'Fromage de chèvre',
            'Fromage de brebis', 'Fromage de vache', 'Fromage gorgonzola', 'Fromage mozzarella',
            'Fromage parmesan', 'Fromage roquefort', 'Fromage taleggio', 'Fromage à raclette', 'Fruits de la passion',
            'Galette de riz', 'Gambas', 'Gelée de groseille', 'Gingembre', 'Gouda',
            'Graisse de canard', 'Grand Marnier', 'Grenadine', 'Gruau', 'Graines de chia', 'Graines de courge',
            'Graines de lin', 'Graines de pavot', 'Graines de sésame', 'Graines de tournesol',
            'Gratin dauphinois', 'Grenouilles', 'Groseilles', 'Gruau d\'avoine', 'Gruau de sarrasin', 'Guacamole',
            'Haricots noirs', 'Haricots rouges', 'Haricots verts', 'Huile', 'Huile d\'olive',
            'Huîtres', 'Jambon de parme', 'Jus d\'orange', 'Ketchup', 'Kiwi', 'Kiwis', 'Lait', 'Laitue',
            'Lamelles de truffes', 'Lardons', 'Lasagnes', 'Laurier', 'Lemon curd', 'Lentilles',
            'Lingettes nettoyantes', 'Litchis', 'Malt', 'Mandarines', 'Mangue', 'Mascarpone', 'Mayonnaise', 'Menthe',
            'Miel', 'Millet', 'Mimolette', 'Miso', 'Moutarde', 'Mozzarella',
            'Mûres', 'Mûres blanches', 'Mûres rouges', 'Mûres sauvages', 'Noix', 'Noix de coco', 'Noix de muscade',
            'Noix de saint jacques', 'Noix du brésil', 'Noix de cajou', 'Nougat',
            'Nougatine', 'Nouilles de riz', 'Oignons', 'Olives', 'Olives noires', 'Olives vertes', 'Oranges', 'Origan',
            'Oseille', 'Ossobuco', 'Oursins', 'Oursins frais', 'Pain', 'Pain d\'épices',
            'Pain de mie', 'Pain de seigle', 'Pain de campagne', 'Pain complet', 'Pain intégral', 'Pain italien',
            'Pain multicéréales', 'Pain noir', 'Pain noir allemand', 'Pain norvégien', 'Pain pita',
            'Pain rassis', 'Pain sans gluten', 'Pain suédois', 'Pain à burger', 'Pain à la tomate', 'Pain à l\'ail',
            'Pain à l\'épeautre', 'Pain à la châtaigne', 'Pain à la semoule', 'Pain à la vanille',
            'Pain à l\'épeautre et aux noix', 'Pain à la farine d\'orge', 'Pain à la farine de châtaigne',
            'Pain à la farine de kamut', 'Pain à la farine de riz', 'Pain à la farine de seigle', 'Pain à la levure',
            'Pain à la levure chimique', 'Pain à la levure de boulanger', 'Pain à la levure de boulanger et au lait',
            'Pain à la levure de boulanger et à l\'eau', 'Pain à la levure et à la bière', 'Pain à la mie jaune',
            'Pain à la mie jaune et aux noix', 'Pain à la mie jaune et à la levure',
            'Pain à la mie jaune et à la levure de boulanger', 'Pain à la mie jaune et à la levure chimique',
            'Pain à la mie jaune et à la levure de bière',
            'Pain à la mie jaune et à la farine de riz', 'Pain à la mie jaune et à la farine de kamut',
            'Pain à la mie jaune et à la farine de blé', 'Pain à la mie jaune et à la farine de seigle',
            'Pain à la mie jaune et à la farine d\'orge',
            'Pain à la mie jaune et à la farine de châtaigne', 'Pain à la mie jaune et à la farine de maïs',
            'Pain à la mie jaune et à la farine de lin', 'Pain à la mie jaune et à la farine d\'avoine',

            # Ajoutez d'autres ingrédients selon vos besoins
        ]

        unites = ['g', 'kg', 'ml', 'cl', 'cuillère à soupe', 'cuillère à café', 'pincée']

        ingredients_data = [{'nom_ingredient': nom, 'unite': random.choice(unites)} for nom in nom_ingredients]

        for ingredient in ingredients_data:
            nom_ingredient = ingredient['nom_ingredient']
            unite = ingredient['unite']

            existing_ingredient = Ingredients.objects.filter(nom_ingredient=nom_ingredient).first()

            if not existing_ingredient:
                Ingredients.objects.create(nom_ingredient=nom_ingredient, unite=unite)
                self.stdout.write(self.style.SUCCESS(f'Ingrédient "{nom_ingredient}" ajouté avec succès.'))
            else:
                self.stdout.write(self.style.WARNING(f'Ingrédient "{nom_ingredient}" existe déjà dans la base de données.'))
