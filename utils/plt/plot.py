import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO


def generate_plot():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.plot(x, y)
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.title('Sine wave')
    # Save the plot as a bytes object
    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    return img_bytes.getvalue()
