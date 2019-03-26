
# coding: utf-8

# # Ratioplot
# Display two histograms and their ratio.
# 
# This program illustrates how to plot two histograms and their
# ratio on the same canvas. Original macro by Olivier Couet.
# 
# 
# 
# 
# **Author:** Michael Moran  
#
#
# ***
# This program is modified to produce comparison plot of different process 
# The script takes the output of mvaTool.C
# python plotHists.py -r <region> -p <POI> -o <plotOpen> -d<dir> -n<NORM> -c<category> -s<SPLIT> 
# python plotHists.py -r 2lss -p Bin2l -n 1 -b 1 -c SubCat2l -s inclusive
# 9 March 2019   Binghuan Li
# *** 
#

import sys, os, subprocess
import optparse
import distutils.util
import math
import ROOT
from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TString, TFile, TH1, THStack, gROOT, TStyle, TAttFill, TLegend, TGraphAsymmErrors
from ROOT import kBlack, kBlue, kRed, kCyan, kViolet, kGreen, kOrange, kGray, kPink, kTRUE
from ROOT import gROOT

gROOT.SetBatch(kTRUE)


usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-r', '--region',        dest='region'  ,      help='region to plot: 2lss or ttWctrl',      default='2lss',        type='string')
parser.add_option('-p', '--parameter',        dest='POI'  ,      help='parameter of interest',      default='Bin2l',        type='string')
parser.add_option('-c', '--category',        dest='SubCat'  ,      help='categorization',      default='SubCat2l',        type='string')
parser.add_option('-o', '--open',        dest='OPEN'  ,      help='to hold plot open(1) or not(0)',      default='0',        type='int')
parser.add_option('-d', '--dir',        dest='DirOfRootplas'  ,      help='input file full path',      default='/home/binghuan/Work/RootTestFiles/TTHLep_2019/data/2019Rootplas/rootplas_20190227/Output/',        type='string')
parser.add_option('-n', '--norm',        dest='NORM'  ,      help='norm to unit (1) or not(0)',      default='1',        type='int')
parser.add_option('-s', '--split',        dest='SPLIT'  ,      help='to produce plot in subgategory',      default='inclusive',        type='string')

(opt, args) = parser.parse_args()
POI = opt.POI
region = opt.region
OPEN = opt.OPEN
NORM = opt.NORM
DirOfRootplas = opt.DirOfRootplas
SubCat = opt.SubCat
SPLIT = opt.SPLIT

#header_postfix = "2lss l^{#pm}l^{#pm} "
header_postfix = " 2lss "
if region =="ttWctrl": header_postfix = " ttWctrl "


#Samples=["TTH","H","TTW+TTWW","TTZ","EWK","Rares","Conv","Fakes","Flips"]
Samples=["TTH","TTW","TTZ","Fakes+Flips"]
Process={
    "TTH":["TTH_hww","TTH_hzz","TTH_htt","TTH_hmm","TTH_hot"],
    "H":["THW_hww","THW_hzz","THW_htt","THQ_hww","THQ_hzz","THQ_htt"],
    "TTZ":["TTZ"],"TTW+TTWW":["TTW","TTWW"],"Conv":["Conv"],"EWK":["EWK"],"Rares":["Rares"],"Fakes":["Fakes","FakeSub"],"Flips":["Flips"],"Data":["Data"],"TTW":["TTW"],"Fakes+Flips":["Fakes","FakeSub","Flips"],
    }
Color={"TTH":kRed,"H":kPink-4,"TTZ":kGreen,"TTW+TTWW":kGreen+3,"Conv":kOrange,"EWK":kViolet,"Rares":kCyan,"Fakes":kGray,"Flips":kBlack,"TTW":kBlue,"Fakes+Flips":kBlack}
Style={"TTH":1001,"H":1001,"TTZ":1001,"TTW+TTWW":1001,"Conv":1001,"EWK":1001,"Rares":1001,"Fakes":1001,"Flips":1001,"TTW":1001,"Fakes+Flips":1001}

subCats={
"SubCat2l":["inclusive","ee_neg","ee_pos", "em_bl_neg","em_bl_pos","em_bt_neg","em_bt_pos", "mm_bl_neg","mm_bl_pos","mm_bt_neg","mm_bt_pos" ],
"DNNCat":["ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNCat_option2":["ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNCat_option3":["ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNSubCat1_option1":["ee_neg","ee_pos","em_ttHnode","em_ttJnode","em_ttWnode","em_ttZnode","mm_ttHnode","mm_ttJnode","mm_ttWnode","mm_ttZnode"],
"DNNSubCat1_option2":["ee_neg","ee_pos","em_ttHnode","em_ttJnode","em_ttWnode","em_ttZnode","mm_ttHnode","mm_ttJnode","mm_ttWnode","mm_ttZnode"],
"DNNSubCat1_option3":["ee_neg","ee_pos","em_ttHnode","em_ttJnode","em_ttWnode","em_ttZnode","mm_ttHnode","mm_ttJnode","mm_ttWnode","mm_ttZnode"],
"DNNSubCat2_option1":["ee_ttHnode","ee_ttJnode","ee_ttWnode","ee_ttZnode","em_ttHnode","em_ttJnode","em_ttWnode","em_ttZnode","mm_ttHnode","mm_ttJnode","mm_ttWnode","mm_ttZnode"],
"DNNSubCat2_option2":["ee_ttHnode","ee_ttJnode","ee_ttWnode","ee_ttZnode","em_ttHnode","em_ttJnode","em_ttWnode","em_ttZnode","mm_ttHnode","mm_ttJnode","mm_ttWnode","mm_ttZnode"],
"DNNSubCat2_option3":["ee_ttHnode","ee_ttJnode","ee_ttWnode","ee_ttZnode","em_ttHnode","em_ttJnode","em_ttWnode","em_ttZnode","mm_ttHnode","mm_ttJnode","mm_ttWnode","mm_ttZnode"],
}

signals=["TTH"]
if "ttWnode" in SPLIT:
    signals=["TTW+TTWW"]
elif "ttJnode" in SPLIT:
    signals=["Fakes","Conv","Flips"]
elif "ttZnode" in SPLIT:
    signals=["TTZ"]

Channels = []
if not subCats.has_key(SubCat):
    print ("ERROR : " + SubCat +" is not a key of subCats ")
    os._exit()
else:
    Channels = [SPLIT]
    header_postfix += "," + SPLIT.replace("_","\_") 
    print (" Plot channel "+SPLIT)

outputDir = DirOfRootplas+"plots/"+SubCat+"/"+region+"/"+SPLIT
inputRegName = region
if region == "2lss": inputRegName = "SigRegion"

if not os.path.exists(outputDir):
    os.popen("mkdir -p "+outputDir)

def read_rootfile(samplename="TTH_hww"):
    ''' read a root file '''
    fullfilename = DirOfRootplas+SubCat+"/"+SPLIT+"/"+inputRegName+"/output_"+SPLIT+"_"+samplename+".root"
    inputfile = TFile(fullfilename,"read")
    return inputfile

def TGraphToTH1(h1, graph):
    nPoints = graph.GetN()
    for i in range(nPoints):
        x = ROOT.Double(0)
        y = ROOT.Double(0)
        graph.GetPoint(i, x, y)
        xbin = h1.GetXaxis().FindBin(x)
        h1.SetBinContent(xbin,y)
        h1.SetBinError(xbin,math.sqrt(y))

def createSum(h1, h2):
    h3 = h1.Clone("h3")
    h3.SetLineColor(kBlack)
    h3.SetFillColor(kGray+3)
    h3.SetFillStyle(3001)
    h3.SetTitle("")
    #h3.SetMinimum(0.8)
    #h3.SetMaximum(1.35)
    # Set up plot for markers and errors
    h3.Sumw2()
    h3.SetStats(0)
    h3.Add(h2)

    return h3


def readHists():
    inputfile  = read_rootfile() # assuming TTH_hww is always there 
    gROOT.cd()
    histName = POI+"_TTH_hww" 
    h0 = inputfile.Get(histName)
    h_totalbkg = h0.Clone("h_totalbkg")
    h_totalbkg.SetDirectory(0)
    h_totalbkg.Reset()
    h_totalbkg.SetLineColor(kBlack)
    h_totalbkg.SetFillColor(kGray+3)
    h_totalbkg.SetFillStyle(3001)
    h_totalbkg.SetTitle("")
    #h_totalbkg.SetMinimum(0.8)
    #h_totalbkg.SetMaximum(1.35)
    h_totalbkg.Sumw2()
    h_totalbkg.SetStats(0)
            
    h_totalsig = h0.Clone("h_totalsig")
    h_totalsig.SetDirectory(0)
    h_totalsig.Reset()
    #h_totalsig.SetMarkerStyle(20)

    legend = TLegend(0.2,0.6,0.8,0.88)
    #legend.SetHeader("2017 "+fit_type+", 2lss l^{#pm}l^{#pm} #mu(ttH)=#hat#mu")
    legend.SetHeader("2017 prefit, "+header_postfix)
    legend.SetNColumns(3)
    legend.SetBorderSize(0)
    
    hists = []
    Samples.reverse()
    for sample in Samples:
        isSignal = False
        if sample in signals: isSignal = True
        hist=h_totalsig.Clone(sample)
        hist.SetStats(0)
        hist.Reset()
        hist.SetTitle("#scale[0.9]{#font[22]{CMS} #font[12]{Preliminary}                                                              41.53 fb^{-1}(13TeV)}")
        # loop over signal
        if isSignal:
            for p in Process[sample]:
                rootfile  = read_rootfile(p)
                if rootfile.IsZombie():continue
                gROOT.cd()
                h1 = rootfile.Get(POI+"_"+p)
                #h1.SetDirectory(0)
                #if p == "FakeSub" and sample == "Fakes":
                if p == "FakeSub":
                    h_totalsig.Add(h1, -1)
                    hist.Add(h1, -1)
                else:
                    h_totalsig.Add(h1)
                    hist.Add(h1)
                rootfile.Close()
            #hist.SetFillColor(Color[sample])
            hist.SetFillColor(0)
            hist.SetLineColor(Color[sample])
            hist.SetFillStyle(Style[sample])
            hist.SetMarkerStyle(1)
            hists.append(hist)
            legend.AddEntry(hist,sample,"l")
        # loop over bkg
        else:
            for p in Process[sample]:
                rootfile  = read_rootfile(p)
                if rootfile.IsZombie():continue
                gROOT.cd()
                #print " try to get histogram : " + POI+"_"+p
                h1 = rootfile.Get(POI+"_"+p)
                h1.SetDirectory(0)
                #if p == "FakeSub" and sample == "Fakes":
                if p == "FakeSub":
                    h_totalbkg.Add(h1, -1)
                    hist.Add(h1, -1)
                else:
                    h_totalbkg.Add(h1)
                    hist.Add(h1)
                rootfile.Close()
            #hist.SetFillColor(Color[sample])
            hist.SetFillColor(0)
            hist.SetLineColor(Color[sample])
            hist.SetFillStyle(Style[sample])
            hist.SetMarkerStyle(1)
            hists.append(hist)
            legend.AddEntry(hist,sample,"l")
                 
        
    inputfile.Close()
     
    return hists, h_totalsig, h_totalbkg, legend

def createTotalMCErr(h1, POI):
    h2 = h1.Clone("h2")
    h2.Sumw2()
    nbins = h2.GetNbinsX()

    # Adjust y-axis settings
    y = h2.GetYaxis()
    y.SetTitle("S/#sqrt{B}")
    y.SetTitleSize(25)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.55)
    y.SetLabelFont(43)
    y.SetLabelSize(20)

    # Adjust x-axis settings
    x = h2.GetXaxis()
    x.SetTitle(POI)
    x.SetTitleSize(25)
    x.SetTitleFont(43)
    x.SetTitleOffset(3.0)
    x.SetLabelFont(43)
    x.SetLabelSize(20)

    return h2

def createRatio(h1, h2):
    h3 = h1.Clone("h3")
    h3.SetLineColor(kBlack)
    h3.SetMarkerStyle(20)
    h3.SetTitle("")
    #h3.SetMinimum(0.8)
    #h3.SetMaximum(1.35)
    # Set up plot for markers and errors
    h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)
    
    # Adjust y-axis settings
    y = h3.GetYaxis()
    y.SetTitle("S/#sqrt{B}")
    y.CenterTitle()
    y.SetNdivisions(505)
    y.SetTitleSize(25)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.55)
    y.SetLabelFont(43)
    y.SetLabelSize(20)

    # Adjust x-axis settings
    x = h3.GetXaxis()
    x.SetTitle(POI)
    x.SetTitleSize(25)
    x.SetTitleFont(43)
    x.SetTitleOffset(3.0)
    x.SetLabelFont(43)
    x.SetLabelSize(20)


    return h3

def createSqrt(h1):
    h2 = h1.Clone("h2")
    h2.SetLineColor(kBlack)
    h2.SetMarkerStyle(20)
    h2.SetTitle("")
    #h2.SetMinimum(0.8)
    #h2.SetMaximum(1.35)
    # Set up plot for markers and errors
    h2.Sumw2()
    h2.SetStats(0)
    nbins = h2.GetNbinsX()
    for b in range(nbins+1):
        BinContent = h2.GetBinContent(b)
        BinContentErr = h2.GetBinError(b)
        #print "Bin "+str(b)+" BinContent "+str(BinContent)+" BinContentErr "+str(BinContentErr)
        BinValue = 0
        if BinContent > 0: 
            BinValue = math.sqrt(BinContent)
            h2.SetBinContent(b,BinValue)
            h2.SetBinError(b,BinContentErr/(2*BinValue))
        else: 
            h2.SetBinContent(b,0)
            h2.SetBinError(b,0)
    return h2

def createCanvasPads():
    c = TCanvas("c", "canvas", 800, 800)
    # Upper histogram plot is pad1
    pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0)  # joins upper and lower plot
    pad1.SetTicks(0,1) 
    pad1.Draw()
    # Lower ratio plot is pad2
    c.cd()  # returns to main canvas before defining pad2
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
    pad2.SetTopMargin(0)  # joins upper and lower plot
    pad2.SetBottomMargin(0.25)
    pad2.SetTicks(0,1) 
    #pad2.SetGridx()
    pad2.Draw()

    return c, pad1, pad2



def plotHists():
    
    # create required parts
    hists, h_totalsig, h_totalbkg, leg = readHists()
    h_sqrtB = createSqrt(h_totalbkg)
    h_MCerr = createTotalMCErr(h_sqrtB, POI)
    h_ratio = createRatio(h_totalsig, h_sqrtB)
    c, pad1, pad2 = createCanvasPads()
    
    # draw everything
    
    pad1.cd()
    maximum=0
    for hist in hists:
        if NORM ==1:
            hist.Scale(1./hist.Integral())
        if hist.GetMaximum()>maximum: maximum = hist.GetMaximum()
    upperbound = 2.*maximum
    lowerbound = -maximum/40.
    for i  in range(len(hists)):
        hist = hists[i]
        if i ==0:
            hist.SetMinimum(lowerbound)
            hist.SetMaximum(upperbound)
            # Adjust y-axis settings
            y = hist.GetYaxis()
            if NORM==1:
                y.SetTitle("Unit ")
            else:
                y.SetTitle("Events ")
            y.SetTitleSize(25)
            y.SetTitleFont(43)
            y.SetTitleOffset(1.55)
            y.SetLabelFont(43)
            y.SetLabelSize(20)
            hist.Draw("HIST")
        else:
            hist.Draw("HISTsame")
    
    leg.Draw("same")
    
    
    # to avoid clipping the bottom zero, redraw a small axis
    
    #axis = TGaxis(-5, 20, -5, 220, 20, 220, 510, "")
    #axis.SetLabelFont(43)
    #axis.SetLabelSize(15)
    #axis.Draw()
    
    pad2.cd()
    h_ratio.SetMinimum(0.)
    h_ratio.SetMaximum(6.)
    h_ratio.Draw("ep")
  
    c.SaveAs(outputDir+"/"+SubCat+"_"+POI+"_"+region+"_"+SPLIT+"_SigVsBkg.png") 
    # To hold window open when running from command line
    if OPEN==1: text = raw_input()

# Draw all canvases 
if __name__ == "__main__":
    plotHists()

