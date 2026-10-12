from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify

from .models import Product
from .forms import ProductForm


def main_func(request):
    return render(request, template_name='main.html')


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]
    return render(request, 'product.html', {'product': product, 'related': related})


def manager_panel(request):
    edit_id = request.GET.get('edit')
    product = Product.objects.filter(pk=edit_id).first() if edit_id else None

    if request.method == 'POST':
        if 'delete_id' in request.POST:
            Product.objects.filter(pk=request.POST['delete_id']).delete()
            return redirect('manager_panel')

        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            obj = form.save(commit=False)
            if not obj.slug:
                base = slugify(obj.name, allow_unicode=True) or 'product'
                candidate, i = base, 1
                while Product.objects.filter(slug=candidate).exclude(pk=obj.pk).exists():
                    i += 1
                    candidate = f'{base}-{i}'
                obj.slug = candidate
            obj.save()
            return redirect('product_detail', slug=obj.slug)
    else:
        form = ProductForm(instance=product)

    return render(request, 'manager.html', {
        'form': form,
        'products': Product.objects.all(),
        'editing': product,
    })