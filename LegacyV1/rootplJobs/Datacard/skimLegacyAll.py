import sys, os, subprocess
import commands
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread

print ( "\n ------------------------ \n  please remember to separate VH into WH and ZH \n ----------------------------- \n")


frameworkDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/LegacyV1/"
BaseDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplas_LegacyAll_20191025/"

#Regions=["DiLepRegion"]#"TriLepRegion","QuaLepRegion","ttZctrl","WZctrl","QuaLepRegion","ZZctrl"]
Regions=["DiLepRegion","TriLepRegion","QuaLepRegion","ttZctrl","WZctrl","QuaLepRegion","ZZctrl"]

Selections=["datafakes", "dataflips", "prompt", "mcfakes", "mcflips", "fakesub", "dataobs", "conv"]

#DirOfRegions = ["ttH2018All2L","ttH2018All3L","ttH2018All4L"]

DirOfRegions = [
"ttH2016Data2L","ttH2016All2L","ttH2017Data2L","ttH2017All2L","ttH2018Data2L","ttH2018All2L",
"ttH2016Data3L","ttH2016All3L","ttH2017Data3L","ttH2017All3L","ttH2018Data3L","ttH2018All3L",
"ttH2016Data4L","ttH2016All4L","ttH2017Data4L","ttH2017All4L","ttH2018Data4L","ttH2018All4L"
]

HiggsDecay = {"hww":2,"hzz":6,"htt":3, "hmm":11, "hzg":7} # hot:999

HiggsProcess = ["qqH","ggH","VH","ZH","TTH","THQ","THW","ttH"]
#ProcessesAll = ["THW"]
#ProcessesJES = ["THW"]
ProcessesAll = [ "TTH","THQ", "THW", "VH", "ZH", "ggH", "qqH", "TTZ", "TTW", "Convs", "WZ", "ZZ", "Rares","TTWW","ST","FakeSub","Fakes","Flips", "mcFlips", "mcFakes", "Data","EWK","ttH","TT"]
ProcessesJES = [ "TTH","THQ", "THW", "VH", "ZH", "ggH", "qqH", "TTZ", "TTW", "Convs", "WZ", "ZZ", "Rares","TTWW","ST","FakeSub","mcFlips", "mcFakes","EWK","ttH","TT"]
ProcessesData = ["Fakes","Flips","Data"] 
#ProcessesData = [] 

Samples= {
"2016":{
"TTH":["Legacy16V1_ttHnobb"],
"ttH":["Legacy16V1_TTH_ctcvcp"],
"THQ":["Legacy16V1_THQ_TuneCP5_ctcvcp"],
"THW":["Legacy16V1_THW_TuneCP5_ctcvcp"],
"VH":["Legacy16V1_VHToNonbb"],
"ZH":["Legacy16V1_ZHTobb","Legacy16V1_ZHToTauTau"],
"ggH":["Legacy16V1_ggHToTauTau_v3","Legacy16V1_ggHToZZTo4L","Legacy16V1_ggHToWWToLNuQQ","Legacy16V1_ggHToWWTo2L2Nu","Legacy16V1_ggHToMuMu","Legacy16V1_ggHToBB_v2","Legacy16V1_ggHToBB_ext1","Legacy16V1_ggHToGG"],
"qqH":["Legacy16V1_VBFHToTauTau","Legacy16V1_VBFHToZZTo4L","Legacy16V1_VBFHToWWToLNuQQ","Legacy16V1_VBFHToWWTo2L2Nu","Legacy16V1_VBFHToMuMu","Legacy16V1_VBFHToBB_v1","Legacy16V1_VBFHToBB_ext1","Legacy16V1_VBFHToGG_ext1","Legacy16V1_VBFHToGG_ext2"],
"TTZ":["Legacy16V1_TTZ_M1to10","Legacy16V1_TTZ_M10_ext1","Legacy16V1_TTZ_M10_ext2","Legacy16V1_TTJets_DiLep_v1","Legacy16V1_TTJets_DiLep_ext","Legacy16V1_TTJets_TToSingleLep_v1","Legacy16V1_TTJets_TToSingleLep_ext","Legacy16V1_TTJets_TbarToSingleLep_v1","Legacy16V1_TTJets_TbarToSingleLep_ext"],
"TT":["Legacy16V1_TTJets_DiLep_v1","Legacy16V1_TTJets_DiLep_ext","Legacy16V1_TTJets_TToSingleLep_v1","Legacy16V1_TTJets_TToSingleLep_ext","Legacy16V1_TTJets_TbarToSingleLep_v1","Legacy16V1_TTJets_TbarToSingleLep_ext"],
"TTW":["Legacy16V1_TTWJets"],
"TTWW":["Legacy16V1_TTWW"],
"ST":["Legacy16V1_ST_sCh_lepDecay_PS","Legacy16V1_ST_tCh_top","Legacy16V1_ST_tCh_antitop_PS","Legacy16V1_ST_tW_top","Legacy16V1_ST_tW_antitop"],
"EWK":["Legacy16V1_WWTo2LNu","Legacy16V1_WJets_v1","Legacy16V1_WJets_ext","Legacy16V1_DYJets_M50","Legacy16V1_DYJets_M10to50"],
"WZ":["Legacy16V1_WZTo3LNu"],
"ZZ":["Legacy16V1_ZZTo4L"],
"Convs":['Legacy16V1_TTGJets_v1', 'Legacy16V1_TTGJets_ext', 'Legacy16V1_TGJetsLep', 'Legacy16V1_WGToLNuG_ext1', 'Legacy16V1_WGToLNuG_ext2', 'Legacy16V1_WGToLNuG_ext3', 'Legacy16V1_ZGToLLG', 'Legacy16V1_DYJets_M10to50', 'Legacy16V1_DYJets_M50', 'Legacy16V1_WZG','Legacy16V1_WJets_v1','Legacy16V1_WJets_ext'],
"Rares":["Legacy16V1_tWll","Legacy16V1_WW_DS","Legacy16V1_WWW","Legacy16V1_WWZ","Legacy16V1_WZZ","Legacy16V1_ZZZ","Legacy16V1_TTTT","Legacy16V1_tZq_PS","Legacy16V1_WpWpJJ"],
"mcFakes":["Legacy16V1_ttHnobb","Legacy16V1_VHToNonbb","Legacy16V1_THQ_TuneCP5_ctcvcp","Legacy16V1_THW_TuneCP5_ctcvcp","Legacy16V1_VHToNonbb","Legacy16V1_ZHTobb","Legacy16V1_ZHToTauTau","Legacy16V1_ggHToTauTau_v3","Legacy16V1_ggHToZZTo4L","Legacy16V1_ggHToWWToLNuQQ","Legacy16V1_ggHToWWTo2L2Nu","Legacy16V1_ggHToMuMu","Legacy16V1_ggHToBB_v2","Legacy16V1_ggHToBB_ext1","Legacy16V1_ggHToGG","Legacy16V1_VBFHToTauTau","Legacy16V1_VBFHToZZTo4L","Legacy16V1_VBFHToWWToLNuQQ","Legacy16V1_VBFHToWWTo2L2Nu","Legacy16V1_VBFHToMuMu","Legacy16V1_VBFHToBB_v1","Legacy16V1_VBFHToBB_ext1","Legacy16V1_VBFHToGG_ext1","Legacy16V1_VBFHToGG_ext2","Legacy16V1_TTZ_M1to10","Legacy16V1_TTZ_M10_ext1","Legacy16V1_TTZ_M10_ext2","Legacy16V1_TTJets_DiLep_v1","Legacy16V1_TTJets_DiLep_ext","Legacy16V1_TTJets_TToSingleLep_v1","Legacy16V1_TTJets_TToSingleLep_ext","Legacy16V1_TTJets_TbarToSingleLep_v1","Legacy16V1_TTJets_TbarToSingleLep_ext","Legacy16V1_TTWJets","Legacy16V1_TTWW","Legacy16V1_WWTo2LNu","Legacy16V1_WJets_v1","Legacy16V1_WJets_ext","Legacy16V1_DYJets_M50","Legacy16V1_DYJets_M10to50","Legacy16V1_WZTo3LNu","Legacy16V1_ZZTo4L","Legacy16V1_tWll","Legacy16V1_WW_DS","Legacy16V1_WWW","Legacy16V1_WWZ","Legacy16V1_WZZ","Legacy16V1_ZZZ","Legacy16V1_TTTT","Legacy16V1_tZq_PS","Legacy16V1_WpWpJJ","Legacy16V1_ST_sCh_lepDecay_PS","Legacy16V1_ST_tCh_top","Legacy16V1_ST_tCh_antitop_PS","Legacy16V1_ST_tW_top","Legacy16V1_ST_tW_antitop"],
"mcFlips":["Legacy16V1_ttHnobb","Legacy16V1_VHToNonbb","Legacy16V1_THQ_TuneCP5_ctcvcp","Legacy16V1_THW_TuneCP5_ctcvcp","Legacy16V1_VHToNonbb","Legacy16V1_ZHTobb","Legacy16V1_ZHToTauTau","Legacy16V1_ggHToTauTau_v3","Legacy16V1_ggHToZZTo4L","Legacy16V1_ggHToWWToLNuQQ","Legacy16V1_ggHToWWTo2L2Nu","Legacy16V1_ggHToMuMu","Legacy16V1_ggHToBB_v2","Legacy16V1_ggHToBB_ext1","Legacy16V1_ggHToGG","Legacy16V1_VBFHToTauTau","Legacy16V1_VBFHToZZTo4L","Legacy16V1_VBFHToWWToLNuQQ","Legacy16V1_VBFHToWWTo2L2Nu","Legacy16V1_VBFHToMuMu","Legacy16V1_VBFHToBB_v1","Legacy16V1_VBFHToBB_ext1","Legacy16V1_VBFHToGG_ext1","Legacy16V1_VBFHToGG_ext2","Legacy16V1_TTZ_M1to10","Legacy16V1_TTZ_M10_ext1","Legacy16V1_TTZ_M10_ext2","Legacy16V1_TTJets_DiLep_v1","Legacy16V1_TTJets_DiLep_ext","Legacy16V1_TTJets_TToSingleLep_v1","Legacy16V1_TTJets_TToSingleLep_ext","Legacy16V1_TTJets_TbarToSingleLep_v1","Legacy16V1_TTJets_TbarToSingleLep_ext","Legacy16V1_TTWJets","Legacy16V1_TTWW","Legacy16V1_WWTo2LNu","Legacy16V1_WJets_v1","Legacy16V1_WJets_ext","Legacy16V1_DYJets_M50","Legacy16V1_DYJets_M10to50","Legacy16V1_WZTo3LNu","Legacy16V1_ZZTo4L","Legacy16V1_tWll","Legacy16V1_WW_DS","Legacy16V1_WWW","Legacy16V1_WWZ","Legacy16V1_WZZ","Legacy16V1_ZZZ","Legacy16V1_TTTT","Legacy16V1_tZq_PS","Legacy16V1_WpWpJJ","Legacy16V1_ST_sCh_lepDecay_PS","Legacy16V1_ST_tCh_top","Legacy16V1_ST_tCh_antitop_PS","Legacy16V1_ST_tW_top","Legacy16V1_ST_tW_antitop"],
"Data":['Legacy16V1_SEleBlockB', 'Legacy16V1_SEleBlockC', 'Legacy16V1_SEleBlockD', 'Legacy16V1_SEleBlockE', 'Legacy16V1_SEleBlockF', 'Legacy16V1_SEleBlockG', 'Legacy16V1_SEleBlockH', 'Legacy16V1_SMuBlockB', 'Legacy16V1_SMuBlockC', 'Legacy16V1_SMuBlockD',
'Legacy16V1_SMuBlockE', 'Legacy16V1_SMuBlockF', 'Legacy16V1_SMuBlockG', 'Legacy16V1_SMuBlockH', 'Legacy16V1_DblEGBlockB', 'Legacy16V1_DblEGBlockC', 'Legacy16V1_DblEGBlockD', 'Legacy16V1_DblEGBlockE', 'Legacy16V1_DblEGBlockF', 'Legacy16V1_DblEGBlockG',
'Legacy16V1_DblEGBlockH', 'Legacy16V1_DblMuBlockB', 'Legacy16V1_DblMuBlockC', 'Legacy16V1_DblMuBlockD', 'Legacy16V1_DblMuBlockE', 'Legacy16V1_DblMuBlockF', 'Legacy16V1_DblMuBlockG', 'Legacy16V1_DblMuBlockH', 'Legacy16V1_MuEGBlockB', 'Legacy16V1_MuEGBlockC',
'Legacy16V1_MuEGBlockD', 'Legacy16V1_MuEGBlockE', 'Legacy16V1_MuEGBlockF', 'Legacy16V1_MuEGBlockG', 'Legacy16V1_MuEGBlockH',],
"FakeSub":["Legacy16V1_ttHnobb","Legacy16V1_VHToNonbb","Legacy16V1_THQ_TuneCP5_ctcvcp","Legacy16V1_THW_TuneCP5_ctcvcp","Legacy16V1_VHToNonbb","Legacy16V1_ZHTobb","Legacy16V1_ZHToTauTau","Legacy16V1_ggHToTauTau_v3","Legacy16V1_ggHToZZTo4L","Legacy16V1_ggHToWWToLNuQQ","Legacy16V1_ggHToWWTo2L2Nu","Legacy16V1_ggHToMuMu","Legacy16V1_ggHToBB_v2","Legacy16V1_ggHToBB_ext1","Legacy16V1_ggHToGG","Legacy16V1_VBFHToTauTau","Legacy16V1_VBFHToZZTo4L","Legacy16V1_VBFHToWWToLNuQQ","Legacy16V1_VBFHToWWTo2L2Nu","Legacy16V1_VBFHToMuMu","Legacy16V1_VBFHToBB_v1","Legacy16V1_VBFHToBB_ext1","Legacy16V1_VBFHToGG_ext1","Legacy16V1_VBFHToGG_ext2","Legacy16V1_TTZ_M1to10","Legacy16V1_TTZ_M10_ext1","Legacy16V1_TTZ_M10_ext2","Legacy16V1_TTJets_DiLep_v1","Legacy16V1_TTJets_DiLep_ext","Legacy16V1_TTJets_TToSingleLep_v1","Legacy16V1_TTJets_TToSingleLep_ext","Legacy16V1_TTJets_TbarToSingleLep_v1","Legacy16V1_TTJets_TbarToSingleLep_ext","Legacy16V1_TTWJets","Legacy16V1_TTWW","Legacy16V1_WWTo2LNu","Legacy16V1_WJets_v1","Legacy16V1_WJets_ext","Legacy16V1_DYJets_M50","Legacy16V1_DYJets_M10to50","Legacy16V1_WZTo3LNu","Legacy16V1_ZZTo4L","Legacy16V1_tWll","Legacy16V1_WW_DS","Legacy16V1_WWW","Legacy16V1_WWZ","Legacy16V1_WZZ","Legacy16V1_ZZZ","Legacy16V1_TTTT","Legacy16V1_tZq_PS","Legacy16V1_WpWpJJ","Legacy16V1_ST_sCh_lepDecay_PS","Legacy16V1_ST_tCh_top","Legacy16V1_ST_tCh_antitop_PS","Legacy16V1_ST_tW_top","Legacy16V1_ST_tW_antitop"],
"Fakes":['Legacy16V1_SEleBlockB', 'Legacy16V1_SEleBlockC', 'Legacy16V1_SEleBlockD', 'Legacy16V1_SEleBlockE', 'Legacy16V1_SEleBlockF', 'Legacy16V1_SEleBlockG', 'Legacy16V1_SEleBlockH', 'Legacy16V1_SMuBlockB', 'Legacy16V1_SMuBlockC', 'Legacy16V1_SMuBlockD',
'Legacy16V1_SMuBlockE', 'Legacy16V1_SMuBlockF', 'Legacy16V1_SMuBlockG', 'Legacy16V1_SMuBlockH', 'Legacy16V1_DblEGBlockB', 'Legacy16V1_DblEGBlockC', 'Legacy16V1_DblEGBlockD', 'Legacy16V1_DblEGBlockE', 'Legacy16V1_DblEGBlockF', 'Legacy16V1_DblEGBlockG',
'Legacy16V1_DblEGBlockH', 'Legacy16V1_DblMuBlockB', 'Legacy16V1_DblMuBlockC', 'Legacy16V1_DblMuBlockD', 'Legacy16V1_DblMuBlockE', 'Legacy16V1_DblMuBlockF', 'Legacy16V1_DblMuBlockG', 'Legacy16V1_DblMuBlockH', 'Legacy16V1_MuEGBlockB', 'Legacy16V1_MuEGBlockC',
'Legacy16V1_MuEGBlockD', 'Legacy16V1_MuEGBlockE', 'Legacy16V1_MuEGBlockF', 'Legacy16V1_MuEGBlockG', 'Legacy16V1_MuEGBlockH',],
"Flips":['Legacy16V1_SEleBlockB', 'Legacy16V1_SEleBlockC', 'Legacy16V1_SEleBlockD', 'Legacy16V1_SEleBlockE', 'Legacy16V1_SEleBlockF', 'Legacy16V1_SEleBlockG', 'Legacy16V1_SEleBlockH', 'Legacy16V1_SMuBlockB', 'Legacy16V1_SMuBlockC', 'Legacy16V1_SMuBlockD',
'Legacy16V1_SMuBlockE', 'Legacy16V1_SMuBlockF', 'Legacy16V1_SMuBlockG', 'Legacy16V1_SMuBlockH', 'Legacy16V1_DblEGBlockB', 'Legacy16V1_DblEGBlockC', 'Legacy16V1_DblEGBlockD', 'Legacy16V1_DblEGBlockE', 'Legacy16V1_DblEGBlockF', 'Legacy16V1_DblEGBlockG',
'Legacy16V1_DblEGBlockH', 'Legacy16V1_DblMuBlockB', 'Legacy16V1_DblMuBlockC', 'Legacy16V1_DblMuBlockD', 'Legacy16V1_DblMuBlockE', 'Legacy16V1_DblMuBlockF', 'Legacy16V1_DblMuBlockG', 'Legacy16V1_DblMuBlockH', 'Legacy16V1_MuEGBlockB', 'Legacy16V1_MuEGBlockC',
'Legacy16V1_MuEGBlockD', 'Legacy16V1_MuEGBlockE', 'Legacy16V1_MuEGBlockF', 'Legacy16V1_MuEGBlockG', 'Legacy16V1_MuEGBlockH',],
},
"2017":{
"TTH":["Legacy17V1_ttHnobb"],
"THQ":["Legacy17V1_THQ_ctcvcp"], 
"THW":["Legacy17V1_THW_ctcvcp"], 
"VH":["Legacy17V1_VHToNonbb"], 
"ZH":["Legacy17V1_ZHTobb","Legacy17V1_ZHToTauTau",], 
"ggH":["Legacy17V1_GGHToTauTau_v1","Legacy17V1_GGHToTauTau_ext","Legacy17V1_ggHToZZTo4L_ext1","Legacy17V1_ggHToZZTo4L_ext3","Legacy17V1_ggHToZZTo4L_ext4","Legacy17V1_ggHToZZTo2L2Q","Legacy17V1_ggHToWWToLNuQQ","Legacy17V1_ggHToWWTo2L2Nu","Legacy17V1_ggHToMuMu_v1","Legacy17V1_ggHToMuMu_ext1","Legacy17V1_ggHToBB","Legacy17V1_ggHToGG"], 
"qqH":["Legacy17V1_VBFHToTauTau","Legacy17V1_VBFHToZZTo4L_ext2","Legacy17V1_VBFHToZZTo4L_ext1","Legacy17V1_VBFHToZZTo4L_v1","Legacy17V1_VBFHToWWToLNuQQ","Legacy17V1_VBFHToWWTo2L2Nu","Legacy17V1_VBFHToMuMu","Legacy17V1_VBFHToBB","Legacy17V1_VBFHToGG"], 
"TTZ":["Legacy17V1_TTZ_M1to10","Legacy17V1_TTZ_M10_PS","Legacy17V1_TTJets_DiLep","Legacy17V1_TTJets_TToSingleLep","Legacy17V1_TTJets_TbarToSingleLep"],
"TT":["Legacy17V1_TTJets_DiLep","Legacy17V1_TTJets_TToSingleLep","Legacy17V1_TTJets_TbarToSingleLep"], 
"TTW":["Legacy17V1_TTW_PS"], 
"Convs":["Legacy17V1_TTGJets_v1","Legacy17V1_TTGJets_ext","Legacy17V1_TGJetsLep","Legacy17V1_WGToLNuG_Tune","Legacy17V1_ZGToLLG_01J","Legacy17V1_W1JetsToLNu","Legacy17V1_W2JetsToLNu","Legacy17V1_W3JetsToLNu","Legacy17V1_W4JetsToLNu","Legacy17V1_DYJets_M10to50_v1","Legacy17V1_DYJets_M10to50_ext","Legacy17V1_DYJets_M50_v1","Legacy17V1_DYJets_M50_ext","Legacy17V1_WZG"], 
"WZ":["Legacy17V1_WZTo3LNu"], 
"ZZ":["Legacy17V1_ZZTo4L_v1","Legacy17V1_ZZTo4L_ext1","Legacy17V1_ZZTo4L_ext2"], 
"Rares":["Legacy17V1_tWll","Legacy17V1_WW_DS","Legacy17V1_WWW","Legacy17V1_WWZ","Legacy17V1_WZZ","Legacy17V1_ZZZ","Legacy17V1_TTTT","Legacy17V1_TTTT_PS","Legacy17V1_tZq","Legacy17V1_WpWpJJ"],
"TTWW":["Legacy17V1_TTWW"],
"ST":["Legacy17V1_ST_sCh_lepDecay_PS","Legacy17V1_ST_tCh_top_PS","Legacy17V1_ST_tCh_antitop_PS","Legacy17V1_ST_tW_top_PS","Legacy17V1_ST_tW_antitop_PS",],
"FakeSub":["Legacy17V1_ttHnobb","Legacy17V1_THQ_ctcvcp","Legacy17V1_THW_ctcvcp","Legacy17V1_VHToNonbb","Legacy17V1_ZHTobb","Legacy17V1_ZHToTauTau","Legacy17V1_GGHToTauTau_v1","Legacy17V1_GGHToTauTau_ext","Legacy17V1_ggHToZZTo4L_ext1","Legacy17V1_ggHToZZTo4L_ext3","Legacy17V1_ggHToZZTo4L_ext4","Legacy17V1_ggHToZZTo2L2Q","Legacy17V1_ggHToWWToLNuQQ","Legacy17V1_ggHToWWTo2L2Nu","Legacy17V1_ggHToMuMu_v1","Legacy17V1_ggHToMuMu_ext1","Legacy17V1_ggHToBB","Legacy17V1_ggHToGG","Legacy17V1_VBFHToTauTau","Legacy17V1_VBFHToZZTo4L_ext2","Legacy17V1_VBFHToZZTo4L_ext1","Legacy17V1_VBFHToZZTo4L_v1","Legacy17V1_VBFHToWWToLNuQQ","Legacy17V1_VBFHToWWTo2L2Nu","Legacy17V1_VBFHToMuMu","Legacy17V1_VBFHToBB","Legacy17V1_VBFHToGG","Legacy17V1_TTZ_M1to10","Legacy17V1_TTZ_M10_PS","Legacy17V1_TTJets_DiLep","Legacy17V1_TTJets_TToSingleLep","Legacy17V1_TTJets_TbarToSingleLep","Legacy17V1_TTW_PS","Legacy17V1_WZTo3LNu","Legacy17V1_ZZTo4L_v1","Legacy17V1_ZZTo4L_ext1","Legacy17V1_ZZTo4L_ext2","Legacy17V1_tWll","Legacy17V1_WW_DS","Legacy17V1_WWW","Legacy17V1_WWZ","Legacy17V1_WZZ","Legacy17V1_ZZZ","Legacy17V1_TTTT","Legacy17V1_TTTT_PS","Legacy17V1_tZq","Legacy17V1_WpWpJJ","Legacy17V1_TTWW","Legacy17V1_ST_sCh_lepDecay_PS","Legacy17V1_ST_tCh_top_PS","Legacy17V1_ST_tCh_antitop_PS","Legacy17V1_ST_tW_top_PS","Legacy17V1_ST_tW_antitop_PS","Legacy17V1_WWTo2LNu_v1","Legacy17V1_WWTo2LNu_ext","Legacy17V1_WJets_v1","Legacy17V1_WJets_ext","Legacy17V1_DYJets_M10to50_v1","Legacy17V1_DYJets_M10to50_ext","Legacy17V1_DYJets_M50_v1","Legacy17V1_DYJets_M50_ext"],
"mcFlips":["Legacy17V1_ttHnobb","Legacy17V1_THQ_ctcvcp","Legacy17V1_THW_ctcvcp","Legacy17V1_VHToNonbb","Legacy17V1_ZHTobb","Legacy17V1_ZHToTauTau","Legacy17V1_GGHToTauTau_v1","Legacy17V1_GGHToTauTau_ext","Legacy17V1_ggHToZZTo4L_ext1","Legacy17V1_ggHToZZTo4L_ext3","Legacy17V1_ggHToZZTo4L_ext4","Legacy17V1_ggHToZZTo2L2Q","Legacy17V1_ggHToWWToLNuQQ","Legacy17V1_ggHToWWTo2L2Nu","Legacy17V1_ggHToMuMu_v1","Legacy17V1_ggHToMuMu_ext1","Legacy17V1_ggHToBB","Legacy17V1_ggHToGG","Legacy17V1_VBFHToTauTau","Legacy17V1_VBFHToZZTo4L_ext2","Legacy17V1_VBFHToZZTo4L_ext1","Legacy17V1_VBFHToZZTo4L_v1","Legacy17V1_VBFHToWWToLNuQQ","Legacy17V1_VBFHToWWTo2L2Nu","Legacy17V1_VBFHToMuMu","Legacy17V1_VBFHToBB","Legacy17V1_VBFHToGG","Legacy17V1_TTZ_M1to10","Legacy17V1_TTZ_M10_PS","Legacy17V1_TTJets_DiLep","Legacy17V1_TTJets_TToSingleLep","Legacy17V1_TTJets_TbarToSingleLep","Legacy17V1_TTW_PS","Legacy17V1_WZTo3LNu","Legacy17V1_ZZTo4L_v1","Legacy17V1_ZZTo4L_ext1","Legacy17V1_ZZTo4L_ext2","Legacy17V1_tWll","Legacy17V1_WW_DS","Legacy17V1_WWW","Legacy17V1_WWZ","Legacy17V1_WZZ","Legacy17V1_ZZZ","Legacy17V1_TTTT","Legacy17V1_TTTT_PS","Legacy17V1_tZq","Legacy17V1_WpWpJJ","Legacy17V1_TTWW","Legacy17V1_ST_sCh_lepDecay_PS","Legacy17V1_ST_tCh_top_PS","Legacy17V1_ST_tCh_antitop_PS","Legacy17V1_ST_tW_top_PS","Legacy17V1_ST_tW_antitop_PS","Legacy17V1_WWTo2LNu_v1","Legacy17V1_WWTo2LNu_ext","Legacy17V1_WJets_v1","Legacy17V1_WJets_ext","Legacy17V1_DYJets_M10to50_v1","Legacy17V1_DYJets_M10to50_ext","Legacy17V1_DYJets_M50_v1","Legacy17V1_DYJets_M50_ext"],
"mcFakes":["Legacy17V1_ttHnobb","Legacy17V1_THQ_ctcvcp","Legacy17V1_THW_ctcvcp","Legacy17V1_VHToNonbb","Legacy17V1_ZHTobb","Legacy17V1_ZHToTauTau","Legacy17V1_GGHToTauTau_v1","Legacy17V1_GGHToTauTau_ext","Legacy17V1_ggHToZZTo4L_ext1","Legacy17V1_ggHToZZTo4L_ext3","Legacy17V1_ggHToZZTo4L_ext4","Legacy17V1_ggHToZZTo2L2Q","Legacy17V1_ggHToWWToLNuQQ","Legacy17V1_ggHToWWTo2L2Nu","Legacy17V1_ggHToMuMu_v1","Legacy17V1_ggHToMuMu_ext1","Legacy17V1_ggHToBB","Legacy17V1_ggHToGG","Legacy17V1_VBFHToTauTau","Legacy17V1_VBFHToZZTo4L_ext2","Legacy17V1_VBFHToZZTo4L_ext1","Legacy17V1_VBFHToZZTo4L_v1","Legacy17V1_VBFHToWWToLNuQQ","Legacy17V1_VBFHToWWTo2L2Nu","Legacy17V1_VBFHToMuMu","Legacy17V1_VBFHToBB","Legacy17V1_VBFHToGG","Legacy17V1_TTZ_M1to10","Legacy17V1_TTZ_M10_PS","Legacy17V1_TTJets_DiLep","Legacy17V1_TTJets_TToSingleLep","Legacy17V1_TTJets_TbarToSingleLep","Legacy17V1_TTW_PS","Legacy17V1_WZTo3LNu","Legacy17V1_ZZTo4L_v1","Legacy17V1_ZZTo4L_ext1","Legacy17V1_ZZTo4L_ext2","Legacy17V1_tWll","Legacy17V1_WW_DS","Legacy17V1_WWW","Legacy17V1_WWZ","Legacy17V1_WZZ","Legacy17V1_ZZZ","Legacy17V1_TTTT","Legacy17V1_TTTT_PS","Legacy17V1_tZq","Legacy17V1_WpWpJJ","Legacy17V1_TTWW","Legacy17V1_ST_sCh_lepDecay_PS","Legacy17V1_ST_tCh_top_PS","Legacy17V1_ST_tCh_antitop_PS","Legacy17V1_ST_tW_top_PS","Legacy17V1_ST_tW_antitop_PS","Legacy17V1_WWTo2LNu_v1","Legacy17V1_WWTo2LNu_ext","Legacy17V1_WJets_v1","Legacy17V1_WJets_ext","Legacy17V1_DYJets_M10to50_v1","Legacy17V1_DYJets_M10to50_ext","Legacy17V1_DYJets_M50_v1","Legacy17V1_DYJets_M50_ext"],
"Fakes":['Legacy17V1_SEleBlockB', 'Legacy17V1_SEleBlockC', 'Legacy17V1_SEleBlockD', 'Legacy17V1_SEleBlockE', 'Legacy17V1_SEleBlockF', 'Legacy17V1_SMuBlockB', 'Legacy17V1_SMuBlockC', 'Legacy17V1_SMuBlockD', 'Legacy17V1_SMuBlockE', 'Legacy17V1_SMuBlockF', 'Legacy17V1_DblEGBlockB', 'Legacy17V1_DblEGBlockC', 'Legacy17V1_DblEGBlockD', 'Legacy17V1_DblEGBlockE', 'Legacy17V1_DblEGBlockF', 'Legacy17V1_DblMuBlockB', 'Legacy17V1_DblMuBlockC', 'Legacy17V1_DblMuBlockD', 'Legacy17V1_DblMuBlockE', 'Legacy17V1_DblMuBlockF', 'Legacy17V1_MuEGBlockB', 'Legacy17V1_MuEGBlockC', 'Legacy17V1_MuEGBlockD', 'Legacy17V1_MuEGBlockE', 'Legacy17V1_MuEGBlockF'],
"Flips":['Legacy17V1_SEleBlockB', 'Legacy17V1_SEleBlockC', 'Legacy17V1_SEleBlockD', 'Legacy17V1_SEleBlockE', 'Legacy17V1_SEleBlockF', 'Legacy17V1_SMuBlockB', 'Legacy17V1_SMuBlockC', 'Legacy17V1_SMuBlockD', 'Legacy17V1_SMuBlockE', 'Legacy17V1_SMuBlockF', 'Legacy17V1_DblEGBlockB', 'Legacy17V1_DblEGBlockC', 'Legacy17V1_DblEGBlockD', 'Legacy17V1_DblEGBlockE', 'Legacy17V1_DblEGBlockF', 'Legacy17V1_DblMuBlockB', 'Legacy17V1_DblMuBlockC', 'Legacy17V1_DblMuBlockD', 'Legacy17V1_DblMuBlockE', 'Legacy17V1_DblMuBlockF', 'Legacy17V1_MuEGBlockB', 'Legacy17V1_MuEGBlockC', 'Legacy17V1_MuEGBlockD', 'Legacy17V1_MuEGBlockE', 'Legacy17V1_MuEGBlockF'],
"Data":['Legacy17V1_SEleBlockB', 'Legacy17V1_SEleBlockC', 'Legacy17V1_SEleBlockD', 'Legacy17V1_SEleBlockE', 'Legacy17V1_SEleBlockF', 'Legacy17V1_SMuBlockB', 'Legacy17V1_SMuBlockC', 'Legacy17V1_SMuBlockD', 'Legacy17V1_SMuBlockE', 'Legacy17V1_SMuBlockF', 'Legacy17V1_DblEGBlockB', 'Legacy17V1_DblEGBlockC', 'Legacy17V1_DblEGBlockD', 'Legacy17V1_DblEGBlockE', 'Legacy17V1_DblEGBlockF', 'Legacy17V1_DblMuBlockB', 'Legacy17V1_DblMuBlockC', 'Legacy17V1_DblMuBlockD', 'Legacy17V1_DblMuBlockE', 'Legacy17V1_DblMuBlockF', 'Legacy17V1_MuEGBlockB', 'Legacy17V1_MuEGBlockC', 'Legacy17V1_MuEGBlockD', 'Legacy17V1_MuEGBlockE', 'Legacy17V1_MuEGBlockF'],
"EWK":["Legacy17V1_WWTo2LNu_v1","Legacy17V1_WWTo2LNu_ext","Legacy17V1_WJets_v1","Legacy17V1_WJets_ext","Legacy17V1_DYJets_M10to50_v1","Legacy17V1_DYJets_M10to50_ext","Legacy17V1_DYJets_M50_v1","Legacy17V1_DYJets_M50_ext"],
"ttH":["Legacy17V1_TTH_ctcvcp"],
},
"2018":{
"TTH":["Legacy18V1_ttHToNonbb"],
"THQ":["Legacy18V1_THQ_ctcvcp"], 
"THW":["Legacy18V1_THW_ctcvcp"], 
"VH":["Legacy18V1_VHToNonbb"], 
"ZH":["Legacy18V1_ZHTobb_v2","Legacy18V1_ZHTobb_ext","Legacy18V1_ZHToTauTau",], 
"ggH":["Legacy18V1_GGHToTauTau","Legacy18V1_ggHToZZTo4L","Legacy18V1_ggHToZZTo2L2Q","Legacy18V1_ggHToWWToLNuQQ","Legacy18V1_ggHToWWTo2L2Nu","Legacy18V1_ggHToMuMu_v2","Legacy18V1_ggHToMuMu_ext1","Legacy18V1_ggHToBB","Legacy18V1_ggHToGG"], 
"qqH":["Legacy18V1_VBFHToTauTau","Legacy18V1_VBFHToZZTo4L","Legacy18V1_VBFHToWWToLNuQQ","Legacy18V1_VBFHToWWTo2L2Nu","Legacy18V1_VBFHToMuMu","Legacy18V1_VBFHToBB","Legacy18V1_VBFHToGG"], 
"TTZ":["Legacy18V1_TTZ_M1to10","Legacy18V1_TTZ_M10","Legacy18V1_TTJets_TbarToSingleLep","Legacy18V1_TTJets_TToSingleLep","Legacy18V1_TTJets_DiLep"], 
"TT":["Legacy18V1_TTJets_TbarToSingleLep","Legacy18V1_TTJets_TToSingleLep","Legacy18V1_TTJets_DiLep"],
"TTW":["Legacy18V1_TTWJets"], 
"Convs":["Legacy18V1_TTGJets","Legacy18V1_TGJetsLep","Legacy18V1_WGToLNuG_Tune","Legacy18V1_ZGToLLG_01J","Legacy18V1_W1JetsToLNu","Legacy18V1_W2JetsToLNu","Legacy18V1_W3JetsToLNu","Legacy18V1_W4JetsToLNu","Legacy18V1_DYJets_M10to50","Legacy18V1_DYJets_M50_v1","Legacy18V1_DYJets_M50_ext","Legacy18V1_WZG"], 
"WZ":["Legacy18V1_WZTo3LNu"], 
"ZZ":["Legacy18V1_ZZTo4L_v1","Legacy18V1_ZZTo4L_ext"], 
"Rares":["Legacy18V1_tWll","Legacy18V1_WW_DS","Legacy18V1_WWW","Legacy18V1_WWZ","Legacy18V1_WZZ","Legacy18V1_ZZZ","Legacy18V1_TTTT","Legacy18V1_tZq","Legacy18V1_WpWpJJ"],
"TTWW":["Legacy18V1_TTWW_v1","Legacy18V1_TTWW_ext1"],
"ST":["Legacy18V1_ST_sCh_lepDecay","Legacy18V1_ST_tCh_top","Legacy18V1_ST_tCh_antitop","Legacy18V1_ST_tW_top","Legacy18V1_ST_tW_antitop"],
"EWK":["Legacy18V1_WWTo2LNu","Legacy18V1_DYJets_M10to50","Legacy18V1_DYJets_M50_v1","Legacy18V1_DYJets_M50_ext","Legacy18V1_WJets"],
"FakeSub":["Legacy18V1_ttHToNonbb","Legacy18V1_THQ_ctcvcp","Legacy18V1_THW_ctcvcp","Legacy18V1_VHToNonbb","Legacy18V1_ZHTobb_v2","Legacy18V1_ZHTobb_ext","Legacy18V1_ZHToTauTau","Legacy18V1_GGHToTauTau","Legacy18V1_ggHToZZTo4L","Legacy18V1_ggHToZZTo2L2Q","Legacy18V1_ggHToWWToLNuQQ","Legacy18V1_ggHToWWTo2L2Nu","Legacy18V1_ggHToMuMu_v2","Legacy18V1_ggHToMuMu_ext1","Legacy18V1_ggHToBB","Legacy18V1_ggHToGG","Legacy18V1_VBFHToTauTau","Legacy18V1_VBFHToZZTo4L","Legacy18V1_VBFHToWWToLNuQQ","Legacy18V1_VBFHToWWTo2L2Nu","Legacy18V1_VBFHToMuMu","Legacy18V1_VBFHToBB","Legacy18V1_VBFHToGG","Legacy18V1_TTZ_M1to10","Legacy18V1_TTZ_M10","Legacy18V1_TTJets_TbarToSingleLep","Legacy18V1_TTJets_TToSingleLep","Legacy18V1_TTJets_DiLep","Legacy18V1_TTWJets","Legacy18V1_WZTo3LNu","Legacy18V1_ZZTo4L_v1","Legacy18V1_ZZTo4L_ext","Legacy18V1_tWll","Legacy18V1_WW_DS","Legacy18V1_WWW","Legacy18V1_WWZ","Legacy18V1_WZZ","Legacy18V1_ZZZ","Legacy18V1_TTTT","Legacy18V1_tZq","Legacy18V1_WpWpJJ","Legacy18V1_TTWW_v1","Legacy18V1_TTWW_ext1","Legacy18V1_ST_sCh_lepDecay","Legacy18V1_ST_tCh_top","Legacy18V1_ST_tCh_antitop","Legacy18V1_ST_tW_top","Legacy18V1_ST_tW_antitop","Legacy18V1_WWTo2LNu","Legacy18V1_DYJets_M10to50","Legacy18V1_DYJets_M50_v1","Legacy18V1_DYJets_M50_ext","Legacy18V1_WJets"],
"mcFlips":["Legacy18V1_ttHToNonbb","Legacy18V1_THQ_ctcvcp","Legacy18V1_THW_ctcvcp","Legacy18V1_VHToNonbb","Legacy18V1_ZHTobb_v2","Legacy18V1_ZHTobb_ext","Legacy18V1_ZHToTauTau","Legacy18V1_GGHToTauTau","Legacy18V1_ggHToZZTo4L","Legacy18V1_ggHToZZTo2L2Q","Legacy18V1_ggHToWWToLNuQQ","Legacy18V1_ggHToWWTo2L2Nu","Legacy18V1_ggHToMuMu_v2","Legacy18V1_ggHToMuMu_ext1","Legacy18V1_ggHToBB","Legacy18V1_ggHToGG","Legacy18V1_VBFHToTauTau","Legacy18V1_VBFHToZZTo4L","Legacy18V1_VBFHToWWToLNuQQ","Legacy18V1_VBFHToWWTo2L2Nu","Legacy18V1_VBFHToMuMu","Legacy18V1_VBFHToBB","Legacy18V1_VBFHToGG","Legacy18V1_TTZ_M1to10","Legacy18V1_TTZ_M10","Legacy18V1_TTJets_TbarToSingleLep","Legacy18V1_TTJets_TToSingleLep","Legacy18V1_TTJets_DiLep","Legacy18V1_TTWJets","Legacy18V1_WZTo3LNu","Legacy18V1_ZZTo4L_v1","Legacy18V1_ZZTo4L_ext","Legacy18V1_tWll","Legacy18V1_WW_DS","Legacy18V1_WWW","Legacy18V1_WWZ","Legacy18V1_WZZ","Legacy18V1_ZZZ","Legacy18V1_TTTT","Legacy18V1_tZq","Legacy18V1_WpWpJJ","Legacy18V1_TTWW_v1","Legacy18V1_TTWW_ext1","Legacy18V1_ST_sCh_lepDecay","Legacy18V1_ST_tCh_top","Legacy18V1_ST_tCh_antitop","Legacy18V1_ST_tW_top","Legacy18V1_ST_tW_antitop","Legacy18V1_WWTo2LNu","Legacy18V1_DYJets_M10to50","Legacy18V1_DYJets_M50_v1","Legacy18V1_DYJets_M50_ext","Legacy18V1_WJets"],
"mcFakes":["Legacy18V1_ttHToNonbb","Legacy18V1_THQ_ctcvcp","Legacy18V1_THW_ctcvcp","Legacy18V1_VHToNonbb","Legacy18V1_ZHTobb_v2","Legacy18V1_ZHTobb_ext","Legacy18V1_ZHToTauTau","Legacy18V1_GGHToTauTau","Legacy18V1_ggHToZZTo4L","Legacy18V1_ggHToZZTo2L2Q","Legacy18V1_ggHToWWToLNuQQ","Legacy18V1_ggHToWWTo2L2Nu","Legacy18V1_ggHToMuMu_v2","Legacy18V1_ggHToMuMu_ext1","Legacy18V1_ggHToBB","Legacy18V1_ggHToGG","Legacy18V1_VBFHToTauTau","Legacy18V1_VBFHToZZTo4L","Legacy18V1_VBFHToWWToLNuQQ","Legacy18V1_VBFHToWWTo2L2Nu","Legacy18V1_VBFHToMuMu","Legacy18V1_VBFHToBB","Legacy18V1_VBFHToGG","Legacy18V1_TTZ_M1to10","Legacy18V1_TTZ_M10","Legacy18V1_TTJets_TbarToSingleLep","Legacy18V1_TTJets_TToSingleLep","Legacy18V1_TTJets_DiLep","Legacy18V1_TTWJets","Legacy18V1_WZTo3LNu","Legacy18V1_ZZTo4L_v1","Legacy18V1_ZZTo4L_ext","Legacy18V1_tWll","Legacy18V1_WW_DS","Legacy18V1_WWW","Legacy18V1_WWZ","Legacy18V1_WZZ","Legacy18V1_ZZZ","Legacy18V1_TTTT","Legacy18V1_tZq","Legacy18V1_WpWpJJ","Legacy18V1_TTWW_v1","Legacy18V1_TTWW_ext1","Legacy18V1_ST_sCh_lepDecay","Legacy18V1_ST_tCh_top","Legacy18V1_ST_tCh_antitop","Legacy18V1_ST_tW_top","Legacy18V1_ST_tW_antitop","Legacy18V1_WWTo2LNu","Legacy18V1_DYJets_M10to50","Legacy18V1_DYJets_M50_v1","Legacy18V1_DYJets_M50_ext","Legacy18V1_WJets"],
"Fakes":['Legacy18V1_SMuBlockA', 'Legacy18V1_SMuBlockB', 'Legacy18V1_SMuBlockC', 'Legacy18V1_SMuBlockD', 'Legacy18V1_EleGBlockA', 'Legacy18V1_EleGBlockB', 'Legacy18V1_EleGBlockC', 'Legacy18V1_EleGBlockD', 'Legacy18V1_DblMuBlockA', 'Legacy18V1_DblMuBlockB', 'Legacy18V1_DblMuBlockC', 'Legacy18V1_DblMuBlockD', 'Legacy18V1_MuEGBlockA', 'Legacy18V1_MuEGBlockB', 'Legacy18V1_MuEGBlockC', 'Legacy18V1_MuEGBlockD'],
"Flips":['Legacy18V1_SMuBlockA', 'Legacy18V1_SMuBlockB', 'Legacy18V1_SMuBlockC', 'Legacy18V1_SMuBlockD', 'Legacy18V1_EleGBlockA', 'Legacy18V1_EleGBlockB', 'Legacy18V1_EleGBlockC', 'Legacy18V1_EleGBlockD', 'Legacy18V1_DblMuBlockA', 'Legacy18V1_DblMuBlockB', 'Legacy18V1_DblMuBlockC', 'Legacy18V1_DblMuBlockD', 'Legacy18V1_MuEGBlockA', 'Legacy18V1_MuEGBlockB', 'Legacy18V1_MuEGBlockC', 'Legacy18V1_MuEGBlockD'],
"Data":['Legacy18V1_SMuBlockA', 'Legacy18V1_SMuBlockB', 'Legacy18V1_SMuBlockC', 'Legacy18V1_SMuBlockD', 'Legacy18V1_EleGBlockA', 'Legacy18V1_EleGBlockB', 'Legacy18V1_EleGBlockC', 'Legacy18V1_EleGBlockD', 'Legacy18V1_DblMuBlockA', 'Legacy18V1_DblMuBlockB', 'Legacy18V1_DblMuBlockC', 'Legacy18V1_DblMuBlockD', 'Legacy18V1_MuEGBlockA', 'Legacy18V1_MuEGBlockB', 'Legacy18V1_MuEGBlockC', 'Legacy18V1_MuEGBlockD'],
"ttH":["Legacy18V1_TTH_ctcvcp"],
}
}


if not os.path.exists("Rootplas/"):
    os.popen("mkdir -p Rootplas/")

InfoFileName = "InfoSkim.txt"
InfoFile      = file(InfoFileName,"w")

for Region in Regions:
    OutputRegionDir = BaseDir+"Rootplas/"+Region
    if not os.path.exists("Rootplas/" + Region):
        os.popen("mkdir -p Rootplas/"+Region)
    for dirOfRegion in DirOfRegions:
        if "DiLepRegion" in Region and "2L" not in dirOfRegion:
            #print ("skip DiLepRegion") 
            continue
        if ("TriLepRegion" in Region or "WZctrl" in Region or "ttZctrl" in Region) and "3L" not in dirOfRegion:
            #print ("skip TriLepRegion WZctrl ttZctrl") 
            continue
        if ("QuaLepRegion" in Region or "ZZctrl" in Region) and "4L" not in dirOfRegion:
            #print ("skip QuaLepRegion ZZctrl") 
            continue
        year=0
        if dirOfRegion.find("ttH2018")>=0:
            year=2018
        elif dirOfRegion.find("ttH2017")>=0:
            year=2017
        elif dirOfRegion.find("ttH2016")>=0:
            year=2016
        if os.path.exists(BaseDir+dirOfRegion):
            os.chdir(BaseDir+dirOfRegion)
        else:
            print >> InfoFile, "Dir " + BaseDir + dirOfRegion + " deosn't exist !!! Skip !!!"
            continue
        if not os.path.exists(OutputRegionDir+"/"+str(year)):
            os.popen("mkdir -p "+OutputRegionDir+"/"+str(year))
        dirsToCheck = [f for f in os.listdir(".") if os.path.isdir(f)]
        if "skims" in dirsToCheck : dirsToCheck.remove("skims")
        Processes = ProcessesAll
        OutputDir = ""
        jesFix =""
        if "JESUp"  in dirOfRegion:
            OutputDir = OutputRegionDir+"/"+str(year) +"/JESUp"+Region
            jesFix ="JESUp"
            Processes = ProcessesJES
        elif "JESDown"  in dirOfRegion:
            OutputDir = OutputRegionDir+"/"+str(year) +"/JESDown"+Region
            jesFix ="JESDown"
            Processes = ProcessesJES
        elif "Data"  in dirOfRegion:
            OutputDir = OutputRegionDir+"/"+str(year) +"/"+Region
            jesFix =""
            Processes = ProcessesData
        else:
            OutputDir = OutputRegionDir+"/"+str(year) +"/"+Region
            Processes = ProcessesJES
        for p in Processes:
            sampleType ="prompt"
            if p == "FakeSub": sampleType="fakesub"
            elif p == "Flips": sampleType="dataflips"
            elif p == "Convs": sampleType="conv"
            elif p == "Data": sampleType="dataobs"
            elif p == "Fakes": sampleType="datafakes"
            elif p == "mcFakes": sampleType="mcfakes"
            elif p == "mcFlips": sampleType="mcflips"
            if not os.path.exists(OutputDir):
                os.popen("mkdir -p "+OutputDir)
            outputfilename = OutputDir+"/"+p+"_"+Region+".root"
            inputfile = " "
            foundKey = False
            samples={}
            if year==2016:
                foundKey = (p in Samples["2016"])
                samples = Samples["2016"]
            elif year==2017:
                foundKey = (p in Samples["2017"])
                samples = Samples["2017"]
            elif year==2018:
                foundKey = (p in Samples["2018"])
                samples = Samples["2018"]
            if not foundKey:
                print >> InfoFile, " Region " + Region + " process " + p + " is missed in Samples "+ str(year)
                continue
            for i in samples[p]:
                if not os.path.exists(i+"/skims/merged"+i+"_"+sampleType+"_"+Region+".root"):
                    #print >>  InfoFile, " Region " + Region + " missed sample in process " + p  + " : "+i
                    print ("current dir %s miss file:"%(BaseDir+dirOfRegion), (i+"/skims/merged"+i+"_"+sampleType+"_"+Region+".root"))
                    continue
                elif os.path.getsize(i+"/skims/merged"+i+"_"+sampleType+"_"+Region+".root")<10000:
                    continue
                inputfile = inputfile + (" "+i+"/skims/merged"+i+"_"+sampleType+"_"+Region+".root")
            command_ls_merge = "hadd -f " + outputfilename + inputfile
            print(command_ls_merge)
            os.system(command_ls_merge)
        
            # higgs filters
            filterHiggs = 0
            if p in HiggsProcess:
                for higgsdecay, value in HiggsDecay.items():
                    filterHiggs = value
                    command_skim = "root -l -b -q "+frameworkDir+"copytree.C'("+'"'+OutputDir+'","'+OutputDir+'","'+p+"_"+Region+'","'+p+"_"+higgsdecay+"_"+Region+'",'+str(filterHiggs)+")'"
                    print(command_skim)
                    os.system(command_skim) 
              
    os.chdir(BaseDir)
