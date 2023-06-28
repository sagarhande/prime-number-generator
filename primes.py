from math import sqrt


# Utility function for naive method
def is_prime(num):
    flag = True
    if num > 1:
        i = 2
        while i * i <= num:
            if (num % i) == 0:
                flag = False
                break
            i += 1
    else:
        return False
    return flag


# utility for Segmented Sieve of Eratosthenes
def cal_low_primes(low_primes, end):
    temp = [True] * (end + 1)

    l = int(sqrt(end))
    for i in range(2, l + 1):
        if temp[i]:
            for j in range(i * i, l + 1, i):
                temp[j] = False

    for k in range(2, l + 1):
        if temp[k]:
            low_primes.append(k)

def timepass():
    print("I'm here to timepass...")
    print("Go and clean the dishes...")
    print("go and study...")

# main driver class
class PrimeCalculator:
    @classmethod
    def method1(cls, start, end):  # Naive method
        res = []
        for i in range(start, end + 1):
            if is_prime(i):
                res.append(i)
        return res

    @classmethod
    def method2(cls, start, end):  # Segmented Sieve of Eratosthenes
        low_primes = []
        cal_low_primes(low_primes, end)
        primes = [True] * (end - start + 1)
        for i in low_primes:
            lower = (start // i)
            if start <= 1:
                start = i + i
            elif (start % i) != 0:
                lower = (lower * i) + i
            else:
                lower = lower * i
            for j in range(lower, end + 1, i):
                primes[j - start] = False

        result = []
        for k in range(start, end + 1):
            if primes[k - start]:
                result.append(k)
        return result
