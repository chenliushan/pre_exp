words = ['cat', 'window', 'defenestrate']
for w in words[:]:  # Lacking [:] will cause infinite loop
    if len(w) > 6:
        words.insert(0, w)

print(words)

print('\nrange(10)')
for i in range(10):
    print('i=', i, end=',')

print('\nrange(5,9)')
for i in range(5, 9):
    print('i=', i, end=',')

print('\nrange(0,10,2)')
for i in range(0, 10, 2):
    print('i=', i, end=',')

print("\n", range(10))


def my_fun(arg1, arg2='Hei', arg3=''):
    if len(arg1) > 1:
        print(arg2, arg1)
        if (arg3):
            print(arg3)

my_fun('jana')
my_fun('jana',arg3='lalala')
my_fun('jana','lalala')