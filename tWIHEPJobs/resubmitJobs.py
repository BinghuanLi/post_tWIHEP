import sys, os, subprocess
from threading import Thread

samples=[
"qcd1000_1500",
"qcd100_200",
"qcd1500_2000",
"qcd2000_inf",
"qcd200_300",
"qcd300_500",
"qcd500_700",
"qcd700_1000",
"sChan",
"tChan_top",
"tChan_antitop",
"ttbar",
"ttbarBU",
"tW_top",
"tW_antitop",
"ww",
"wz",
"zz",
"zPlusJetsLowMass",
"zPlusJetsHighMass",
"wPlusJetsMCatNLO",
"tW_top_nfh",
"tW_antitop_nfh"
]

dataSamples=[
"SingMuB",
"SingMuC",
"SingMuD",
"SingMuE",
"SingMuF",
"SingMuG",
"SingMuH"
]

samplesSyst = [
"tW_antitop_DS",
"tW_antitop_isrup",
"tW_antitop_isrdown",
"tW_antitop_fsrup",
"tW_antitop_fsrdown",
"tW_antitop_herwig",
"tW_antitop_MEup",
"tW_antitop_MEdown",
"tW_antitop_PSup",
"tW_antitop_PSdown",
"tW_top_DS",
"tW_top_isrup",
"tW_top_isrdown",
"tW_top_fsrup",
"tW_top_fsrdown",
"tW_top_herwig",
"tW_top_MEup",
"tW_top_MEdown",
"tW_top_PSup",
"tW_top_PSdown",
"ttbar_isrup",
"ttbar_isrdown",
"ttbar_fsrup",
"ttbar_fsrdown",
"ttbar_tuneup",
"ttbar_tunedown",
"ttbar_herwig",
"ttbar_amcatnlo",
"ttbar_hdampup",
"ttbar_hdampdown"
]

samplesDataMuEle=[
"MuEleGmRecoverB1","MuEleGmRecoverC1","MuEleGmRecoverD1","MuEleGmRecoverE1","MuEleGmRecoverF1","MuEleGmRecoverF2","MuEleGmRecoverG1","MuEleGmRecoverH1","MuEleGmRecoverH2",
"SEleRecoverB1","SEleRecoverC1","SEleRecoverD1","SEleRecoverE1","SEleRecoverF1","SEleRecoverF2","SEleRecoverG1","SEleRecoverH1",
"SMuRecoverB1","SMuRecoverC1","SMuRecoverD1","SMuRecoverE1","SMuRecoverF1","SMuRecoverF2","SMuRecoverG1","SMuRecoverH1","SMuRecoverH2",
"MuEleGmB1","MuEleGmC1","MuEleGmD1","MuEleGmE1","MuEleGmF1","MuEleGmF2","MuEleGmG1","MuEleGmH1","MuEleGmH2",
"SEleB1","SEleC1","SEleD1","SEleE1","SEleF1","SEleF2","SEleG1","SEleH1","SEleH2",
"SMuB1","SMuC1","SMuD1","SMuE1","SMuF1","SMuF2","SMuG1","SMuH1","SMuH2"
]

samplesDataDiMu=[
"DMuRecoverB1","DMuRecoverC1","DMuRecoverD1","DMuRecoverE1","DMuRecoverF1","DMuRecoverF2","DMuRecoverG1","DMuRecoverH1","DMuRecoverH2",
"SEleRecoverB1","SEleRecoverC1","SEleRecoverD1","SEleRecoverE1","SEleRecoverF1","SEleRecoverF2","SEleRecoverG1","SEleRecoverH1",
"SMuRecoverB1","SMuRecoverC1","SMuRecoverD1","SMuRecoverE1","SMuRecoverF1","SMuRecoverF2","SMuRecoverG1","SMuRecoverH1","SMuRecoverH2",
"DMuB1","DMuC1","DMuD1","DMuE1","DMuF1","DMuF2","DMuG1","DMuH1","DMuH2",
"SEleB1","SEleC1","SEleD1","SEleE1","SEleF1","SEleF2","SEleG1","SEleH1","SEleH2",
"SMuB1","SMuC1","SMuD1","SMuE1","SMuF1","SMuF2","SMuG1","SMuH1","SMuH2"
]

samplesDataDiEle=[
"DEleGmRecoverB1","DEleGmRecoverC1","DEleGmRecoverD1","DEleGmRecoverE1","DEleGmRecoverF1","DEleGmRecoverF2","DEleGmRecoverG1","DEleGmRecoverH1","DEleGmRecoverH2",
"SEleRecoverB1","SEleRecoverC1","SEleRecoverD1","SEleRecoverE1","SEleRecoverF1","SEleRecoverF2","SEleRecoverG1","SEleRecoverH1",
"SMuRecoverB1","SMuRecoverC1","SMuRecoverD1","SMuRecoverE1","SMuRecoverF1","SMuRecoverF2","SMuRecoverG1","SMuRecoverH1","SMuRecoverH2",
"DEleGmB1","DEleGmC1","DEleGmD1","DEleGmE1","DEleGmF1","DEleGmF2","DEleGmG1","DEleGmH1","DEleGmH2",
"SEleB1","SEleC1","SEleD1","SEleE1","SEleF1","SEleF2","SEleG1","SEleH1","SEleH2",
"SMuB1","SMuC1","SMuD1","SMuE1","SMuF1","SMuF2","SMuG1","SMuH1","SMuH2"
]

nJobs = {
"qcd1000_1500":13,
"qcd100_200":193,
"qcd1500_2000":10,
"qcd2000_inf":6,
"qcd200_300":46,
"qcd300_500":50,
"qcd500_700":48,
"qcd700_1000":36,
"sChan":3,
"tChan":48,
"ttbar":242,

"tW_top":3,
"tW_antitop":3,
"wPlusJets":115,
"ww":3,
"wz":3,
"zz":3,
"zPlusJetsLowMass":76,
"zPlusJetsHighMass":69,
"wPlusJetsMCatNLO":60,
"tW_top_nfh":20,
"tW_antitop_nfh":10,
"SingMuB":174,
"SingMuC":58,
"SingMuD":98,
"SingMuE":83,
"SingMuF":61,
"SingMuG":132,
"SingMuH":147
}

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

samplesToCheck=[
"TT_PSwgt_ToSemiLep",
]
#dirsToCheck = [
#"ttH2LAllJESUp"
#]

dirsToCheck = [f for f in os.listdir(".") if os.path.isdir(f)]

#dirsToCheck = ["tWSysts/","tW2j1tSysts/","tW3j2tSysts/","tW4j1tSysts/","tW4j2tSysts/"]

print dirsToCheck

ignoredDirs = [
#"ttHData2LAll2L"
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
    #samplesToCheck = [dirToCheck+"/TTHnobb"]
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
