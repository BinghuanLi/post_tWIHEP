
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
# This program is modified to produce pre-fit StackPlots and Data/MC comparison and the yield table
# The script takes the output of mvaTool.C
# python stackplot.py -r <region> -p <POI> -o <plotOpen> -d<dir> -l<LATEX> -b<blind> -c<category> -s<SPLIT> 
# python stackplot.py -r 2lss -p Bin2l -l 1 -b 1 -c SubCat2l
# 4 March 2019   Binghuan Li
# *** 
#

import sys, os, subprocess
import optparse
import distutils.util
import math
import ROOT
from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TString, TFile, TH1, THStack, gROOT, TStyle, TAttFill, TLegend, TGraphAsymmErrors
from ROOT import kBlack, kBlue, kRed, kCyan, kViolet, kGreen, kOrange, kGray, kPink

usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-r', '--region',        dest='region'  ,      help='region to plot: 2lss or ttWctrl',      default='2lss',        type='string')
parser.add_option('-b', '--blind',        dest='blind'  ,      help='to plot data(0) or not(1)',      default='1',        type='int')
parser.add_option('-p', '--parameter',        dest='POI'  ,      help='parameter of interest',      default='Bin2l',        type='string')
parser.add_option('-c', '--category',        dest='SubCat'  ,      help='categorization',      default='SubCat2l',        type='string')
parser.add_option('-o', '--open',        dest='OPEN'  ,      help='to hold plot open(1) or not(0)',      default='0',        type='int')
parser.add_option('-d', '--dir',        dest='DirOfRootplas'  ,      help='input file full path',      default='/home/binghuan/Work/RootTestFiles/TTHLep_2019/data/2019Rootplas/rootplas_20190227/Output/',        type='string')
parser.add_option('-l', '--latex',        dest='LATEX'  ,      help='to print latex(1) or not(0)',      default='0',        type='int')
parser.add_option('-s', '--split',        dest='SPLIT'  ,      help='to produce plot in subgategory',      default='inclusive',        type='string')

(opt, args) = parser.parse_args()
POI = opt.POI
region = opt.region
OPEN = opt.OPEN
LATEX = opt.LATEX
DirOfRootplas = opt.DirOfRootplas
SubCat = opt.SubCat
SPLIT = opt.SPLIT
blind = opt.blind

#header_postfix = "2lss l^{#pm}l^{#pm} "
header_postfix = " 2lss "
if region =="ttWctrl": header_postfix = " ttWctrl "

Expected = "expected" 
if blind !=1 : Expected = "observed"

Samples=["TTH","H","TTW+TTWW","TTZ","EWK","Rares","Conv","Fakes","Flips","Data"]
Process={
    "TTH":["TTH_hww","TTH_hzz","TTH_htt","TTH_hmm","TTH_hot"],
    "H":["THW_hww","THW_hzz","THW_htt","THQ_hww","THQ_hzz","THQ_htt"],
    "TTZ":["TTZ"],"TTW+TTWW":["TTW","TTWW"],"Conv":["Conv"],"EWK":["EWK"],"Rares":["Rares"],"Fakes":["Fakes","FakeSub"],"Flips":["Flips"],"Data":["Data"]
    }
Color={"TTH":kRed,"H":kPink,"TTZ":kGreen,"TTW+TTWW":kGreen+3,"Conv":kOrange,"EWK":kViolet,"Rares":kCyan,"Fakes":kBlack,"Flips":kBlack}
Style={"TTH":1001,"H":1001,"TTZ":1001,"TTW+TTWW":1001,"Conv":1001,"EWK":1001,"Rares":1001,"Fakes":3005,"Flips":3006}

subCats={
"SubCat2l":["inclusive","ee_neg","ee_pos", "em_bl_neg","em_bl_pos","em_bt_neg","em_bt_pos", "mm_bl_neg","mm_bl_pos","mm_bt_neg","mm_bt_pos" ],
"DNNCat":["ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNCat_option2":["ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNCat_option3":["ttHnode","ttJnode","ttWnode","ttZnode"],
}

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
    h3.SetMinimum(0.8)
    h3.SetMaximum(1.35)
    # Set up plot for markers and errors
    h3.Sumw2()
    h3.SetStats(0)
    h3.Add(h2)

    return h3


def readHists():
    hstack = THStack("hstack","hstack")
    hstack.SetTitle("#scale[0.9]{#font[22]{CMS} #font[12]{Preliminary}                                                              41.53 fb^{-1}(13TeV)}")
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
    h_totalbkg.SetMinimum(0.8)
    h_totalbkg.SetMaximum(1.35)
    h_totalbkg.Sumw2()
    h_totalbkg.SetStats(0)
            
    h_totalsig = h0.Clone("h_totalsig")
    h_totalsig.SetDirectory(0)
    h_totalsig.Reset()
    h_totalsig.SetMarkerStyle(20)

    h_totalmc = h0.Clone("h_totalmc")
    h_totalmc.SetDirectory(0)
    h_totalmc.Reset()
    h_totalmc.SetLineColor(kBlack)
    h_totalmc.SetFillColor(kGray+3)
    h_totalmc.SetFillStyle(3001)
    h_totalmc.SetTitle("")
    h_totalmc.SetMinimum(0.8)
    h_totalmc.SetMaximum(1.35)
    h_totalmc.Sumw2()
    h_totalmc.SetStats(0)

    h_dataobs = h0.Clone("h_dataobs")
    h_dataobs.SetDirectory(0)
    h_dataobs.Reset()
    h_dataobs.SetMarkerStyle(20)

    latexString =""
    expString =" SM Exp"
    dataString =" Data Obs"
    latexString += ("\\begin{frame}\n\\frametitle{"+POI.replace("_","\_")+"}\n\\begin{table}[]\n\scalebox{0.8}{\n\\begin{tabular}{"+"l"*(1+len(Channels))+"}\n")
    latexString += ("& "+SPLIT.replace("_","\_")+" \\\\ \n")

    legend = TLegend(0.2,0.6,0.8,0.88)
    #legend.SetHeader("2017 "+fit_type+", 2lss l^{#pm}l^{#pm} #mu(ttH)=#hat#mu")
    legend.SetHeader("2017 prefit, "+header_postfix)
    legend.SetNColumns(3)
    legend.SetBorderSize(0)

    Samples.reverse()
    for sample in Samples:
        hist=h_totalsig.Clone(sample)
        hist.Reset()
        if not sample == "Data" : latexString += sample + " &"
        # loop over data
        if sample == "Data" or sample == "data":
            for p in Process[sample]:
                rootfile  = read_rootfile(p)
                gROOT.cd()
                h1 = rootfile.Get(POI+"_"+p)
                #h1.SetDirectory(0)
                h_dataobs.Add(h1)
                rootfile.Close()
        # loop over mc
        # loop over signal
        elif "TTH" in sample:
            for p in Process[sample]:
                rootfile  = read_rootfile(p)
                gROOT.cd()
                h1 = rootfile.Get(POI+"_"+p)
                #h1.SetDirectory(0)
                h_totalsig.Add(h1)
                h_totalmc.Add(h1)
                hist.Add(h1)
                rootfile.Close()
            hist.SetFillColor(Color[sample])
            hist.SetLineColor(kBlack)
            hist.SetFillStyle(Style[sample])
            if hist.Integral()>0.05:
                error = ROOT.Double(0)
                hist.IntegralAndError(0,hist.GetNbinsX(),error)
                latexString += "$ "+str(round(hist.Integral(),2))+" \\pm "+str(round(error,2))+"$ \\\\ \n"
            elif hist.Integral()>0:
                latexString += "  \\textless{}0.05 \\\\ \n"
            else: latexString += " - \\\\ \n "
            hstack.Add(hist)
            legend.AddEntry(hist,sample,"f")
        # loop over bkg
        else:
            for p in Process[sample]:
                rootfile  = read_rootfile(p)
                gROOT.cd()
                #print " try to get histogram : " + POI+"_"+p
                h1 = rootfile.Get(POI+"_"+p)
                h1.SetDirectory(0)
                if p == "FakeSub" and sample == "Fakes":
                    h_totalbkg.Add(h1, -1)
                    h_totalmc.Add(h1, -1)
                    hist.Add(h1, -1)
                else:
                    h_totalbkg.Add(h1)
                    h_totalmc.Add(h1)
                    hist.Add(h1)
                rootfile.Close()
            hist.SetFillColor(Color[sample])
            hist.SetLineColor(kBlack)
            hist.SetFillStyle(Style[sample])
            if hist.Integral()>0.05:
                error = ROOT.Double(0)
                hist.IntegralAndError(0,hist.GetNbinsX(),error)
                latexString += "$ "+str(round(hist.Integral(),2))+" \\pm "+str(round(error,2))+"$ \\\\ \n"
            elif hist.Integral()>0:
                latexString += "  \\textless{}0.05 \\\\ \n"
            else: latexString += " - "
            hstack.Add(hist)
            legend.AddEntry(hist,sample,"f")
                 
        

    totMC_error = ROOT.Double(0)
    h_totalmc.IntegralAndError(0,h_totalmc.GetNbinsX(),totMC_error)
    expString += "  &  $ "+str(round(h_totalmc.Integral(),2))+" \\pm "+str(round(totMC_error,2))+"$ \\\\ \n"
    
    totbkg_error = ROOT.Double(0)
    h_totalbkg.IntegralAndError(0,h_totalbkg.GetNbinsX(),totbkg_error)
    expString += "Tot Bkg  &  $ "+str(round(h_totalbkg.Integral(),2))+" \\pm "+str(round(totbkg_error,2))+"$ \\\\ \n"
    
    totdata_error = ROOT.Double(0)
    h_dataobs.IntegralAndError(0,h_dataobs.GetNbinsX(),totdata_error)
    dataString += "  &  $ "+str(round(h_dataobs.Integral(),2))+" \\pm "+str(round(totdata_error,2))+"$ \n"
    
    if not blind == 1: latexString += (expString + dataString)
    else : latexString += expString
    latexString += ("\\end{tabular}\n}\n\\end{table}\n\\end{frame}\n \\end{document}\n")
    if LATEX==1 : 
        latexfile = file(outputDir+"/"+POI+"_"+Expected+"_yield.tex","w")
        latexfile.write("\\documentclass{beamer}\n\\usetheme{Warsaw}\n\n\\usepackage{graphicx}\n\\useoutertheme{infolines}\n\\setbeamertemplate{headline}{}\n\n\\begin{document}\n\n")
        latexfile.write(latexString)

    inputfile.Close()
     
    return h_totalsig, h_totalbkg, h_totalmc, h_dataobs, hstack, legend

def createTotalMCErr(h1, POI):
    h2 = h1.Clone("h2")
    h2.Sumw2()
    nbins = h2.GetNbinsX()
    for b in range(nbins+1):
        BinContent = h2.GetBinContent(b)
        BinContentErr = h2.GetBinError(b)
        #print "Bin "+str(b)+" BinContent "+str(BinContent)+" BinContentErr "+str(BinContentErr)
        h2.SetBinContent(b,1)
        if BinContent != 0 : h2.SetBinError(b,BinContentErr/BinContent)
        else: h2.SetBinError(b,0)

    # Adjust y-axis settings
    y = h2.GetYaxis()
    if blind==1 :
        y.SetTitle("Sig/Bkg. ")
    else:
        y.SetTitle("Data/pred. ")
    y.CenterTitle()
    y.SetNdivisions(505)
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
    h3.SetMinimum(0.8)
    h3.SetMaximum(1.35)
    # Set up plot for markers and errors
    h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)

    return h3


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



def stackplot():
    
    # create required parts
    h_totalsig, h_totalbkg, h_TotalMC, h_dataobs, hstack, leg = readHists()
    if blind ==1 :
        h_MCerr = createTotalMCErr(h_totalbkg, POI)
        h_ratio = createRatio(h_totalsig, h_totalbkg)
    else:
        h_MCerr = createTotalMCErr(h_TotalMC, POI)
        h_ratio = createRatio(h_dataobs, h_TotalMC)
    c, pad1, pad2 = createCanvasPads()
    if not blind ==1 :
        leg.AddEntry(h_dataobs,"observed","lep")
    leg.AddEntry(h_TotalMC,"Uncertainty","f")
    
    # draw everything
    
    pad1.cd()
    maximum = h_dataobs.GetMaximum()
    upperbound = 2.*maximum
    lowerbound = -maximum/40.
    hstack.SetMinimum(lowerbound)
    hstack.SetMaximum(upperbound)
    hstack.Draw("HISTY") 
    # Adjust y-axis settings
    y = hstack.GetYaxis()
    y.SetTitle("Events ")
    y.SetTitleSize(25)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.55)
    y.SetLabelFont(43)
    y.SetLabelSize(20)
    
    
    h_TotalMC.Draw("e2same")
    if blind !=1:
        h_dataobs.Draw("same")
    leg.Draw("same")
    
    
    # to avoid clipping the bottom zero, redraw a small axis
    
    #axis = TGaxis(-5, 20, -5, 220, 20, 220, 510, "")
    #axis.SetLabelFont(43)
    #axis.SetLabelSize(15)
    #axis.Draw()
    
    pad2.cd()
    if blind ==1 :
        h_MCerr.SetMinimum(0.)
        h_MCerr.SetMaximum(1.)
    else:
        h_MCerr.SetMinimum(0.5)
        h_MCerr.SetMaximum(1.8)
    h_MCerr.Draw("e2") 
    h_ratio.Draw("epsame")
  
    c.SaveAs(outputDir+"/"+POI+"_"+Expected+".png") 
    # To hold window open when running from command line
    if OPEN==1: text = raw_input()

# Draw all canvases 
if __name__ == "__main__":
    stackplot()

