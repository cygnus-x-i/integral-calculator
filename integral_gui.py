
# ################################################################################################################
# # Check for libraries
# while True:
#     try:
#         # If all libraries are present, continue to next section
#         import tkinter as tk
#         from tkinter import messagebox
#         from sympy import Symbol, sympify, integrate
#         import sympy as sy
#         break

#     except ImportError as imp_err:
#         import os
#         import random

#         print(f"\nYou are missing:  {imp_err.name}")

#         # Generates a random passcode
#         passcode = ""
#         characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%&_=+-?~"
#         for i in range(10):
#             passcode += random.choice(characters)

#         # Enter the passcode for installation -- I don't like installing things on other people's computers
#         # without them knowing what they are downloading.  This prevents accidental installation.
#         while input(f"Enter the following characters to install {imp_err.name}:  {passcode}  ") != passcode:
#             print("\nPasscodes do not match, please try again")
#             passcode = ""
#             for i in range(10):
#                 passcode += random.choice(characters)

#         os.system(f"pip install {imp_err.name}") # Installs missing library

#         # Return to try block to re-import libraries #
import tkinter as tk
from tkinter import messagebox
from sympy import Symbol, sympify, integrate
import sympy as sy
################################################################################################################
# Python Integration GUI

# Variable of integration - set to x
x = Symbol('x')

def function_input():
    """
    Takes input of a function of x, and the upper/lower bounds
    Converts function to a function readable by sympy

    Return: Tuple
        f: sympified function
        a: lower bound
        b: upper bound
    """
    global function_entry, lower_bound_entry, upper_bound_entry

    f_expr = function_entry.get()
    a_input = lower_bound_entry.get()
    b_input = upper_bound_entry.get()

    try:
        f = sympify(f_expr)
        a = sympify(a_input)
        b = sympify(b_input)

        return (f, a, b)

    except Exception as e:
        raise ValueError(f"Errror {e}")

def calc_integrals(event=None):
    """
    - Makes sure the lower bound is less than or equal to the upper bound
    - Finds the definite and indefinite integrals of the function given in 
        function_input()
    - Catches any divide by zero errors

    This function does two things because it is much less code to write than 
    splitting it into two functions, and it works more or less the same.
    """
    global result_label, indefinite_result_label, error_label

    # Clear previous error messages
    error_label.config(text="")

    try:
        func, a, b = function_input()

        if a > b:
            raise ValueError("Lower bound must be less than upper bound.")

        # Calculates definite integral
        integral = integrate(func, (x, a, b))
        result_text = f"Definite Integral Result: {integral}"
        # Make the results more readable
        result_text = result_text.replace("pi", "π").replace("**", "^")\
            .replace("log", "ln").replace("ln_", "log_")
        result_label.config(text=result_text)
        result_label.config(width=len(result_text))

        # Calculates indefinite Integral
        indefinite_integral = integrate(func, x)
        indefinite_result_text = f"Indefinite Integral Result: {indefinite_integral} + C"
        # Make the results more readable
        indefinite_result_text = indefinite_result_text.replace("pi", "π")\
            .replace("**", "^").replace("log", "ln").replace("ln_", "log_")
        indefinite_result_label.config(text=indefinite_result_text)
        indefinite_result_label.config(width=len(indefinite_result_text))

    except ValueError as ve:
        error_label.config(text=str(ve))

    except ZeroDivisionError:
        error_label.config(text="Error: Division by zero.")

    except Exception as e:
        error_label.config(text=f"Error: {str(e)}")

def calc_def_integral(func, a, b):
    # No longer used; combined into above function
    x = sy.Symbol("x")
    func = sympify(func)
    a = sympify(a)
    b = sympify(b)
    integral = integrate(func, (x, a, b))
    return str(integral)

def calc_indef_integral(func, var):
    # No longer used; combined with above function
    x = sy.Symbol(var)
    func = sympify(func)
    integral = integrate(func, x)
    return str(integral)

def clear_fields(event=None):
    # Clears all fields in the GUI
    global function_entry, lower_bound_entry, upper_bound_entry, result_label, indefinite_result_label, error_label
    function_entry.delete(0, tk.END)
    lower_bound_entry.delete(0, tk.END)
    upper_bound_entry.delete(0, tk.END)
    result_label.config(text="")
    indefinite_result_label.config(text="")
    error_label.config(text = "")

def show_instructions(event=None):
    # Displayed when the user presses Alt+Enter
    information = """
    Special Characters and Functions in Sympy:

    - Basic arithmetic operators: +, -, *, /
    - Exponentiation: ** (e.g., x**2 for x squared)
    - Constants: pi (π), E (Euler's number)
    - Infinity: oo, -oo
    - Trigonometric functions: sin(), cos(), tan(), cot(), sec(), csc()
    - Inverse trigonometric functions: asin(), acos(), atan(), acot(), asec(), acsc()
    - Hyperbolic functions: sinh(), cosh(), tanh(), coth(), sech(), csch()
    - Inverse hyperbolic functions: asinh(), acosh(), atanh(), acoth(), asech(), acsch()
    - Logarithmic functions: log() = ln(), log_b()
    - Exponential function: exp()  (e^_)
    - Square root function: sqrt()
    - Absolute value function: abs()
    - Ceiling and floor functions: ceiling(), floor()
    - Factorial function: factorial()
    - Derivative: diff(function, variable)

    - nan - not a number
    - Remember that log() is the symbol for ln() in sympy. There is an alias built into sympy so you can use ln(), but if you get log() as a returned value, it really means ln().
    - Occasionally sympy will return the same expression that you put in.  This means it is too complex for sympy to handle, and unfortunately won't work.e

    No implicit multiplication yet.
    Make sure to enter the functions and expressions using the correct syntax.  If you aren't getting expected results or a lot of syntax errors, use parentheses.
    Complex Composite Functions are not supported.
    """
    messagebox.showinfo("Information", information)

def main():
    # GUI Setup
    root = tk.Tk()
    root.title("Integral Calculator")

    global function_entry, lower_bound_entry, upper_bound_entry, result_label, indefinite_result_label, error_label

    # Function Entry
    function_label = tk.Label(root, text="Expression for f(x):")
    function_label.pack()
    function_entry = tk.Entry(root, width=50)
    function_entry.pack(pady=5)

    # Lower Bound Entry
    lower_bound_label = tk.Label(root, text="Lower bound (a):")
    lower_bound_label.pack()
    lower_bound_entry = tk.Entry(root, width=20)
    lower_bound_entry.pack(pady=5)

    # Upper Bound Entry
    upper_bound_label = tk.Label(root, text="Upper bound (b):")
    upper_bound_label.pack()
    upper_bound_entry = tk.Entry(root, width=20)
    upper_bound_entry.pack(pady=5)

    # Instruction Label
    instruction_label = tk.Label(root, text="Press Alt + Enter for more information", fg="blue")
    instruction_label.pack(pady=5)

    # Calculate Button
    calculate_button = tk.Button(root, text="Calculate\n(Enter)", command=calc_integrals)
    calculate_button.pack(side=tk.LEFT, padx=20, pady=5)
    root.bind("<Return>", calc_integrals)

    # Clear Button
    clear_button = tk.Button(root, text="Clear\n(Ctrl+Enter)", command=clear_fields)
    clear_button.pack(side=tk.LEFT, padx=5, pady=5)
    root.bind("<Control-Return>", clear_fields)

    # Alt + Enter to show instructions
    root.bind("<Alt-Return>", show_instructions)

    # Definite Integral Result Label
    result_label = tk.Label(root, text="", width=50)
    result_label.pack(pady=5)

    # Indefinite Integral Result Label
    indefinite_result_label = tk.Label(root, text="", width=50)
    indefinite_result_label.pack(pady=5)

    # Error Label
    error_label = tk.Label(root, text="", fg="red", width = 100)
    error_label.pack(pady=5)

    # Escape to exit
    # root.bind("<Escape>", quit)

    root.mainloop()

if __name__ == "__main__":
    main()
