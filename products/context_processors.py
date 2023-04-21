from .models import Category


def category_links(request):
#    print("cp")
    # ak=Category.objects.all()
    # print(ak.count())

    return {'links':Category.objects.all(),}