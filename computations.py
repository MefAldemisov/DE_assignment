import numpy as np              # math
import matplotlib.pyplot as plt # graphs
import warnings                 # to except output on log(0)
plt.style.use("default")        # important for IDE
warnings.filterwarnings("ignore", category=RuntimeWarning)

class IVP:
    '''
        Class that represents any first-order ivp 
        where x is defined everywhere except some dots
        It is separated due to the fact,
        that it would be possibly
        essential to emplement solutions of
        some other equations
    '''
    def __init__(self, x_0, y_0, x_max, der, c_1, y_ex, undef_x):
        '''
        (x_0, y_0) - coordinates of the inital value
        x_max - int, max x to approximate
        der - lambda function of x, y - derivative
        c_1 - lambda function of x, y - coefficient
        y_ex - lambda function of x - exact solution
        undef_x - lambda function- retrns true if x is undefined
        '''
        self.__der = der
        self.__c_1 = c_1
        self.__y_ex = y_ex

        self.x_max = x_max
        self.x_0 = x_0
        self.y_0 = y_0

        self.y = self.__create_y_exact()
        self.undefined_x = undef_x # list of dots that are forbidden for this function

    def derivative(self, x, y):
        '''
        x, y - np.arrays/numbers to
        compute derivative of my function
        '''
        if self.undefined_x(x):
            warnings.warn("x is out of range", RuntimeWarning)
            x = np.array(x) if type(x) != np.array else x
            x[self.undefined_x(x)] = None
        return self.__der(x, y)

    def __create_y_exact(self):
        '''
        returns the exact solution of IVP 
        with constant substituted
        '''
        c_1 = self.__c_1(self.x_0, self.y_0)
        return lambda x: self.__y_ex(x, c_1)

class my_IVP(IVP):

    '''
        Class that represents specificly my IVP
    '''

    def __init__(self, x_0=1, y_0=2, x_max=10):
        '''
        Class that plots the results of approximation
        for a forth IVP (works with any of them)
        (x_0, y_0) - coordinates of the inital value
        x_max - int, max x to approximate
        '''
        assert x_max > x_0, "x_0 is out of range"
        assert x_0 != 0, "x_0 is out of range"
        self.der = lambda x, y: 2*x**3 + 2*y/x
        self.c_1 = lambda x, y: y/(x)**2 - x**2
        self.y_ex = lambda x, c_1 : x**4 + c_1*x**2
        # undefined case checking
        undef_arr = [0]
        if (y_0 < x_0**4 and x_0 != 0):
            sqrt = (-self.c_1(x_0, y_0))**0.5
            undef_arr = [sqrt, -sqrt]
        self.undef_x = lambda x: x in undef_arr
        
        super().__init__(   x_0, y_0, x_max, 
                            der=self.der, 
                            c_1=self.c_1,
                            y_ex=self.y_ex,
                            undef_x=self.undef_x)
class IVP_plotter:

    def __init__(self):
        '''
        Class that plots the results of approximation
        for a given IVP (works with any of them)
        '''
        pass
    
    def __compute_euler(self, x, ivp):
        '''
        For a given ivp of class IVP computes the approximation 
        of the solution by Euler's method 
        on a given set of inputs (x)
        '''
        assert len(x) > 1, "Not enought data to approximate on"
        y = x.copy() # create array of the same length
        y[0] = ivp.y_0
        for i in range(1, len(x)):
            y[i] = y[i-1] + (x[1] - x[0]) * ivp.derivative(x[i-1], y[i-1])
        return y

    def __compute_improved_euler(self, x, ivp):
        '''
        For a given ivp of class IVP computes the approximation 
        of the solution by Inptoved Euler's method 
        on a given set of inputs (x)
        '''
        assert len(x) > 1, "Not enough data to approximate on"
        y = x.copy() # create array of the same length
        h = x[1] - x[0] # step length
        y[0] = ivp.y_0
        for i in range(1, len(x)):
            adder = ivp.derivative(x[i], y[i-1]+h*ivp.derivative(x[i-1], y[i-1]))
            y[i] = y[i-1] + h / 2 * (ivp.derivative(x[i-1], y[i-1]) + adder)
        return y

    def __compute_runge_kutta(self, x, ivp):
        '''
        For a given ivp of class IVP computes the approximation 
        of the solution by Runge Kutta's method 
        on a given set of inputs (x)
        '''
        assert len(x) > 1, "Not enought data to approximate on"

        y = x.copy() # create array of the same length
        h = x[1] - x[0] # step length
        y[0] = ivp.y_0
        for i in range(1, len(x)):
            k1 = ivp.derivative(x[i-1], y[i-1])
            k2 = ivp.derivative(x[i-1]+h/2, y[i-1]+h/2*k1)
            k3 = ivp.derivative(x[i-1]+h/2, y[i-1]+h/2*k2)
            k4 = ivp.derivative(x[i-1]+h, y[i-1]+h*k3)
            y[i] = y[i-1] + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        return y

    def __plot_results(self, x, ys, title, subplot_index=1, axis_names=["x","y"], ivp=None, methods=[1, 1, 1, 1]):
        '''
        Internal method that only plots 4 graphs

        x - np.array, x-axis values, length n
        ys - array with dimensionality (4, n), subarrays - np.arrays
        title - string that will be the eader og the plot
        subplot index - int, 0 if not required
                        in [1, 2, 3] if needed
        axis_names - array with len 2, names of the axis to be written
        ivp - IVP, problem to be solved, for exact solution only
        methods - bynary array of length 3: 0 or 1 - skip/plot for each method
                  and if we should use the log plot for local errors
        '''
        assert len(ys) == 4, "Incorrect dimensionality"
        assert subplot_index in range(4), "No such subplot supported"
        assert len(axis_names) == 2, "Wrong axis names"

        if subplot_index > 0:   plt.subplot(120+subplot_index)

        plt.title(title)
        plt.xlabel(axis_names[0])
        plt.ylabel(axis_names[1])

        if (subplot_index == 1):
            assert ivp, "No ivp to compute precise graph"
            x_first = np.arange(ivp.x_0, ivp.x_max, 0.001)
            plt.plot(x_first, ivp.y(x_first), 'k-', label="exact", lw=1)

        if (methods[0]): plt.plot(x, ys[1], 'r--', label="Euler")
        if (methods[1]): plt.plot(x, ys[2], 'b-.', label="Improved Euler", alpha=0.7, lw=2)
        if (methods[2]): plt.plot(x, ys[3], 'g', label="Runge-Kutta", markersize=5, alpha=0.5, lw=3)

        plt.legend()
        plt.grid()

    def __get_local_for_fn(self, x, y_exact, function, ivp):
        '''
        Returns local error for a given function

        x - np.array, axis to compute on
        y_exact - np.array, precise values
        errors - np.array, approximation
        function - function, approximator
        ivp - IVP, problem to be solved
        '''
        l_err = [] # to be returned
        for i in range(1, len(y_exact)):
            # calculate new approximation with the base on the next precise (x, y)
            new_ivp = IVP(x[i-1], y_exact[i-1], x[i], ivp.der, ivp.c_1, ivp.y_ex, ivp.undef_x)
            # a smal bug is here: y exact fpr each ivp is computed again
            # 
            # append the difference to the resulting array
            l_err.append(y_exact[i]-(function(x[i-1:i+1], new_ivp)[-1])) 
        # zero added as a first value
        return np.array([0]+l_err)

    def __local(self, exact_values, x, ivp):
        '''
        For a given global_errors array 
        outputs the array of the local errors

        approximations - array of 4 np.arrays with computed 
            exact, 
            euler, 
            improved euler,
            rk
        approximations

        x - the first axis with dimensionality of subarrays
        ivp - problem to be solved
        '''
        result = [
            np.zeros(len(exact_values)),
            self.__get_local_for_fn(x, exact_values, self.__compute_euler, ivp),
            self.__get_local_for_fn(x, exact_values, self.__compute_improved_euler, ivp),
            self.__get_local_for_fn(x, exact_values, self.__compute_runge_kutta, ivp)
        ]
        return result


    def plot_ivp(self, ivp, N=100, methods=[1]*5):
        '''
        Outputs the matplotpib.pyplot figure
        with 3 subplots:
            - resulted approximation of the given IVP
            - global errors from x
            - local errors from x
        N - int, length of the array of x
        methods - bynary array of length 3: 0 or 1 - skip/plot for each method
                  and if we should use the log plot for local/global errors
        '''
        assert N > 0, "Amount of x-es should be greater then 0"
        x = np.linspace(ivp.x_0, ivp.x_max, N)
        f = plt.figure(figsize=(10, 4))
        # computations
        approximations = [  ivp.y(x),
                            self.__compute_euler(x, ivp), 
                            self.__compute_improved_euler(x, ivp), 
                            self.__compute_runge_kutta(x, ivp)]
       
        # global_errors = [approximations[0]-appr for appr in approximations]
        local_errors = self.__local(approximations[0], x, ivp)
        # plotting    
        self.__plot_results(x, approximations, "Approximations of the IVP", 1, ivp=ivp, methods=methods)
        # self.__plot_results(x, global_errors, "Global errors", 2)
        local_to_plot = local_errors if methods[3]==0 else [np.log10(abs(err)) for err in local_errors]
        self.__plot_results(x, local_to_plot, "Local errors", 2, 
                            axis_names=["x", "log(y)" if methods[3] else "y"], methods=methods)
        return f


    def __get_global_error(self, N, ivp, approximation):
        '''
        N - length of the x array
        ivp - the problem to solve
        approximation - function that takes x and ivp and returns array of x's dimensionality
        '''
        x = np.linspace(ivp.x_0, ivp.x_max, N)
        # x = np.array(list(itertools.compress(x, [i ivp.undefined_x(x[i]) for i in range(len(x))])))  
        diff = approximation(x, ivp)[-1] - ivp.y(x)[-1]
        return diff

    def __get_error_array(self, Ns, ivp, function):
        '''
        Ns - length of x to be checked
        ivp - initial value proble to solve
        function -  function that takes x and ivp and returns array of x's dimensionality 
                    (appoximation)

        Returns the array of the last errors for all n
        '''
        error = [self.__get_global_error(int(n), ivp, function) for n in Ns]
        return error

    def plot_global_errors_analysis(self, ivp, n_min=100, n_max=1000, n_length=100, methods=[1]*5):
        '''
        ivp - inital value problem to solve
        n_min - min length of x's array
        n_max - max length of x's array
        n_length - amount of n to check within given bounds
        methods - bynary array of length 4: 0 or 1 - skip/plot for each method 
                  and if we should use the log plot for local/global errors
        '''
        # contracts
        assert n_max > n_min, "n_min is out of range"
        assert n_max > 0, "n_max should be positive integer"
        assert n_min > 0, "n_min should be positive integer"
        assert n_length > 0, "n_length should be positive integer"
        assert len(methods) == 5, "Invalid length of methods array"

        f = plt.figure(figsize=(10, 4))
        # computation
        Ns = np.linspace(n_min, n_max, n_length)
        ys = [  np.zeros(len(Ns)),
                self.__get_error_array(Ns, ivp, self.__compute_euler),
                self.__get_error_array(Ns, ivp, self.__compute_improved_euler),
                self.__get_error_array(Ns, ivp, self.__compute_runge_kutta)]
        # plotting
        if methods[-1]: ys = [np.log10(np.abs(arr)) for arr in ys]
        self.__plot_results(Ns, ys, "Methods' max global errors", 0, 
                            ["N", "log(error)" if methods[-1] else "error"], methods=methods)
        return f
    