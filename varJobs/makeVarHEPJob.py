import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread

#####
##   Parameters to be specified by the user
#####
# rootplas are saved as inputBaseDir/regionName/(JESUp/Down)regionName/process_(JESUp/Down)regionName.root
# please move rootplas from inputBaseDir/regionName/(JESUp/Down)regionName to inputBaseDir/(JESUp/Down)regionName

cwd = os.getcwd()

frameworkDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/varJobs/"
inputBaseDir = cwd 
outputBaseDir = cwd 

dirsIgnored =  ["ttZctrl"]

#dirsToCheck = ["SigRegion","JESUpSigRegion","JESDownSigRegion","ttWctrl","JESUpttWctrl","JESDownttWctrl"]
dirsToCheck = ["SigRegion","JESUpSigRegion","JESDownSigRegion"]

ignorefiles = ["TTH","H"]

ListOfCats={
    "SubCat2l":{1:"ee_neg",2:"ee_pos",3:"em_bl_neg",4:"em_bl_pos",5:"em_bt_neg",6:"em_bt_pos",7:"mm_bl_neg",8:"mm_bl_pos",9:"mm_bt_neg",10:"mm_bt_pos"},
    "DNNCat":{1:"ttHnode",2:"ttJnode",3:"ttWnode",4:"ttZnode"},
    "DNNCat_option2":{1:"ttHnode",2:"ttJnode",3:"ttWnode",4:"ttZnode"},
    "DNNCat_option3":{1:"ttHnode",2:"ttJnode",3:"ttWnode",4:"ttZnode"},
    }


executable =  "runReadingNoMVA.C"

def prepareCshJob(shFile,channel):
    subFile      = file(shFile,"w")
    print >> subFile, "#!/bin/bash"
    print >> subFile, "/bin/hostname"
    print >> subFile, "source /cvmfs/sft.cern.ch/lcg/views/LCG_93/x86_64-slc6-gcc62-opt/setup.sh"
    print >> subFile, "gcc -v"
    print >> subFile, "pwd"
    # i+1 stands for channel, i==SubCat2l, in ttH 2lss
    for dirToCheck in dirsToCheck:
        if dirToCheck in dirsIgnored: continue
        if not os.path.exists("Output/"+key+"/"+value[channel]+"/"+dirToCheck):
            os.popen("mkdir -p Output/"+key+"/"+value[channel]+"/"+dirToCheck)
        inputfiles = [f for f in os.listdir("./"+dirToCheck) if "root" in f]
        for inputfile in inputfiles:
            process = inputfile.split(("_"+dirToCheck))[0]
            if process in ignorefiles: continue
            if process == "data" or process =="Fakes" or process== "Flips":
                command_run = "root -l -b -q "+frameworkDir+executable+"'"+'("'+process+'","'+dirToCheck+'","Output/'+key+"/"+value[channel]+"/"+dirToCheck+'",true,'+str(channel)+',"'+key+'"'+")'"
                print >> subFile, command_run 
            else:
                command_run = "root -l -b -q "+frameworkDir+executable+"'"+'("'+process+'","'+dirToCheck+'","Output/'+key+"/"+value[channel]+"/"+dirToCheck+'",false,'+str(channel)+',"'+key+'"'+")'"
                print >> subFile, command_run 
    subprocess.call("chmod 777 "+shFile, shell=True)


if not os.path.exists("Output"):
        os.popen("mkdir Output")

allJobFile = 0
if os.path.exists(os.getcwd()+"/all.sh"):
    allJobFile = open(os.getcwd()+"/all.sh","a")
else:
    allJobFile = open(os.getcwd()+"/all.sh","w")
    allJobFile.write("#!/bin/bash\n")

for key,value in ListOfCats.iteritems():
  n_values = len(value)
  print ("SubCat is " + key + " with subcatgories of " +str(n_values))
  start = 0
  end = n_values
  if not value.has_key(0):
      start = 1
      end = n_values +1
  for i in range(start, end):
    # one job for one channel ~ 20 mins
    if not os.path.exists("Output/"+key+"/"+value[i]):
        os.popen("mkdir -p Output/"+key+"/"+value[i])
    shFileName = outputBaseDir + "/Output/" +key+"/"+value[i] + "/"+value[i]+"Job.sh"
    logFileName = outputBaseDir + "/Output/" +key+"/"+value[i] + "/"+value[i]+"job.log"
    errorFileName = outputBaseDir + "/Output/" +key+"/"+value[i] + "/"+value[i]+"job.error"
    prepareCshJob(shFileName,i)
    print >> allJobFile, "hep_sub "+ shFileName + " -o "+logFileName+ " -e "+errorFileName

allJobFile.close()
print "Finished " 
 
