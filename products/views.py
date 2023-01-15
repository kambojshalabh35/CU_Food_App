from queue import Empty
from django.shortcuts import redirect, render

from adminAndSellers.models import Seller
from .models import Product, Order
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from slugify import slugify

# Create your views here.
def home(request):
    topproducts=Product.objects.order_by('noofsales').reverse()[:5]
    featuredproducts=Product.objects.order_by('noofsales').reverse()[5:10]
    favproducts=Product.objects.order_by('noofsales').reverse()[10:15]
    
    return render(request, 'home.html', {"featuredproducts":featuredproducts, "topproducts":topproducts, "favproducts":favproducts})

def seller_product(request, slug):
    products=Product.objects.filter(seller_linked_user=slug)
    sellers=Product.objects.filter(seller_linked_user=slug)[0:1]
    
    seller="False"
    if(sellers):
        seller=sellers[0].seller

    return render(request, 'seller.html', {"products":products, "seller":seller})

def your_products(request):
    seller=request.user.seller
    products=Product.objects.filter(seller=seller)
    if(products.exists()):
        return render(request, 'yourproducts.html',{"products":products,"noproducts":"false"})
    else:
        return render(request, 'yourproducts.html',{"noproducts":"true"})

def order_info(request, orderID):
    info=Order.objects.get(orderNumber=orderID)
    if(request.user.seller==info.seller):
        cinfo=User.objects.get(username=info.customer)
        product=Product.objects.get(slug=info.slug)
        return render(request, 'order-info.html', {'orderinfo':info, "customerinfo":cinfo, "product":product})
    else:
        return redirect('/page-not-found')

def add_product(request):
    if (request.method=='POST'):
        title=request.POST['title']
        description=request.POST['description']
        price=request.POST['price']
        image=request.FILES['image']
        seller=request.user.seller
        seller_linked_user = request.user.seller.user_linked
        slug=slugify(str(seller.shop_name)+" "+str(title))
        fs = FileSystemStorage()
        img = fs.save("uploads/"+str(image.name), image)

        Product.objects.create(seller=seller, seller_linked_user= seller_linked_user, title=title, slug=slug, description=description, price=price,image=img)

        return redirect('/your-products')

    else:
        return render(request, 'add-product.html')
    
def buy_product(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'buy-product.html', {"product":product})

def edit_product(request, slug):
    product = Product.objects.get(slug=slug)
    if(request.method=='POST'):
        title=request.POST['title']
        description=request.POST['description']
        price=request.POST['price']
        seller=request.user.seller
        slug=slugify(str(seller.shop_name)+" "+str(title))
        changeimg = request.POST['changeimg']

        if(changeimg=="true"):
            fs = FileSystemStorage()
            fs.delete(str(product.image))

            image=request.FILES['image']
            fs = FileSystemStorage()
            img = fs.save("uploads/"+str(image.name), image)

            product.title=title
            product.slug=slug
            product.description=description
            product.price=price
            product.image=img
            product.save()
            return redirect('/your-products')
        
        else:
            product.title=title
            product.slug=slug
            product.description=description
            product.price=price
            product.save()
            return redirect('/your-products')

    else:
        return render(request, 'edit-product.html', {"product":product})

def order_product(request, slug):
    product = Product.objects.get(slug=slug)
    if(request.user.is_authenticated):
        if(request.method=='POST'):
            order_type = request.POST['ordertype']
            if(order_type=="True"):
                block = request.POST['block']
                landmark = request.POST['landmark']
                seller = product.seller
                customer = request.user
                title = product.title
                quantity = request.POST['quantity']
                contactNumber = request.POST['contactnumber']
                price = product.price
                order = Order.objects.create(seller=seller, customer=customer, slug=slug, title=title, quantity=quantity, contactNumber=contactNumber, price=price, order_type=order_type, image=product.image.url, block=block, landmark=landmark)
                ordernumber = order.orderNumber
                return redirect("/order-success/"+str(ordernumber)+"/delivery")

            else:
                block = "None"
                landmark = "None"
                seller = product.seller
                customer = request.user
                title = product.title
                quantity = request.POST['quantity']
                contactNumber = request.POST['contactnumber']
                price = product.price
                order = Order.objects.create(seller=seller, customer=customer, slug=slug, title=title, quantity=quantity, contactNumber=contactNumber, price=price, order_type=order_type, image=product.image.url, block=block, landmark=landmark, delivery_status="pending")
                ordernumber = order.orderNumber
                return redirect("/order-success/"+str(ordernumber)+"/dining")

        else:
            return render(request, 'place-order.html', {"product":product})
    else:
        return redirect('/login')

def mark_as_delivered(request, slug):
    order = Order.objects.get(orderNumber=slug)
    pslug=order.slug
    product=Product.objects.get(slug=pslug)
    quantity=order.quantity

    nosales = product.noofsales
    product.noofsales = nosales + quantity
    product.save()

    order.delivery_status = "delivered"
    order.save()
    return redirect('/seller-orders')

def mark_as_cancelled(request, slug):
    order = Order.objects.get(orderNumber=slug)
    order.delivery_status = "cancelled"
    order.save()
    return redirect('/seller-orders')

def order_success(request, slug, type):
    orderno = Order.objects.get(orderNumber=slug).customer
    if(orderno==request.user):
        return render(request, 'order.html', {"order":slug, "type": type})
    
    else:
        return redirect('/page-not-found')

def seller_orders(request):
    seller=request.user.seller
    orders=Order.objects.filter(seller=seller)
    return render(request, 'orders.html', {"orders":orders})

def my_orders(request):
    customer = request.user
    orders=Order.objects.filter(customer=customer)
    return render(request, 'my-orders.html', {"orders":orders})

def delete_product(request, slug):
    product = Product.objects.get(slug=slug)
    productimage = product.image
    fs = FileSystemStorage()
    fs.delete(str(productimage))
    product.delete()
    return redirect('/your-products')

def invalid_request(request):
    return render(request, '404.html')

def page_not_found(request, exception):
    return render(request, '404.html')