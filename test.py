def str_to_list(texte: str):
    separer = texte.split(';')
    rendu = []
    renren = []
    for i in range(len(separer)):
        rendu.append(separer[i].split(','))
    for k in rendu:
        if k != ['']:
            renren.append(f"Marque : {k[0]}, taille : {k[1]}")
    return renren

text = ';SCALA,37;GRIP,42'
str_to_list(text)