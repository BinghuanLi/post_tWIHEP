import sys, os, subprocess
import commands
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread

#Regions=["SigRegion","ttWctrl","DiLepRegion"]
Regions=["DiLepRegion"]

#DirOfRegions = ["ttH2016TrainDNN2L","ttH2016TrainHj2L","ttH2017TrainDNN2L","ttH2017TrainHj2L","ttH2018TrainDNN2L","ttH2018TrainHj2L"]
DirOfRegions = ["ttH2018TrainDNN2L","ttH2018TrainHj2L"]


#ProcessesMVA = ["ttHnobb","ttZJets","ttWJets","ttJets","ttJets_PS","ttJ_mad","ttJ_amc","TTH_ctcvcp","THQ_ctcvcp","THW_ctcvcp"]
ProcessesMVA = ["THW_ctcvcp"]

Samples= {
"2016":{
"ttHnobb":["Legacy16V1_TTHnobb"],
"THQ_ctcvcp":["Legacy16V1_THQ_Tune8M1_ctcvcp"],
"THW_ctcvcp":["Legacy16V1_THW_Tune8M1_ctcvcp"],
"ttZJets":["Legacy16V1_ttZ"],
"ttWJets":["Legacy16V1_ttW"],
"ttJets_PS":["Legacy16V1_TTTo2L_PS","Legacy16V1_TTToSemiLep_PS","Legacy16V1_TTToHad_PS"],
},
"2017":{
"ttHnobb":["Legacy17V1_TTHnobb_v1","Legacy17V1_TTHnobb_ext"],
"ttZJets":["Legacy17V1_ttZ_ext","Legacy17V1_ttZ_v1"],
"ttWJets":["Legacy17V1_ttW_v1","Legacy17V1_ttW_ext"],
"ttJets_PS":["Legacy17V1_TTTo2L_PS","Legacy17V1_TTToSemiLep_PS","Legacy17V1_TTToHad_PS"],
"ttJets":["Legacy17V1_TTTo2L","Legacy17V1_TTToSemiLep","Legacy17V1_TTToHad"],
},
"2018":{
"ttHnobb":["Legacy18V1_TTHnobb"],
"ttZJets":["Legacy18V1_ttZ_Tune"],
"ttWJets":["Legacy18V1_ttW_Tune"],
"THQ_ctcvcp":["Legacy18V1_THQ_ctcvcp"],
"THW_ctcvcp":["Legacy18V1_THW_ctcvcp"],
"ttJets":["Legacy18V1_TTTo2L","Legacy18V1_TTToSemiLep","Legacy18V1_TTToHad"],
"ttJ_mad":["Legacy18V1_TTJets_mad"],
"ttJ_amc":["Legacy18V1_TTJets_amc"],
}
}

BaseDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplas_LegacyMVA_20190927/"

if not os.path.exists("Rootplas/TrainMVA"):
    os.popen("mkdir -p Rootplas/TrainMVA")

InfoFileName = "InfoSkim.txt"
InfoFile      = file(InfoFileName,"w")

for Region in Regions:
    OutputRegionDir = BaseDir+"Rootplas/TrainMVA/"+Region
    if not os.path.exists("Rootplas/TrainMVA/" + Region):
        os.popen("mkdir -p Rootplas/TrainMVA/"+Region)
    for dirOfRegion in DirOfRegions:
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
        if not os.path.exists("skims"):
            os.popen("mkdir skims")
        dirsToCheck = [f for f in os.listdir(".") if os.path.isdir(f)]
        if "skims" in dirsToCheck : dirsToCheck.remove("skims")
        Processes = ProcessesMVA
        for p in Processes:
            for d in dirsToCheck:
                command_ls_channel = "ls -ltr "+d+"/skims/merged"+d+"_"+Region+".root"
                checkfile = commands.getstatusoutput(command_ls_channel)
                if checkfile[0]!=512:
                    command_mv_file = "mv "+d+"/skims/merged"+d+"_"+Region+".root skims/"
                    os.popen(command_mv_file)
        for p in Processes:
            if not os.path.exists(OutputRegionDir+"/" + dirOfRegion):
                os.popen("mkdir -p "+OutputRegionDir+"/"+dirOfRegion)
            outputfilename = OutputRegionDir+"/"+dirOfRegion+"/"+p+"_"+Region+".root"
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
                if not os.path.exists("skims/merged"+i+"_"+Region+".root"):
                    print >>  InfoFile, " Region " + Region + " missed sample in process " + p  + " : "+i
                    continue
                inputfile = inputfile + " skims/merged"+i+"_"+Region+".root"
            command_ls_merge = "hadd -f " + outputfilename + inputfile
            print(command_ls_merge)
            os.system(command_ls_merge)
             
    os.chdir(BaseDir)
