
n = 0 * 10 + 3 * 9 + 7 * 8 + 2 * 7 + 1 * 6 + 7 * 5 + 8 * 4 + 3 * 3 + 2 * 3

resto = n % 11
r2 = 11 - resto
if resto == 0 or resto == 1:
    print("o digito é 0")
else:
    print("o digito é {}".format(11-resto))

n2 = 0 * 11 + 3 * 10 + 7 * 9 + 2 * 8 + 1 * 7 + 7 * 6 + 8 * 5 + 3 * 4 + 3 * 3 + 2 * 2

resto2 = n2 % 11

if resto2 == 0 or resto2 ==1:
    print("odigito é zero")
else:
    print("o digito é {}".format(11-resto2))
