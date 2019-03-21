
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
# This program is modified to produce pre-fit systematic shift plot and the syst table
# The script takes the output of createDatacard.py
# python plotSysts.py -r <region> -p <POI> -o <plotOpen> -d<dir> -l<LATEX> -b<blind> -c<category> -s<SPLIT> 
# python plotSysts.py -r 2lss -p Bin2l -l 1 -b 1 -c SubCat2l -s ee_neg
# 12 March 2019   Binghuan Li
# *** 
#

import sys, os, subprocess
import optparse
import distutils.util
import math
import ROOT
from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TString, TFile, TH1, THStack, gROOT, TStyle, TAttFill, TLegend, TGraphAsymmErrors, TLine
from ROOT import kBlack, kBlue, kRed, kCyan, kViolet, kGreen, kOrange, kGray, kPink, kTRUE
from ROOT import gROOT

gROOT.SetBatch(kTRUE)


usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-r', '--region',        dest='region'  ,      help='region to plot: 2lss or ttWctrl',      default='2lss',        type='string')
parser.add_option('-p', '--parameter',        dest='POI'  ,      help='parameter of interest',      default='Bin2l',        type='string')
parser.add_option('-c', '--category',        dest='SubCat'  ,      help='categorization',      default='SubCat2l',        type='string')
parser.add_option('-o', '--open',        dest='OPEN'  ,      help='to hold plot open(1) or not(0)',      default='0',        type='int')
parser.add_option('-d', '--dir',        dest='DirOfRootplas'  ,      help='input file full path',      default='/mnt/Sharing/TTHLep/TTHLep_2019/Talks/rootplasDNN_0307.1/fakeable/V0307.1_fakeable_datacards/',        type='string')
parser.add_option('-n', '--norm',        dest='NORM'  ,      help='norm to unit (1) or not(0)',      default='0',        type='int')
parser.add_option('-l', '--latex',        dest='LATEX'  ,      help='to print latex(1) or not(0)',      default='0',        type='int')
parser.add_option('-s', '--split',        dest='SPLIT'  ,      help='to produce plot in subgategory',      default='ee_neg',        type='string')

(opt, args) = parser.parse_args()
POI = opt.POI
region = opt.region
OPEN = opt.OPEN
NORM = opt.NORM
DirOfRootplas = opt.DirOfRootplas
SubCat = opt.SubCat
LATEX = opt.LATEX
SPLIT = opt.SPLIT

#header_postfix = "2lss l^{#pm}l^{#pm} "
header_postfix = " 2lss "
if region =="ttWctrl": header_postfix = " ttWctrl "

# currently, latex file works only for Samples.size() < =4

Samples=["TTH","TTW","TTZ","Fakes"]
Process={
    "TTH":["TTH_hww","TTH_hzz","TTH_htt","TTH_hmm","TTH_hot"],
    "H":["THW_hww","THW_hzz","THW_htt","THQ_hww","THQ_hzz","THQ_htt"],
    "TTZ":["TTZ"],"TTW":["TTW"],"TTW+TTWW":["TTW","TTWW"],"Conv":["Conv"],"EWK":["EWK"],"Rares":["Rares"],"Fakes":["Fakes"],"Flips":["Flips"]
    }
Color={"Nominal":kBlack,"SystUp":kRed,"SystDown":kBlue}
Style={"Nominal":1001,"SystUp":1001,"SystDown":1001}

# the nuisances to plot
#Nuisances =[
#"CMS_ttHl16_lepEff_muloose","CMS_ttHl16_lepEff_mutight","CMS_ttHl16_lepEff_elloose","CMS_ttHl16_lepEff_eltight","CMS_ttHl17_Clos_e_norm","CMS_ttHl17_Clos_m_norm","CMS_ttHl17_Clos_e_bt_norm","CMS_ttHl17_Clos_m_bt_norm",
#"CMS_ttHl17_trigger","CMS_ttHl17_btag_HFStats1","CMS_ttHl17_btag_HFStats2","CMS_ttHl16_btag_cErr1","CMS_ttHl16_btag_cErr2","CMS_ttHl16_btag_LF","CMS_ttHl16_btag_HF","CMS_ttHl_thu_shape_ttW","CMS_ttHl_thu_shape_ttH","CMS_ttHl_thu_shape_ttZ","CMS_scale_j","CMS_ttHl17_btag_LFStats1","CMS_ttHl17_btag_LFStats2",
#"CMS_ttHl16_FRm_norm","CMS_ttHl16_FRm_pt","CMS_ttHl16_FRm_be","CMS_ttHl16_FRe_norm","CMS_ttHl16_FRe_pt","CMS_ttHl16_FRe_be","CMS_ttHl17_Clos_e_shape","CMS_ttHl17_Clos_m_shape",
#"PU"
#]

Nuisances =[
"CMS_scale_j"
]

header_postfix += "," + SPLIT.replace("_","\_") 
print (" Plot channel "+SPLIT)

outputDir = DirOfRootplas+"SystPlots/"

if not os.path.exists(outputDir):
    os.popen("mkdir -p "+outputDir)

def read_rootfile():
    ''' read a root file '''
    fullfilename = DirOfRootplas+SubCat+"/"+POI+"/ttH_"+region+"_"+SPLIT+".root"
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


def readHists(SystName):
    inputfile  = read_rootfile() # assuming TTH_hww is always there 
    gROOT.cd()
    histName = "TTH_hww" 
    h0 = inputfile.Get(histName)
            
    h_nominal = h0.Clone("h_nominal")
    h_nominal.SetDirectory(0)
    h_nominal.Reset()
    h_nominal.SetMarkerStyle(1)

    
    hists= {}
    legends={}
     
    Samples.reverse()
    for sample in Samples:
        legend = TLegend(0.4,0.6,0.9,0.88)
        #legend.SetHeader("2017 "+fit_type+", 2lss l^{#pm}l^{#pm} #mu(ttH)=#hat#mu")
        legend.SetHeader("2017 prefit, "+header_postfix)
        #legend.SetNColumns(3)
        legend.SetBorderSize(0)
        hist=h_nominal.Clone(sample)
        hist.SetStats(0)
        hist.Reset()
        hist.SetTitle("#scale[0.9]{#font[22]{CMS} #font[12]{Preliminary}                                                              41.53 fb^{-1}(13TeV)}")
        hist_up=h_nominal.Clone(sample+"_"+SystName+"Up")
        hist_up.SetStats(0)
        hist_up.Reset()
        hist_down=h_nominal.Clone(sample+"_"+SystName+"Down")
        hist_down.SetStats(0)
        hist_down.Reset()
        for p in Process[sample]:
            rootfile  = read_rootfile()
            if rootfile.IsZombie():continue
            gROOT.cd()
            if not rootfile.GetListOfKeys().Contains(p+"_"+SystName+"Up"): continue
            h1 = rootfile.Get(p)
            h1_up = rootfile.Get(p+"_"+SystName+"Up")
            print ( " get "+p+"_"+SystName+"Up " )
            h1_down = rootfile.Get(p+"_"+SystName+"Down")
            hist.Add(h1)
            hist_up.Add(h1_up)
            hist_down.Add(h1_down)
            rootfile.Close()
        hist.SetFillColor(0)
        hist.SetLineColor(Color["Nominal"])
        hist.SetMarkerColor(Color["Nominal"])
        hist_up.SetFillColor(0)
        hist_up.SetLineColor(Color["SystUp"])
        hist_up.SetMarkerColor(Color["SystUp"])
        hist_down.SetFillColor(0)
        hist_down.SetLineColor(Color["SystDown"])
        hist_down.SetMarkerColor(Color["SystDown"])
        h_list=[]
        h_list.append(hist)
        h_list.append(hist_up)
        h_list.append(hist_down)
        hists[sample]=h_list
        legend.AddEntry(hist,sample,"l")
        legend.AddEntry(hist_up,sample+"_"+SystName+"Up","l")
        legend.AddEntry(hist_down,sample+"_"+SystName+"Down","l")
        legends[sample]=legend
        
    inputfile.Close()
    
    # hists = {"sampleName":[h_nominal, h_up, h_down]} 
    return hists, legends

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
    h3.SetMarkerStyle(1)
    h3.SetTitle("")
    #h3.SetMinimum(0.8)
    #h3.SetMaximum(1.35)
    # Set up plot for markers and errors
    h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)
    
    # Adjust y-axis settings
    y = h3.GetYaxis()
    y.SetTitle("var/nominal")
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



def plotSysts():
  latexString =""
  for SystName in Nuisances:  
    # create required parts
    hists, legs = readHists(SystName)
    plotNames = []
    for sample in Samples:
        if not hists.has_key(sample): continue
        h_nom = hists[sample][0]
        h_up = hists[sample][1]
        h_down = hists[sample][2]
        h_ratio = createRatio(h_nom, h_nom)
        h_ratio_up = createRatio(h_up, h_nom)
        h_ratio_down = createRatio(h_down, h_nom)
        c, pad1, pad2 = createCanvasPads()
    
        # draw everything
        
        pad1.cd()
        maximum=0
        for hist in hists[sample]:
            if NORM ==1:
                hist.Scale(1./hist.Integral())
            if hist.GetMaximum()>maximum: maximum = hist.GetMaximum()
        upperbound = 2.*maximum
        lowerbound = -maximum/40.
        for i  in range(len(hists[sample])):
            hist = hists[sample][i]
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
        
        legs[sample].Draw("same")
        
        
        # to avoid clipping the bottom zero, redraw a small axis
        
        #axis = TGaxis(-5, 20, -5, 220, 20, 220, 510, "")
        #axis.SetLabelFont(43)
        #axis.SetLabelSize(15)
        #axis.Draw()
        
        pad2.cd()
        pad2.SetGridy()
        bins = h_ratio.GetNbinsX()
        LowEdge = h_ratio.GetBinLowEdge(1)
        HighEdge = h_ratio.GetBinLowEdge(bins+1)
        line = TLine(LowEdge,1,HighEdge,1);
        h_ratio_up.SetMinimum(0.5)
        h_ratio_up.SetMaximum(1.5)
        h_ratio_up.Draw("hist")
        h_ratio_down.Draw("histsame")
        line.SetLineColor(kBlack)
        line.Draw("same")
      
        c.SaveAs(outputDir+"/"+SubCat+"_"+POI+"_"+region+"_"+SPLIT+"_"+sample+"_"+SystName+".png")
        plotNames.append(SubCat+"_"+POI+"_"+region+"_"+SPLIT+"_"+sample+"_"+SystName+".png") 
    # To hold window open when running from command line
    if OPEN==1: text = raw_input()
    latexString += ("\\begin{frame}\n\\frametitle{"+POI.replace("_","\_")+" "+SystName.replace("_","\_")+"}\n\\begin{columns}\n\\begin{column}{6cm}\n\\pgfimage[height=4cm, width = 6cm]{")
    latexString += (plotNames[0]+"}\\\\\n\\pgfimage[height=4cm, width = 6cm]{"+plotNames[1]+"}\n\\end{column}\n\\begin{column}{6cm}\n\\pgfimage[height=4cm, width = 6cm]{")
    latexString += (plotNames[2]+"}\\\\\n\\pgfimage[height=4cm, width = 6cm]{"+plotNames[3]+"}\n\\end{column}\n\\end{columns}\n\\end{frame}\n\n")
  if LATEX==1 : 
    latexfile = file(outputDir+"/"+SubCat+"_"+POI+"_"+region+"_"+SPLIT+"_Systematics.tex","w")
    latexfile.write("\\documentclass{beamer}\n\\usetheme{Warsaw}\n\n\\usepackage{graphicx}\n\\useoutertheme{infolines}\n\\setbeamertemplate{headline}{}\n\n\\begin{document}\n\n")
    latexfile.write(latexString)
    latexfile.write("\\end{document}\n")

  

# Draw all canvases 
if __name__ == "__main__":
    plotSysts()

