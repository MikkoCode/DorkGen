import re
from bs4 import BeautifulSoup


def extract_words(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator=' ')
    words = re.findall(r'\b\w+\b', text)
    return set(words)


def extract_keywords(html):
    soup = BeautifulSoup(html, 'html.parser')
    keywords = set()

    # Extract keywords from title
    if soup.title:
        keywords.update(soup.title.string.split())

    # Extract keywords from meta description and keywords
    for meta in soup.find_all('meta'):
        if meta.get('name') in ['description', 'keywords'] and meta.get('content'):
            keywords.update(meta.get('content').split())

    # Extract keywords from h1 and h2 tags
    for tag in ['h1', 'h2', 'a']:
        for element in soup.find_all(tag):
            keywords.update(element.get_text().split())

    return keywords


def generate_single_word_dorks(words):
    return [f'intext:"{word}"' for word in words]


def generate_chained_dorks(words):
    and_dorks = ' AND '.join([f'intext:"{word}"' for word in words])
    or_dorks = ' OR '.join([f'intext:"{word}"' for word in words])
    return and_dorks, or_dorks


def generate_advanced_dorks(words):
    advanced_dorks = []
    for word in words:
        advanced_dorks.append(f'site:{word}.com')
        advanced_dorks.append(f'inurl:{word}')
        advanced_dorks.append(f'intitle:"{word}"')
        advanced_dorks.append(f'intext:"{word}"')
        advanced_dorks.append(f'site:{word}.com intitle:"{word}"')
        advanced_dorks.append(f'site:{word}.com inurl:{word}')
        advanced_dorks.append(f'inurl:{word} intitle:"{word}"')
        advanced_dorks.append(f'intext:{word} inurl:{word}')
    return advanced_dorks


def create_dorks(html):
    words = extract_words(html)
    keywords = extract_keywords(html)
    combined_words = words.union(keywords)

    single_word_dorks = generate_single_word_dorks(combined_words)
    chained_dorks_and, chained_dorks_or = generate_chained_dorks(combined_words)
    advanced_dorks = generate_advanced_dorks(combined_words)

    other_dorks = [f'intitle:"{word}" intext:"{word}" inurl:"{word}"' for word in combined_words]

    return single_word_dorks + [chained_dorks_and, chained_dorks_or] + advanced_dorks + other_dorks
