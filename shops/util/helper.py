from shops.models import Shop


def check_name(shop_name: str):
    return True  if Shop.objects.filter(name=shop_name).exists() else False
