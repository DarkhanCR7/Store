from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.urls import reverse
from .models import Product


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Введите вашу электронную почту')
    first_name = forms.CharField(max_length=30, required=False, help_text='Ваше имя')
    last_name = forms.CharField(max_length=150, required=False, help_text='Ваша фамилия')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user


def home(request):
    products = Product.objects.all()[:6]
    return render(request, 'products/home.html', {'products': products})


def product_list(request):
    q = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', '')
    products = Product.objects.all()
    if q:
        products = products.filter(name__icontains=q) | products.filter(description__icontains=q)
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    return render(request, 'products/list.html', {'products': products, 'q': q, 'sort': sort})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/detail.html', {'product': product})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('storeProducts:product_list'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'products/register.html', {'form': form})


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    cart[str(product.pk)] = cart.get(str(product.pk), 0) + 1
    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', reverse('storeProducts:product_list')))


def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    cart.pop(str(pk), None)
    request.session['cart'] = cart
    return redirect(reverse('storeProducts:view_cart'))


def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        try:
            p = Product.objects.get(pk=int(pid))
        except Product.DoesNotExist:
            continue
        subtotal = p.price * qty
        total += subtotal
        items.append({'product': p, 'qty': qty, 'subtotal': subtotal})
    return render(request, 'products/cart.html', {'items': items, 'total': total})


