import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread


#Categories=["SubCat2l","DNNCat","DNNCat_option2","DNNCat_option3","DNNSubCat1_option1","DNNSubCat1_option2","DNNSubCat1_option3","DNNSubCat2_option1","DNNSubCat2_option2","DNNSubCat2_option3"]
Categories=["SubCat2l"]

varPerCat={
"SubCat2l":["DNN_maxval","DNN_maxval_option2","Bin2l","leadLep_jetdr","secondLep_jetdr","n_presel_jet","nBJetLoose","nBJetMedium","jet1_pt","jet2_pt","jet3_pt","jet4_pt","jet1_eta","jet2_eta","jet3_eta","jet4_eta","Hj_tagger_resTop","metLD","maxeta","massL","avg_dr_jet","mbb","mT_lep1","mT_lep2","lep1_conePt","lep1_eta","lep2_conePt","lep2_eta","resTop_BDT","Dilep_mtWmin","massll","Sum2lCharge","MHT","Dilep_pdgId","Dilep_htllv","HighestJetCSV","HtJet","minMllAFOS","minMllAFAS","minMllSFOS","nLepFO","nLepTight","mbb_loose","dr_leps","mvaOutput_2lss_ttV","mvaOutput_2lss_ttbar","n_presel_ele","n_presel_mu"],
"DNNCat":["DNN_maxval","DNN_maxval_option2","Bin2l","leadLep_jetdr","secondLep_jetdr","n_presel_jet","nBJetLoose","nBJetMedium","jet1_pt","jet2_pt","jet3_pt","jet4_pt","jet1_eta","jet2_eta","jet3_eta","jet4_eta","Hj_tagger_resTop","metLD","maxeta","massL","avg_dr_jet","mbb","mT_lep1","mT_lep2","lep1_conePt","lep1_eta","lep2_conePt","lep2_eta","resTop_BDT","Dilep_mtWmin","massll","Sum2lCharge","MHT","Dilep_pdgId","Dilep_htllv","HighestJetCSV","HtJet","minMllAFOS","minMllAFAS","minMllSFOS","nLepFO","nLepTight","mbb_loose","dr_leps","mvaOutput_2lss_ttV","mvaOutput_2lss_ttbar","n_presel_ele","n_presel_mu"],
#"DNNCat":["DNN_maxval"],
"DNNCat":["DNN_maxval","DNN_maxval_option2","Bin2l","leadLep_jetdr","secondLep_jetdr","n_presel_jet","nBJetLoose","nBJetMedium","jet1_pt","jet2_pt","jet3_pt","jet4_pt","jet1_eta","jet2_eta","jet3_eta","jet4_eta","Hj_tagger_resTop","metLD","maxeta","massL","avg_dr_jet","mbb","mT_lep1","mT_lep2","lep1_conePt","lep1_eta","lep2_conePt","lep2_eta","resTop_BDT","Dilep_mtWmin","massll","Sum2lCharge","MHT","Dilep_pdgId","Dilep_htllv","HighestJetCSV","HtJet","minMllAFOS","minMllAFAS","minMllSFOS","nLepFO","nLepTight","mbb_loose","dr_leps","mvaOutput_2lss_ttV","mvaOutput_2lss_ttbar","n_presel_ele","n_presel_mu"],
"DNNCat_option2":["DNN_maxval_option2"],
"DNNCat_option3":["DNN_maxval_option3"],
"DNNSubCat1_option1":["DNN_maxval"],
"DNNSubCat1_option2":["DNN_maxval_option2"],
"DNNSubCat1_option3":["DNN_maxval_option3"],
"DNNSubCat2_option1":["DNN_maxval"],
"DNNSubCat2_option2":["DNN_maxval_option2"],
"DNNSubCat2_option3":["DNN_maxval_option3"],
}

# show 2lss for the moment
regPerCat={
"SubCat2l":["DiLepRegion"],
"DNNCat":["DiLepRegion"],
"DNNCat_option2":["2lss"],
"DNNCat_option3":["2lss"],
"DNNSubCat1_option1":["2lss"],
"DNNSubCat1_option2":["2lss"],
"DNNSubCat1_option3":["2lss"],
"DNNSubCat2_option1":["2lss"],
"DNNSubCat2_option2":["2lss"],
"DNNSubCat2_option3":["2lss"],
}

dirName = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplasDNN_20190613_LongerFully/Rootplas/Output_GT20/"

for category in Categories:
    for var in varPerCat[category]:
        print ( "plot var: "+var+ " in cat: "+ category)
        for reg in regPerCat[category]:
            command_run = "python plotHists.py -r "+reg+" -p "+var+" -c "+category+" -d "+dirName+" -s inclusive" 
            print(command_run) 
            os.system(command_run)
