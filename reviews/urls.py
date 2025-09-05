from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.BookListView.as_view(), name='book-list'),
    path('signup/', views.signup_view, name='signup'),

    # login/logout
    path('login/', auth_views.LoginView.as_view(template_name='reviews/registrations/login.html'), name='login'),
path('logout/', auth_views.LogoutView.as_view(next_page='book-list'), name='logout'),

    # book & review URLs
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('book/<int:pk>/review/add/', views.ReviewCreateView.as_view(), name='review-add'),
    path('review/<int:pk>/update/', views.ReviewUpdateView.as_view(), name='review-update'),
    path('review/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review-delete'),

    # user dashboard
    path('my-reviews/', views.user_reviews, name='user-reviews'),

    # search
    path('search/', views.search_books, name='search-books'),
]
