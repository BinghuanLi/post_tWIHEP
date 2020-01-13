import sys, os, subprocess
from threading import Thread
import ROOT
from ROOT import TFile


allMissedFile = open("allMissingFiles.sh","w")

allMissedFile.write("#!/bin/bash\n")


usePromptFake = False

samplesToCheck=[
]
dirsToCheck = [
#"ttH2L"
]

dirsToCheck = [f for f in os.listdir(".") if os.path.isdir(f)]

#dirsToCheck = ["tWSysts/","tW2j1tSysts/","tW3j2tSysts/","tW4j1tSysts/","tW4j2tSysts/"]

print dirsToCheck

ignoredDirs = [
#"ttHJESUp2L","ttHJESDown2L","ttH2L","ttHDatattZctrl3L","ttHttZctrl3L","ttHData2L","ttHttWctrl2L","ttHDatattWctrl2L",
]
skippedDirs = [
]
nErrorFiles = {}
totalResubmits = 0

#Regions=["SigRegion","ttWctrl","DiLepRegion"]
Regions=["DiLepRegion"]



def runDirCheck(dirToCheck):
    if dirToCheck in ignoredDirs:
        print "!!!!!!!!!!!!!!!!!!!! Ignore {0} directory manually !!!!!!!!!!!!!!!!!!!!!!!!!!!!".format(dirToCheck)
        return
    missedFile = open("missingFiles{0}.sh".format(dirToCheck),"w")
    missedFile.write("#!/bin/bash\n")
    if not os.path.isdir(dirToCheck):
        print "!!!!!!!!!!!!!!!!!!!! Skipping {0} directory which doesn't exist !!!!!!!!!!!!!!!!!!!!!!!!!!!!".format(dirToCheck)
        skippedDirs.append(dirToCheck)
        return
    print ">>>>>>>>>>>>>>>>> Executing over {0} directory <<<<<<<<<<<<<<<<".format(dirToCheck)
#    samplesToCheck = samples if not "Data" in dirToCheck else dataSamples
    nErrorFiles[dirToCheck] = 0
    samplesToCheck = [dirToCheck + "/" + f for f in os.listdir(dirToCheck) if os.path.isdir(dirToCheck + "/" + f)]
    isTrainMVA = False
    if "TrainMVA" in dirToCheck: isTrainMVA = True
    for sample in samplesToCheck:
        print "Sample: {0}".format(sample)
#        prefix = dirToCheck + "/" + sample
        prefix = sample
        if not os.path.isdir(prefix + "/logs/") : continue
        scriptFiles = [f for f in os.listdir(prefix+"/scripts/")]
        
        for scFile in scriptFiles:
            errorFile = prefix + "/logs/" + scFile.split(".")[0] + ".error"
            sampleName =  scFile.split(".")[0]
            files = [f for f in os.listdir(prefix + "/skims/") if sampleName in f]
            #print files
            hasSkimFile = True
            missFile =""
            process = sample.split("/")[1]
            for region in Regions:
                if (sampleName+"_"+region+".root") not in files: 
                    missFile = sampleName+"_"+region+".root"
                    hasSkimFile = False
                    continue
    
            #skimFile = prefix + "/skims/" + scFile.split(".")[0] + "Skim.root"
            #if not os.path.isfile(skimFile):
            #    print skimFile, " doesn't exists!"
            if not hasSkimFile:
                print missFile, "doesn't exists !"
                nErrorFiles[dirToCheck] += 1
                missedFile.write("hep_sub "+prefix+"/scripts/"+scFile+" -e "+errorFile.split(".sh")[0]+" -o "+errorFile.split(".error")[0]+".log\n")
                continue
            else:
                missFile = prefix + "/skims/"+sampleName+"_"+region+".root"
                inputfile = TFile(missFile,"read")
                if not inputfile.GetListOfKeys().Contains("syncTree"):
                    print (sampleName+"_"+region+".root", "syncTree deosn't exitst!") 
                    nErrorFiles[dirToCheck] += 1
                    missedFile.write("hep_sub "+prefix+"/scripts/"+scFile+" -e "+errorFile.split(".sh")[0]+" -o "+errorFile.split(".error")[0]+".log\n")
                    continue
                
            if not os.path.isfile(errorFile):
                print errorFile, "doesn't have a log file"
                nErrorFiles[dirToCheck] += 1
                missedFile.write("hep_sub "+prefix+"/scripts/"+scFile+" -e "+errorFile.split(".sh")[0]+" -o "+errorFile.split(".error")[0]+".log\n")
                continue
            if "Aborted" in open(errorFile).read() or "*** Break ***" in open(errorFile).read() or "invalid ELF header" in open(errorFile).read() or "aborted" in open(errorFile).read() or "No such file or directory" in open(errorFile).read():
                print errorFile
                nErrorFiles[dirToCheck] += 1
                missedFile.write("hep_sub "+prefix+"/scripts/"+scFile+" -e "+errorFile.split(".sh")[0]+" -o "+errorFile.split(".error")[0]+".log\n")
#                missedFile.write("hep_sub "+prefix+"/scripts/"+errorFile.split(".error")[0]+".sh  -e "+prefix+"/logs/"+errorFile.split(".error")[0]+".error -o "+prefix+"/logs/"+errorFile.split(".error")[0]+".log\n")
#                missedFile.write("condor_submit "+prefix + "/scripts/"+errorFile.split(".error")[0]+".submit -group cms -name job@schedd01.ac.cn\n")

if __name__ == "__main__":
    threads = {}
    for dirToCheck in dirsToCheck:
        print dirToCheck
        threads[dirToCheck] = Thread(target = runDirCheck, args = (dirToCheck,) )
        allMissedFile.write("bash missingFiles{0}.sh\n".format(dirToCheck))
        threads[dirToCheck].start()
    for key in threads.keys():
        threads[key].join()
        
print "Skipping the following directories: ", skippedDirs
for dirChecked in dirsToCheck:
    if dirChecked in nErrorFiles.keys(): print "There were {0} jobs to resubmit in {1} directory".format(nErrorFiles[dirChecked],dirChecked)
print "There were {0} error files".format(totalResubmits)
