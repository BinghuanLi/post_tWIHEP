#!/usr/bin/env python
import sys, os
import optparse
import ROOT as r
from datetime import datetime
r.gROOT.SetBatch(True)

from ROOT import TFile
from pprint import pprint

usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-i', '--inputDir',        dest='inputDir'  ,      help='inputDir',      default='/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/CombineStuff/CMSSW_10_2_13/src/datacards/legacy_PHD_SM_28June/DNNSubCat2_BIN_RunII/ttH_breakdown_exp_results/runII/',        type='string')
parser.add_option('-b', '--bestFit',        dest='bestFitFile'  ,      help='bestFitFile',      default='higgsCombinebestfit.MultiDimFit.mH125.root',        type='string')
parser.add_option('-p', '--POI',        dest='POI'  ,      help='POI',      default='r_ttH',        type='string')
parser.add_option('-t', '--tag',        dest='tag'  ,      help='tag',      default='test',        type='string')
parser.add_option('-f', '--freezedNP',        dest='freezedNP'  ,      help='NP to be freezed',      default='stat',        type='string')
(opt, args) = parser.parse_args()

bestFitFile = opt.bestFitFile
POI = opt.POI
tag = opt.tag
inputDir = opt.inputDir
freezedNP = opt.freezedNP
freezedFile = bestFitFile.replace("bestfit",freezedNP)

outputDir = inputDir + "/results"
####### check output dir ############
if not os.path.exists(outputDir):
    print('mkdir ', outputDir)
    os.makedirs(outputDir)


########## create log file ##########
logfile = open("{}/uncertaintyBreakDown_{}_{}.log".format(outputDir, tag, POI) ,"a")
logfile.write("TIME : {}\n".format(datetime.now()))


def getTripletFromFile(fName, poi):
    f = TFile.Open(fName)
    # f.Print()
    t = f.Get('limit')
    # t.Scan('*')
    vals = []
    i=0
    r_bestFit = -1
    for e in t:
        if i >2:
            continue
        #vals.append( (e.quantileExpected, e.limit) )
        if poi=="r_ttH":
            if e.quantileExpected == -1 : r_bestFit = e.r_ttH
            vals.append( (e.quantileExpected, e.r_ttH) )
        elif poi=="r_tH":
            if e.quantileExpected == -1 : r_bestFit = e.r_tH
            vals.append( (e.quantileExpected, e.r_tH) )
        elif poi=="r_ttW":
            if e.quantileExpected == -1 : r_bestFit = e.r_ttW
            vals.append( (e.quantileExpected, e.r_ttW) )
        else:
            print(" ERROR: POI must be r_ttH, r_tH or r_ttW")
            sys.exit()
        i +=1 
    logfile.write("{} : {} best fit {} \n".format(fName, poi, r_bestFit))
    #print (vals)
    return UncertaintiesFromTriplet(vals), r_bestFit

def UncertaintiesFromTriplet(triplet):
    #This assumes that the values are ordered as central(0),lower(1),upper(2)
    #This could be found from the quantileExpected value, but I was lazy
    up = triplet[2][1] - triplet[0][1]
    dn = triplet[1][1] - triplet[0][1]
    # print dn, up
    return (dn, up)

from math import sqrt
def quadDiff(unc1, unc2, rs):
    if not ( rs[0] == rs[1]):
        print ( "WARNING, r0 and r1 best fit is different: r0 is {}, r1 is {}.  ".format(rs[0], rs[1]))
    if ( unc1[0]**2 < unc2[0]**2) or ( unc1[1]**2 < unc2[1]**2):
        print ( "WARNING, freezeNP {} leads to larger uncertainty, to FIXME, I take the absoulte value ".format(freezedNP))
    dn = sqrt( abs(unc1[0]**2 - unc2[0]**2) )
    up = sqrt( abs(unc1[1]**2 - unc2[1]**2) )
    return (-dn/rs[0], up/rs[0])

uncs = []
Rs = []

for f in [bestFitFile, freezedFile]:
    f1 = "{}/{}".format(inputDir, f)
    values, r = getTripletFromFile(f1, POI)
    uncs.append(values)
    Rs.append(r)

diff = quadDiff(uncs[0],uncs[1], Rs)

logfile.write("%s freezed : _{%.3f}^{+%.3f} \n "%(freezedNP, diff[0], diff[1]))
