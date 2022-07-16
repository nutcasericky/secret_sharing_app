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



# Driver code
if __name__ == '__main__':
    # (3,5) sharing scheme
    t, n = 3, 5
    user_input = str(input("Key in the secret of length less than 9: ")) # asking user for string input
    secret = ""
    for i in range(len(user_input)): # turning the string into ascii values
        secret += str(ord(user_input[i]))
    secret = int(secret)

    print(f'Original Secret: {secret}')

    # Phase I: Generation of shares
    shares = generate_shares(n, t, secret)
    print(f'Shares: {", ".join(str(share) for share in shares)}')

    # Phase II: Secret Reconstruction
    # Picking t shares randomly for
    # reconstruction
    pool = random.sample(shares, t)
    print(f'Combining shares: {", ".join(str(share) for share in pool)}')

    reconstructed = str(reconstruct(shares))
    # turning the ascii values into original letters
    i = 0
    recon_secret = ""
    while i < len(reconstructed):
        if reconstructed[i] == "1": # a 3 number ascii value
            recon_secret += chr(int(reconstructed[i:i+3]))
            i += 3
        else: # a 2 number ascii value
            recon_secret += chr(int(reconstructed[i:i+2]))
            i += 2

    print(f'Reconstructed secret: {recon_secret}')
