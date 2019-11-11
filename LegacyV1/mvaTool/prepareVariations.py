import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread



#dirsToCheck = [f for f in os.listdir(".") if os.path.isdir(f)]
dirsIgnored =  ["ttZctrl"]

dirsToCheck = ["SigRegion","JESUpSigRegion","JESDownSigRegion","ttWctrl","JESUpttWctrl","JESDownttWctrl"]
#dirsToCheck = ["SigRegion","JESUpSigRegion"]

ignorefiles = ["TTH","H"]


ListOfCats={"SubCat2l":{0:"inclusive", 1:"ee_neg",2:"ee_pos",3:"em_bl_neg",4:"em_bl_pos",5:"em_bt_neg",6:"em_bt_pos",7:"mm_bl_neg",8:"mm_bl_pos",9:"mm_bt_neg",10:"mm_bt_pos"}}

if not os.path.exists("Output"):
        os.popen("mkdir Output")

for key,value in ListOfCats.iteritems():
  n_values = len(value)
  print ("SubCat is " + key + " with subcatgories of " +str(n_values-1)  )
  for i in range(n_values):
#for i in range(6,10):
    # i+1 stands for channel, i==SubCat2l, in ttH 2lss
    for dirToCheck in dirsToCheck:
        if dirToCheck in dirsIgnored: continue
        if not os.path.exists("Output/"+key+"/"+value[i]+"/"+dirToCheck):
            os.popen("mkdir -p Output/"+key+"/"+value[i]+"/"+dirToCheck)
        inputfiles = [f for f in os.listdir("./"+dirToCheck) if "root" in f]
        #inputfiles = ["TTH_hmm"]
        for inputfile in inputfiles:
            process = inputfile.split(("_"+dirToCheck))[0]
            if process in ignorefiles: continue
            if process == "data" or process =="Fakes" or process== "Flips":
                command_run = "root -l -b -q runReadingNoMVA.C'"+'("'+process+'","'+dirToCheck+'","Output/'+key+"/"+value[i]+"/"+dirToCheck+'",true,'+str(i)+',"'+key+'"'+")'"
                print command_run
                os.system(command_run)
            else:
                command_run = "root -l -b -q runReadingNoMVA.C'"+'("'+process+'","'+dirToCheck+'","Output/'+key+"/"+value[i]+"/"+dirToCheck+'",false,'+str(i)+',"'+key+'"'+")'"
                #command_run = "root -l -b -q runReadingNoMVA.C'"+'("'+process+'","","Output/","false",'+str(i+1)+")'"
                print command_run
                os.system(command_run)
    #root -l runReadingNoMVA.C'("TTH","2LSS/","output/")'
