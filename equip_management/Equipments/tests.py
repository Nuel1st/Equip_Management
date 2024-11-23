from django.test import TestCase

# Create your tests here.
from .models import Equipment, Surveyor, EquipmentRequest

class EquipmentRequestTestCase(TestCase):

    def setUp(self):
        self.surveyor = Surveyor.objects.create(first_name='John', last_name='Doe')
        self.equipment = Equipment.objects.create(name='GNSS-100', equipment_type='GNSS', status='In Store')

    def test_request_equipment(self):
        response = self.client.post('/equipment_request/', {
            'surveyor': self.surveyor.id,
            'equipment': self.equipment.id,
        })
        self.assertEqual(response.status_code, 302)
        self.equipment.refresh_from_db()
        self.assertEqual(self.equipment.status, 'In Field')

    def test_request_equipment_already_in_field(self):
        self.equipment.status = 'In Field'
        self.equipment.save()
        response = self.client.post('/equipment_request/', {
            'surveyor': self.surveyor.id,
            'equipment': self.equipment.id,
        })
        self.assertFormError(response, 'form', 'equipment', 'Equipment is already in the field')
