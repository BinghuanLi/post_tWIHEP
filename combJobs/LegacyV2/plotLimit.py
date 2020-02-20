import sys
import argparse
import os
from ROOT import gROOT, TFile
import numpy as np
from matplotlib import pyplot as plt

gROOT.SetBatch(1)

inputbasedir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/CombineStuff/CMSSW_8_1_0/src/HiggsAnalysis/SM_2lss_0tau_V1110_OptBIN/"
outputbasedir = inputbasedir + "/plots"
year = 2018

if not os.path.exists(outputbasedir):
    print ('mkdir: ', outputbasedir)
    os.makedirs(outputbasedir)


DNN_labels={
"DNNSubCat2_option1":{"keyname":"DNNSubCat2","variable":"DNNSubCat2_nBin","cat":["ee_ttHnode","ee_Restnode","ee_ttWnode","ee_tHQnode","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"],"nbins":[x for x in range(2,20)]}
}

def parseName(dirname):
    label = "test"
    if "ttHnode_nBin" in dirname:
        label = "4poi_ttHnode"
    elif "Restnode_nBin" in dirname:
        label = "4poi_Restnode"
    elif "tHQnode_nBin" in dirname:
        label = "4poi_tHQnode"
    elif "ttWnode_nBin" in dirname:
        label = "4poi_ttWnode"
    filename = "higgsCombine%s.AsymptoticLimits.mH125.root"%label
    return filename


def readlimit(filename, QT = 0.5):
    # qt should be 0.025, 0.160, 0.500, 0.840, 0.975 , -1
    tf = TFile(filename, "r")
    tree = tf.Get("limit")
    limit = -1 
    for event in tree:
        if abs(event.quantileExpected - QT) < 0.01:
            limit = event.limit
    tf.Close()
    return limit


def plot_1D_limit(plotname, category, nbins):
    print ( " plot %s %s"%(plotname, category))
    limits = []
    for nbin in nbins:
        dirName = "%s/%s_%s_nBin%i_SM_2lss_0tau"%(inputbasedir, plotname, category, nbin)
        filename = parseName(dirName)
        limit = readlimit("%s/results/%i/%s"%(dirName,year,filename))
        limits.append(limit)
        print (" nbin %i , limit %f"%(nbin, limit))
         
    xbins = np.array(nbins)
    ylimit = np.array(limits)
    
    fig, ax = plt.subplots(figsize=(6,6))
    ax.plot(xbins, ylimit, lw=1, label='%s_%s_limit0p5'%(plotname, category), marker = 'o')
    
    ax.set_ylabel("limit")
    ax.set_xlabel("nBins")
    ax.legend()
    ax.grid()
    fig.savefig("%s/%s_%s_%i_limit0p5.png"%(outputbasedir, plotname,category, year))
    fig.savefig("%s/%s_%s_%i_limit0p5.pdf"%(outputbasedir,plotname,category, year))
    print ("save figure")
    plt.close()

if __name__ == "__main__":
    for key, value in DNN_labels.items():
        for subcat in value["cat"]:
            plot_1D_limit(value["keyname"], subcat, value["nbins"])






        
