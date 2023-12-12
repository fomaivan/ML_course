import numpy as np

def get_dominant_eigenvalue_and_eigenvector(data, num_steps):
    """
    data: np.ndarray – symmetric diagonalizable real-valued matrix
    num_steps: int – number of power method steps
    
    Returns:
    eigenvalue: float – dominant eigenvalue estimation after `num_steps` steps
    eigenvector: np.ndarray – corresponding eigenvector estimation
    """
    ### YOUR CODE HERE
    vector = np.array([0.5] * data.shape[1])
    for i in range(num_steps):
        vector = (data @ vector) / np.linalg.norm(data @ vector)
    value = float(vector.dot(data @ vector) / vector.dot(vector))
    return value, vector