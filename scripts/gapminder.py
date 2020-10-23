import os
import glob
import numpy as np
import pandas as pd
import pylab as plt
import matplotlib.cm as cm
from matplotlib.ticker import FixedLocator, FixedFormatter
import matplotlib.pyplot as pyplot
import imageio


def cols_to_integers(fert_data, life_data, pop_data):
    """
    Take the column's name and turn it into integers that are then used
    as index for building up

    Parameters:
    ----------
    fert_data: data frame containing the information about fertility
    life_data: data frame containing the information about life expectancy
    pop_data: data frame containing the information about population sizes
    """
    ncol_life = [int(x) for x in life.columns]
    ncol_pop = [x for x in pop.columns]
    fert_data.set_axis(axis=1, labels=ncol_life, inplace=True)
    life_data.set_axis(axis=1, labels=ncol_life, inplace=True)
    pop_data.set_axis(axis=1, labels=ncol_pop, inplace=True)
    return fert_data, life_data, pop_data

def build_dataframe(fert_data, life_data, pop_data):
    """
    Creates hierarchichal indexes, and convert the multiple series's dataframes
    into one data frame

    Parameters:
    ----------
    fert_data: yearly indexed fertility data frame
    life_data: yearly indexed life expectancy data frame
    pop_data:  yearly indexed population sizes data frame
    """
    sfert = fert_data.stack()
    slife = life_data.stack()
    spop = pop_data.stack()
    dataframe = {'fertility':sfert, 'lifeExp':slife, 'growth':spop}
    dataframe = pd.DataFrame(data = dataframe).stack()
    return dataframe

def plot_lifeExpectancy(dataframe, ncountries):
    """
    Select and plot life expectancy for specific countries

    Parameters:
    ----------
    dataframe: dataframe containing the multiple series merged dataframe
    output by build_dataframe()
    ncountries: list with names of the countries to plot
    """
    dataframe = dataframe.unstack((0,2))
    dataframe = dataframe.drop(dataframe.index[0:150])
    subset = dataframe[ncountries]
    subset.plot(figsize = (14, 10))
    plt.title('Life expectancy and offspring changes in subset countries',
        fontsize=18, color = 'blue')
    plt.xlabel('Years', fontsize=14)
    plt.ylabel('Rate of change', fontsize=14)
    plt.tick_params(axis='x', labelsize=14)
    plt.tick_params(axis='y', labelsize=14)
    plt.legend( fontsize = 14)
    plt.savefig('../plots/LifeExpectancy.svg', format="svg")

def plot_lifeExp_fert(dataframe):
    """
    Plot scatterplot for life expectancy versus fetility for all years

    Parameters:
    ----------
    dataframe: dataframe containing the multiple series merged dataframe
    output by build_dataframe()
    """
    dataframe = dataframe.unstack(2)
    dataframe.plot.scatter('lifeExp', 'fertility', s=0.7, figsize=(14, 10),
                            color='red')
    plt.title('Life expectancy and offspring changes overtime',
             fontsize=18, color = 'blue')
    plt.xlabel('Life expectancy(Years)', fontsize=14)
    plt.ylabel('Number of children', fontsize=14)
    plt.tick_params(axis='x', labelsize=14)
    plt.tick_params(axis='y', labelsize=14)
    plt.savefig('../plots/LifeExpectancy_and_fertility.svg', format="svg")

def plot_lifeExp_fert_year(dataframe, year):
    """
    Plot scatterplot for life expectancy versus fetility for one year

    Parameters:
    ----------
    dataframe: dataframe containing the multiple series merged dataframe
    output by build_dataframe()
    year: year to be plotted
    """
    dataframe = dataframe.unstack(1)
    dataframe = dataframe[int(year)]
    dataframe = dataframe.unstack(1)
    dataframe.plot.scatter('lifeExp', 'fertility', s=0.7, figsize=(14, 10),
                            color='green')
    plt.title('Life expectancy and offspring changes in ' + str(year),
                fontsize=18, color = 'green' )
    plt.xlabel('Life expectancy(Years)', fontsize=14)
    plt.ylabel('Number of children', fontsize=14)
    plt.tick_params(axis='x', labelsize=14)
    plt.tick_params(axis='y', labelsize=14)
    plt.savefig('../plots/LifeExpectancy_and_fertility_' + str(year) + '.svg',
                format="svg")

def plot_one_year(dataframe, year, first, last):
    """
    Creates scatterplot for fetility versus life expectancy
    for a specific year between 1800 and 2015

    Parameters:
    ----------
    dataframe: dataframe containing the multiple series merged dataframe
    output by build_dataframe()
    first = first year to be selected
    last = last year to be selected
    """
    dataframe = dataframe.unstack(1)
    i = year
    size = dataframe['growth']/50000
    length = dataframe['lifeExp']
    colormap = plt.cm.gist_ncar # creating color map values
    colorst = [colormap(j) for j in np.linspace(0, 0.9,len(length))]
    dataframe.plot.scatter('lifeExp', 'fertility', s=size, figsize=(20, 14),
                            color=colorst, alpha = 0.4)
    plt.xlim(0, 90)
    plt.ylim(0, 10)
    name = 'Life expectancy versus offspring from '
    title = name + str(first) + ' to ' + str(last)
    plt.title(title,  fontsize=18, color = 'green')
    ax = plt.gca()
    plt.text(0.85, 0.85, i, horizontalalignment='center',
            verticalalignment='center', transform=ax.transAxes, fontsize= 80)
    plt.xlabel('Life Expectancy (Years)', fontsize=14)
    plt.ylabel('Number of Children', fontsize=14)
    plt.tick_params(axis='x', labelsize=14)
    plt.tick_params(axis='y', labelsize=14)
    name = 'lifExpec_' + str(i) + '.png'
    plt.savefig('../plots/'+ name, format="png")
    plt.close()

def multiple_scatterplots(dataframe, first, last):
    """
    Creates an animated scatterplot for fetility versus life expectancy
    from a range of years between 1800 and 2015

    Parameters:
    ----------
    dataframe: dataframe containing the multiple series merged dataframe
    output by build_dataframe()
    first = first year to be selected
    last = last year to be selected
    """
    dataframe = dataframe.loc[:,first:last]
    dataframe = dataframe.unstack(1)
    for i in range(int(first), int(last) + 1):
        dataframe_n = dataframe[i]
        plot_one_year(dataframe_n, i, first, last)


def generate_gif(first, last):
    """
    Generate an animated gif file by combining multiple nultiple_scatterplots
    """
    images = []
    for i in range(first, last + 1):
        filename = '../plots/lifExpec_{}.png'.format(i)
        images.append(imageio.imread(filename))
    imageio.mimsave('../plots/FertilityVsLifeExpectancy.gif', images, fps=5)
    files = glob.glob('../plots/*.png')
    for f in files:
        os.remove(f)


fert = pd.read_csv('../data/gapminder_total_fertility.csv')
fert = fert.set_index('Total fertility rate')

life = pd.read_excel('../data/gapminder_lifeexpectancy.xlsx')
life = life.set_index('Life expectancy').drop(labels=2016, axis=1)

pop = pd.read_excel('../data/gapminder_population.xlsx')
pop = pop.set_index('Total population')
countries = ['Germany', 'France', 'Sweden']

if __name__ == "__main__":
    fert, life, pop = cols_to_integers(fert, life, pop)
    data = build_dataframe(fert, life, pop)
    plot_lifeExpectancy(data, countries)
    plot_lifeExp_fert(data)
    plot_lifeExp_fert_year(data, 1950)
    multiple_scatterplots(data, 1960, 2015)
    generate_gif(1960, 2015)
