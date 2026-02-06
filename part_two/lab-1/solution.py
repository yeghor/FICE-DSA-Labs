import math

# if i == 0:
#     result = self.x
    
#     if i < self.n:
#         return result + self.__first_recursive_approximator(i+1, result)
# else:
#     if previous_step is None:
#         raise ValueError("No previsous step provided to i larger that 0")

#     result = previous_step * (2*i - 1)**2 * self.x**2 / (2*i * (2*i + 1))

#     if i < self.n:
#         return result + self.__first_recursive_approximator(i-1, result)
    
# return result

class ArccosApproximator:
    def __init__(self, n: int, x: float) -> None:
        self.n = n
        self.x = x

    def __approx_on_return(self, i: int) -> float:
        cur = None

        print(f"cur={cur}")
        
        if i == 0:
            return self.x, self.x
        else:
            prev, sum_ = self.__approx_on_return(i-1)
            cur = prev * (2*i - 1)**2 * self.x**2 / (2*i * (2*i + 1))

        print(f"cur={cur}")

        return cur, sum_ + cur

    def __approx_on_descent(self) -> float:
        pass

    def __approx_partially(self, i: int) -> float:
        pass        


    def approximate(self) -> float:
        return (math.pi / 2) - self.__approx_on_return(0, 0, 0)


n, x = 10, 0.5 # x must be in range [-1, 1]

approx = ArccosApproximator(n, x)

print(f"Approximator: {approx.approximate()}")
print(f"True result: {math.acos(x)}")