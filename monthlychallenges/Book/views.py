# views.py
from django.urls import reverse_lazy
#from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required
#from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from .models import Book

class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'author', 'published_date', 'isbn_number']
    template_name = 'Book/book_form.html'
    success_url = reverse_lazy('book_list')
    
#@login_required
class BookListView(ListView):
    model = Book
    template_name = 'templates/Book/book_list.html'
    
class BookUpdateView(UpdateView):
    model = Book
    fields = ['title', 'author', 'published_date', 'isbn_number']
    template_name = 'Book/book_form.html'
    success_url = reverse_lazy('book_list')
    
class BookDeleteView(DeleteView):
    model = Book
    template_name = 'Book/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')