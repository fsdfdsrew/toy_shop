from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Category, Toy, Brand, ToyImage, Review, AgeGroup, Order, OrderItem
import random
from django.core.paginator import Paginator
from django.db.models import Q, Case, When, IntegerField
from django.contrib import messages
from .forms import ReviewForm
from .tasks import send_order_confirmation_email

# Create your views here.

def get_cart_count(request):
    """Подсчитывает общее количество товаров в корзине"""
    cart = request.session.get('cart', {})
    return sum(cart.values()) if cart else 0

def home(request):
    categories_all = list(Category.objects.filter(parent__isnull=True, is_active=True))
    categories = random.sample(categories_all, min(4, len(categories_all))) if categories_all else []
    toys = list(Toy.objects.filter(is_active=True))
    random_toys = random.sample(toys, min(3, len(toys))) if toys else []
    brands = Brand.objects.filter(is_active=True)
    return render(request, 'toys/home.html', {
        'categories': categories,
        'random_toys': random_toys,
        'brands': brands,
        'cart_count': get_cart_count(request),
    })

def toy_detail(request, slug):
    toy = get_object_or_404(Toy, slug=slug, is_active=True)
    images = toy.images.all()
    reviews = toy.reviews.filter(is_approved=True)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.toy = toy
            review.is_approved = False  # Модерация
            review.save()
            messages.success(request, 'Ваш отзыв отправлен и появится после модерации!')
            return redirect(request.path)
    return render(request, 'toys/toy_detail.html', {
        'toy': toy,
        'images': images,
        'reviews': reviews,
        'form': form,
        'cart_count': get_cart_count(request),
    })

def shop(request):
    # Фильтры
    age_id = request.GET.get('age')
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')
    search = request.GET.get('q')

    toys = Toy.objects.filter(is_active=True)

    if age_id:
        toys = toys.filter(age_group_id=age_id)
    if category_id:
        # Получаем выбранную категорию и все её подкатегории
        selected_category = Category.objects.filter(id=category_id).first()
        if selected_category:
            subcategories = Category.objects.filter(Q(parent=selected_category) | Q(id=selected_category.id)).values_list('id', flat=True)
            toys = toys.filter(category_id__in=subcategories)
        else:
            toys = toys.filter(category_id=category_id)
    if brand_id:
        toys = toys.filter(brand_id=brand_id)
    if search:
        toys = toys.filter(Q(name__icontains=search) | Q(description__icontains=search))

    # Сортировка: сначала товары в наличии, потом по приоритету, и наконец товары с нулевым остатком
    toys = toys.annotate(
        priority=Case(
            When(stock=0, then=5),  # Товары с нулевым остатком в конце
            When(is_featured=True, then=1),  # Рекомендуемые
            When(is_bestseller=True, then=2),  # Бестселлеры  
            When(is_new=True, then=3),  # Новинки
            default=4,  # Обычные товары
            output_field=IntegerField(),
        )
    ).order_by('priority', '-created_at')

    # Пагинация
    paginator = Paginator(toys, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    age_groups = AgeGroup.objects.filter(is_active=True).order_by('min_age')
    categories = Category.objects.filter(parent__isnull=True, is_active=True)
    brands = Brand.objects.filter(is_active=True)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'toys/_shop_products.html', {
            'page_obj': page_obj,
            'selected_age': age_id,
            'selected_category': category_id,
            'selected_brand': brand_id,
            'search': search,
        })
    return render(request, 'toys/shop.html', {
        'age_groups': age_groups,
        'categories': categories,
        'brands': brands,
        'page_obj': page_obj,
        'selected_age': age_id,
        'selected_category': category_id,
        'selected_brand': brand_id,
        'search': search,
        'cart_count': get_cart_count(request),
    })

def cart_detail(request):
    cart = request.session.get('cart', {})
    toys = Toy.objects.filter(id__in=cart.keys())
    cart_items = []
    total = 0
    for toy in toys:
        qty = cart[str(toy.id)]
        subtotal = toy.price * qty
        cart_items.append({'toy': toy, 'qty': qty, 'subtotal': subtotal})
        total += subtotal
    return render(request, 'toys/cart.html', {
        'cart_items': cart_items, 
        'total': total,
        'cart_count': get_cart_count(request),
    })

def cart_add(request, toy_id):
    cart = request.session.get('cart', {})
    toy_id = str(toy_id)
    qty = int(request.POST.get('qty', 1))
    cart[toy_id] = cart.get(toy_id, 0) + qty
    request.session['cart'] = cart
    
    # Если это AJAX запрос, возвращаем JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': get_cart_count(request),
            'message': 'Товар добавлен в корзину'
        })
    
    # Обычный запрос - редирект
    return redirect(request.POST.get('next', 'cart_detail'))

def cart_remove(request, toy_id):
    cart = request.session.get('cart', {})
    toy_id = str(toy_id)
    if toy_id in cart:
        del cart[toy_id]
        request.session['cart'] = cart
    return redirect('cart_detail')

def cart_decrease(request, toy_id):
    cart = request.session.get('cart', {})
    toy_id = str(toy_id)
    if toy_id in cart:
        if cart[toy_id] > 1:
            cart[toy_id] -= 1
        else:
            del cart[toy_id]  # Если количество станет 0, удаляем товар
        request.session['cart'] = cart
    return redirect('cart_detail')

def cart_clear(request):
    request.session['cart'] = {}
    return redirect('cart_detail')

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Ваша корзина пуста.')
        return redirect('cart_detail')
    
    toys = Toy.objects.filter(id__in=cart.keys())
    cart_items = []
    total = 0
    
    for toy in toys:
        qty = cart[str(toy.id)]
        subtotal = toy.price * qty
        cart_items.append({'toy': toy, 'qty': qty, 'subtotal': subtotal})
        total += subtotal
    
    if request.method == 'POST':
        # Создаём заказ
        order = Order.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            total_amount=total
        )
        
        # Создаём товары заказа
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                toy=item['toy'],
                quantity=item['qty'],
                price=item['toy'].price,
                subtotal=item['subtotal']
            )
        
        # Очищаем корзину
        request.session['cart'] = {}
        
        # Отправляем письмо пользователю
        send_order_confirmation_email.delay(order.id)
        
        return redirect('order_success', order_number=order.order_number)
    
    return render(request, 'toys/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'cart_count': get_cart_count(request),
    })

def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    print(f"DEBUG: Order object: {order}")
    print(f"DEBUG: Order fields:")
    print(f"  - order_number: {order.order_number}")
    print(f"  - first_name: {order.first_name}")
    print(f"  - last_name: {order.last_name}")
    print(f"  - email: {order.email}")
    print(f"  - phone: {order.phone}")
    print(f"  - address: {order.address}")
    print(f"  - total_amount: {order.total_amount}")
    print(f"  - total_amount type: {type(order.total_amount)}")
    return render(request, 'toys/order_success.html', {
        'order': order,
        'cart_count': get_cart_count(request),
    })
