from math import sqrt


# utility for Sieve of Eratosthenes
def fillPrimes(chprime, end):
    ck = [True] * (end + 1)

    l = int(sqrt(end))
    for i in range(2, l + 1):
        if ck[i]:
            for j in range(i * i, l + 1, i):
                ck[j] = False

    for k in range(2, l + 1):
        if ck[k]:
            chprime.append(k)


# Utility function for naive method
def isPrime(num):
    flag = True
    if num > 1:
        i = 2
        while i*i <= num:
            if (num % i) == 0:
                flag = False
                break
            i += 1
    else:
        return False
    return flag


# main driver class
class PrimeCalculator:
    @classmethod
    def method1(cls, start, end):    # Naive method
        res=[]
        for i in range(start, end+1):
            if isPrime(i):
                res.append(i)
        return res

    @classmethod
    def method2(cls, start, end):     # Sieve of Eratosthenes
        chprime = list()
        fillPrimes(chprime, end)
        prime = [True] * (end - start + 1)
        for i in chprime:
            lower = (start // i)
            if start <= 1:
                start = i + i
            elif (start % i) != 0:
                lower = (lower * i) + i
            else:
                lower = lower * i
            for j in range(lower, end + 1, i):
                prime[j - start] = False

        res = []
        for k in range(start, end + 1):
            if prime[k - start]:
                res.append(k)
        return res



