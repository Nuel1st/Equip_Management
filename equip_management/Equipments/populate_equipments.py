from django.core.management.base import BaseCommand
from your_app.models import Equipment

class Command(BaseCommand):
    help = "Populate Equipment table"

    def handle(self, *args, **kwargs):
        equipment_list = [
            {"name": "GNSS Receiver 1", "equipment_type": "GNSS", "status": "In Store"},
            {"name": "Drone Model X", "equipment_type": "Drone", "status": "In Store"},
            {"name": "Level Instrument Pro", "equipment_type": "Level Instrument", "status": "In Store"},
            {"name": "Total Station TS3", "equipment_type": "Total Station", "status": "In Store"},
        ]

        for equipment in equipment_list:
            Equipment.objects.get_or_create(
                name=equipment["name"],
                equipment_type=equipment["equipment_type"],
                status=equipment["status"],
            )
        self.stdout.write(self.style.SUCCESS("Equipment added successfully!"))
