from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import RecommendationRequest, BookRecommendation
from .services import BookRecommendationService


def home(request):
    """Homepage with form to enter preferences."""
    # Get recent requests from session
    recent_requests = request.session.get('recent_requests', [])
    return render(request, 'recommendations/home.html', {'recent_requests': recent_requests})


def about(request):
    """About page explaining how BookClerk works."""
    # Get recent requests from session for the header menu
    recent_requests = request.session.get('recent_requests', [])
    return render(request, 'recommendations/about.html', {'recent_requests': recent_requests})


@require_http_methods(["POST"])
def get_recommendations(request):
    """Process user preferences and get book recommendations."""
    user_preferences = request.POST.get('preferences', '').strip()
    
    if not user_preferences:
        messages.error(request, 'Please enter your book preferences.')
        return redirect('home')
    
    try:
        # Create a new recommendation request
        req = RecommendationRequest.objects.create(user_preferences=user_preferences)
        
        # Get recommendations from OpenAI
        service = BookRecommendationService()
        recommendations = service.get_book_recommendations(user_preferences)
        
        # Save recommendations to database
        for rec_data in recommendations:
            title = rec_data.get('title', 'Unknown Title')
            author = rec_data.get('author', 'Unknown Author')
            
            # Generate Amazon affiliate link
            amazon_url = service.generate_amazon_affiliate_link(title, author)
            
            BookRecommendation.objects.create(
                request=req,
                title=title,
                author=author,
                description=rec_data.get('description', 'No description available.'),
                reason=rec_data.get('reason', 'No reason provided.'),
                amazon_url=amazon_url
            )
        
        # Add to session recent requests
        recent_requests = request.session.get('recent_requests', [])
        recent_requests.insert(0, {
            'id': req.id,
            'preferences': user_preferences,
            'created_at': req.created_at.isoformat()
        })
        # Keep only last 10
        request.session['recent_requests'] = recent_requests[:10]
        
        return redirect('view_recommendations', request_id=req.id)
        
    except Exception as e:
        messages.error(request, f'Error getting recommendations: {str(e)}')
        return redirect('home')


def view_recommendations(request, request_id):
    """Display recommendations for a specific request."""
    try:
        req = RecommendationRequest.objects.get(id=request_id)
        recommendations = req.recommendations.all()
        # Get recent requests from session for the hamburger menu
        recent_requests = request.session.get('recent_requests', [])
        return render(request, 'recommendations/recommendations.html', {
            'recommendation_request': req,
            'recommendations': recommendations,
            'recent_requests': recent_requests
        })
    except RecommendationRequest.DoesNotExist:
        messages.error(request, 'Recommendations not found.')
        return redirect('home')
