import tkinter as tk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from computations import IVP, IVP_plotter, my_IVP

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
        self.ivp = my_IVP(self.x_0_default, self.y_0_default, self.x_max_default)
        self.computer = IVP_plotter()

        self.initUI()

    def save_figure(self, fig):  
        f = tk.filedialog.asksaveasfile(mode='w', defaultextension=".png")
        if f is None: return
        fig.savefig(f.name)
        f.close()

    def initUI(self):
        '''
        GUI building
        '''
        self.master.title("DE Assignment")
        self.pack()
        # frames creation
        frame = Frame(self, borderwidth=1)
        frame.pack()
        # description
        Label(frame, text="Initial parameters:").grid(row=0, column=0, columnspan=3)
        # labels creation
        x_0_var, y_0_var, x_max_var, n_var = IntVar(), IntVar(), IntVar(), IntVar()

        Label(frame, text="x_0:").grid(row=1, column=0)
        Entry(frame, text=x_0_var).grid(row=1, column=1)
        
        Label(frame, text="y_0:").grid(row=1, column=2)
        Entry(frame, text=y_0_var).grid(row=1, column=3)

        Label(frame, text="x_max:").grid(row=1, column=4)
        Entry(frame, text=x_max_var).grid(row=1, column=5)

        Label(frame, text="N:").grid(row=1, column=6)
        Entry(frame, text=n_var).grid(row=1, column=7)

        x_0_var.set(self.x_0_default)
        y_0_var.set(self.y_0_default)
        x_max_var.set(self.x_max_default)
        n_var.set(self.n_default)
        
        # figure drawing

        def plot_first_figure():
            '''
            draws current ivp's approximation
            '''
            self.figure1 = IVP_plotter().plot_ivp(self.ivp, int(n_var.get()))
            self.bar = FigureCanvasTkAgg(self.figure1, frame).get_tk_widget()
            self.bar.grid(column=0, row=2, rowspan=6, columnspan=10)

        plot_first_figure()

        def replot_graph():
            '''
            funcion, that plots the graph of approximations
            (putted inside to have access to the variables)
            '''
            # update ivp
            x_0 = int(x_0_var.get())
            y_0 = int(y_0_var.get())
            x_max = int(x_max_var.get())
            self.ivp = my_IVP(x_0, y_0, x_max)
            # update GUI
            self.bar = None
            plot_first_figure()
            replot_error_graph()

        # buttons
        Button(frame, text="Show", command=replot_graph).grid(row=1, column=8)
        Button(frame, text="Save", command=lambda :self.save_figure(self.figure1)).grid(row=1, column=9)

        # second part of the frame
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
        
        def plot_second_graph():
            '''
            plots the graph of global errors
            '''
            n_min = int(n_min_var.get())
            n_max = int(n_max_var.get())
            n_length = int(n_length_var.get())

            self.figure2 = IVP_plotter().plot_global_errors_analysis(self.ivp, n_min, n_max, n_length)
            self.bar2 = FigureCanvasTkAgg(self.figure2, frame).get_tk_widget()
            self.bar2.grid(column=0, row=11, rowspan=6, columnspan=10)

        plot_second_graph()

        def replot_error_graph():
            '''
            updates the existing error graph
            '''
            self.bar2 = None
            plot_second_graph()
            
        Button(frame, text="Show", command=replot_error_graph).grid(row=10, column=8)
        Button(frame, text="Save", command=lambda: self.save_figure(self.figure2)).grid(row=10, column=9)

def main():
    '''
    Shows the GUI
    '''
    root = Tk()
    GUI(root)
    root.mainloop()
    
# start
if __name__ == '__main__':
    main()