import os

q =  ' '
while q != '': 
    q = input('query: ')
    os.system('socli -iq '+q)
