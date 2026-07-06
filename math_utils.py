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
