import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread

# please run this file in the same directory you put the datacards

cwd = os.getcwd()

frameworkDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/combJobs/"
inputBaseDir = cwd 

'''
text2workspace.py ttH_DiLepRegion.txt -o ttH_DiLepRegion_3poi.root -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/TTW.*:r_ttW[1,0,6]' --PO 'map=.*/TTWW.*:r_ttW[1,0,6]' --PO 'map=.*/ttH.*:r_ttH[1,-1,3]' --PO 'map=.*/tH.*:r_tH[1,-1,3]'
combine -M AsymptoticLimits ttH_DiLepRegion_3poi.root -t -1 --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 -n 3poi -m 125 > ExpLimit_ttH_DiLepRegion_3poi_r_ttH_FloatOtherPOI.log
combine -M AsymptoticLimits ttH_DiLepRegion_3poi.root -t -1 --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 --freezeParameters r_ttW,r_tH -n 3poi -m 125 > ExpLimit_ttH_DiLepRegion_3poi_r_ttH_NoFloatOtherPOI.log
combine -M MultiDimFit ttH_DiLepRegion_3poi.root --algo singles --cl=0.68 -t -1 -P r_ttH --setParameters r_ttW=1,r_ttH=1,r_tH=1 --floatOtherPOI=1 --saveFitResult -n 3poi --saveWorkspace > ExpSigStrength_3poi_r_ttH_FloatOtherPOI.log
combine -M MultiDimFit ttH_DiLepRegion_3poi.root --algo singles --cl=0.68 -t -1 -P r_ttH --setParameters r_ttW=1,r_ttH=1,r_tH=1 --floatOtherPOI=0 --saveFitResult -n 3poi --saveWorkspace > ExpSigStrength_3poi_r_ttH_NoFloatOtherPOI.log
'''

floatOtherPOI = 0 # -1/0/1 ; 0: NoFloat, 1: Float, -1: Both
makeSigStrenght = True
makeLimit = True

# Set to False ATM if floatOtherPOI = -1 or 1
# Needs to figure out how to add r_ttW r_ttZ...
makeImpact = False
makeSignificance = False
impact = "estimateImpact_expected.sh"


dirsToCheck = [f for f in os.listdir(".") if os.path.isdir(f)]
dirsToIgnore = ["V0403_loose_PreProcess_datacards_None","V0403_loose_PreProcess_datacards_NoShape","V0403_loose_PreProcess_datacards_NoSyst","V0403_loose_PreProcess_datacards_NoStat"]

#Categories=["SubCat2l","DNNCat","DNNCat_option2","DNNCat_option3","DNNAMS2Cat1_option1","DNNAMS2Cat1_option2","DNNAMS2Cat1_option3","DNNAMS3Cat1_option1","DNNAMS3Cat1_option2","DNNAMS3Cat1_option3"]
Categories=["DNNSubCat2_option1"]
varPerCat={
"SubCat2l":["Bin2l"],
"DNNCat":["DNN_maxval"],
"DNNCat_option2":["DNN_maxval_option2"],
"DNNCat_option3":["DNN_maxval_option3"],
"DNNSubCat1_option1":["DNN_maxval"],
"DNNSubCat1_option2":["DNN_maxval_option2"],
"DNNSubCat1_option3":["DNN_maxval_option3"],
"DNNSubCat2_option1":["DNN_maxval"],
"DNNSubCat2_option2":["DNN_maxval_option2"],
"DNNSubCat2_option3":["DNN_maxval_option3"],
"DNNAMS2Cat1_option1":["DNN_maxval"],
"DNNAMS2Cat1_option2":["DNN_maxval_option2"],
"DNNAMS2Cat1_option3":["DNN_maxval_option3"],
"DNNAMS3Cat1_option1":["DNN_maxval"],
"DNNAMS3Cat1_option2":["DNN_maxval_option2"],
"DNNAMS3Cat1_option3":["DNN_maxval_option3"],
}

regPerCat={
"SubCat2l":["DiLepRegion"],
"DNNCat":["DiLepRegion"],
"DNNCat_option2":["2lss","ttWctrl"],
"DNNCat_option3":["2lss","ttWctrl"],
"DNNSubCat1_option1":["DiLepRegion"],
"DNNSubCat1_option2":["2lss","ttWctrl"],
"DNNSubCat1_option3":["2lss","ttWctrl"],
"DNNSubCat2_option1":["DiLepRegion"],
"DNNSubCat2_option2":["2lss","ttWctrl"],
"DNNSubCat2_option3":["2lss","ttWctrl"],
"DNNAMS2Cat1_option1":["2lss","ttWctrl"],
"DNNAMS2Cat1_option2":["2lss","ttWctrl"],
"DNNAMS2Cat1_option3":["2lss","ttWctrl"],
"DNNAMS3Cat1_option1":["2lss","ttWctrl"],
"DNNAMS3Cat1_option2":["2lss","ttWctrl"],
"DNNAMS3Cat1_option3":["2lss","ttWctrl"],
#"SubCat2l":["2lss"],
#"DNNCat":["2lss"],
#"DNNCat_option2":["2lss"],
#"DNNCat_option3":["2lss"],
#"DNNSubCat1_option1":["2lss"],
#"DNNSubCat1_option2":["2lss"],
#"DNNSubCat1_option3":["2lss"],
#"DNNSubCat2_option1":["2lss"],
#"DNNSubCat2_option2":["2lss"],
#"DNNSubCat2_option3":["2lss"],
#"DNNAMS2Cat1_option1":["2lss"],
#"DNNAMS2Cat1_option2":["2lss"],
#"DNNAMS2Cat1_option3":["2lss"],
#"DNNAMS3Cat1_option1":["2lss"],
#"DNNAMS3Cat1_option2":["2lss"],
#"DNNAMS3Cat1_option3":["2lss"],
}

subCats={
#"SubCat2l":["inclusive","ee_neg","ee_pos", "em_bl_neg","em_bl_pos","em_bt_neg","em_bt_pos", "mm_bl_neg","mm_bl_pos","mm_bt_neg","mm_bt_pos" ]
"SubCat2l":["ee_neg","ee_pos", "em_bl_neg","em_bl_pos","em_bt_neg","em_bt_pos", "mm_bl_neg","mm_bl_pos","mm_bt_neg","mm_bt_pos" ],
"DNNCat":["ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNCat_option2":["ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNCat_option3":["ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNSubCat1_option1":["ee_neg","ee_pos","em_ttHnode","em_ttJnode","em_ttWnode","em_ttZnode","mm_ttHnode","mm_ttJnode","mm_ttWnode","mm_ttZnode"],
"DNNSubCat1_option2":["ee_neg","ee_pos","em_ttHnode","em_ttJnode","em_ttWnode","em_ttZnode","mm_ttHnode","mm_ttJnode","mm_ttWnode","mm_ttZnode"],
"DNNSubCat1_option3":["ee_neg","ee_pos","em_ttHnode","em_ttJnode","em_ttWnode","em_ttZnode","mm_ttHnode","mm_ttJnode","mm_ttWnode","mm_ttZnode"],
"DNNSubCat2_option1":["ee_ttHnode","ee_ttJnode","ee_ttWnode","ee_ttZnode","em_ttHnode","em_ttJnode","em_ttWnode","em_ttZnode","mm_ttHnode","mm_ttJnode","mm_ttWnode","mm_ttZnode"],
"DNNSubCat2_option2":["ee_ttHnode","ee_ttJnode","ee_ttWnode","ee_ttZnode","em_ttHnode","em_ttJnode","em_ttWnode","em_ttZnode","mm_ttHnode","mm_ttJnode","mm_ttWnode","mm_ttZnode"],
"DNNSubCat2_option3":["ee_ttHnode","ee_ttJnode","ee_ttWnode","ee_ttZnode","em_ttHnode","em_ttJnode","em_ttWnode","em_ttZnode","mm_ttHnode","mm_ttJnode","mm_ttWnode","mm_ttZnode"],
"DNNAMS2Cat1_option1":["loose_ttHnode","tight_ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNAMS2Cat1_option2":["loose_ttHnode","tight_ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNAMS2Cat1_option3":["loose_ttHnode","tight_ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNAMS3Cat1_option1":["loose_ttHnode","tight_ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNAMS3Cat1_option2":["loose_ttHnode","tight_ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNAMS3Cat1_option3":["loose_ttHnode","tight_ttHnode","ttJnode","ttWnode","ttZnode"],
}

def prepareCshJob(shFile,category, dirName):
    subFile      = file(shFile,"w")
    print >> subFile, "#!/bin/bash"
    print >> subFile, "/bin/hostname"
    print >> subFile, "gcc -v"
    print >> subFile, "pwd"
    print >> subFile, "cd "+dirName+"/"
    print >> subFile, "eval `scramv1 runtime -sh`"
    SystFix =""
    if "None" in dirName:
        SystFix = " -S 0 "
    datacardName = "ttH"
    combineCards = "combineCards.py"
    for region in regPerCat[category]:
        datacardName += ("_"+region)
        for subCat in subCats[category]:
            count = 0
            datacard = open(dirName+"/ttH_"+region+"_"+subCat+".txt",'r').read()
            count = datacard.count("ttH_"+region+"_"+subCat)
            if count <3: continue
            combineCards += (" ttH_"+region+"_"+subCat+"=ttH_"+region+"_"+subCat+".txt")
    combineCards += (" > "+datacardName+".txt")
    print >> subFile, combineCards
    convertCards =  "text2workspace.py {}.txt -o {}_3poi.root -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/TTW.*:r_ttW[1,0,6]' --PO 'map=.*/TTWW.*:r_ttW[1,0,6]' --PO 'map=.*/ttH.*:r_ttH[1,-1,3]' --PO 'map=.*/tH.*:r_tH[1,-1,3]'".format(datacardName,datacardName)
    print >> subFile, convertCards
    
    
    if makeLimit:
        ExpLimit_Float = "combine -M AsymptoticLimits "+datacardName + "_3poi.root -t -1 -m 125 -n 3poi_FloatOtherPOI --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 "+SystFix+" > ExpLimit_"+datacardName+"_3poi_FloatOtherPOI.log"
        ExpLimit_NoFloat = "combine -M AsymptoticLimits "+datacardName + "_3poi.root -t -1 -m 125 -n 3poi_NoFloatOtherPOI --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 --freezeParameters r_ttW,r_tH"+SystFix+" > ExpLimit_"+datacardName+"_3poi_NoFloatOtherPOI.log"
        if floatOtherPOI == -1:
            print >> subFile, ExpLimit_Float
            print >> subFile, ExpLimit_NoFloat
        elif floatOtherPOI == 0:
            print >> subFile, ExpLimit_NoFloat
        elif floatOtherPOI == 1:
            print >> subFile, ExpLimit_Float
    if makeSigStrenght:
        ExpSig_Float = "combine -M MultiDimFit --saveFitResult --saveWorkspace --algo signles --cl=0.68 -t -1 -P r_ttH --setParameters r_ttW=1,r_ttH=1,r_tH=1 --floatOtherPOI=1 -d "+datacardName + "_3poi.root -m 125 -n 3poi_FloatOtherPOI "+SystFix+"> ExpSigStrength_"+datacardName+"_3poi_FloatOtherPOI.log"
        ExpSig_NoFloat = "combine -M MultiDimFit --saveFitResult --saveWorkspace --algo signles --cl=0.68 -t -1 -P r_ttH --setParameters r_ttW=1,r_ttH=1,r_tH=1 --floatOtherPOI=0 -d "+datacardName + "_3poi.root -m 125 -n 3poi_NoFloatOtherPOI "+SystFix+"> ExpSigStrength_"+datacardName+"_3poi_NoFloatOtherPOI.log"
        if floatOtherPOI == -1:
            print >> subFile, ExpSig_Float
            print >> subFile, ExpSig_NoFloat
        elif floatOtherPOI == 0:
            print >> subFile, ExpSig_NoFloat
        elif floatOtherPOI == 1:
            print >> subFile, ExpSig_Float
    if makeSignificance:
        ExpSignific = "combine -M Significance "+datacardName + ".txt --expectSignal=1 -t -1 -m 125 "+SystFix+"> ExpSignificance_"+datacardName+".log"
        print >> subFile, ExpSignific
    if makeImpact:
        ExpImpact = "./"+impact+" "+datacardName 
        print >> subFile, ExpImpact
    subprocess.call("chmod 777 "+shFile, shell=True)

allJobFile = 0
if os.path.exists(os.getcwd()+"/all.sh"):
    allJobFile = open(os.getcwd()+"/all.sh","a")
else:
    allJobFile = open(os.getcwd()+"/all.sh","w")
    allJobFile.write("#!/bin/bash\n")


for dirToCheck in dirsToCheck:
  if dirToCheck in dirsToIgnore: continue
  for category in Categories:
    for var in varPerCat[category]:
        fix =""
        for regionName in regPerCat[category]:
            fix += ("_"+regionName)
        DirName_datacard = inputBaseDir+"/"+dirToCheck+"/"+category+"/"+var
        shFileName = DirName_datacard + "/Fit_"+category+"_"+var+fix+"_Job.sh"
        logFileName = DirName_datacard + "/Fit_"+category+"_"+var+fix+"_Job.log"
        errorFileName = DirName_datacard + "/Fit_"+category+"_"+var+fix+"_Job.error"
        prepareCshJob(shFileName, category, DirName_datacard)
        command_cp = "cp "+frameworkDir+impact+" "+DirName_datacard
        print(command_cp)
        os.system(command_cp)
        print >> allJobFile, "hep_sub "+ shFileName + " -o "+logFileName+ " -e "+errorFileName

allJobFile.close()
print "Finished " 
