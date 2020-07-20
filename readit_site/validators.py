import re
from .models import SubreaditModel

PATTERN = re.compile('[!@#$%^&*(),.?":{}|<> ]')

def validate_subreadit(form):
    name = form.cleaned_data['name']
    query = SubreaditModel.objects.filter(name=name)
    if query.exists():
        return "Subreadit already exists"
    elif len(re.split(PATTERN, name)) > 1:
        return "No special charecters or whitespace in name"
    else:
        return True 
    