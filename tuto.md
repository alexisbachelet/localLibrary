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

The admin site is for data base managment (like fuflfil it).
To do it we need to register our model in the admin section:

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

Go to the `/admin` page

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

### Views used templates

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
  <p>Welcome to LocalLie
  brary, a website developed by <em>Mozilla Developer Network</em>!</p>
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

## Class of views

The concept is to create views (function and object) from a class.
So we can loop on all DataBase elements in a much more generic ways.
No need to create 200 views, just one class to get the data of one primary keys.

### List page: list all records

To gets the list of all recods in a model. The URL is: `catalog/books`
We used `as_view()` to transform a class to a views.

```python
# /catalog/urls.py
urlpatterns = [
    path('books/', views.BookListView.as_view(), name='books'),
]
```

```python
# /catalof/views.py
from django.views import generic

class BookListView(generic.ListView):
    # 1) One line to list all the availaible books.
    model = Book

    # OPTIONAL!
    # 2) But we can add some extra variable to custom the default behavior.
    # 2)a) The template variable name which contains all the books (list).
    # By default the name is "object_list" or "book_list".
    #context_object_name = 'my_book_list'

    # 2)b) Filter the list instead of display all books.
    #queryset = Book.objects.filter(title__icontains='war')[:5]
    
    # 2)c) Specify the template to use. By default the path is: 
    # /catalog/templates/catalog/book_list.html
    # For list view we need to create inside templates a second dir with the
    # same app's name.
    #template_name = 'books/my_arbitrary_template_name_list.html'
```

The views need to use one template:

```html
<!-- /catalog/templates/catalog/book_list.html -->
{% extends "base_generic.html" %}

{% block content %}
  <h1>Book List</h1>
  {% if book_list %}  <!-- Test if book_list is not empty -->
  <ul>
    {% for book in book_list %}
      <li>
        <!-- The book URL -->
        <a href="{{ book.get_absolute_url }}">{{ book.title }}</a> ({{book.author}})
      </li>
    {% endfor %}
  </ul>
  {% else %}
    <p>There are no books in the library.</p>
  {% endif %}
{% endblock %}
```

Reminders:

```python
def get_absolute_url(self):
  """Returns the URL to access a detail record for this book."""
  # Reverse an url mapper : create an url from a book id.
  # Normally we get an URL an we extract the book id from it.
  # book-detail is the name of a URL.
  return reverse("book-detail", args=[str(self.id)])
```

### Detail page: all fields

To get all informations of one record in model (SQL Table) : `catalog/book/<id>`

```python
# /catalog/urls.py
# Primary Key field with is type
urlpatterns = [
  path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
],
```

Optional: We can also use regex instead:

```python
# we can optionaly use regex:
re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
# () to capture the partern and give the value to the view.
    # (?P<name>...) capture the patern and give a named value to the view.
```

Optional: We can also use extra parameters in a view with a dictionary:

```python
path('myurl/<str:fish>', views.my_view, {'myVar': 'aValue'}, name='name')
```

So `myurl/halibut` point to the view:
`views.my_view(request, fish=halibut, myVar='aValue')`

```python
# /catalog/views.py
class BookDetailView(generic.DetailView):
    model = Book
```

```html
<!-- /catalog/templates/catalog/book_detail.html -->
{% extends "base_generic.html" %}

{% block content %}
  <h1>Title: {{ book.title }}</h1>

  <p>
    <strong>Author:</strong>
    <!-- 
      Reverse the author-detail url which is use a id 
      So we need to give an id to correctly reverse the id
    -->
    <a href="{% url 'author-detail' book.author.pk %}">{{ book.author }}</a>
    <!-- 
    If we want we can also to this manualy with: 
     <a href="{{ book.author.get_absolute_url }}">{{ book.author }}</a>
    -->
  </p> 
  
  <p><strong>Summary:</strong> {{ book.summary }}</p>
  <p><strong>ISBN:</strong> {{ book.isbn }}</p>
  <p><strong>Language:</strong> {{ book.language }}</p>
  <!-- We pipe function with "|" and give parameters with ":" -->
  <!-- join(book.genre.all, ", ") -->
  <p><strong>Genre:</strong> {{ book.genre.all|join:", " }}</p>

  <div style="margin-left:20px;margin-top:20px">
    <h4>Copies</h4>

    <!-- We loop on each instances of this books -->
    <!-- We can have several copy of the same book -->
    <!-- 
      Because it's one to many relatchiship Djando created
      a special function thar return all the instances linked to the book.
      We use "_set()" because it's a set of values.
    -->
    <!-- We use all() but we can filter(title__contains='wild') also -->
    {% for copy in book.bookinstance_set.all %}
      <hr>  <!-- Horizontal Rules -->
      <p class="{% if copy.status == 'a' %}text-success{% elif copy.status == 'm' %}text-danger{% else %}text-warning{% endif %}">
        <!-- 
          Status is a choice field.
          So it's not directly in the table there is an external table.
          We cant directly access to the value.
          We need to use the django magic with "get_" and "_display".
        -->
        {{ copy.get_status_display }}
      </p>
      {% if copy.status != 'a' %}
        <p><strong>Due to be returned:</strong> {{ copy.due_back }}</p>
      {% endif %}
      <p><strong>Imprint:</strong> {{ copy.imprint }}</p>
      <p class="text-muted"><strong>Id:</strong> {{ copy.id }}</p>
    {% endfor %}
  </div>
{% endblock %}
```

### Pagination

We can enabled pagination with:

```python
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
```

So every 10 records (books) we create an another page `/catalog/books/?page=2`

But it's much more conveniant to access it with arrows on the bottom of the page:

```html
<!-- /catalog/templates/base_generic.html -->
{% block pagination %}
{% if is_paginated %}
<div class="pagination">
  <span class="page-links">

    {% if page_obj.has_previous %}
    <a href="{{ request.path }}?page={{ page_obj.previous_page_number }}">previous</a>
    {% endif %}

    <span class="page-current">
      Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
    </span>

    {% if page_obj.has_next %}
    <a href="{{ request.path }}?page={{ page_obj.next_page_number }}">next</a>
    {% endif %}

  </span>
</div>
{% endif %}
{% endblock %}
```
