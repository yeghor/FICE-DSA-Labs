import math
import typing
import matplotlib.pyplot as plt
import numpy as np

class ArccosApproximator:
    def __init__(self, n: int, x: float) -> None:
        self.n = n
        self.x = x

    def __approx_on_return(self, i: int) -> float:
        cur = None
        
        if i == 0:
            return self.x, self.x
        else:
            prev, sum_ = self.__approx_on_return(i-1)
            cur = prev * (2*i - 1)**2 * self.x**2 / (2*i * (2*i + 1))

        return cur, sum_ + cur

    def __approx_on_descent(self, i: int, p: float, t: float) -> float:
        res = None
        
        if i == 0:
            res = self.__approx_on_descent(i+1, self.x, self.x)
        elif i > self.n:
            return t
        else:
            cur = p * (2*i - 1)**2 * self.x**2 / (2*i * (2*i + 1))
            res = self.__approx_on_descent(i+1, cur, t+cur)

        return res

    def __approx_partially(self, i: int, p: float) -> float:
        sum_ = None
        cur = 0
        
        if i == 0:
            cur = self.x
            sum_ = self.__approx_partially(i+1, self.x)
        elif i >= self.n:
            return p * (2*i - 1)**2 * self.x**2 / (2*i * (2*i + 1))
        else:
            cur = p * (2*i - 1)**2 * self.x**2 / (2*i * (2*i + 1))
            sum_ = self.__approx_partially(i+1, cur)

        return cur + sum_

    def approximate(self, recursion_method: typing.Literal["return", "descent", "partially"]) -> float:
        term = math.pi / 2

        match recursion_method:
            case "return":
                # __approx_on_return returns tuple -> (last_current, sum_) due to way it works.
                # We need to get only sum_ return value, that is being stored as second element with index=1
                return term - self.__approx_on_return(self.n)[1]
            case "descent":
                return term - self.__approx_on_descent(0, 0, 0)
            case "partially":
                return term - self.__approx_partially(0, 0)

if __name__ == "__main__":
    input_x = float(input("Enter x value (float in range [-1, 1]): "))
    plot_n = int(input("Enter n range (integer in range [1, 994]): "))

    if not 1 <= plot_n <= 994:
        raise ValueError("Invalid n valaue entered!")
    elif not -1 <= input_x <= 1:
        raise ValueError("Invalid x value. Arccos handle x only in [-1, 1] range!")

    approximator = ArccosApproximator(n=plot_n, x=input_x)

    for method in ["return", "descent", "partially"]:
        print(f"Starting {method} testing!")

        for n_ in range(1, plot_n+1):
            approximator.n = n_

            approx_res = approximator.approximate(recursion_method=method)
            true_res = math.acos(input_x)

            print(f"Testing on n={n_}")
            print(f"Approx result: {approx_res}")
            print(f"True result: {true_res}")
            print()

        print(f"\n================\n")

    X, y = [_ for _ in np.linspace(-1, 1, 100)], []

    plot_n = int(input("Enter plot n in range (integer in range [1, 994]): "))

    if not 1 <= plot_n <= 994:
        raise ValueError("Invalid n value entered!")

    for x in X:
        approximator.x = x

        approx_res = approximator.approximate(recursion_method="return")
        true_res = math.acos(x)

        y.append(abs(approx_res - true_res))
    
    plt.plot(X, y)
    plt.grid(True)
    plt.ylabel("Approx error")
    plt.xlabel("x")
    plt.title(f"Method: return | n: {approximator.n}")

    plt.show()
