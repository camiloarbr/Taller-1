from django.shortcuts import render
from .models import News

# Create your views here.
def news(request):
    news = News.objects.all().order_by('-date_added')
    return render(request, 'news/news.html', {'news': news})


