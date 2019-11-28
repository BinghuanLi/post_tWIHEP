import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread

# please run this file in the same directory you put the datacards

cwd = os.getcwd()

frameworkDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/combJobs/"
inputBaseDir = cwd 

'''
text2workspace.py ttH_DiLepRegion.txt -o ttH_DiLepRegion_3poi.root -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/TTW.*:r_ttW[1,0,6]' --PO 'map=.*/TTWW.*:r_ttW[1,0,6]' --PO 'map=.*/ttH.*:r_ttH[1,-1,3]' --PO 'map=.*/tH.*:r_tH[1,-1,3]'
combine -M AsymptoticLimits ttH_DiLepRegion_3poi.root -t -1 --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 -n 3poi -m 125 > ExpLimit_ttH_DiLepRegion_3poi_r_ttH_FloatOtherPOI.log
combine -M AsymptoticLimits ttH_DiLepRegion_3poi.root -t -1 --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 --freezeParameters r_ttW,r_tH -n 3poi -m 125 > ExpLimit_ttH_DiLepRegion_3poi_r_ttH_NoFloatOtherPOI.log
combine -M MultiDimFit ttH_DiLepRegion_3poi.root --algo singles --cl=0.68 -t -1 -P r_ttH --setParameters r_ttW=1,r_ttH=1,r_tH=1 --floatOtherPOI=1 --saveFitResult -n 3poi --saveWorkspace > ExpSigStrength_3poi_r_ttH_FloatOtherPOI.log
combine -M MultiDimFit ttH_DiLepRegion_3poi.root --algo singles --cl=0.68 -t -1 -P r_ttH --setParameters r_ttW=1,r_ttH=1,r_tH=1 --floatOtherPOI=0 --saveFitResult -n 3poi --saveWorkspace > ExpSigStrength_3poi_r_ttH_NoFloatOtherPOI.log
'''

floatOtherPOI = 1 # -1/0/1 ; 0: NoFloat, 1: Float, -1: Both
makeSigStrenght = False
makeLimit = False
makeWS = True

# Set to False ATM if floatOtherPOI = -1 or 1
# Needs to figure out how to add r_ttW r_ttZ...
makeImpact = True
makeShapes = False
makeSignificance = True


#dirsToCheck = [f for f in os.listdir(".") if os.path.isdir(f)]
dirsToCheck = ["BDT_ee_pos_RunII"]
dirsToIgnore = ["buggy"]

DatacardName = "ttH_2lss_0tau"
#years = ["2016","2017","2018","runII"]
years = ["2016"]



def prepareCshJob(shFile, dirName, datacardName, year):
    subFile      = file(shFile,"w")
    print >> subFile, "#!/bin/bash"
    print >> subFile, "/bin/hostname"
    print >> subFile, "gcc -v"
    print >> subFile, "pwd"
    print >> subFile, "cd "+dirName+"/results/"+year
    print >> subFile, "eval `scramv1 runtime -sh`"
    if makeWS:
        # print >> subFile, combineCards
        convertCards =  "text2workspace.py {}/{}.txt -o {}_3poi.root -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/TTW.*:r_ttW[1,0,6]' --PO 'map=.*/TTWW.*:r_ttW[1,0,6]' --PO 'map=.*/ttH.*:r_ttH[1,-1,3]' --PO 'map=.*/tH.*:r_tH[1,-1,3]'".format(dirName,datacardName,datacardName)
        if "node_nBin" in dirName:
            convertCards =  "text2workspace.py {}/{}.txt -o {}_4poi.root -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/TTW.*:r_ttW[1,0,6]' --PO 'map=.*/TTWW.*:r_ttW[1,0,6]' --PO 'map=.*/ttH.*:r_ttH[1,-1,3]' --PO 'map=.*/tH.*:r_tH[1,-1,3]' --PO 'map=.*/data_fakes:r_fakes[1,-1,3]'".format(dirName,datacardName,datacardName)
             
        print >> subFile, convertCards
    
    if "ttHnode_nBin" in dirName:
        ExpLimit_NoFloat = "combine -M AsymptoticLimits "+datacardName + "_4poi.root -t -1 -m 125 -n 4poi_ttHnode --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1,r_fakes=1 --freezeParameters r_ttW,r_tH,r_fakes > ExpLimit_"+datacardName+"_r_ttH.log"
        print >> subFile, ExpLimit_NoFloat
    elif "Restnode_nBin" in dirName:
        ExpLimit_NoFloat = "combine -M AsymptoticLimits "+datacardName + "_4poi.root -t -1 -m 125 -n 4poi_Restnode --redefineSignalPOI r_fakes --setParameters r_ttH=1,r_ttW=1,r_tH=1,r_fakes=1 --freezeParameters r_ttW,r_tH,r_ttH > ExpLimit_"+datacardName+"_r_fakes.log"
        print >> subFile, ExpLimit_NoFloat
    elif "tHQnode_nBin" in dirName:
        ExpLimit_NoFloat = "combine -M AsymptoticLimits "+datacardName + "_4poi.root -t -1 -m 125 -n 4poi_tHQnode --redefineSignalPOI r_tH --setParameters r_ttH=1,r_ttW=1,r_tH=1,r_fakes=1 --freezeParameters r_ttW,r_fakes,r_ttH > ExpLimit_"+datacardName+"_r_tHQ.log"
        print >> subFile, ExpLimit_NoFloat
    elif "ttWnode_nBin" in dirName:
        ExpLimit_NoFloat = "combine -M AsymptoticLimits "+datacardName + "_4poi.root -t -1 -m 125 -n 4poi_ttWnode --redefineSignalPOI r_ttW --setParameters r_ttH=1,r_ttW=1,r_tH=1,r_fakes=1 --freezeParameters r_tH,r_fakes,r_ttH > ExpLimit_"+datacardName+"_r_ttW.log"
        print >> subFile, ExpLimit_NoFloat
    else:        
        if makeLimit:
            ExpLimit_Float = "combine -M AsymptoticLimits "+datacardName + "_3poi.root -t -1 -m 125 -n 3poi_FloatOtherPOI --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1  > ExpLimit_"+datacardName+"_3poi_FloatOtherPOI.log"
            ExpLimit_NoFloat = "combine -M AsymptoticLimits "+datacardName + "_3poi.root -t -1 -m 125 -n 3poi_NoFloatOtherPOI --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 --freezeParameters r_ttW,r_tH > ExpLimit_"+datacardName+"_3poi_NoFloatOtherPOI.log"
            if floatOtherPOI == -1:
                print >> subFile, ExpLimit_Float
                print >> subFile, ExpLimit_NoFloat
            elif floatOtherPOI == 0:
                print >> subFile, ExpLimit_NoFloat
            elif floatOtherPOI == 1:
                print >> subFile, ExpLimit_Float
        if makeSigStrenght:
            ExpSig_Float = "combine -M MultiDimFit --saveFitResult --saveWorkspace --algo singles --cl=0.68 -t -1 -P r_ttH --setParameters r_ttW=1,r_ttH=1,r_tH=1 --floatOtherPOI=1 -d "+datacardName + "_3poi.root -m 125 -n 3poi_FloatOtherPOI > ExpSigStrength_"+datacardName+"_3poi_FloatOtherPOI.log"
            ExpSig_NoFloat = "combine -M MultiDimFit --saveFitResult --saveWorkspace --algo singles --cl=0.68 -t -1 -P r_ttH --setParameters r_ttW=1,r_ttH=1,r_tH=1 --floatOtherPOI=0 -d "+datacardName + "_3poi.root -m 125 -n 3poi_NoFloatOtherPOI > ExpSigStrength_"+datacardName+"_3poi_NoFloatOtherPOI.log"
            if floatOtherPOI == -1:
                print >> subFile, ExpSig_Float
                print >> subFile, ExpSig_NoFloat
            elif floatOtherPOI == 0:
                print >> subFile, ExpSig_NoFloat
            elif floatOtherPOI == 1:
                print >> subFile, ExpSig_Float
        if makeSignificance:
            ExpSignific_Float = "combine -M Significance --signif "+datacardName + "_3poi.root -t -1 -m 125 --redefineSignalPOI r_ttH --setParameters r_ttH=1 > ExpSignificance_"+datacardName+"_FloatOtherPOI.log"
            ExpSignific_NoFloat = "combine -M Significance --signif "+datacardName + "_3poi.root -t -1 -m 125 --redefineSignalPOI r_ttH --setParameters r_ttH=1 --freezeParameters r_ttW,r_tH > ExpSignificance_"+datacardName+"_NoFloatOtherPOI.log"
            if floatOtherPOI == -1:
                print >> subFile, ExpSignific_Float
                print >> subFile, ExpSignific_NoFloat
            elif floatOtherPOI == 0:
                print >> subFile, ExpSignific_NoFloat
            elif floatOtherPOI == 1:
                print >> subFile, ExpSignific_Float
        if makeImpact:
            ExpImpact_Float = "combineTool.py -M Impacts -d "+datacardName + "_3poi.root -t -1 -m 125 -n 3poi_FloatOtherPOI --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 --doInitialFit  > ExpImpact_"+datacardName+"_3poi_FloatOtherPOI_InitialFit.log"
            ExpImpact_Float += "\ncombineTool.py -M Impacts -d "+datacardName + "_3poi.root -t -1 -m 125 -n 3poi_FloatOtherPOI --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 --doFits --parallel 8  > ExpImpact_"+datacardName+"_3poi_FloatOtherPOI_doFits.log"
            ExpImpact_Float += "\ncombineTool.py -M Impacts -d "+datacardName + "_3poi.root -t -1 -m 125 -n 3poi_FloatOtherPOI --redefineSignalPOI r_ttH -o impacts_exp_3poi_FloatOtherPOI.json  > ExpImpact_"+datacardName+"_3poi_FloatOtherPOI_2json.log"
            ExpImpact_Float += "\nplotImpacts.py -i impacts_exp_3poi_FloatOtherPOI.json -o impacts_exp_3poi_FloatOtherPOI"
            ExpImpact_NoFloat = "combineTool.py -M Impacts -d "+datacardName + "_3poi.root -t -1 -m 125 -n 3poi_NoFloatOtherPOI --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 --freezeParameters r_ttW,r_tH --doInitialFit  > ExpImpact_"+datacardName+"_3poi_NoFloatOtherPOI_InitialFit.log"
            ExpImpact_NoFloat += "\ncombineTool.py -M Impacts -d "+datacardName + "_3poi.root -t -1 -m 125 -n 3poi_NoFloatOtherPOI --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 --freezeParameters r_ttW,r_tH --doFits --parallel 8  > ExpImpact_"+datacardName+"_3poi_NoFloatOtherPOI_doFits.log"
            ExpImpact_NoFloat += "\ncombineTool.py -M Impacts -d "+datacardName + "_3poi.root -t -1 -m 125 -n 3poi_NoFloatOtherPOI --redefineSignalPOI r_ttH --setPararmeters r_ttH=1,r_ttW=1,r_tH=1 --freezeParameters r_ttW,r_tH -o impacts_exp_3poi_NoFloatOtherPOI.json  > ExpImpact_"+datacardName+"_3poi_NoFloatOtherPOI_2json.log"
            ExpImpact_NoFloat += "\nplotImpacts.py -i impacts_exp_3poi_NoFloatOtherPOI.json -o impacts_exp_3poi_NoFloatOtherPOI"
            if floatOtherPOI == -1:
                print >> subFile, ExpImpact_Float
                print >> subFile, ExpImpact_NoFloat
            elif floatOtherPOI == 0:
                print >> subFile, ExpImpact_NoFloat
            elif floatOtherPOI == 1:
                print >> subFile, ExpImpact_Float
        if makeShapes:
            Shapes_NoFloat = "combine -M FitDiagnostics -t -1 --redefineSignalPOI r_ttH --setParameters r_ttW=1,r_ttH=1,r_tH=1 --freezeParameters r_ttW,r_tH -d "+datacardName + "_3poi.root --saveShapes --saveWithUncertainties -m 125 -n 3poi_NoFloatOtherPOI > ExpShapes_"+datacardName+"_3poi_NoFloatOtherPOI.log"
            Shapes_Float = "combine -M FitDiagnostics -t -1 --setParameters r_ttW=1,r_ttH=1,r_tH=1 -d "+datacardName + "_3poi.root --saveShapes --saveWithUncertainties -m 125 -n 3poi_FloatOtherPOI > ExpShapes_"+datacardName+"_3poi_FloatOtherPOI.log"
            if floatOtherPOI == -1:
                print >> subFile, Shapes_Float
                print >> subFile, Shapes_NoFloat
            elif floatOtherPOI == 0:
                print >> subFile, Shapes_NoFloat
            elif floatOtherPOI == 1:
                print >> subFile, Shapes_Float
    subprocess.call("chmod 777 "+shFile, shell=True)

allJobFile = 0
if os.path.exists(os.getcwd()+"/all.sh"):
    allJobFile = open(os.getcwd()+"/all.sh","a")
else:
    allJobFile = open(os.getcwd()+"/all.sh","w")
    allJobFile.write("#!/bin/bash\n")


for dirToCheck in dirsToCheck:
  if dirToCheck in dirsToIgnore: continue
  for year in years:
        DirName_datacard = inputBaseDir+"/"+dirToCheck
        if not os.path.exists("{}/results/{}".format(DirName_datacard,year)):
            os.popen("mkdir -p {}/results/{}".format(DirName_datacard,year))
        #print(var)
        print(DirName_datacard)
        datacardName = "%s_%s"%(DatacardName,year)
        shFileName = DirName_datacard + "/results/"+year+"/Fit_"+dirToCheck+"_"+datacardName+"_Job.sh"
        logFileName = DirName_datacard + "/results/"+year+"/Fit_"+dirToCheck+"_"+datacardName+"_Job.log"
        errorFileName = DirName_datacard + "/results/"+year+"/Fit_"+dirToCheck+"_"+datacardName+"_Job.error"
        prepareCshJob(shFileName, DirName_datacard, datacardName, year)
        #command_cp = "cp "+frameworkDir+impact+" "+DirName_datacard
        #print(command_cp)
        #os.system(command_cp)
        print >> allJobFile, "hep_sub "+ shFileName + " -o "+logFileName+ " -e "+errorFileName

allJobFile.close()
print "Finished " 
