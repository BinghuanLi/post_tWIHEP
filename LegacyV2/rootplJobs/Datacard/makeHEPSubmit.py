import sys
import os
import glob
import string
import subprocess
from string import digits
#####
##   Parameters to be specified by the user
#####
variations = ["JESUp","JESDown","JERUp","JERDown","MetShiftUp","MetShiftDown"]
# JEC sources
Jecsources={
"2016":["FlavorQCD","RelativeBal","HF","BBEC1","EC2","Absolute","BBEC1_2016","EC2_2016","Absolute_2016","HF_2016","RelativeSample_2016"],
"2017":["FlavorQCD","RelativeBal","HF","BBEC1","EC2","Absolute","BBEC1_2017","EC2_2017","Absolute_2017","HF_2017","RelativeSample_2017"],
"2018":["FlavorQCD","RelativeBal","HF","BBEC1","EC2","Absolute","BBEC1_2018","EC2_2018","Absolute_2018","HF_2018","RelativeSample_2018"],
#"2016":["RelativeBal","HF","BBEC1","EC2","Absolute","BBEC1_2016","EC2_2016","Absolute_2016","HF_2016"],
#"2017":["RelativeBal","HF","BBEC1","EC2","Absolute","BBEC1_2017","EC2_2017","Absolute_2017","HF_2017"],
#"2018":["RelativeBal","HF","BBEC1","EC2","Absolute","BBEC1_2018","EC2_2018","Absolute_2018","HF_2018"],
#"2016":["FlavorQCD","RelativeSample_2016"],
#"2017":["FlavorQCD","RelativeSample_2017"],
#"2018":["FlavorQCD","RelativeSample_2018"],
}

#analysis and task
Regions=["DiLepRegion"]#"TriLepRegion","QuaLepRegion","ttZctrl","WZctrl","QuaLepRegion","ZZctrl"]

#Selections=["datafakes", "dataflips", "prompt", "mcfakes", "mcflips", "fakesub", "dataobs", "conv"]
Selections=["datafakes", "dataflips", "prompt", "fakesub", "dataobs", "conv"]
#Selections=["conv"]

DirOfRegions = [
# 2L nominal
"ttH2016Data2L", "ttH2016All2L", "ttH2017Data2L", "ttH2017All2L", "ttH2018Data2L", "ttH2018All2L",
# 2L systematics
"ttH2016SR2LMetShiftUp","ttH2016SR2LMetShiftDown","ttH2016SR2LJERUp","ttH2016SR2LJERDown",
"ttH2016SR2LJESUp_FlavorQCD","ttH2016SR2LJESDown_FlavorQCD", "ttH2016SR2LJESUp_RelativeBal","ttH2016SR2LJESDown_RelativeBal", "ttH2016SR2LJESUp_HF","ttH2016SR2LJESDown_HF", "ttH2016SR2LJESUp_BBEC1","ttH2016SR2LJESDown_BBEC1", "ttH2016SR2LJESUp_EC2","ttH2016SR2LJESDown_EC2", "ttH2016SR2LJESUp_Absolute","ttH2016SR2LJESDown_Absolute",
"ttH2016SR2LJESUp_RelativeSample_2016","ttH2016SR2LJESDown_RelativeSample_2016", "ttH2016SR2LJESUp_BBEC1_2016","ttH2016SR2LJESDown_BBEC1_2016", "ttH2016SR2LJESUp_EC2_2016","ttH2016SR2LJESDown_EC2_2016", "ttH2016SR2LJESUp_Absolute_2016","ttH2016SR2LJESDown_Absolute_2016", "ttH2016SR2LJESUp_HF_2016","ttH2016SR2LJESDown_HF_2016", 
"ttH2017SR2LMetShiftUp","ttH2017SR2LMetShiftDown","ttH2017SR2LJERUp","ttH2017SR2LJERDown",
"ttH2017SR2LJESUp_FlavorQCD","ttH2017SR2LJESDown_FlavorQCD", "ttH2017SR2LJESUp_RelativeBal","ttH2017SR2LJESDown_RelativeBal", "ttH2017SR2LJESUp_HF","ttH2017SR2LJESDown_HF", "ttH2017SR2LJESUp_BBEC1","ttH2017SR2LJESDown_BBEC1", "ttH2017SR2LJESUp_EC2","ttH2017SR2LJESDown_EC2", "ttH2017SR2LJESUp_Absolute","ttH2017SR2LJESDown_Absolute",
"ttH2017SR2LJESUp_RelativeSample_2017","ttH2017SR2LJESDown_RelativeSample_2017", "ttH2017SR2LJESUp_BBEC1_2017","ttH2017SR2LJESDown_BBEC1_2017", "ttH2017SR2LJESUp_EC2_2017","ttH2017SR2LJESDown_EC2_2017", "ttH2017SR2LJESUp_Absolute_2017","ttH2017SR2LJESDown_Absolute_2017", "ttH2017SR2LJESUp_HF_2017","ttH2017SR2LJESDown_HF_2017",
"ttH2018SR2LMetShiftUp","ttH2018SR2LMetShiftDown","ttH2018SR2LJERUp","ttH2018SR2LJERDown",
"ttH2018SR2LJESUp_FlavorQCD","ttH2018SR2LJESDown_FlavorQCD", "ttH2018SR2LJESUp_RelativeBal","ttH2018SR2LJESDown_RelativeBal", "ttH2018SR2LJESUp_HF","ttH2018SR2LJESDown_HF", "ttH2018SR2LJESUp_BBEC1","ttH2018SR2LJESDown_BBEC1", "ttH2018SR2LJESUp_EC2","ttH2018SR2LJESDown_EC2", "ttH2018SR2LJESUp_Absolute","ttH2018SR2LJESDown_Absolute",
"ttH2018SR2LJESUp_RelativeSample_2018","ttH2018SR2LJESDown_RelativeSample_2018", "ttH2018SR2LJESUp_BBEC1_2018","ttH2018SR2LJESDown_BBEC1_2018", "ttH2018SR2LJESUp_EC2_2018","ttH2018SR2LJESDown_EC2_2018", "ttH2018SR2LJESUp_Absolute_2018","ttH2018SR2LJESDown_Absolute_2018", "ttH2018SR2LJESUp_HF_2018","ttH2018SR2LJESDown_HF_2018",
#"ttH2016Data3L","ttH2016All3L","ttH2017Data3L","ttH2017All3L","ttH2018Data3L","ttH2018All3L",
#"ttH2016Data4L","ttH2016All4L","ttH2017Data4L","ttH2017All4L","ttH2018Data4L","ttH2018All4L"
]

analysis = ""
taskname = "EvtSel"
frameworkDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/LegacyV2/"
inputBaseDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/skims_LegacyAll_20200111/"
outputBaseDir =  "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplas_LegacyAll_SVATrig_20200122/"

executable = "Rootplas_LegacyAll.C"

selectedSamples = []

samplesConv = [
# 2016
'Legacy16V2_TTGJets_v1', 'Legacy16V2_TTGJets_ext', 'Legacy16V2_TGJetsLep', 'Legacy16V2_WZG','Legacy16V2_ZGToLLG','Legacy16V2_WGToLNuG_01J', 
#'Legacy16V2_WGToLNuG_ext1', 'Legacy16V2_WGToLNuG_ext2', 'Legacy16V2_WGToLNuG_ext3', 'Legacy16V2_DYJets_M10to50', 'Legacy16V2_DYJets_M50', 
#"Legacy16V2_W1JetsToLNu", "Legacy16V2_W2JetsToLNu_v1", "Legacy16V2_W2JetsToLNu_ext", "Legacy16V2_W3JetsToLNu_v1", "Legacy16V2_W3JetsToLNu_ext", "Legacy16V2_W4JetsToLNu_v1","Legacy16V2_W4JetsToLNu_ext", 
# 2017
"Legacy17V2_TTGJets_v1","Legacy17V2_TTGJets_ext","Legacy17V2_TGJetsLep","Legacy17V2_WZG", "Legacy17V2_ZGToLLG_01J","Legacy17V2_WGToLNuG_01J",
#"Legacy17V2_WGToLNuG_Tune", "Legacy17V2_W1JetsToLNu","Legacy17V2_W2JetsToLNu","Legacy17V2_W3JetsToLNu","Legacy17V2_W4JetsToLNu","Legacy17V2_DYJets_M10to50_v1","Legacy17V2_DYJets_M10to50_ext","Legacy17V2_DYJets_M50_v1","Legacy17V2_DYJets_M50_ext",
# 2018
"Legacy18V2_TTGJets","Legacy18V2_TGJetsLep", "Legacy18V2_ZGToLLG_01J", "Legacy18V2_WZG", "Legacy18V2_WGToLNuG_01J",
#"Legacy18V2_WGToLNuG_Tune",
#"Legacy18V2_W1JetsToLNu","Legacy18V2_W2JetsToLNu","Legacy18V2_W3JetsToLNu","Legacy18V2_W4JetsToLNu","Legacy18V2_DYJets_M10to50","Legacy18V2_DYJets_M50_v1","Legacy18V2_DYJets_M50_ext",
]


samplesIgnored=[
'Legacy16V2_WGToLNuG_ext1', 'Legacy16V2_WGToLNuG_ext2', 'Legacy16V2_WGToLNuG_ext3', 'Legacy16V2_DYJets_M10to50', 'Legacy16V2_DYJets_M50', 
"Legacy16V2_W1JetsToLNu", "Legacy16V2_W2JetsToLNu_v1", "Legacy16V2_W2JetsToLNu_ext", "Legacy16V2_W3JetsToLNu_v1", "Legacy16V2_W3JetsToLNu_ext", "Legacy16V2_W4JetsToLNu_v1","Legacy16V2_W4JetsToLNu_ext", 
"Legacy17V2_WGToLNuG_Tune", "Legacy17V2_W1JetsToLNu","Legacy17V2_W2JetsToLNu","Legacy17V2_W3JetsToLNu","Legacy17V2_W4JetsToLNu","Legacy17V2_DYJets_M10to50_v1","Legacy17V2_DYJets_M10to50_ext","Legacy17V2_DYJets_M50_v1","Legacy17V2_DYJets_M50_ext",
"Legacy18V2_WGToLNuG_Tune",
"Legacy18V2_W1JetsToLNu","Legacy18V2_W2JetsToLNu","Legacy18V2_W3JetsToLNu","Legacy18V2_W4JetsToLNu","Legacy18V2_DYJets_M10to50","Legacy18V2_DYJets_M50_v1","Legacy18V2_DYJets_M50_ext",
]

#samples = samplesIgnored 
samples = []

#####
##   The script itsself
#####
allSubmit = 0
allMerge = 0
allMergeJobFile = 0
allSkim = 0

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

allSkim = open(os.getcwd()+"/allskim.sh","w")
print >> allSkim, "/bin/hostname"
print >> allSkim, "source /afs/ihep.ac.cn/soft/CMS/64bit/root/profile/rootenv-entry 6.08.02"
print >> allSkim, "gcc -v"
print >> allSkim, "pwd"
print >> allSkim, "cd "+outputBaseDir
print >> allSkim, "python skimLegacyAll.py"
print >> allSkim, "python varMerge.py"
subprocess.call("chmod 777 allskim.sh", shell=True)

allSkim.close()


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

def prepareCshJob(samples,shFile,inputDir,outputDir, sampleName, regiondir):
        subFile      = file(shFile,"w")
        print >> subFile, "#!/bin/bash"
        print >> subFile, "/bin/hostname"
        print >> subFile, "source /publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/LegacyV2/setup.sh" 
        print >> subFile, "gcc -v"
        print >> subFile, "pwd"
        print >> subFile, "cd "+frameworkDir
        process = sampleName
        isVars = False
        varName = ""
        for var in variations:
            if var in regiondir:
                isVars = True
                varName = regiondir.split("SR2L")[1]
                break
        for sample in samples:
            era = 0
            if "Legacy16" in sample:
                era = 2016
            if "Legacy17" in sample:
                era = 2017
            if "Legacy18" in sample:
                era = 2018
            for region in Regions:
                if "DiLepRegion" in region and "2L" not in regiondir:
                    #print ("skip DiLepRegion") 
                    continue
                if ("TriLepRegion" in region or "WZctrl" in region or "ttZctrl" in region) and "3L" not in regiondir:
                    #print ("skip TriLepRegion WZctrl ttZctrl") 
                    continue
                if ("QuaLepRegion" in region or "ZZctrl" in region) and "4L" not in regiondir:
                    #print ("skip QuaLepRegion ZZctrl") 
                    continue
                for selection in Selections:
                    if isVars and selection not in ["conv","prompt"]:
                        #print ("skip for MC vars excpet conv and prompt ")
                        continue
                    if "Block" not in process and "data"in selection:
                        #print ("skip datas for MC ")
                        continue
                    if "Block" in process and not "data"in selection:
                        #print ("skip mcMatch for data ")
                        continue
                    if "2L" not in regiondir and "flips"in selection:
                        #print ("skip flips") 
                        continue
                    if selection == "conv" and process not in samplesConv:
                        #print ("skip conv") 
                        continue
                    print >> subFile, "root -b -q -l "+executable+"'(\""+inputDir+'","'+outputDir+'","'+sample[:-9]+'","'+selection+'","'+region+'","'+varName+'",'+str(era)+")'"
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
            if len(selectedSamples) >0 and sample not in selectedSamples:
                continue
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
            
            shFileName = outputBaseDir + "/" + analysis + regiondir + "/" + sampleName + "/scripts/" + sample + ".sh"
            logFileName = outputBaseDir + "/" + analysis + regiondir + "/" + sampleName + "/logs/" + sample + ".log"
            errorFileName = outputBaseDir + "/" + analysis + regiondir + "/" + sampleName + "/logs/" + sample + ".error"
                
            inputDir = inputBaseDir + regiondir + "/" + sample + "/skims/" 
            outputDir = outputBaseDir + "/" + analysis + regiondir + "/" +sampleName + "/skims/"
            #print (shFileName)
            prepareCshJob(inputFiles,shFileName,inputDir,outputDir, sampleName, regiondir)
            print >> allJobFile, "hep_sub "+ shFileName + " -o "+logFileName+ " -e "+errorFileName

            # write merge files
            for region in Regions:
                MergeFileName = analysis+regiondir+region+"merge.sh"
                MergeFile = MergeFiles[MergeFileName]
                if "DiLepRegion" in region and "2L" not in regiondir:
                    continue
                if ("TriLepRegion" in region or "WZctrl" in region or "ttZctrl" in region) and "3L" not in regiondir:
                    continue
                if ("QuaLepRegion" in region or "ZZctrl" in region ) and "4L" not in regiondir:
                    continue
                for selection in Selections:
                    if "Block" not in sampleName and "data"in selection:
                        continue
                    if "Block" in sampleName and not "data"in selection:
                        #print ("skip mcMatch for data ")
                        continue
                    if "2L" not in regiondir and "flips"in selection:
                        continue
                    if selection == "conv" and sampleName not in samplesConv:
                        continue
                    print >> MergeFile, "hadd -f "+outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/merged"+sampleName+"_"+selection+"_"+region+".root  "+ outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/"+sampleName+"*_"+selection+"_"+region+".root"
    
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
