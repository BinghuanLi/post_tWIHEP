import sys
import argparse
import os
from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TString, TFile, TH1, THStack, gROOT, TStyle, TAttFill, TLegend, TGraphAsymmErrors, TLine
from ROOT import kBlack, kBlue, kRed, kCyan, kViolet, kGreen, kOrange, kGray, kPink, kTRUE

gROOT.SetBatch(1)

######### to run #########
#### python make_overlay.py --createROOTfile -y 2016 -i -o 
##########################

#### start  user defined variables


# options
usage = 'usage: %prog [options]'
parser = argparse.ArgumentParser(usage)
parser.add_argument('-d', '--dataset', nargs='?', help = 'dataset to plot', const="TTH", default="TTH")
parser.add_argument('-y', '--year', nargs='?', help = 'year to plot -1 to compare TR in three years ', const=2018, type=int ,default=2018)
parser.add_argument('-i', '--inputDir', nargs='?', help = 'inputDir', const="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_NNs/data/LegacyMVA_1108/DiLepRegion/TR_SR_RunII/", default="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_NNs/data/LegacyMVA_1108/DiLepRegion/TR_SR_RunII/")
parser.add_argument('-o', '--outputDir', nargs='?', help = 'outputDir', const="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_NNs/plots/Legacy_MVA_1108/", default="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_NNs/plots/Legacy_MVA_1108/")
parser.add_argument('--createROOTfile',        dest='createROOTfile'  ,      help='create or not the root files containing all the hist, must be true for the first time you run a given region',  action='store_true')

args = parser.parse_args()
year = args.year
dataset = args.dataset
inputDirectories = args.inputDir
outputdir = args.outputDir
createROOTfile = args.createROOTfile

treename = "syncTree";
cut = ""
 
features={
#"mT_lep1":{"nbin":25,"min":0.,"max":500,"cut":"EventWeight %s"%cut,"xlabel":"mT_lep1","logy":0},
#"mT_lep2":{"nbin":25,"min":0.,"max":500,"cut":"EventWeight %s"%cut,"xlabel":"mT_lep2","logy":0},
#"jet1_pt":{"nbin":25,"min":0.,"max":500.,"cut":"EventWeight %s"%cut,"xlabel":"jet1_pt","logy":0},
#"jet1_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"jet1_eta","logy":0},
#"jet1_phi":{"nbin":25,"min":-3.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"jet1_phi","logy":0},
#"jet1_E":{"nbin":25,"min":0.,"max":500,"cut":"EventWeight %s"%cut,"xlabel":"jet1_energy","logy":0},
#"jet2_pt":{"nbin":25,"min":0.,"max":250.,"cut":"EventWeight %s"%cut,"xlabel":"jet2_pt","logy":0},
#"jet2_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"jet2_eta","logy":0},
#"jet2_phi":{"nbin":25,"min":-3.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"jet2_phi","logy":0},
#"jet2_E":{"nbin":25,"min":0.,"max":500,"cut":"EventWeight %s"%cut,"xlabel":"jet2_energy","logy":0},
#"jet3_pt":{"nbin":25,"min":0.,"max":250.,"cut":"EventWeight %s"%cut,"xlabel":"jet3_pt","logy":0},
#"jet3_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"jet3_eta","logy":0},
#"jet3_phi":{"nbin":25,"min":-3.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"jet3_phi","logy":0},
#"jet3_E":{"nbin":25,"min":0.,"max":500,"cut":"EventWeight %s"%cut,"xlabel":"jet3_energy","logy":0},
#"jet4_pt":{"nbin":25,"min":0.,"max":250.,"cut":"EventWeight %s"%cut,"xlabel":"jet4_pt","logy":0},
#"jet4_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"jet4_eta","logy":0},
#"jet4_phi":{"nbin":25,"min":-3.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"jet4_phi","logy":0},
#"jet4_E":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"jet4_energy","logy":0},
#"jetFwd1_pt":{"nbin":25,"min":0.,"max":250.,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd1_pt","logy":1},
#"jetFwd1_eta":{"nbin":25,"min":-5.,"max":5.,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd1_eta","logy":1},
#"jetFwd2_pt":{"nbin":25,"min":0.,"max":250.,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd2_pt","logy":1},
#"jetFwd2_eta":{"nbin":25,"min":-5.,"max":5.,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd2_eta","logy":1},
#"metLD":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"metLD","logy":0},
#"lep1_conePt":{"nbin":25,"min":0.,"max":250.,"cut":"EventWeight %s"%cut,"xlabel":"lep1_pt","logy":0},
#"lep1_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"lep1_eta","logy":0},
#"lep1_phi":{"nbin":25,"min":-3.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"lep1_phi","logy":0},
#"lep1_E":{"nbin":25,"min":0.,"max":500,"cut":"EventWeight %s"%cut,"xlabel":"lep1_energy","logy":0},
#"lep2_conePt":{"nbin":25,"min":0.,"max":250.,"cut":"EventWeight %s"%cut,"xlabel":"lep2_pt","logy":0},
#"lep2_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"lep2_eta","logy":0},
#"lep2_phi":{"nbin":25,"min":-3.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"lep2_phi","logy":0},
#"lep2_E":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"lep2_energy","logy":0},
#"mindr_lep1_jet":{"nbin":25,"min":0.,"max":5.0,"cut":"EventWeight %s"%cut,"xlabel":"mindr_lep1_jet","logy":0},
#"mindr_lep2_jet":{"nbin":25,"min":0.,"max":5.0,"cut":"EventWeight %s"%cut,"xlabel":"mindr_lep2_jet","logy":0},
#"max_lep_eta":{"nbin":25,"min":0.,"max":3.0,"cut":"EventWeight %s"%cut,"xlabel":"max_lep_eta","logy":0},
#"nLightJet":{"nbin":6,"min":-0.5,"max":5.5,"cut":"EventWeight %s"%cut,"xlabel":"nLightJet","logy":0},
#"min_Deta_mostfwdJet_jet":{"nbin":25,"min":0.,"max":5,"cut":"EventWeight %s"%cut,"xlabel":"min_Deta_mostfwdJet_jet","logy":1},
#"min_Deta_leadfwdJet_jet":{"nbin":25,"min":0.,"max":5,"cut":"EventWeight %s"%cut,"xlabel":"min_Deta_leadfwdJet_jet","logy":1},
#"mT2_top_3particle":{"nbin":25,"min":0.,"max":500,"cut":"EventWeight %s"%cut,"xlabel":"mT2_top_3particle","logy":0},
#"mT2_top_2particle":{"nbin":25,"min":0.,"max":500,"cut":"EventWeight %s"%cut,"xlabel":"mT2_top_2particle","logy":0},
#"mT2_W":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"mT2_W","logy":0},
#"angle_bbpp_highest2b":{"nbin":25,"min":0.,"max":3.3,"cut":"EventWeight %s"%cut,"xlabel":"angle_bbpp_highest2b","logy":0},
#"mbb":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"mbb","logy":0},
#"mbb_loose":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"mbb_loose","logy":0},
#"hadTop_BDT":{"nbin":25,"min":-1.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"hadTop_BDT","logy":0},
#"hadTop_pt":{"nbin":25,"min":0.,"max":500,"cut":"EventWeight %s"%cut,"xlabel":"hadTop_pt","logy":0},
#"Hj_tagger_hadTop":{"nbin":25,"min":-1.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"Hj_tagger_hadTop","logy":0},
#"Hj_tagger":{"nbin":25,"min":-1.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"Hj_tagger","logy":0},
#"nBJetLoose":{"nbin":6,"min":-0.5,"max":5.5,"cut":"EventWeight %s"%cut,"xlabel":"nBJetLoose","logy":0},
#"nBJetMedium":{"nbin":6,"min":-0.5,"max":5.5,"cut":"EventWeight %s"%cut,"xlabel":"nBJetMedium","logy":0},
#"n_presel_jet":{"nbin":8,"min":-0.5,"max":7.5,"cut":"EventWeight %s"%cut,"xlabel":"n_presel_jet","logy":0},
#"n_presel_jetFwd":{"nbin":5,"min":-0.5,"max":4.5,"cut":"EventWeight %s"%cut,"xlabel":"n_presel_jetFwd","logy":0},
"mass_dilep":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"mass_dilep","logy":1},
#"nElectron":{"nbin":3,"min":-0.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"nElectron","logy":0},
#"lep1_charge":{"nbin":3,"min":-1.5,"max":1.5,"cut":"EventWeight %s"%cut,"xlabel":"lep1_charge","logy":0},
}

systematics=["nominal"]
upDown=["_SysUp","_SysDown"]


Color={"%s_SR_%i"%(dataset,year):kBlack,"%s_TR_%i"%(dataset,year):kRed}
sampleName = ["%s_SR_%i"%(dataset,year),"%s_TR_%i"%(dataset,year)]

postfix = ".root"
plotname = "%s_SRTR_%i"%(dataset,year)

if year == -1:
    Color={"%s_TR_2016"%(dataset):kBlack,"%s_TR_2017"%(dataset):kRed, "%s_TR_2018"%(dataset): kBlue}
    sampleName = ["%s_TR_2016"%(dataset),"%s_TR_2017"%(dataset),"%s_TR_2018"%(dataset)]
    plotname = "%s_TR_161718"%(dataset)


# the root file saving the histograms
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
    inputfile = TFile(filename,"read")
    if inputfile.IsZombie():
        print("inputfile is Zombie")
        sys.exit()
    # loop over features
    for feature, values in features.items():
        # set up legend
        legend = TLegend(0.2,0.6,0.7,0.88)
        legend.SetHeader("CMS preliminary")
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
                h_ratio = createRatio(hist_nom, hist_nom, values["xlabel"],normalization)
                h_ratio.SetMarkerColor(Color[sample])
                legend.AddEntry(hist_nom,hist_nom_name,"l")
            else:    
                hist_name = sample+"_"+feature
                if not inputfile.GetListOfKeys().Contains(hist_name): 
                    print ( "%s doesn't have histogram %s"%(filename, hist_name))
                    continue
                hist_var = inputfile.Get(hist_name)
                hist_var.SetFillColor(0)
                hist_var.SetLineColor(Color[sample])
                hist_var.SetMarkerColor(Color[sample])
                hist_vars.append(hist_var)
                h_ratio_var = createRatio(hist_var, hist_nom,values["xlabel"], normalization)
                h_ratio_var.SetMarkerColor(Color[sample])
                hist_ratio_vars.append(h_ratio_var)
                legend.AddEntry(h_ratio_var,hist_name,"l")
                
            i = i+1     
        
        # draw everything

        pad1.cd()
        pad1.SetGridx()
        pad1.SetGridy()
        if values["logy"]==1:
            pad1.SetLogy()
        
        # set bounds
        Y_name = "Events"
        maximum=0
        
        for hist in hist_vars:
            if normalization:
                hist.Scale(1./hist.Integral())
            if hist.GetMaximum()>maximum: maximum = hist.GetMaximum()
        upperbound = 1.8*maximum
        lowerbound = -maximum/40.
        if values["logy"]==1:
            upperbound = 10*maximum
            lowerbound = 0.0000001
        
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
        y.SetTitleSize(25)
        y.SetTitleFont(43)
        y.SetTitleOffset(1.55)
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
        
        hist_nom.Draw("HIST")
        
        for hist in hist_vars:
            hist.Draw("HISTsame") 

        legend.Draw("same")

        
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

        c.SaveAs("%s%s_%s_%s_isNorm%s_wtStat%s_overlay.png"%(outputdir,feature,plotname,syst,normalization,showStats))

# Draw all canvases 
if __name__ == "__main__":
    plotSysts()
