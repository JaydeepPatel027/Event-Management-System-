from django.core.management.base import BaseCommand
from event_management_application.models import EventService, ServiceOption

class Command(BaseCommand):
    help = 'Copy ServiceOption rows to all EventService rows with the same service_name'

    def handle(self, *args, **kwargs):
        # Get all unique service names
        all_service_names = EventService.objects.values_list('service_name', flat=True).distinct()

        for service_name in all_service_names:
            # Get all EventService rows for this service
            service_rows = EventService.objects.filter(service_name=service_name)

            # Get options from the first occurrence that has options
            first_service_with_options = service_rows.filter(options__isnull=False).first()
            if not first_service_with_options:
                continue  # No options exist for this service anywhere

            options_to_copy = ServiceOption.objects.filter(service=first_service_with_options)

            # Copy options to other EventService rows if missing
            for service_row in service_rows:
                existing_options = ServiceOption.objects.filter(service=service_row).values_list('option_name', flat=True)
                for opt in options_to_copy:
                    if opt.option_name not in existing_options:
                        ServiceOption.objects.create(
                            service=service_row,
                            option_name=opt.option_name,
                            price=opt.price,
                            photo_url=opt.photo_url
                        )

        self.stdout.write(self.style.SUCCESS('✅ All options copied for shared services across events.'))
