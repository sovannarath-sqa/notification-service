from django.core.management.base import BaseCommand
from credential.models.otaprofile import OTAProfile

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):

        OTAProfile.objects.create(name='Airbnb', logo = 'a', description='This is a description')
        OTAProfile.objects.create(name='Agoda', logo = 'a', description='This is another description')
        OTAProfile.objects.create(name='Boocking.com', logo = 'a', description='This is booking.com' )
        OTAProfile.objects.create(name='Rakuten', logo = 'b', description='This is Rakuten')

        self.stdout.write(self.style.SUCCESS('Database seeded successfully'))
