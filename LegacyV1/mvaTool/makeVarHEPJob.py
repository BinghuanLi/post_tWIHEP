import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread

#####
##   Parameters to be specified by the user
#####
# rootplas are saved as inputBaseDir/regionName/year/(JESUp/Down)regionName/process_(JESUp/Down)regionName.root

cwd = os.getcwd()

frameworkDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/LegacyV1/mvaTool/"
inputBaseDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplas_LegacyAll_20191025/Rootplas/"
outputBaseDir = cwd 

years=["2016","2017","2018"]

dirsIgnored =  ["ttZctrl"]

nPerBins = [5]
ReBin = True
DNNSig = True
BinDir = "BinData_SigDNN"
if not ReBin : BinDir = "BinData_Regular"
elif not DNNSig : BinDir = "BinData_SigTTH"


#Regions = ["SigRegion", "ttWctrl"]
Regions = ["DiLepRegion"]
# key,value to loops
ListOfCats={
    #"SubCat2l":{0:"inclusive",1:"ee_neg",2:"ee_pos",3:"em_bl_neg",4:"em_bl_pos",5:"em_bt_neg",6:"em_bt_pos",7:"mm_bl_neg",8:"mm_bl_pos",9:"mm_bt_neg",10:"mm_bt_pos"},
    "SubCat2l":{1:"ee_neg",2:"ee_pos",3:"em_bl_neg",4:"em_bl_pos",5:"em_bt_neg",6:"em_bt_pos",7:"mm_bl_neg",8:"mm_bl_pos",9:"mm_bt_neg",10:"mm_bt_pos"},
    #"DNNCat":{1:"ttHnode",2:"Restnode",3:"ttWnode",4:"tHQnode"},
    #"DNNCat_option2":{1:"ttHnode",2:"Restnode",3:"ttWnode",4:"tHQnode"},
    #"DNNCat_option3":{1:"ttHnode",2:"Restnode",3:"ttWnode",4:"tHQnode"},
    #"DNNSubCat1_option1":{1:"ee_neg",2:"ee_pos",3:"em_ttHnode",4:"em_Restnode",5:"em_ttWnode",6:"em_tHQnode",7:"mm_ttHnode",8:"mm_Restnode",9:"mm_ttWnode",10:"mm_tHQnode"},
    #"DNNSubCat1_option2":{1:"ee_neg",2:"ee_pos",3:"em_ttHnode",4:"em_Restnode",5:"em_ttWnode",6:"em_tHQnode",7:"mm_ttHnode",8:"mm_Restnode",9:"mm_ttWnode",10:"mm_tHQnode"},
    #"DNNSubCat1_option3":{1:"ee_neg",2:"ee_pos",3:"em_ttHnode",4:"em_Restnode",5:"em_ttWnode",6:"em_tHQnode",7:"mm_ttHnode",8:"mm_Restnode",9:"mm_ttWnode",10:"mm_tHQnode"},
    "DNNSubCat2_option1":{1:"ee_ttHnode",2:"ee_Restnode",3:"ee_ttWnode",4:"ee_tHQnode",5:"em_ttHnode",6:"em_Restnode",7:"em_ttWnode",8:"em_tHQnode",9:"mm_ttHnode",10:"mm_Restnode",11:"mm_ttWnode",12:"mm_tHQnode"},
    #"DNNSubCat2_option2":{1:"ee_ttHnode",2:"ee_Restnode",3:"ee_ttWnode",4:"ee_tHQnode",5:"em_ttHnode",6:"em_Restnode",7:"em_ttWnode",8:"em_tHQnode",9:"mm_ttHnode",10:"mm_Restnode",11:"mm_ttWnode",12:"mm_tHQnode"},
    #"DNNSubCat2_option3":{1:"ee_ttHnode",2:"ee_Restnode",3:"ee_ttWnode",4:"ee_tHQnode",5:"em_ttHnode",6:"em_Restnode",7:"em_ttWnode",8:"em_tHQnode",9:"mm_ttHnode",10:"mm_Restnode",11:"mm_ttWnode",12:"mm_tHQnode"}
    #"DNNAMS2Cat1_option1":{1:"loose_ttHnode",2:"tight_ttHnode",3:"Restnode",4:"ttWnode",5:"tHQnode"},
    #"DNNAMS2Cat1_option2":{1:"loose_ttHnode",2:"tight_ttHnode",3:"Restnode",4:"ttWnode",5:"tHQnode"},
    #"DNNAMS2Cat1_option3":{1:"loose_ttHnode",2:"tight_ttHnode",3:"Restnode",4:"ttWnode",5:"tHQnode"},
    #"DNNAMS3Cat1_option1":{1:"loose_ttHnode",2:"tight_ttHnode",3:"Restnode",4:"ttWnode",5:"tHQnode"},
    #"DNNAMS3Cat1_option2":{1:"loose_ttHnode",2:"tight_ttHnode",3:"Restnode",4:"ttWnode",5:"tHQnode"},
    #"DNNAMS3Cat1_option3":{1:"loose_ttHnode",2:"tight_ttHnode",3:"Restnode",4:"ttWnode",5:"tHQnode"},
    }

dirsToCheck = {
#"SubCat2l":["SigRegion","JESUpSigRegion","JESDownSigRegion","ttWctrl","JESUpttWctrl","JESDownttWctrl"],
"SubCat2l":["DiLepRegion"],
"DNNCat":["DiLepRegion"],
#"DNNCat_option2":["SigRegion","JESUpSigRegion","JESDownSigRegion","ttWctrl","JESUpttWctrl","JESDownttWctrl"],
#"DNNCat_option3":["SigRegion","JESUpSigRegion","JESDownSigRegion","ttWctrl","JESUpttWctrl","JESDownttWctrl"],
"DNNSubCat1_option1":["DiLepRegion"],
#"DNNSubCat1_option2":["SigRegion","JESUpSigRegion","JESDownSigRegion","ttWctrl","JESUpttWctrl","JESDownttWctrl"],
#"DNNSubCat1_option3":["SigRegion","JESUpSigRegion","JESDownSigRegion","ttWctrl","JESUpttWctrl","JESDownttWctrl"],
"DNNSubCat2_option1":["DiLepRegion"],
#"DNNSubCat2_option2":["SigRegion","JESUpSigRegion","JESDownSigRegion","ttWctrl","JESUpttWctrl","JESDownttWctrl"],
#"DNNSubCat2_option3":["SigRegion","JESUpSigRegion","JESDownSigRegion","ttWctrl","JESUpttWctrl","JESDownttWctrl"],
#"DNNAMS2Cat1_option1":["SigRegion","JESUpSigRegion","JESDownSigRegion","ttWctrl","JESUpttWctrl","JESDownttWctrl"],
#"DNNAMS2Cat1_option2":["SigRegion","JESUpSigRegion","JESDownSigRegion","ttWctrl","JESUpttWctrl","JESDownttWctrl"],
#"DNNAMS2Cat1_option3":["SigRegion","JESUpSigRegion","JESDownSigRegion","ttWctrl","JESUpttWctrl","JESDownttWctrl"],
#"DNNAMS3Cat1_option1":["SigRegion","JESUpSigRegion","JESDownSigRegion","ttWctrl","JESUpttWctrl","JESDownttWctrl"],
#"DNNAMS3Cat1_option2":["SigRegion","JESUpSigRegion","JESDownSigRegion","ttWctrl","JESUpttWctrl","JESDownttWctrl"],
#"DNNAMS3Cat1_option3":["SigRegion","JESUpSigRegion","JESDownSigRegion","ttWctrl","JESUpttWctrl","JESDownttWctrl"]
}

ignorefiles = ["TTH","H"]


treeNames={
"SubCat2l":"syncTree",
"DNNCat":"syncTree",
"DNNCat_option2":"syncTree",
"DNNCat_option3":"syncTree",
"DNNSubCat1_option1":"syncTree",
"DNNSubCat1_option2":"syncTree",
"DNNSubCat1_option3":"syncTree",
"DNNSubCat2_option1":"syncTree",
"DNNSubCat2_option2":"syncTree",
"DNNSubCat2_option3":"syncTree",
"DNNAMS2Cat1_option1":"syncTree",
"DNNAMS2Cat1_option2":"syncTree",
"DNNAMS2Cat1_option3":"syncTree",
"DNNAMS3Cat1_option1":"syncTree",
"DNNAMS3Cat1_option2":"syncTree",
"DNNAMS3Cat1_option3":"syncTree",
}


executable =  "runReadingNoMVA.C"

def prepareCshJob(shFile,channel, nPerBin, key, value, dataEra):
    subFile      = file(shFile,"w")
    print >> subFile, "#!/bin/bash"
    print >> subFile, "/bin/hostname"
    print >> subFile, "source /cvmfs/sft.cern.ch/lcg/views/LCG_93/x86_64-slc6-gcc62-opt/setup.sh"
    print >> subFile, "gcc -v"
    print >> subFile, "pwd"
    Output = "Output_%s_GT%s"%(year,nPerBin)
    # i+1 stands for channel, i==SubCat2l, in ttH 2lss
    for dirToCheck in dirsToCheck[key]:
        if dirToCheck in dirsIgnored: continue
        regName = "SigRegion"
        for reg in Regions: 
            if reg in dirToCheck: regName = reg
        if not os.path.exists(Output+"/"+key+"/"+value[channel]+"/"+dirToCheck):
            os.popen("mkdir -p "+Output+"/"+key+"/"+value[channel]+"/"+dirToCheck)
        dirOI = inputBaseDir+"/"+reg+"/"+year+"/"+dirToCheck
        if not os.path.isdir(dirOI):
            print ( "WARNING %s doesn't exists !!!! "%dirOI)
            continue
        inputfiles = [f for f in os.listdir(dirOI) if "root" in f]
        for inputfile in inputfiles:
            process = inputfile.split(("_"+dirToCheck))[0]
            if process in ignorefiles: continue
            if process == "data" or process =="Fakes" or process== "Flips" or process=="Data":
                command_run = "root -l -b -q "+frameworkDir+executable+"'"+'("'+regName+'","'+inputBaseDir+"/"+BinDir+'/","'+process+'","'+dirToCheck+'","'+Output+'/'+key+"/"+value[channel]+"/"+dirToCheck+'",true,'+str(nPerBin)+','+str(channel)+',"'+key+'","'+treeNames[key]+'","'+inputBaseDir+'",'+dataEra+")'"
                print >> subFile, command_run 
            else:
                command_run = "root -l -b -q "+frameworkDir+executable+"'"+'("'+regName+'","'+inputBaseDir+"/"+BinDir+'/","'+process+'","'+dirToCheck+'","'+Output+'/'+key+"/"+value[channel]+"/"+dirToCheck+'",false,'+str(nPerBin)+','+str(channel)+',"'+key+'","'+treeNames[key]+'","'+inputBaseDir+'",'+dataEra+")'"
                #command_run = "root -l -b -q "+frameworkDir+executable+"'"+'("'+process+'","'+dirToCheck+'","Output/'+key+"/"+value[channel]+"/"+dirToCheck+'",false,'+str(channel)+',"'+key+'","'+treeNames[key]+'")'+"'"
                print >> subFile, command_run 
    subprocess.call("chmod 777 "+shFile, shell=True)

for nPerBin in nPerBins:
    for year in years:
        outputdir = "Output_%s_GT%s"%(year,nPerBin)
        if not os.path.exists(outputdir):
            os.popen("mkdir "+outputdir)
    
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
                if not os.path.exists(outputdir+"/"+key+"/"+value[i]):
                    os.popen("mkdir -p "+outputdir+"/"+key+"/"+value[i])
                shFileName = outputBaseDir + "/"+outputdir+"/" +key+"/"+value[i] + "/"+value[i]+"Job.sh"
                logFileName = outputBaseDir + "/"+outputdir+"/" +key+"/"+value[i] + "/"+value[i]+"job.log"
                errorFileName = outputBaseDir + "/"+outputdir+"/" +key+"/"+value[i] + "/"+value[i]+"job.error"
                prepareCshJob(shFileName, i, nPerBin, key, value, year)
                print >> allJobFile, "hep_sub "+ shFileName + " -o "+logFileName+ " -e "+errorFileName

allJobFile.close()
print "Finished " 
 
