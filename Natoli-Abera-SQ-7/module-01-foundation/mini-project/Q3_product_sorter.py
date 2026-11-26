products=[
    {"phone": 15000},
    {"PC": 80000},
    {"printer": 5000}

]

def sort_product_by_price(products):
    return sorted(products, key=lambda product:product[1])

sorted_products = sort_product_by_price(products)

for product, price in sorted_products:
    print (product,"-",price,"ETB")