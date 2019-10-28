import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Frame, Button, Label, Entry, IntVar
from tkinter import BOTH, LEFT, TOP, RIGHT
from computations import IVP, IVP_plotter

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
        self.computer = IVP_plotter()

        self.initUI()

    def initUI(self):

        self.master.title("DE Assignment")
        self.pack()

        frame = Frame(self, borderwidth=1)
        frame.pack()
        Label(frame, text="Initial parameters:").grid(row=0, column=0)
        
        x_0_var, y_0_var, x_max_var, n_var = IntVar(), IntVar(), IntVar(), IntVar()

        Label(frame, text="x_0:").grid(row=1, column=0)
        Entry(frame, text=x_0_var).grid(row=1, column=1)
        
        Label(frame, text="y_0:").grid(row=1, column=2)
        Entry(frame, text=y_0_var).grid(row=1, column=3)

        Label(frame, text="x_max:").grid(row=1, column=4)
        Entry(frame, text=x_max_var).grid(row=1, column=5)

        Label(frame, text="N:").grid(row=1, column=6)
        e_n = Entry(frame, text=n_var)
        e_n.grid(row=1, column=7)

        x_0_var.set(self.x_0_default)
        y_0_var.set(self.y_0_default)
        x_max_var.set(self.x_max_default)
        n_var.set(self.n_default)
        
        figure = IVP_plotter().plot_ivp(self.ivp)

        self.bar = FigureCanvasTkAgg(figure, frame).get_tk_widget()
        self.bar.grid(column=0, row=2, rowspan=6, columnspan=9)

        def plot_graph():
            x_0 = int(x_0_var.get())
            y_0 = int(y_0_var.get())
            x_max = int(x_max_var.get())
            n = int(n_var.get())
            
            self.bar = None
            self.ivp = IVP(x_0, y_0, x_max)
            figure = IVP_plotter().plot_ivp(self.ivp, n)
            self.bar = FigureCanvasTkAgg(figure, frame).get_tk_widget()
            self.bar.grid(column=0, row=2, rowspan=6, columnspan=9)
            plot_error_graph()

        Button(frame, text="Show the result", command=plot_graph).grid(row=1, column=8)
        
        # second part
        Label(frame, text="Errors").grid(row=9, column=0)
        n_min_var, n_max_var, n_length_var = IntVar(), IntVar(), IntVar()

        Label(frame, text="n_min:").grid(row=10, column=0)
        Entry(frame, text=n_min_var).grid(row=10, column=1)
        
        Label(frame, text="n_max:").grid(row=10, column=2)
        Entry(frame, text=n_max_var).grid(row=10, column=3)

        Label(frame, text="n_length:").grid(row=10, column=4)
        Entry(frame, text=n_length_var).grid(row=10, column=5)

        n_min_var.set(self.n_min)
        n_max_var.set(self.n_max)
        n_length_var.set(self.n_length)
        
        figure = IVP_plotter().plot_global_errors_analysis(self.ivp, self.n_min, self.n_max, self.n_length)

        self.bar = FigureCanvasTkAgg(figure, frame).get_tk_widget()
        self.bar.grid(column=0, row=11, rowspan=6, columnspan=9)

        def plot_error_graph():
            n_min = int(n_min_var.get())
            n_max = int(n_max_var.get())
            n_length = int(n_length_var.get())
            
            self.bar = None
            figure = IVP_plotter().plot_global_errors_analysis(self.ivp, n_min, n_max, n_length)
            self.bar = FigureCanvasTkAgg(figure, frame).get_tk_widget()
            self.bar.grid(column=0, row=11, rowspan=6, columnspan=9)
            
        Button(frame, text="Show the result", command=plot_error_graph).grid(row=10, column=8, columnspan=2)

def main():
    root = Tk()
    GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()