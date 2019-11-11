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

frameworkDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/varJobs/"
inputBaseDir = cwd + "/Raw"
outputBaseDir = cwd + "/Rootplas" 

#dirsToChecks = ["SigRegion","JESUpSigRegion","JESDownSigRegion","ttWctrl","JESUpttWctrl","JESDownttWctrl"]
dirsToChecks = ["DiLepRegion","JESUpDiLepRegion","JESDownDiLepRegion"]
#dirsToChecks = ["SigRegion","ttWctrl"]
DNNSig = True
SaveROOT = True

BinDir = "BinData_SigDNN"
if not DNNSig : BinDir = "BinData_SigTTH"

executable =  "BinOptimizer.C"

def prepareCshJob(shFile,region):
    subFile      = file(shFile,"w")
    print >> subFile, "#!/bin/bash"
    print >> subFile, "/bin/hostname"
    print >> subFile, "source /cvmfs/sft.cern.ch/lcg/views/LCG_93/x86_64-slc6-gcc62-opt/setup.sh"
    print >> subFile, "gcc -v"
    print >> subFile, "pwd"
    command_run = "root -l -b -q "+frameworkDir+executable+"'"+'("'+inputBaseDir+'","'+outputBaseDir+'","'+region+'",'+str(DNNSig).lower()+","+str(SaveROOT).lower()+")'"
    print >> subFile, command_run 
    subprocess.call("chmod 777 "+shFile, shell=True)


if not os.path.exists("Rootplas"):
        os.popen("mkdir Rootplas")
if not os.path.exists("Rootplas"+BinDir):
        os.popen("mkdir -p Rootplas/"+BinDir)

allJobFile = 0
if os.path.exists(os.getcwd()+"/all.sh"):
    allJobFile = open(os.getcwd()+"/all.sh","a")
else:
    allJobFile = open(os.getcwd()+"/all.sh","w")
    allJobFile.write("#!/bin/bash\n")

for dirToCheck in dirsToChecks:
    # one job for one dir ~ 20 mins
    if not os.path.exists(outputBaseDir+"/"+dirToCheck):
        os.popen("mkdir -p "+outputBaseDir+"/"+dirToCheck)
    shFileName = outputBaseDir + "/" + dirToCheck + "/" +dirToCheck+"Job.sh"
    logFileName = outputBaseDir + "/" + dirToCheck + "/" +dirToCheck+"Job.log"
    errorFileName = outputBaseDir + "/" + dirToCheck + "/" +dirToCheck+"Job.error"
    prepareCshJob(shFileName, dirToCheck)
    print >> allJobFile, "hep_sub "+ shFileName + " -o "+logFileName+ " -e "+errorFileName

allJobFile.close()
print "Finished " 
 
