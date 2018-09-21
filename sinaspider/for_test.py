# -*- coding:utf-8 -*-

a = [1,3]
b = [4,7]

def main():
    for i in range(0,3):
        print '第%d次' % i
        hea()

def hea():
    for i in a:
        for j in b:
            c = i+j
            if c == 7:
                return
            print c

main()
