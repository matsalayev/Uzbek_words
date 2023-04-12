import requests
from bs4 import BeautifulSoup
import csv

def get_urls():
    result = list()
    response = requests.get('https://imlo.uz/letter/A')
    soup = BeautifulSoup(response.content, 'html.parser')
    div = soup.find('div', {'class': 'my-4 lg:my-12'})
    links = div.find_all('a')
    for link in links:
        if str(link.get('href')).__contains__('letter'):
            result.append(str(link.get('href')))
    return result
def get_count_pages(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    divs = soup.find_all('div', {'class': 'w-full'})
    for div in divs:
        links = div.find_all('a')
        temp = list()
        for link in links:
            p = str(link.get('aria-label')).split('\n')
            temp.append(p)
        try:
            test = temp[len(temp) - 2][1]
            num = ''
            for i in test:
                if i != ' ':
                    num += i
            return int(num)
        except:
            continue
def get_word_links(url):
    result = list()
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        if str(link.get('href')).__contains__('word'):
            result.append(str(link.get('href')))
    return result
def get_word_info(url):
    result = list()
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    result.append(soup.find('h1', {'class': 'font-bold text-2xl lg:text-5xl mb-0'}).text.strip())
    text = soup.find('div', {'class': 'lowercase flex space-x-3'}).text.strip()
    if text.__contains__('\n'):
        t = text.split('\n')[0]
        space = '                                   '
        if t.__contains__(','):
            t = t.split(',')[0] + ' &' + t.split(',')[1] + ' |' + text.split('\n')[len(text.split('\n'))-1].replace(space, '')
            result.append(t)
        else:
            t = t + ' |' + text.split('\n')[len(text.split('\n'))-1].replace(space, '')
            result.append(t)
    elif text.__contains__(','):
        t = text.split(',')[0] + ' &' + text.split(',')[1]
        result.append(t)
    else:
        result.append(text)
    temp = soup.find('div', {'class': 'space-y-4'}).find_all('span', {'class': 'font-bold'})[3].text.strip()
    result.append(temp.lower())
    result.append(soup.find('div', {'class': 'space-y-4'}).find_all('span', {'class': 'font-bold'})[2].text.strip())
    div = soup.find('div', {'class': 'bg-sky-500 text-white rounded-2xl p-6 space-y-4 lg:space-y-0 lg:space-x-6 lg:flex'})
    num = div.find('div', {'class': 'font-bold text-xl'}).text.strip()
    result.append(num)
    return result
def start():
    urls = get_urls()
    print('barcha harflar uchun url manzillar aniqlandi')
    for url in urls:
        n = get_count_pages(url+'?size=500')
        print(f'{url[len(url)-1]} harfi uchun sahifalar soni aniqlandi : {n}')
        for i in range(1, n + 1, 1):
            new_url = url + f'?size=500&page={i}'
            links = get_word_links(new_url)
            print(f'{i} - sahifa ochildi, sahifada {len(links)-1} ta so\'z mavjud')
            j = 0
            for link in links:
                    p = get_word_info(link)
                    j += 1
                    print(f'  {j} - so\'z ma\'lumotlari muvaffaqiyatli ko\'chirib olindi...')
                    print(p)
                    with open('uzbek_words.csv', mode='a', newline='', encoding='utf8') as file:
                        writer = csv.writer(file)
                        writer.writerow(p)
    print('Ma\'lumotlar muvaffaqiyatli saqlandi')
start()