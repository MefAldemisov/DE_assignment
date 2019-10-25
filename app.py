import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Frame, Button, Label, Entry, IntVar
from tkinter import BOTH, LEFT, TOP, RIGHT
plt.style.use("default")

class IVP:
    
    def __init__(self, x_0=1, y_0=2, x_max=10):
        assert x_max > x_0, "x_0 is out of range"
        self.x_max = x_max
        self.x_0 = x_0
        self.y_0 = y_0
        self.y = self.__create_y_exact()
    
    def derivative(self, x, y):
        return 2*x**3 + 2*y/x

    def __create_y_exact(self):
        assert self.x_0 != 0, "Invalid x_0 value"
        c_1 = self.y_0/(self.x_0)**2 - self.x_0**2
        return lambda x : x**4 + c_1*x**2
    
class IVP_computer:
    
    def __init__(self):
        pass
    
    def __compute_euler(self, x, ivp):
        y = x.copy()
        y[0] = ivp.derivative(ivp.x_0, ivp.y_0)
        for i in range(1, len(x)):
            y[i] = y[i-1]+(x[1]-x[0])*ivp.derivative(x[i-1], y[i-1])
        return y

    def __compute_improved_euler(self, x, ivp):
        y = x.copy()
        h = x[1]-x[0]
        y[0] = ivp.derivative(ivp.x_0, ivp.y_0)
        for i in range(1, len(x)):
            adder = ivp.derivative(x[i], y[i-1]+h*ivp.derivative(x[i-1], y[i-1]))
            y[i] = y[i-1]+h/2*(ivp.derivative(x[i-1], y[i-1]) + adder)
        return y

    def __compute_runge_kutta(self, x, ivp):
        y = x.copy()
        h = x[1]-x[0]
        y[0] = ivp.derivative(ivp.x_0, ivp.y_0)
        for i in range(1, len(x)):
            k1 = ivp.derivative(x[i-1], y[i-1])
            k2 = ivp.derivative(x[i-1]+h/2, y[i-1]+h/2*k1)
            k3 = ivp.derivative(x[i-1]+h/2, y[i-1]+h/2*k2)
            k4 = ivp.derivative(x[i-1]+h, y[i-1]+h*k3)
            y[i] = y[i-1] + h/6*(k1 + 2*k2 + 2*k3 + k4)
        return y

    def __get_error(self, N, ivp, approximation, return_abs=True):
        x = np.linspace(ivp.x_0, ivp.x_max, N)
        diff = approximation(x, ivp)[-1] - ivp.y(x[-1])
        if return_abs:
            return abs(diff)
        return diff

    def __get_error_array(self, Ns, ivp, function, return_abs=True):
        error = []
        for n in Ns:
            error.append(self.__get_error(int(n), ivp, function, return_abs))
        return error

    def plot_errors(self, ivp, n_min=2, n_max=1000, n_length=100):
        Ns = np.linspace(n_min, n_max, n_length)
        f = plt.figure(figsize=(5, 5))
        plt.title("Methods' errors")
        plt.xlabel("n")
        plt.ylabel("error")
        plt.plot(Ns, self.__get_error_array(Ns, ivp, self.__compute_euler), 'ro', label="euler")
        plt.plot(Ns, self.__get_error_array(Ns, ivp, self.__compute_improved_euler), 'bo', label="improved euler")
        plt.plot(Ns, self.__get_error_array(Ns, ivp, self.__compute_runge_kutta), 'go', label="rk")
        plt.grid()
        plt.legend()
        plt.savefig("errors.png")
        return f
    
    def get_least_error(self):
        pass

    def plot_results(self, ivp, N=100):
        
        x = np.linspace(ivp.x_0, ivp.x_max, N)
        f = plt.figure(figsize=(5, 5))
        plt.title(r"IVP for: $y'=2\frac{y}{x}+2x^3$")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.plot(x, ivp.y(x), 'k-', label="exact")
        plt.plot(x, self.__compute_euler(x, ivp), 'r--', label="euler")
        plt.plot(x, self.__compute_improved_euler(x, ivp), 'b--', label="improved euler")
        plt.plot(x, self.__compute_runge_kutta(x, ivp), 'g--', label="rk")
        plt.legend()
        plt.grid()
        plt.savefig("result.png")
        return f

class GUI(Frame):

    def __init__(self, root):
        super().__init__()
        self.root = root
        self.x_0_default = 1
        self.y_0_default = 2
        self.x_max_default = 10
        self.n_default = 100
        self.n_min = 2
        self.n_max = 1000
        self.n_length = 100
        self.ivp = IVP(self.x_0_default, self.y_0_default, self.x_max_default)
        self.computer = IVP_computer()

        self.initUI()

    def initUI(self):

        self.master.title("DE Assignment")
        self.pack()

        frame = Frame(self, borderwidth=1)
        frame.pack()

        Label(frame, text="Initial parameters:").grid(row=0, column=0)
        x_0_var, y_0_var, x_max_var, n_var = IntVar(), IntVar(), IntVar(), IntVar()

        Label(frame, text="x_0:").grid(row=1, column=0)
        e_x_0 = Entry(frame, text=x_0_var)
        e_x_0.grid(row=1, column=1)
        
        Label(frame, text="y_0:").grid(row=2, column=0)
        e_y_0 = Entry(frame, text=y_0_var)
        e_y_0.grid(row=2, column=1)

        Label(frame, text="x_max:").grid(row=3, column=0)
        e_x_max = Entry(frame, text=x_max_var)
        e_x_max.grid(row=3, column=1)

        Label(frame, text="N:").grid(row=4, column=0)
        e_n = Entry(frame, text=n_var)
        e_n.grid(row=4, column=1)

        x_0_var.set(self.x_0_default)
        y_0_var.set(self.y_0_default)
        x_max_var.set(self.x_max_default)
        n_var.set(self.n_default)
        
        figure = IVP_computer().plot_results(self.ivp)

        self.bar = FigureCanvasTkAgg(figure, frame).get_tk_widget()
        self.bar.grid(column=3, row=0, rowspan=6, columnspan=4)

        def plot_graph():
            x_0 = int(e_x_0.get())
            y_0 = int(e_y_0.get())
            x_max = int(e_x_max.get())
            n = int(e_n.get())
            
            self.bar = None
            self.ivp = IVP(x_0, y_0, x_max)
            figure = IVP_computer().plot_results(self.ivp, n)
            self.bar = FigureCanvasTkAgg(figure, frame).get_tk_widget()
            self.bar.grid(column=2, row=0, rowspan=6, columnspan=2)

        def change_frame():
            frame.destroy()
            self.errorUI()
            
        Button(frame, text="Show the result", command=plot_graph).grid(row=5, column=0, columnspan=2)
        Button(frame, text="Show errrors", command=change_frame).grid(row=6, column=0, columnspan=2)

    def errorUI(self):
        frame = Frame(self, borderwidth=1)
        frame.pack()

        Label(frame, text="Errors").grid(row=0, column=0)
        n_min_var, n_max_var, n_length_var = IntVar(), IntVar(), IntVar()

        Label(frame, text="n_min:").grid(row=1, column=0)
        e_x_0 = Entry(frame, text=n_min_var)
        e_x_0.grid(row=1, column=1)
        
        Label(frame, text="n_max:").grid(row=2, column=0)
        e_y_0 = Entry(frame, text=n_max_var)
        e_y_0.grid(row=2, column=1)

        Label(frame, text="n_length:").grid(row=3, column=0)
        e_x_max = Entry(frame, text=n_length_var)
        e_x_max.grid(row=3, column=1)

        n_min_var.set(self.n_min)
        n_max_var.set(self.n_max)
        n_length_var.set(self.n_length)
        
        figure = IVP_computer().plot_errors(self.ivp, self.n_min, self.n_max, self.n_length)

        self.bar = FigureCanvasTkAgg(figure, frame).get_tk_widget()
        self.bar.grid(column=3, row=0, rowspan=6, columnspan=4)

        def plot_graph():
            n_min = int(n_min_var.get())
            n_max = int(n_max_var.get())
            n_length = int(n_length_var.get())
            
            self.bar = None
            figure = IVP_computer().plot_errors(self.ivp, n_min, n_max, n_length)
            self.bar = FigureCanvasTkAgg(figure, frame).get_tk_widget()
            self.bar.grid(column=2, row=0, rowspan=6, columnspan=2)
            
        def change_frame():
            frame.destroy()
            self.initUI()

        Button(frame, text="Show the result", command=plot_graph).grid(row=5, column=0, columnspan=2)
        Button(frame, text="Change IV", command=change_frame).grid(row=6, column=0, columnspan=2)

def main():
    root = Tk()
    GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()