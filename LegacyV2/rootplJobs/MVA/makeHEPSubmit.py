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
Regions=["DiLepRegion"]

#DirOfRegions = ["ttH2016TrainDNN2L","ttH2017TrainDNN2L","ttH2018TrainDNN2L"]
#DirOfRegions = ["ttH2017TrainDNN2L","ttH2018TrainDNN2L"]
DirOfRegions = ["ttH2017TrainDNN2L"]

analysis = ""
taskname = "EvtSel"
frameworkDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/LegacyV2/"
inputBaseDir =  "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/skims_LegacyMVA_20191204/"
outputBaseDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplas_LegacyMVA_20191204/"

usePromptFake = False

executable_TrainMVA_2lss = "Rootplas_TrainMVA.C"

selectedSamples = []

samplesIgnored=[
"Legacy17V2_TTHnobb_ext","Legacy17V2_TTTo2L","Legacy17V2_TTTo2L_PS","Legacy17V2_TTToSemiLep","Legacy17V2_TTToSemiLep_PS","Legacy17V2_TTToHad","Legacy17V2_TTToHad_PS","Legacy17V2_ttZ_v1","Legacy17V2_ttZ_ext","Legacy17V2_ttW_v1","Legacy17V2_ttW_ext",
]

samples = []

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

def prepareCshJob(sample,shFile,inputDir,outputDir, sampleName):
        subFile      = file(shFile,"w")
        print >> subFile, "#!/bin/bash"
        print >> subFile, "/bin/hostname"
        print >> subFile, "source /publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/LegacyV1/setup.sh" 
        print >> subFile, "gcc -v"
        print >> subFile, "pwd"
        print >> subFile, "cd "+frameworkDir
        process = sampleName
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
                prepareCshJob(fileName,shFileName,inputDir,outputDir, sampleName)
                print >> allJobFile, "hep_sub "+ shFileName + " -o "+logFileName+ " -e "+errorFileName

            # write merge files
            for region in Regions:
                MergeFileName = analysis+regiondir+region+"merge.sh"
                MergeFile = MergeFiles[MergeFileName]
                print >> MergeFile, "hadd -f "+outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/merged"+sampleName+"_"+region+".root  "+ outputBaseDir + "/" + analysis + regiondir + "/"+ sampleName + "/skims/"+sampleName+"*_"+region+".root"
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
