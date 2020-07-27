import sys
import os
from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TString, TFile, TH1, THStack, gROOT, TStyle, TAttFill, TLegend, TGraphAsymmErrors, TLine, gStyle
from ROOT import kBlack, kBlue, kRed, kCyan, kViolet, kGreen, kOrange, kGray, kPink, kTRUE

#### start  user defined variables

inputDirectories = "/home/binghuan/Work/TTHLep/TTHLep_RunII/ttH_hjtagger_xgboost/data/";
treename = "syncTree";
 
features={
#"Jet25_isToptag":{"nbin":2,"min":-0.5,"max":1.5,"cut":"EvtWeight * (n_presel_jet>=1)","xlabel":"Jet25_isToptag"},
"Jet25_bDiscriminator":{"nbin":20,"min":0.,"max":1.,"cut":"EvtWeight * (n_presel_jet>=1)","xlabel":"Jet25_bDiscriminator"},
"Jet25_pt":{"nbin":20,"min":0.,"max":500.,"cut":"EvtWeight * (n_presel_jet>=1)","xlabel":"Jet25_pt"},
#"Jet25_eta":{"nbin":20,"min":-2.5,"max":2.5,"cut":"EvtWeight * (n_presel_jet>=1)","xlabel":"Jet25_eta"},
#"Jet25_phi":{"nbin":20,"min":-3.5,"max":3.5,"cut":"EvtWeight * (n_presel_jet>=1)","xlabel":"Jet25_phi"},
#"Jet25_energy":{"nbin":20,"min":0.,"max":500,"cut":"EvtWeight * (n_presel_jet>=1)","xlabel":"Jet25_energy"},
#"Jet25_px":{"nbin":20,"min":-250,"max":250,"cut":"EvtWeight * (n_presel_jet>=1)","xlabel":"Jet25_px"},
#"Jet25_py":{"nbin":20,"min":-250,"max":250,"cut":"EvtWeight * (n_presel_jet>=1)","xlabel":"Jet25_py"},
"Jet25_qg":{"nbin":20,"min":0.,"max":1.,"cut":"EvtWeight * (n_presel_jet>=1)","xlabel":"Jet25_qg"},
#"Jet25_mass":{"nbin":50,"min":0.,"max":50.,"cut":"EvtWeight * (n_presel_jet>=1)","xlabel":"Jet25_mass"},
#"Jet25_lepdetamax":{"nbin":50,"min":-4.,"max":4.,"cut":"EvtWeight * (n_presel_jet>=1)","xlabel":"Jet25_lepdetamax"},
#"Jet25_lepdetamin":{"nbin":50,"min":-2.5,"max":2.5,"cut":"EvtWeight * (n_presel_jet>=1)","xlabel":"Jet25_lepdetamin"},
#"Jet25_lepdphimax":{"nbin":50,"min":-3.2,"max":3.2,"cut":"EvtWeight * (n_presel_jet>=1)","xlabel":"Jet25_lepdphimax"},
#"Jet25_lepdphimin":{"nbin":50,"min":-3.2,"max":3.2,"cut":"EvtWeight * (n_presel_jet>=1)","xlabel":"Jet25_lepdphimin"},
"Jet25_lepdrmax":{"nbin":20,"min":0.,"max":5.,"cut":"EvtWeight * (n_presel_jet>=1)","xlabel":"Jet25_lepdrmax"},
"Jet25_lepdrmin":{"nbin":20,"min":0.,"max":4.5,"cut":"EvtWeight * (n_presel_jet>=1)","xlabel":"Jet25_lepdrmin"},
}

systematics=["nominal"]
upDown=["_SysUp","_SysDown"]
Color={"ttWJets_2018":kBlack,"ttWJets_2017":kRed,"ttWJets_2016":kBlue}

sampleName = ["ttWJets_2018","ttWJets_2017","ttWJets_2016"]
postfix = "_NJet.root"
plotname = "Hj_ttWJets_NJet_era"

# directory of output
outputdir = "/home/binghuan/Work/Presentations/PHD/plots/"

# the root file saving the histograms
createROOTfile = True  # Set to Truth for the first time
filename = "%s%s.root"%(outputdir,plotname)

# options
normalization = True # Normalize to unit
showStats = False



##### end user defined variables
# check outputdir
if not os.path.exists(outputdir):
    print ('mkdir: ', outputdir)
    os.makedirs(outputdir)

# create root file, this will overwrite the root file
if createROOTfile:
    exec(open("/home/binghuan/Work/Macros/plotters/make_hists.py").read())

def createRatio(h1, h2, POI, norm):
    if norm:
        h1.Scale(1./h1.Integral())
        h2.Scale(1./h2.Integral())
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
    y.SetTitle("era/2018")
    y.CenterTitle()
    y.SetNdivisions(505)
    y.SetTitleSize(30)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.3)
    y.SetLabelFont(43)
    y.SetLabelSize(20)

    # Adjust x-axis settings
    x = h3.GetXaxis()
    x.SetTitle(POI)
    x.SetTitleSize(35)
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
    pad2.SetBottomMargin(0.30)
    pad2.SetTicks(0,1) 
    #pad2.SetGridx()
    pad2.Draw()

    return c, pad1, pad2


def plotSysts():
    inputfile = TFile(filename,"read")
    if inputfile.IsZombie():
        print("inputfile is Zombie")
        sys.exit()
    # loop over features
    for feature, values in features.items():
        # set up legend
        legend = TLegend(0.2,0.6,0.7,0.88)
        legend.SetHeader("")
        #legend.SetNColumns(3)
        legend.SetBorderSize(0)
                
        c, pad1, pad2 = createCanvasPads()

        # loop over samples
        hist_vars = []
        hist_ratio_vars = []
        i=0
        for sample in sampleName:
            if i ==0:
                # get nominal histograms
                hist_nom_name = sample+"_"+feature
                if not inputfile.GetListOfKeys().Contains(hist_nom_name): 
                    print ( "%s doesn't have histogram %s"%(filename, hist_nom_name))
                    continue
                hist_nom = inputfile.Get(hist_nom_name)
                hist_nom.SetFillColor(0)
                hist_nom.SetLineColor(Color[sample])
                hist_nom.SetMarkerColor(Color[sample])
                hist_nom.SetLineWidth(2)
                h_ratio = createRatio(hist_nom, hist_nom, values["xlabel"],normalization)
                h_ratio.SetMarkerColor(Color[sample])
                legend.AddEntry(hist_nom,sample,"l")
            else:    
                hist_name = sample+"_"+feature
                if not inputfile.GetListOfKeys().Contains(hist_name): 
                    print ( "%s doesn't have histogram %s"%(filename, hist_name))
                    continue
                hist_var = inputfile.Get(hist_name)
                hist_var.SetFillColor(0)
                hist_var.SetLineColor(Color[sample])
                hist_var.SetMarkerColor(Color[sample])
                hist_var.SetLineWidth(2)
                hist_vars.append(hist_var)
                h_ratio_var = createRatio(hist_var, hist_nom,values["xlabel"], normalization)
                h_ratio_var.SetMarkerColor(Color[sample])
                hist_ratio_vars.append(h_ratio_var)
                legend.AddEntry(h_ratio_var,sample,"l")
                
            i = i+1     
        
        # draw everything

        pad1.cd()
        #pad1.SetGridx()
        #pad1.SetGridy()
        
        # set bounds
        Y_name = "Events"
        maximum=0
        
        for hist in hist_vars:
            if normalization:
                hist.Scale(1./hist.Integral())
            if hist.GetMaximum()>maximum: maximum = hist.GetMaximum()
        upperbound = 1.8*maximum
        lowerbound = -maximum/40.
        
        Y_name = "Events"
        if normalization:
            hist_nom.Scale(1./hist_nom.Integral())
            Y_name = " Unit "
        if showStats:
            hist_nom.SetStats(1)
            
        hist_nom.SetMaximum(upperbound)
        hist_nom.SetMinimum(lowerbound)
        # Adjust y-axis settings
        y = hist_nom.GetYaxis()
        y.SetTitleSize(30)
        y.SetTitleFont(43)
        y.SetTitleOffset(1.3)
        y.SetLabelFont(43)
        y.SetLabelSize(20)
        y.SetTitle(Y_name) 
        
        # Adjust x-axis settings
        x = hist_nom.GetXaxis()
        x.SetTitleSize(25)
        x.SetTitleFont(43)
        x.SetTitleOffset(1.55)
        x.SetLabelFont(43)
        x.SetLabelSize(20)
        x.SetTitle(values["xlabel"])
        
        hist_nom.SetTitle("Signal Jets in ttHnobb")
        hist_nom.Draw("HIST")
        
        for hist in hist_vars:
            hist.Draw("HISTsame") 

        legend.Draw("same")

        
        pad2.cd()
        #pad2.SetGridx()
        #pad2.SetGridy()
        bins = h_ratio.GetNbinsX()
        LowEdge = h_ratio.GetBinLowEdge(1)
        HighEdge = h_ratio.GetBinLowEdge(bins+1)
        line = TLine(LowEdge,1,HighEdge,1)
        line.SetLineColor(kBlack)
        h_ratio.GetXaxis().SetRangeUser(values["min"], values["max"])
        h_ratio.SetFillColor(kGray+3)
        h_ratio.SetFillStyle(3001)
        h_ratio.Draw("E2")
        h_ratio.SetMinimum(0.5)
        h_ratio.SetMaximum(1.5)
        for i in range(len(hist_ratio_vars)):
            hist_ratio_vars[i].Draw("EPsame")
        
        
        line.Draw("same")

        c.SaveAs("%s%s_%s_%s_isNorm%s_wtStat%s.png"%(outputdir,feature,plotname,syst,normalization,showStats))

# Draw all canvases 
if __name__ == "__main__":
    gStyle.SetLegendTextSize(0.05)
    plotSysts()
