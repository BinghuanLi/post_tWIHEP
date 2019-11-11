import os
import sys
import ROOT

SR_base_dir = "/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/data/rootplas_V2_20191025/DiLepRegion/"

TR_base_dir = "/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_NNs/data/LegacyMVA_1108/DiLepRegion/"

outputdir = TR_base_dir + "TR_SR_RunII"
if not os.path.exists(outputdir):
    print ('mkdir: ', outputdir)
    os.makedirs(outputdir)


filenames = {
    #"TTH_TR_2016":["ttH2016TrainDNN2L/ttHnobb_DiLepRegion.root"],
    #"THQ_TR_2016":["ttH2016TrainDNN2L/THQ_ctcvcp_DiLepRegion.root"],
    #"THW_TR_2016":["ttH2016TrainDNN2L/THW_ctcvcp_DiLepRegion.root"],
    #"TTW_TR_2016":["ttH2016TrainDNN2L/ttWJets_DiLepRegion.root"],
    #"TTJ_TR_2016":["ttH2016TrainDNN2L/ttJets_PS_DiLepRegion.root"],
    #"TTH_TR_2017":["ttH2017TrainDNN2L/ttHnobb_DiLepRegion.root"],
    ###"THQ_TR_2017":["ttH2017TrainDNN2L/THQ_ctcvcp_DiLepRegion.root"],
    #"TTW_TR_2017":["ttH2017TrainDNN2L/ttWJets_DiLepRegion.root"],
    #"TTJ_TR_2017":["ttH2017TrainDNN2L/ttJets_PS_DiLepRegion.root"],
    #"TTH_TR_2018":["ttH2018TrainDNN2L/ttHnobb_DiLepRegion.root"],
    #"THQ_TR_2018":["ttH2018TrainDNN2L/THQ_ctcvcp_DiLepRegion.root"],
    #"THW_TR_2018":["ttH2018TrainDNN2L/THW_ctcvcp_DiLepRegion.root"],
    #"TTW_TR_2018":["ttH2018TrainDNN2L/ttWJets_DiLepRegion.root"],
    #"TTJ_TR_2018":["ttH2018TrainDNN2L/ttJets_DiLepRegion.root"],
    #"TTH_SR_2016":["2016/DiLepRegion/TTH_DiLepRegion.root"],
    #"THQ_SR_2016":["2016/DiLepRegion/THQ_DiLepRegion.root"],
    #"THW_SR_2016":["2016/DiLepRegion/THW_DiLepRegion.root"],
    #"TTW_SR_2016":["2016/DiLepRegion/TTW_DiLepRegion.root"],
    "TTJ_SR_2016":["2016/DiLepRegion/mcFakes_DiLepRegion.root","2016/DiLepRegion/mcFlips_DiLepRegion.root"],
    #"TTH_SR_2017":["2017/DiLepRegion/TTH_DiLepRegion.root"],
    #"THQ_SR_2017":["2017/DiLepRegion/THQ_DiLepRegion.root"],
    #"THW_SR_2017":["2017/DiLepRegion/THW_DiLepRegion.root"],
    #"TTW_SR_2017":["2017/DiLepRegion/TTW_DiLepRegion.root"],
    "TTJ_SR_2017":["2017/DiLepRegion/mcFakes_DiLepRegion.root","2017/DiLepRegion/mcFlips_DiLepRegion.root"],
    #"TTH_SR_2018":["2018/DiLepRegion/TTH_DiLepRegion.root"],
    #"THQ_SR_2018":["2018/DiLepRegion/THQ_DiLepRegion.root"],
    #"THW_SR_2018":["2018/DiLepRegion/THW_DiLepRegion.root"],
    #"TTW_SR_2018":["2018/DiLepRegion/TTW_DiLepRegion.root"],
    "TTJ_SR_2018":["2018/DiLepRegion/mcFakes_DiLepRegion.root","2018/DiLepRegion/mcFlips_DiLepRegion.root"],
    }



for key, values in filenames.items():
    inputdir = SR_base_dir
    if "_TR_" in key:
        inputdir = TR_base_dir
    cmd = "hadd -f %s/%s.root "%(outputdir, key)
    for value in values:
        cmd += "%s/%s "%(inputdir,value)
    print ( " command ".format(cmd))
    os.system(cmd)

