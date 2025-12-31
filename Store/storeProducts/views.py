from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django import forms
from django.urls import reverse
from .models import Product, UserProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Введите вашу электронную почту')
    first_name = forms.CharField(max_length=30, required=False, help_text='Ваше имя')
    last_name = forms.CharField(max_length=150, required=False, help_text='Ваша фамилия')
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text="Минимум 8 символов"
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        help_text="Введите пароль ещё раз"
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Это имя пользователя уже занято')
        return username
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
            # Создаем профиль пользователя
            UserProfile.objects.get_or_create(user=user)
        return user


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label='Имя')
    last_name = forms.CharField(max_length=150, required=False, label='Фамилия')
    email = forms.EmailField(required=False, label='Email')
    
    class Meta:
        model = UserProfile
        fields = ('avatar', 'bio')
        labels = {
            'avatar': 'Аватар',
            'bio': 'Биография'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        profile = super().save(commit=commit)
        if profile.user:
            profile.user.first_name = self.cleaned_data.get('first_name', '')
            profile.user.last_name = self.cleaned_data.get('last_name', '')
            profile.user.email = self.cleaned_data.get('email', '')
            profile.user.save()
        return profile


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
    
    # Пагинация: 12 товаров на странице
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products/list.html', {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'q': q,
        'sort': sort,
        'paginator': paginator
    })


def product_list_second(request):
    """Второй каталог товаров"""
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
    
    # Пагинация: 9 товаров на странице
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products/second.html', {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'q': q,
        'sort': sort,
        'paginator': paginator
    })


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
            # Форма остаётся на странице с ошибками
            return render(request, 'products/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'products/register.html', {'form': form})


@login_required(login_url='login')
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('storeProducts:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'products/profile.html', {'form': form, 'profile': profile})


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


