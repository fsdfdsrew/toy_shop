# Generated by Django 5.1.6 on 2025-06-23 22:03

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgeGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название')),
                ('min_age', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Минимальный возраст')),
                ('max_age', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(18)], verbose_name='Максимальный возраст')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
            ],
            options={
                'verbose_name': 'Возрастная группа',
                'verbose_name_plural': 'Возрастные группы',
                'ordering': ['min_age'],
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название бренда')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL-адрес')),
                ('country', models.CharField(blank=True, max_length=50, verbose_name='Страна')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='brands/', verbose_name='Логотип')),
                ('website', models.URLField(blank=True, verbose_name='Веб-сайт')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL-адрес')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories/', verbose_name='Изображение')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='toys.category', verbose_name='Родительская категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Toy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True, verbose_name='URL-адрес')),
                ('sku', models.CharField(blank=True, max_length=50, unique=True, verbose_name='Артикул')),
                ('description', models.TextField(verbose_name='Описание')),
                ('short_description', models.CharField(blank=True, max_length=255, verbose_name='Краткое описание')),
                ('specifications', models.JSONField(blank=True, default=dict, verbose_name='Характеристики')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена')),
                ('old_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Старая цена')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='Количество на складе')),
                ('min_stock', models.PositiveIntegerField(default=0, verbose_name='Минимальный остаток')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Рекомендуемый')),
                ('is_bestseller', models.BooleanField(default=False, verbose_name='Бестселлер')),
                ('is_new', models.BooleanField(default=False, verbose_name='Новинка')),
                ('condition', models.CharField(choices=[('new', 'Новый'), ('used', 'Б/у'), ('refurbished', 'Восстановленный')], default='new', max_length=20, verbose_name='Состояние')),
                ('gender', models.CharField(choices=[('unisex', 'Унисекс'), ('boys', 'Для мальчиков'), ('girls', 'Для девочек')], default='unisex', max_length=10, verbose_name='Пол')),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Вес (кг)')),
                ('dimensions', models.CharField(blank=True, max_length=100, verbose_name='Размеры')),
                ('main_image', models.ImageField(upload_to='toys/main/', verbose_name='Главное изображение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('views_count', models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')),
                ('age_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='toys', to='toys.agegroup', verbose_name='Возрастная группа')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='toys', to='toys.brand', verbose_name='Бренд')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='toys', to='toys.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Игрушка',
                'verbose_name_plural': 'Игрушки',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('rating', models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Оценка')),
                ('comment', models.TextField(verbose_name='Комментарий')),
                ('is_approved', models.BooleanField(default=False, verbose_name='Одобрен')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('toy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='toys.toy', verbose_name='Игрушка')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ToyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='toys/gallery/', verbose_name='Изображение')),
                ('alt_text', models.CharField(blank=True, max_length=200, verbose_name='Альтернативный текст')),
                ('is_main', models.BooleanField(default=False, verbose_name='Главное изображение')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('toy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='toys.toy', verbose_name='Игрушка')),
            ],
            options={
                'verbose_name': 'Изображение игрушки',
                'verbose_name_plural': 'Изображения игрушек',
                'ordering': ['order', 'created_at'],
            },
        ),
    ]
