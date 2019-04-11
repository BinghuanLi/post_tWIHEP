import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread

#####
##   Parameters to be specified by the user
#####
# rootplas are saved as inputBaseDir/regionName/(JESUp/Down)regionName/process_(JESUp/Down)regionName.root
# please move rootplas from inputBaseDir/regionName/(JESUp/Down)regionName to inputBaseDir/(JESUp/Down)regionName

cwd = os.getcwd()

inputBaseDir =  "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplasDNN_20190409/"
outputBaseDir = cwd + "/Raw" 

dirsToChecks = ["SigRegion","JESUpSigRegion","JESDownSigRegion","ttWctrl","JESUpttWctrl","JESDownttWctrl"]
inputDirs = {
"SigRegion":"2019-04-09_newvars_loose_loose",
"JESUpSigRegion":"2019-04-09_newvars_loose_loose_JESUp",
"JESDownSigRegion":"2019-04-09_newvars_loose_loose_JESDown",
"ttWctrl":"2019-04-09_ttWctrl_newvars_loose_loose",
"JESUpttWctrl":"2019-04-09_ttWctrl_newvars_loose_loose_JESUp",
"JESDownttWctrl":"2019-04-09_ttWctrl_newvars_loose_loose_JESDown"
}


for dirToCheck in dirsToChecks:
    if not os.path.exists(outputBaseDir+"/"+dirToCheck):
        os.popen("mkdir -p "+outputBaseDir+"/"+dirToCheck)
    command_mv = "mv "+inputBaseDir+inputDirs[dirToCheck]+"/*.root " + outputBaseDir+"/"+dirToCheck
    print(command_mv)
    os.system(command_mv)

print "Finished " 
 
