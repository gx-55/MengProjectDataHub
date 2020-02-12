import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re
from matplotlib.ticker import FormatStrFormatter
import math
from extract_data import extract_key_value
import pathlib
import os
from mpl_toolkits.mplot3d import Axes3D
import plotly.express as px
import json
from google_sheet import googleSheetClient




class dataHub(object):
    def __init__(self,dictName, inputFileName, outPutFileName):
        self.curPath = str(pathlib.Path(__file__).parent.absolute())
        self.newDict = self.curPath + '/' +dictName
        if not os.path.exists(self.newDict):
            os.makedirs(self.newDict)
        self.client = googleSheetClient()
        self.inputFileName = inputFileName
        self.outPutFileName = self.newDict + '/' +outPutFileName
        self.df = pd.DataFrame()
        self.list_not_null = []
        self.list_is_null = []
        self.dicx = [0,6.5e7,7e7,7.8e7,8.6e7,9.4e7,10.2e7,11e7,11.8e7,12.6e7,13.4e7]
        self.dicy = [0, 6.2e7,6.9e7,7.6e7,8.3e7,9e7,9.7e7,10.4e7,11e7,11.6e7,12.2e7,12.8e7,13.5e7,14.2e7]
        self.count = 0
        self.newDf = pd.DataFrame()
    
    def extractData(self):
        outPutFileName = self.outPutFileName + '.txt'
        if os.path.exists(outPutFileName):
            os.remove(outPutFileName)
        extract_key_value(self.inputFileName,outPutFileName)

    def load(self):
        txt = pd.read_table(self.outPutFileName + '.txt', sep=",")
        tempFile = self.outPutFileName + '.csv'
        txt.to_csv(tempFile,index=False)
        data = pd.read_csv(tempFile, sep='\s*,\s*',header=0, encoding='ascii', engine='python')
        self.df = pd.DataFrame(data)
        return self.df
        
    def removeDefault(self):
        self.df = self.df[self.df["Stage X coordinate"] != 0]
        return self.df

    def __getMatrix(self):
        df = self.df
        dicx = self.dicx
        dicy = self.dicy
        i = 1
        while(i < len(dicx)):
            j = 1
            self.list_not_null.append([])
            self.list_is_null.append([])
            while(j < len(dicy)):
                self.list_not_null[i - 1].append(df
                            [df['Stage X coordinate'] < dicx[i]]
                            [ df['Stage Y coordinate'] < dicy[j]]
                            [dicx[i - 1] < df['Stage X coordinate']]
                            [dicy[j - 1] <df['Stage Y coordinate']]
                            [df['Measurement Method'] == 4]
                            )
                self.list_is_null[i - 1].append(df
                            [df['Stage X coordinate'] < dicx[i]]
                            [ df['Stage Y coordinate'] < dicy[j]]
                            [dicx[i - 1] < df['Stage X coordinate']]
                            [dicy[j - 1] <df['Stage Y coordinate']]
                            [df['Measurement Method'] == 0]
                            )
                j+=1
            i+=1
            
    def buildNewDf(self):
        self.__getMatrix()
        final_list = []
        wanted_W = []
        wanted_G = []
        count = 1500
        for i in range(6):

            for j in range(6):
                wanted_W.append(count)

            count += 500

        for i in range(6):
            count = 1500
            for j in range(6):
                wanted_G.append(count)
                count += 500
    
    

        df_w = pd.DataFrame(wanted_W)
        df_g = pd.DataFrame(wanted_G)
        
        list_is_null = self.list_is_null
        list_not_null = self.list_not_null
        col = []
        raw_data = {'0': [], '1': [], '2': [], '3': [],'4': []}
        nullColume = pd.DataFrame(raw_data)
        self.count = 0
        testFrames = []
        for i in range(10):
            testFrames.append([])
            for j in range(13):
                if list_is_null[i][j].shape == (0,11):
                    testFrame = pd.concat((list_is_null[i][j],nullColume),axis = 1)
                    new_columns = testFrame.columns.values;
                    new_columns[10] = 'Characteristic Value W'
                    new_columns[11] = 'Wanted Value W'
                    new_columns[12] = 'Abstraction in W'
                    new_columns[13] = 'Characteristic Value G'
                    new_columns[14] = 'Wanted Value G'
                    new_columns[15] = 'Abstraction in G'
                    testFrame.columns = new_columns
                    testFrames[i].append(testFrame)

                    continue
                list_is_null[i][j] = list_is_null[i][j].reset_index( drop=True)
                list_not_null[i][j] = list_not_null[i][j].reset_index( drop=True)
                testFrame = pd.concat((list_is_null[i][j],df_w,df_w[0] - list_is_null[i][j]["Characteristic value"],list_not_null[i][j]['Characteristic value'],df_g,df_g[0] - list_not_null[i][j]["Characteristic value"]),axis = 1)
                new_columns = testFrame.columns.values;
                new_columns[10] = 'Characteristic Value W'
                new_columns[11] = 'Wanted Value W'
                new_columns[12] = 'Abstraction in W'
                new_columns[13] = 'Characteristic Value G'
                new_columns[14] = 'Wanted Value G'
                new_columns[15] = 'Abstraction in G'
                testFrame.columns = new_columns
                testFrames[i].append(testFrame)
                self.count += 1
        temp = []
        newDf = pd.DataFrame(temp)
        for i in range(10):
            for j in range(13):
                newDf = pd.concat((newDf,testFrames[i][j]),axis = 0)

        newDf["Stage X coordinate"] = newDf["Stage X coordinate"].div(1e6)
        newDf["Stage Y coordinate"] = newDf["Stage Y coordinate"].div(1e6)
        newDf['Abstraction in W'] = newDf['Abstraction in W'].div(10)
        newDf['Abstraction in G'] = newDf['Abstraction in G'].div(10)
        self.newDf = newDf
        return newDf
    
    def getGroupNum(self):
        return self.count
    
    def get2DDistributionImage(self,imageName = None):
        newDf = self.newDf
        plt.figure(figsize=(13,10))
        plt.scatter(newDf['Stage X coordinate'], 
                    # defender size in year 298 as the y axis
                    newDf['Stage Y coordinate'], 
                    # the marker as

                    c = newDf['Abstraction in W'],
                    # the alpha
                    alpha=0.7,
                    # with size
                    s = 12,
                    # labelled this
                    label='Year 298')
        plt.colorbar()
        plt.scatter(newDf['Stage X coordinate'][ newDf['Abstraction in W'].abs() < 30], 
                    # defender size in year 298 as the y axis
                    newDf['Stage Y coordinate'][ newDf['Abstraction in W'].abs() < 30], 
                    # the marker as

                    color = 'r',
                    # the alpha
                    alpha=0.7,
                    # with size
                    s = 1,
                    # labelled this
                    label='Year 298')

        plt.xlim([min(newDf['Stage X coordinate'])-30, max(newDf['Stage X coordinate'])+30])
        plt.ylim([min(newDf['Stage Y coordinate'])-30, max(newDf['Stage Y coordinate'])+30])
        ax = plt.gca()

        #ax.yaxis.set_units(cm)
        circle1 = plt.Circle((100, 100), 60,fill=False)
        ax.add_artist(circle1)
        ax = plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d mm'))
        ax = plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%d mm'))
        if(imageName is None):
            imageName = self.outPutFileName + '_2D' + '.png'
        plt.savefig(imageName)
        return plt
    
    def get3DDistributionImage(self, imageName = None):
        fig = px.scatter_3d(self.newDf, x="Stage X coordinate", y='Stage Y coordinate', z='Abstraction in G',
              color='Abstraction in G')
        fig.show()
        if(imageName is None):
            imageName = self.outPutFileName + '_3D' + '.png'
        fig.write_image(imageName)

    def outputAsCsv(self):
        self.newDf.to_csv(self.outPutFileName+'_o'+'.csv', index = False)