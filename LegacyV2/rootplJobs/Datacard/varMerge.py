import sys, os, subprocess
import commands
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread

print ( "\n ------------------------ \n  please remember to separate VH into WH and ZH \n ----------------------------- \n")


BaseDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplas_LegacyAll_SVATrig_20200122/"

years = ["2016","2017","2018"]
#years = ["2018"]

# currently implement only 2l region
Regions=["DiLepRegion"]

ignoredfiles = ["Data","Flips","Fakes","FakeSub"]

def checkdir(region, year):
    nomdir = BaseDir + "/Rootplas/" + region + "/" + year + "/" + region
    systdir = BaseDir + "/Rootplas/" + region + "/" + year + "/Syst_" + region
    vardir = BaseDir + "/Rootplas/" + region + "/" + year + "/Var_" + region
    return nomdir, systdir, vardir



for Region in Regions:
    for year in years:
        nomDir, systDir, varDir = checkdir(Region, year)

        if not os.path.exists(nomDir):
            print ("error : "+nomDir+ " deosn't exists")
            continue
        
        if not os.path.exists(systDir):
            print ("warning : "+systDir+" deosn't exists, copy "+nomDir+ " to "+varDir)
            copy_command = "cp -r %s %s"%(nomDir, varDir)
            print(copy_command)
            os.system(copy_command)
            continue
    
        if not os.path.exists(varDir):
            os.popen("mkdir -p "+varDir)
    
        checkfiles = [f for f in os.listdir(nomDir) if ".root" in f]
        for checkfile in checkfiles:
            filename = checkfile.split(".")[0]
            isskip = False
            for ignore in ignoredfiles:
                if ignore in checkfile:
                    print( " ignore file %s because it's not MC variations "%checkfile)
                    isskip = True
                    break
            if isskip: 
                copy_command = "cp %s/%s.root %s/%s.root"%(nomDir, filename, varDir, filename)
                print(copy_command)
                os.system(copy_command)
                continue
            merge_command = "hadd -f %s/%s.root %s/%s.root %s/%s*.root"%(varDir, filename, nomDir, filename, systDir, filename)
            print(merge_command)
            os.system(merge_command)
    

