from django.shortcuts import render
from products.models import Product
from orders.models import Basket, Order
from blogs.models import Comment
from products.models import Photo
from .forms import CommitForm


def details_product(request, slug, order_id=None, active_fancy_tab_id=1):
    weight_or_pcs = None
    loop_times = None
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    if order_id:
        order_is = Order.objects.get(id=order_id, session_key=session_key)
        weight_or_pcs = order_is.weight_or_pcs
    global this_product
    this_product = Product.objects.get(slug_product__iexact=slug, is_active=True)
    details_photos = Photo.objects.filter(product_id=this_product.id, is_active=True, main_photo=True).order_by('dates_upload')
    count_of_photos = details_photos.count()
    comments = Comment.objects.filter(product_commit=this_product).order_by('dates_commit')
    basket_present = []
    category_for_back = this_product.category_plus_type_product.category.slug_category
    if this_product.average_rating:
        loop_times = range(0, this_product.average_rating)
    if request.user.is_active:
        basket_present = Basket.objects.filter(client=request.user.client, state_of_status='executed')
    return render(request, 'details_product/details_product.html', context={'details_photos': details_photos,
                                                                            'details': this_product,
                                                                            'count_of_photos': count_of_photos,
                                                                            'comments': comments,
                                                                            'loop_times': loop_times,
                                                                            'basket_present': basket_present,
                                                                            'weight_or_pcs': weight_or_pcs,
                                                                            'change_weight_or_pcs_order': order_id,
                                                                            'category_for_back': category_for_back,
                                                                            'active_fancy_tab_id': active_fancy_tab_id})


def send_commit(request):
    if request.method == 'POST':
        commit_form = CommitForm(request.POST or None)
        if commit_form.is_valid():
            r_commit = commit_form.cleaned_data['r_commit']
            rating = commit_form.cleaned_data['rating']
            client_commit = request.user.client
            new_commit = Comment(client_commit=client_commit, product_commit=this_product, r_commit=r_commit, rating=rating)
            new_commit.save()
    comments = Comment.objects.filter(product_commit=this_product).order_by('dates_commit')
    return render(request, 'list_of_comments/list_of_comments.html', context={'comments': comments})
