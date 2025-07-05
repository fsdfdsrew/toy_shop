from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Category(models.Model):
    name = models.CharField(_("Название"), max_length=100, unique=True)
    slug = models.SlugField(_("URL-адрес"), unique=True, max_length=100)
    description = models.TextField(_("Описание"), blank=True)
    image = models.ImageField(_("Изображение"), upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, 
                              related_name='children', verbose_name=_("Родительская категория"))
    is_active = models.BooleanField(_("Активна"), default=True)
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата обновления"), auto_now=True)

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

class Brand(models.Model):
    name = models.CharField(_("Название бренда"), max_length=100, unique=True)
    slug = models.SlugField(_("URL-адрес"), unique=True, max_length=100)
    country = models.CharField(_("Страна"), max_length=50, blank=True)
    description = models.TextField(_("Описание"), blank=True)
    logo = models.ImageField(_("Логотип"), upload_to='brands/', blank=True, null=True)
    website = models.URLField(_("Веб-сайт"), blank=True)
    is_active = models.BooleanField(_("Активен"), default=True)
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    class Meta:
        verbose_name = _("Бренд")
        verbose_name_plural = _("Бренды")
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('brand_detail', kwargs={'slug': self.slug})

class AgeGroup(models.Model):
    name = models.CharField(_("Название"), max_length=50, unique=True)
    min_age = models.PositiveIntegerField(_("Минимальный возраст"), validators=[MinValueValidator(0)])
    max_age = models.PositiveIntegerField(_("Максимальный возраст"), validators=[MaxValueValidator(18)])
    description = models.TextField(_("Описание"), blank=True)
    image = models.ImageField(_("Изображение"), upload_to='age_groups/', blank=True, null=True)
    is_active = models.BooleanField(_("Активна"), default=True)

    class Meta:
        verbose_name = _("Возрастная группа")
        verbose_name_plural = _("Возрастные группы")
        ordering = ['min_age']

    def __str__(self):
        return f"{self.name} ({self.min_age}-{self.max_age} лет)"

class Toy(models.Model):
    CONDITION_CHOICES = [
        ('new', _('Новый')),
        ('used', _('Б/у')),
        ('refurbished', _('Восстановленный')),
    ]

    GENDER_CHOICES = [
        ('unisex', _('Унисекс')),
        ('boys', _('Для мальчиков')),
        ('girls', _('Для девочек')),
    ]

    # Основная информация
    name = models.CharField(_("Название"), max_length=200)
    slug = models.SlugField(_("URL-адрес"), max_length=200, unique=True, blank=True)
    sku = models.CharField(_("Артикул"), max_length=50, unique=True, blank=True)
    
    # Связи с другими моделями
    category = models.ForeignKey(Category, verbose_name=_("Категория"), on_delete=models.CASCADE, related_name='toys')
    brand = models.ForeignKey(Brand, verbose_name=_("Бренд"), on_delete=models.SET_NULL, null=True, blank=True, related_name='toys')
    age_group = models.ForeignKey(AgeGroup, verbose_name=_("Возрастная группа"), on_delete=models.SET_NULL, null=True, related_name='toys')
    
    # Описание и характеристики
    description = models.TextField(_("Описание"))
    short_description = models.CharField(_("Краткое описание"), max_length=255, blank=True)
    specifications = models.JSONField(_("Характеристики"), default=dict, blank=True)
    
    # Цена и наличие
    price = models.DecimalField(_("Цена"), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    old_price = models.DecimalField(_("Старая цена"), max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(_("Количество на складе"), default=0)
    min_stock = models.PositiveIntegerField(_("Минимальный остаток"), default=0)
    
    # Статус и видимость
    is_active = models.BooleanField(_("Активен"), default=True)
    is_featured = models.BooleanField(_("Рекомендуемый"), default=False)
    is_bestseller = models.BooleanField(_("Бестселлер"), default=False)
    is_new = models.BooleanField(_("Новинка"), default=False)
    
    # Дополнительные характеристики
    condition = models.CharField(_("Состояние"), max_length=20, choices=CONDITION_CHOICES, default='new')
    gender = models.CharField(_("Пол"), max_length=10, choices=GENDER_CHOICES, default='unisex')
    weight = models.DecimalField(_("Вес (кг)"), max_digits=5, decimal_places=2, blank=True, null=True)
    dimensions = models.CharField(_("Размеры"), max_length=100, blank=True)
    
    # Изображения
    main_image = models.ImageField(_("Главное изображение"), upload_to='toys/main/')
    
    # Метаданные
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата обновления"), auto_now=True)
    views_count = models.PositiveIntegerField(_("Количество просмотров"), default=0)

    class Meta:
        verbose_name = _("Игрушка")
        verbose_name_plural = _("Игрушки")
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"TOY-{uuid.uuid4().hex[:8].upper()}"
        if not self.slug:
            self.slug = f"{self.name.lower().replace(' ', '-')}-{self.sku.lower()}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('toy_detail', kwargs={'slug': self.slug})

    @property
    def is_available(self):
        return self.is_active and self.stock > self.min_stock

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0

class ToyImage(models.Model):
    toy = models.ForeignKey(Toy, on_delete=models.CASCADE, related_name='images', verbose_name=_("Игрушка"))
    image = models.ImageField(_("Изображение"), upload_to='toys/gallery/')
    alt_text = models.CharField(_("Альтернативный текст"), max_length=200, blank=True)
    is_main = models.BooleanField(_("Главное изображение"), default=False)
    order = models.PositiveIntegerField(_("Порядок"), default=0)
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    class Meta:
        verbose_name = _("Изображение игрушки")
        verbose_name_plural = _("Изображения игрушек")
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Изображение {self.toy.name}"

class Review(models.Model):
    toy = models.ForeignKey(Toy, on_delete=models.CASCADE, related_name='reviews', verbose_name=_("Игрушка"))
    name = models.CharField(_("Имя"), max_length=100)
    email = models.EmailField(_("Email"))
    rating = models.PositiveIntegerField(_("Оценка"), choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(_("Комментарий"))
    is_approved = models.BooleanField(_("Одобрен"), default=False)
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.toy.name} ({self.rating}/5)"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Ожидает обработки')),
        ('processing', _('В обработке')),
        ('shipped', _('Отправлен')),
        ('delivered', _('Доставлен')),
        ('cancelled', _('Отменён')),
    ]

    order_number = models.CharField(_("Номер заказа"), max_length=20, unique=True)
    first_name = models.CharField(_("Имя"), max_length=100)
    last_name = models.CharField(_("Фамилия"), max_length=100)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Телефон"), max_length=20)
    address = models.TextField(_("Адрес доставки"))
    
    total_amount = models.DecimalField(_("Общая сумма"), max_digits=10, decimal_places=2)
    status = models.CharField(_("Статус"), max_length=20, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата обновления"), auto_now=True)

    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ {self.order_number} - {self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Генерируем номер заказа: ORD-YYYYMMDD-XXXX
            from datetime import datetime
            import random
            date_str = datetime.now().strftime('%Y%m%d')
            random_suffix = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            self.order_number = f"ORD-{date_str}-{random_suffix}"
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_("Заказ"))
    toy = models.ForeignKey(Toy, on_delete=models.CASCADE, verbose_name=_("Игрушка"))
    quantity = models.PositiveIntegerField(_("Количество"))
    price = models.DecimalField(_("Цена за единицу"), max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(_("Сумма"), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("Товар заказа")
        verbose_name_plural = _("Товары заказа")

    def __str__(self):
        return f"{self.toy.name} x{self.quantity} - {self.subtotal} ₽"

    def save(self, *args, **kwargs):
        if not self.subtotal:
            self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)