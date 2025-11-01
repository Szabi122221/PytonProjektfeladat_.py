class Dolgozo_KSZ_Osztaly:
    def __init__(self, nev, kor):
        self.nev = nev
        self.kor = int(kor)

    def __str__(self):
        return f"{self.nev} ({self.kor} év)"


def rendezes_ksz_fv(dolgozok, kulcs):
    if kulcs == 'nev':
        return sorted(dolgozok, key=lambda d: d.nev)
    elif kulcs == 'kor':
        return sorted(dolgozok, key=lambda d: d.kor)
    return dolgozok