from django.db import models
from django.contrib.auth.models import User

class Equipment(models.Model):
    EQUIPMENT_TYPES = [
        ('GNSS', 'GNSS'),
        ('Total Station', 'Total Station'),
        ('Level Instrument', 'Level Instrument'),
        ('Drone', 'Drone'),
    ]

    STATUS_CHOICES = [
        ('In Store', 'In Store'),
        ('In Field', 'In Field'),
    ]

    name = models.CharField(max_length=30)
    equipment_type = models.CharField(max_length=30, choices=EQUIPMENT_TYPES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='In Store')

    def __str__(self):
        return f"{self.name} ({self.status})"

class Surveyor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=80)

    def __str__(self):
        return self.user.username

class Equipment_Request(models.Model):  # Class name should use PascalCase (e.g., EquipmentRequest)
    surveyor = models.ForeignKey(Surveyor, on_delete=models.CASCADE, null=True, blank=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now_add=True)
    # returned_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[('Requested', 'Requested'), ('In Field', 'In Field')],
        default='Requested'
    )

    def __str__(self):
        return f"Request by {self.surveyor} for {self.equipment}"
