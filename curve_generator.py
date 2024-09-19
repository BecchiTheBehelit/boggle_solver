import matplotlib.pyplot as plt
import numpy as np

def main():
    # Read x-y pairs from the file
    try:
        with open('pairs.txt', 'r') as file:
            lines = file.readlines()
        
        # Extract x and y values from the file
        pairs = [list(map(int, line.strip().split(', '))) for line in lines]
        x_values, y_values = zip(*pairs)
    except FileNotFoundError:
        print("File 'pairs.txt' not found. Please make sure the file exists and contains valid data.")
        return
    except ValueError:
        print("Invalid data in the file. Each line should contain two integers separated by a comma and space.")
        return

    # Fit a quadratic curve (2nd-degree polynomial)
    coefficients = np.polyfit(x_values, y_values, 2)

    # Create a curve using the fitted coefficients
    curve = np.poly1d(coefficients)

    # Generate x values for smooth curve plotting (including x=5)
    x_smooth = np.linspace(min(x_values), 5, 100)

    # Calculate the y values for the smooth curve
    y_smooth = curve(x_smooth)

    # Plot the input data and the extended curve
    plt.scatter(x_values, y_values, label='Data Points', color='blue')
    plt.plot(x_smooth, y_smooth, label='Extended Curve Fit', color='red')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Scatter Plot and Extended Curve Fit')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
