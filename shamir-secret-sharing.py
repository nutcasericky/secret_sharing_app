import random
from decimal import Decimal

FIELD_SIZE = 10 ** 5  # size of the graph?


def reconstruct(shares):
    """
    Combines individual shares using Lagranges interpolation.
    """
    sums = 0
    prod_arr = []

    for j, share_j in enumerate(shares):
        xj, yj = share_j
        prod = Decimal(1)

        for i, share_i in enumerate(shares):
            xi, _ = share_i
            if i != j:
                prod *= Decimal(Decimal(xi) / (xi - xj))

        prod *= yj
        sums += Decimal(prod)

    return int(round(Decimal(sums), 0))


def polynom(x, coefficients):
    """
    This generates a single point on the graph of given polynomial
    in `x`. The polynomial is given by the list of `coefficients`.
    """
    point = 0
    # Loop through reversed list, so that indices from enumerate match the
    # actual coefficient indices
    for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
        point += x ** coefficient_index * coefficient_value
    return point


def coeff(t, secret):
    """
    Randomly generate a list of coefficients for a polynomial with
    degree of `t` - 1, whose constant is `secret`.

    For example with a 3rd degree coefficient like this:
        3x^3 + 4x^2 + 18x + 554

        554 is the secret, and the polynomial degree + 1 is
        how many points are needed to recover this secret.
        (in this case it's 4 points).
    """
    coeff = [random.randrange(0, FIELD_SIZE) for _ in range(t - 1)]
    coeff.append(secret)
    return coeff


def generate_shares(n, m, secret):
    """
    Split given `secret` into `n` shares with minimum threshold
    of `m` shares to recover this `secret`, using SSS algorithm.
    """
    coefficients = coeff(m, secret)
    shares = []

    for i in range(1, n + 1):
        x = random.randrange(1, FIELD_SIZE)
        shares.append((x, polynom(x, coefficients)))

    return shares

def num2secret(num):
    string = str(num)
    # turning the ascii values into original letters
    i = 0
    secret = ""
    while i < len(string):
        if string[i] == "1":  # a 3 number ascii value
            secret += chr(int(string[i:i + 3]))
            i += 3
        else:  # a 2 number ascii value
            secret += chr(int(string[i:i + 2]))
            i += 2
    return secret

def string2num(string):
    secret = ""
    for i in range(len(string)):
        secret += str(ord(string[i]))
    secret = int(secret)
    return secret

def options():
    print()
    print("Press 1 to Generate shares")
    print("Press 2 to Reconstruct secret")
    print("Press 3 to Quit")
    return input("What would you like to do: ")

# Driver code
if __name__ == '__main__':
    # (3,5) sharing scheme
    quit = False
    while not quit:
        user_option = options() # to display out the options + ask for input
        if user_option == "1":

            # generate shares
            user_input = str(input("Key in the secret: "))  # asking user for string input
            secret = string2num(user_input) # converting the string to ascii
            print(f'Original Secret: {secret}')
            n = int(input("How many shares do you want to create: "))
            t = int(input("How many shares do you want for the secret to be restored: "))
            shares = generate_shares(n, t, secret) # generating the secret
            print(f'Shares: {", ".join(str(share) for share in shares)}')

        elif user_option == "2":
            # reconstruction of shares
            num_of_shares = int(input("how many shares are there: "))
            pool = [] # a list of shares that are keyed it
            for i in range(num_of_shares):
                x = int(input(f"please key in x values of share no {i+1}: "))
                y = int(input(f"please key in y values of share no {i+1}: "))
                pool.append((x, y))
            print(f'Combining shares: {", ".join(str(share) for share in pool)}')
            print(f'Reconstructed secret: {num2secret(reconstruct(pool))}')

        elif user_option == "3": # to quit
            quit = True
            break
        else: # input validation
            print("please type in a number from 1-3")
            continue

