# Django Tutorial

## Initialtion

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
    path('catalog/', include('catalog.urls'))
    path('', include('catalog.urls'))
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

## Data Base

### Model Creation

```python
# /locallibrary/catalog/
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
