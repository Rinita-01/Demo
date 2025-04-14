from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from books.models import Book
from .models import Review

@login_required
def submit_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    existing_review = Review.objects.filter(user=request.user, book=book).first()

    if request.method == 'POST':
        if existing_review:
            return JsonResponse({'error': 'You have already reviewed this book.'}, status=400)

        rating_input = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()

        try:
            rating = int(rating_input)
            if rating < 1 or rating > 5:
                raise ValueError("Invalid rating")
        except (TypeError, ValueError):
            return JsonResponse({'error': 'Please select a valid rating between 1 and 5.'}, status=400)

        if not comment:
            return JsonResponse({'error': 'Comment cannot be empty.'}, status=400)

        review = Review.objects.create(
            user=request.user,
            book=book,
            rating=rating,
            comment=comment
        )

        return JsonResponse({
            'message': 'Review submitted successfully.',
            'review': {
                'username': request.user.username,
                'rating': review.rating,
                'comment': review.comment,
            }
        })

    return render(request, 'reviews/submit_review.html', {'book': book})