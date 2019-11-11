import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread


allMissedFile = open("allMissingFiles.sh","w")

allMissedFile.write("#!/bin/bash\n")


CheckMerged = True # true to check "merged*.root"

samplesConv = [
"TTGToJets_ext1","WGToLNuG_ext2","TGJets_v1","WGToLNuG_ext1","ZGTo2LG","TGJets_ext1"
]

dirsToCheck = [
#"ttH2L",
]

dirsToCheck = [f for f in os.listdir(".") if os.path.isdir(f)]

#dirsToCheck = ["tWSysts/","tW2j1tSysts/","tW3j2tSysts/","tW4j1tSysts/","tW4j2tSysts/"]
#dirsToCheck = ["ttH2LAll2L","ttH2LAllJESUp","ttH2LAllJESDown"]

print dirsToCheck

# skip null files for skim merge
threshold = 20000
Thresh_Entry = 25000 # for files with size (threshold, Tresh_Entry), check the number of entries of the root file

ignoredDirs = [
#"ttH","ttHMuEleJERUp","ttHMuEleJERDown","ttHMuEleJESUp","ttHMuEleJESDown",
#"ttHMuEleJERUpConv","ttHMuEleJERDownConv","ttHMuEleJESUpConv","ttHMuEleJESDownConv",
#"ttHTrainMVA2L","ttHlepSB2L","ttHttWctrl2L","ttHttZctrl3L"
#"ttHData2L","ttHfake2L","ttHDatalepSB2L","ttHDatattWctrl2L",
#"ttHDatattZctrl3L","ttHfakesttWctrl2L","ttHfakesttZctrl3L",
#"ttHflips2L","ttHflipsttWctrl2L",
"Rootplas"
]
skippedDirs = []
nErrorFiles = {}
totalResubmits = 0

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
    if "Syst" in dirToCheck: samplesToCheck = samplesSyst
    if "Conv" in dirToCheck: samplesToCheck = samplesConv
    #if "MuEle" in dirToCheck: samplesToCheck = samplesDataMuEle
    #if "DiMu" in dirToCheck: samplesToCheck = samplesDataDiMu
    #if "DiEle" in dirToCheck: samplesToCheck = samplesDataDiEle
    samplesToCheck = [dirToCheck + "/" + f for f in os.listdir(dirToCheck) if os.path.isdir(dirToCheck + "/" + f)]
    #samplesToCheck = ["WZTo3LNu","THQ","THW"]
    for sample in samplesToCheck:
        if "Inv" in dirToCheck and not "Data" in dirToCheck: continue
        print "Sample: {0}".format(sample)
#        prefix = dirToCheck + "/" + sample
        prefix = sample
        if not os.path.isdir(prefix + "/logs/") : continue
        skimFiles = []
        if CheckMerged:
            skimFiles = [f for f in os.listdir(prefix+"/skims/") if "root" in f and "merge" in f]
        else:
            skimFiles = [f for f in os.listdir(prefix+"/skims/") if "root" in f and "merge" not in f]
#        print skimFiles
        
        os.popen('mkdir -p '+prefix+"/skims/null/")
        for skimFile in skimFiles:
            if "Legacy18V1_TTJets_TToSingleLep23" in skimFile:
                print (skimFile, threshold)
            if os.path.getsize(prefix+'/skims/'+skimFile) < threshold:
                os.popen('mv '+prefix+'/skims/'+skimFile+' '+prefix+"/skims/null/")
                print skimFile, " smaller than "+str(threshold)+ " !"
                continue
#                missedFile.write("hep_sub "+prefix+"/scripts/"+errorFile.split(".error")[0]+".sh  -e "+prefix+"/logs/"+errorFile.split(".error")[0]+".error -o "+prefix+"/logs/"+errorFile.split(".error")[0]+".log\n")
#                missedFile.write("condor_submit "+prefix + "/scripts/"+errorFile.split(".error")[0]+".submit -group cms -name job@schedd01.ac.cn\n")
            elif os.path.getsize(prefix+'/skims/'+skimFile) < Thresh_Entry:
                inputfile = TFile.Open(prefix+'/skims/'+skimFile,"read")
                tree = inputfile.Get("syncTree")
                entry = tree.GetEntries()
                inputfile.Close()
                if(entry == 0):
                    os.popen('mv '+prefix+'/skims/'+skimFile+' '+prefix+"/skims/null/")
                    print skimFile, " number of tree entries is 0 !"


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
