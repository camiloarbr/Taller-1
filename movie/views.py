from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
from collections import Counter

def home(request):
    search_term = request.GET.get('searchMovie')
    movies = Movie.objects.filter(title__icontains=search_term) if search_term else Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': search_term, 'movies': movies})

def about(request):
    return render(request, 'about.html')

def statistics_view(request):
    # Get all movies
    all_movies = Movie.objects.all()
    
    # Create a dictionary to store the count of movies by year
    movie_counts_by_year = {}
    
    # Filter movies by year and count the number of movies per year
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        movie_counts_by_year[year] = movie_counts_by_year.get(year, 0) + 1
    
    # Bar width
    bar_width = 0.5
    # Bar positions
    bar_positions = range(len(movie_counts_by_year))
    
    # Create the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    
    # Customize the chart
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    
    # Adjust spacing between bars
    plt.subplots_adjust(bottom=0.3)
    
    # Save the chart to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    # Convert the chart to base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')
    
    # Render the statistics.html template with the chart
    return render(request, 'statistics.html', {'graphic': graphic})

def genre_statistics_view(request):
    # Get all movies
    all_movies = Movie.objects.all()
    
    # Count movies by genre
    genre_counts = Counter()
    for movie in all_movies:
        # Get the first genre (before any comma if multiple genres)
        genre = movie.genre.split(',')[0].strip() if movie.genre else 'Unspecified'
        genre_counts[genre] += 1
    
    # Sort genres by count in descending order
    sorted_genres = dict(sorted(genre_counts.items(), key=lambda x: x[1], reverse=True))
    
    # Create the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(sorted_genres)), sorted_genres.values(), align='center')
    
    # Customize the chart
    plt.title('Movies by Genre', fontsize=14, pad=20)
    plt.xlabel('Genre', fontsize=12)
    plt.ylabel('Number of Movies', fontsize=12)
    plt.xticks(range(len(sorted_genres)), sorted_genres.keys(), rotation=45, ha='right')
    
    # Add value labels on top of each bar
    for i, v in enumerate(sorted_genres.values()):
        plt.text(i, v, str(v), ha='center', va='bottom')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the chart to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    plt.close()
    
    # Convert the chart to base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')
    
    # Render the genre_statistics.html template with the chart
    return render(request, 'genre_statistics.html', {
        'graphic': graphic,
        'genre_data': sorted_genres
    })
