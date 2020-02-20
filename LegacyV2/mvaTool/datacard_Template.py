#!/usr/bin/env python
import ROOT
from ROOT import TString, TFile, TTree, TCanvas, TH1F, TH1, THStack, TColor, gROOT
from array import array
import sys,os,math
import optparse
import distutils.util

regPerCat={
"SubCat2l":["Var_DiLepRegion"],
"SVACat2l":["Var_DiLepRegion"],
"SVACat3j":["Var_DiLepRegion"],
"DNNCat":["Var_DiLepRegion"],
"DNNCat_option2":["2lss","ttWctrl"],
"DNNCat_option3":["2lss","ttWctrl"],
"DNNSubCat1_option1":["Var_DiLepRegion"],
"DNNSubCat1_option2":["2lss","ttWctrl"],
"DNNSubCat1_option3":["2lss","ttWctrl"],
"DNNSubCat2_option1":["Var_DiLepRegion"],
"DNNSubCat2_option2":["Var_DiLepRegion"],
"DNNSubCat2_option3":["2lss","ttWctrl"],
"DNNAMS2Cat1_option1":["2lss","ttWctrl"],
"DNNAMS2Cat1_option2":["2lss","ttWctrl"],
"DNNAMS2Cat1_option3":["2lss","ttWctrl"],
"DNNAMS3Cat1_option1":["2lss","ttWctrl"],
"DNNAMS3Cat1_option2":["2lss","ttWctrl"],
"DNNAMS3Cat1_option3":["2lss","ttWctrl"],
}
subCats={
#"SubCat2l":["inclusive","ee_neg","ee_pos", "em_bl_neg","em_bl_pos","em_bt_neg","em_bt_pos", "mm_bl_neg","mm_bl_pos","mm_bt_neg","mm_bt_pos" ]
"SubCat2l":["ee_neg","ee_pos", "em_bl_neg","em_bl_pos","em_bt_neg","em_bt_pos", "mm_bl_neg","mm_bl_pos","mm_bt_neg","mm_bt_pos" ],
"SVACat2l":["ee_lj","ee_hj", "em_lj_neg","em_hj_neg","em_lj_pos","em_hj_pos", "mm_lj_neg","mm_hj_neg","mm_lj_pos","mm_hj_pos"],
"SVACat3j":["ee","em_neg", "em_pos","mm_neg","mm_pos"],
"DNNCat":["ttHnode","Restnode","ttWnode","tHQnode"],
"DNNCat_option2":["ttHnode","Restnode","ttWnode","tHQnode"],
"DNNCat_option3":["ttHnode","Restnode","ttWnode","tHQnode"],
"DNNSubCat1_option1":["ee_neg","ee_pos","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"],
"DNNSubCat1_option2":["ee_neg","ee_pos","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"],
"DNNSubCat1_option3":["ee_neg","ee_pos","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"],
"DNNSubCat2_option1":["ee_ttHnode","ee_Restnode","ee_ttWnode","ee_tHQnode","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"],
"DNNSubCat2_option2":["ee_ttHnode","ee_Restnode","ee_ttWnode","ee_tHQnode","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"],
"DNNSubCat2_option3":["ee_ttHnode","ee_Restnode","ee_ttWnode","ee_tHQnode","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"],
"DNNAMS2Cat1_option1":["loose_ttHnode","tight_ttHnode","Restnode","ttWnode"],
"DNNAMS2Cat1_option2":["loose_ttHnode","tight_ttHnode","Restnode","ttWnode"],
"DNNAMS2Cat1_option3":["loose_ttHnode","tight_ttHnode","Restnode","ttWnode"],
"DNNAMS3Cat1_option1":["loose_ttHnode","tight_ttHnode","Restnode","ttWnode"],
"DNNAMS3Cat1_option2":["loose_ttHnode","tight_ttHnode","Restnode","ttWnode"],
"DNNAMS3Cat1_option3":["loose_ttHnode","tight_ttHnode","Restnode","ttWnode"],
}

usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-v', '--var',        dest='variable'  ,      help='variable name of final discriminator',      default='Bin2l',        type='string')
parser.add_option('-i', '--inDir',        dest='inDir'  ,      help='inDir of histograms',      default='V0212_datacards/',        type='string')
parser.add_option('-c', '--cat',        dest='category'  ,      help='type of channels',      default="SubCat2l",        type='string')
parser.add_option('-s', '--syst', action='store_false',        dest='SystUnc'  ,      help='to exclude systematics',      default=True)
parser.add_option('-m', '--mc', action='store_false',        dest='StatUnc'  ,      help='to exclude stats',      default=True)
parser.add_option('-t', '--template', action='store_false',        dest='ShapeUnc'  ,      help='to exclude shapes',      default=True)
parser.add_option('-p', '--Postfix', dest='Postfix',        help='to exclude shapes',      default="", type='string')
parser.add_option('-y', '--year',        dest='year'  ,      help='data taking year',      default=2018,        type='int')
parser.add_option('-n', '--namefix',        dest='namefix'  ,      help='namefix',      default="datacard",        type='string')

(opt, args) = parser.parse_args()


inDir = opt.inDir
variableName = opt.variable
cat_str = opt.category
SystUnc = opt.SystUnc
StatUnc = opt.StatUnc
ShapeUnc = opt.ShapeUnc
Postfix = opt.Postfix
year = opt.year
namefix = opt.namefix
isTHQ = False

if Postfix == "_" : 
    Postfix =""

if len(Postfix) > 0: isTHQ = True

#useData = False
AutoMC = True
RemoveZeroSample = True

channels = subCats[cat_str]
Regions = regPerCat[cat_str]
POI = variableName 
DirOfRootplas = inDir +  cat_str + "/"


#Regions = ["2lss"]


numberOfBins={"Bin2l": 11,"mT_lep2":10,"Hj_tagger":10,"mT_lep1":10,"Dilep_mtWmin":10,"massll":10,"Sum2lCharge":2,"nLooseJet":7,"mht":10,"metLD":10,"Dilep_bestMVA":8,"Dilep_worseMVA":8,"Dilep_pdgId":3,"Dilep_htllv":10,"Dilep_nTight":3,"HighestJetCSV":15,"HtJet":10,"Mt_metleadlep":10,"maxeta":10,"leadLep_jetdr":10,"secondLep_jetdr":10,"minMllAFOS":10,"minMllAFAS":10,"minMllSFOS":10,"nLepFO":6,"nLepTight":6,"puWeight":30,"bWeight":30,"TriggerSF":30,"lepSF":30,"leadLep_BDT":10,"secondLep_BDT":10,"TrueInteractions":100,"nBestVTX":100,"mvaOutput_2lss_ttV":10,"mvaOutput_2lss_ttbar":10,"nBJetLoose":5,"nBJetMedium":5,"lep1_conePt":50,"lep2_conePt":50,"PFMET":40,"PFMETphi":10,"jet1_CSV":10,"jet2_CSV":10,"jet3_CSV":10,"jet4_CSV":10}

Prefix = namefix + "_"

h_data_name ="data_obs"

samplesToUse=[]

samples = [
"ttH_hww","ttH_hzz","ttH_htt","ttH_hmm","ttH_hzg",
"tHq_hww","tHq_hzz","tHq_htt",
"tHW_hww","tHW_hzz","tHW_htt",
"ggH_hww","ggH_hzz","ggH_htt",
"qqH_hww","qqH_hzz","qqH_htt",
#"VH_hww","VH_hzz","VH_htt",
"HH",
"WH_hww","WH_hzz","WH_htt",
"ZH_htt","ZH_hww","ZH_hzz",
"TTWH_htt","TTWH_hww","TTWH_hzz",
"TTZH_htt","TTZH_hww","TTZH_hzz",
"TTWW","TTW","TTZ","WZ","ZZ","Rares","Convs","data_fakes","data_flips"]
#"TTWW","TTW","TTZ","WZ","ZZ","Rares","Convs","mcFakes","mcFlips"

samplesMM = [
"ttH_hww","ttH_hzz","ttH_htt","ttH_hmm","ttH_hzg",
"tHq_hww","tHq_hzz","tHq_htt",
"tHW_hww","tHW_hzz","tHW_htt",
"ggH_hww","ggH_hzz","ggH_htt",
"qqH_hww","qqH_hzz","qqH_htt",
#"VH_hww","VH_hzz","VH_htt",
"HH",
"WH_hww","WH_hzz","WH_htt",
"ZH_htt","ZH_hww","ZH_hzz",
"TTWH_htt","TTWH_hww","TTWH_hzz",
"TTZH_htt","TTZH_hww","TTZH_hzz",
#"TTWW","TTW","TTZ","WZ","ZZ","Rares","Convs","mcFakes",
"TTWW","TTW","TTZ","WZ","ZZ","Rares","Convs","data_fakes",
]

samplesEE = [
"ttH_hww","ttH_hzz","ttH_htt","ttH_hzg",
"tHq_hww","tHq_hzz","tHq_htt",
"tHW_hww","tHW_hzz","tHW_htt",
"ggH_hww","ggH_hzz","ggH_htt",
"qqH_hww","qqH_hzz","qqH_htt",
#"VH_hww","VH_hzz","VH_htt",
"HH",
"WH_hww","WH_hzz","WH_htt",
"ZH_htt","ZH_hww","ZH_hzz",
"TTWH_htt","TTWH_hww","TTWH_hzz",
"TTZH_htt","TTZH_hww","TTZH_hzz",
#"TTWW","TTW","TTZ","WZ","ZZ","Rares","Convs","mcFakes","mcFlips",
 "TTWW","TTW","TTZ","WZ","ZZ","Rares","Convs","data_fakes","data_flips"
]

Rates = {
"Rares":0, "WZ":0, "ZZ":0, "Convs":0, "TTW":0, "TTWW":0, "TTZ":0, "data_fakes":0, "data_flips":0, 
#"Rares":0, "WZ":0, "ZZ":0, "Convs":0, "TTW":0, "TTWW":0, "TTZ":0, "mcFakes":0, "mcFlips":0, 
"ttH_htt":0,"ttH_hww":0,"ttH_hzz":0,"ttH_hzg":0,"ttH_hmm":0,
"tHq_htt":0,"tHq_hww":0,"tHq_hzz":0,
"ggH_htt":0,"ggH_hww":0,"ggH_hzz":0,
"qqH_htt":0,"qqH_hww":0,"qqH_hzz":0,
#"VH_htt":0,"VH_hww":0,"VH_hzz":0,
"HH":0,
"WH_htt":0,"WH_hww":0,"WH_hzz":0,
"ZH_htt":0,"ZH_hww":0,"ZH_hzz":0,
"TTWH_htt":0,"TTWH_hww":0,"TTWH_hzz":0,
"TTZH_htt":0,"TTZH_hww":0,"TTZH_hzz":0,
"tHW_htt":0,"tHW_hww":0,"tHW_hzz":0
}

Labels = {
"Rares":11, "WZ":10, "ZZ":6, "Convs":12, "TTW":8, "TTWW":7, "TTZ":9, "data_fakes":13, "data_flips":25,"mcFakes":14, "mcFlips":26, 
"ttH_htt":-7,"ttH_hww":-9,"ttH_hzz":-8,"ttH_hzg":-5,"ttH_hmm":-6,
#"tHq_htt":3,"tHq_hww":1,"tHq_hzz":2,
#"tHW_htt":6,"tHW_hww":4,"tHW_hzz":5
# marked as bkg atm
#"VH_htt":19,"VH_hww":17,"VH_hzz":18,
#"ggH_htt":22,"ggH_hww":20,"ggH_hzz":21,
#"qqH_htt":25,"qqH_hww":23,"qqH_hzz":24,
"HH":30,
"WH_htt":-40,"WH_hww":-41,"WH_hzz":-42,
"ZH_htt":-37,"ZH_hww":-38,"ZH_hzz":-39,
"TTWH_htt":31,"TTWH_hww":32,"TTWH_hzz":33,
"TTZH_htt":34,"TTZH_hww":35,"TTZH_hzz":36,
"VH_htt":-19,"VH_hww":-17,"VH_hzz":-18,
"ggH_htt":-22,"ggH_hww":-20,"ggH_hzz":-21,
"qqH_htt":-25,"qqH_hww":-23,"qqH_hzz":-24,
"tHq_htt":-13,"tHq_hww":-11,"tHq_hzz":-12,
"tHW_htt":-16,"tHW_hww":-14,"tHW_hzz":-15
 }

print (isTHQ)

if isTHQ:
    Labels["VH_htt"]=19
    Labels["VH_hww"]=17
    Labels["VH_hzz"]=18
    Labels["ggH_htt"]=22
    Labels["ggH_hww"]=20
    Labels["ggH_hzz"]=21
    Labels["qqH_htt"]=25
    Labels["qqH_hww"]=23
    Labels["qqH_hzz"]=24
    Labels["ZH_htt"]=37
    Labels["ZH_hww"]=38
    Labels["ZH_hzz"]=39
    Labels["WH_htt"]=40
    Labels["WH_hww"]=41
    Labels["WH_hzz"]=42
               

### the nuisances that will be written into the datacards
CommonNuisances=[
# lnN
# theory systematics
"pdf_Higgs_ttH","QCDscale_ttH","pdf_tHq", "QCDscale_tHq", "pdf_tHW", "QCDscale_tHW", "pdf_TTW","QCDscale_TTW", "pdf_TTWW","QCDscale_TTWW", "pdf_TTZ", "QCDscale_TTZ","CMS_ttHl_WZ_theo",
"pdf_WH","QCDscale_WH","pdf_ZH","QCDscale_ZH","pdf_qqH","QCDscale_qqH","pdf_ggH","QCDscale_ggH",
"BR_htt","BR_hww","BR_hzz","BR_hzg","BR_hmm",
# experimental systematics
"CMS_ttHl_QF","CMS_ttHl_EWK_4j","CMS_ttHl_Convs","CMS_ttHl_Rares","CMS_ttHl_EWK",
"lumi_corr",
# lnU
# experimental
#"CMS_ttHl_WZ_lnU","CMS_ttHl_ZZ_lnU",
# shape
"CMS_ttHl_lepEff_muloose","CMS_ttHl_lepEff_elloose",
"CMS_ttHl_lepEff_mutight","CMS_ttHl_lepEff_eltight",
#"CMS_ttHl_Clos_e_norm","CMS_ttHl_Clos_m_norm",
"CMS_ttHl_Clos_e_shape","CMS_ttHl_Clos_m_shape",
"CMS_ttHl_FRm_norm","CMS_ttHl_FRm_pt","CMS_ttHl_FRm_be","CMS_ttHl_FRe_norm","CMS_ttHl_FRe_pt","CMS_ttHl_FRe_be",
"CMS_ttHl_thu_shape_ttH_x1","CMS_ttHl_thu_shape_ttH_y1",
"CMS_ttHl_btag_cErr1","CMS_ttHl_btag_cErr2","CMS_ttHl_btag_LF","CMS_ttHl_btag_HF",
# independent samples
#"CMS_ttHl_JER","CMS_ttHl_UnclusteredEn","CMS_scale_j_jesFlavorQCD",
#"CMS_scale_j_jesRelativeBal","CMS_scale_j_jesHF","CMS_scale_j_jesBBEC1","CMS_scale_j_jesEC2","CMS_scale_j_jesAbsolute",
]

Nuisance_2016=[
# lnN
"lumi_2016",
# shape
#"CMS_ttHl16_trigger",
"CMS_ttHl16_L1PreFiring",
"CMS_ttHl16_btag_HFStats1","CMS_ttHl16_btag_HFStats2","CMS_ttHl16_btag_LFStats1","CMS_ttHl16_btag_LFStats2","PU_16",
# uncorrelated
#"CMS_scale_j_jesRelativeSample_2016",
#"CMS_scale_j_jesBBEC1_2016","CMS_scale_j_jesEC2_2016","CMS_scale_j_jesAbsolute_2016","CMS_scale_j_jesHF_2016",
]

Nuisance_2017=[
# lnN
"lumi_2017",
# shape
#"CMS_ttHl17_trigger",
"CMS_ttHl17_L1PreFiring",
"CMS_ttHl17_btag_HFStats1","CMS_ttHl17_btag_HFStats2","CMS_ttHl17_btag_LFStats1","CMS_ttHl17_btag_LFStats2","PU_17",
# uncorrelated
#"CMS_scale_j_jesRelativeSample_2017",
#"CMS_scale_j_jesBBEC1_2017","CMS_scale_j_jesEC2_2017","CMS_scale_j_jesAbsolute_2017","CMS_scale_j_jesHF_2017",
]

Nuisance_2018=[
# lnN
"lumi_2018",
# shape
#"CMS_ttHl18_trigger",
"CMS_ttHl18_btag_HFStats1","CMS_ttHl18_btag_HFStats2","CMS_ttHl18_btag_LFStats1","CMS_ttHl18_btag_LFStats2","PU_18",
# uncorrelated
#"CMS_scale_j_jesRelativeSample_2018",
#"CMS_scale_j_jesBBEC1_2018","CMS_scale_j_jesEC2_2018","CMS_scale_j_jesAbsolute_2018","CMS_scale_j_jesHF_2018",
]

Nuisances = []
if year == 2016:
    Nuisances = CommonNuisances + Nuisance_2016
    print ( " use 2016 nuisances ")
elif year == 2017:
    Nuisances = CommonNuisances + Nuisance_2017
    print ( " use 2017 nuisances ")
elif year == 2018:
    Nuisances = CommonNuisances + Nuisance_2018
    print ( " use 2018 nuisances ")
else:
    print ( " You pass %i to year, however it must be 2016/2017 or 2018, I don't know what to do other than exit the script "%year)
    sys.exit()

# not sure where to find CP related uncertainties, so put SM value at the moment
TH_systs={
"pdf_tHq":{
    "kt_m3_kv_1":"1.009", "kt_m2_kv_1":"1.009", "kt_m1p5_kv_1":"1.009", "kt_m1p25_kv_1":"1.009", "kt_m0p75_kv_1":"1.009", "kt_m0p5_kv_1":"1.009", "kt_m0p25_kv_1":"1.009", "kt_0_kv_1":"1.009", "kt_0p25_kv_1":"1.010", "kt_0p5_kv_1":"1.010", "kt_0p75_kv_1":"1.010", "kt_1_kv_1":"1.010", "kt_1p25_kv_1":"1.010", "kt_1p5_kv_1":"1.009", "kt_2_kv_1":"1.009", "kt_3_kv_1":"1.009", 
    "kt_m2_kv_1p5":"1.009", "kt_m1p5_kv_1p5":"1.009", "kt_m1p25_kv_1p5":"1.009", "kt_m1_kv_1p5":"1.009", "kt_m0p5_kv_1p5":"1.009", "kt_m0p25_kv_1p5":"1.009", "kt_0p25_kv_1p5":"1.009", "kt_0p5_kv_1p5":"1.010", "kt_1_kv_1p5":"1.010", "kt_1p25_kv_1p5":"1.010", "kt_2_kv_1p5":"1.009", 
    "kt_m3_kv_0p5":"1.009", "kt_m2_kv_0p5":"1.009", "kt_m1p25_kv_0p5":"1.009", "kt_1p25_kv_0p5":"1.009", "kt_2_kv_0p5":"1.009", "kt_3_kv_0p5":"1.009", 
    "cosa_m0p9": "1.010" , "cosa_m0p8":  "1.010" , "cosa_m0p7": "1.010" , "cosa_m0p6": "1.010" , "cosa_m0p5": "1.010" , "cosa_m0p4": "1.010" , "cosa_m0p3": "1.010" ,"cosa_m0p2": "1.010" , "cosa_m0p1": "1.010" , "cosa_mp0001": "1.010" , "cosa_0p1": "1.010" , "cosa_0p2": "1.010" , "cosa_0p3": "1.010" , "cosa_0p4": "1.010" , "cosa_0p5": "1.010" , "cosa_0p6": "1.010" , "cosa_0p7": "1.010" , "cosa_0p8": "1.010" , "cosa_0p9": "1.010"
    },
"QCDscale_tHq":{
    "kt_m3_kv_1":"0.969/1.021", "kt_m2_kv_1":"0.968/1.026", "kt_m1p5_kv_1":"0.964/1.025", "kt_m1p25_kv_1":"0.966/1.026", "kt_m0p75_kv_1":"0.959/1.029", "kt_m0p5_kv_1":"0.956/1.032", "kt_m0p25_kv_1":"0.950/1.035", "kt_0_kv_1":"0.945/1.039", "kt_0p25_kv_1":"0.938/1.044", "kt_0p5_kv_1":"0.929/1.050", "kt_0p75_kv_1":"0.924/1.057", "kt_1_kv_1":"0.933/1.041", "kt_1p25_kv_1":"0.954/1.023", "kt_1p5_kv_1":"0.971/1.012", "kt_2_kv_1":"0.964/1.01", "kt_3_kv_1":"0.963/1.008", 
    "kt_m2_kv_1p5":"0.964/1.025", "kt_m1p5_kv_1p5":"0.961/1.027", "kt_m1p25_kv_1p5":"0.961/1.028", "kt_m1_kv_1p5":"0.957/1.030", "kt_m0p5_kv_1p5":"0.953/1.034", "kt_m0p25_kv_1p5":"0.950/1.036", "kt_0p25_kv_1p5":"0.939/1.042", "kt_0p5_kv_1p5":"0.935/1.046", "kt_1_kv_1p5":"0.924/1.057", "kt_1p25_kv_1p5":"0.925/1.055", "kt_2_kv_1p5":"0.961/1.020", 
    "kt_m3_kv_0p5":"0.973/1.019", "kt_m2_kv_0p5":"0.971/1.020", "kt_m1p25_kv_0p5":"0.970/1.021", "kt_1p25_kv_0p5":"0.963/1.009", "kt_2_kv_0p5":"0.964/1.010", "kt_3_kv_0p5":"0.968/1.012", 
    "cosa_m0p9": "0.933/1.041" , "cosa_m0p8":  "0.933/1.041" , "cosa_m0p7": "0.933/1.041" , "cosa_m0p6": "0.933/1.041" , "cosa_m0p5": "0.933/1.041" , "cosa_m0p4": "0.933/1.041" , "cosa_m0p3": "0.933/1.041" ,"cosa_m0p2": "0.933/1.041" , "cosa_m0p1": "0.933/1.041" , "cosa_mp0001": "0.933/1.041" , "cosa_0p1": "0.933/1.041" , "cosa_0p2": "0.933/1.041" , "cosa_0p3": "0.933/1.041" , "cosa_0p4": "0.933/1.041" , "cosa_0p5": "0.933/1.041" , "cosa_0p6": "0.933/1.041" , "cosa_0p7": "0.933/1.041" , "cosa_0p8": "0.933/1.041" , "cosa_0p9": "0.933/1.041"
    },
"pdf_tHW":{
    "kt_m3_kv_1":"1.038", "kt_m2_kv_1":"1.038", "kt_m1p5_kv_1":"1.039", "kt_m1p25_kv_1":"1.039", "kt_m0p75_kv_1":"1.040", "kt_m0p5_kv_1":"1.040", "kt_m0p25_kv_1":"1.040", "kt_0_kv_1":"1.039", "kt_0p25_kv_1":"1.038", "kt_0p5_kv_1":"1.035", "kt_0p75_kv_1":"1.029", "kt_1_kv_1":"1.027", "kt_1p25_kv_1":"1.028", "kt_1p5_kv_1":"1.039", "kt_2_kv_1":"1.032", "kt_3_kv_1":"1.034", 
    "kt_m2_kv_1p5":"1.039", "kt_m1p5_kv_1p5":"1.039", "kt_m1p25_kv_1p5":"1.039", "kt_m1_kv_1p5":"1.039", "kt_m0p5_kv_1p5":"1.040", "kt_m0p25_kv_1p5":"1.040", "kt_0p25_kv_1p5":"1.039", "kt_0p5_kv_1p5":"1.038", "kt_1_kv_1p5":"1.031", "kt_1p25_kv_1p5":"1.028", "kt_2_kv_1p5":"1.028", 
    "kt_m3_kv_0p5":"1.037", "kt_m2_kv_0p5":"1.038", "kt_m1p25_kv_0p5":"1.038", "kt_1p25_kv_0p5":"1.033", "kt_2_kv_0p5":"1.035", "kt_3_kv_0p5":"1.035", 
    "cosa_m0p9": "1.027" , "cosa_m0p8":  "1.027" , "cosa_m0p7": "1.027" , "cosa_m0p6": "1.027" , "cosa_m0p5": "1.027" , "cosa_m0p4": "1.027" , "cosa_m0p3": "1.027" ,"cosa_m0p2": "1.027" , "cosa_m0p1": "1.027" , "cosa_mp0001": "1.027" , "cosa_0p1": "1.027" , "cosa_0p2": "1.027" , "cosa_0p3": "1.027" , "cosa_0p4": "1.027" , "cosa_0p5": "1.027" , "cosa_0p6": "1.027" , "cosa_0p7": "1.027" , "cosa_0p8": "1.027" , "cosa_0p9": "1.027"
    },
"QCDscale_tHW":{
    "kt_m3_kv_1":"0.973/1.023", "kt_m2_kv_1":"0.975/1.022", "kt_m1p5_kv_1":"0.978/1.021", "kt_m1p25_kv_1":"0.980/1.020", "kt_m0p75_kv_1":"0.983/1.020", "kt_m0p5_kv_1":"0.986/1.017", "kt_m0p25_kv_1":"0.989/1.016", "kt_0_kv_1":"0.988/1.015", "kt_0p25_kv_1":"0.985/1.016", "kt_0p5_kv_1":"0.980/1.021", "kt_0p75_kv_1":"0.961/1.032", "kt_1_kv_1":"0.939/1.046", "kt_1p25_kv_1":"0.946/1.048", "kt_1p5_kv_1":"0.937/1.046", "kt_2_kv_1":"0.945/1.04", "kt_3_kv_1":"0.954/1.033", 
    "kt_m2_kv_1p5":"0.979/1.021", "kt_m1p5_kv_1p5":"0.982/1.019", "kt_m1p25_kv_1p5":"0.984/1.019", "kt_m1_kv_1p5":"0.985/1.019", "kt_m0p5_kv_1p5":"0.988/1.016", "kt_m0p25_kv_1p5":"0.988/1.016", "kt_0p25_kv_1p5":"0.986/1.015", "kt_0p5_kv_1p5":"0.983/1.018", "kt_1_kv_1p5":"0.970/1.028", "kt_1p25_kv_1p5":"0.953/1.036", "kt_2_kv_1p5":"0.935/1.048", 
    "kt_m3_kv_0p5":"0.970/1.023", "kt_m2_kv_0p5":"0.972/1.023", "kt_m1p25_kv_0p5":"0.975/1.022", "kt_1p25_kv_0p5":"0.948/1.037", "kt_2_kv_0p5":"0.957/1.030", "kt_3_kv_0p5":"0.960/1.028", 
    "cosa_m0p9": "0.939/1.046" , "cosa_m0p8":  "0.939/1.046" , "cosa_m0p7": "0.939/1.046" , "cosa_m0p6": "0.939/1.046" , "cosa_m0p5": "0.939/1.046" , "cosa_m0p4": "0.939/1.046" , "cosa_m0p3": "0.939/1.046" ,"cosa_m0p2": "0.939/1.046" , "cosa_m0p1": "0.939/1.046" , "cosa_mp0001": "0.939/1.046" , "cosa_0p1": "0.939/1.046" , "cosa_0p2": "0.939/1.046" , "cosa_0p3": "0.939/1.046" , "cosa_0p4": "0.939/1.046" , "cosa_0p5": "0.939/1.046" , "cosa_0p6": "0.939/1.046" , "cosa_0p7": "0.939/1.046" , "cosa_0p8": "0.939/1.046" , "cosa_0p9": "0.939/1.046"
    },
}


systTypes={
"lnN":[
"pdf_Higgs_ttH","QCDscale_ttH","pdf_tHq", "QCDscale_tHq", "pdf_tHW", "QCDscale_tHW", "pdf_TTW","QCDscale_TTW", "pdf_TTWW","QCDscale_TTWW", "pdf_TTZ", "QCDscale_TTZ","CMS_ttHl_WZ_theo",
"pdf_WH","QCDscale_WH","pdf_ZH","QCDscale_ZH","pdf_qqH","QCDscale_qqH","pdf_ggH","QCDscale_ggH",
"BR_htt","BR_hww","BR_hzz","BR_hzg","BR_hmm",
"CMS_ttHl_QF","CMS_ttHl_EWK_4j","CMS_ttHl_Convs","CMS_ttHl_Rares","CMS_ttHl_EWK",
"lumi_2016","lumi_2017","lumi_2018","lumi_corr"
],
"lnU":[
"CMS_ttHl_WZ_lnU","CMS_ttHl_ZZ_lnU",
]
}


if not ShapeUnc:
    if year == 2016:
        Nuisances = [
"pdf_Higgs_ttH","QCDscale_ttH","pdf_tHq", "QCDscale_tHq", "pdf_tHW", "QCDscale_tHW", "pdf_TTW","QCDscale_TTW", "pdf_TTWW","QCDscale_TTWW", "pdf_TTZ", "QCDscale_TTZ","CMS_ttHl_WZ_theo",
"pdf_WH","QCDscale_WH","pdf_ZH","QCDscale_ZH","pdf_qqH","QCDscale_qqH","pdf_ggH","QCDscale_ggH",
"BR_htt","BR_hww","BR_hzz","BR_hzg","BR_hmm",
"CMS_ttHl_QF","CMS_ttHl_EWK_4j","CMS_ttHl_Convs","CMS_ttHl_Rares","CMS_ttHl_EWK",
#"CMS_ttHl_WZ_lnU","CMS_ttHl_ZZ_lnU",
"lumi_2016"
        ]
    elif year == 2017:
        Nuisances = [
"pdf_Higgs_ttH","QCDscale_ttH","pdf_tHq", "QCDscale_tHq", "pdf_tHW", "QCDscale_tHW", "pdf_TTW","QCDscale_TTW", "pdf_TTWW","QCDscale_TTWW", "pdf_TTZ", "QCDscale_TTZ","CMS_ttHl_WZ_theo",
"pdf_WH","QCDscale_WH","pdf_ZH","QCDscale_ZH","pdf_qqH","QCDscale_qqH","pdf_ggH","QCDscale_ggH",
"BR_htt","BR_hww","BR_hzz","BR_hzg","BR_hmm",
"CMS_ttHl_QF","CMS_ttHl_EWK_4j","CMS_ttHl_Convs","CMS_ttHl_Rares","CMS_ttHl_EWK",
#"CMS_ttHl_WZ_lnU","CMS_ttHl_ZZ_lnU",
"lumi_2017"
    ]
    elif year == 2018:
        Nuisances = [
"pdf_Higgs_ttH","QCDscale_ttH","pdf_tHq", "QCDscale_tHq", "pdf_tHW", "QCDscale_tHW", "pdf_TTW","QCDscale_TTW", "pdf_TTWW","QCDscale_TTWW", "pdf_TTZ", "QCDscale_TTZ","CMS_ttHl_WZ_theo",
"pdf_WH","QCDscale_WH","pdf_ZH","QCDscale_ZH","pdf_qqH","QCDscale_qqH","pdf_ggH","QCDscale_ggH",
"BR_htt","BR_hww","BR_hzz","BR_hzg","BR_hmm",
"CMS_ttHl_QF","CMS_ttHl_EWK_4j","CMS_ttHl_Convs","CMS_ttHl_Rares","CMS_ttHl_EWK",
#"CMS_ttHl_WZ_lnU","CMS_ttHl_ZZ_lnU",
"lumi_2018"
    ]

channelSyst={
"CMS_ttHl_lepEff_muloose":{"mm":"1","em":"1","ee":"-"}, #
"CMS_ttHl_lepEff_mutight":{"mm":"1","em":"1","ee":"-"}, #
"CMS_ttHl_lepEff_elloose":{"mm":"-","em":"1","ee":"1"}, #
"CMS_ttHl_lepEff_eltight":{"mm":"-","em":"1","ee":"1"}, #
"CMS_ttHl_Clos_e_norm":{"mm":"-","em":"1","ee":"1"}, #
"CMS_ttHl_Clos_m_norm":{"mm":"1","em":"1","ee":"-"}, #
#"CMS_ttHl17_Clos_e_bt_norm":{"mm_bt":"-","em_bt":"1.100","ee_bt":"1.200"},#
#"CMS_ttHl17_Clos_m_bt_norm":{"mm_bt":"1.300","em_bt":"1.150","ee_bt":"-"},#
"CMS_ttHl_Clos_e_shape":{"mm":"-","em":"1","ee":"1"},#
"CMS_ttHl_Clos_m_shape":{"mm":"1","em":"1","ee":"-"},#
"CMS_ttHl_FRe_norm":{"mm":"-","em":"1","ee":"1"},
"CMS_ttHl_FRm_norm":{"mm":"1","em":"1","ee":"-"},
"CMS_ttHl_FRe_pt":{"mm":"-","em":"1","ee":"1"},
"CMS_ttHl_FRm_pt":{"mm":"1","em":"1","ee":"-"},
"CMS_ttHl_FRe_be":{"mm":"-","em":"1","ee":"1"},
"CMS_ttHl_FRm_be":{"mm":"1","em":"1","ee":"-"},
}

YearYields={
"lumi_corr":{
    2016:{"WZ": "1.014" , "ZZ": "1.014" , "Rares": "1.014" , "Convs" : "1.014", "ttH_htt":"1.014","ttH_hww":"1.014","ttH_hzz":"1.014","ttH_hzg":"1.014","ttH_hmm": "1.014", "TTW" : "1.014", "tHq_htt":"1.014","tHq_hww":"1.014","tHq_hzz":"1.014","tHW_htt":"1.014","tHW_hww":"1.014","tHW_hzz":"1.014", "TTWW":"1.014", "TTZ": "1.014", "data_fakes": "1.014", "data_flips":"1.014","ggH_hww": "1.014", "ggH_hzz": "1.014", "ggH_htt": "1.014", "qqH_hww": "1.014", "qqH_hzz": "1.014", "qqH_htt": "1.014", "VH_hww":"1.014", "VH_hzz": "1.014", "VH_htt": "1.014", "mcFakes": "1.014", "mcFlips": "1.014", "HH": "1.014",  "WH_hww": "1.014", "WH_hzz": "1.014", "WH_htt": "1.014",  "ZH_htt": "1.014", "ZH_hww": "1.014", "ZH_hzz": "1.014",  "TTWH_htt": "1.014", "TTWH_hww": "1.014", "TTWH_hzz": "1.014",  "TTZH_htt": "1.014", "TTZH_hww": "1.014", "TTZH_hzz": "1.014" },
    2017:{"WZ": "1.013" , "ZZ": "1.013" , "Rares": "1.013" , "Convs" : "1.013", "ttH_htt":"1.013","ttH_hww":"1.013","ttH_hzz":"1.013","ttH_hzg":"1.013","ttH_hmm": "1.013", "TTW" : "1.013", "tHq_htt":"1.013","tHq_hww":"1.013","tHq_hzz":"1.013","tHW_htt":"1.013","tHW_hww":"1.013","tHW_hzz":"1.013", "TTWW":"1.013", "TTZ": "1.013", "data_fakes": "1.013", "data_flips":"1.013","ggH_hww": "1.013", "ggH_hzz": "1.013", "ggH_htt": "1.013", "qqH_hww": "1.013", "qqH_hzz": "1.013", "qqH_htt": "1.013", "VH_hww":"1.013", "VH_hzz": "1.013", "VH_htt": "1.013", "mcFakes": "1.013", "mcFlips": "1.013", "HH": "1.013",  "WH_hww": "1.013", "WH_hzz": "1.013", "WH_htt": "1.013",  "ZH_htt": "1.013", "ZH_hww": "1.013", "ZH_hzz": "1.013",  "TTWH_htt": "1.013", "TTWH_hww": "1.013", "TTWH_hzz": "1.013",  "TTZH_htt": "1.013", "TTZH_hww": "1.013", "TTZH_hzz": "1.013" },
    2018:{"WZ": "1.021" , "ZZ": "1.021" , "Rares": "1.021" , "Convs" : "1.021", "ttH_htt":"1.021","ttH_hww":"1.021","ttH_hzz":"1.021","ttH_hzg":"1.021","ttH_hmm": "1.021", "TTW" : "1.021", "tHq_htt":"1.021","tHq_hww":"1.021","tHq_hzz":"1.021","tHW_htt":"1.021","tHW_hww":"1.021","tHW_hzz":"1.021", "TTWW":"1.021", "TTZ": "1.021", "data_fakes": "1.021", "data_flips":"1.021","ggH_hww": "1.021", "ggH_hzz": "1.021", "ggH_htt": "1.021", "qqH_hww": "1.021", "qqH_hzz": "1.021", "qqH_htt": "1.021", "VH_hww":"1.021", "VH_hzz": "1.021", "VH_htt": "1.021", "mcFakes": "1.021", "mcFlips": "1.021", "HH": "1.021",  "WH_hww": "1.021", "WH_hzz": "1.021", "WH_htt": "1.021",  "ZH_htt": "1.021", "ZH_hww": "1.021", "ZH_hzz": "1.021",  "TTWH_htt": "1.021", "TTWH_hww": "1.021", "TTWH_hzz": "1.021",  "TTZH_htt": "1.021", "TTZH_hww": "1.021", "TTZH_hzz": "1.021" },
}
}

YieldSysts={
"pdf_TTZ":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "0.966/1.035", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"QCDscale_TTZ":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "0.904/1.112", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"pdf_TTW":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "1.04", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"QCDscale_TTW":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "0.885/1.129", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"pdf_Higgs_ttH":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"1.036","ttH_hww":"1.036","ttH_hzz":"1.036","ttH_hzg":"1.036","ttH_hmm": "1.036", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"pdf_qqbar":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "1.040", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"QCDscale_ttZ":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "0.904/1.112", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"lumi_2016":{"WZ": "1.022" , "ZZ": "1.022" , "Rares": "1.022" , "Convs" : "1.022", "ttH_htt":"1.022","ttH_hww":"1.022","ttH_hzz":"1.022","ttH_hzg":"1.022","ttH_hmm": "1.022", "TTW" : "1.022", "tHq_htt":"1.022","tHq_hww":"1.022","tHq_hzz":"1.022","tHW_htt":"1.022","tHW_hww":"1.022","tHW_hzz":"1.022", "TTWW":"1.022", "TTZ": "1.022", "data_fakes": "1.022", "data_flips":"1.022","ggH_hww": "1.022", "ggH_hzz": "1.022", "ggH_htt": "1.022", "qqH_hww": "1.022", "qqH_hzz": "1.022", "qqH_htt": "1.022", "VH_hww":"1.022", "VH_hzz": "1.022", "VH_htt": "1.022", "mcFakes": "1.022", "mcFlips": "1.022", "HH": "1.022",  "WH_hww": "1.022", "WH_hzz": "1.022", "WH_htt": "1.022",  "ZH_htt": "1.022", "ZH_hww": "1.022", "ZH_hzz": "1.022",  "TTWH_htt": "1.022", "TTWH_hww": "1.022", "TTWH_hzz": "1.022",  "TTZH_htt": "1.022", "TTZH_hww": "1.022", "TTZH_hzz": "1.022" },
"lumi_2017":{"WZ": "1.020" , "ZZ": "1.020" , "Rares": "1.020" , "Convs" : "1.020", "ttH_htt":"1.020","ttH_hww":"1.020","ttH_hzz":"1.020","ttH_hzg":"1.020","ttH_hmm": "1.020", "TTW" : "1.020", "tHq_htt":"1.020","tHq_hww":"1.020","tHq_hzz":"1.020","tHW_htt":"1.020","tHW_hww":"1.020","tHW_hzz":"1.020", "TTWW":"1.020", "TTZ": "1.020", "data_fakes": "1.020", "data_flips":"1.020","ggH_hww": "1.020", "ggH_hzz": "1.020", "ggH_htt": "1.020", "qqH_hww": "1.020", "qqH_hzz": "1.020", "qqH_htt": "1.020", "VH_hww":"1.020", "VH_hzz": "1.020", "VH_htt": "1.020", "mcFakes": "1.020", "mcFlips": "1.020", "HH": "1.020",  "WH_hww": "1.020", "WH_hzz": "1.020", "WH_htt": "1.020",  "ZH_htt": "1.020", "ZH_hww": "1.020", "ZH_hzz": "1.020",  "TTWH_htt": "1.020", "TTWH_hww": "1.020", "TTWH_hzz": "1.020",  "TTZH_htt": "1.020", "TTZH_hww": "1.020", "TTZH_hzz": "1.020" },
"lumi_2018":{"WZ": "1.015" , "ZZ": "1.015" , "Rares": "1.015" , "Convs" : "1.015", "ttH_htt":"1.015","ttH_hww":"1.015","ttH_hzz":"1.015","ttH_hzg":"1.015","ttH_hmm": "1.015", "TTW" : "1.015", "tHq_htt":"1.015","tHq_hww":"1.015","tHq_hzz":"1.015","tHW_htt":"1.015","tHW_hww":"1.015","tHW_hzz":"1.015", "TTWW":"1.015", "TTZ": "1.015", "data_fakes": "1.015", "data_flips":"1.015","ggH_hww": "1.015", "ggH_hzz": "1.015", "ggH_htt": "1.015", "qqH_hww": "1.015", "qqH_hzz": "1.015", "qqH_htt": "1.015", "VH_hww":"1.015", "VH_hzz": "1.015", "VH_htt": "1.015", "mcFakes": "1.015", "mcFlips": "1.015", "HH": "1.015",  "WH_hww": "1.015", "WH_hzz": "1.015", "WH_htt": "1.015",  "ZH_htt": "1.015", "ZH_hww": "1.015", "ZH_hzz": "1.015",  "TTWH_htt": "1.015", "TTWH_hww": "1.015", "TTWH_hzz": "1.015",  "TTZH_htt": "1.015", "TTZH_hww": "1.015", "TTZH_hzz": "1.015" },
"lumi_corr":{"WZ": "1.016" , "ZZ": "1.016" , "Rares": "1.016" , "Convs" : "1.016", "ttH_htt":"1.016","ttH_hww":"1.016","ttH_hzz":"1.016","ttH_hzg":"1.016","ttH_hmm": "1.016", "TTW" : "1.016", "tHq_htt":"1.016","tHq_hww":"1.016","tHq_hzz":"1.016","tHW_htt":"1.016","tHW_hww":"1.016","tHW_hzz":"1.016", "TTWW":"1.016", "TTZ": "1.016", "data_fakes": "1.016", "data_flips":"1.016","ggH_hww": "1.016", "ggH_hzz": "1.016", "ggH_htt": "1.016", "qqH_hww": "1.016", "qqH_hzz": "1.016", "qqH_htt": "1.016", "VH_hww":"1.016", "VH_hzz": "1.016", "VH_htt": "1.016", "mcFakes": "1.016", "mcFlips": "1.016", "HH": "1.016",  "WH_hww": "1.016", "WH_hzz": "1.016", "WH_htt": "1.016",  "ZH_htt": "1.016", "ZH_hww": "1.016", "ZH_hzz": "1.016",  "TTWH_htt": "1.016", "TTWH_hww": "1.016", "TTWH_hzz": "1.016",  "TTZH_htt": "1.016", "TTZH_hww": "1.016", "TTZH_hzz": "1.016" },
"pdf_gg":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "0.966", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"pdf_TTWW":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"1.030", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"QCDscale_ttH":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"0.907/1.058","ttH_hww":"0.907/1.058","ttH_hzz":"0.907/1.058","ttH_hzg":"0.907/1.058","ttH_hmm": "0.907/1.058", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"QCDscale_TTWW":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"0.891/1.081", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"CMS_ttHl_QF":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "1.300","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"CMS_ttHl_EWK_4j":{"WZ": "1.300" , "ZZ": "1.300" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"CMS_ttHl_EWK":{"WZ": "1.500" , "ZZ": "1.500" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"CMS_ttHl_WZ_lnU":{"WZ": "1.300" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"CMS_ttHl_ZZ_lnU":{"WZ": "3.000" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"CMS_ttHl_Convs":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "1.500", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"CMS_ttHl_Rares":{"WZ": "-" , "ZZ": "-" , "Rares": "1.500" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"BR_htt":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"1.016","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"1.016","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"1.016","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "1.016", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "1.016", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "1.016", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "1.016",  "ZH_htt": "1.016", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "1.016", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "1.016", "TTZH_hww": "-", "TTZH_hzz": "-" },
"BR_hww":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"1.015","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"1.015","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"1.015","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "1.015", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "1.015", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"1.015", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "1.015", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "1.015", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "1.015", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "1.015", "TTZH_hzz": "-" },
"BR_hzz":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"1.015","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"1.015","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"1.015", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "1.015", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "1.105", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "1.015", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "1.015", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "1.015",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "1.015",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "1.015" },
"BR_hzg":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"1.010","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"BR_hmm":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "1.010", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"CMS_ttHl16_lepEff_mutight":{"WZ": "1.030" , "ZZ": "1.030" , "Rares": "1.030" , "Convs" : "1.030", "ttH_htt":"1.030","ttH_hww":"1.030","ttH_hzz":"1.030","ttH_hzg":"1.030","ttH_hmm": "1.030", "TTW" : "1.030", "tHq_htt":"1.030","tHq_hww":"1.030","tHq_hzz":"1.030","tHW_htt":"1.030","tHW_hww":"1.030","tHW_hzz":"1.030", "TTWW":"1.030", "TTZ": "1.030", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"CMS_ttHl16_lepEff_eltight":{"WZ": "1.030" , "ZZ": "1.030" , "Rares": "1.030" , "Convs" : "1.030", "ttH_htt":"1.030","ttH_hww":"1.030","ttH_hzz":"1.030","ttH_hzg":"1.030","ttH_hmm": "1.030", "TTW" : "1.030", "tHq_htt":"1.030","tHq_hww":"1.030","tHq_hzz":"1.030","tHW_htt":"1.030","tHW_hww":"1.030","tHW_hzz":"1.030", "TTWW":"1.030", "TTZ": "1.030", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"CMS_ttHl17_Clos_e_norm":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "1.100", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"CMS_ttHl17_Clos_e_bt_norm":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "1.100", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"CMS_ttHl17_Clos_m_norm":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "1.100", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"CMS_ttHl17_Clos_m_bt_norm":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "1.150", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"QCDscale_tHq":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"0.933/1.041","tHq_hww":"0.933/1.041","tHq_hzz":"0.933/1.041","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"pdf_tHq":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"1.010","tHq_hww":"1.010","tHq_hzz":"1.010","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"QCDscale_tHW":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"0.939/1.046","tHW_hww":"0.939/1.046","tHW_hzz":"0.939/1.046", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"pdf_tHW":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"1.027","tHW_hww":"1.027","tHW_hzz":"1.027", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"pdf_qg":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"1.010","tHq_hww":"1.010","tHq_hzz":"1.010","tHW_htt":"1.027","tHW_hww":"1.027","tHW_hzz":"1.027", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"CMS_ttHl_WZ_theo":{"WZ": "1.07" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"pdf_WH":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "1.019", "WH_hzz": "1.019", "WH_htt": "1.019",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"QCDscale_WH":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "0.95/1.07", "WH_hzz": "0.95/1.07", "WH_htt": "0.95/1.07",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"pdf_ZH":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "1.016", "ZH_hww": "1.016", "ZH_hzz": "1.016",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"QCDscale_ZH":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "0.962/1.031", "ZH_hww": "0.962/1.031", "ZH_hzz": "0.962/1.031",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"pdf_qqH":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "1.021", "qqH_hzz": "1.021", "qqH_htt": "1.021", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"QCDscale_qqH":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "-", "ggH_hzz": "-", "ggH_htt": "-", "qqH_hww": "0.96/1.03", "qqH_hzz": "0.96/1.03", "qqH_htt": "0.96/1.03", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"pdf_ggH":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "1.031", "ggH_hzz": "1.031", "ggH_htt": "1.031", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
"QCDscale_ggH":{"WZ": "-" , "ZZ": "-" , "Rares": "-" , "Convs" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hzg":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "data_fakes": "-", "data_flips": "-","ggH_hww": "0.924/1.081", "ggH_hzz": "0.924/1.081", "ggH_htt": "0.924/1.081", "qqH_hww": "-", "qqH_hzz": "-", "qqH_htt": "-", "VH_hww":"-", "VH_hzz": "-", "VH_htt": "-", "mcFakes": "-", "mcFlips": "-", "HH": "-",  "WH_hww": "-", "WH_hzz": "-", "WH_htt": "-",  "ZH_htt": "-", "ZH_hww": "-", "ZH_hzz": "-",  "TTWH_htt": "-", "TTWH_hww": "-", "TTWH_hzz": "-",  "TTZH_htt": "-", "TTZH_hww": "-", "TTZH_hzz": "-" },
}

ShapeSysts={
# year dependent
"PU_16": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl16_trigger": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl16_btag_HFStats1": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl16_btag_HFStats2": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl16_btag_LFStats1": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl16_btag_LFStats2": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl16_L1PreFiring": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesRelativeSample_2016": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesBBEC1_2016": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesEC2_2016": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesAbsolute_2016": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesHF_2016": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"PU_17": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl17_trigger": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl17_btag_HFStats1": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl17_btag_HFStats2": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl17_btag_LFStats1": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl17_btag_LFStats2": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl17_L1PreFiring": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesRelativeSample_2017": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesBBEC1_2017": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesEC2_2017": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesAbsolute_2017": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesHF_2017": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"PU_18": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl18_trigger": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl18_btag_HFStats1": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl18_btag_HFStats2": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl18_btag_LFStats1": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl18_btag_LFStats2": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl18_L1PreFiring": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesRelativeSample_2018": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesBBEC1_2018": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesEC2_2018": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesAbsolute_2018": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesHF_2018": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],

# all years
"CMS_ttHl_thu_shape_ttH_x1":["ttH_htt","ttH_hzz","ttH_hww","ttH_hmm","ttH_hzg","tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","TTW","TTZ"],
"CMS_ttHl_thu_shape_ttH_y1":["ttH_htt","ttH_hzz","ttH_hww","ttH_hmm","ttH_hzg","tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","TTW","TTZ"],

"CMS_ttHl_FRm_norm":["data_fakes"],
"CMS_ttHl_FRm_pt":["data_fakes"],
"CMS_ttHl_FRm_be":["data_fakes"],
"CMS_ttHl_Clos_m_shape":["data_fakes"],
"CMS_ttHl_Clos_m_norm":["data_fakes"], #
"CMS_ttHl_FRe_norm":["data_fakes"],
"CMS_ttHl_FRe_pt":["data_fakes"],
"CMS_ttHl_FRe_be":["data_fakes"],
"CMS_ttHl_Clos_e_shape":["data_fakes"],
"CMS_ttHl_Clos_e_norm":["data_fakes"], #

"CMS_ttHl_JER": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl_UnclusteredEn": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesFlavorQCD": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesRelativeBal": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesHF": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesBBEC1": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesEC2": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_scale_j_jesAbsolute": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl_btag_cErr1": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl_btag_cErr2": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl_btag_LF": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl_btag_HF": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],

"CMS_ttHl_lepEff_muloose": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl_lepEff_mutight": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl_lepEff_elloose": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],
"CMS_ttHl_lepEff_eltight": ["Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hzg", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","ggH_hww", "ggH_hzz", "ggH_htt", "qqH_hww", "qqH_hzz", "qqH_htt", "VH_hww", "VH_hzz", "VH_htt","HH", "WH_hww","WH_hzz","WH_htt", "ZH_htt","ZH_hww","ZH_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz", "mcFakes", "mcFlips"],

}



def read_rootfile(samplename, dirOfRootpla):
    ''' read a root file '''
    fullfilename = dirOfRootpla+samplename
    inputfile = TFile(fullfilename,"read")
    return inputfile


def writecard(CardFile, Process , syst, channel, rootfile, errorLog):
    ''' write the line of cards for a specific systmatic '''
    
    likeShape = True
    if not channelSyst.has_key(syst):
        likeShape = False 
    else:
        for chan in channelSyst[syst].keys():
            print (chan)
            if chan in channel or "_bl_" in channel or "ee_" in channel: likeShape = False
    print (syst + " likeShape is " + str(likeShape))

    if YieldSysts.has_key(syst) and not likeShape:
        # find type of systmatic extrapolation
        typeSyst = ""
        for systType in systTypes.keys(): 
            if syst in systTypes[systType]: typeSyst = systType
        
        if len(typeSyst)==0: 
            print (" unkown typeSyst for syst %s"%syst)
            sys.exit()

        stringToWrite = syst + " " + typeSyst + "    " 
        if not syst in channelSyst.keys(): 
            for p in Process:
                # use range because I'm not sure the loop order of using for p in Process 
                # print " I'm writing syst " + syst
                if syst in YearYields.keys():
                    YieldSysts[syst][p] = YearYields[syst][year][p]
                if syst in TH_systs.keys() and YieldSysts[syst][p] != "-" and isTHQ:
                    YieldSysts[syst][p] = TH_systs[syst][Postfix[1:]]
                stringToWrite += YieldSysts[syst][p]+"    "
            print >> CardFile, stringToWrite 
            print (syst + " write the yield ")
        else:
            for chan in channelSyst[syst].keys():
                if chan in channel and channelSyst[syst][chan]!="-":
                    for p in Process:
                        if YieldSysts[syst][p] !="-":
                            stringToWrite += channelSyst[syst][chan]+ "    "
                        else : stringToWrite += "-    "
                    print >> CardFile, stringToWrite 
                    print (syst + " write the channel yield ")
                     

    else:
        stringToWrite = syst + " shape     " 
        if not syst in channelSyst.keys(): 
            for p in Process:
            
                shapeImpact = "-"
                # use range because I'm not sure the loop order of using for p in Process 
                if p in ShapeSysts[syst]: 
                    shapeImpact="1" 
                    # check the up down yield
                    histonameUp = p+"_"+syst+"Up"
                    print histonameUp
                    histoUp = rootfile.Get(histonameUp)
                    yieldUp = round(histoUp.Integral(),3)
                    histonameDown = p+"_"+syst+"Down"
                    histoDown = rootfile.Get(histonameDown)
                    yieldDown = round(histoDown.Integral(),3)
                    nominal = Rates[p]
                    if((yieldUp-nominal)*(yieldDown-nominal))>0:
                        print >> errorLog, "In Channel "+channel+", process "+p+" systematic "+syst+" Up: " +str(yieldUp) + " and Down: " + str(yieldDown) + " at same side of nominal: "+ str(Rates[p])+", please Check"
                stringToWrite += shapeImpact+"    "
            print >> CardFile, stringToWrite
            print (syst + " write the shape ")
        else:
                if not likeShape:
                    for chan in channelSyst[syst].keys():
                        if chan in channel and channelSyst[syst][chan]!="-":
                            for p in Process:
                                if p in ShapeSysts[syst]:
                                    stringToWrite += channelSyst[syst][chan]+ "    "
                                else : stringToWrite += "-    "
                            print >> CardFile, stringToWrite 
                            print (syst + " write the channel shape")
                else:
                    for p in Process:
                        if p in ShapeSysts[syst]:
                            stringToWrite += "1    "
                        else : stringToWrite += "-    "
                    print >> CardFile, stringToWrite 
                    print (syst + " write the channel likeshape")


def writeStatsCard(CardFile, Process , StatsList):
    for p in Process:
        for syst in StatsList[p]:
        # loop over the BinSyst of a given process
            stringToWrite = syst + " shape     " 
            for proc in Process:
                shapeImpact = "-"
                if p == proc: shapeImpact="1"
                stringToWrite += shapeImpact + "    "
            print >> CardFile, stringToWrite

def createStatsList(Region, Process, channel, numberOfBin, rootfile):
    returnStatsList = {}
    for p in Process:
        processSysts=[]
        for i in range(numberOfBin):
            histonameUp = p+"_"+p+"_ttH"+Region+channel+"_template_statbin"+str(i+1)+"Up"
            histoUp = rootfile.Get(histonameUp)
            if histoUp : processSysts.append(p+"_ttH"+Region+channel+"_template_statbin"+str(i+1))
            else : print histonameUp + " not found " 
        returnStatsList[p] = processSysts
    return returnStatsList


def main():
    ''' please make sure the script is running on ROOT>=6 , otherwise you need to add SumW2 when you declare a histograms '''
    for region in Regions:
        if "DiLepRegion" in region: region = "2lss_0tau"
        if cat_str == "SVACat3j": region ="2lss_3j"
        if cat_str == "SVACat2l": region ="2lss_geq4j"
        if 1 > 0: # dummy used for loop
            dirOfRootplas = DirOfRootplas + POI + "/"
            ErrorLog = file(dirOfRootplas+"errorLog.sh","w")
            print "We are now writing region " + region + " using POI "+ POI
            
            for channel in channels:
                # select which samples to loop over for each channel
                yield_data=0.
                if "mm" in channel: samplesToLoop = samplesMM
                elif "ee" in channel: samplesToLoop = samplesEE
                else : samplesToLoop = samples
                
                
                samplesToUse = samplesToLoop[:] 
                print("samplesToUse\n")
                print(samplesToUse)

                    
                # create a txt file to save the template
                TemplateCardsName = dirOfRootplas+Prefix+region+"_"+channel + "_"+ str(year) + Postfix + ".txt"
                TemplateFile = file(TemplateCardsName,"w")
        
                # open and read root file
                filename = Prefix + region + "_" +channel + "_"+str(year) + Postfix + ".root"
                inputfile  = read_rootfile(filename, dirOfRootplas)
                gROOT.cd()
                
                # save rates
                #if useData: 
                h_data = inputfile.Get(h_data_name)
                yield_data = round(h_data.Integral(),3)
                
                print samplesToLoop 
                for sample in samplesToLoop:
                    if inputfile.GetListOfKeys().Contains(sample):
                        hist = inputfile.Get(sample)
                        Rates[sample] = round(hist.Integral(),3)
                    if RemoveZeroSample:
                        if Rates[sample] <0.01: 
                            print ("POI "+ POI +":remove sample "+sample +" because rates[samples] is < 0.01,  integral " + str(Rates[sample] ))
                            samplesToUse.remove(sample)
                        else:
                            for syst in Nuisances:
                                if not ShapeSysts.has_key(syst):continue
                                if sample not in ShapeSysts[syst]:continue
                                histonameUp = sample+"_"+syst+"Up"
                                histoUp = inputfile.Get(histonameUp)
                                yieldUp = round(histoUp.Integral(),5)
                                histonameDown = sample+"_"+syst+"Down"
                                histoDown = inputfile.Get(histonameDown)
                                yieldDown = round(histoDown.Integral(),5)
                                if yieldUp==0 or yieldDown==0:
                                    print histonameUp + "/Down integral " + str(yieldUp)+"/"+str(yieldDown)
                                    print "POI "+ POI +":remove sample "+sample +" because sys"+ syst +" yield Up or Down is " + str(yieldUp)+"/"+str(yieldDown)
                                    samplesToUse.remove(sample)
                                    break
                    #if not useData:
                    #    yield_data += Rates[sample]
                    print "sample "+sample +" integral " + str(Rates[sample] )

                # write begin parts of datacards
                print samplesToLoop 
                print samplesToUse 
                
                print >> TemplateFile, "## Datacard for cut file ttH-multilepton/ttH_"+region+".txt\nshapes *        * "+Prefix+region+"_"+channel+ "_" + str(year) +Postfix +".root $PROCESS $PROCESS_$SYSTEMATIC \n##-------------------------------\nbin       "+Prefix+region+"_"+channel+ "_" + str(year) + Postfix +"\nobservation "+str(yield_data)+"\n##-------------------------------\n##-------------------------------"
        
                binToWrite    ="bin       "
                processToWrite="process   "
                labelToWrite  ="process   "
                rateToWrite   ="rate      "
                
                for sample in samplesToUse:
                    binToWrite += "   "+Prefix+region+"_"+channel + "_" + str(year) +Postfix
                    processToWrite += "             "+sample
                    labelToWrite += "               "+str(Labels[sample])
                    rateToWrite += "                "+str(Rates[sample])
        
        
                print >> TemplateFile, binToWrite 
                print >> TemplateFile, processToWrite 
                print >> TemplateFile, labelToWrite
                print >> TemplateFile, rateToWrite
                print >> TemplateFile, "##------------------------------------"
                
                # write each systematics
                if SystUnc:
                    for syst in Nuisances:
                        writecard(TemplateFile, samplesToUse , syst, channel, inputfile, ErrorLog)
             
                if StatUnc:
                    if not AutoMC: 
                        # create statsBin list 
                        binStatsList = createStatsList(region, samplesToUse, channel, numberOfBins[POI], inputfile)
                
                        # write each BinStats
                        writeStatsCard(TemplateFile, samplesToUse , binStatsList)
                    else:
                        print >> TemplateFile, "* autoMCStats 10 "
                

main()
