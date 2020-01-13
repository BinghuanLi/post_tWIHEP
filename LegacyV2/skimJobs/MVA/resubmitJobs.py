import sys, os, subprocess
from threading import Thread
import ROOT
from ROOT import TFile

allMissedFile = open("allMissingFiles.sh","w")
allMissedFile.write("#!/bin/bash\n")


samples94XMC = [
"TTHnobb", "ttH_powheg_ToNonbb", "TTWToLNu", "TTW_PSwgt_ToLNu", "TTZToLLNuNu_M10", "TTZToLL_M1to10", "TTWW", "DY_M10to50", "DY_M50", "DY_ext_M50", "WJets", "WWTo2L2Nu", "WZTo3LNu", "ZZTo4L", "ZZ_ext_To4L", "TT_PSwgt_To2L2Nu", "TTTo2L2Nu", "TT_PSwgt_ToSemiLep", "TTToSemiLep", "TT_PSwgt_ToHadron", "TTToHadron", "ST_tW_top", "ST_tW_antitop", "STt_top", "STt_antitop", "STs", "TTGJets", "tZq","WW_DS_To2L2Nu", "WWW", "WWZ", "WZZ", "ZZZ", "TTTT_Tune"
]

samples94XData = [
"SEleBlockB", "SEleBlockC", "SEleBlockD", "SEleBlockE", "SEleBlockF", "SMuBlockB", "SMuBlockC", "SMuBlockD", "SMuBlockE", "SMuBlockF", "DblEGBlockB", "DblEGBlockC", "DblEGBlockD", "DblEGBlockE", "DblEGBlockF", "DblMuBlockB", "DblMuBlockC", "DblMuBlockD", "DblMuBlockE", "DblMuBlockF", "MuEGBlockB", "MuEGBlockC", "MuEGBlockD", "MuEGBlockE", "MuEGBlockF",
]
samplesConv = [
"TTGToJets_ext1","WGToLNuG_ext2","TGJets_v1","WGToLNuG_ext1","ZGTo2LG","TGJets_ext1"
]

mysamplesToCheck=[
"DYJetsToLL_M4to50_HT600toInf","TTH_ctcvcp"
]
#dirsToCheck = [
#"ttH2LAllJESUp"
#]

dirsToCheck = [f for f in os.listdir(".") if os.path.isdir(f)]

#dirsToCheck = ["tWSysts/","tW2j1tSysts/","tW3j2tSysts/","tW4j1tSysts/","tW4j2tSysts/"]

print dirsToCheck

ignoredDirs = [
"ttHData2LAll2L"
#"ttHJESUp2L","ttHJESDown2L","ttH2L","ttHDatattZctrl3L","ttHttZctrl3L","ttHData2L","ttHttWctrl2L","ttHDatattWctrl2L",
]
skippedDirs = [
]
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
    if "Data" in dirToCheck or "flips" in dirToCheck or "fakes" in dirToCheck: samplesToCheck = samples94XData
    #if "DiMu" in dirToCheck: samplesToCheck = samplesDataDiMu
    #if "DiEle" in dirToCheck: samplesToCheck = samplesDataDiEle
    nErrorFiles[dirToCheck] = 0
    samplesToCheck = [dirToCheck + "/" + f for f in os.listdir(dirToCheck) if os.path.isdir(dirToCheck + "/" + f)]
    #samplesToCheck = [dirToCheck + "/" + f for f in mysamplesToCheck]
    for sample in samplesToCheck:
        if "Inv" in dirToCheck and not "Data" in dirToCheck: continue
        print "Sample: {0}".format(sample)
#        prefix = dirToCheck + "/" + sample
        prefix = sample
        if not os.path.isdir(prefix + "/logs/") : continue
        scriptFiles = [f for f in os.listdir(prefix+"/scripts/")]
        
        files = [f for f in os.listdir(prefix + "/logs/") if "error" in f]
        for scFile in scriptFiles:
            errorFile = prefix + "/logs/" + scFile.split(".")[0] + ".error"
            skimFile = prefix + "/skims/" + scFile.split(".")[0] + "Skim.root"
            if not os.path.isfile(skimFile):
                print skimFile, " doesn't exists!"
                nErrorFiles[dirToCheck] += 1
                missedFile.write("hep_sub "+prefix+"/scripts/"+scFile+" -e "+errorFile.split(".sh")[0]+" -o "+errorFile.split(".error")[0]+".log\n")
                continue
            else:
                inputfile = TFile(skimFile,"read")
                myDir = inputfile.Get("TNT")
                if not myDir.GetListOfKeys().Contains("BOOM"):
                    print (skimFile, "TNT/BOOM deosn't exitst!") 
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
