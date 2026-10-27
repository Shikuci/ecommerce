from django.shortcuts import render, redirect


def index(request):
    return render(request, 'index.html')


def store(request):
    return render(request, 'store.html')


def cart(request):
    return render(request, 'cart.html')


def signin(request):
    return render(request, 'signin.html')


def register(request):
    return render(request, 'register.html')


def product_detail(request):
    return render(request, 'product-detail.html')


def order_complete(request):
    return render(request, 'order_complete.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def search_result(request):
    return render(request, 'search-result.html')




def place_order(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        city = request.POST.get('city', '').strip()
        street = request.POST.get('street', '').strip()
        payment_method = request.POST.get('payment_method', '')

        if not all([
            first_name,
            last_name,
            phone,
            email,
            city,
            street,
            payment_method,
        ]):
            return render(request, 'place-order.html', {
                'error': 'Бүх шаардлагатай талбарыг бөглөнө үү.'
            })

        # Одоогоор зөвхөн формын илгээлтийг шалгаж байна.
        # Захиалгыг database-д хадгалах логик хараахан холбогдоогүй.

        return render(request, 'order_complete.html', {
            'success': 'Захиалгын мэдээлэл амжилттай илгээгдлээ.'
        })

    return render(request, 'place-order.html')