# Django Tutorial

## Initialisation

### Create Django Environment

Where you want.

```bash
python3 -V  # 3.8.10
sudo apt install python3-pip
python3 -m venv virtualenv
source virtualenv/bin/activate
pip install django~=4.0
python -m django --version
```

File tree

```markdown
./
├── catalog/
├── db.sqlite3
├── localLibrary/
├── manage.py*
└── tuto.md
```

Link the new app to the project

```python
# /localLibrary/settings.py
INSTALLED_APPS = [
    'catalog.apps.CatalogConfig'
]
```

```python
# /localLibrary/urls.py
utlpatterns = [
    path('admin/', admin.site.urls)
    path('catalog/', include('catalog.urls')),
    path('', RedirectView.as_view(url='catalog/')),
]
```

```python
# /catalog/urls.py
from django.urls import path
from . import views
urlpatterns = []
```

### Database Creation

If you are django expert, you can create files then modify and after apply them.

```bash
python manage.py makemigration  # Create.
python manage.py migrate  # Apply. 
```

```bash
python manage.py runserver
```

### Git Init

Create an empty repo on gitHub and folow their instructions:

```bash
git init
git add origin
git push -u orgin master  # Upstream branche.
```

### Private Key Generation

To quickly push on gitHub:

```bash
ssh-keygen -t rsa
cd .ssh/
eval "$(ssh-agent -s)"
ssh-add myPrivateKey
```

## Model

Model are the table in the Data Base

### Model Creation

```python
# /catalog/models.py
class Author(models.Model):
    """Model representing an author."""
    # If there is no primary key django creata automaticaly an id field.
    first_name = models.CharField(max_length=100)
    # blank = User can sent blank value.
    # null = Blank values are coverted to null.  
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['first_name', 'date_of_birth']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.first_name}'
```

### Create Record

```python
myRecord = myModel(myField='a')
myRecord.anotherField = 2
myRecord.save()
```

### Find a record

```python
allRecords = MyModel.objects.all()
myRecord = MyModel.objects.filter(title__contains='wild')  # "__" is like A dot.
aBook = MyBook.objects.filter(genre__name__contains='fiction')  # Foreign Key.
```

## Admin Site

Data Base managment like fuflfil it. To do it register our model in the admin section:

```python
# /catalog/admin.py
from .models import Author, Genre, Book, BookInstance, Language

# Define the admin class or use the default.
@admin.register(Book)
class AuthorAdmin(admin.ModelAdmin):
    # We can also add method to have special display with filter.
    list_display = ('last_name', 'first_name', ('date_of_birth', 'date_of_death'))  # Used parenhesis to have horozontaly display.
    #list_filter = ('status', 'due_back')

admin.site.register(Book)  # By default.
admin.site.register(Author, AuthorAdmin) 
```

```bash
python manage.py createsuperuser
```

go to `/admin` the page we can add book redirect to this urls: `admin/catalog/book/add/`

## Views

To use the database in your files.

### View Creation

```python
# /localLibrary/urls.py
# "Include" no nned of imports.
urlpatterns += [path('catalog/', include('catalog.urls')),]
```

```python
# /catalog/urls.py
import . import views  # Need an import because is not on strings.
urlpatterns += [
    path('', views.index, name="index"),  # Reverse = creta url from a name.
]
```

```python
# /catalog/urls.py
# Development only!
# Use static() to add URL mapping to serve static files (CSS, JS, images).
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

```python
# /catalog/views.py
from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
```

### Views are used by templates

Template are html file with blancks that the view function (DataBase extraction) fill it out.

By default Django search templates or static file (used by templates) on app directectory :

```python
TEMPLATES = [{
    "DIRS": [],
    "APP_DIRS": True,  # The options to seach the "templates/" dir on app dir.
}]
```

Even if django can search on these folder. We need to create it.

```bash
mkdir catalog/templates
mkdir catalog/static/css
```

We have :

+ Template Variables `{{ maVariable }}`
+ Template Tag (function) `{% uneFct  etSonParam %}`

```html
<!-- /catalog/templates/base_generic.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  {% block title %}<title>Local Library</title>{% endblock %}
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link 
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" 
    rel="stylesheet" 
    integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" 
    crossorigin="anonymous"
  >
  <!-- 
    Add additional CSS in static file.
    {% static 'endPath'}  will complete the end with the path's begigining.
    {% static 'css/styles.css'} become catalog/static/css/styles.css
    We need to load it before use it.
  -->
  {% load static %}
  <link rel="stylesheet" href="{% static 'css/styles.css' %}">
</head>

<!-- Because Boostrap work on a grid system we need to specify rows and cols -->
<!-- Blocks allow to replace generic file by mush more specific content -->
<body>
  <div class="container-fluid">  <!-- Always 100% of screen not by step -->
    <div class="row">
      <div class="col-sm-2">
      {% block sidebar %}
        <ul class="sidebar-nav">
          <li><a href="{% url 'index' %}">Home</a></li>  <!-- Reverse URL -->
          <li><a href="">All books</a></li>
          <li><a href="">All authors</a></li>
        </ul>
      {% endblock %}
      </div>
      <div class="col-sm-10 ">{% block content %}{% endblock %}</div>
    </div>
  </div>
</body>
</html>
```

```css
/* /catalog/static/css/styles.css */
.sidebar-nav {
  margin-top: 20px;
  padding: 0;
  list-style: none;
}
```

We have now the base for all html files but we need to extend the base to make specific html file:

```html
<!-- /catalog/templates/index.html -->
<!-- Take the full base html file and change only the block content by this -->
{% extends "base_generic.html" %}

{% block content %}
  <h1>Local Library Home</h1>
  <p>Welcome to LocalLibrary, a website developed by <em>Mozilla Developer Network</em>!</p>
  <h2>Dynamic content</h2>
  <p>The library has the following record counts:</p>
  <ul>
    <li><strong>Books:</strong> {{ num_books }}</li>
    <li><strong>Copies:</strong> {{ num_instances }}</li>
    <li><strong>Copies available:</strong> {{ num_instances_available }}</li>
    <li><strong>Authors:</strong> {{ num_authors }}</li>
  </ul>
{% endblock %}
```
