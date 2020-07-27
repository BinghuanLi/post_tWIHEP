import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread
import shlex
import multiprocessing
from subprocess import Popen, PIPE
import time



#Categories=["DNNCat","DNNSubCat1_option1","DNNSubCat2_option1"]
Categories=["SubCat2l"]
#Categories=["DNNSubCat2_option1"]
#Categories=["SVACat3j","SubCat2l"]
varPerCat={
"SubCat2l":[
    "Bin2l",
    #"lep1_conePt",
    #"DNN_maxval", "DNN_ttHnode_all", "DNN_ttWnode_all", "DNN_Restnode_all", "DNN_tHQnode_all", "nBJetMedium", "nBJetLoose", "n_presel_jet", "n_presel_jetFwd", "Bin2l", "SVABin2l", "mvaOutput_2lss_ttV", "mvaOutput_2lss_ttbar", "Hj_tagger_hadTop", "Hj_tagger", "hadTop_BDT", "Dilep_pdgId", "avg_dr_jet", "lep1_charge", "lep1_conePt", "lep2_conePt", "lep1_eta", "lep2_eta", "lep1_phi", "lep2_phi", "jet1_pt", "jet2_pt", "jet3_pt", "jet4_pt", "jet1_eta", "jet2_eta", "jet3_eta", "jet4_eta", "jet1_phi", "jet2_phi", "jet3_phi", "jet4_phi", "jetFwd1_pt", "jetFwd1_eta", "mT_lep1", "mT_lep2", "maxeta", "mbb", "metLD", "mindr_lep1_jet", "mindr_lep2_jet"
    ],
"SVACat2l":["SVABin2l"],
"SVACat3j":[
    "DNN_maxval", "DNN_ttHnode_all", "DNN_ttWnode_all", "DNN_Restnode_all", "DNN_tHQnode_all", "nBJetMedium", "nBJetLoose", "n_presel_jet", "n_presel_jetFwd", "Bin2l", "SVABin2l", "mvaOutput_2lss_ttV", "mvaOutput_2lss_ttbar", "Hj_tagger_hadTop", "Hj_tagger", "hadTop_BDT", "Dilep_pdgId", "avg_dr_jet", "lep1_charge", "lep1_conePt", "lep2_conePt", "lep1_eta", "lep2_eta", "lep1_phi", "lep2_phi", "jet1_pt", "jet2_pt", "jet3_pt", "jet4_pt", "jet1_eta", "jet2_eta", "jet3_eta", "jet4_eta", "jet1_phi", "jet2_phi", "jet3_phi", "jet4_phi", "jetFwd1_pt", "jetFwd1_eta", "mT_lep1", "mT_lep2", "maxeta", "mbb", "metLD", "mindr_lep1_jet", "mindr_lep2_jet",
],
"DNNCat":["DNN_maxval"],
"DNNCat_option2":["DNN_maxval_option2"],
#"DNNCat_option2":["DNN_maxval_option2","Bin2l","leadLep_jetdr","secondLep_jetdr","n_presel_jet","nBJetLoose","nBJetMedium","jet1_pt","jet2_pt","jet3_pt","jet4_pt","jet1_eta","jet2_eta","jet3_eta","jet4_eta","Hj_tagger_resTop","metLD","maxeta","massL","avg_dr_jet","mbb","mT_lep1","mT_lep2","lep1_conePt","lep1_eta","lep2_conePt","lep2_eta","resTop_BDT"],
"DNNCat_option3":["DNN_maxval_option3"],
"DNNSubCat1_option1":["DNN_maxval"],
"DNNSubCat1_option2":["DNN_maxval_option2"],
"DNNSubCat1_option3":["DNN_maxval_option3"],
"DNNSubCat2_option1":["DNNSubCat2_BIN"],
#"DNNSubCat2_option1":["DNN_maxval","DNNSubCat2_BIN","DNNSubCat2_nBin1","DNNSubCat2_nBin2","DNNSubCat2_nBin3","DNNSubCat2_nBin4","DNNSubCat2_nBin5","DNNSubCat2_nBin6","DNNSubCat2_nBin7","DNNSubCat2_nBin8","DNNSubCat2_nBin9","DNNSubCat2_nBin10","DNNSubCat2_nBin11", "DNNSubCat2_nBin12","DNNSubCat2_nBin13","DNNSubCat2_nBin14","DNNSubCat2_nBin15","DNNSubCat2_nBin16", "DNNSubCat2_nBin17","DNNSubCat2_nBin18","DNNSubCat2_nBin19"],
#"DNNSubCat2_option1":["DNN_maxval","DNNSubCat2_BIN","DNNSubCat2_nBin3","DNNSubCat2_nBin5","DNNSubCat2_nBin13"],
"DNNSubCat2_option2":["DNNSubCat2_option2_BIN"],
"DNNSubCat2_option3":["DNN_maxval_option3"],
"DNNAMS2Cat1_option1":["DNN_maxval"],
"DNNAMS2Cat1_option2":["DNN_maxval_option2"],
"DNNAMS2Cat1_option3":["DNN_maxval_option3"],
"DNNAMS3Cat1_option1":["DNN_maxval"],
"DNNAMS3Cat1_option2":["DNN_maxval_option2"],
"DNNAMS3Cat1_option3":["DNN_maxval_option3"],
}

Uncs = ["All"]
Opts = {
"All":" ",
"NoStat":" -m ",
"NoSyst":" -s ",
"NoShape":" -t ",
"None":" -s -m ",
}


def makecards(inDir, outName, syst_ctcvcp, year, useData=False):
        starttime = time.time()
        
        dirfix = "exp"
        unblind = "" 
        if useData:
            unblind = " --unblind "
            dirfix = "obs"
        
        version = "%s_%s"%(outName, dirfix)
        inputDir = "%s/Output_%i_GT5"%(inDir,year)

        if createROOT :
          for category in Categories:
            if not os.path.exists(inputDir+"/"+category+"/SystsDiLepRegion"):
                os.popen("mkdir -p "+inputDir+"/"+category+"/Systs2lss")
                os.popen("mkdir -p "+inputDir+"/"+category+"/SyststtWctrl")
                os.popen("mkdir -p "+inputDir+"/"+category+"/Systs2lss_0tau")
            for var in varPerCat[category]:
                DirName_datacard = version+"_datacards/"+category+"/"+var
                print ( "write histograms for var: "+var+ " in cat: "+ category)
                if not os.path.exists(DirName_datacard):
                    os.popen("mkdir -p "+DirName_datacard)
                for name in namefix:
                    if len(syst_ctcvcp)==0:
                        command_run = "python createDatacardRootFile.py -s 0 -i "+inputDir+"/"+category+"/ -o "+DirName_datacard+"/ -v "+var+" -c "+category+ " -y " + str(year)+ " -n "+ name +unblind + " > "+DirName_datacard+"/Information.txt"
                    else:
                        command_run = "python createDatacardRootFile.py -s 0 -i "+inputDir+"/"+category+"/ -o "+DirName_datacard+"/ -v "+var+" -c "+category+ " -y " + str(year)+ " -n "+ name + unblind+" -p "+syst_ctcvcp+" > "+DirName_datacard+"/Information.txt"
                    print(command_run)
                    os.system(command_run) 
        
        for Unc in Uncs:
            for category in Categories:
                for var in varPerCat[category]:
                    DirName_datacard = version+"_datacards_"+Unc+"/"+category+"/"+var
                    print ( "write txt for var: "+var+ " in cat: "+ category)
                    if not os.path.exists(DirName_datacard):
                        os.popen("mkdir -p "+DirName_datacard)
                    command_cp = "cp "+version+"_datacards/"+category+"/"+var+"/*"+str(year)+"*"+syst_ctcvcp+".root " +version+"_datacards_"+Unc+"/"+category+"/"+var
                    print(command_cp)
                    os.system(command_cp)
                    for name in namefix:
                        command_run = "python datacard_Template.py -i "+version+"_datacards_"+Unc+"/ -v "+var+" -c "+category+Opts[Unc]+ " -p _"+ syst_ctcvcp + " -y " + str(year) +" -n " + name +" > "+DirName_datacard+"/datacard.log"
                        print(command_run) 
                        #try:
                        #    p2 = Popen(shlex.split(command_run), stdout=PIPE, stderr=PIPE, cwd=inDir)
                        #    comboutput = p2.communicate()[0]
                        #except OSError:
                        #    print " command_run failed"
                        #    comboutput = None
                        os.system(command_run) 
        elapsed = time.time() - starttime
        return " %i-ITC-%s-%s-: -30s \033[92mDone\033[0m in %.2f min" % (year, syst_ctcvcp, dirfix, elapsed/60.)

years=[2016,2017,2018]
#years=[2016]
#namefix= ["ttH", "tHq"] # "ttH" for normal usage, "tHq" for kt kv usage
namefix= ["ttH"] # "ttH" for normal usage, "tHq" for kt kv usage
createROOT= True

systs_ctcvcp = [
#"",
"kt_m3_kv_1",
"kt_m2_kv_1","kt_m1p5_kv_1","kt_m1p25_kv_1","kt_m0p75_kv_1","kt_m0p5_kv_1","kt_m0p25_kv_1","kt_0_kv_1","kt_0p25_kv_1","kt_0p5_kv_1","kt_0p75_kv_1",
"kt_1_kv_1",
"kt_m1_kv_1",
"kt_1p25_kv_1",
"kt_1p5_kv_1","kt_2_kv_1","kt_3_kv_1",
"kt_m2_kv_1p5","kt_m1p5_kv_1p5","kt_m1p25_kv_1p5","kt_m1_kv_1p5","kt_m0p5_kv_1p5","kt_m0p25_kv_1p5","kt_0p25_kv_1p5","kt_0p5_kv_1p5","kt_1_kv_1p5","kt_1p25_kv_1p5","kt_2_kv_1p5",
"kt_m3_kv_0p5","kt_m2_kv_0p5","kt_m1p25_kv_0p5","kt_1p25_kv_0p5","kt_2_kv_0p5","kt_3_kv_0p5",
#"cosa_m0p9","cosa_m0p8","cosa_m0p7","cosa_m0p6","cosa_m0p5","cosa_m0p4","cosa_m0p3","cosa_m0p2","cosa_m0p1","cosa_mp0","cosa_0p1","cosa_0p2","cosa_0p3","cosa_0p4","cosa_0p5","cosa_0p6","cosa_0p7","cosa_0p8","cosa_0p9"
]
inputDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/mvaTool_LegacyAll_DNN_ITC_20200624"
outlabel = "PHD_ITC_BDT_0629"

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=8)
    futures = []
    starttime = time.time()
    tfs=[False, True]
    #tfs=[True]
    for tf in tfs:
        for syst in systs_ctcvcp:
            for era in years:
                #jobname ="unblind % % ktkv-%"%(tf, era, syst)
                future = pool.apply_async(makecards,(inputDir, outlabel, syst, era, tf))
                futures.append(future)

    for n, future in enumerate(futures):
        printout = future.get()
        print "%s (%d/%d)" % (printout, n, len(futures))

    print " \033[1m \033[92mAll Done\033[0m in %.2f min" % ((time.time()-starttime)/60.)
