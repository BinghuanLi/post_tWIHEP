import sys, os, subprocess
import commands
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread

print ( "\n ------------------------ \n  please remember to separate VH into WH and ZH \n ----------------------------- \n")


frameworkDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/LegacyV2/"
BaseDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplas_LegacyAll_20191205/"

Regions=["DiLepRegion"]#"TriLepRegion","QuaLepRegion","ttZctrl","WZctrl","QuaLepRegion","ZZctrl"]
#Regions=["DiLepRegion","TriLepRegion","QuaLepRegion","ttZctrl","WZctrl","QuaLepRegion","ZZctrl"]

Selections=["datafakes", "dataflips", "prompt", "mcfakes", "mcflips", "fakesub", "dataobs", "conv"]

#DirOfRegions = ["ttH2018All2L","ttH2018All3L","ttH2018All4L"]

DirOfRegions = [
"ttH2016Data2L","ttH2016All2L","ttH2017Data2L","ttH2017All2L","ttH2018Data2L","ttH2018All2L",
#"ttH2016Data3L","ttH2016All3L","ttH2017Data3L","ttH2017All3L","ttH2018Data3L","ttH2018All3L",
#"ttH2016Data4L","ttH2016All4L","ttH2017Data4L","ttH2017All4L","ttH2018Data4L","ttH2018All4L"
]

HiggsDecay = {"hww":2,"hzz":6,"htt":3, "hmm":11, "hzg":7} # hot:999

HiggsProcess = ["qqH","ggH","WH","ZH","TTH","THQ","THW","ttH","HH","TTWH","TTZH"]
#ProcessesAll = ["THW"]
#ProcessesJES = ["THW"]
ProcessesAll = [ "TTH","THQ", "THW", "WH", "ZH", "TTWH", "TTZH", "ggH", "qqH", "TTZ", "TTW", "Convs", "WZ", "ZZ", "Rares","TTWW","FakeSub","Fakes","Flips","Data","ttH"]
ProcessesJES = [ "TTH","THQ", "THW", "WH", "ZH", "TTWH", "TTZH", "ggH", "qqH", "TTZ", "TTW", "Convs", "WZ", "ZZ", "Rares","TTWW","FakeSub","ttH"]
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
"EWK":["Legacy16V1_WZTo3LNu","Legacy16V1_ZZTo4L","Legacy16V1_WJets_v1","Legacy16V1_WJets_ext","Legacy16V1_DYJets_M50","Legacy16V1_DYJets_M10to50"],
"WZ":["Legacy16V1_WZTo3LNu","Legacy16V1_WJets_v1","Legacy16V1_WJets_ext"],
"ZZ":["Legacy16V1_ZZTo4L","Legacy16V1_DYJets_M50","Legacy16V1_DYJets_M10to50"],
"Convs":['Legacy16V1_TTGJets_v1', 'Legacy16V1_TTGJets_ext', 'Legacy16V1_TGJetsLep', 'Legacy16V1_WGToLNuG_ext1', 'Legacy16V1_WGToLNuG_ext2', 'Legacy16V1_WGToLNuG_ext3', 'Legacy16V1_ZGToLLG', 'Legacy16V1_DYJets_M10to50', 'Legacy16V1_DYJets_M50', 'Legacy16V1_WZG','Legacy16V1_WJets_v1','Legacy16V1_WJets_ext'],
"Rares":["Legacy16V1_tWll","Legacy16V1_WW_DS","Legacy16V1_WWW","Legacy16V1_WWZ","Legacy16V1_WZZ","Legacy16V1_ZZZ","Legacy16V1_TTTT","Legacy16V1_tZq_PS","Legacy16V1_WpWpJJ","Legacy16V1_WWTo2LNu","Legacy16V1_ST_sCh_lepDecay_PS","Legacy16V1_ST_tCh_top","Legacy16V1_ST_tCh_antitop_PS","Legacy16V1_ST_tW_top","Legacy16V1_ST_tW_antitop"],
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
"TTH":["Legacy17V2_ttHnobb"],
"THQ":["Legacy17V2_THQ_ctcvcp"], 
"THW":["Legacy17V2_THW_ctcvcp"], 
"WH":["Legacy17V2_VHToNonbb"], 
"ZH":["Legacy17V2_ZHTobb","Legacy17V2_ZHToTauTau",], 
"TTWH":["Legacy17V2_TTWH",],
"TTZH":["Legacy17V2_TTZH",],
"HH":["Legacy17V2_ggHHTo2B2VTo2L2Nu_nodeSM", "Legacy17V2_ggHHTo2B2VTo2L2Nu_node2", "Legacy17V2_ggHHTo2B2VTo2L2Nu_node3", "Legacy17V2_ggHHTo2B2VTo2L2Nu_node7",
"Legacy17V2_ggHHTo2B2VTo2L2Nu_node9", "Legacy17V2_ggHHTo2B2VTo2L2Nu_node12", "Legacy17V2_ggHHTo2B2Tau_nodeSM", "Legacy17V2_ggHHTo2B2Tau_node2", "Legacy17V2_ggHHTo2B2Tau_node3", "Legacy17V2_ggHHTo2B2Tau_node4", "Legacy17V2_ggHHTo2B2Tau_node7", "Legacy17V2_ggHHTo2B2Tau_node9", "Legacy17V2_ggHHTo2B2Tau_node12", "Legacy17V2_ggHHTo4Tau_nodeSM",
"Legacy17V2_ggHHTo4Tau_node2", "Legacy17V2_ggHHTo4Tau_node3", "Legacy17V2_ggHHTo4Tau_node7", "Legacy17V2_ggHHTo4Tau_node9", "Legacy17V2_ggHHTo4Tau_node12", "Legacy17V2_ggHHTo2V2Tau_nodeSM", "Legacy17V2_ggHHTo2V2Tau_node2", "Legacy17V2_ggHHTo2V2Tau_node3", "Legacy17V2_ggHHTo2V2Tau_node4", "Legacy17V2_ggHHTo2V2Tau_node5",
"Legacy17V2_ggHHTo2V2Tau_node6", "Legacy17V2_ggHHTo2V2Tau_node7", "Legacy17V2_ggHHTo2V2Tau_node8", "Legacy17V2_ggHHTo2V2Tau_node9", "Legacy17V2_ggHHTo2V2Tau_node10", "Legacy17V2_ggHHTo2V2Tau_node11", "Legacy17V2_ggHHTo2V2Tau_node12", "Legacy17V2_ggHHTo4V_nodeSM", "Legacy17V2_ggHHTo4V_node2", "Legacy17V2_ggHHTo4V_node3",
"Legacy17V2_ggHHTo4V_node4", "Legacy17V2_ggHHTo4V_node5", "Legacy17V2_ggHHTo4V_node6", "Legacy17V2_ggHHTo4V_node7", "Legacy17V2_ggHHTo4V_node8", "Legacy17V2_ggHHTo4V_node9", "Legacy17V2_ggHHTo4V_node10", "Legacy17V2_ggHHTo4V_node11", "Legacy17V2_ggHHTo4V_node12"],
"ggH":["Legacy17V2_GGHToTauTau_v1","Legacy17V2_GGHToTauTau_ext","Legacy17V2_ggHToZZTo4L_ext1","Legacy17V2_ggHToZZTo4L_ext3","Legacy17V2_ggHToZZTo4L_ext4","Legacy17V2_ggHToZZTo2L2Q","Legacy17V2_ggHToWWToLNuQQ","Legacy17V2_ggHToWWTo2L2Nu","Legacy17V2_ggHToMuMu_v1","Legacy17V2_ggHToMuMu_ext1","Legacy17V2_ggHToBB","Legacy17V2_ggHToGG"], 
"qqH":["Legacy17V2_VBFHToTauTau","Legacy17V2_VBFHToZZTo4L_ext2","Legacy17V2_VBFHToZZTo4L_ext1","Legacy17V2_VBFHToZZTo4L_v1","Legacy17V2_VBFHToWWToLNuQQ","Legacy17V2_VBFHToWWTo2L2Nu","Legacy17V2_VBFHToMuMu","Legacy17V2_VBFHToBB","Legacy17V2_VBFHToGG"], 
"TTZ":["Legacy17V2_TTZ_M1to10","Legacy17V2_TTZ_M10_PS","Legacy17V2_TTJets_DiLep","Legacy17V2_TTJets_TToSingleLep","Legacy17V2_TTJets_TbarToSingleLep"],
"TT":["Legacy17V2_TTJets_DiLep","Legacy17V2_TTJets_TToSingleLep","Legacy17V2_TTJets_TbarToSingleLep"], 
"TTW":["Legacy17V2_TTW_PS"], 
"Convs":["Legacy17V2_TTGJets_v1","Legacy17V2_TTGJets_ext","Legacy17V2_TGJetsLep","Legacy17V2_WGToLNuG_Tune","Legacy17V2_ZGToLLG_01J","Legacy17V2_W1JetsToLNu","Legacy17V2_W2JetsToLNu","Legacy17V2_W3JetsToLNu","Legacy17V2_W4JetsToLNu","Legacy17V2_DYJets_M10to50_v1","Legacy17V2_DYJets_M10to50_ext","Legacy17V2_DYJets_M50_v1","Legacy17V2_DYJets_M50_ext","Legacy17V2_WZG"], 
"WZ":["Legacy17V2_WZTo3LNu","Legacy17V2_W1JetsToLNu","Legacy17V2_W2JetsToLNu","Legacy17V2_W3JetsToLNu","Legacy17V2_W4JetsToLNu"], 
"ZZ":["Legacy17V2_ZZTo4L_v1","Legacy17V2_ZZTo4L_ext1","Legacy17V2_ZZTo4L_ext2","Legacy17V2_DYJets_M10to50_v1","Legacy17V2_DYJets_M10to50_ext","Legacy17V2_DYJets_M50_v1","Legacy17V2_DYJets_M50_ext"], 
"Rares":["Legacy17V2_tWll","Legacy17V2_WW_DS","Legacy17V2_WWW","Legacy17V2_WWZ","Legacy17V2_WZZ","Legacy17V2_ZZZ","Legacy17V2_TTTT","Legacy17V2_TTTT_PS","Legacy17V2_tZq","Legacy17V2_WpWpJJ","Legacy17V2_WWTo2LNu_v1","Legacy17V2_WWTo2LNu_ext","Legacy17V2_ST_sCh_lepDecay_PS","Legacy17V2_ST_tCh_top_PS","Legacy17V2_ST_tCh_antitop_PS","Legacy17V2_ST_tW_top_PS","Legacy17V2_ST_tW_antitop_PS"],
"TTWW":["Legacy17V2_TTWW"],
"ST":["Legacy17V2_ST_sCh_lepDecay_PS","Legacy17V2_ST_tCh_top_PS","Legacy17V2_ST_tCh_antitop_PS","Legacy17V2_ST_tW_top_PS","Legacy17V2_ST_tW_antitop_PS"],
"FakeSub":["Legacy17V2_ttHnobb","Legacy17V2_THQ_ctcvcp","Legacy17V2_THW_ctcvcp","Legacy17V2_VHToNonbb","Legacy17V2_ZHTobb","Legacy17V2_ZHToTauTau","Legacy17V2_GGHToTauTau_v1","Legacy17V2_GGHToTauTau_ext","Legacy17V2_ggHToZZTo4L_ext1","Legacy17V2_ggHToZZTo4L_ext3","Legacy17V2_ggHToZZTo4L_ext4","Legacy17V2_ggHToZZTo2L2Q","Legacy17V2_ggHToWWToLNuQQ","Legacy17V2_ggHToWWTo2L2Nu","Legacy17V2_ggHToMuMu_v1","Legacy17V2_ggHToMuMu_ext1","Legacy17V2_ggHToBB","Legacy17V2_ggHToGG","Legacy17V2_VBFHToTauTau","Legacy17V2_VBFHToZZTo4L_ext2","Legacy17V2_VBFHToZZTo4L_ext1","Legacy17V2_VBFHToZZTo4L_v1","Legacy17V2_VBFHToWWToLNuQQ","Legacy17V2_VBFHToWWTo2L2Nu","Legacy17V2_VBFHToMuMu","Legacy17V2_VBFHToBB","Legacy17V2_VBFHToGG","Legacy17V2_TTZ_M1to10","Legacy17V2_TTZ_M10_PS","Legacy17V2_TTJets_DiLep","Legacy17V2_TTJets_TToSingleLep","Legacy17V2_TTJets_TbarToSingleLep","Legacy17V2_TTW_PS","Legacy17V2_WZTo3LNu","Legacy17V2_ZZTo4L_v1","Legacy17V2_ZZTo4L_ext1","Legacy17V2_ZZTo4L_ext2","Legacy17V2_tWll","Legacy17V2_WW_DS","Legacy17V2_WWW","Legacy17V2_WWZ","Legacy17V2_WZZ","Legacy17V2_ZZZ","Legacy17V2_TTTT","Legacy17V2_TTTT_PS","Legacy17V2_tZq","Legacy17V2_WpWpJJ","Legacy17V2_TTWW","Legacy17V2_ST_sCh_lepDecay_PS","Legacy17V2_ST_tCh_top_PS","Legacy17V2_ST_tCh_antitop_PS","Legacy17V2_ST_tW_top_PS","Legacy17V2_ST_tW_antitop_PS","Legacy17V2_WWTo2LNu_v1","Legacy17V2_WWTo2LNu_ext","Legacy17V2_W1JetsToLNu","Legacy17V2_W2JetsToLNu","Legacy17V2_W3JetsToLNu","Legacy17V2_W4JetsToLNu","Legacy17V2_DYJets_M10to50_v1","Legacy17V2_DYJets_M10to50_ext","Legacy17V2_DYJets_M50_v1","Legacy17V2_DYJets_M50_ext","Legacy17V2_TTZH","Legacy17V2_TTWH",
"Legacy17V2_ggHHTo2B2VTo2L2Nu_nodeSM", "Legacy17V2_ggHHTo2B2VTo2L2Nu_node2", "Legacy17V2_ggHHTo2B2VTo2L2Nu_node3", "Legacy17V2_ggHHTo2B2VTo2L2Nu_node7", "Legacy17V2_ggHHTo2B2VTo2L2Nu_node9", "Legacy17V2_ggHHTo2B2VTo2L2Nu_node12", "Legacy17V2_ggHHTo2B2Tau_nodeSM", "Legacy17V2_ggHHTo2B2Tau_node2", "Legacy17V2_ggHHTo2B2Tau_node3", "Legacy17V2_ggHHTo2B2Tau_node4", "Legacy17V2_ggHHTo2B2Tau_node7", "Legacy17V2_ggHHTo2B2Tau_node9", "Legacy17V2_ggHHTo2B2Tau_node12", "Legacy17V2_ggHHTo4Tau_nodeSM", "Legacy17V2_ggHHTo4Tau_node2", "Legacy17V2_ggHHTo4Tau_node3", "Legacy17V2_ggHHTo4Tau_node7", "Legacy17V2_ggHHTo4Tau_node9", "Legacy17V2_ggHHTo4Tau_node12", "Legacy17V2_ggHHTo2V2Tau_nodeSM", "Legacy17V2_ggHHTo2V2Tau_node2", "Legacy17V2_ggHHTo2V2Tau_node3", "Legacy17V2_ggHHTo2V2Tau_node4", "Legacy17V2_ggHHTo2V2Tau_node5", "Legacy17V2_ggHHTo2V2Tau_node6", "Legacy17V2_ggHHTo2V2Tau_node7", "Legacy17V2_ggHHTo2V2Tau_node8", "Legacy17V2_ggHHTo2V2Tau_node9", "Legacy17V2_ggHHTo2V2Tau_node10", "Legacy17V2_ggHHTo2V2Tau_node11", "Legacy17V2_ggHHTo2V2Tau_node12", "Legacy17V2_ggHHTo4V_nodeSM", "Legacy17V2_ggHHTo4V_node2", "Legacy17V2_ggHHTo4V_node3", "Legacy17V2_ggHHTo4V_node4", "Legacy17V2_ggHHTo4V_node5", "Legacy17V2_ggHHTo4V_node6", "Legacy17V2_ggHHTo4V_node7", "Legacy17V2_ggHHTo4V_node8", "Legacy17V2_ggHHTo4V_node9", "Legacy17V2_ggHHTo4V_node10", "Legacy17V2_ggHHTo4V_node11", "Legacy17V2_ggHHTo4V_node12"],
"mcFakes":["Legacy17V2_ttHnobb","Legacy17V2_THQ_ctcvcp","Legacy17V2_THW_ctcvcp","Legacy17V2_VHToNonbb","Legacy17V2_ZHTobb","Legacy17V2_ZHToTauTau","Legacy17V2_GGHToTauTau_v1","Legacy17V2_GGHToTauTau_ext","Legacy17V2_ggHToZZTo4L_ext1","Legacy17V2_ggHToZZTo4L_ext3","Legacy17V2_ggHToZZTo4L_ext4","Legacy17V2_ggHToZZTo2L2Q","Legacy17V2_ggHToWWToLNuQQ","Legacy17V2_ggHToWWTo2L2Nu","Legacy17V2_ggHToMuMu_v1","Legacy17V2_ggHToMuMu_ext1","Legacy17V2_ggHToBB","Legacy17V2_ggHToGG","Legacy17V2_VBFHToTauTau","Legacy17V2_VBFHToZZTo4L_ext2","Legacy17V2_VBFHToZZTo4L_ext1","Legacy17V2_VBFHToZZTo4L_v1","Legacy17V2_VBFHToWWToLNuQQ","Legacy17V2_VBFHToWWTo2L2Nu","Legacy17V2_VBFHToMuMu","Legacy17V2_VBFHToBB","Legacy17V2_VBFHToGG","Legacy17V2_TTZ_M1to10","Legacy17V2_TTZ_M10_PS","Legacy17V2_TTJets_DiLep","Legacy17V2_TTJets_TToSingleLep","Legacy17V2_TTJets_TbarToSingleLep","Legacy17V2_TTW_PS","Legacy17V2_WZTo3LNu","Legacy17V2_ZZTo4L_v1","Legacy17V2_ZZTo4L_ext1","Legacy17V2_ZZTo4L_ext2","Legacy17V2_tWll","Legacy17V2_WW_DS","Legacy17V2_WWW","Legacy17V2_WWZ","Legacy17V2_WZZ","Legacy17V2_ZZZ","Legacy17V2_TTTT","Legacy17V2_TTTT_PS","Legacy17V2_tZq","Legacy17V2_WpWpJJ","Legacy17V2_TTWW","Legacy17V2_ST_sCh_lepDecay_PS","Legacy17V2_ST_tCh_top_PS","Legacy17V2_ST_tCh_antitop_PS","Legacy17V2_ST_tW_top_PS","Legacy17V2_ST_tW_antitop_PS","Legacy17V2_WWTo2LNu_v1","Legacy17V2_WWTo2LNu_ext","Legacy17V2_W1JetsToLNu","Legacy17V2_W2JetsToLNu","Legacy17V2_W3JetsToLNu","Legacy17V2_W4JetsToLNu","Legacy17V2_DYJets_M10to50_v1","Legacy17V2_DYJets_M10to50_ext","Legacy17V2_DYJets_M50_v1","Legacy17V2_DYJets_M50_ext","Legacy17V2_TTZH","Legacy17V2_TTWH",
"Legacy17V2_ggHHTo2B2VTo2L2Nu_nodeSM", "Legacy17V2_ggHHTo2B2VTo2L2Nu_node2", "Legacy17V2_ggHHTo2B2VTo2L2Nu_node3", "Legacy17V2_ggHHTo2B2VTo2L2Nu_node7", "Legacy17V2_ggHHTo2B2VTo2L2Nu_node9", "Legacy17V2_ggHHTo2B2VTo2L2Nu_node12", "Legacy17V2_ggHHTo2B2Tau_nodeSM", "Legacy17V2_ggHHTo2B2Tau_node2", "Legacy17V2_ggHHTo2B2Tau_node3", "Legacy17V2_ggHHTo2B2Tau_node4", "Legacy17V2_ggHHTo2B2Tau_node7", "Legacy17V2_ggHHTo2B2Tau_node9", "Legacy17V2_ggHHTo2B2Tau_node12", "Legacy17V2_ggHHTo4Tau_nodeSM", "Legacy17V2_ggHHTo4Tau_node2", "Legacy17V2_ggHHTo4Tau_node3", "Legacy17V2_ggHHTo4Tau_node7", "Legacy17V2_ggHHTo4Tau_node9", "Legacy17V2_ggHHTo4Tau_node12", "Legacy17V2_ggHHTo2V2Tau_nodeSM", "Legacy17V2_ggHHTo2V2Tau_node2", "Legacy17V2_ggHHTo2V2Tau_node3", "Legacy17V2_ggHHTo2V2Tau_node4", "Legacy17V2_ggHHTo2V2Tau_node5", "Legacy17V2_ggHHTo2V2Tau_node6", "Legacy17V2_ggHHTo2V2Tau_node7", "Legacy17V2_ggHHTo2V2Tau_node8", "Legacy17V2_ggHHTo2V2Tau_node9", "Legacy17V2_ggHHTo2V2Tau_node10", "Legacy17V2_ggHHTo2V2Tau_node11", "Legacy17V2_ggHHTo2V2Tau_node12", "Legacy17V2_ggHHTo4V_nodeSM", "Legacy17V2_ggHHTo4V_node2", "Legacy17V2_ggHHTo4V_node3", "Legacy17V2_ggHHTo4V_node4", "Legacy17V2_ggHHTo4V_node5", "Legacy17V2_ggHHTo4V_node6", "Legacy17V2_ggHHTo4V_node7", "Legacy17V2_ggHHTo4V_node8", "Legacy17V2_ggHHTo4V_node9", "Legacy17V2_ggHHTo4V_node10", "Legacy17V2_ggHHTo4V_node11", "Legacy17V2_ggHHTo4V_node12"],
"mcFlips":["Legacy17V2_ttHnobb","Legacy17V2_THQ_ctcvcp","Legacy17V2_THW_ctcvcp","Legacy17V2_VHToNonbb","Legacy17V2_ZHTobb","Legacy17V2_ZHToTauTau","Legacy17V2_GGHToTauTau_v1","Legacy17V2_GGHToTauTau_ext","Legacy17V2_ggHToZZTo4L_ext1","Legacy17V2_ggHToZZTo4L_ext3","Legacy17V2_ggHToZZTo4L_ext4","Legacy17V2_ggHToZZTo2L2Q","Legacy17V2_ggHToWWToLNuQQ","Legacy17V2_ggHToWWTo2L2Nu","Legacy17V2_ggHToMuMu_v1","Legacy17V2_ggHToMuMu_ext1","Legacy17V2_ggHToBB","Legacy17V2_ggHToGG","Legacy17V2_VBFHToTauTau","Legacy17V2_VBFHToZZTo4L_ext2","Legacy17V2_VBFHToZZTo4L_ext1","Legacy17V2_VBFHToZZTo4L_v1","Legacy17V2_VBFHToWWToLNuQQ","Legacy17V2_VBFHToWWTo2L2Nu","Legacy17V2_VBFHToMuMu","Legacy17V2_VBFHToBB","Legacy17V2_VBFHToGG","Legacy17V2_TTZ_M1to10","Legacy17V2_TTZ_M10_PS","Legacy17V2_TTJets_DiLep","Legacy17V2_TTJets_TToSingleLep","Legacy17V2_TTJets_TbarToSingleLep","Legacy17V2_TTW_PS","Legacy17V2_WZTo3LNu","Legacy17V2_ZZTo4L_v1","Legacy17V2_ZZTo4L_ext1","Legacy17V2_ZZTo4L_ext2","Legacy17V2_tWll","Legacy17V2_WW_DS","Legacy17V2_WWW","Legacy17V2_WWZ","Legacy17V2_WZZ","Legacy17V2_ZZZ","Legacy17V2_TTTT","Legacy17V2_TTTT_PS","Legacy17V2_tZq","Legacy17V2_WpWpJJ","Legacy17V2_TTWW","Legacy17V2_ST_sCh_lepDecay_PS","Legacy17V2_ST_tCh_top_PS","Legacy17V2_ST_tCh_antitop_PS","Legacy17V2_ST_tW_top_PS","Legacy17V2_ST_tW_antitop_PS","Legacy17V2_WWTo2LNu_v1","Legacy17V2_WWTo2LNu_ext","Legacy17V2_W1JetsToLNu","Legacy17V2_W2JetsToLNu","Legacy17V2_W3JetsToLNu","Legacy17V2_W4JetsToLNu","Legacy17V2_DYJets_M10to50_v1","Legacy17V2_DYJets_M10to50_ext","Legacy17V2_DYJets_M50_v1","Legacy17V2_DYJets_M50_ext","Legacy17V2_TTZH","Legacy17V2_TTWH",
"Legacy17V2_ggHHTo2B2VTo2L2Nu_nodeSM", "Legacy17V2_ggHHTo2B2VTo2L2Nu_node2", "Legacy17V2_ggHHTo2B2VTo2L2Nu_node3", "Legacy17V2_ggHHTo2B2VTo2L2Nu_node7", "Legacy17V2_ggHHTo2B2VTo2L2Nu_node9", "Legacy17V2_ggHHTo2B2VTo2L2Nu_node12", "Legacy17V2_ggHHTo2B2Tau_nodeSM", "Legacy17V2_ggHHTo2B2Tau_node2", "Legacy17V2_ggHHTo2B2Tau_node3", "Legacy17V2_ggHHTo2B2Tau_node4", "Legacy17V2_ggHHTo2B2Tau_node7", "Legacy17V2_ggHHTo2B2Tau_node9", "Legacy17V2_ggHHTo2B2Tau_node12", "Legacy17V2_ggHHTo4Tau_nodeSM", "Legacy17V2_ggHHTo4Tau_node2", "Legacy17V2_ggHHTo4Tau_node3", "Legacy17V2_ggHHTo4Tau_node7", "Legacy17V2_ggHHTo4Tau_node9", "Legacy17V2_ggHHTo4Tau_node12", "Legacy17V2_ggHHTo2V2Tau_nodeSM", "Legacy17V2_ggHHTo2V2Tau_node2", "Legacy17V2_ggHHTo2V2Tau_node3", "Legacy17V2_ggHHTo2V2Tau_node4", "Legacy17V2_ggHHTo2V2Tau_node5", "Legacy17V2_ggHHTo2V2Tau_node6", "Legacy17V2_ggHHTo2V2Tau_node7", "Legacy17V2_ggHHTo2V2Tau_node8", "Legacy17V2_ggHHTo2V2Tau_node9", "Legacy17V2_ggHHTo2V2Tau_node10", "Legacy17V2_ggHHTo2V2Tau_node11", "Legacy17V2_ggHHTo2V2Tau_node12", "Legacy17V2_ggHHTo4V_nodeSM", "Legacy17V2_ggHHTo4V_node2", "Legacy17V2_ggHHTo4V_node3", "Legacy17V2_ggHHTo4V_node4", "Legacy17V2_ggHHTo4V_node5", "Legacy17V2_ggHHTo4V_node6", "Legacy17V2_ggHHTo4V_node7", "Legacy17V2_ggHHTo4V_node8", "Legacy17V2_ggHHTo4V_node9", "Legacy17V2_ggHHTo4V_node10", "Legacy17V2_ggHHTo4V_node11", "Legacy17V2_ggHHTo4V_node12"],
"Fakes":['Legacy17V2_SEleBlockB', 'Legacy17V2_SEleBlockC', 'Legacy17V2_SEleBlockD', 'Legacy17V2_SEleBlockE', 'Legacy17V2_SEleBlockF', 'Legacy17V2_SMuBlockB', 'Legacy17V2_SMuBlockC', 'Legacy17V2_SMuBlockD', 'Legacy17V2_SMuBlockE', 'Legacy17V2_SMuBlockF', 'Legacy17V2_DblEGBlockB', 'Legacy17V2_DblEGBlockC', 'Legacy17V2_DblEGBlockD', 'Legacy17V2_DblEGBlockE', 'Legacy17V2_DblEGBlockF', 'Legacy17V2_DblMuBlockB', 'Legacy17V2_DblMuBlockC', 'Legacy17V2_DblMuBlockD', 'Legacy17V2_DblMuBlockE', 'Legacy17V2_DblMuBlockF', 'Legacy17V2_MuEGBlockB', 'Legacy17V2_MuEGBlockC', 'Legacy17V2_MuEGBlockD', 'Legacy17V2_MuEGBlockE', 'Legacy17V2_MuEGBlockF'],
"Flips":['Legacy17V2_SEleBlockB', 'Legacy17V2_SEleBlockC', 'Legacy17V2_SEleBlockD', 'Legacy17V2_SEleBlockE', 'Legacy17V2_SEleBlockF', 'Legacy17V2_SMuBlockB', 'Legacy17V2_SMuBlockC', 'Legacy17V2_SMuBlockD', 'Legacy17V2_SMuBlockE', 'Legacy17V2_SMuBlockF', 'Legacy17V2_DblEGBlockB', 'Legacy17V2_DblEGBlockC', 'Legacy17V2_DblEGBlockD', 'Legacy17V2_DblEGBlockE', 'Legacy17V2_DblEGBlockF', 'Legacy17V2_DblMuBlockB', 'Legacy17V2_DblMuBlockC', 'Legacy17V2_DblMuBlockD', 'Legacy17V2_DblMuBlockE', 'Legacy17V2_DblMuBlockF', 'Legacy17V2_MuEGBlockB', 'Legacy17V2_MuEGBlockC', 'Legacy17V2_MuEGBlockD', 'Legacy17V2_MuEGBlockE', 'Legacy17V2_MuEGBlockF'],
"Data":['Legacy17V2_SEleBlockB', 'Legacy17V2_SEleBlockC', 'Legacy17V2_SEleBlockD', 'Legacy17V2_SEleBlockE', 'Legacy17V2_SEleBlockF', 'Legacy17V2_SMuBlockB', 'Legacy17V2_SMuBlockC', 'Legacy17V2_SMuBlockD', 'Legacy17V2_SMuBlockE', 'Legacy17V2_SMuBlockF', 'Legacy17V2_DblEGBlockB', 'Legacy17V2_DblEGBlockC', 'Legacy17V2_DblEGBlockD', 'Legacy17V2_DblEGBlockE', 'Legacy17V2_DblEGBlockF', 'Legacy17V2_DblMuBlockB', 'Legacy17V2_DblMuBlockC', 'Legacy17V2_DblMuBlockD', 'Legacy17V2_DblMuBlockE', 'Legacy17V2_DblMuBlockF', 'Legacy17V2_MuEGBlockB', 'Legacy17V2_MuEGBlockC', 'Legacy17V2_MuEGBlockD', 'Legacy17V2_MuEGBlockE', 'Legacy17V2_MuEGBlockF'],
"EWK":["Legacy17V2_ZZTo4L_v1","Legacy17V2_ZZTo4L_ext1","Legacy17V2_ZZTo4L_ext2","Legacy17V2_WZTo3LNu","Legacy17V2_DYJets_M10to50_v1","Legacy17V2_DYJets_M10to50_ext","Legacy17V2_DYJets_M50_v1","Legacy17V2_DYJets_M50_ext","Legacy17V2_W1JetsToLNu","Legacy17V2_W2JetsToLNu","Legacy17V2_W3JetsToLNu","Legacy17V2_W4JetsToLNu"],
"ttH":["Legacy17V2_TTH_ctcvcp"],
},
"2018":{
"TTH":["Legacy18V2_ttHToNonbb"],
"THQ":["Legacy18V2_THQ_ctcvcp"], 
"THW":["Legacy18V2_THW_ctcvcp"], 
"WH":["Legacy18V2_VHToNonbb"], 
"ZH":["Legacy18V2_ZHTobb_v2","Legacy18V2_ZHTobb_ext","Legacy18V2_ZHToTauTau",], 
"TTWH":["Legacy18V2_TTWH",],
"TTZH":["Legacy18V2_TTZH",],
"ggH":["Legacy18V2_GGHToTauTau","Legacy18V2_ggHToZZTo4L","Legacy18V2_ggHToZZTo2L2Q","Legacy18V2_ggHToWWToLNuQQ","Legacy18V2_ggHToWWTo2L2Nu","Legacy18V2_ggHToMuMu_v2","Legacy18V2_ggHToMuMu_ext1","Legacy18V2_ggHToBB","Legacy18V2_ggHToGG"], 
"qqH":["Legacy18V2_VBFHToTauTau","Legacy18V2_VBFHToZZTo4L","Legacy18V2_VBFHToWWToLNuQQ","Legacy18V2_VBFHToWWTo2L2Nu","Legacy18V2_VBFHToMuMu","Legacy18V2_VBFHToBB","Legacy18V2_VBFHToGG"],
"HH":["Legacy18V2_ggHTo2B2Tau_nodeSM", "Legacy18V2_ggHTo2B2Tau_node2", "Legacy18V2_ggHTo2B2Tau_node3","Legacy18V2_ggHTo2B2Tau_node4", "Legacy18V2_ggHTo2B2Tau_node5", "Legacy18V2_ggHTo2B2Tau_node6", "Legacy18V2_ggHTo2B2Tau_node7", "Legacy18V2_ggHTo2B2Tau_node8", "Legacy18V2_ggHTo2B2Tau_node9", "Legacy18V2_ggHTo2B2Tau_node10", "Legacy18V2_ggHTo2B2Tau_node11", "Legacy18V2_ggHTo2B2Tau_node12",] 
"TTZ":["Legacy18V2_TTZ_M1to10","Legacy18V2_TTZ_M10","Legacy18V2_TTJets_TbarToSingleLep","Legacy18V2_TTJets_TToSingleLep","Legacy18V2_TTJets_DiLep"], 
"TT":["Legacy18V2_TTJets_TbarToSingleLep","Legacy18V2_TTJets_TToSingleLep","Legacy18V2_TTJets_DiLep"],
"TTW":["Legacy18V2_TTWJets"], 
"Convs":["Legacy18V2_TTGJets","Legacy18V2_TGJetsLep","Legacy18V2_WGToLNuG_Tune","Legacy18V2_ZGToLLG_01J","Legacy18V2_W1JetsToLNu","Legacy18V2_W2JetsToLNu","Legacy18V2_W3JetsToLNu","Legacy18V2_W4JetsToLNu","Legacy18V2_DYJets_M10to50","Legacy18V2_DYJets_M50_v1","Legacy18V2_DYJets_M50_ext","Legacy18V2_WZG"], 
"WZ":["Legacy18V2_WZTo3LNu","Legacy18V2_W1JetsToLNu","Legacy18V2_W2JetsToLNu","Legacy18V2_W3JetsToLNu","Legacy18V2_W4JetsToLNu"], 
"ZZ":["Legacy18V2_ZZTo4L_v1","Legacy18V2_ZZTo4L_ext","Legacy18V2_DYJets_M10to50","Legacy18V2_DYJets_M50_v1","Legacy18V2_DYJets_M50_ext"], 
"Rares":["Legacy18V2_tWll","Legacy18V2_WW_DS","Legacy18V2_WWW","Legacy18V2_WWZ","Legacy18V2_WZZ","Legacy18V2_ZZZ","Legacy18V2_TTTT","Legacy18V2_tZq","Legacy18V2_WpWpJJ","Legacy18V2_WWTo2LNu","Legacy18V2_ST_sCh_lepDecay","Legacy18V2_ST_tCh_top","Legacy18V2_ST_tCh_antitop","Legacy18V2_ST_tW_top","Legacy18V2_ST_tW_antitop"],
"TTWW":["Legacy18V2_TTWW_v1","Legacy18V2_TTWW_ext1"],
"ST":["Legacy18V2_ST_sCh_lepDecay","Legacy18V2_ST_tCh_top","Legacy18V2_ST_tCh_antitop","Legacy18V2_ST_tW_top","Legacy18V2_ST_tW_antitop"],
"EWK":["Legacy18V2_DYJets_M10to50","Legacy18V2_DYJets_M50_v1","Legacy18V2_DYJets_M50_ext","Legacy18V2_WZTo3LNu","Legacy18V2_ZZTo4L_v1","Legacy18V2_ZZTo4L_ext","Legacy18V2_W1JetsToLNu","Legacy18V2_W2JetsToLNu","Legacy18V2_W3JetsToLNu","Legacy18V2_W4JetsToLNu"],
"FakeSub":["Legacy18V2_ttHToNonbb","Legacy18V2_THQ_ctcvcp","Legacy18V2_THW_ctcvcp","Legacy18V2_VHToNonbb","Legacy18V2_ZHTobb_v2","Legacy18V2_ZHTobb_ext","Legacy18V2_ZHToTauTau","Legacy18V2_GGHToTauTau","Legacy18V2_ggHToZZTo4L","Legacy18V2_ggHToZZTo2L2Q","Legacy18V2_ggHToWWToLNuQQ","Legacy18V2_ggHToWWTo2L2Nu","Legacy18V2_ggHToMuMu_v2","Legacy18V2_ggHToMuMu_ext1","Legacy18V2_ggHToBB","Legacy18V2_ggHToGG","Legacy18V2_VBFHToTauTau","Legacy18V2_VBFHToZZTo4L","Legacy18V2_VBFHToWWToLNuQQ","Legacy18V2_VBFHToWWTo2L2Nu","Legacy18V2_VBFHToMuMu","Legacy18V2_VBFHToBB","Legacy18V2_VBFHToGG","Legacy18V2_TTZ_M1to10","Legacy18V2_TTZ_M10","Legacy18V2_TTJets_TbarToSingleLep","Legacy18V2_TTJets_TToSingleLep","Legacy18V2_TTJets_DiLep","Legacy18V2_TTWJets","Legacy18V2_WZTo3LNu","Legacy18V2_ZZTo4L_v1","Legacy18V2_ZZTo4L_ext","Legacy18V2_tWll","Legacy18V2_WW_DS","Legacy18V2_WWW","Legacy18V2_WWZ","Legacy18V2_WZZ","Legacy18V2_ZZZ","Legacy18V2_TTTT","Legacy18V2_tZq","Legacy18V2_WpWpJJ","Legacy18V2_TTWW_v1","Legacy18V2_TTWW_ext1","Legacy18V2_ST_sCh_lepDecay","Legacy18V2_ST_tCh_top","Legacy18V2_ST_tCh_antitop","Legacy18V2_ST_tW_top","Legacy18V2_ST_tW_antitop","Legacy18V2_WWTo2LNu","Legacy18V2_DYJets_M10to50","Legacy18V2_DYJets_M50_v1","Legacy18V2_DYJets_M50_ext","Legacy18V2_TTWH","Legacy18V2_TTZH", "Legacy18V2_W1JetsToLNu","Legacy18V2_W2JetsToLNu","Legacy18V2_W3JetsToLNu","Legacy18V2_W4JetsToLNu","Legacy18V2_ggHTo2B2Tau_nodeSM", "Legacy18V2_ggHTo2B2Tau_node2", "Legacy18V2_ggHTo2B2Tau_node3","Legacy18V2_ggHTo2B2Tau_node4", "Legacy18V2_ggHTo2B2Tau_node5", "Legacy18V2_ggHTo2B2Tau_node6", "Legacy18V2_ggHTo2B2Tau_node7", "Legacy18V2_ggHTo2B2Tau_node8", "Legacy18V2_ggHTo2B2Tau_node9", "Legacy18V2_ggHTo2B2Tau_node10", "Legacy18V2_ggHTo2B2Tau_node11", "Legacy18V2_ggHTo2B2Tau_node12"],
"mcFakes":["Legacy18V2_ttHToNonbb","Legacy18V2_THQ_ctcvcp","Legacy18V2_THW_ctcvcp","Legacy18V2_VHToNonbb","Legacy18V2_ZHTobb_v2","Legacy18V2_ZHTobb_ext","Legacy18V2_ZHToTauTau","Legacy18V2_GGHToTauTau","Legacy18V2_ggHToZZTo4L","Legacy18V2_ggHToZZTo2L2Q","Legacy18V2_ggHToWWToLNuQQ","Legacy18V2_ggHToWWTo2L2Nu","Legacy18V2_ggHToMuMu_v2","Legacy18V2_ggHToMuMu_ext1","Legacy18V2_ggHToBB","Legacy18V2_ggHToGG","Legacy18V2_VBFHToTauTau","Legacy18V2_VBFHToZZTo4L","Legacy18V2_VBFHToWWToLNuQQ","Legacy18V2_VBFHToWWTo2L2Nu","Legacy18V2_VBFHToMuMu","Legacy18V2_VBFHToBB","Legacy18V2_VBFHToGG","Legacy18V2_TTZ_M1to10","Legacy18V2_TTZ_M10","Legacy18V2_TTJets_TbarToSingleLep","Legacy18V2_TTJets_TToSingleLep","Legacy18V2_TTJets_DiLep","Legacy18V2_TTWJets","Legacy18V2_WZTo3LNu","Legacy18V2_ZZTo4L_v1","Legacy18V2_ZZTo4L_ext","Legacy18V2_tWll","Legacy18V2_WW_DS","Legacy18V2_WWW","Legacy18V2_WWZ","Legacy18V2_WZZ","Legacy18V2_ZZZ","Legacy18V2_TTTT","Legacy18V2_tZq","Legacy18V2_WpWpJJ","Legacy18V2_TTWW_v1","Legacy18V2_TTWW_ext1","Legacy18V2_ST_sCh_lepDecay","Legacy18V2_ST_tCh_top","Legacy18V2_ST_tCh_antitop","Legacy18V2_ST_tW_top","Legacy18V2_ST_tW_antitop","Legacy18V2_WWTo2LNu","Legacy18V2_DYJets_M10to50","Legacy18V2_DYJets_M50_v1","Legacy18V2_DYJets_M50_ext","Legacy18V2_TTWH","Legacy18V2_TTZH", "Legacy18V2_W1JetsToLNu","Legacy18V2_W2JetsToLNu","Legacy18V2_W3JetsToLNu","Legacy18V2_W4JetsToLNu","Legacy18V2_ggHTo2B2Tau_nodeSM", "Legacy18V2_ggHTo2B2Tau_node2", "Legacy18V2_ggHTo2B2Tau_node3","Legacy18V2_ggHTo2B2Tau_node4", "Legacy18V2_ggHTo2B2Tau_node5", "Legacy18V2_ggHTo2B2Tau_node6", "Legacy18V2_ggHTo2B2Tau_node7", "Legacy18V2_ggHTo2B2Tau_node8", "Legacy18V2_ggHTo2B2Tau_node9", "Legacy18V2_ggHTo2B2Tau_node10", "Legacy18V2_ggHTo2B2Tau_node11", "Legacy18V2_ggHTo2B2Tau_node12"],
"mcFlips":["Legacy18V2_ttHToNonbb","Legacy18V2_THQ_ctcvcp","Legacy18V2_THW_ctcvcp","Legacy18V2_VHToNonbb","Legacy18V2_ZHTobb_v2","Legacy18V2_ZHTobb_ext","Legacy18V2_ZHToTauTau","Legacy18V2_GGHToTauTau","Legacy18V2_ggHToZZTo4L","Legacy18V2_ggHToZZTo2L2Q","Legacy18V2_ggHToWWToLNuQQ","Legacy18V2_ggHToWWTo2L2Nu","Legacy18V2_ggHToMuMu_v2","Legacy18V2_ggHToMuMu_ext1","Legacy18V2_ggHToBB","Legacy18V2_ggHToGG","Legacy18V2_VBFHToTauTau","Legacy18V2_VBFHToZZTo4L","Legacy18V2_VBFHToWWToLNuQQ","Legacy18V2_VBFHToWWTo2L2Nu","Legacy18V2_VBFHToMuMu","Legacy18V2_VBFHToBB","Legacy18V2_VBFHToGG","Legacy18V2_TTZ_M1to10","Legacy18V2_TTZ_M10","Legacy18V2_TTJets_TbarToSingleLep","Legacy18V2_TTJets_TToSingleLep","Legacy18V2_TTJets_DiLep","Legacy18V2_TTWJets","Legacy18V2_WZTo3LNu","Legacy18V2_ZZTo4L_v1","Legacy18V2_ZZTo4L_ext","Legacy18V2_tWll","Legacy18V2_WW_DS","Legacy18V2_WWW","Legacy18V2_WWZ","Legacy18V2_WZZ","Legacy18V2_ZZZ","Legacy18V2_TTTT","Legacy18V2_tZq","Legacy18V2_WpWpJJ","Legacy18V2_TTWW_v1","Legacy18V2_TTWW_ext1","Legacy18V2_ST_sCh_lepDecay","Legacy18V2_ST_tCh_top","Legacy18V2_ST_tCh_antitop","Legacy18V2_ST_tW_top","Legacy18V2_ST_tW_antitop","Legacy18V2_WWTo2LNu","Legacy18V2_DYJets_M10to50","Legacy18V2_DYJets_M50_v1","Legacy18V2_DYJets_M50_ext","Legacy18V2_TTWH","Legacy18V2_TTZH", "Legacy18V2_W1JetsToLNu","Legacy18V2_W2JetsToLNu","Legacy18V2_W3JetsToLNu","Legacy18V2_W4JetsToLNu","Legacy18V2_ggHTo2B2Tau_nodeSM", "Legacy18V2_ggHTo2B2Tau_node2", "Legacy18V2_ggHTo2B2Tau_node3","Legacy18V2_ggHTo2B2Tau_node4", "Legacy18V2_ggHTo2B2Tau_node5", "Legacy18V2_ggHTo2B2Tau_node6", "Legacy18V2_ggHTo2B2Tau_node7", "Legacy18V2_ggHTo2B2Tau_node8", "Legacy18V2_ggHTo2B2Tau_node9", "Legacy18V2_ggHTo2B2Tau_node10", "Legacy18V2_ggHTo2B2Tau_node11", "Legacy18V2_ggHTo2B2Tau_node12"],
"Fakes":['Legacy18V2_SMuBlockA', 'Legacy18V2_SMuBlockB', 'Legacy18V2_SMuBlockC', 'Legacy18V2_SMuBlockD', 'Legacy18V2_EleGBlockA', 'Legacy18V2_EleGBlockB', 'Legacy18V2_EleGBlockC', 'Legacy18V2_EleGBlockD', 'Legacy18V2_DblMuBlockA', 'Legacy18V2_DblMuBlockB', 'Legacy18V2_DblMuBlockC', 'Legacy18V2_DblMuBlockD', 'Legacy18V2_MuEGBlockA', 'Legacy18V2_MuEGBlockB', 'Legacy18V2_MuEGBlockC', 'Legacy18V2_MuEGBlockD'],
"Flips":['Legacy18V2_SMuBlockA', 'Legacy18V2_SMuBlockB', 'Legacy18V2_SMuBlockC', 'Legacy18V2_SMuBlockD', 'Legacy18V2_EleGBlockA', 'Legacy18V2_EleGBlockB', 'Legacy18V2_EleGBlockC', 'Legacy18V2_EleGBlockD', 'Legacy18V2_DblMuBlockA', 'Legacy18V2_DblMuBlockB', 'Legacy18V2_DblMuBlockC', 'Legacy18V2_DblMuBlockD', 'Legacy18V2_MuEGBlockA', 'Legacy18V2_MuEGBlockB', 'Legacy18V2_MuEGBlockC', 'Legacy18V2_MuEGBlockD'],
"Data":['Legacy18V2_SMuBlockA', 'Legacy18V2_SMuBlockB', 'Legacy18V2_SMuBlockC', 'Legacy18V2_SMuBlockD', 'Legacy18V2_EleGBlockA', 'Legacy18V2_EleGBlockB', 'Legacy18V2_EleGBlockC', 'Legacy18V2_EleGBlockD', 'Legacy18V2_DblMuBlockA', 'Legacy18V2_DblMuBlockB', 'Legacy18V2_DblMuBlockC', 'Legacy18V2_DblMuBlockD', 'Legacy18V2_MuEGBlockA', 'Legacy18V2_MuEGBlockB', 'Legacy18V2_MuEGBlockC', 'Legacy18V2_MuEGBlockD'],
"ttH":["Legacy18V2_TTH_ctcvcp"],
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
