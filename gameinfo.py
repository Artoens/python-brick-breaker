def scoreMax():
    scoreMax = 0
    i = 1
    try:
        while True:
            filename = str(i) + '.txt'
            with open(file=filename) as lvl:
                content = list(lvl.read().replace("\n", ""))
                briks = list(filter(lambda e: e != '.', content))
                scoreMax +=  len(briks)
            i += 1
    except IOError as e:
        pass

    return scoreMax