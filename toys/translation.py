from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Brand, Toy, AgeGroup


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


class BrandTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


class ToyTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'short_description')


class AgeGroupTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


# Регистрируем переводы
translator.register(Category, CategoryTranslationOptions)
translator.register(Brand, BrandTranslationOptions)
translator.register(Toy, ToyTranslationOptions)
translator.register(AgeGroup, AgeGroupTranslationOptions) 