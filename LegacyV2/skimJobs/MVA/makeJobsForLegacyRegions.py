#Make the job folders for all of the regions we want to study for the tW lepton+jets

import subprocess

baseDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/tWIHEPFramework/"

for i in ["2017"]:#,"2018"]:
    #for k in ["isSigExt","isDNN","isData","isHjtagger"]:
    #for k in ["isDNN","isHjtagger"]:
    for k in ["isDNN"]:
         #for j in ["nominal","JESUp","JESDown","JERUp","JERDown"]:
         for j in ["nominal"]:
            #for l in ["2","3","4"]:
            for l in ["2"]:
                optstring = "-s %s -j %s -y %s -n %s"%(k,j,i,l)
                print "python "+baseDir+"utils/makeHEPSubmitLegacy.py "+optstring
                subprocess.call( "python "+baseDir+"utils/makeHEPSubmitLegacy.py "+optstring, shell=True)

