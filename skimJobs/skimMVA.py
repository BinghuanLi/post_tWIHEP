import sys, os, subprocess
import commands
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread

#Regions=["SigRegion","ttWctrl","NoJetNCut"]
Regions=["NoJetNCut"]

DirOfRegions = ["ttHTrainMVA2L"]


ProcessesMVA = ["ttHnobb","ttZJets","ttWJets","ttJets"]

Samples= {
"ttHnobb":["ttHnobb"],
"ttZJets":["ttZ_ext_Jets","ttZ_Jets"],
"ttWJets":["ttW_ext_Jets","ttWJets"],
"ttJets":["TT_PSwgt_ToSemiLep","TT_PSwgt_ToHadron","TT_PSwgt_To2L2Nu","TTToSemiLep","TTToHadron","TTTo2L2Nu"]
}

BaseDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplas_mva_20190220/"

if not os.path.exists("Rootplas/TrainMVA"):
    os.popen("mkdir -p Rootplas/TrainMVA")

InfoFileName = "InfoSkim.txt"
InfoFile      = file(InfoFileName,"w")

for Region in Regions:
    OutputRegionDir = BaseDir+"Rootplas/TrainMVA/"+Region
    if not os.path.exists("Rootplas/TrainMVA/" + Region):
        os.popen("mkdir -p Rootplas/TrainMVA/"+Region)
    for dirOfRegion in DirOfRegions:
        if os.path.exists(BaseDir+dirOfRegion):
            os.chdir(BaseDir+dirOfRegion)
        else:
            print >> InfoFile, "Dir " + BaseDir + dirOfRegion + " deosn't exist !!! Skip !!!"
            continue
        if not os.path.exists("skims"):
            os.popen("mkdir skims")
        dirsToCheck = [f for f in os.listdir(".") if os.path.isdir(f)]
        if "skims" in dirsToCheck : dirsToCheck.remove("skims")
        Processes = ProcessesMVA
        for p in Processes:
            for d in dirsToCheck:
                command_ls_channel = "ls -ltr "+d+"/skims/merged"+d+"_TrainMVA_"+Region+".root"
                checkfile = commands.getstatusoutput(command_ls_channel)
                if checkfile[0]!=512:
                    command_mv_file = "mv "+d+"/skims/merged"+d+"_TrainMVA_"+Region+".root skims/"
                    os.popen(command_mv_file)
        for p in Processes:
            outputfilename = OutputRegionDir+"/"+p+"_"+Region+".root"
            inputfile = " "
            for i in Samples[p]:
                if not os.path.exists("skims/merged"+i+"_TrainMVA_"+Region+".root"):
                    print >>  InfoFile, " Region " + Region + " missed sample in process " + p  + " : "+i
                    continue
                inputfile = inputfile + " skims/merged"+i+"_TrainMVA_"+Region+".root"
            command_ls_merge = "hadd -f " + outputfilename + inputfile
            print(command_ls_merge)
            os.system(command_ls_merge)
             
    os.chdir(BaseDir)
