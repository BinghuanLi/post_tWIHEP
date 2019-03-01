import sys
import os
import glob
import string
import subprocess
from string import digits
#####
##   Parameters to be specified by the user
#####
#analysis and task
#Regions=["SigRegion","ttWctrl","NoJetNCut"]
Regions=["SigRegion"]

#DirOfRegions = ["ttH2LAll2L","ttH2LAllJESUp","ttH2LAllJESDown","ttHData2LAll2L"]
DirOfRegions = ["ttH2LAll2L"]

analysis = ""
taskname = "EvtSel"
frameworkDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/Fall17V1/"
inputBaseDir =  "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/skims_20190212/"
outputBaseDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplas_angle_20190212/"

usePromptFake = False

executable_Prompt_2lss = "Rootplas_Prompt_2lss.C"
executable_Prompt_fake = "Rootplas_Prompt_fake.C"
executable_Prompt_flip = "Rootplas_Prompt_flip.C"
executable_Conv_2lss = "Rootplas_Conv_2lss.C"
executable_Data_2lss = "Rootplas_Data_2lss.C"
executable_Fake_2lss = "Rootplas_Fake_2lss.C"
executable_Flip_2lss = "Rootplas_Flip_2lss.C"
executable_TrainMVA_2lss = "Rootplas_TrainMVA_2lss.C"


samples94XData = [
"SEleBlockB", "SEleBlockC", "SEleBlockD", "SEleBlockE", "SEleBlockF", "SMuBlockB", "SMuBlockC", "SMuBlockD", "SMuBlockE", "SMuBlockF", "DblEGBlockB", "DblEGBlockC", "DblEGBlockD", "DblEGBlockE", "DblEGBlockF", "DblMuBlockB", "DblMuBlockC", "DblMuBlockD", "DblMuBlockE", "DblMuBlockF", "MuEGBlockB", "MuEGBlockC", "MuEGBlockD", "MuEGBlockE", "MuEGBlockF"
]
samples94XConv = [
"TTGJets","TGJets_Lep","W1JetsToLNu","W2JetsToLNu","W3JetsToLNu","W4JetsToLNu","DY1JetsToLL_M50","DY2JetsToLL_M50", "DY3JetsToLL_M50", "DY4JetsToLL_M50", "DYJetsToLL_M4to50_HT70to100","DYJetsToLL_M4to50_HT100to200", "DYJetsToLL_M4to50_HT200to400", "DYJetsToLL_M4to50_HT400to600", "DYJetsToLL_M4to50_HT600toInf"
]
samples94XPrompt = [
"TTHnobb","TTZToLLNuNu_M10","TTZToLL_M1to10","TT_PSwgt_To2L2Nu","TT_PSwgt_ToSemiLep","TT_PSwgt_ToHadron",
"TTWToLNu","TTWW","W1JetsToLNu","W2JetsToLNu","W3JetsToLNu","W4JetsToLNu","WZTo3LNu","ZZ_ext_To4L",
"THQ","THW","DY_M10to50","DY_ext_M50","WW_DoubleScatter","WWW","WWZ","WZZ","ZZZ","TTTT_Tune","tWll","tZq","WpWpJJ","TTTW","TTWH","GGH_ext_ToZZ4L","VHToNobb"
]
samplesIgnored=[
"TT_PSwgt_To2L2Nu","TT_PSwgt_ToSemiLep","TT_PSwgt_ToHadron",
"TTWW","W1JetsToLNu","W2JetsToLNu","W3JetsToLNu","W4JetsToLNu","WZTo3LNu","ZZ_ext_To4L",
"TTGJets","TGJets_Lep","W1JetsToLNu","W2JetsToLNu","W3JetsToLNu","W4JetsToLNu","DY1JetsToLL_M50","DY2JetsToLL_M50", "DY3JetsToLL_M50", "DY4JetsToLL_M50", "DYJetsToLL_M4to50_HT70to100","DYJetsToLL_M4to50_HT100to200", "DYJetsToLL_M4to50_HT200to400", "DYJetsToLL_M4to50_HT400to600", "DYJetsToLL_M4to50_HT600toInf",
"THQ","THW","DY_M10to50","DY_ext_M50","WW_DoubleScatter","WWW","WWZ","WZZ","ZZZ","TTTT_Tune","tWll","tZq","WpWpJJ","TTTW","TTWH","GGH_ext_ToZZ4L","VHToNobb",
"WJets","WZG"
]

samples = samplesIgnored 

#####
##   The script itsself
#####
allSubmit = 0
allMerge = 0
allMergeJobFile = 0
if os.path.exists(os.getcwd()+"/all.sh"):
    allSubmit = open(os.getcwd()+"/all.sh","a")
    allMerge = open(os.getcwd()+"/allmerge.sh","a")
    allMergeJobFile = open(os.getcwd()+"/allmergejob.sh","a")
else:
    allSubmit = open(os.getcwd()+"/all.sh","w")
    allMerge = open(os.getcwd()+"/allmerge.sh","w")
    allMergeJobFile = open(os.getcwd()+"/allmergejob.sh","w")
    allSubmit.write("#!/bin/bash\n")
    allMerge.write("#!/bin/bash\n")
    allMergeJobFile.write("#!/bin/bash\n")

def prepareSubmitJob(submitFileName,cshFileName, outPutFileName, errorFileName):
    cshFile      = file(submitFileName,"w")
    print >> cshFile, "Universe     = vanilla"
    print >> cshFile, "getenv       = true"
    print >> cshFile, "Executable   = ",cshFileName
    print >> cshFile, "Output       = ",outPutFileName
    print >> cshFile, "Error        = ",errorFileName
    print >> cshFile, "Queue"

def prepareMergeJob(shFile,inputFile):
        subFile      = file(shFile,"w")
        print >> subFile, "#!/bin/bash"
        print >> subFile, "/bin/hostname"
        print >> subFile, "source /afs/ihep.ac.cn/soft/CMS/64bit/root/profile/rootenv-entry 6.08.02"
        print >> subFile, "gcc -v"
        print >> subFile, "pwd"
        print >> subFile, "cd "+outputBaseDir
        print >> subFile, "bash "+inputFile
        subprocess.call("chmod 777 "+shFile, shell=True)

def prepareCshJob(sample,shFile,inputDir,outputDir, sampleName, regiondir):
        subFile      = file(shFile,"w")
        print >> subFile, "#!/bin/bash"
        print >> subFile, "/bin/hostname"
        print >> subFile, "source /cvmfs/sft.cern.ch/lcg/views/LCG_93/x86_64-slc6-gcc62-opt/setup.sh"
        print >> subFile, "gcc -v"
        print >> subFile, "pwd"
        print >> subFile, "cd "+frameworkDir
        process = sampleName
        if "TrainMVA" not in regiondir:
            if process in samples94XData:
                for region in Regions:
                    print >> subFile, "root -b -q -l "+executable_Data_2lss+"'(\""+inputDir+'","'+outputDir+'","'+sample+'","'+region+'"'+")'"
                    print >> subFile, "root -b -q -l "+executable_Fake_2lss+"'(\""+inputDir+'","'+outputDir+'","'+sample+'","'+region+'"'+")'"
                    print >> subFile, "root -b -q -l "+executable_Flip_2lss+"'(\""+inputDir+'","'+outputDir+'","'+sample+'","'+region+'"'+")'"
            elif process in samples94XConv and process in samples94XPrompt:
                for region in Regions:
                    print >> subFile, "root -b -q -l "+executable_Prompt_2lss+"'(\""+inputDir+'","'+outputDir+'","'+sample+'","'+region+'"'+")'"
                    print >> subFile, "root -b -q -l "+executable_Conv_2lss+"'(\""+inputDir+'","'+outputDir+'","'+sample+'","'+region+'"'+")'"
                    if usePromptFake:
                        print >> subFile, "root -b -q -l "+executable_Prompt_fake+"'(\""+inputDir+'","'+outputDir+'","'+sample+'","'+region+'"'+")'"
            elif process in samples94XPrompt:
                for region in Regions:
                    print >> subFile, "root -b -q -l "+executable_Prompt_2lss+"'(\""+inputDir+'","'+outputDir+'","'+sample+'","'+region+'"'+")'"
                    if usePromptFake:
                        print >> subFile, "root -b -q -l "+executable_Prompt_fake+"'(\""+inputDir+'","'+outputDir+'","'+sample+'","'+region+'"'+")'"
            elif process in samples94XConv:
                for region in Regions:
                    print >> subFile, "root -b -q -l "+executable_Conv_2lss+"'(\""+inputDir+'","'+outputDir+'","'+sample+'","'+region+'"'+")'"
            else:
                print ("ERROR: not TrainMVA, '"+process+"' process not found in samples94XData, samples94XConv, samples94XPrompt")
        else:
            for region in Regions:
                print >> subFile, "root -b -q -l "+executable_TrainMVA_2lss+"'(\""+inputDir+'","'+outputDir+'","'+sample+'","'+region+'"'+")'"
        subprocess.call("chmod 777 "+shFile, shell=True)

#for iroot in range(nroot):
#for region in Regions:
for regiondir in  DirOfRegions:
    allSubmit.write("bash "+analysis+regiondir+"Submit.sh\n")
    allMerge.write("bash "+analysis+regiondir+"merge.sh\n")

    allJobFileName = analysis+ regiondir +"Submit.sh"
    allJobFile      = file(allJobFileName,"w")
    print >> allJobFile, "#!/bin/bash"

    MergeFiles ={}
    for region in Regions:
        MergeFileName = analysis+regiondir+region+"merge.sh"
        MergeFile = file(MergeFileName,"w")
        MergeFiles[MergeFileName]      = MergeFile
#    for regiondir in  DirOfRegions[region]:
    if 1 > 0: # FIXME dummy if
        #dirsToCheck = [f for f in os.listdir(inputBaseDir+regiondir) if os.path.isdir(f)]
        dirsToCheck = [f for f in os.listdir(inputBaseDir+regiondir)]
        samples = dirsToCheck
        print ("regiondirs : "+regiondir + " samples : "+str(samples))    
        for sample in samples:
            if sample in samplesIgnored:
                print ( "sample " + sample + " is skipped" )
                continue
            print sample
            sampleName = sample
    
            #First, let's get rid of any 
    
            os.popen('mkdir -p '+ outputBaseDir + "/" + analysis  + regiondir + "/" + sampleName )
            os.popen('mkdir -p '+ outputBaseDir + "/" + analysis  + regiondir + "/" + sampleName + "/" + "scripts")
            os.popen('mkdir -p '+ outputBaseDir + "/" + analysis  + regiondir + "/" + sampleName + "/" + "logs")
            os.popen('mkdir -p '+ outputBaseDir + "/" + analysis  + regiondir + "/" + sampleName + "/" + "skims")

            inputFiles  = [f for f in os.listdir(inputBaseDir+regiondir+"/"+sample+"/skims/") if sampleName in f]
            for inputfile in inputFiles:
                fileName = inputfile[:-9]
                shFileName = outputBaseDir + "/" + analysis + regiondir + "/" + sampleName + "/scripts/" + fileName + ".sh"
                logFileName = outputBaseDir + "/" + analysis + regiondir + "/" + sampleName + "/logs/" + fileName + ".log"
                errorFileName = outputBaseDir + "/" + analysis + regiondir + "/" + sampleName + "/logs/" + fileName + ".error"
                
                inputDir = inputBaseDir + regiondir + "/" + sample + "/skims/" 
                outputDir = outputBaseDir + "/" + analysis + regiondir + "/" +sampleName + "/skims/"
                #print (shFileName)
                prepareCshJob(fileName,shFileName,inputDir,outputDir, sampleName, regiondir)
                print >> allJobFile, "hep_sub "+ shFileName + " -o "+logFileName+ " -e "+errorFileName

            # write merge files
            if "TrainMVA" not in regiondir:
                if sampleName in samples94XData:
                    for region in Regions:
                        MergeFileName = analysis+regiondir+region+"merge.sh"
                        MergeFile = MergeFiles[MergeFileName]
                        print >> MergeFile, "hadd -f "+outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/merged"+sampleName+"_Data_"+region+".root  "+ outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/"+sampleName+"*_Data2lss_"+region+".root"
                        print >> MergeFile, "hadd -f "+outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/merged"+sampleName+"_Fake_"+region+".root  "+ outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/"+sampleName+"*_Fake2lss_"+region+".root"
                        print >> MergeFile, "hadd -f "+outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/merged"+sampleName+"_Flip_"+region+".root  "+ outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/"+sampleName+"*_Flip2lss_"+region+".root"
                elif sampleName in samples94XConv and sampleName in samples94XPrompt:
                    for region in Regions:
                        MergeFileName = analysis+regiondir+region+"merge.sh"
                        MergeFile = MergeFiles[MergeFileName]
                        print >> MergeFile, "hadd -f "+outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/merged"+sampleName+"_Prompt2lss_"+region+".root  "+ outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/"+sampleName+"*_Prompt2lss_"+region+".root"
                        print >> MergeFile, "hadd -f "+outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/merged"+sampleName+"_Conv2lss_"+region+".root  "+ outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/"+sampleName+"*_Conv2lss_"+region+".root"
                        if usePromptFake:
                            print >> MergeFile, "hadd -f "+outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/merged"+sampleName+"_Promptfake_"+region+".root  "+ outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/"+sampleName+"*_Promptfake_"+region+".root"
                elif sampleName in samples94XPrompt:
                    for region in Regions:
                        MergeFileName = analysis+regiondir+region+"merge.sh"
                        MergeFile = MergeFiles[MergeFileName]
                        print >> MergeFile, "hadd -f "+outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/merged"+sampleName+"_Prompt2lss_"+region+".root  "+ outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/"+sampleName+"*_Prompt2lss_"+region+".root"
                        if usePromptFake:
                            print >> MergeFile, "hadd -f "+outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/merged"+sampleName+"_Promptfake_"+region+".root  "+ outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/"+sampleName+"*_Promptfake_"+region+".root"
                elif sampleName in samples94XConv:
                    for region in Regions:
                        MergeFileName = analysis+regiondir+region+"merge.sh"
                        MergeFile = MergeFiles[MergeFileName]
                        print >> MergeFile, "hadd -f "+outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/merged"+sampleName+"_Conv2lss_"+region+".root  "+ outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/"+sampleName+"*_Conv2lss_"+region+".root"
                else:
                    print ("ERROR not TrainMVA, '"+sampleName+"' sampleName not found in samples94XData, samples94XConv, samples94XPrompt")
            else:
                for region in Regions:
                    MergeFileName = analysis+regiondir+region+"merge.sh"
                    MergeFile = MergeFiles[MergeFileName]
                    print >> MergeFile, "hadd -f "+outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/merged"+sampleName+"_TrainMVA_"+region+".root  "+ outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/"+sampleName+"*_TrainMVA_"+region+".root"
    for region in Regions:
        MergeFileName = analysis+regiondir+region+"merge.sh"
        MergeFile = MergeFiles[MergeFileName]
        shFileName = outputBaseDir + "/" + analysis + regiondir + region + "mergeJob.sh"
        logFileName = outputBaseDir + "/" + analysis + regiondir + region + "mergejob.log"
        errorFileName = outputBaseDir + "/" + analysis + regiondir + region + "mergejob.error"
        prepareMergeJob(shFileName,MergeFileName)
        print >> allMergeJobFile, "hep_sub "+ shFileName + " -o "+logFileName+ " -e "+errorFileName

allSubmit.close()
allMerge.close()
allMergeJobFile.close()
print "Finished " + analysis + region
