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
Regions=["DiLepRegion"]#"TriLepRegion","QuaLepRegion","ttZctrl","WZctrl","QuaLepRegion","ZZctrl"]

Selections=["datafakes", "dataflips", "prompt", "mcfakes", "mcflips", "fakesub", "dataobs", "conv"]

DirOfRegions = [
"ttH2016Data2L","ttH2016All2L","ttH2017Data2L","ttH2017All2L","ttH2018Data2L","ttH2018All2L",
#"ttH2016Data3L","ttH2016All3L","ttH2017Data3L","ttH2017All3L","ttH2018Data3L","ttH2018All3L",
#"ttH2016Data4L","ttH2016All4L","ttH2017Data4L","ttH2017All4L","ttH2018Data4L","ttH2018All4L"
]

analysis = ""
taskname = "EvtSel"
frameworkDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/LegacyV1/"
inputBaseDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/skims_LegacyAll_20191110/"
outputBaseDir =  "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplas_LegacyAll_20191110_v3/"

executable = "Rootplas_LegacyAll.C"

selectedSamples = []

samplesConv = [
# 2016
'Legacy16V1_TTGJets_v1', 'Legacy16V1_TTGJets_ext', 'Legacy16V1_TGJetsLep', 'Legacy16V1_WGToLNuG_ext1', 'Legacy16V1_WGToLNuG_ext2', 'Legacy16V1_WGToLNuG_ext3', 'Legacy16V1_ZGToLLG', 'Legacy16V1_DYJets_M10to50', 'Legacy16V1_DYJets_M50', 'Legacy16V1_WZG','Legacy16V1_WJets_v1','Legacy16V1_WJets_ext',
# 2017
'Legacy17V1_TTGJets_v1', 'Legacy17V1_TTGJets_ext', 'Legacy17V1_TGJetsLep', 'Legacy17V1_WGToLNuG_Tune', 'Legacy17V1_ZGToLLG_01J', 'Legacy17V1_W1JetsToLNu', 'Legacy17V1_W2JetsToLNu', 'Legacy17V1_W3JetsToLNu', 'Legacy17V1_W4JetsToLNu', 'Legacy17V1_DYJets_M10to50_v1', 'Legacy17V1_DYJets_M10to50_ext', 'Legacy17V1_DYJets_M50_v1', 'Legacy17V1_DYJets_M50_ext', 'Legacy17V1_WZG',
# 2018
'Legacy18V1_TTGJets', 'Legacy18V1_TGJetsLep', 'Legacy18V1_WGToLNuG_Tune', 'Legacy18V1_ZGToLLG_01J', 'Legacy18V1_W1JetsToLNu', 'Legacy18V1_W2JetsToLNu', 'Legacy18V1_W3JetsToLNu', 'Legacy18V1_W4JetsToLNu', 'Legacy18V1_DYJets_M10to50', 'Legacy18V1_DYJets_M50_v1','Legacy18V1_DYJets_M50_ext','Legacy18V1_WZG',
]


samplesIgnored=[
"TT_PSwgt_To2L2Nu","TT_PSwgt_ToSemiLep","TT_PSwgt_ToHadron",
]

samples = samplesIgnored 

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
subprocess.call("chmod 777 allskim.sh", shell=True)

allSkim.close()

def prepareCshJob(sample,shFile,inputDir,outputDir, sampleName, regiondir):
        subFile      = file(shFile,"w")




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
        print >> subFile, "source /publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/LegacyV1/setup.sh" 
        print >> subFile, "gcc -v"
        print >> subFile, "pwd"
        print >> subFile, "cd "+frameworkDir
        process = sampleName
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
                print >> subFile, "root -b -q -l "+executable+"'(\""+inputDir+'","'+outputDir+'","'+sample+'","'+selection+'","'+region+'"'+")'"
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
