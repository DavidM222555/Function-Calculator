import matplotlib.pyplot as plt

# Evaluates a function at a given x value.
# Utilizes Horner's method for polynomial evaluation
def evaluate_polynomial(list_of_coefficients, x_value):
    result = list_of_coefficients[0]

    for x in range(1, len(list_of_coefficients)):
        result = result*x_value + list_of_coefficients[x]

    return result

# Purpose: Plots a function with the given coefficients. 
def plot_function(list_of_coefficients, step_size):
    list_of_x_values = list()
    list_of_y_values = list()

    for x in range(-50,51):
        list_of_x_values.append(x*step_size)
        list_of_y_values.append(evaluate_polynomial(list_of_coefficients, x*step_size))

    plt.plot(list_of_x_values, list_of_y_values)

    plt.savefig("Figure.png")

    return("Figure.jpg")
