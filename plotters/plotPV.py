import sys
import argparse
import os
from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TString, TFile, TH1, THStack, gROOT, TStyle, TAttFill, TLegend, TGraphAsymmErrors, TLine, gStyle
from ROOT import kBlack, kBlue, kRed, kCyan, kViolet, kGreen, kOrange, kGray, kPink, kTRUE

gROOT.SetBatch(1)

######### to run #########
#### python make_overlay.py --createROOTfile -y 2016 -i -o 
##########################

#### start  user defined variables


# options
usage = 'usage: %prog [options]'
parser = argparse.ArgumentParser(usage)
parser.add_argument('-y', '--year', nargs='?', help = 'year to plot -1 to compare TR in three years ', const=18, type=int ,default=18)
parser.add_argument('-i', '--inputDir', nargs='?', help = 'inputDir', const="/home/binghuan/Work/TTHLep/TTHLep_RunII/data_to_mc_corrections/weights/ttH2018/", default="/home/binghuan/Work/TTHLep/TTHLep_RunII/data_to_mc_corrections/weights/ttH2018/")
parser.add_argument('-o', '--outputDir', nargs='?', help = 'outputDir', const="/home/binghuan/Work/TTHLep/TTHLep_RunII/data_to_mc_corrections/plots/PV/", default="/home/binghuan/Work/TTHLep/TTHLep_RunII/data_to_mc_corrections/plots/PV/")
parser.add_argument('--createROOTfile',        dest='createROOTfile'  ,      help='create or not the root files containing all the hist, must be true for the first time you run a given region',  action='store_true')

args = parser.parse_args()
year = args.year
inputDirectories = args.inputDir
outputdir = args.outputDir
createROOTfile = args.createROOTfile

fileName = "PU_data_MC_2018.root"
if year ==17:
    inputDirectories = "/home/binghuan/Work/TTHLep/TTHLep_RunII/data_to_mc_corrections/weights/ttH2017/"
    fileName = "PU_data_MC_2017.root"
elif year ==16:
    inputDirectories = "/home/binghuan/Work/TTHLep/TTHLep_RunII/data_to_mc_corrections/weights/ttH2016/"
    fileName = "PU_data_MC_2016.root"


#samples = ["data","ttH","ttW","ttZ","W3Jets"]
#Color={"data":kBlack,"ttH":kRed,"ttW":kGreen,"ttZ":kBlue,"W3Jets":kViolet}
#Style={"data":1,"ttH":1,"ttW":1,"ttZ":1,"W3Jets":1}
samples = ["xs = 69.2 mb","xs = 72.4 mb","xs = 66.0 mb"]
Color={"xs = 69.2 mb":kBlack,"xs = 72.4 mb":kRed,"xs = 66.0 mb":kBlue}
Style={"xs = 69.2 mb":1,"xs = 72.4 mb":1,"xs = 66.0 mb":1}
sampleName = {
"xs = 69.2 mb":"pileup","xs = 72.4 mb":"pileup_plus","xs = 66.0 mb":"pileup_minus"
#2016
#"data":"pileup","ttH":"Legacy16V2_ttHnobb","ttW":"Legacy16V2_TTWJets","ttZ":"Legacy16V2_TTZ_M10_ext1","W3Jets":"Legacy16V2_W3JetsToLNu_ext"
#2017
#"data":"pileup","ttH":"Legacy17V2_ttHnobb","ttW":"Legacy17V2_TTWJets","ttZ":"Legacy17V2_TTZ_M10","W3Jets":"Legacy17V2_W3JetsToLNu"
#2018
#"data":"pileup","ttH":"Legacy18V2_ttHToNonbb","ttW":"Legacy18V2_TTWJets","ttZ":"Legacy18V2_TTZ_M10","W3Jets":"Legacy18V2_W3JetsToLNu"
}

# lumi information
luminosity = {16: 35.92 , 17: 41.53  , 18: 59.74}

plotname = "uncert_pileup_20%i"%(year)
#plotname = "compr_pileup_20%i"%(year)
fileName = inputDirectories + fileName

# options
normalization = True # Normalize to unit
showStats = False
UseLogY = False


##### end user defined variables
# check outputdir
if not os.path.exists(outputdir):
    print ('mkdir: ', outputdir)
    os.makedirs(outputdir)

def createRatio(h1, h2, c, style, POI, norm):
    if norm:
        h1.Scale(1./h1.Integral())
        h2.Scale(1./h2.Integral())
    h3 = h1.Clone("h3")
    h3.SetMarkerStyle(style)
    h3.SetLineColor(c)
    h3.SetFillColor(c)
    h3.SetTitle("")
    #h3.SetMinimum(0.8)
    #h3.SetMaximum(1.35)
    # Set up plot for markers and errors
    h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)
    
    # Adjust y-axis settings
    y = h3.GetYaxis()
    y.SetTitle("data/mc")
    y.CenterTitle()
    y.SetNdivisions(505)
    y.SetTitleSize(40)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.55)
    y.SetLabelFont(43)
    y.SetLabelSize(20)

    # Adjust x-axis settings
    x = h3.GetXaxis()
    x.SetTitle(POI)
    x.SetTitleSize(40)
    x.SetTitleFont(43)
    x.SetTitleOffset(3.0)
    x.SetLabelFont(43)
    x.SetLabelSize(20)


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


def plotSysts():
    inputfile = TFile(fileName,"read")
    if inputfile.IsZombie():
        print("inputfile is Zombie")
        sys.exit()
    # loop over features
    #for feature, values in features.items():
    # set up legend
    legend = TLegend(0.4,0.6,0.9,0.88)
    #legend.SetHeader("sample name")
    legend.SetHeader("minimum bias cross section")
    #legend.SetNColumns(3)
    legend.SetBorderSize(0)
            
    c, pad1, pad2 = createCanvasPads()

    # loop over samples
    hist_vars = []
    hist_ratio_vars = []
    i=0
    for sample in samples:
        if i ==0:
            # get nominal histograms
            hist_nom_name = sampleName[sample]
            if not inputfile.GetListOfKeys().Contains(hist_nom_name): 
                print ( "%s doesn't have histogram %s"%(fileName, hist_nom_name))
                continue
            hist_nom = inputfile.Get(hist_nom_name)
            hist_nom.SetFillColor(0)
            hist_nom.SetLineColor(Color[sample])
            hist_nom.SetMarkerColor(Color[sample])
            hist_nom.SetLineStyle(Style[sample])
            hist_nom.SetLineWidth(2)
            #h_ratio = createRatio(hist_nom, hist_nom, Color[sample], Style[sample], "vertex multiplicity",normalization)
            #h_ratio.SetMarkerColor(Color[sample])
            legend.AddEntry(hist_nom,sample,"l")
        else:    
            hist_name = sampleName[sample]
            if not inputfile.GetListOfKeys().Contains(hist_name): 
                print ( "%s doesn't have histogram %s"%(fileName, hist_name))
                continue
            hist_var = inputfile.Get(hist_name)
            hist_var.SetFillColor(0)
            hist_var.SetLineColor(Color[sample])
            hist_var.SetMarkerColor(Color[sample])
            hist_var.SetLineStyle(Style[sample])
            hist_var.SetLineWidth(2)
            hist_vars.append(hist_var)
            #h_ratio_var = createRatio(hist_nom, hist_var, Color[sample] , Style[sample],  "vertex multiplicity", normalization)
            #h_ratio_var.SetMarkerColor(Color[sample])
            #hist_ratio_vars.append(h_ratio_var)
            #legend.AddEntry(h_ratio_var,hist_name,"l")
            legend.AddEntry(hist_var,sample,"l")
            
        i = i+1     
    
    # draw everything

    #pad1.cd()
    #pad1.SetGridx()
    #pad1.SetGridy()
    c1 = TCanvas("c", "canvas", 800, 800)
    c1.SetLeftMargin(1.65)
    c1.SetBottomMargin(1.65)
    #c1.SetGridx()
    #c1.SetGridy()
    if UseLogY:
        c1.SetLogy()
    
    # set bounds
    Y_name = "Events"
    maximum=0
    
    for hist in hist_vars:
        if normalization:
            hist.Scale(1./hist.Integral())
        if hist.GetMaximum()>maximum: maximum = hist.GetMaximum()
    upperbound = 1.8*maximum
    lowerbound = -maximum/40.
    if UseLogY:
        upperbound = 10*maximum
        lowerbound = 0.0000001
    
    Y_name = "Events"
    if normalization:
        hist_nom.Scale(1./hist_nom.Integral())
        Y_name = " Prob. "
    if showStats:
        hist_nom.SetStats(1)
    else:    
        hist_nom.SetStats(0)
        
    hist_nom.SetTitle("#scale[1.0]{ 20%i at %.2f fb^{-1}(13TeV)}"%(year,luminosity[year]))
    hist_nom.SetMaximum(upperbound)
    hist_nom.SetMinimum(lowerbound)
    # Adjust y-axis settings
    y = hist_nom.GetYaxis()
    y.SetTitleFont(43)
    y.SetTitleOffset(0.8)
    y.SetLabelFont(43)
    y.SetLabelSize(20)
    y.SetTitle(Y_name) 
    y.SetTitleSize(40) 
    
    # Adjust x-axis settings
    x = hist_nom.GetXaxis()
    x.SetTitleFont(43)
    x.SetTitleOffset(0.8)
    x.SetLabelFont(43)
    x.SetLabelSize(20)
    x.SetTitle("vertex mulpliticy")
    x.SetTitleSize(40) 
    
    hist_nom.Draw("HIST")
    
    for hist in hist_vars:
        hist.Draw("HISTsame") 

    legend.Draw("same")

    '''    
    pad2.cd()
    pad2.SetGridx()
    pad2.SetGridy()
    bins = h_ratio.GetNbinsX()
    LowEdge = h_ratio.GetBinLowEdge(1)
    HighEdge = h_ratio.GetBinLowEdge(bins+1)
    line = TLine(LowEdge,1,HighEdge,1)
    line.SetLineColor(kBlack)
    for i in range(len(hist_ratio_vars)):
        if i==0:
            hist_ratio_vars[i].Draw("EP")
            hist_ratio_vars[i].SetMinimum(0.5)
            hist_ratio_vars[i].SetMaximum(1.5)
        else:
            hist_ratio_vars[i].Draw("EPsame")
    
    
    
    line.Draw("same")
    '''
    
    c1.SaveAs("%s%s_isNorm%s_overlay.png"%(outputdir,plotname,normalization))

# Draw all canvases 
if __name__ == "__main__":
    gStyle.SetLegendTextSize(0.04)
    plotSysts()
