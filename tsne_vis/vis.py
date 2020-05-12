import numpy as np
import sklearn
from sklearn.manifold import TSNE
import pickle as pkl
from sklearn.datasets import load_digits

import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import matplotlib

# Random state.
RS = 20200512

# We import seaborn to make nice plots.
import seaborn as sns

sns.set_style('darkgrid')
sns.set_palette('muted')
sns.set_context("notebook", font_scale=1.5,
                rc={"lines.linewidth": 2.5})


def scatter(x, colors):
    class_num = np.max(colors) + 1
    # We choose a color palette with seaborn.
    palette = np.array(sns.color_palette("hls", class_num))
    # palette = np.array(sns.color_palette("husl", class_num))

    # We create a scatter plot.
    f = plt.figure(figsize=(8, 8))
    ax = plt.subplot(aspect='equal')
    sc = ax.scatter(x[:, 0], x[:, 1], lw=0, s=40,
                    # marker='o', edgecolors='w',
                    c=palette[colors.astype(np.int)])
    plt.xlim(-25, 25)
    plt.ylim(-25, 25)
    ax.axis('off')
    ax.axis('tight')

    # # We add the labels for each digit.
    # txts = []
    # for i in range(10):
    #     # Position of each label.
    #     xtext, ytext = np.median(x[colors == i, :], axis=0)
    #     txt = ax.text(xtext, ytext, str(i), fontsize=24)
    #     txt.set_path_effects([
    #         PathEffects.Stroke(linewidth=5, foreground="w"),
    #         PathEffects.Normal()])
    #     txts.append(txt)

    # return f, ax, sc, txts


if __name__ == '__main__':
    # digits = load_digits()
    # # We first reorder the data points according to the handwritten numbers.
    # X = np.vstack([digits.data[digits.target == i]
    #                for i in range(10)])
    # y = np.hstack([digits.target[digits.target == i]
    #                for i in range(10)])

    fts_dir = 'C:\\Users\\yifan\\Desktop\\PAMI_v3\\fts\\sun2012_gin.pkl'
    with open(fts_dir, 'rb') as fp:
        fts = pkl.load(fp)
    X = fts['fts']
    y = np.argmax(fts['preds'], axis=1)

    digits_proj = TSNE(random_state=RS).fit_transform(X)
    scatter(digits_proj, y)
    # plt.savefig('digits_tsne-generated.png', dpi=120)
    plt.show()
