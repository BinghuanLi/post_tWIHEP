import sys, os, subprocess
import commands
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread



#Regions=["SigRegion","ttWctrl","NoJetNCut"]
Regions=["ttWctrl"]

DirOfRegions = ["ttH2LAll2L","ttH2LAllJESUp","ttH2LAllJESDown","ttHData2LAll2L"]

HiggsDecay = {"hww":2,"hzz":6,"htt":3, "hmm":11, "hot":999}

frameworkDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/IHEPJobs/"
BaseDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplasV1_20190212/"

#ProcessesAll = [ "TTH", "TTZ", "TTW", "Conv", "EWK", "Rares","H","TTWW","Fakes","Flips","Data"]
ProcessesAll = [ "TTH_hww", "THW_hww","THQ_hww", "TTH_htt", "THW_htt","THQ_htt","TTH_hzz", "THW_hzz","THQ_hzz", "TTH_hmm", "TTH_hot", "TTZ", "TTW", "Conv", "EWK", "Rares","TTWW","FakeSub","FlipSub","Fakes","Flips","Data"]
ProcessesJES = [ "TTH_hww", "THW_hww","THQ_hww", "TTH_htt", "THW_htt","THQ_htt","TTH_hzz", "THW_hzz","THQ_hzz", "TTH_hmm", "TTH_hot", "TTZ", "TTW", "Conv", "EWK", "Rares","TTWW","FakeSub","FlipSub"]
ProcessesData = ["Fakes","Flips","Data"] 

Samples= {
"TTH":["TTHnobb"], # madspin
"TTH_hww":["TTHnobb"], # madspin
"TTH_hzz":["TTHnobb"], # madspin
"TTH_htt":["TTHnobb"], # madspin
"TTH_hmm":["TTHnobb"], # madspin
"TTH_hot":["TTHnobb"], # madspin
"TTZ":["TTZToLLNuNu_M10","TTZToLL_M1to10","TT_PSwgt_To2L2Nu","TT_PSwgt_ToSemiLep","TT_PSwgt_ToHadron"],
"TTW":["TTWToLNu"],
"TTWW":["TTWW"],
"H":["THQ","THW"],
"THW_hww":["THW"],
"THW_hzz":["THW"],
"THW_htt":["THW"],
"THQ_hww":["THQ"],
"THQ_hzz":["THQ"],
"THQ_htt":["THQ"],
"EWK":["W1JetsToLNu","W2JetsToLNu","W3JetsToLNu","W4JetsToLNu","WZTo3LNu","ZZ_ext_To4L"],
"Conv":["TTGJets","TGJets_Lep","W1JetsToLNu","W2JetsToLNu","W3JetsToLNu","W4JetsToLNu","DY1JetsToLL_M50","DY2JetsToLL_M50", "DY3JetsToLL_M50", "DY4JetsToLL_M50", "DYJetsToLL_M4to50_HT70to100","DYJetsToLL_M4to50_HT100to200", "DYJetsToLL_M4to50_HT200to400", "DYJetsToLL_M4to50_HT400to600", "DYJetsToLL_M4to50_HT600toInf"],
"Rares":["DY_M10to50","DY_ext_M50","WW_DoubleScatter","WWW","WWZ","WZZ","ZZZ","TTTT_Tune","tWll","tZq","WpWpJJ","TTTW","TTWH","GGH_ext_ToZZ4L","VHToNobb"],
"FakeSub":["TTHnobb","TTZToLLNuNu_M10","TTZToLL_M1to10","TT_PSwgt_To2L2Nu","TT_PSwgt_ToSemiLep","TT_PSwgt_ToHadron","TTWToLNu","TTWW","THW","THQ","W1JetsToLNu","W2JetsToLNu","W3JetsToLNu","W4JetsToLNu","WZTo3LNu","ZZ_ext_To4L","DY_M10to50","DY_ext_M50","WW_DoubleScatter","WWW","WWZ","WZZ","ZZZ","TTTT_Tune","tWll","tZq","WpWpJJ","TTTW","TTWH","GGH_ext_ToZZ4L","VHToNobb"],
"FlipSub":["TTHnobb","TTZToLLNuNu_M10","TTZToLL_M1to10","TT_PSwgt_To2L2Nu","TT_PSwgt_ToSemiLep","TT_PSwgt_ToHadron","TTWToLNu","TTWW","THW","THQ","W1JetsToLNu","W2JetsToLNu","W3JetsToLNu","W4JetsToLNu","WZTo3LNu","ZZ_ext_To4L","DY_M10to50","DY_ext_M50","WW_DoubleScatter","WWW","WWZ","WZZ","ZZZ","TTTT_Tune","tWll","tZq","WpWpJJ","TTTW","TTWH","GGH_ext_ToZZ4L","VHToNobb"],
"Fakes":[ "SEleBlockB", "SEleBlockC", "SEleBlockD", "SEleBlockE", "SEleBlockF", "SMuBlockB", "SMuBlockC", "SMuBlockD", "SMuBlockE", "SMuBlockF", "DblEGBlockB", "DblEGBlockC", "DblEGBlockD", "DblEGBlockE", "DblEGBlockF", "DblMuBlockB", "DblMuBlockC", "DblMuBlockD", "DblMuBlockE", "DblMuBlockF", "MuEGBlockB", "MuEGBlockC", "MuEGBlockD", "MuEGBlockE", "MuEGBlockF"],
"Flips":[ "SEleBlockB", "SEleBlockC", "SEleBlockD", "SEleBlockE", "SEleBlockF", "SMuBlockB", "SMuBlockC", "SMuBlockD", "SMuBlockE", "SMuBlockF", "DblEGBlockB", "DblEGBlockC", "DblEGBlockD", "DblEGBlockE", "DblEGBlockF", "DblMuBlockB", "DblMuBlockC", "DblMuBlockD", "DblMuBlockE", "DblMuBlockF", "MuEGBlockB", "MuEGBlockC", "MuEGBlockD", "MuEGBlockE", "MuEGBlockF"],
"Data":[ "SEleBlockB", "SEleBlockC", "SEleBlockD", "SEleBlockE", "SEleBlockF", "SMuBlockB", "SMuBlockC", "SMuBlockD", "SMuBlockE", "SMuBlockF", "DblEGBlockB", "DblEGBlockC", "DblEGBlockD", "DblEGBlockE", "DblEGBlockF", "DblMuBlockB", "DblMuBlockC", "DblMuBlockD", "DblMuBlockE", "DblMuBlockF", "MuEGBlockB", "MuEGBlockC", "MuEGBlockD", "MuEGBlockE", "MuEGBlockF"],

}


if not os.path.exists("Rootplas"):
    os.popen("mkdir Rootplas")

InfoFileName = "InfoSkim.txt"
InfoFile      = file(InfoFileName,"w")

for Region in Regions:
    OutputRegionDir = BaseDir+"Rootplas/"+Region
    if not os.path.exists("Rootplas/" + Region+"/"+Region):
        os.popen("mkdir -p Rootplas/"+Region+"/"+Region)
    if not os.path.exists("Rootplas/" + Region +"/JESUp"+Region):
        os.popen("mkdir -p Rootplas/"+Region+"/JESUp"+Region)
    if not os.path.exists("Rootplas/" + Region +"/JESDown"+Region):
        os.popen("mkdir -p Rootplas/"+Region+"/JESDown"+Region)
    for dirOfRegion in DirOfRegions:
        if os.path.exists(BaseDir+dirOfRegion):
            os.chdir(BaseDir+dirOfRegion)
        else:
            print >> InfoFile, "Dir " + BaseDir + dirOfRegion + " deosn't exist !!! Skip !!!"
            continue
        dirsToCheck = [f for f in os.listdir(".") if os.path.isdir(f)]
        #if "Skim" in dirsToCheck : dirsToCheck.remove("Skim")
        Processes = ProcessesAll
        OutputDir = ""
        jesFix =""
        if "JESUp"  in dirOfRegion:
            OutputDir = OutputRegionDir +"/JESUp"+Region
            jesFix ="JESUp"
            Processes = ProcessesJES
        elif "JESDown"  in dirOfRegion:
            OutputDir = OutputRegionDir +"/JESDown"+Region
            jesFix ="JESDown"
            Processes = ProcessesJES
        elif "Data"  in dirOfRegion:
            OutputDir = OutputRegionDir +"/"+Region
            jesFix =""
            Processes = ProcessesData
        else:
            OutputDir = OutputRegionDir + "/"+Region
            Processes = ProcessesJES
            jesFix =""
        for p in Processes:
            dirsToSkims = [f for f in dirsToCheck if f in Samples[p]]
            inputfiles=""
            outputfile = OutputDir+"/"+p+"_"+jesFix+Region+".root"
            # skim files if H
            for d in dirsToSkims:
                sampleType ="Prompt2lss"
                if p == "FakeSub": sampleType="Promptfake"
                elif p == "FlipSub": sampleType="Promptflip"
                elif p == "Conv": sampleType="Conv2lss"
                elif p == "Data": sampleType="Data"
                elif p == "Fakes": sampleType="Fake"
                elif p == "Flips": sampleType="Flip"
                command_ls_channel = "ls -ltr " +d+"/skims/merged"+d+"_"+sampleType+"_"+Region+".root"
                checkfile = commands.getstatusoutput(command_ls_channel)
                print (command_ls_channel)
                if checkfile[0]!=512:
                    if os.path.getsize(d+"/skims/merged"+d+"_"+sampleType+"_"+Region+".root") < 10000 : continue
                    filterHiggs = 0
                    if ("TTH" in p or "ttH" in p or "THQ" in p or "THW" in p) and "Train" not in dirOfRegion:
                        higgsType = "" 
                        if "htt" in p :
                            filterHiggs = HiggsDecay["htt"]
                            higgsType = "htt"
                        elif "hzz" in p : 
                            filterHiggs = HiggsDecay["hzz"]
                            higgsType = "hzz"
                        elif "hww" in p : 
                            filterHiggs = HiggsDecay["hww"]
                            higgsType = "hww"
                        elif "hmm" in p : 
                            filterHiggs = HiggsDecay["hmm"]
                            higgsType = "hmm"
                        elif "hot" in p : 
                            filterHiggs = HiggsDecay["hot"]
                            higgsType = "hot"
                        command_skim = "root -l -b -q "+frameworkDir+"copytree.C'("+'"'+d+"/skims/"+'","'+d+"/skims"+'","'+d+'","'+d+"_"+higgsType+'","'+sampleType+"_"+Region+'","'+jesFix+Region+'",'+str(filterHiggs)+")'"
                        print (command_skim)
                        os.system(command_skim)
                        if os.path.getsize(d+"/skims/merged"+d+"_"+higgsType+"_"+jesFix+Region+".root") < 10000 : continue
                        inputfiles += (d+"/skims/merged"+d+"_"+higgsType+"_"+jesFix+Region+".root ")
                    else:
                        print ("add normal files to merged: " + d+"/skims/merged"+d+"_"+sampleType+"_"+Region+".root ")
                        inputfiles += (d+"/skims/merged"+d+"_"+sampleType+"_"+Region+".root ")

            command_ls_merge = "hadd -f " + outputfile + " " + inputfiles
            print(command_ls_merge)
            os.system(command_ls_merge)
             
    os.chdir(BaseDir)
