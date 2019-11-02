from tkinter import *
from tkinter import messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from computations import IVP, IVP_plotter, my_IVP

class GUI(Frame):

    def __init__(   self, root, x_0=1, y_0=2, x_max=10, n_def=100, 
                    n_min=2, n_max=1000, n_len=100):
        '''
        GUI initialization:
        root - Tk() entity
        '''
        
        super().__init__()
        self.root = root

        self.frame = Frame(self, borderwidth=1)
        self.frame.pack()

        vars_values = [x_0, y_0, x_max, n_def, n_min, n_max, n_len]
        vars_names = ['x_0', 'y_0', 'x_max', 'n', 'n_min', 'n_max', 'n_length']
        self.variables = { var_name: IntVar() for var_name in vars_names }

        self.checks = [IntVar() for x in range(3)]
        for ch in self.checks: ch.set(1)

        self.figures = [None, None]
        self.bars = [None, None]

        for (var_name, var_value) in zip(vars_names, vars_values):
            self.variables[var_name].set(var_value)

        try:
            self.ivp = my_IVP(x_0, y_0, x_max)
            self.computer = IVP_plotter()
        except AssertionError as err:
            messagebox.showwarning("Warning", str(err))

        self.__initUI()

    def __save_figure(self, index):  
        '''
        figure saving
        fig - figure to save
        '''
        f = filedialog.asksaveasfile(mode='w', defaultextension=".png")
        if f is None: return
        self.figures[index].savefig(f.name)
        f.close()

    def get_checks(self):
        # getter = lambda x: int(x.get())
        
        return [ ch.get() for ch in self.checks]

    def __add_variables_row(self, row_index, var_names):
        '''
            row_index - integer
            var_names - list of variables names to be used in Entry
        '''
        col_index = 0
        for var_name in var_names:
            Label(self.frame, text=var_name+':').grid(row=row_index, column=col_index)
            Entry(self.frame, text=self.variables[var_name]).grid(row=row_index, column=col_index+1)
            col_index += 2

    def get_plot_by_index(self, index):
        '''
            if index is 0 - plots ivp
            if index is 1 - pltse errors graph
            returns plt.figure
        '''
        if index == 0:

            args = [self.variables[var_name].get() 
                    for var_name in ['x_0', 'y_0', 'x_max']]
            self.ivp = my_IVP(*args)
            return self.computer.plot_ivp(self.ivp, int(self.variables['n'].get()), methods=self.get_checks())

        elif index == 1:
            args = [self.variables[var_name].get() 
                    for var_name in ['n_min', 'n_max', 'n_length']]

            return self.computer.plot_global_errors_analysis(self.ivp, *args, methods=self.get_checks())
        

    def plot_figure(self, index=0, bar_row=2):
        '''
            void method,
            updates the graph of bu the fiven index
            and puts it at the bar_row place
        '''
        self.figures[index] = None
        self.bars[index] = None

        try:
            self.figures[index] = self.get_plot_by_index(index)
        except AssertionError as err:
            messagebox.showwarning("Warning", str(err))

        self.bars[index] = FigureCanvasTkAgg(self.figures[index], self.frame).get_tk_widget()
        self.bars[index].grid(column=0, row=bar_row, rowspan=6, columnspan=10)
        if index == 0: self.plot_figure(1, 12)


    def __initUI(self):
        '''
        GUI building
        '''
        self.master.title("DE Assignment")
        self.pack()
        # description

        Label(self.frame, text="Initial parameters:").grid(row=0, column=0, columnspan=3)
        # checkboxes
        methods = ["Euler", "Improved Euler", "RK"]

        col_index = 0
        for i in range(len(self.checks)):
            Checkbutton(self.frame, text=methods[i]+':', variable=self.checks[i], onvalue=1, offvalue=0
                        ).grid(row=1, column=col_index, columnspan=2)
            col_index += 2

        self.__add_variables_row (2, ['x_0', 'y_0', 'x_max', 'n'])
        self.plot_figure(0, 3)
        Button(self.frame, text="Show", command=lambda: self.plot_figure(0, 3)).grid(row=1, column=8)
        Button(self.frame, text="Save", command=lambda: self.__save_figure(0)).grid(row=1, column=9)
        
        # second part of the frame
        Label(self.frame, text="Errors").grid(row=9, column=0)
        self.__add_variables_row(11,  ['n_min', 'n_max', 'n_length'])
        self.plot_figure(1, 12)
        Button(self.frame, text="Show", command=lambda: self.plot_figure(1, 12)).grid(row=10, column=8)
        Button(self.frame, text="Save", command=lambda: self.__save_figure(1)).grid(row=10, column=9)

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