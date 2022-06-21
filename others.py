def adding_statement(value):
    f = open('statement', 'r', encoding='utf-8').readlines()
    if value not in f and value + '\n' not in f:
        m = open('statement', 'w+')
        m.write(''.join(f) + value + '\n')
        m.close()
    else:
        print(value + ' already exists')

def check_don(id):
    h = open('dons', 'r').readline().split('|')
    if str(id) in h:
        return 1
    else:
        return 0

def check_statement(id):
    f = open('statement', 'r', encoding='utf-8').readlines()
    for i in f:
        if str(id) in i.split(' '):
            return i.split(' ')[1][:-1:]

def replace_statement(id, final_value):
    f = open('statement', 'r',encoding='utf-8').readlines()
    for i in f:
        if str(id) in i.split(' ') or i == '\n':
            f.remove(i)
    t = open('statement', 'w+')
    t.write('\n'.join(f))
    t.close()
    adding_statement(str(id) + final_value)

def best_of_five(ingr):
    f = open('currentingr.txt', 'r', encoding='utf-8').readline().split('|')
    print(f)
    try:
        mass = {}
        for i in f:
            co = 0
            po = len(i)
            for k in ingr:
                if k in i:
                    g = list(i)
                    g.remove(k)
                    co += 1
            mass.setdefault(co/po, i)
        e = mass.keys()
        e1 = []
        for d in e:
            e1.append(float(d))
        if len(e1)>5:
            e1 = sorted(e1)[-5::]
        else:
            e1 = sorted(e1)
        final = []
        for s in e1:
            final.append(mass[s])
        return final
    except Exception:
        print(1)

def add_to_cart(id, value):
    co = 0
    t = 1
    f = open('pplfood', 'r').readlines()
    for i in f:
        if str(id) in i.split('|'):
            kek = i[:-1]
            f.remove(i)
            try:
                f.remove(['\n'])
            except ValueError:
                f = f[:-1:]
            co = 1
            break
    t = open('pplfood', 'w+')
    if co == 0:
        t = open('pplfood', 'w')
        t.write(''.join(f))
        t.write(str(id) +'|' + value + '\n')
        t.close()
    else:
        t = open('pplfood', 'w')
        t.write(''.join(f))
        t.write(kek + '|' + value + '\n')
        t.close()

def searching(id):#(на выходе массив с ккотейлями)
    f = open('recepies+ingr', 'r', encoding='utf-8').readlines()
    kokres = {}
    l = [line.rstrip() for line in f]
    for y in l:
        po = y.split('%')
        kokres.setdefault(po[0], po[1::])
    print(kokres)

    y = open('pplfood', 'r').readlines()
    f = [line.rstrip() for line in y]
    for j in f:
        if str(id) == str(j.split('|')[0]):
            cart = j.split('|')[1::]
    print(cart)


    gotowaya_viborka = []
    for t in kokres.keys():
        check = 0
        for r in kokres[t]:
            if r not in cart:
                check = 1
                break
        if check != 1:
            gotowaya_viborka.append(t)
    print(gotowaya_viborka)
    return gotowaya_viborka

def discard_pplfood(id):
    f = open('pplfood', 'r').readlines()
    m = open('pplfood', 'w')
    for k in f:
        if k.split('|')[0] != str(id):
            m.write(k)
    m.close()
