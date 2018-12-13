# THIS CODE IS MY OWN WORK, IT WAS WRITTEN WITHOUT CONSULTING
# A TUTOR OR CODE WRITTEN BY OTHER STUDENTS - Jie Lin
# Python 3

#coding=utf-8
"""
@version: 1.0
@author: Jie Lin
@Mail: jlin246@emory.edu
@code environment: ubuntu 18.01
"""

import numpy as np      # Python package for number crunching/math
import pandas as pd     # Python package for data analysis - used widely in 
                        # Data Science
import matplotlib.pyplot as plt #Popular plotting/graphing library
from matplotlib import style
import sys

def noisyCount(sensitivety,epsilon):
    beta = sensitivety/epsilon
    u1 = np.random.random()
    u2 = np.random.random()
    if u1 <= 0.5:
        n_value = -beta*np.log(1.-u2)
    else:
        n_value = beta*np.log(u2)
    return n_value
 
def laplace_mech(data,sensitivety,epsilon):
    for i in range(len(data)):
        data[i] += noisyCount(sensitivety,epsilon)
    return data


def readData(file_dir):
	data = pd.read_csv(file_dir);
	dataDf = pd.DataFrame(data);
	return dataDf;

# perform random range queries over the three attributes
def sqlData(dataDf, age, gender, race):
	returnDf = dataDf[(dataDf.Age == age) & (dataDf.Gender == gender) & (dataDf.Race == race)];
	return returnDf;

#produce histograms and csv
def produceHistograms(dataDf, sensitivety, epsilon):
	for i in range(1,3):
		for j in range(1,6):
			tempData = dataDf[(dataDf.Gender == i) & (dataDf.Race == j)];

			# Histogram data can be created using the histogram() function in numpy  
			# np.histogram bins the data into 10 equal sized bins
			hist, binEdges = np.histogram(tempData['Age'])
			
			bins = np.arange(tempData.Age.min(), tempData.Age.max(), 1)
			n, bins, patches = plt.hist(x=tempData['Age'], bins = bins, color = 'steelblue', alpha = 0.7,rwidth=0.85)

			n = laplace_mech(n,sensitivety, epsilon);

			#Set up Fonts for the text on the plot
			font = {'family' : 'normal',
			    'weight' : 'bold',
			    'size'   : 24}
			plt.rc('font', **font)

			# the histogram set up by matplotlib can then be plotted
			plt.grid(axis='y', alpha=0.75)
			titleName = "gender == "+ str(i) + " race == "+str(j);
			plt.title(titleName);
			plt.xlabel('age')

			picName = "his_"+str(i)+"_"+str(j)+".png";
			plt.legend()
			plt.savefig(picName);
			#clear cache
			plt.show();
			file_name = "his_"+str(i)+"_"+str(j)+".csv";
			df = pd.DataFrame({'bin_leftedge': bins[:-1], 'count': n})
			df.to_csv(file_name, encoding='utf-8');

	print();
	print("histograms has been output to where the program is located")
	print("Synthetic datasets are created where the program is located")

#perform randome queries and calculate average relative error
def performRandomQueries(dataDf,numberQ):
	errorCumlate = 0;
	for i in range(numberQ):
		age = np.random.randint(low=17,high=91);
		gender = np.random.randint(low=1,high=3);
		race = np.random.randint(low=1,high=6);
		sqlLine ="SQL is: Select Count(*) where age in "+str(age)+" and gender = "+ str(gender)+" and race = "+str(race); 
		print(sqlLine);
		sqlDf = sqlData(dataDf, age, gender, race);
		numberOfOrgin = sqlDf.shape[0];
		readFileDir = file_name = "./his_"+str(gender)+"_"+str(race)+".csv";
		histo_df = readData(readFileDir);
		histo_filtered_df = histo_df[(histo_df.bin_leftedge == age)]
		if(histo_filtered_df.shape[0]!=0):
			print(histo_filtered_df);	
			numberOfFil = float(histo_filtered_df["count"]);
			errorCumlate=errorCumlate+numberOfOrgin-numberOfFil;
	averageError = errorCumlate/numberQ;
	result = "The average relative error is "+str(averageError);
	print(result);

def main_process(dataSet_dir,epsilon,numberQ):
	data = readData(dataSet_dir);
	produceHistograms(data,1,float(epsilon));
	performRandomQueries(data,int(numberQ));


if __name__ == '__main__':
	main_process(sys.argv[1],sys.argv[2],sys.argv[3]);
	