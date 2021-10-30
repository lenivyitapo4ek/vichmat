{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 217,
   "id": "6ef02642",
   "metadata": {},
   "outputs": [],
   "source": [
    "import csv\n",
    "from os import mkdir\n",
    "from os.path import isdir, join as join_path\n",
    "from functools import partial\n",
    "from warnings import filterwarnings\n",
    "\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "from mpl_toolkits.mplot3d import Axes3D"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 218,
   "id": "fdb5d95c",
   "metadata": {},
   "outputs": [],
   "source": [
    "with open('Atmosphere_1.csv') as f:\n",
    "    reader = csv.reader(f)\n",
    "    #print(list(reader))\n",
    "    x_str, y_str = [], []\n",
    "    x, y = [], []\n",
    "    headers = next(reader)\n",
    "    for row in reader:\n",
    "        #print(row)\n",
    "        x_str.append(row[0])\n",
    "        y_str.append(row[1])\n",
    "    #print (x_str)\n",
    "    for elem in x_str:\n",
    "        x.append(float(elem))\n",
    "    for elem in y_str:\n",
    "        y.append(float(elem))\n",
    "    #print (y)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 219,
   "id": "a177b0b7",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "449"
      ]
     },
     "execution_count": 219,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "len(y)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 220,
   "id": "3dc53149",
   "metadata": {},
   "outputs": [],
   "source": [
    "a = y\n",
    "h=x[3]-x[2]\n",
    "u = [((a[i] - a[i - 1]) / h) for i in range(1, len(y))] # разности ньютона\n",
    "u2 = [12 * (u[i - 1] - u[i - 2]) / (2 * h) for i in range(2, len(y))] # подсчет столбца d в уравнении А*С = d"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 221,
   "id": "06f0d5a0",
   "metadata": {},
   "outputs": [],
   "source": [
    "#коэффициенты прогоночного уравнения:\n",
    "\n",
    "n = 0.5\n",
    "l = 0.5\n",
    "m = 2\n",
    "\n",
    "p, q =[0]*len(u2), [0]*len(u2)\n",
    "\n",
    "p[1] = n/m\n",
    "q[1] = u2[0] / m\n",
    "\n",
    "for i in range(1, len(u2)-2, 1):\n",
    "    p[i + 1] = -n / (l * p[i] + m)\n",
    "    q[i + 1] = (u2[i] - l * q[i]) / (l * p[i] + m)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 222,
   "id": "a579aadc",
   "metadata": {},
   "outputs": [],
   "source": [
    "# подсчет коэф с\n",
    "\n",
    "c = [0]*len(u2)\n",
    "c[len(u2)-1] = (u2[len(u2)-2] - q[len(u2)-1] * l) / (l * p[len(u2)-1] + m)\n",
    "\n",
    "for i in range(len(u2)-2, 1, -1):\n",
    "    c[i] = p[i] * c[i + 1] + q[i]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 223,
   "id": "47e56b52",
   "metadata": {},
   "outputs": [],
   "source": [
    "b, d = [0]*len(u2), [0]*len(u2)\n",
    "\n",
    "# подсчет коэф b\n",
    "for i in range(1, len(u2)):\n",
    "    b[i] = c[i] * h / 3 + c[i - 1] * h / 6 + u[i - 1]\n",
    "\n",
    "# подсчет коэф d\n",
    "for i in range(1, len(u2)):\n",
    "    d[i] = (c[i] - c[i - 1]) / h"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 224,
   "id": "bb100008",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "#построение графика\n",
    "plt.figure()\n",
    "for i in range(1, 10):\n",
    "    t = np.linspace(x[i - 1], x[i], 100)\n",
    "    plt.plot(t, a[i] + b[i] * (t - x[i]) + (c[i] * (t - x[i]) ** 2) / 2 + (d[i] / 6) * (t - x[i]) ** 3)\n",
    "plt.show()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
