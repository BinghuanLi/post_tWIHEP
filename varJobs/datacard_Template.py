#!/usr/bin/env python
import ROOT
from ROOT import TString, TFile, TTree, TCanvas, TH1F, TH1, THStack, TColor, gROOT
from array import array
import sys,os,math
import optparse
import distutils.util

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

usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-v', '--var',        dest='variable'  ,      help='variable name of final discriminator',      default='Bin2l',        type='string')
parser.add_option('-i', '--inDir',        dest='inDir'  ,      help='inDir of histograms',      default='V0212_datacards/',        type='string')
parser.add_option('-c', '--cat',        dest='category'  ,      help='type of channels',      default="SubCat2l",        type='string')
parser.add_option('-s', '--syst', action='store_false',        dest='SystUnc'  ,      help='to exclude systematics',      default=True)
parser.add_option('-m', '--mc', action='store_false',        dest='StatUnc'  ,      help='to exclude stats',      default=True)
parser.add_option('-t', '--template', action='store_false',        dest='ShapeUnc'  ,      help='to exclude shapes',      default=True)

(opt, args) = parser.parse_args()


inDir = opt.inDir
variableName = opt.variable
cat_str = opt.category
SystUnc = opt.SystUnc
StatUnc = opt.StatUnc
ShapeUnc = opt.ShapeUnc


AutoMC = True
RemoveZeroSample = True

channels = subCats[cat_str]
Regions = regPerCat[cat_str]
POI = variableName 
DirOfRootplas = inDir +  cat_str + "/"

#Regions = ["2lss"]


numberOfBins={"Bin2l": 11,"mT_lep2":10,"Hj_tagger":10,"mT_lep1":10,"Dilep_mtWmin":10,"massll":10,"Sum2lCharge":2,"nLooseJet":7,"mht":10,"metLD":10,"Dilep_bestMVA":8,"Dilep_worseMVA":8,"Dilep_pdgId":3,"Dilep_htllv":10,"Dilep_nTight":3,"HighestJetCSV":15,"HtJet":10,"Mt_metleadlep":10,"maxeta":10,"leadLep_jetdr":10,"secondLep_jetdr":10,"minMllAFOS":10,"minMllAFAS":10,"minMllSFOS":10,"nLepFO":6,"nLepTight":6,"puWeight":30,"bWeight":30,"TriggerSF":30,"lepSF":30,"leadLep_BDT":10,"secondLep_BDT":10,"TrueInteractions":100,"nBestVTX":100,"mvaOutput_2lss_ttV":10,"mvaOutput_2lss_ttbar":10,"nBJetLoose":5,"nBJetMedium":5,"lep1_conePt":50,"lep2_conePt":50,"PFMET":40,"PFMETphi":10,"jet1_CSV":10,"jet2_CSV":10,"jet3_CSV":10,"jet4_CSV":10}

Prefix = "ttH_"
Postfix = ".root"

h_data_name ="data_obs"

samplesToUse=[]

samples = [
#"ttH_hww","ttH_hzz","ttH_htt","ttH_hot",
"ttH_hww","ttH_hzz","ttH_htt","ttH_hmm","ttH_hot",
"tHq_hww","tHq_hzz","tHq_htt",
"tHW_hww","tHW_hzz","tHW_htt",
"TTWW","TTW","TTZ","EWK","Rares","Conv","Fakes","Flips"]

samplesMM = [
#"ttH_hww","ttH_hzz","ttH_htt","ttH_hot",
"ttH_hww","ttH_hzz","ttH_htt","ttH_hmm","ttH_hot",
"tHq_hww","tHq_hzz","tHq_htt",
"tHW_hww","tHW_hzz","tHW_htt",
"TTWW","TTW","TTZ","EWK","Rares","Fakes"]

samplesEE = ["ttH_hww","ttH_hzz","ttH_htt","ttH_hot",
"tHq_hww","tHq_hzz","tHq_htt",
"tHW_hww","tHW_hzz","tHW_htt",
"TTWW","TTW","TTZ","EWK","Rares","Conv","Fakes","Flips"]

Rates = {
"Rares":0, "EWK":0, "Conv":0, "TTW":0, "TTWW":0, "TTZ":0, "Fakes":0, "Flips":0, 
"ttH_htt":0,"ttH_hww":0,"ttH_hzz":0,"ttH_hot":0,"ttH_hmm":0,
"tHq_htt":0,"tHq_hww":0,"tHq_hzz":0,
"tHW_htt":0,"tHW_hww":0,"tHW_hzz":0

 }

Labels = {
"Rares":11, "EWK":10, "Conv":12, "TTW":8, "TTWW":7, "TTZ":9, "Fakes":13, "Flips":25, 
"ttH_htt":-7,"ttH_hww":-9,"ttH_hzz":-8,"ttH_hot":-5,"ttH_hmm":-6,
#"tHq_htt":3,"tHq_hww":1,"tHq_hzz":2,
#"tHW_htt":6,"tHW_hww":4,"tHW_hzz":5
"tHq_htt":-13,"tHq_hww":-11,"tHq_hzz":-12,
"tHW_htt":-16,"tHW_hww":-14,"tHW_hzz":-15
 }

### the nuisances that will be written into the datacards
Nuisances =[
"QCDscale_ttW","pdf_Higgs_ttH","pdf_qqbar","QCDscale_ttZ","lumi_13TeV_2017","pdf_gg","QCDscale_ttH","CMS_ttHl_QF","CMS_ttHl_EWK_4j","CMS_ttHl_Convs","CMS_ttHl_Rares","QCDscale_ttWW","pdf_ttWW",
"BR_htt","BR_hvv","BR_hzz","CMS_ttHl16_lepEff_muloose","CMS_ttHl16_lepEff_mutight","CMS_ttHl16_lepEff_elloose","CMS_ttHl16_lepEff_eltight","CMS_ttHl17_Clos_e_norm","CMS_ttHl17_Clos_m_norm","QCDscale_tHq","QCDscale_tHW","pdf_qg","CMS_ttHl17_Clos_e_bt_norm","CMS_ttHl17_Clos_m_bt_norm",
"CMS_ttHl17_trigger","CMS_ttHl17_btag_HFStats1","CMS_ttHl17_btag_HFStats2","CMS_ttHl16_btag_cErr1","CMS_ttHl16_btag_cErr2","CMS_ttHl16_btag_LF","CMS_ttHl16_btag_HF","CMS_ttHl_thu_shape_ttW","CMS_ttHl_thu_shape_ttH","CMS_ttHl_thu_shape_ttZ","CMS_scale_j","CMS_ttHl17_btag_LFStats1","CMS_ttHl17_btag_LFStats2",
"CMS_ttHl16_FRm_norm","CMS_ttHl16_FRm_pt","CMS_ttHl16_FRm_be","CMS_ttHl16_FRe_norm","CMS_ttHl16_FRe_pt","CMS_ttHl16_FRe_be","CMS_ttHl17_Clos_e_shape","CMS_ttHl17_Clos_m_shape",
]
#Nuisances =[
#"CMS_ttHl17_Clos_e_bt_norm",
#]
systTypes={
"lnN":[
"QCDscale_ttW","pdf_Higgs_ttH","pdf_qqbar","QCDscale_ttZ","lumi_13TeV_2017","pdf_gg","QCDscale_ttH","CMS_ttHl_QF","CMS_ttHl_EWK_4j","CMS_ttHl_Convs","CMS_ttHl_Rares","QCDscale_ttWW","pdf_ttWW",
"BR_htt","BR_hvv","BR_hzz","CMS_ttHl16_lepEff_mutight","CMS_ttHl16_lepEff_eltight","CMS_ttHl17_Clos_e_norm","CMS_ttHl17_Clos_m_norm","QCDscale_tHq","QCDscale_tHW","pdf_qg","CMS_ttHl17_Clos_e_bt_norm","CMS_ttHl17_Clos_m_bt_norm",
#"CMS_ttHl16_lepEff_elloose","CMS_ttHl16_lepEff_muloose"
]
}

if not ShapeUnc:
    Nuisances = ["QCDscale_ttW","pdf_Higgs_ttH","pdf_qqbar","QCDscale_ttZ","lumi_13TeV_2017","pdf_gg","QCDscale_ttH","CMS_ttHl_QF","CMS_ttHl_EWK_4j","CMS_ttHl_Convs","CMS_ttHl_Rares","QCDscale_ttWW","pdf_ttWW","BR_htt","BR_hvv","BR_hzz","QCDscale_tHq","QCDscale_tHW","pdf_qg"]

channelSyst={
#"CMS_ttHl16_lepEff_muloose":{"mm":"1.040","em":"1.020","ee":"-"}, #
"CMS_ttHl16_lepEff_mutight":{"mm":"1.060","em":"1.030","ee":"-"}, #
#"CMS_ttHl16_lepEff_elloose":{"mm":"-","em":"1.020","ee":"1.040"}, #
"CMS_ttHl16_lepEff_eltight":{"mm":"-","em":"1.030","ee":"1.060"}, #
"CMS_ttHl17_Clos_e_norm":{"mm":"-","em":"1.100","ee":"1.200"}, #
"CMS_ttHl17_Clos_m_norm":{"mm":"1.200","em":"1.100","ee":"-"}, #
"CMS_ttHl17_Clos_e_bt_norm":{"mm_bt":"-","em_bt":"1.100","ee_bt":"1.200"},#
"CMS_ttHl17_Clos_m_bt_norm":{"mm_bt":"1.300","em_bt":"1.150","ee_bt":"-"},#
"CMS_ttHl17_Clos_e_shape":{"mm":"-","em":"1","ee":"1"},#
"CMS_ttHl17_Clos_m_shape":{"mm":"1","em":"1","ee":"-"},#
"CMS_ttHl16_FRe_norm":{"mm":"-","em":"1","ee":"1"},
"CMS_ttHl16_FRm_norm":{"mm":"1","em":"1","ee":"-"},
"CMS_ttHl16_FRe_pt":{"mm":"-","em":"1","ee":"1"},
"CMS_ttHl16_FRm_pt":{"mm":"1","em":"1","ee":"-"},
"CMS_ttHl16_FRe_be":{"mm":"-","em":"1","ee":"1"},
"CMS_ttHl16_FRm_be":{"mm":"1","em":"1","ee":"-"},
}

YieldSysts={
"QCDscale_ttW":{"EWK": "-" , "Rares": "-" , "Conv" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hot":"-","ttH_hmm": "-", "TTW" : "0.885/1.129", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "Fakes": "-", "Flips": "-"},
"pdf_Higgs_ttH":{"EWK": "-" , "Rares": "-" , "Conv" : "-", "ttH_htt":"1.036","ttH_hww":"1.036","ttH_hzz":"1.036","ttH_hot":"1.036","ttH_hmm": "1.036", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "Fakes": "-", "Flips": "-"},
"pdf_qqbar":{"EWK": "-" , "Rares": "-" , "Conv" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hot":"-","ttH_hmm": "-", "TTW" : "1.040", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "Fakes": "-", "Flips": "-"},
"QCDscale_ttZ":{"EWK": "-" , "Rares": "-" , "Conv" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hot":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "0.904/1.112", "Fakes": "-", "Flips": "-"},
"lumi_13TeV_2017":{"EWK": "1.023" , "Rares": "1.023" , "Conv" : "1.023", "ttH_htt":"1.023","ttH_hww":"1.023","ttH_hzz":"1.023","ttH_hot":"1.023","ttH_hmm": "1.023", "TTW" : "1.023", "tHq_htt":"1.023","tHq_hww":"1.023","tHq_hzz":"1.023","tHW_htt":"1.023","tHW_hww":"1.023","tHW_hzz":"1.023", "TTWW":"1.023", "TTZ": "1.023", "Fakes": "-", "Flips":"-"},
"pdf_gg":{"EWK": "-" , "Rares": "-" , "Conv" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hot":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "0.966", "Fakes": "-", "Flips": "-"},
"pdf_ttWW":{"EWK": "-" , "Rares": "-" , "Conv" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hot":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"1.030", "TTZ": "-", "Fakes": "-", "Flips": "-"},
"QCDscale_ttH":{"EWK": "-" , "Rares": "-" , "Conv" : "-", "ttH_htt":"0.907/1.058","ttH_hww":"0.907/1.058","ttH_hzz":"0.907/1.058","ttH_hot":"0.907/1.058","ttH_hmm": "0.907/1.058", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "Fakes": "-", "Flips": "-"},
"QCDscale_ttWW":{"EWK": "-" , "Rares": "-" , "Conv" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hot":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"0.891/1.081", "TTZ": "-", "Fakes": "-", "Flips": "-"},
"CMS_ttHl_QF":{"EWK": "-" , "Rares": "-" , "Conv" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hot":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "Fakes": "-", "Flips": "1.300"},
"CMS_ttHl_EWK_4j":{"EWK": "2.000" , "Rares": "-" , "Conv" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hot":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "Fakes": "-", "Flips": "-"},
"CMS_ttHl_Convs":{"EWK": "-" , "Rares": "-" , "Conv" : "1.300", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hot":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "Fakes": "-", "Flips": "-"},
"CMS_ttHl_Rares":{"EWK": "-" , "Rares": "1.500" , "Conv" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hot":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "Fakes": "-", "Flips": "-"},
"BR_htt":{"EWK": "-" , "Rares": "-" , "Conv" : "-", "ttH_htt":"1.016","ttH_hww":"-","ttH_hzz":"-","ttH_hot":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "Fakes": "-", "Flips": "-"},
"BR_hvv":{"EWK": "-" , "Rares": "-" , "Conv" : "-", "ttH_htt":"-","ttH_hww":"1.015","ttH_hzz":"-","ttH_hot":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "Fakes": "-", "Flips": "-"},
"BR_hzz":{"EWK": "-" , "Rares": "-" , "Conv" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"1.015","ttH_hot":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "Fakes": "-", "Flips": "-"},
#"CMS_ttHl16_lepEff_muloose":{"EWK": "1.020" , "Rares": "1.020" , "Conv" : "1.020", "ttH_htt":"1.020","ttH_hww":"1.020","ttH_hzz":"1.020","ttH_hot":"1.020","ttH_hmm": "1.020", "TTW" : "1.020", "tHq_htt":"1.020","tHq_hww":"1.020","tHq_hzz":"1.020","tHW_htt":"1.020","tHW_hww":"1.020","tHW_hzz":"1.020", "TTWW":"1.020", "TTZ": "1.020", "Fakes": "-", "Flips": "-"},
"CMS_ttHl16_lepEff_mutight":{"EWK": "1.030" , "Rares": "1.030" , "Conv" : "1.030", "ttH_htt":"1.030","ttH_hww":"1.030","ttH_hzz":"1.030","ttH_hot":"1.030","ttH_hmm": "1.030", "TTW" : "1.030", "tHq_htt":"1.030","tHq_hww":"1.030","tHq_hzz":"1.030","tHW_htt":"1.030","tHW_hww":"1.030","tHW_hzz":"1.030", "TTWW":"1.030", "TTZ": "1.030", "Fakes": "-", "Flips": "-"},
#"CMS_ttHl16_lepEff_elloose":{"EWK": "1.020" , "Rares": "1.020" , "Conv" : "1.020", "ttH_htt":"1.020","ttH_hww":"1.020","ttH_hzz":"1.020","ttH_hot":"1.020","ttH_hmm": "1.020", "TTW" : "1.020", "tHq_htt":"1.020","tHq_hww":"1.020","tHq_hzz":"1.020","tHW_htt":"1.020","tHW_hww":"1.020","tHW_hzz":"1.020", "TTWW":"1.020", "TTZ": "1.020", "Fakes": "-", "Flips": "-"},
"CMS_ttHl16_lepEff_eltight":{"EWK": "1.030" , "Rares": "1.030" , "Conv" : "1.030", "ttH_htt":"1.030","ttH_hww":"1.030","ttH_hzz":"1.030","ttH_hot":"1.030","ttH_hmm": "1.030", "TTW" : "1.030", "tHq_htt":"1.030","tHq_hww":"1.030","tHq_hzz":"1.030","tHW_htt":"1.030","tHW_hww":"1.030","tHW_hzz":"1.030", "TTWW":"1.030", "TTZ": "1.030", "Fakes": "-", "Flips": "-"},
"CMS_ttHl17_Clos_e_norm":{"EWK": "-" , "Rares": "-" , "Conv" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hot":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "Fakes": "1.100", "Flips": "-"},
"CMS_ttHl17_Clos_e_bt_norm":{"EWK": "-" , "Rares": "-" , "Conv" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hot":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "Fakes": "1.100", "Flips": "-"},
"CMS_ttHl17_Clos_m_norm":{"EWK": "-" , "Rares": "-" , "Conv" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hot":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "Fakes": "1.100", "Flips": "-"},
"CMS_ttHl17_Clos_m_bt_norm":{"EWK": "-" , "Rares": "-" , "Conv" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hot":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "Fakes": "1.150", "Flips": "-"},
"QCDscale_tHq":{"EWK": "-" , "Rares": "-" , "Conv" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hot":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"0.933/1.041","tHq_hww":"0.933/1.041","tHq_hzz":"0.933/1.041","tHW_htt":"-","tHW_hww":"-","tHW_hzz":"-", "TTWW":"-", "TTZ": "-", "Fakes": "-", "Flips": "-"},
"QCDscale_tHW":{"EWK": "-" , "Rares": "-" , "Conv" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hot":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"-","tHq_hww":"-","tHq_hzz":"-","tHW_htt":"0.939/1.046","tHW_hww":"0.939/1.046","tHW_hzz":"0.939/1.046", "TTWW":"-", "TTZ": "-", "Fakes": "-", "Flips": "-"},
"pdf_qg":{"EWK": "-" , "Rares": "-" , "Conv" : "-", "ttH_htt":"-","ttH_hww":"-","ttH_hzz":"-","ttH_hot":"-","ttH_hmm": "-", "TTW" : "-", "tHq_htt":"1.010","tHq_hww":"1.010","tHq_hzz":"1.010","tHW_htt":"1.027","tHW_hww":"1.027","tHW_hzz":"1.027", "TTWW":"-", "TTZ": "-", "Fakes": "-", "Flips": "-"},
}

ShapeSysts={
#"PU": ["Rares","EWK","Conv","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hot", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz"],
"CMS_scale_j": ["Rares","EWK","Conv","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hot", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz"],
"CMS_ttHl17_trigger":["Rares","EWK","Conv","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hot", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz"],
"CMS_ttHl17_btag_HFStats1":["Rares","EWK","Conv","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hot", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz"],
"CMS_ttHl17_btag_HFStats2":["Rares","EWK","Conv","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hot", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz"],
"CMS_ttHl16_btag_cErr1":["Rares","EWK","Conv","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hot", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz"],
"CMS_ttHl16_btag_cErr2":["Rares","EWK","Conv","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hot", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz"],
"CMS_ttHl16_btag_LF":["Rares","EWK","Conv","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hot", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz"],
"CMS_ttHl16_btag_HF":["Rares","EWK","Conv","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hot", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz"],
"CMS_ttHl17_btag_LFStats1":["Rares","EWK","Conv","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hot", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz"],
"CMS_ttHl17_btag_LFStats2":["Rares","EWK","Conv","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hot", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz"],
"CMS_ttHl_thu_shape_ttW":["TTW"],
"CMS_ttHl_thu_shape_ttH":["ttH_htt","ttH_hzz","ttH_hww","ttH_hmm","ttH_hot"],
"CMS_ttHl_thu_shape_ttZ":["TTZ"],

"CMS_ttHl16_FRm_norm":["Fakes"],
"CMS_ttHl16_FRm_pt":["Fakes"],
"CMS_ttHl16_FRm_be":["Fakes"],
"CMS_ttHl17_Clos_m_shape":["Fakes"],
"CMS_ttHl16_FRe_norm":["Fakes"],
"CMS_ttHl16_FRe_pt":["Fakes"],
"CMS_ttHl16_FRe_be":["Fakes"],
"CMS_ttHl17_Clos_e_shape":["Fakes"],

"CMS_ttHl16_lepEff_muloose":["Rares","EWK","Conv","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hot", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz"], #
"CMS_ttHl16_lepEff_mutight":["Rares","EWK","Conv","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hot", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz"], #
"CMS_ttHl16_lepEff_elloose":["Rares","EWK","Conv","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hot", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz"], #
"CMS_ttHl16_lepEff_eltight":["Rares","EWK","Conv","TTW","TTZ","TTWW","ttH_htt","ttH_hww","ttH_hzz","ttH_hmm","ttH_hot", "tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz"], #
"CMS_ttHl17_Clos_e_norm":["Fakes"], #
"CMS_ttHl17_Clos_m_norm":["Fakes"], #
"CMS_ttHl17_Clos_e_bt_norm":["Fakes"],#
"CMS_ttHl17_Clos_m_bt_norm":["Fakes"],#
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
        for systType in systTypes.keys(): 
            if syst in systTypes[systType]: typeSyst = systType
        
        stringToWrite = syst + " " + systType + "    " 
        if not syst in channelSyst.keys(): 
            for p in Process:
                # use range because I'm not sure the loop order of using for p in Process 
                # print " I'm writing syst " + syst
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

                # create a txt file to save the template
                TemplateCardsName = dirOfRootplas+Prefix+region+"_"+channel + ".txt"
                TemplateFile = file(TemplateCardsName,"w")
        
                # open and read root file
                filename = Prefix + region + "_" +channel + Postfix
                inputfile  = read_rootfile(filename, dirOfRootplas)
                gROOT.cd()
                
                # save rates 
                h_data = inputfile.Get(h_data_name)
                yield_data = round(h_data.Integral(),1)
                
                print samplesToLoop 
                for sample in samplesToLoop:
                    if inputfile.GetListOfKeys().Contains(sample):
                        hist = inputfile.Get(sample)
                        Rates[sample] = round(hist.Integral(),3)
                    if RemoveZeroSample:
                        if Rates[sample] ==0: 
                            print "POI "+ POI +":remove sample "+sample +" because rates[samples] is 0,  integral " + str(Rates[sample] )
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

                    else: print "sample "+sample +" integral " + str(Rates[sample] )

                # write begin parts of datacards
                print samplesToLoop 
                print samplesToUse 
                
                print >> TemplateFile, "## Datacard for cut file ttH-multilepton/2lss_tight.txt\nshapes *        * ttH_"+region+"_"+channel+".root $PROCESS $PROCESS_$SYSTEMATIC \n##-------------------------------\nbin       ttH_"+region+"_"+channel+"\nobservation "+str(yield_data)+"\n##-------------------------------\n##-------------------------------"
        
                binToWrite    ="bin       "
                processToWrite="process   "
                labelToWrite  ="process   "
                rateToWrite   ="rate      "
                
                for sample in samplesToUse:
                    binToWrite += "   ttH_"+region+"_"+channel
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
