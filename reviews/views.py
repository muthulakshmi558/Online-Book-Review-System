from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm

from .models import Book, Review
from .forms import ReviewForm, BookSearchForm

# ----------------------------
# Home / Book List
# ----------------------------
class BookListView(ListView):
    model = Book
    template_name = 'reviews/home.html'
    context_object_name = 'books'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_range'] = range(1, 6)  # 1 to 5 stars
        return context


# ----------------------------
# Book Detail & Reviews
# ----------------------------
class BookDetailView(DetailView):
    model = Book
    template_name = 'reviews/book_detail.html'
    context_object_name = 'book'


# ----------------------------
# Add Review
# ----------------------------
class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def form_valid(self, form):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        form.instance.book = book
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Review added successfully!")

        # Email notification to user
        send_mail(
            'New Review Added',
            f'Your review for "{book.title}" has been posted successfully!',
            settings.DEFAULT_FROM_EMAIL,
            [self.request.user.email],
            fail_silently=True
        )
        return response

    def get_success_url(self):
        return reverse_lazy('book-detail', kwargs={'pk': self.object.book.pk})


# ----------------------------
# Edit Review
# ----------------------------
class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user or self.request.user.is_staff

    def get_success_url(self):
        messages.success(self.request, "Review updated successfully!")
        return self.object.book.get_absolute_url()


# ----------------------------
# Delete Review
# ----------------------------
class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user or self.request.user.is_staff

    def get_success_url(self):
        messages.success(self.request, "Review deleted successfully!")
        return reverse_lazy('book-list')


# ----------------------------
# User Reviews Dashboard
# ----------------------------
@login_required
def user_reviews(request):
    reviews = request.user.review_set.all()
    return render(request, 'reviews/user_reviews.html', {'reviews': reviews})


# ----------------------------
# Search Page (optional, if separate from home)
# ----------------------------
def search_books(request):
    form = BookSearchForm(request.GET)
    books = Book.objects.none()
    if form.is_valid():
        query = form.cleaned_data['query']
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    return render(request, 'reviews/search_results.html', {'books': books, 'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please login.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'reviews/registrations/signup.html', {'form': form})