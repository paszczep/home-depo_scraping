import json


def get_product_info(tile):
    product_dict = {}

    product_url = tile.find("a", {"class": "header product-pod--ie-fix"})['href']
    product_dict['url'] = f'https://www.homedepot.com{product_url}'

    product_brand = tile.find('span', {"class": "product-pod__title__brand--bold"})
    if product_brand is not None:
        product_dict['brand'] = product_brand.text

    product_dict['title'] = tile.find('span', {"class": "product-pod__title__product"}).text

    product_model = tile.find('div', {"class": "product-identifier product-identifier__model"})
    if product_model is not None:
        product_dict['model'] = product_model.text

    main_price_divs = tile.find_all('div', {"class": "price-format__main-price"})
    print(main_price_divs)
    if main_price_divs is not None:
        if len(main_price_divs) == 1:
            main_price = [el.text for el in main_price_divs[0].find_all('span')]
            product_dict['main_price'] = f'{main_price[0]}{main_price[1]}.{main_price[2]}'
        else:
            print('in here you', main_price_divs)

    lower_price_element = tile.find('div', {"class": "price-detailed__lower-price-wrapper"})
    if lower_price_element is not None:
        if lower_price_element.text == 'See Lower Price in Cart':
            product_dict['manufacturer price'] = True

    tile_was_price = tile.find('div', {"class": "price__was-price"})
    if tile_was_price is not None:
        was_price = [el.text for el in tile_was_price.find_all('span') if '/' not in el.text]
        if len(was_price) > 0:
            product_dict['was_price'] = was_price[0]

    tile_price = tile.find('div', {'class': 'price'})
    print(tile_price)

    prod_specs_div = tile.find('div', {"class": "kpf__specs kpf__specs--simple kpf__specs--one-column"})
    if prod_specs_div is not None:
        property_names = [el.text for el in prod_specs_div.find_all('div') if 'kpf__name' in str(el['class'])]
        property_values = [el.text for el in prod_specs_div.find_all('div') if 'kpf__value' in str(el['class'])]
        prod_prop_dict = dict(zip(property_names, property_values))
        product_dict['specs'] = json.dumps(prod_prop_dict)

        product_dict['specs'] = prod_prop_dict

    return product_dict
