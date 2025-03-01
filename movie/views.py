from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64

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
