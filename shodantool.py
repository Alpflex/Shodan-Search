# -*- coding: utf-8 -*-
#########################Importerar moduler

from func import *


####################################################################################################


def main():
    val = input("""
    Kolla om ditt utgående IP-adress är synilg: 1
    Kolla om ditt företags namn är synilg till Shodan: 2
    """)
    if val == '1':
        print('1')
        hostsearch()
    elif val == '2':
        print('2')
        searchcompany()
    else:
        print('Var godd och välj ett av alternativerna')
        main()




main()

while True:
    a = 0
    a = a + 1
