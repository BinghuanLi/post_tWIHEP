import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread
import optparse

usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-f', '--float',        dest='floatOtherPOI'  ,      help='floatOtherPOI or not',      default='-1',        type='int')
parser.add_option('-e', '--era',        dest='era'  ,      help='era 0 means to run all only',      default='0',        type='int')
parser.add_option('-o', '--outDir',        dest='outDir'  ,      help='outDir',      default='obs_results',        type='string')
parser.add_option('-p', '--POI',        dest='POI'  ,      help='POI',      default='r_ttH',        type='string')
parser.add_option("-n","--noRate", dest="noRate", action='store_true')
parser.add_option("-i","--impact", dest="makeImpact", action='store_true')
parser.add_option("-S","--shapes", dest="makeShapes", action='store_true')
parser.add_option("-L","--scan", dest="makeLikeli", action='store_true')
parser.add_option("-g","--GOF", dest="makeGOF", action='store_true')
parser.add_option("-b","--BreakDown", dest="makeBreakDown", action='store_true')

(opt, args) = parser.parse_args()



# please run this file in the same directory you put the datacards

cwd = os.getcwd()

frameworkDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/combJobs/"
inputBaseDir = cwd 

'''
text2workspace.py ttH_DiLepRegion.txt -o ttH_DiLepRegion_3poi.root -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/TTW.*:r_ttW[1,0,6]' --PO 'map=.*/TTWW.*:r_ttW[1,0,6]' --PO 'map=.*/ttH.*:r_ttH[1,-1,3]' --PO 'map=.*/tH.*:r_tH[1,-1,3]'
combine -M AsymptoticLimits ttH_DiLepRegion_3poi.root --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 -n 3poi -m 125 > ObsLimit_ttH_DiLepRegion_3poi_r_ttH_FloatOtherPOI.log
combine -M AsymptoticLimits ttH_DiLepRegion_3poi.root --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 --freezeParameters r_ttW,r_tH -n 3poi -m 125 > ObsLimit_ttH_DiLepRegion_3poi_r_ttH_NoFloatOtherPOI.log
combine -M MultiDimFit ttH_DiLepRegion_3poi.root --algo singles --cl=0.68 -P r_ttH --setParameters r_ttW=1,r_ttH=1,r_tH=1 --floatOtherPOI=1 --saveFitResult -n 3poi --saveWorkspace > ObsSigStrength_3poi_r_ttH_FloatOtherPOI.log
combine -M MultiDimFit ttH_DiLepRegion_3poi.root --algo singles --cl=0.68 -P r_ttH --setParameters r_ttW=1,r_ttH=1,r_tH=1 --floatOtherPOI=0 --saveFitResult -n 3poi --saveWorkspace > ObsSigStrength_3poi_r_ttH_NoFloatOtherPOI.log
'''

floatOtherPOI =  opt.floatOtherPOI # -1/0/1 ; 0: NoFloat, 1: Float, -1: Both
                   # for Impact/likeliscan, 0:TH 1:TTH, -1:Both
makeSigStrenght = True 
makeLimit = False
makeSignificance =True
makeWS = True

if opt.noRate:
    makeSigStrenght = False
    makeLimit = False
    makeSignificance = False

# Set to False ATM if floatOtherPOI = -1 or 1
# Needs to figure out how to add r_ttW r_ttZ...
makeImpact = opt.makeImpact
makeShapes = opt.makeShapes
makeLikeli = opt.makeLikeli
makeGOF = opt.makeGOF
makeBreakDown = opt.makeBreakDown

results_dir = opt.outDir
POI = opt.POI


#dirsToCheck = [f for f in os.listdir(".") if os.path.isdir(f)]
dirsToCheck = ["BDT_RunII"]
dirsToIgnore = []

DatacardName = "ttH_2lss_0tau"
years = ["2016","2017","2018","runII"]
if opt.era == 0:
    years = ["runII"]


def prepareCshJob(shFile, dirName, datacardName, year):
    subFile      = file(shFile,"w")
    print >> subFile, "#!/bin/bash"
    print >> subFile, "/bin/hostname"
    print >> subFile, "gcc -v"
    print >> subFile, "pwd"
    print >> subFile, "cd {}/{}/{}".format(dirName,results_dir,year)
    print >> subFile, "eval `scramv1 runtime -sh`"
    print >> subFile, "ulimit -s unlimited"
    if makeWS:
        # print >> subFile, combineCards
        convertCards =  "text2workspace.py {}/{}.txt -o {}_3poi.root -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/TTW.*:r_ttW[1,0,6]' --PO 'map=.*/TTWW.*:r_ttW[1,0,6]' --PO 'map=.*/ttH.*:r_ttH[1,-1,3]' --PO 'map=.*/tH.*:r_tH[1,-40,40]' --channel-masks".format(dirName,datacardName,datacardName)
        if "node_nBin" in dirName:
            convertCards =  "text2workspace.py {}/{}.txt -o {}_4poi.root -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/TTW.*:r_ttW[1,0,6]' --PO 'map=.*/TTWW.*:r_ttW[1,0,6]' --PO 'map=.*/ttH.*:r_ttH[1,-1,3]' --PO 'map=.*/tH.*:r_tH[1,-40,40]' --PO 'map=.*/data_fakes:r_fakes[1,-1,3]'".format(dirName,datacardName,datacardName)
             
        print >> subFile, convertCards
    
    if "ttHnode_nBin" in dirName:
        ObsLimit_NoFloat = "combine -M AsymptoticLimits "+datacardName + "_4poi.root -m 125 -n 4poi_ttHnode --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1,r_fakes=1 --freezeParameters r_ttW,r_tH,r_fakes > ObsLimit_"+datacardName+"_r_ttH.log"
        print >> subFile, ObsLimit_NoFloat
    elif "Restnode_nBin" in dirName:
        ObsLimit_NoFloat = "combine -M AsymptoticLimits "+datacardName + "_4poi.root -m 125 -n 4poi_Restnode --redefineSignalPOI r_fakes --setParameters r_ttH=1,r_ttW=1,r_tH=1,r_fakes=1 --freezeParameters r_ttW,r_tH,r_ttH > ObsLimit_"+datacardName+"_r_fakes.log"
        print >> subFile, ObsLimit_NoFloat
    elif "tHQnode_nBin" in dirName:
        ObsLimit_NoFloat = "combine -M AsymptoticLimits "+datacardName + "_4poi.root -m 125 -n 4poi_tHQnode --redefineSignalPOI r_tH --setParameters r_ttH=1,r_ttW=1,r_tH=1,r_fakes=1 --freezeParameters r_ttW,r_fakes,r_ttH > ObsLimit_"+datacardName+"_r_tHQ.log"
        print >> subFile, ObsLimit_NoFloat
    elif "ttWnode_nBin" in dirName:
        ObsLimit_NoFloat = "combine -M AsymptoticLimits "+datacardName + "_4poi.root -m 125 -n 4poi_ttWnode --redefineSignalPOI r_ttW --setParameters r_ttH=1,r_ttW=1,r_tH=1,r_fakes=1 --freezeParameters r_tH,r_fakes,r_ttH > ObsLimit_"+datacardName+"_r_ttW.log"
        print >> subFile, ObsLimit_NoFloat
    else:        
        if makeLimit:
            ObsLimit_Float = "combine -M AsymptoticLimits "+datacardName + "_3poi.root -m 125 -t -1 -n 3poi_FloatOtherPOI --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsLimit_"+datacardName+"_3poi_FloatOtherPOI.log"
            ObsLimit_NoFloat = "combine -M AsymptoticLimits "+datacardName + "_3poi.root -m 125 -t -1 -n 3poi_NoFloatOtherPOI --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 --freezeParameters r_tH --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsLimit_"+datacardName+"_3poi_NoFloatOtherPOI.log"
            if floatOtherPOI == -1:
                print >> subFile, ObsLimit_Float
                print >> subFile, ObsLimit_NoFloat
            elif floatOtherPOI == 0:
                print >> subFile, ObsLimit_NoFloat
            elif floatOtherPOI == 1:
                print >> subFile, ObsLimit_Float
        if makeSigStrenght:
            ObsSig_Float = "combine -M MultiDimFit --saveFitResult --saveWorkspace --algo singles --cl=0.68 -P r_ttH -P r_ttW -P r_tH --setParameters r_ttW=1,r_ttH=1,r_tH=1 --floatOtherPOI=1 -d "+datacardName + "_3poi.root -m 125 -t -1 -n 3poi_FloatOtherPOI --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsSigStrength_"+datacardName+"_3poi_FloatOtherPOI.log"
            ObsSig_NoFloat = "combine -M MultiDimFit --saveFitResult --saveWorkspace --algo singles --cl=0.68 -P r_ttH -P r_ttW -P r_tH --setParameters r_ttW=1,r_ttH=1,r_tH=1 --floatOtherPOI=1 --freezeParameters r_tH -d "+datacardName + "_3poi.root -m 125 -t -1 -n 3poi_NoFloatOtherPOI --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsSigStrength_"+datacardName+"_3poi_NoFloatOtherPOI.log"
            if floatOtherPOI == -1:
                print >> subFile, ObsSig_Float
                print >> subFile, ObsSig_NoFloat
            elif floatOtherPOI == 0:
                print >> subFile, ObsSig_NoFloat
            elif floatOtherPOI == 1:
                print >> subFile, ObsSig_Float
        if makeSignificance:
            ObsTTHSignific_Float = "combine -M Significance --signif "+datacardName + "_3poi.root -m 125 -t -1 --redefineSignalPOI r_ttH --setParameters r_ttH=1 --uncapped 1 --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsTTHSignificance_"+datacardName+"_FloatOtherPOI.log"
            ObsTHSignific_Float = "combine -M Significance --signif "+datacardName + "_3poi.root -m 125 -t -1 --redefineSignalPOI r_tH --setParameters r_tH=1 --uncapped 1 --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsTHSignificance_"+datacardName+"_FloatOtherPOI.log"
            ObsTTHSignific_NoFloat = "combine -M Significance --signif "+datacardName + "_3poi.root -m 125 -t -1 --redefineSignalPOI r_ttH --setParameters r_ttH=1 --freezeParameters r_tH --uncapped 1 --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsTTHSignificance_"+datacardName+"_NoFloatOtherPOI.log"
            ObsTHSignific_NoFloat = "combine -M Significance --signif "+datacardName + "_3poi.root -m 125 -t -1 --redefineSignalPOI r_tH --setParameters r_tH=1 --freezeParameters r_ttH --uncapped 1 --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsTHSignificance_"+datacardName+"_NoFloatOtherPOI.log"
            if floatOtherPOI == -1:
                print >> subFile, ObsTTHSignific_Float
                print >> subFile, ObsTTHSignific_NoFloat
                print >> subFile, ObsTHSignific_Float
                print >> subFile, ObsTHSignific_NoFloat
            elif floatOtherPOI == 0:
                print >> subFile, ObsTTHSignific_NoFloat
                print >> subFile, ObsTHSignific_NoFloat
            elif floatOtherPOI == 1:
                print >> subFile, ObsTTHSignific_Float
                print >> subFile, ObsTHSignific_Float
        if makeImpact:
            ObsImpact_TTHFloat = "combineTool.py -M Impacts -d "+datacardName + "_3poi.root -m 125 -t -1 -n 3poi_TTHFloatOtherPOI --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 --doInitialFit --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsImpact_"+datacardName+"_3poi_TTHFloatOtherPOI_InitialFit.log"
            ObsImpact_TTHFloat += "\ncombineTool.py -M Impacts -d "+datacardName + "_3poi.root -m 125 -t -1 -n 3poi_TTHFloatOtherPOI --redefineSignalPOI r_ttH --setParameters r_ttH=1,r_ttW=1,r_tH=1 --doFits --parallel 8 --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsImpact_"+datacardName+"_3poi_TTHFloatOtherPOI_doFits.log"
            ObsImpact_TTHFloat += "\ncombineTool.py -M Impacts -d "+datacardName + "_3poi.root -m 125 -t -1 -n 3poi_TTHFloatOtherPOI --redefineSignalPOI r_ttH -o impacts_exp_3poi_TTHFloatOtherPOI.json --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsImpact_"+datacardName+"_3poi_TTHFloatOtherPOI_2json.log"
            ObsImpact_TTHFloat += "\nplotImpacts.py -i impacts_exp_3poi_TTHFloatOtherPOI.json -o impacts_exp_3poi_TTHFloatOtherPOI"
            ObsImpact_THFloat = "combineTool.py -M Impacts -d "+datacardName + "_3poi.root -m 125 -t -1 -n 3poi_THFloatOtherPOI --redefineSignalPOI r_tH --setParameters r_ttH=1,r_ttW=1,r_tH=1 --doInitialFit --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic  > ObsImpact_"+datacardName+"_3poi_THFloatOtherPOI_InitialFit.log"
            ObsImpact_THFloat += "\ncombineTool.py -M Impacts -d "+datacardName + "_3poi.root -m 125 -t -1 -n 3poi_THFloatOtherPOI --redefineSignalPOI r_tH --setParameters r_ttH=1,r_ttW=1,r_tH=1 --doFits --parallel 8  --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsImpact_"+datacardName+"_3poi_THFloatOtherPOI_doFits.log"
            ObsImpact_THFloat += "\ncombineTool.py -M Impacts -d "+datacardName + "_3poi.root -m 125 -t -1 -n 3poi_THFloatOtherPOI --redefineSignalPOI r_tH --setPararmeters r_ttH=1,r_ttW=1,r_tH=1 -o impacts_exp_3poi_THFloatOtherPOI.json --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsImpact_"+datacardName+"_3poi_THFloatOtherPOI_2json.log"
            ObsImpact_THFloat += "\nplotImpacts.py -i impacts_exp_3poi_THFloatOtherPOI.json -o impacts_exp_3poi_THFloatOtherPOI"
            if floatOtherPOI == -1:
                print >> subFile, ObsImpact_TTHFloat
                print >> subFile, ObsImpact_THFloat
            elif floatOtherPOI == 0:
                print >> subFile, ObsImpact_THFloat
            elif floatOtherPOI == 1:
                print >> subFile, ObsImpact_TTHFloat
        if makeShapes:
            Shapes_Float = "combineTool.py -M FitDiagnostics --setParameters r_ttW=1,r_ttH=1,r_tH=1 -d "+datacardName + "_3poi.root --saveShapes --saveWithUncertainties --saveNormalization -m 125 -t -1 -n _shapes_combine_ttH_2lss_0tau_"+ year+" --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsShapes_"+datacardName+"_3poi_FloatOtherPOI.log"
            Shapes_NoFloat = "combineTool.py -M FitDiagnostics --setParameters r_ttW=1,r_ttH=1,r_tH=1 --freezeParmaters r_tH -d "+datacardName + "_3poi.root --saveShapes --saveWithUncertainties --saveNormalization -m 125 -t -1 -n _shapes_freezeTH_combine_ttH_2lss_0tau_"+ year+" --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsShapes_"+datacardName+"_3poi_NoFloatOtherPOI.log"
            if floatOtherPOI == -1:
                print >> subFile, Shapes_Float
                print >> subFile, Shapes_NoFloat
            elif floatOtherPOI == 0:
                print >> subFile, Shapes_NoFloat
            elif floatOtherPOI == 1:
                print >> subFile, Shapes_Float
        if makeLikeli:
            ObsLikeli_TTHFloat = "combine -M MultiDimFit --algo singles --cl=0.68 -P r_ttH --setParameters r_ttW=1,r_tH=1 --setParameterRanges r_ttH,-1,4 --floatOtherPOI=1 --robustFit 1 -d %s_3poi.root -m 125 -t -1 -n bestfit --saveWorkspace --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsLikeli_%s_3poi_TTHbestfit.log"%(datacardName,datacardName)
            ObsLikeli_TTHFloat += "\ncombine -M MultiDimFit --algo grid --points=100 -P r_ttH --setParameters r_ttW=1,r_tH=1 --setParameterRanges r_ttH,-1,4 --floatOtherPOI=1 --robustFit 1 -m 125 -t -1 -n stat higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsLikeli_%s_3poi_TTHStatOnly.log"%datacardName
            ObsLikeli_TTHFloat += "\ncombine -M MultiDimFit --algo grid --points=100 -P r_ttH --setParameters r_ttW=1,r_tH=1 --setParameterRanges r_ttH,-1,4 --floatOtherPOI=1 --robustFit 1 -n nominal -m 125 -t -1 -d %s_3poi.root --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsLikeli_%s_3poi_TTHnominal.log"%(datacardName,datacardName)
            ObsLikeli_TTHFloat += "\nplot1DScan.py higgsCombinenominal.MultiDimFit.mH125.root --others 'higgsCombinestat.MultiDimFit.mH125.root:Stat only:2' --breakdown syst,stat --output ttH_likeliscat_exp --POI r_ttH --main-label Expected"
            ObsLikeli_THFloat = "combine -M MultiDimFit --algo singles --cl=0.68 -P r_tH --setParameters r_ttW=1,r_ttH=1 --setParameterRanges r_tH,-40,40 --floatOtherPOI=1 --robustFit 1 -d %s_3poi.root -m 125 -t -1 -n bestfit --saveWorkspace --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsLikeli_%s_3poi_THbestfit.log"%(datacardName,datacardName)
            ObsLikeli_THFloat += "\ncombine -M MultiDimFit --algo grid --points=100 -P r_tH --setParameters r_ttW=1,r_ttH=1 --setParameterRanges r_tH,-40,40 --floatOtherPOI=1 --robustFit 1 -m 125 -t -1 -n stat higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsLikeli_%s_3poi_THStatOnly.log"%datacardName
            ObsLikeli_THFloat += "\ncombine -M MultiDimFit --algo grid --points=100 -P r_tH --setParameters r_ttW=1,r_ttH=1 --setParameterRanges r_tH,-40,40 --floatOtherPOI=1 --robustFit 1 -n nominal -m 125 -t -1 -d %s_3poi.root --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > ObsLikeli_%s_3poi_THnominal.log"%(datacardName,datacardName)
            ObsLikeli_THFloat += "\nplot1DScan.py higgsCombinenominal.MultiDimFit.mH125.root --others 'higgsCombinestat.MultiDimFit.mH125.root:Stat only:2' --breakdown syst,stat --output tH_likeliscat_exp --POI r_tH --main-label Expected"
            if floatOtherPOI == -1:
                print >> subFile, ObsLikeli_TTHFloat
                print >> subFile, ObsLikeli_THFloat
            elif floatOtherPOI == 0:
                print >> subFile, ObsLikeli_THFloat
            elif floatOtherPOI == 1:
                print >> subFile, ObsLikeli_TTHFloat
        if makeGOF:
            GOF= "combine -M GoodnessOfFit --algo saturated --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerTolerance 1e-1 -s -1 -D data_obs --fixedSignalStrength 1 %s_3poi.root -n data_obs > ObsGOF_%s_dataobs.log"%(datacardName,datacardName)
            GOF += "\ncombine -M GoodnessOfFit --algo saturated --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerTolerance 1e-1 -s -1 -D data_obs --fixedSignalStrength 1 -t 300 --toysFrequentist %s_3poi.root -n toys300 > ObsGOF_%s_toys.log"%(datacardName,datacardName)
            print >> subFile, GOF


        if makeBreakDown and year=="runII":
            BreakDown = "combine -M MultiDimFit --algo singles --cl=0.68 -P r_ttH -P r_tH -P r_ttW --setParameters r_ttW=1,r_ttH=1,r_tH=1 --floatOtherPOI=1 --robustFit 1 -d %s_3poi.root -m 125 -t -1 -n bestfit --saveWorkspace --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > BreakDown_BestFit.log"%datacardName
            BreakDown += "\ncombine -M MultiDimFit --algo singles --cl=0.68 -P {} --setParameters r_ttH=1,r_ttW=1,r_tH=1 --floatOtherPOI=1 --robustFit 1 -m 125 -t -1 -n stat higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > BreakDown_freezeAllConstrained.log".format(POI)
            BreakDown += "\ncombine -M MultiDimFit --algo singles --cl=0.68 -P {} --setParameters r_ttH=1,r_ttW=1,r_tH=1 --floatOtherPOI=1 --robustFit 1 -m 125 -t -1 -n autoMCStats higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeNuisanceGroups autoMCStats --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > BreakDown_freezeautoMCStats.log".format(POI)
            BreakDown += "\ncombine -M MultiDimFit --algo singles --cl=0.68 -P {} --setParameters r_ttH=1,r_ttW=1,r_tH=1 --floatOtherPOI=1 --robustFit 1 -m 125 -t -1 -n lumi higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeNuisanceGroups lumi --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > BreakDown_freezelumi.log".format(POI)
            BreakDown += "\ncombine -M MultiDimFit --algo singles --cl=0.68 -P {} --setParameters r_ttH=1,r_ttW=1,r_tH=1 --floatOtherPOI=1 --robustFit 1 -m 125 -t -1 -n lepEff higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeNuisanceGroups lepEff --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > BreakDown_freezelepEff.log".format(POI)
            BreakDown += "\ncombine -M MultiDimFit --algo singles --cl=0.68 -P {} --setParameters r_ttH=1,r_ttW=1,r_tH=1 --floatOtherPOI=1 --robustFit 1 -m 125 -t -1 -n btag higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeNuisanceGroups btag --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > BreakDown_freezebtag.log".format(POI)
            BreakDown += "\ncombine -M MultiDimFit --algo singles --cl=0.68 -P {} --setParameters r_ttH=1,r_ttW=1,r_tH=1 --floatOtherPOI=1 --robustFit 1 -m 125 -t -1 -n Jec higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeNuisanceGroups Jec --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > BreakDown_freezeJec.log".format(POI)
            BreakDown += "\ncombine -M MultiDimFit --algo singles --cl=0.68 -P {} --setParameters r_ttH=1,r_ttW=1,r_tH=1 --floatOtherPOI=1 --robustFit 1 -m 125 -t -1 -n misID higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeNuisanceGroups misID --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > BreakDown_freezemisID.log".format(POI)
            BreakDown += "\ncombine -M MultiDimFit --algo singles --cl=0.68 -P {} --setParameters r_ttH=1,r_ttW=1,r_tH=1 --floatOtherPOI=1 --robustFit 1 -m 125 -t -1 -n Trigger higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeNuisanceGroups Trigger --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > BreakDown_freezeTrigger.log".format(POI)
            BreakDown += "\ncombine -M MultiDimFit --algo singles --cl=0.68 -P {} --setParameters r_ttH=1,r_ttW=1,r_tH=1 --floatOtherPOI=1 --robustFit 1 -m 125 -t -1 -n Theory higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeNuisanceGroups Theory --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > BreakDown_freezeTheory.log".format(POI)
            BreakDown += "\ncombine -M MultiDimFit --algo singles --cl=0.68 -P {} --setParameters r_ttH=1,r_ttW=1,r_tH=1 --floatOtherPOI=1 --robustFit 1 -m 125 -t -1 -n BkgNorm higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeNuisanceGroups BkgNorm --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > BreakDown_freezeBkgNorm.log".format(POI)
            BreakDown += "\ncombine -M MultiDimFit --algo singles --cl=0.68 -P {} --setParameters r_ttH=1,r_ttW=1,r_tH=1 --floatOtherPOI=1 --robustFit 1 -m 125 -t -1 -n Prefire higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeNuisanceGroups Prefire --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > BreakDown_freezePrefire.log".format(POI)
            BreakDown += "\ncombine -M MultiDimFit --algo singles --cl=0.68 -P {} --setParameters r_ttH=1,r_ttW=1,r_tH=1 --floatOtherPOI=1 --robustFit 1 -m 125 -t -1 -n Pileup higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeNuisanceGroups Pileup --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic > BreakDown_freezePileup.log".format(POI)
            print >> subFile, BreakDown

    subprocess.call("chmod 777 "+shFile, shell=True)

allJobFile = 0
if os.path.exists(os.getcwd()+"/"+results_dir+"all.sh"):
    allJobFile = open(os.getcwd()+"/"+results_dir+"all.sh","a")
else:
    allJobFile = open(os.getcwd()+"/"+ results_dir + "all.sh","w")
    allJobFile.write("#!/bin/bash\n")


for dirToCheck in dirsToCheck:
  if dirToCheck in dirsToIgnore: continue
  for year in years:
        DirName_datacard = inputBaseDir+"/"+dirToCheck
        if not os.path.exists("{}/{}/{}".format(DirName_datacard, results_dir,year)):
            os.popen("mkdir -p {}/{}/{}".format(DirName_datacard,results_dir,year))
        #print(var)
        print(DirName_datacard)
        datacardName = "%s_%s"%(DatacardName,year)
        shFileName = DirName_datacard + "/"+results_dir+"/"+year+"/Fit_"+results_dir+dirToCheck+"_"+datacardName+"_Job.sh"
        logFileName = DirName_datacard + "/"+results_dir+"/"+year+"/Fit_"+results_dir+dirToCheck+"_"+datacardName+"_Job.log"
        errorFileName = DirName_datacard + "/"+results_dir+"/"+year+"/Fit_"+results_dir+dirToCheck+"_"+datacardName+"_Job.error"
        prepareCshJob(shFileName, DirName_datacard, datacardName, year)
        #command_cp = "cp "+frameworkDir+impact+" "+DirName_datacard
        #print(command_cp)
        #os.system(command_cp)
        print >> allJobFile, "hep_sub -os SL7 "+ shFileName + " -o "+logFileName+ " -e "+errorFileName

allJobFile.close()
print "Finished " 
