from .models import Category

# anything here will be available in all the templates
# should be added to the templates in the settings to works
def add_variable_to_context(request):
    return {
        'categories': Category.objects.all()
    }

