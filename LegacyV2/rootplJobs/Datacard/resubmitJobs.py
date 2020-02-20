import sys, os, subprocess
from threading import Thread
import ROOT
from ROOT import TFile


allMissedFile = open("allMissingFiles.sh","w")

allMissedFile.write("#!/bin/bash\n")

usePromptFake = False
Regions=["DiLepRegion"]#"TriLepRegion","QuaLepRegion","ttZctrl","WZctrl","QuaLepRegion","ZZctrl"]
Selections=["datafakes", "dataflips", "prompt", "fakesub", "dataobs", "conv"]

variations = ["JESUp","JESDown","JERUp","JERDown","MetShiftUp","MetShiftDown"]


samplesConv = [
# 2016
'Legacy16V2_TTGJets_v1', 'Legacy16V2_TTGJets_ext', 'Legacy16V2_TGJetsLep', 'Legacy16V2_WZG','Legacy16V2_ZGToLLG','Legacy16V2_WGToLNuG_01J', 
#'Legacy16V2_WGToLNuG_ext1', 'Legacy16V2_WGToLNuG_ext2', 'Legacy16V2_WGToLNuG_ext3', 'Legacy16V2_DYJets_M10to50', 'Legacy16V2_DYJets_M50', 
#"Legacy16V2_W1JetsToLNu", "Legacy16V2_W2JetsToLNu_v1", "Legacy16V2_W2JetsToLNu_ext", "Legacy16V2_W3JetsToLNu_v1", "Legacy16V2_W3JetsToLNu_ext", "Legacy16V2_W4JetsToLNu_v1","Legacy16V2_W4JetsToLNu_ext", 
# 2017
"Legacy17V2_TTGJets_v1","Legacy17V2_TTGJets_ext","Legacy17V2_TGJetsLep","Legacy17V2_WZG", "Legacy17V2_ZGToLLG_01J","Legacy17V2_WGToLNuG_01J",
#"Legacy17V2_WGToLNuG_Tune", "Legacy17V2_W1JetsToLNu","Legacy17V2_W2JetsToLNu","Legacy17V2_W3JetsToLNu","Legacy17V2_W4JetsToLNu","Legacy17V2_DYJets_M10to50_v1","Legacy17V2_DYJets_M10to50_ext","Legacy17V2_DYJets_M50_v1","Legacy17V2_DYJets_M50_ext",
# 2018
"Legacy18V2_TTGJets","Legacy18V2_TGJetsLep", "Legacy18V2_ZGToLLG_01J", "Legacy18V2_WZG", "Legacy18V2_WGToLNuG_01J",
#"Legacy18V2_WGToLNuG_Tune",
#"Legacy18V2_W1JetsToLNu","Legacy18V2_W2JetsToLNu","Legacy18V2_W3JetsToLNu","Legacy18V2_W4JetsToLNu","Legacy18V2_DYJets_M10to50","Legacy18V2_DYJets_M50_v1","Legacy18V2_DYJets_M50_ext",
]


inputBaseDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/skims_LegacyAll_20200111/"
outputBaseDir =  "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplas_LegacyAll_SVATrig_20200122/"


samplesToCheck=[
]
dirsToCheck = [
#"ttH2L"
]

dirsToCheck = [f for f in os.listdir(".") if os.path.isdir(f)]

#dirsToCheck = ["ttH2018All2L"]

print dirsToCheck

ignoredDirs = [
"Rootplas",
]
skippedDirs = [
]
nErrorFiles = {}
totalResubmits = 0




def runDirCheck(dirToCheck):
    isVars = False
    varName = ""
    for var in variations:
        if var in dirToCheck:
            isVars = True
            varName = dirToCheck.split("SR2L")[1]
            break
    treeName = "syncTree"+varName
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
    #samplesToCheck = ["WZTo3LNu","THQ","THW"]
    for sample in samplesToCheck:
        print "Sample: {0}".format(sample)
#        prefix = dirToCheck + "/" + sample
        prefix = sample
        if not os.path.isdir(prefix + "/logs/") : continue
        scFile = prefix+".sh"
        infiles = [f for f in os.listdir(inputBaseDir + prefix + "/skims/") if sample.split("/")[1] in f]
        #print(infiles) 
        for infile in infiles:
            errorFile = prefix + "/logs/" + sample.split("/")[1] + ".error"
            sampleName =  infile.split("Skim")[0]
            files = [f for f in os.listdir(prefix + "/skims/") if sampleName in f]
            #print files
            hasSkimFile = True
            isZombieFile = False
            missFile =""
            zombieFile = ""
            process = sample.split("/")[1]
            print( "check file " + infile)
            for region in Regions:
                if "DiLepRegion" in region and "2L" not in dirToCheck:
                    continue
                if ("TriLepRegion" in region or "WZctrl" in region or "ttZctrl" in region) and "3L" not in dirToCheck:
                    continue
                if ("QuaLepRegion" in region or "ZZctrl" in region) and "4L" not in dirToCheck:
                    continue
                for selection in Selections:
                    if isVars and selection not in ["conv","prompt"]:
                        #print ("skip for MC vars excpet conv and prompt ")
                        continue
                    if "Block" not in dirToCheck and "data"in selection:
                        continue
                    if "Block" in process and not "data"in selection:
                        #print ("skip mcMatch for data ")
                        continue
                    if "2L" not in dirToCheck and "flips"in selection:
                        continue
                    if selection == "conv" and process not in samplesConv:
                        continue
                    if (sampleName + "_"+selection+"_"+region+".root") not in files:
                        missFile = sampleName+"_"+selection+"_"+region+".root"
                        hasSkimFile = False
                        continue
                    else:
                        missFile = prefix + "/skims/"+sampleName+"_"+selection+"_"+region+".root"
                        #print("check root file ", missFile)
                        inputfile = TFile(missFile,"read")
                        if not inputfile.GetListOfKeys().Contains(treeName):
                            isZombieFile = True
                            zombieFile = missFile
                            continue
                if isZombieFile or not hasSkimFile: break
                 

            #skimFile = prefix + "/skims/" + scFile.split(".")[0] + "Skim.root"
            #if not os.path.isfile(skimFile):
            #    print skimFile, " doesn't exists!"
            if not hasSkimFile:
                print missFile, "doesn't exists !"
                nErrorFiles[dirToCheck] += 1
                missedFile.write("hep_sub "+prefix+"/scripts/"+sample.split("/")[1] + ".sh -e "+errorFile.split(".sh")[0]+" -o "+errorFile.split(".error")[0]+".log\n")
                break
            elif isZombieFile:
                print (zombieFile, treeName + " deosn't exitst!") 
                nErrorFiles[dirToCheck] += 1
                missedFile.write("hep_sub "+prefix+"/scripts/"+sample.split("/")[1] + ".sh -e "+errorFile.split(".sh")[0]+" -o "+errorFile.split(".error")[0]+".log\n")
                break
                
            if not os.path.isfile(errorFile):
                print errorFile, "doesn't have a log file"
                nErrorFiles[dirToCheck] += 1
                missedFile.write("hep_sub "+prefix+"/scripts/"+sample.split("/")[1] + ".sh -e "+errorFile.split(".sh")[0]+" -o "+errorFile.split(".error")[0]+".log\n")
                break
            #if "Aborted" in open(errorFile).read() or "*** Break ***" in open(errorFile).read() or "invalid ELF header" in open(errorFile).read() or "aborted" in open(errorFile).read() or "No such file or directory" in open(errorFile).read():
            if "Aborted" in open(errorFile).read() or "*** Break ***" in open(errorFile).read() or "invalid ELF header" in open(errorFile).read() or "aborted" in open(errorFile).read() or "No such file or directory" in open(errorFile).read(): 
                print errorFile
                nErrorFiles[dirToCheck] += 1
                missedFile.write("hep_sub "+prefix+"/scripts/"+sample.split("/")[1] + ".sh -e "+errorFile.split(".sh")[0]+" -o "+errorFile.split(".error")[0]+".log\n")
                break
#                missedFile.write("hep_sub "+prefix+"/scripts/"+errorFile.split(".error")[0]+".sh  -e "+prefix+"/logs/"+errorFile.split(".error")[0]+".error -o "+prefix+"/logs/"+errorFile.split(".error")[0]+".log\n")
#                missedFile.write("condor_submit "+prefix + "/scripts/"+errorFile.split(".error")[0]+".submit -group cms -name job@schedd01.ac.cn\n")

if __name__ == "__main__":
    threads = {}
    for dirToCheck in dirsToCheck:
        if dirToCheck in ignoredDirs:
            print "!!!!!!!!!!!!!!!!!!!! Ignore {0} directory manually !!!!!!!!!!!!!!!!!!!!!!!!!!!!".format(dirToCheck)
            continue
        print dirToCheck
        threads[dirToCheck] = Thread(target = runDirCheck, args = (dirToCheck,) )
        allMissedFile.write("bash missingFiles{0}.sh\n".format(dirToCheck))
        threads[dirToCheck].start()
    for key in threads.keys():
        threads[key].join()
        
print "Skipping the following directories: ", skippedDirs
for dirChecked in dirsToCheck:
    if dirChecked in nErrorFiles.keys(): 
        print "There were {0} jobs to resubmit in {1} directory".format(nErrorFiles[dirChecked],dirChecked)
        totalResubmits += nErrorFiles[dirChecked]
        
print "There were {0} error files".format(totalResubmits)
