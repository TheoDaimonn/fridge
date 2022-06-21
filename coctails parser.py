import requests
from bs4 import BeautifulSoup
typ = open('set.txt','r',encoding='utf-8').readline().split('&')
for y in typ:
    try:
        url = y
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        title = soup.find_all('title')
        title = str(title)[8::]
        title = title[:-9]

        img = soup.find_all(class_="catalog-element-info__picture")
        print(str(img))
        img = str(img).split('src="')[1][:-11]


        ingr_names = soup.find_all(class_="about-cocktail__param-title")
        ingr_names = str(ingr_names).split('>')[1::]
        p = []
        for i in range(0,len(ingr_names), 2):
            if '</a' in ingr_names[i]:
                p.append(ingr_names[i][:-4:])
            else:
                p.append(ingr_names[i][:-7:])

        ingr_names = p
        ingr_names[len(ingr_names) - 1] = ingr_names[len(ingr_names) - 1]

        ingr_values = soup.find_all(class_='about-cocktail__param-value')
        ingr_values = str(ingr_values).split('>')[1::]
        p = []
        for i in range(0,len(ingr_values), 2):
          p.append(ingr_values[i][:-7:])
        ingr_values = p
        headline = str(soup.find_all('ol')).split('<ol>')[1].split('<li>')
        po = []
        for t in range(len(headline)):
          po.append(f'{t})'+ headline[t][:-6])
        headline = po[1::]
        headline[len(headline) - 1] = headline[len(headline) - 1][:-6:]

        img_data = requests.get('https://amwine.ru'+img).content
        with open(f'{title}.jpg', 'wb+') as handler:
            handler.write(img_data)
            handler.close()
        with open(f'{title}', 'w+', encoding='utf-8') as f:
            f.write(title + '\n')
            for k in range(len(ingr_names)):
                f.write(ingr_names[k] + ingr_values[k] + '\n')
            f.write('\n')
            f.write('\n'.join(headline))
            f.close()
        op = open('currentingr.txt', 'r',encoding='utf-8').readline().split('|')
        sm = open('currentingr.txt', 'w+', encoding='utf-8')
        for u in ingr_names:
            if u not in op:
                op.append(u)
        sm.write('|'.join(op))
        sm.close()

        ik = open('recepies+ingr', 'r', encoding='utf-8').readlines()
        t = open('recepies+ingr', 'w+', encoding='utf-8')
        ik.append(title + '%'+'%'.join(ingr_names)+ '\n')
        t.write(''.join(ik))
        t.close()


        print(title)
        print(img)
        print(ingr_names)
        print(ingr_values)
        print(headline)
    except Exception:
        pass