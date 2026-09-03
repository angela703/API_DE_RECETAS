from django.shortcuts import render


def home(request):
	return render(request, 'api_recetas/home.html')


def page_not_found(request, exception):
	return render(request, 'api_recetas/404.html', status=404)
