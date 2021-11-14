# Amazon Top Reviews for Products
# Tutorial from John Watson Rooney YouTube channel

from requests_html import HTMLSession
import pandas as pd


def get_asins(search_term): 
    url = f'http://amazon.com/s?k={search_term}'
    r = s.get(url)
    r.html.render(sleep=2)
    asins = r.html.find('div.s-main-slot div[data-asin]')

    #for asin in asins:
    #    if asin.attrs['data-asin'] != '':
    #        print(asin.attrs['data-asin'])

    # List comprehension of for loop above:
    return [asin.attrs['data-asin'] for asin in asins if asin.attrs['data-asin'] != '']

# print(get_asins('nvme'))

def get_data(asin):
    r = s.get(f'https://www.amazon.com/dp/{asin}?th=1')
    r.html.render(sleep=1)
    product_name = r.html.find('#productTitle', first=True).full_text.strip()
    try: 
        ratings_count = r.html.find('#acrCustomerReviewText', first=True).full_text
    except: 
        ratings_count = 0
    reviews = r.html.find('div[data-hook=review]')

    top_reviews = []

    for rev in reviews: 
        try:
            rating_title = rev.find('a[data-hook=review-title] span', first=True).full_text
        except: 
            rating_title = ''
        try:
            star_rating = rev.find('i[data-hook=review-star-rating] span', first=True).full_text
        except: 
            star_rating = ''

        ratings = {
            'rating_title': rating_title,
            'star_rating': star_rating,
        }

        top_reviews.append(ratings)

    product = {
        'product_name': product_name, 
        'ratings_count': ratings_count, 
        'top_reviews': top_reviews,
    }

    print(product)
    return product

# get_data('B07MFZXR1B')

def main():
    search_term = 'nvme'
    asins = get_asins(search_term)
    print(f'Found {len(asins)} asins')
    results = [get_data(asin) for asin in asins]
    df = pd.DataFrame(results)
    df.to_csv(search_term + '.csv', index=False)
    print('Saved items to CSV file.')


if __name__ == '__main__':
    s = HTMLSession()
    main()