from src.com.fwk.business.info.cinclude import CInclude


def a(aa):
    t=aa
    t.gtpbeginflag=0
    print('a-',t.gtpbeginflag)

def b(bb):
    g = bb
    g.gtpbeginflag=1
    print('b-',g.gtpbeginflag)



def main():
    cinc = CInclude()
    cinc.gtpbeginflag=3
    print('m-',cinc.gtpbeginflag)

    a(cinc)
    b(cinc)

    print(cinc.gtpbeginflag)

main()