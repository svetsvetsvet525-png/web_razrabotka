from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'slug', 'brand', 'price', 'old_price',
            'sku', 'stock', 'image', 'short_description', 'description',
            'specs', 'rating', 'review_count', 'is_active',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'specs': forms.Textarea(attrs={'rows': 6}),
            'name': forms.TextInput(attrs={'placeholder': 'Механическая клавиатура K55 Pro'}),
            'image': forms.TextInput(attrs={'placeholder': '/static/img/k55-main.webp'}),
            'slug': forms.TextInput(attrs={'placeholder': 'оставьте пустым — заполнится само'}),
        }
        labels = {
            'slug': 'URL (пусто = сгенерируется из названия)',
        }