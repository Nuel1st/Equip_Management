from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Equipment, Surveyor, Equipment_Request
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def home(request):
    """Displays the application's homepage."""
    return render(request, 'Equipments/home.html')

# Form for Equipment Request
class EquipmentRequestForm(ModelForm):
    class Meta:
        model = Equipment_Request  # Ensure this matches your model
        fields = ['equipment']  # Do not include surveyor; it will be set automatically

# Equipment Request view
# @login_required  # Ensure user is logged in
def equipment_request(request):
    """Handles equipment request creation."""
    # try:
    #     surveyor = Surveyor.objects.get(user=request.user)  # Get the logged-in user's surveyor profile
    # except Surveyor.DoesNotExist:
    #     messages.error(request, 'You do not have an associated surveyor profile. Please contact support.')
    #     return redirect('home')
    surveyor = None  # Default to None if there's no user or no surveyor profile
    
    # Check if the user is authenticated and retrieve the Surveyor profile if it exists
    if request.user.is_authenticated:
        try:
            surveyor = Surveyor.objects.get(user=request.user)
        except Surveyor.DoesNotExist:
            pass  # No surveyor profile; surveyor remains None

        

    if request.method == 'POST':
        form = EquipmentRequestForm(request.POST)
        if form.is_valid():
            if surveyor:  # If a surveyor profile exists, associate it with the request
                form.instance.surveyor = surveyor
            equipment = form.cleaned_data['equipment']
            if equipment.status == 'In Store':
                form.save()
                equipment.status = 'In Field'
                equipment.save()
                return redirect('equipment_request')
            else:
                form.add_error('equipment', 'Equipment is already in the field canbot be request until returned')
    else:
        form = EquipmentRequestForm()

    # Pass only "In Store" equipment for dropdown filtering
    equipment_in_store = Equipment.objects.filter(status='In Store')
    return render(request, 'Equipments/equipment_request.html', {'form': form, 'equipment_in_store': equipment_in_store})

# Dynamic equipment dropdown
# @login_required
def get_equipment_dropdown(request):
    """Returns a filtered list of equipment for the dynamic dropdown."""
    equipment_type = request.GET.get('equipment_type', '')
    if equipment_type:  # Ensure equipment_type is not empty
        equipment = Equipment.objects.filter(equipment_type=equipment_type, status='In Store')
        equipment_list = [{'id': eq.id, 'name': eq.name} for eq in equipment]
    else:
        equipment_list = []

    return JsonResponse({'equipment': equipment_list})
