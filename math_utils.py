def transpose(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    new_matrix = [[0] * rows for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            new_matrix[j][i] = matrix[i][j]
    return new_matrix

def matrix_multiply(A, B):
    r1=len(A)
    r2=len(B)
    c1=len(A[0])
    c2=len(B[0])
    result = [[0] * c2 for _ in range(r1)]

    for i in range(r1):
        for j in range(c2):
            for k in range(c1):
                result[i][j] += (A[i][k] * B[k][j])
    return result

def linear_regression(X,y, learning_rate = 0.0001,iterations = 1000):
    betas = [0, 0, 0, 0, 0]
    n = len(X)
    for _ in range(iterations):
        gradients = [0, 0, 0, 0, 0]
        for i in range(n):
            predicted = predict(X[i],betas)
            error = predicted - y[i]
            gradients[0] += error
            for j in range(4):
                gradients[j+1] += error * X[i][j]
        for j in range(5):
            betas[j] -= learning_rate * (1/n) * gradients[j]
    return betas

def predict(row, betas):
    predicted = betas[0] + betas[1]*row[0] + betas[2]*row[1] + betas[3]*row[2] + betas[4]*row[3]
    return predicted


def calculate_mse(X, y, betas):
    n = len(X)
    total_error = 0
    for i in range(n):
        predicted = predict(X[i], betas)
        error = predicted - y[i]
        squared_error = error**2
        total_error += squared_error
    mse = total_error/n
    return mse
        