from django.core.management.base import BaseCommand
from wagtail.models import Site, Page
from home.models import HomePage


class Command(BaseCommand):
    help = 'Set up the initial HomePage for the site'

    def handle(self, *args, **options):
        # Get the existing root page created by Wagtail
        try:
            root = Page.objects.get(depth=1)
        except Page.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Root page not found. Run migrations first.')
            )
            return

        # Check if HomePage already exists
        if HomePage.objects.filter(slug='home').exists():
            home_page = HomePage.objects.get(slug='home')
            self.stdout.write(
                self.style.WARNING('HomePage already exists')
            )
        else:
            # Create HomePage as a child of root
            home_page = HomePage(
                title='Amazon Manager',
                slug='home',
                body='<p>Welcome to Amazon Manager - your comprehensive solution for managing Amazon operations.</p>'
            )
            root.add_child(instance=home_page)
            self.stdout.write(
                self.style.SUCCESS('HomePage created successfully')
            )

        # Set up the site to point to our HomePage
        try:
            site = Site.objects.get(is_default_site=True)
            site.root_page = home_page
            site.save()
            self.stdout.write(
                self.style.SUCCESS('Site updated to use HomePage as root')
            )
        except Site.DoesNotExist:
            site = Site.objects.create(
                hostname='localhost',
                port=8000,
                site_name='Amazon Manager',
                root_page=home_page,
                is_default_site=True
            )
            self.stdout.write(
                self.style.SUCCESS('Site created successfully')
            )

        self.stdout.write(
            self.style.SUCCESS('Site setup completed successfully')
        )