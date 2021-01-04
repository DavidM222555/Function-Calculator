import tkinter as tk
import MathFunctions
from PIL import Image, ImageTk

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.title("Numerical Calculator")

        # We immediately switch the frame to the StartPage
        self.switch_frame(StartPage)

        self.minsize(700,700)
        self.maxsize(700,700)

    # Functionality for changing between the various pages/views of this application
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)

        if(self._frame is not None):
            self._frame.destroy()

        self._frame = new_frame
        self._frame.pack(fill='both', expand = True)

# On this page we allow the user to choose the type of function they are 
# going to want to perform calculations on. 
class StartPage(tk.Frame):
    def __init__(self, master):

        tk.Frame.__init__(self, master)
        self.configure(bg = '#FFFFFF')

        title = tk.Label(self, text = "FUNCTION CALCULATOR", font = ("Times New Roman", 28), bg = "#FFFFFF")
        title.place(relx = .52, rely = .18, anchor = tk.N)

        polynomial = tk.Button(self, text = 'Polynomial function', width = 20, height = 2, command = lambda: master.switch_frame(PolynomialPage))
        polynomial.place(relx = .5, rely = .57, anchor = tk.N)
        trigonometric = tk.Button(self, text = 'Trig function', width = 20, height = 2, command = lambda: master.switch_frame(TrigPage))
        trigonometric.place(relx = .5, rely = .63, anchor = tk.N)
        exponential = tk.Button(self, text = 'Exponential function', width = 20, height = 2, command = lambda: master.switch_frame(ExponentialPage))
        exponential.place(relx = .5, rely = .69, anchor = tk.N)
        logarithm = tk.Button(self, text = 'Logarithmic function', width = 20, height = 2, command = lambda: master.switch_frame(LogarithmPage))
        logarithm.place(relx = .5, rely = .75, anchor = tk.N)

class PolynomialPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg = '#FFFFFF')

        title_label = tk.Label(self, text = "POLYNOMIAL SOLVER", font=("Times New Roman", 24), bg = '#FFFFFF')
        title_label.place(relx = .5, rely = .05, anchor = tk.N)

        degreeOfPolynomial = 0
        listOfCoefficients = []

        instructions = tk.Label(self, text = "Please enter the coefficients of the polynomial: (You can leave it blank for zero)", font = ("Times New Roman", 12), bg = "#FFFFFF")
        degreeOfPolynomial_label = tk.Label(self, text = 'Degree of polynomial (min:0, max:7)', bg = '#FFFFFF', font = ("Times New Roman", 12))
        degreeOfPolynomial_label.place(relx = .45, rely = .2, anchor = tk.N)
        degreeOfPolynomial = tk.Entry(self, width = 5, relief = tk.GROOVE)
        degreeOfPolynomial.place(relx = .65, rely = .2, anchor = tk.N)

        submitButton = tk.Button(self, text = 'Submit', width = 7, height = 1, command = lambda: submit_degree())
        submitButton.place(relx = .5, rely = .3, anchor = tk.N)

        # Button for the user to return to the main menu page
        mainMenuButton = tk.Button(self, text = 'Main Menu', width = 9, height = 1, command = lambda: master.switch_frame(StartPage))
        mainMenuButton.place(relx = .9, rely = .07, anchor = tk.N)

        # Get the degree currently in the degreeOfPolynomial entry box
        def submit_degree():
            degreeOfPolynomialINT = (int)(degreeOfPolynomial.get()) + 1

            if(degreeOfPolynomialINT < 0 or degreeOfPolynomialINT > 8):
                invalid = tk.Label(self, text = 'Please enter a correct degree')
                invalid.place(relx = .5, rely = .76, anchor = tk.N)
                invalid.after(3000, invalid.destroy) # Delete the box after 3000 ms
            else:
                degreeOfPolynomial_label.destroy()
                submitButton.destroy()
                degreeOfPolynomial.destroy()

                getCoefficients(degreeOfPolynomialINT)

        # Sets up the entry boxes for getting the coefficients for the polynomial
        def getCoefficients(degreeOfPolynomial):
            instructions.place(relx = .5, rely = .15, anchor = tk.N)

            # These variables are used for placing the buttons on the page in an ordered manner
            # The following for loop will increment them in a fashion that keeps them orderly
            xLabelOffset = 0
            yLabelOffSet = 0

            # Used to store the label and entry widgets for later access and cleanup
            listOfLabels = []
            listOfEntryBoxes = []

            # This function places the buttons for getting the associated coefficients
            for x in range(0, degreeOfPolynomial):
                if(x == 4):
                    xLabelOffset = 0
                    yLabelOffSet += .2

                labelString = 'k*x^' + (str)(x) + " ="
                listOfLabels.append(tk.Label(self, text = labelString, font = ("Times New Roman", 10), bg = "#FFFFFF"))
                listOfLabels[x].place(relx = .2 + xLabelOffset, rely = .25 + yLabelOffSet)
                listOfEntryBoxes.append(tk.Entry(self, width = 5, relief = tk.GROOVE))
                listOfEntryBoxes[x].place(relx = .2 + xLabelOffset + .07, rely = .25 + yLabelOffSet)

                xLabelOffset += .15

            submitButton = tk.Button(self, text = 'Submit', width = 7, height = 1, command = lambda: displayFunction(listOfEntryBoxes, listOfLabels, submitButton))
            submitButton.place(relx = .5, rely = .6, anchor = tk.N)

        # We display the function and give options for calculating the derivative and integral
        def displayFunction(listOfEntryBoxes, listOfLabels, submitButton):

            # We get the entries and then destroy them
            for entry in listOfEntryBoxes:
                if(entry.get() == ''):
                    listOfCoefficients.append(0)
                else:
                    listOfCoefficients.append((int)(entry.get()))

                entry.destroy() # Delete the entry box

            for label in listOfLabels: # Delete all the labels
                label.destroy()

            # Delete the instructions at the top
            instructions.destroy()

            # Delete the old submit button
            submitButton.destroy()

            # Produce the function string that we will show to the user
            functionString = "f(x) = "

            for x in range(len(listOfCoefficients) - 1, -1, -1):
                if(listOfCoefficients[x] != 0 and x == 0):
                    functionString += (str)(listOfCoefficients[x])
                elif(listOfCoefficients[x] == 0):
                    functionString += ""
                else:
                    functionString += (str)(listOfCoefficients[x]) + "x^" + (str)(x) + " + "
            
            # If the entire function is blank we make it the function y = 0
            if(functionString == "f(x) = "):
                functionString += "0"
            
            # Display the function for the user
            labelForFunction = tk.Label(self, text = functionString, font = ("Times New Roman", 12), bg = '#FFFFFF')
            labelForFunction.place(relx = .5, rely = .4, anchor = tk.N)

            # We now display the functions for calculating the deriviatve, integral, and root of the function
            button_for_derivative = tk.Button(self, text = "Symbolic derivative", font = ("Times New Roman", 11), width = 17, height = 2)
            button_for_integral = tk.Button(self, text = "Symbolic integral", font = ("Times New Roman", 11), width = 17, height = 2)
            button_for_numerical_derivative = tk.Button(self, text = "Numerical derivative", font = ("Times New Roman", 11), width = 17, height = 2)
            button_for_numerical_integral = tk.Button(self, text = "Numerical integration", font = ("Times New Roman", 11), width = 17, height = 2)

            button_for_derivative.place(relx = .3, rely = .7, anchor = tk.N)
            button_for_integral.place(relx = .6, rely = .7, anchor = tk.N)
            button_for_numerical_derivative.place(relx = .3, rely = .8, anchor = tk.N)
            button_for_numerical_integral.place(relx = .6, rely = .8, anchor = tk.N)


class TrigPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg = '#FFFFFF')

        title_label = tk.Label(self, text = "TRIG SOLVER", font=("Times New Roman", 24), bg = '#FFFFFF')
        title_label.place(relx = .5, rely = .05, anchor = tk.N)

class ExponentialPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg = '#FFFFFF')

        title_label = tk.Label(self, text = "EXPONENTIAL SOLVER", font=("Times New Roman", 24), bg = '#FFFFFF')
        title_label.place(relx = .5, rely = .05, anchor = tk.N)

class LogarithmPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg = '#FFFFFF')

        title_label = tk.Label(self, text = "LOGARITHM SOLVER", font=("Times New Roman", 24), bg = '#FFFFFF')
        title_label.place(relx = .5, rely = .05, anchor = tk.N)

listOfCoefficients = [1,2,3,4]
print(MathFunctions.evaluate_polynomial(listOfCoefficients, 4))

# Runs the application
app = Application()
app.mainloop()