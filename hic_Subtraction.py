# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 11:29:04 2019
@author: yyzou
this script to get the subtraction of two hic matrix
input : .cool file with a certain resolution
---------
"""

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import cooler
import click
import os
from os.path import exists
from math import log


def read_in(file_path):
    return cooler.Cooler(file_path)


"""
  get matrix data then calculate input1 - input2
  normalized by log10() with positive and negative signs unchanged
"""


def get_Subtraction(c1, c2, area_s, area_e):
    mat1 = (
        c1.matrix(balance=False, sparse=True)[area_s:area_e, area_s:area_e]
    ).toarray()
    mat2 = (
        c2.matrix(balance=False, sparse=True)[area_s:area_e, area_s:area_e]
    ).toarray()
    # print(mat1.sum(), mat2.sum())
    arr1 = (mat1 / mat1.sum()) * (mat1.sum() + mat2.sum())
    arr2 = (mat2 / mat2.sum()) * (mat1.sum() + mat2.sum())
    # arr1 = np.log(arr1, out=np.zeros_like(arr1), where=(arr1!=0))
    # arr2 = np.log(arr2, out=np.zeros_like(arr2), where=(arr2!=0))
    arr_sub = np.divide(arr1, arr2, out=np.zeros_like(arr2), where=(arr2 != 0))
    # print(np.min(arr_sub), np.max(arr_sub), len(arr_sub), np.mean(arr1), np.mean(arr2))
    # arr_list = np.array([[x*log(x+1 if x>=0 else -x+1,10)/(abs(x)+1) for x in row ] for row in arr_sub])
    # arr_list1 = np.array([[x*log(x+1 if x>=0 else -x+1,10)/(abs(x)+1) for x in row ] for row in arr1])
    # arr_list2 = np.array([[x*log(x+1 if x>=0 else -x+1,10)/(abs(x)+1) for x in row ] for row in arr2])
    arr_list = arr_sub
    arr_list1 = arr1
    arr_list2 = arr2
    arr = arr_list.reshape(arr_list.shape[0], arr_list.shape[1])
    arr1 = arr_list1.reshape(arr_list1.shape[0], arr_list1.shape[1])
    arr2 = arr_list2.reshape(arr_list2.shape[0], arr_list2.shape[1])
    return arr, arr1, arr2


def get_fig(data, data1, data2, area_s, area_e, outdir, outfig):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    im = ax.matshow(
        np.log(data, out=np.zeros_like(data), where=(data != 0)),
        cmap="seismic",
        interpolation="none",
        vmin=-0.5,
        vmax=0.5,
    )  ## vmin vmax determin the range of colorbar

    fig.colorbar(im)
    if outfig[:-4] == ".png":
        fig.savefig(outdir + outfig, dpi=300)
    else:
        fig.savefig(outdir + outfig)
    plt.clf()

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    im = ax.matshow(
        np.log(data1, out=np.zeros_like(data1), where=(data1 != 0)),
        cmap="inferno_r",
        interpolation="none",
    )  ## vmin vmax determine colorbar range
    fig.colorbar(im)
    fig.savefig(outdir + outfig + "_mat1.png", dpi=300)
    plt.clf()

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    im = ax.matshow(
        np.log(data2, out=np.zeros_like(data2), where=(data2 != 0)),
        cmap="inferno_r",
        interpolation="none",
    )  # vmin vmax determine colorbar range
    fig.colorbar(im)
    fig.savefig(outdir + outfig + "_mat2.png", dpi=300)
    plt.clf()


def process(input1, input2, area_s, area_e, outdir, outfig):
    c1 = read_in(input1)
    c2 = read_in(input2)
    arr, arr1, arr2 = get_Subtraction(c1, c2, area_s, area_e)
    get_fig(arr, arr1, arr2, area_s, area_e, outdir, outfig)


@click.command(name="hic_Subtraction")
@click.argument("input1")
@click.argument("input2")
@click.option("area_s", "-s", default=0, help="comparasion starts area")
@click.option("area_e", "-e", default=None, help="comparasion starts area")
@click.option("--outdir", "-O", default="./", help="path to output files.")
@click.option("--outfig", "-fig", default="test.png", help="name of output figure.")
def main_(input1, input2, area_s, area_e, outdir, outfig):
    if not exists(outdir):
        os.mkdir(outdir)
    process(input1, input2, int(area_s), int(area_e), outdir, outfig)


if __name__ == "__main__":
    main_()
