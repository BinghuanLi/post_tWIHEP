import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread

# please run this file in the same directory you put the datacards

cwd = os.getcwd()

frameworkDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/combJobs/"
inputBaseDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/mvaTool_LegacyAll_SVATrig_20200122/"

'''
text2workspace.py ttH_DiLepRegion.txt -o ttH_DiLepRegion_3poi.root -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/TTW.*:r_ttW[1,0,6]' --PO 'map=.*/TTWW.*:r_ttW[1,0,6]' --PO 'map=.*/ttH.*:r_ttH[1,-1,3]' --PO 'map=.*/tH.*:r_tH[1,-1,3]'
combine -M AsymptoticLimits ttH_DiLepRegion_3poi.root -t -1 --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 -n 3poi -m 125 > ExpLimit_ttH_DiLepRegion_3poi_r_ttH_FloatOtherPOI.log
combine -M AsymptoticLimits ttH_DiLepRegion_3poi.root -t -1 --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 --freezeParameters r_ttW,r_tH -n 3poi -m 125 > ExpLimit_ttH_DiLepRegion_3poi_r_ttH_NoFloatOtherPOI.log
combine -M MultiDimFit ttH_DiLepRegion_3poi.root --algo singles --cl=0.68 -t -1 -P r_ttH --setParameters r_ttW=1,r_ttH=1,r_tH=1 --floatOtherPOI=1 --saveFitResult -n 3poi --saveWorkspace > ExpSigStrength_3poi_r_ttH_FloatOtherPOI.log
combine -M MultiDimFit ttH_DiLepRegion_3poi.root --algo singles --cl=0.68 -t -1 -P r_ttH --setParameters r_ttW=1,r_ttH=1,r_tH=1 --floatOtherPOI=0 --saveFitResult -n 3poi --saveWorkspace > ExpSigStrength_3poi_r_ttH_NoFloatOtherPOI.log
'''

systs_ctcvcp = [
"",
#"kt_m3_kv_1","kt_m2_kv_1","kt_m1p5_kv_1","kt_m1p25_kv_1","kt_m0p75_kv_1","kt_m0p5_kv_1","kt_m0p25_kv_1","kt_0_kv_1","kt_0p25_kv_1","kt_0p5_kv_1","kt_0p75_kv_1","kt_1_kv_1","kt_1p25_kv_1","kt_1p5_kv_1","kt_2_kv_1","kt_3_kv_1","kt_m2_kv_1p5","kt_m1p5_kv_1p5","kt_m1p25_kv_1p5","kt_m1_kv_1p5","kt_m0p5_kv_1p5","kt_m0p25_kv_1p5","kt_0p25_kv_1p5","kt_0p5_kv_1p5","kt_1_kv_1p5","kt_1p25_kv_1p5","kt_2_kv_1p5","kt_m3_kv_0p5","kt_m2_kv_0p5","kt_m1p25_kv_0p5","kt_1p25_kv_0p5","kt_2_kv_0p5","kt_3_kv_0p5",
#"cosa_m0p9","cosa_m0p8","cosa_m0p7","cosa_m0p6","cosa_m0p5","cosa_m0p4","cosa_m0p3","cosa_m0p2","cosa_m0p1","cosa_mp0","cosa_0p1","cosa_0p2","cosa_0p3","cosa_0p4","cosa_0p5","cosa_0p6","cosa_0p7","cosa_0p8","cosa_0p9"
]

dirsToIgnore = []

#years = [2016,2017,2018]
years = [2018]

ToCopy = True 
makeCTCV_card = False
loopBins = False

datacardBaseName = "ttH"
tHqBaseName = "ttH"

datacard_labels={
#"DNNSubCat2_nBin10":[{"region":"2lss_0tau","label":"DNNSubCat2_option1","variable":"DNNSubCat2_nBin10","cat":["ee_ttHnode","ee_Restnode","ee_ttWnode","ee_tHQnode","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"]}],
"DNNSubCat2_BIN":[{"region":"2lss_0tau","label":"DNNSubCat2_option1","variable":"DNNSubCat2_BIN","cat":["ee_ttHnode","ee_Restnode","ee_ttWnode","ee_tHQnode","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"]}],
"SVA_BIN":[{"region":"2lss_3j","label":"SVACat3j","variable":"SVABin2l","cat":["ee","em_neg","em_pos","mm_neg","mm_pos"]},{"region":"2lss_geq4j","label":"SVACat2l","variable":"SVABin2l","cat":["ee_lj","ee_hj","em_lj_neg","em_hj_neg","em_lj_pos","em_hj_pos","mm_lj_neg","mm_hj_neg","mm_lj_pos","mm_hj_pos"]}],
#"DNNSubCat2_reBin":[{"region":"2lss_0tau","label":"DNNSubCat2_option1","variable":"DNNSubCat2_reBin","cat":["ee_ttHnode","ee_Restnode","ee_ttWnode","ee_tHQnode","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"]}],
#"DNNSubCat2_option2_BIN":[{"region":"2lss_0tau","label":"DNNSubCat2_option2","variable":"DNNSubCat2_option2_BIN","cat":["ee_ttHnode","ee_Restnode","ee_ttWnode","ee_tHQnode","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"]}],
#"DNNSubCat2_option2_reBin":[{"region":"2lss_0tau","label":"DNNSubCat2_option2","variable":"DNNSubCat2_option2_reBin","cat":["ee_ttHnode","ee_Restnode","ee_ttWnode","ee_tHQnode","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"]}],
#"BDT":[{"region":"2lss_0tau","label":"SubCat2l","variable":"Bin2l","cat":["ee_neg","ee_pos", "em_bl_neg","em_bl_pos","em_bt_neg","em_bt_pos", "mm_bl_neg","mm_bl_pos","mm_bt_neg","mm_bt_pos"]}],
}

DNN_labels={
"DNNSubCat2_option1":{"keyname":"DNNSubCat2","variable":"DNNSubCat2_nBin","cat":["ee_ttHnode","ee_Restnode","ee_ttWnode","ee_tHQnode","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"],"nbins":[x for x in range(1,20)]},
"DNNSubCat2_option2":{"keyname":"DNNSubCat2_option2","variable":"DNNSubCat2_option2_nBin","cat":["ee_ttHnode","ee_Restnode","ee_ttWnode","ee_tHQnode","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"],"nbins":[x for x in range(1,20)]},
}

def makecards(syst_ctcv, tocopy, name):
  for key, values in datacard_labels.items():
    DirName_datacard_All = "%s/%s_RunII/"%(cwd,key)
    if not os.path.exists(DirName_datacard_All):
        os.popen("mkdir -p "+DirName_datacard_All)
    os.chdir(DirName_datacard_All)
    combineCards_All = "combineCards.py"
    datacardNameAll = name + "_2lss_0tau_runII"  + syst_ctcv+ ".txt"
    for year in years:
        datacardName = name + "_2lss_0tau_" +str(year) + syst_ctcv+ ".txt"
        combineCards = "combineCards.py"
        # loope over regions:
        for value in values:
            region = value["region"]
            label = value["label"]
            variable = value["variable"]
            categories = value["cat"]
            for subCat in categories:
                if ( tocopy ) :

                    inputdirs = "%s/ttH_2lss_0tau_fixjer_22Jan_datacards_All/%s/%s/"%(inputBaseDir,label,variable)
                    command_cp = "cp %s/*%s*%i* ."%(inputdirs,subCat,year)
                    print(command_cp)
                    os.system(command_cp)
                count = 0
                datacard = open(name+"_"+region+"_"+subCat+"_"+str(year)+".txt",'r').read()
                count = datacard.count(name+"_"+region+"_"+subCat+"_"+str(year))
                if count <3: continue
                combineCards += (" "+name+"_"+region+"_"+subCat+"_"+str(year) +"="+name+"_"+region+"_"+subCat+"_"+str(year)+".txt")
        
        combineCards += (" > "+datacardName)
        combineCards_All += (" %s_2lss_0tau_%i=%s"%(name,year,datacardName))
        print(combineCards)
        os.system(combineCards)
    combineCards_All += (" > "+datacardNameAll)  
    print(combineCards_All)
    os.system(combineCards_All)
  
  os.chdir(cwd)
  return

def makeBincards(tocopy, name, key, region, label, variable, subCat):
    datacardName = name + "_"+region
    for year in years:
        datacardName += "_%i.txt"%year
        DirName_datacard = "%s/%s_SM_%s"%(cwd,key,region)
        if not os.path.exists(DirName_datacard):
            os.popen("mkdir -p "+DirName_datacard)
        os.chdir(DirName_datacard)
        
        combineCards = "combineCards.py"
        if ( tocopy ) :
            inputdirs = "%s/ttH_%s_deeptau2p1_1205_OptBIN_datacards_All/%s/%s/"%(inputBaseDir,region,label,variable)
            command_cp = "cp %s/*%s*%i* ."%(inputdirs,subCat,year)
            print(command_cp)
            os.system(command_cp)
        count = 0
        datacard = open(name+"_"+region+"_"+subCat+"_"+str(year)+".txt",'r').read()
        count = datacard.count(name+"_"+region+"_"+subCat+"_"+str(year))
        if count <3: continue
        combineCards += (" "+name+"_"+region+"_"+subCat+"_"+str(year) +"="+name+"_"+region+"_"+subCat+"_"+str(year)+".txt")
        
        combineCards += (" > "+datacardName)
        print(combineCards)
        os.system(combineCards)
  
    os.chdir(cwd)
    return

if loopBins:
    for key, value in DNN_labels.items():
        for subcat in value["cat"]:
            for nbin in value["nbins"]:
                region = "2lss_0tau"
                mykey = value["keyname"] + "_" + subcat  + "_nBin" + str(nbin)
                myvar = value["variable"] + str(nbin)
                makeBincards(ToCopy, datacardBaseName, mykey, region, key, myvar, subcat)
else:
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
