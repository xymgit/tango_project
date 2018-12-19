from django.http import HttpResponse
from django.shortcuts import render

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

# Create your views here.


def index(request):
    # return HttpResponse("Rango says hey there partner!<br/> <a href='/rango/about/'>About</a>")

    # context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    # return render(request, 'rango/index.html', context=context_dict)

    Category_list = Category.objects.order_by('-likes')[:5]
    Page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': Category_list, 'pages': Page_list}
    return render(request, 'rango/index.html', context_dict)


def about(request):
    # To complete the exercise in chapter 4, we need to remove the following line
    # return HttpResponse("Rango says here is the about page.<br/> <a href='/rango/'>View index page</a>")
    # and replace it with a pointer to ther about.html template using the render method
    return render(request, 'rango/about.html', {})


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one models instanse or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        # Retrive all of the associated pages.
        # Note that filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)

        # Add our results list to the template context under name pages.
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form:
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved
            # We could give a confirmation message
            # But since the most recent category added is on the index age
            # Then we can direct the user back to the index page.
            return index(request)
        else:
            # The supplied form contained errors -
            # Just print them to the terminal.
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    
    context_dict = {'form':form, 'category':category}
    return render(request, 'rango/add_page.html', context_dict)
