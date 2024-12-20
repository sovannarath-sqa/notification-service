from django.core.management.base import BaseCommand
from credential.models.propertyprofile import PropertyProfile

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):

        PropertyProfile.objects.create(
            name = 'Minn 蒲田 Kamata',
            suitebook_id = 1128,
            aos_slug = 'minn_kamata',
            aos_organization_name = 'SQUEEZE Inc.',
            aos_organization_slug = 'squeeze',
            logo = 'a'
        )

        PropertyProfile.objects.create(
            name = 'シアテル羽田Ⅱ HanedaⅡ',
            suitebook_id = 1769,
            aos_slug = 'theatel_haneda_2',
            aos_organization_name = 'SQUEEZE Inc.',
            aos_organization_slug = 'squeeze'
        )

        PropertyProfile.objects.create(
            name= 'シアテル羽田 Haneda Airport',
            suitebook_id= 641,
            aos_slug= 'theatel_haneda',
            aos_organization_name= 'SQUEEZE Inc.',
            aos_organization_slug= 'squeeze',
        )

        PropertyProfile.objects.create(
            name= 'Minn 上野 Ueno',
            suitebook_id = 1239,
            aos_slug= 'minn_ueno',
            aos_organization_name= 'SQUEEZE Inc.',
            aos_organization_slug= 'squeeze',
        )
        

        self.stdout.write(self.style.SUCCESS('Database seeded successfully'))
