import json


def price_string_from_div(price_div):
    price_els = [el.text for el in price_div.find_all('span')]
    price_str = f'{price_els[0]}{price_els[1]}.{price_els[2]}'
    return price_str


def get_product_info(product_soup):
    product_dict = {}

    product_url = product_soup.find("a", {"class": "header product-pod--ie-fix"})['href']
    product_dict['url'] = f'https://www.homedepot.com{product_url}'

    product_brand = product_soup.find('span', {"class": "product-pod__title__brand--bold"})
    if product_brand is not None:
        product_dict['brand'] = product_brand.text

    product_dict['title'] = product_soup.find('span', {"class": "product-pod__title__product"}).text

    product_model = product_soup.find('div', {"class": "product-identifier product-identifier__model"})
    if product_model is not None:
        product_dict['model'] = product_model.text

    # main_price_divs = tile.find_all('div', {"class": "price"})
    price_divs = product_soup.find_all('div', {"class": "price"})
    if len(price_divs) == 2:
        price_lower, price_upper,  = price_divs[0], price_divs[1]
        price_lower = price_string_from_div(price_lower)
        price_upper = price_string_from_div(price_upper)
        product_dict['main_price'] = f'{price_lower} - {price_upper}'
        # product_dict['range_price'] = True
    elif len(price_divs) == 1:
        product_dict['main_price'] = price_string_from_div(price_divs.pop())
        # product_dict['range_price'] = False

        # for price_div in price_divs:
        #     print('price_div', price_div)
        #     if price_div is not None:
        #         # print('price div', price_div)
        #         main_price_els = price_div.find('div', {'class': "price-format__main-price"})
        #         price_els = [el.text for el in main_price_els.find_all('span')]
        #         print(f'{price_els[0]}{price_els[1]}.{price_els[2]}')
                # for price_el in main_price_els:
                #     print('price_el', price_el)

    # lower_price_element = tile.find('div', {"class": "price-detailed__lower-price-wrapper"})
    # if lower_price_element is not None:
    #     if lower_price_element.text == 'See Lower Price in Cart':
    #         product_dict['manufacturer price'] = True

    tile_was_price = product_soup.find('div', {"class": "price__was-price"})
    if tile_was_price is not None:
        was_price = [el.text for el in tile_was_price.find_all('span') if '/' not in el.text]
        if len(was_price) > 0:
            product_dict['was_price'] = was_price[0]
    else:
        was_price = product_soup.find('span', {'class': "u__strike"})
        if was_price is not None:
            product_dict['was_price'] = was_price.text

    prod_specs_div = product_soup.find('div', {"class": "kpf__specs kpf__specs--simple kpf__specs--one-column"})
    if prod_specs_div is not None:
        property_names = [el.text for el in prod_specs_div.find_all('div') if 'kpf__name' in str(el['class'])]
        property_values = [el.text for el in prod_specs_div.find_all('div') if 'kpf__value' in str(el['class'])]
        prod_prop_dict = dict(zip(property_names, property_values))
        product_dict['specs'] = json.dumps(prod_prop_dict)
        product_dict['specs'] = prod_prop_dict
    for key, value in product_dict.items():
        print(key, value)
    return product_dict
