import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread

# please run this file in the same directory you put the datacards

cwd = os.getcwd()

frameworkDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/combJobs/"
inputBaseDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/mvaTool_LegacyAll_20191025_v2/" 

'''
text2workspace.py ttH_DiLepRegion.txt -o ttH_DiLepRegion_3poi.root -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/TTW.*:r_ttW[1,0,6]' --PO 'map=.*/TTWW.*:r_ttW[1,0,6]' --PO 'map=.*/ttH.*:r_ttH[1,-1,3]' --PO 'map=.*/tH.*:r_tH[1,-1,3]'
combine -M AsymptoticLimits ttH_DiLepRegion_3poi.root -t -1 --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 -n 3poi -m 125 > ExpLimit_ttH_DiLepRegion_3poi_r_ttH_FloatOtherPOI.log
combine -M AsymptoticLimits ttH_DiLepRegion_3poi.root -t -1 --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 --freezeParameters r_ttW,r_tH -n 3poi -m 125 > ExpLimit_ttH_DiLepRegion_3poi_r_ttH_NoFloatOtherPOI.log
combine -M MultiDimFit ttH_DiLepRegion_3poi.root --algo singles --cl=0.68 -t -1 -P r_ttH --setParameters r_ttW=1,r_ttH=1,r_tH=1 --floatOtherPOI=1 --saveFitResult -n 3poi --saveWorkspace > ExpSigStrength_3poi_r_ttH_FloatOtherPOI.log
combine -M MultiDimFit ttH_DiLepRegion_3poi.root --algo singles --cl=0.68 -t -1 -P r_ttH --setParameters r_ttW=1,r_ttH=1,r_tH=1 --floatOtherPOI=0 --saveFitResult -n 3poi --saveWorkspace > ExpSigStrength_3poi_r_ttH_NoFloatOtherPOI.log
'''

systs_ctcvcp = [
"kt_m3_kv_1","kt_m2_kv_1","kt_m1p5_kv_1","kt_m1p25_kv_1","kt_m0p75_kv_1","kt_m0p5_kv_1","kt_m0p25_kv_1","kt_0_kv_1","kt_0p25_kv_1","kt_0p5_kv_1","kt_0p75_kv_1","kt_1_kv_1","kt_1p25_kv_1","kt_1p5_kv_1","kt_2_kv_1","kt_3_kv_1","kt_m2_kv_1p5","kt_m1p5_kv_1p5","kt_m1p25_kv_1p5","kt_m1_kv_1p5","kt_m0p5_kv_1p5","kt_m0p25_kv_1p5","kt_0p25_kv_1p5","kt_0p5_kv_1p5","kt_1_kv_1p5","kt_1p25_kv_1p5","kt_m3_kv_0p5","kt_m2_kv_0p5","kt_m1p25_kv_0p5","kt_1p25_kv_0p5","kt_2_kv_0p5","kt_3_kv_0p5",
#"cosa_m0p9","cosa_m0p8","cosa_m0p7","cosa_m0p6","cosa_m0p5","cosa_m0p4","cosa_m0p3","cosa_m0p2","cosa_m0p1","cosa_mp0","cosa_0p1","cosa_0p2","cosa_0p3","cosa_0p4","cosa_0p5","cosa_0p6","cosa_0p7","cosa_0p8","cosa_0p9"
]

dirsToIgnore = []

years = [2016,2017,2018]
#years = [2016]

ToCopy = True 
makeCTCV_card = True

datacardBaseName = "datacard"
tHqBaseName = "tHq"

datacard_labels={
#"DNN":[{"region":"DiLepRegion","label":"DNNSubCat2_option1","variable":"DNN_maxval","cat":["ee_ttHnode","ee_Restnode","ee_ttWnode","ee_tHQnode","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"]}],
"BDT":[{"region":"DiLepRegion","label":"SubCat2l","variable":"Bin2l","cat":["ee_neg","ee_pos", "em_bl_neg","em_bl_pos","em_bt_neg","em_bt_pos", "mm_bl_neg","mm_bl_pos","mm_bt_neg","mm_bt_pos"]}],
}

def makecards(syst_ctcv, tocopy, name):
  for key, values in datacard_labels.items():
    DirName_datacard_All = "%s/%s_RunII_datacards_All/RunII"%(cwd,key)
    if not os.path.exists(DirName_datacard_All):
        os.popen("mkdir -p "+DirName_datacard_All)
    combineCards_All = "combineCards.py"
    datacardName = name + "_DiLepRegion" + syst_ctcv+ ".txt"
    if "tHq" in datacardName:
        datacardName = name + "_DiLepRegion" + syst_ctcv+ "_card.txt"
    for year in years:
        DirName_datacard = "%s/%s_RunII_datacards_All/%s"%(cwd,key,year)
        if not os.path.exists(DirName_datacard):
            os.popen("mkdir -p "+DirName_datacard)
        os.chdir(DirName_datacard)
        
        combineCards = "combineCards.py"
        # loope over regions:
        for value in values:
            region = value["region"]
            label = value["label"]
            variable = value["variable"]
            categories = value["cat"]
            if ( tocopy ) :
                inputdirs = "%s%s_RunII_%i_V1025.1_datacards_All/%s/%s/"%(inputBaseDir,region,year,label,variable)
                command_cp = "cp %s/* ."%(inputdirs)
                print(command_cp)
                os.system(command_cp)
            for subCat in categories:
                count = 0
                datacard = open(name+"_"+region+"_"+subCat+syst_ctcv+".txt",'r').read()
                count = datacard.count(name+"_"+region+"_"+subCat)
                if count <3: continue
                combineCards += (" "+name+"_"+region+"_"+subCat+"="+name+"_"+region+"_"+subCat+syst_ctcv+".txt")
        
        combineCards += (" > "+datacardName)
        combineCards_All += (" %s_%i=../%i/%s"%(name,year,year,datacardName))
        print(combineCards)
        os.system(combineCards)
    os.chdir(DirName_datacard_All)
    combineCards_All += (" > "+datacardName)  
    print(combineCards_All)
    os.system(combineCards_All)
  
  os.chdir(cwd)
  return

if makeCTCV_card:
    n= 0
    for systs_ctcv in systs_ctcvcp:
        systs_ctcv = "_"+systs_ctcv        
        if ToCopy and n == 0:
            makecards(systs_ctcv, True, tHqBaseName)
        else:
            makecards(systs_ctcv, False, tHqBaseName)
        n += 1
    ToCopy = False

makecards("", ToCopy, datacardBaseName)

print "Finished " 
