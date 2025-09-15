import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.axes
from typing import Union, Tuple

def dim_color(color: Union[str, Tuple[float, float, float]], 
              factor: float=0.5) -> Tuple[float, float, float]:
    """
    ----------------------------------------------------------------------------
    This functions dim a color by blending it with white.
    ----------------------------------------------------------------------------
    Parameters:
    - color: str or tuple of floats
        Any matplotlib-recognized color format (name, hex, or RBG tuple).
    - factor: float
        factor = 0 (original color); factor = 1 (white). Default is 0.5.
    ----------------------------------------------------------------------------
    Returns:
    - dimmed: tuple of floats
        The dimmed RGB color as a 3-tuple of values within [0, 1].
    ----------------------------------------------------------------------------
    """
    # Convert to RGB tuple
    rgb = mcolors.to_rgb(color)       
    # Blend with white
    dimmed = tuple( (1-factor)*c + factor*1 for c in rgb )  
    
    return dimmed

def plot_grid(ax: matplotlib.axes.Axes, X: np.ndarray, Y: np.ndarray, 
              title: str, clr: Union[str, tuple[float, float, float]] = "black", 
              lw: float = 1.0, ls: str = '-') -> None:
    """
    ----------------------------------------------------------------------------
    Helper function to plot a structured grid of results.
    ----------------------------------------------------------------------------
    Parameters:
    - ax: matplotlib.axes.Axes
        Matplotlib axes object where the grid will be plotted.
    - X: np.ndarray
        2D array representing the X-coordinates of a meshgrid.
    - Y: np.ndarray
        2D array representing the Y-coordinates of a meshgrid.
    - title: str
        Title of the plot.
    - clr: str or tuple of floats, optional
        Color of the grid lines and corners (default: "black"). Accepts any 
        matplotlib-recognized color format.
    - lw: float, optional
        Line width for the internal grid lines (default: 1.0).
    - ls: str, optional
        Line style for the grid lines (default: "-").
    ----------------------------------------------------------------------------
    Returns:
    - None
        The function modifies the given axes object directly.
    ----------------------------------------------------------------------------
    """
    # Plot horizontal and vertical internal lines (thin)
    for i in range(1, Y.shape[0]-1):
        ax.plot(X[i, :], Y[i, :], color = dim_color(clr, 0.5), linewidth = lw, linestyle = ls)
    for j in range(1, X.shape[1]-1):
        ax.plot(X[:, j], Y[:, j], color = dim_color(clr, 0.5), linewidth = lw, linestyle = ls)
    
    # Plot the outer border (bolder)
    lw_new = 1.5*lw
    ax.plot(X[0, :], Y[0, :], color = clr, linewidth = lw_new, linestyle = ls)      # bottom
    ax.plot(X[-1, :], Y[-1, :], color = clr, linewidth = lw_new, linestyle = ls)    # top
    ax.plot(X[:, 0], Y[:, 0], color = clr, linewidth = lw_new, linestyle = ls)      # left
    ax.plot(X[:, -1], Y[:, -1], color = clr, linewidth = lw_new, linestyle = ls)    # right
    # Plot the corners
    corner_x = [X[0, 0], X[0, -1], X[-1, 0], X[-1, -1]]
    corner_y = [Y[0, 0], Y[0, -1], Y[-1, 0], Y[-1, -1]]
    ax.scatter(corner_x, corner_y, color = clr, zorder = 2)
    
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize = 10, weight="bold")

def apply_transformation(X: np.ndarray, Y: np.ndarray, 
                         T: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    ----------------------------------------------------------------------------
    Apply a 2x2 transformation matrix T to a 2D grid (X, Y).
    ----------------------------------------------------------------------------
    Parameters: 
    - X: np.ndarray
        2D array representing the X-coordinates of a meshgrid.
    - Y: np.ndarray
        2D array representing the Y-coordinates of a meshgrid.
    - T: np.ndarray
        2x2 transformation matrix.
    ----------------------------------------------------------------------------
    Returns:
    - X_new: np.ndarray
        Transformed X-coordinates (same shape as X).
    - Y_new: np.ndarray
        Transformed Y-coordinates (same shape as Y).
    """
    # Flattens X and Y arrays into 1D arrays, and then stack them in a matrix (2 x 2)
    coords = np.vstack([X.ravel(), Y.ravel()])
    # Multiply reference configuration by transformation matrix, obtaining transformed array
    transformed = T @ coords
    # Reshape flat 1D array back to a 2D grid, so it matches original meshgrid structure       
    X_new = transformed[0, :].reshape(X.shape)
    Y_new = transformed[1, :].reshape(Y.shape)
    
    return X_new, Y_new

def plot_comparison(ax: matplotlib.axes.Axes, X_original: np.ndarray, 
                    Y_original: np.ndarray, X: np.ndarray, Y: np.ndarray, 
                    title: str, 
                    clr_ref: Union[str, tuple[float, float, float]] = "black", 
                    clr_trans: Union[str, tuple[float, float, float]] = "red") -> None:
    """
    ----------------------------------------------------------------------------
    Plot a comparison between an original grid and a transformed grid.
    ----------------------------------------------------------------------------
    Parameters:
    - ax: matplotlib.axes.Axes
        Matplotlib axes object where the grids will be plotted.
    - X_original: np.ndarray
        2D array representing the X-coordinates of the reference meshgrid.
    - Y_original: np.ndarray
        2D array representing the Y-coordinates of the reference meshgrid.
    - X: np.ndarray
        2D array representing the X-coordinates of the transformed meshgrid.
    - Y: np.ndarray
        2D array representing the Y-coordinates of the transformed meshgrid.
    - title: str
        Title of the plot.
    - clr_ref: str or tuple of floats, optional
        Color for the reference grid (default: "black").
    - clr_trans: str or tuple of floats, optional
        Color for the transformed grid (default: "red").
    ----------------------------------------------------------------------------
    Returns:
    - None
        The function modifies the given axes object directly.
    ----------------------------------------------------------------------------
    """
    plot_grid(ax, X_original, Y_original, title, clr = clr_ref, ls = '--') 
    plot_grid(ax, X, Y, title, clr = clr_trans, ls = '-')   

if __name__ == "__main__":
    # --------------------------------------------------------------------------
    # Input
    # --------------------------------------------------------------------------
    save = True
    dpi = 600
    figname = "output.png"
    # --------------------------------------------------------------------------
    # Generate reference grid
    # --------------------------------------------------------------------------
    n = 5
    x = np.linspace(0, 1, n)
    y = np.linspace(0, 1, n)
    X, Y = np.meshgrid(x, y)
    # --------------------------------------------------------------------------
    # Define transformation matrices
    # --------------------------------------------------------------------------
    T_identity = np.eye(2)

    T_extension = np.array([[1.0 + 0.2, 0.0],
                            [0.0, 1.0]])

    T_compression = np.array([[0.8, 0.0],
                            [0.0, 1.0]])

    T_expansion = np.array([[1.2, 0.0],
                            [0.0, 1.2]])

    T_contraction = np.array([[0.8, 0.0],
                            [0.0, 0.8]])

    T_isochoric = np.array([[1*1.2,   0.0], 
                            [0.0, 1/1.2]])

    T_shear = np.array([[1.0, 0.2], 
                        [0.2, 1.0]])

    theta = np.pi/4.0
    T_rotation = np.array([[np.cos(theta), np.sin(theta)],
                        [-np.sin(theta), np.cos(theta)]])

    # --------------------------------------------------------------------------
    # Plot all cases
    # --------------------------------------------------------------------------
    fig, axs = plt.subplots(2, 4, figsize=(14, 6), layout="constrained")
    plot_grid(axs[0, 0], X, Y, "Reference")
    plot_comparison(axs[0, 1], X, Y, *apply_transformation(X, Y, T_extension), "Extension")
    plot_comparison(axs[0, 2], X, Y, *apply_transformation(X, Y, T_compression), "Compression")
    plot_comparison(axs[0, 3], X, Y, *apply_transformation(X, Y, T_expansion), title = "Expansion")
    plot_comparison(axs[1, 0], X, Y, *apply_transformation(X, Y, T_contraction), title = "Contraction")
    plot_comparison(axs[1, 1], X, Y, *apply_transformation(X, Y, T_isochoric), title = "Isochoric (Volume Conservation)")
    plot_comparison(axs[1, 2], X, Y, *apply_transformation(X, Y, T_shear), title = "Pure Shear")
    plot_comparison(axs[1, 3], X, Y, *apply_transformation(X, Y, T_rotation), title = "Rotation")

    if save == True:
        plt.savefig(figname, dpi = dpi)

    plt.show()