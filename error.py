from uncertainties import ufloat
from pandas import read_csv

def create_ufloat(data, err):
    ufloat_data = []
    for i, d in enumerate(data):
        ufloat_data.append(ufloat(d, err[i]))

    return ufloat_data


def calc_2_var_err(data1, data2, op):
    """
    Calulates error in c = a Y b where Y is an operation among +, -, *, / 
    """
    if op == "+":
        equation = lambda a,b : a + b

    elif op == "-":
        equation = lambda a,b : a - b
    
    elif op == "*":
        equation = lambda a,b : a * b
        
    elif op == "/":
        equation = lambda a,b : a / b
    
    return_data = []
    for i, d in enumerate(data1):
        return_data.append(equation(d, data2[i]))
    
    return return_data


def calc_err(data, formula):
    """
    Formula is of the form a*b+c with no space between operators
    data is of the form [[a_data], [b_data],...] and in the same order as the formula
    """
    operators = ((len(formula) - 1)/2) + 1
    temp_data = data[0]
    temp_op = ''
    i = 1
    while i != operators:
        temp_op = formula[2*i-1]
        temp_data = calc_2_var_err(temp_data, data[i], temp_op)
        i += 1

    return temp_data


data = read_csv('data.csv', sep='\t')
cols = len(data.columns)
data = data.to_numpy()

Data  = [create_ufloat(data[:,i],data[:,i+1]) for i in range(0,cols,2)]

formula = "a*b+c"
final_calc = calc_err(Data, formula)

print(final_calc)