# encoding:utf-8
#
import matplotlib.pyplot as plt
import numpy as np


def scatterplot(x_data, y_data, x_label="", y_label="", title="", color="r", yscale_log=False):
    # Create the plot object
    _, ax = plt.subplots()  # Plot the data, set the size (s), color and transparency (alpha)
    # of the points
    ax.scatter(x_data, y_data, s=10, color=color, alpha=0.75)
    if yscale_log == True:
        ax.set_yscale('log')  # Label the axes and provide a title
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.show()


def lineplot(x_data, y_data, x_label="", y_label="", title=""):
    # Create the plot object
    _, ax = plt.subplots()  # Plot the best fit line, set the linewidth (lw), color and
    # transparency (alpha) of the line
    ax.plot(x_data, y_data, lw=2, color='#539caf', alpha=1)  # Label the axes and provide a title
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.show()


def histogram(data, n_bins, cumulative=False, x_label="", y_label="", title=""):
    _, ax = plt.subplots()
    ax.hist(data, n_bins=n_bins, cumulative=cumulative, color='#539caf')
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
def ttt():
    import simpleflow as sf
    # Create a graph
    with sf.Graph().as_default():
        a = sf.constant(1.0, name='a')
        b = sf.constant(2.0, name='b')
        result = sf.add(a, b, name='result')
        # Create a session to compute
        with tf.Session() as sess:
            print(sess.run(result))

# scatterplot([1, 2], [3, 6])

X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
C, S = np.cos(X), np.sin(X)
# lineplot(X, C)
# scatterplot(X, S)
histogram(X, S)
