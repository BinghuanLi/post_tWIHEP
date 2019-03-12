
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
# This program is modified to produce post-fit/pre-fit StackPlots and Data/MC comparison and the yield table
# The script takes the output of CombineTool
# python ratioplot.py -f <fittype> -r <region> -p <POI> -o <plotOpen> -d<dir> -l<LATEX> -b<blind> -c<category> -s<SPLIT>
# python ratioplot.py -f prefit -r 2lss -p Bin2l -l 1 -b 1 -c SubCat2l -s ee_neg
# 12 Sep 2018   Binghuan Li
# *** 
#

import os
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
parser.add_option('-f', '--fit',        dest='fit_type'  ,      help='prefit/fit_b or fit_s',      default='prefit',        type='string')
parser.add_option('-r', '--region',        dest='region'  ,      help='region to plot: 2lss or ttWctrl',      default='2lss',        type='string')
parser.add_option('-b', '--blind',        dest='blind'  ,      help='to plot data(0) or not(1)',      default='1',        type='int')
parser.add_option('-p', '--parameter',        dest='POI'  ,      help='parameter of interest',      default='Bin2l',        type='string')
parser.add_option('-c', '--category',        dest='SubCat'  ,      help='categorization',      default='SubCat2l',        type='string')
parser.add_option('-o', '--open',        dest='OPEN'  ,      help='to hold plot open(1) or not(0)',      default='0',        type='int')
parser.add_option('-d', '--dir',        dest='DirOfRootplas'  ,      help='input file full path',      default='/home/binghuan/Work/RootTestFiles/TTHLep_2019/data/2019Rootplas/rootplas_20190227/V0227_datacards/',        type='string')
parser.add_option('-l', '--latex',        dest='LATEX'  ,      help='to print latex(1) or not(0)',      default='0',        type='int')
parser.add_option('-s', '--split',        dest='SPLIT'  ,      help='to produce plot in subgategory',      default='inclusive',        type='string')

(opt, args) = parser.parse_args()
POI = opt.POI
region = opt.region
fit_type = opt.fit_type
OPEN = opt.OPEN
LATEX = opt.LATEX
DirOfRootplas = opt.DirOfRootplas
SubCat = opt.SubCat
SPLIT = opt.SPLIT
blind = opt.blind

#header_postfix = "2lss l^{#pm}l^{#pm} "
header_postfix = "2lss "
if region =="ttWctrl": header_postfix = " ttWctrl "
    
Expected = "expected" 
if blind !=1 : Expected = "observed"


Samples=["TTH","H","TTW+TTWW","TTZ","EWK","Rares","Conv","Fakes","Flips"]
Process={
    "TTH":["TTH_hww","TTH_hzz","TTH_htt","TTH_hmm","TTH_hot"],
    "H":["THW_hww","THW_hzz","THW_htt","THQ_hww","THQ_hzz","THQ_htt"],
    "TTZ":["TTZ"],"TTW+TTWW":["TTW","TTWW"],"Conv":["Conv"],"EWK":["EWK"],"Rares":["Rares"],"Fakes":["Fakes"],"Flips":["Flips"]
    }
Color={"TTH":kRed,"H":kPink,"TTZ":kGreen,"TTW+TTWW":kGreen+3,"Conv":kOrange,"EWK":kViolet,"Rares":kCyan,"Fakes":kBlack,"Flips":kBlack}
Style={"TTH":1001,"H":1001,"TTZ":1001,"TTW+TTWW":1001,"Conv":1001,"EWK":1001,"Rares":1001,"Fakes":3005,"Flips":3006}

subCats={
"SubCat2l":["ee_neg","ee_pos", "em_bl_neg","em_bl_pos","em_bt_neg","em_bt_pos", "mm_bl_neg","mm_bl_pos","mm_bt_neg","mm_bt_pos" ],
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

Channels = []
if not subCats.has_key(SubCat):
    print ("ERROR : " + SubCat +"is not a key of subCats ")
    os._exit()
elif SPLIT=="inclusive":
    Channels = subCats[SubCat]
    print (" Plot all channels ")
elif SPLIT not in subCats[SubCat]:
    print ("ERROR : " + SPLIT +"is not channel of "+SubCat)
    os._exit()
else:
    Channels = [SPLIT]
    header_postfix += "," + SPLIT.replace("_","\_") 
    print (" Plot channel "+SPLIT)


def read_rootfile(samplename=""):
    ''' read a root file '''
    fullfilename = DirOfRootplas+SubCat+"/"+POI+"/fitDiagnostics"+samplename+".root"
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


def readHists(postfix=""):
    hstack = THStack("hstack","hstack")
    hstack.SetTitle("#scale[0.9]{#font[22]{CMS} #font[12]{Preliminary}                                                              41.53 fb^{-1}(13TeV)}")
    inputfile  = read_rootfile(postfix)
    gROOT.cd()
    dirName = "ttH_"+region+"_"+Channels[0]
    h0 = inputfile.Get("shapes_"+fit_type+"/"+dirName+"/total")
    h_totalbkg = h0.Clone("h_totalbkg")
    h_totalbkg.SetDirectory(0)
    h_totalbkg.Reset()
            
    h_totalsig = h0.Clone("h_totalsig")
    h_totalsig.SetDirectory(0)
    h_totalsig.Reset()

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
    latexString += ("\\begin{frame}\n\\frametitle{"+POI.replace("_","\_")+" "+fit_type.replace("_","\_")+"}\n\\begin{table}[]\n\scalebox{0.38}{\n\\begin{tabular}{"+"l"*(2+len(Channels))+"}\n")
    for channel in Channels:
        FitDir = inputfile.Get("shapes_"+fit_type)
        directory = "shapes_"+fit_type+"/ttH_"+region+"_"+channel+"/" 
        SkipChannel = False
        if not FitDir.GetListOfKeys().Contains("ttH_"+region+"_"+channel):
            print " skip " + directory
            SkipChannel = True
        else:
            h_bkg = inputfile.Get(directory+"total_background").Clone(directory+"total_background")
            h_totalbkg.Add(h_bkg)
             
            h_sig = inputfile.Get(directory+"total_signal").Clone(directory+"total_signal")
            h_totalsig.Add(h_sig)
        
            h_total = inputfile.Get(directory+"total").Clone(directory+"total")
            h_totalmc.Add(h_total)
        
            g_data = inputfile.Get(directory+"data").Clone(directory+"data")
            h_data = h_total.Clone("h_data")
            h_data.Reset()
            TGraphToTH1(h_data, g_data)
            h_dataobs.Add(h_data)
       
        if not SkipChannel:
            SM_error = ROOT.Double(0)
            h_total.IntegralAndError(0,h_total.GetNbinsX(),SM_error)
            expString += "  &  $ "+str(round(h_total.Integral(),2))+" \\pm "+str(round(SM_error,2))+"$"
        
            data_error = ROOT.Double(0)
            h_data.IntegralAndError(0,h_data.GetNbinsX(),data_error)
            dataString += "  &  $ "+str(round(h_data.Integral(),2))+" \\pm "+str(round(data_error,2))+"$"
        else:
            expString += "  &  - "
            dataString += "  &  - "
        
         
        latexString += ("& "+channel.replace("_","\_")+"   ")

    totMC_error = ROOT.Double(0)
    h_totalmc.IntegralAndError(0,h_totalmc.GetNbinsX(),totMC_error)
    expString += "  &  $ "+str(round(h_totalmc.Integral(),2))+" \\pm "+str(round(totMC_error,2))+"$ \\\\ \n"
    
    totdata_error = ROOT.Double(0)
    h_dataobs.IntegralAndError(0,h_dataobs.GetNbinsX(),totdata_error)
    dataString += "  &  $ "+str(round(h_dataobs.Integral(),2))+" \\pm "+str(round(totdata_error,2))+"$ \n"
    
    latexString += "& total "+ region +" \\\\ \n"

    legend = TLegend(0.2,0.6,0.8,0.88)
    #legend.SetHeader("2017 "+fit_type+", 2lss l^{#pm}l^{#pm} #mu(ttH)=#hat#mu")
    legend.SetHeader("2017 "+fit_type+", "+header_postfix)
    legend.SetNColumns(3)
    legend.SetBorderSize(0)

    Samples.reverse()
    for sample in Samples:
        hist=h_totalsig.Clone(sample)
        hist.Reset()
        latexString += sample
        for channel in Channels:
            h_sample =hist.Clone(sample+"_sample")
            h_sample.Reset()
            latexString += "    & "
            for p in Process[sample]:
                histname = "shapes_"+fit_type+"/ttH_"+region+"_"+channel+"/"+p 
                h1 = inputfile.Get(histname)
                if h1:
                    #print h1.Integral()
                    hist.Add(h1)
                    h_sample.Add(h1)
            if h_sample.Integral()>0.05:
                error = ROOT.Double(0)
                h_sample.IntegralAndError(0,h_sample.GetNbinsX(),error)
                latexString += "$ "+str(round(h_sample.Integral(),2))+" \\pm "+str(round(error,2))+"$"
            elif h_sample.Integral()>0:
                latexString += "  \\textless{}0.05"
            else: latexString += " - "
                 
        if hist.Integral()>0: 
            hist.SetDirectory(0)
            hist.SetFillColor(Color[sample])
            hist.SetLineColor(kBlack)
            hist.SetFillStyle(Style[sample])
            hstack.Add(hist)
            legend.AddEntry(hist,sample,"f")
            if hist.Integral()>0.05:
                IntegralError = ROOT.Double(0)
                hist.IntegralAndError(0,hist.GetNbinsX(),IntegralError)
                latexString += "    & $ "+str(round(hist.Integral(),2))+" \\pm "+str(round(IntegralError,2))+" $ \\\\ \n"
            else:
                latexString += "    & \\textless{}0.05 \\\\ \n"
        else: latexString += " & - \\\\ \n"

    latexString += (expString + dataString)
    latexString += ("\\end{tabular}\n}\n\\end{table}\n\\end{frame}\n \\end{document}\n")
    if LATEX==1 : 
        latexfile = file(DirOfRootplas+SubCat+"/"+POI+"/"+SubCat+"_"+POI+"_"+region+"_"+fit_type+"_"+SPLIT+"_"+Expected+"_yield.tex","w")
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



def ratioplot():
    
    # create required parts
    h_totalsig, h_totalbkg, h_TotalMC, h_dataobs, hstack, leg = readHists()
    h_ratio = createRatio(h_dataobs, h_TotalMC)
    h_MCerr = createTotalMCErr(h_TotalMC, POI)
    c, pad1, pad2 = createCanvasPads()
    leg.AddEntry(h_dataobs,Expected,"lep")
    leg.AddEntry(h_TotalMC,"Uncertainty","f")
    
    # draw everything
    
    pad1.cd()
    maximum = h_dataobs.GetMaximum()
    upperbound = 2.3*maximum
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
    h_dataobs.Draw("same")
    leg.Draw("same")
    
    
    # to avoid clipping the bottom zero, redraw a small axis
    
    #axis = TGaxis(-5, 20, -5, 220, 20, 220, 510, "")
    #axis.SetLabelFont(43)
    #axis.SetLabelSize(15)
    #axis.Draw()
    
    pad2.cd()
    h_MCerr.SetMinimum(0.5)
    h_MCerr.SetMaximum(1.8)
    h_MCerr.Draw("e2") 
    h_ratio.Draw("epsame")
  
    c.SaveAs(DirOfRootplas+SubCat+"/"+POI+"/"+SubCat+"_"+POI+"_"+region+"_"+fit_type+"_"+SPLIT+"_"+Expected+".png") 
    # To hold window open when running from command line
    if OPEN==1: text = raw_input()

# Draw all canvases 
if __name__ == "__main__":
    ratioplot()

