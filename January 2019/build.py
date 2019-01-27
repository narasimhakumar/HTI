var = input('Please enter Y(es) or N(o): ')
if 'y' in var[0].lower() or 'yes' in var.lower():
    print ('You entered Yes')
else:
    if var[0].lower() == 'n':
        print ('You entered No')

print('You really entered ' + str(var))
