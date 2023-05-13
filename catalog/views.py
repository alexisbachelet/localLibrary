from django.shortcuts import render
from django.views import generic

# Create your views here.
from .models import Book, Author, BookInstance, Genre


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Variables that we can use later in the template.
    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "index.html", context=context)


class BookListView(generic.ListView):
    # 1) One line to list all the availaible books.
    model = Book
    paginate_by = 10  # Every 10 recors we create a new pages.

    # 2) But we can add some extra variable to custom the default behavior.
    # 2)a) The template variable name which contains all the books (list).
    # By default the name is "object_list" or "book_list".
    # context_object_name = "my_book_list"

    # 2)b) Filter the list instead of display all books.
    # queryset = Book.objects.filter(title__icontains="war")[:5]

    # 2)c) Specify the template to use. By default the path is:
    # /catalog/templates/catalog/book_list.html
    # For list view we need to create inside templates a second dir with the
    # same app's name.
    # template_name = "books/my_arbitrary_template_name_list.html"


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author
