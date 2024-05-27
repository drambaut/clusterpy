import re

def fieldOperation(function, Y, fieldnames):
    """
    This method receives a string which contains a function or formula written by the user. That function has operations between the variables of Y (a data dictionary) which names are contained in fieldnames (a list), the function is applied to the corresponding values in each element of Y. The return value is a list containing the results of the function.

    :param function: function defined by the user, written like a python operation
    :type function: string
    :rtype: list (Y dictionary with the results)
    """ 
    variables = []
    positions = []
    auxiliar1 = []
    count = 0
    results = []
    newfunc = ''
    for i in fieldnames[0:]:
        if re.search(i,function):
            if not (function[function.index(i) - 2: function.index(i)].isalpha()):
                variables.append(i)
                positions.append(fieldnames.index(i))
    for j in Y:
        auxiliar1 = []
        count = 0
        newfunc = function
        for k in positions:
            auxiliar1.append(Y[j][k])
        for l in variables:
            if len(re.findall(l,newfunc)) == 1:
                newfunc = re.compile(l).sub(str(auxiliar1[variables.index(l)]), newfunc)
            else:
                if newfunc.index(re.findall(l, newfunc)[0]) != newfunc.index(re.findall('(\D)' + l, newfunc)[1]):
                    newfunc = re.compile('(\W)-[+,-]' + l).sub(str(auxiliar1[variables.index(l)]), newfunc)
        for l in variables:
            newfunc = re.compile(l).sub(str(auxiliar1[variables.index(l)]), newfunc)
        try:
            n = eval(newfunc)            
        except ZeroDivisionError:
            raise ZeroDivisionError("Division by zero was detected")
        results.append(n)                    
    return results