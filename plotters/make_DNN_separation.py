import sys
import argparse
import os
from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TString, TFile, TH1, THStack, gROOT, TStyle, TAttFill, TLegend, TGraphAsymmErrors, TLine, TLatex, TPaveText
from ROOT import kBlack, kBlue, kRed, kCyan, kViolet, kGreen, kOrange, kGray, kPink, kTRUE

gROOT.SetBatch(1)

######### to run #########
#python make_DNN_separation.py -y 2017 -d TTH --dataset2 TTW --dataset3 THQ --dataset4 TTJ --createROOT -i /home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_NNs/data/LegacyMVA_tau2p1_1204/DiLepRegion/TR_SR_RunII/ -o /home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_NNs/plots/LegacyNN_plotPHD/
##########################

#### start  user defined variables


# options
usage = 'usage: %prog [options]'
parser = argparse.ArgumentParser(usage)
parser.add_argument('-d', '--dataset', nargs='?', help = 'dataset to plot', const="TTZ", default="TTZ")
parser.add_argument('--dataset2', nargs='?', help = 'dataset2 to plot', const="NULL", default="NULL")
parser.add_argument('--dataset3', nargs='?', help = 'dataset3 to plot', const="NULL", default="NULL")
parser.add_argument('--dataset4', nargs='?', help = 'dataset4 to plot', const="NULL", default="NULL")
parser.add_argument('-y', '--year', nargs='?', help = 'year to plot -1 to compare TR in three years ', const=2018, type=int ,default=2018)
parser.add_argument('-i', '--inputDir', nargs='?', help = 'inputDir', const="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_NNs/data/LegacyMVA_1108/DiLepRegion/TR_SR_RunII/", default="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_NNs/data/LegacyMVA_1108/DiLepRegion/TR_SR_RunII/")
parser.add_argument('-o', '--outputDir', nargs='?', help = 'outputDir', const="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_NNs/plots/Legacy_MVA_1108/", default="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_NNs/plots/Legacy_MVA_1108/")
parser.add_argument('--createROOTfile',        dest='createROOTfile'  ,      help='create or not the root files containing all the hist, must be true for the first time you run a given region',  action='store_true')

args = parser.parse_args()
year = args.year
dataset = args.dataset
dataset2 = args.dataset2
dataset3 = args.dataset3
dataset4 = args.dataset4
inputDirectories = args.inputDir
outputdir = args.outputDir
createROOTfile = args.createROOTfile

treename = "syncTree";
cut = ""

########## create log file ##########
logfile = open("{}/sepration.log".format(outputdir) ,"a")
 
features={
"hadTop_BDT":{"nbin":10,"min":0.,"max":1.,"cut":"EventWeight%s"%cut,"xlabel":"hadTop_BDT","logy":0},
"jetFwd1_pt":{"nbin":10,"min":20.,"max":200.,"cut":"EventWeight%s"%cut,"xlabel":"jetFwd1_pt","logy":1},
"jetFwd1_eta":{"nbin":10,"min":-5.,"max":5.,"cut":"EventWeight%s"%cut,"xlabel":"jetFwd1_eta","logy":1},
"n_presel_jet":{"nbin":7,"min":0.5,"max":7.5,"cut":"EventWeight%s"%cut,"xlabel":"n_presel_jet","logy":0},
"mbb":{"nbin":10,"min":0.,"max":200,"cut":"EventWeight%s"%cut,"xlabel":"mbb","logy":0},
"jet3_pt":{"nbin":10,"min":0.,"max":100.,"cut":"EventWeight%s"%cut,"xlabel":"jet3_pt","logy":0},
"mT_lep1":{"nbin":10,"min":0.,"max":200,"cut":"EventWeight%s"%cut,"xlabel":"mT_lep1","logy":0},
"mT_lep2":{"nbin":10,"min":0.,"max":200,"cut":"EventWeight%s"%cut,"xlabel":"mT_lep2","logy":0},
"jet1_pt":{"nbin":10,"min":20.,"max":200.,"cut":"EventWeight%s"%cut,"xlabel":"jet1_pt","logy":0},
"jet1_eta":{"nbin":10,"min":-2.5,"max":2.5,"cut":"EventWeight%s"%cut,"xlabel":"jet1_eta","logy":0},
"jet1_phi":{"nbin":10,"min":-3.15,"max":3.15,"cut":"EventWeight%s"%cut,"xlabel":"jet1_phi","logy":0},
"jet2_pt":{"nbin":10,"min":20.,"max":200.,"cut":"EventWeight%s"%cut,"xlabel":"jet2_pt","logy":0},
"jet2_eta":{"nbin":10,"min":-2.5,"max":2.5,"cut":"EventWeight%s"%cut,"xlabel":"jet2_eta","logy":0},
"jet2_phi":{"nbin":10,"min":-3.15,"max":3.15,"cut":"EventWeight%s"%cut,"xlabel":"jet2_phi","logy":0},
"jet3_eta":{"nbin":10,"min":-2.5,"max":2.5,"cut":"EventWeight%s"%cut,"xlabel":"jet3_eta","logy":0},
"jet3_phi":{"nbin":10,"min":-3.15,"max":3.15,"cut":"EventWeight%s"%cut,"xlabel":"jet3_phi","logy":0},
"jet4_pt":{"nbin":10,"min":0.,"max":100.,"cut":"EventWeight%s"%cut,"xlabel":"jet4_pt","logy":0},
"jet4_eta":{"nbin":10,"min":-2.5,"max":2.5,"cut":"EventWeight%s"%cut,"xlabel":"jet4_eta","logy":0},
"jet4_phi":{"nbin":10,"min":-3.15,"max":3.15,"cut":"EventWeight%s"%cut,"xlabel":"jet4_phi","logy":0},
"metLD":{"nbin":10,"min":0.,"max":200,"cut":"EventWeight%s"%cut,"xlabel":"metLD","logy":0},
"lep1_conePt":{"nbin":10,"min":0.,"max":200.,"cut":"EventWeight%s"%cut,"xlabel":"lep1_pt","logy":0},
"lep1_eta":{"nbin":10,"min":-2.5,"max":2.5,"cut":"EventWeight%s"%cut,"xlabel":"lep1_eta","logy":0},
"lep1_phi":{"nbin":10,"min":-3.15,"max":3.15,"cut":"EventWeight%s"%cut,"xlabel":"lep1_phi","logy":0},
"lep2_conePt":{"nbin":10,"min":0.,"max":100.,"cut":"EventWeight%s"%cut,"xlabel":"lep2_pt","logy":0},
"lep2_eta":{"nbin":10,"min":-2.5,"max":2.5,"cut":"EventWeight%s"%cut,"xlabel":"lep2_eta","logy":0},
"lep2_phi":{"nbin":10,"min":-3.15,"max":3.15,"cut":"EventWeight%s"%cut,"xlabel":"lep2_phi","logy":0},
"mindr_lep1_jet":{"nbin":10,"min":0.,"max":4.0,"cut":"EventWeight%s"%cut,"xlabel":"mindr_lep1_jet","logy":0},
"mindr_lep2_jet":{"nbin":10,"min":0.,"max":4.0,"cut":"EventWeight%s"%cut,"xlabel":"mindr_lep2_jet","logy":0},
"maxeta":{"nbin":10,"min":0.,"max":2.5,"cut":"EventWeight%s"%cut,"xlabel":"maxeta","logy":0},
"Hj_tagger_hadTop":{"nbin":10,"min":0.,"max":1.,"cut":"EventWeight%s"%cut,"xlabel":"Hj_tagger_hadTop","logy":0},
"nBJetLoose":{"nbin":4,"min":0.5,"max":4.5,"cut":"EventWeight%s"%cut,"xlabel":"nBJetLoose","logy":0},
"nBJetMedium":{"nbin":4,"min":-0.5,"max":3.5,"cut":"EventWeight%s"%cut,"xlabel":"nBJetMedium","logy":0},
"n_presel_jetFwd":{"nbin":4,"min":-0.5,"max":3.5,"cut":"EventWeight%s"%cut,"xlabel":"n_presel_jetFwd","logy":0},
"Dilep_pdgId":{"nbin":3,"min":0.5,"max":3.5,"cut":"EventWeight%s"%cut,"xlabel":"Dilep_pdgId","logy":0},
"lep1_charge":{"nbin":3,"min":-1.5,"max":1.5,"cut":"EventWeight%s"%cut,"xlabel":"lep1_charge","logy":0},
"avg_dr_jet":{"nbin":10,"min":0.,"max":5.,"cut":"EventWeight%s"%cut,"xlabel":"avg_dr_jet","logy":0},




#"Hj_tagger":{"nbin":10,"min":0.,"max":1.,"cut":"EventWeight%s"%cut,"xlabel":"Hj_tagger","logy":0},
#"nElectron":{"nbin":3,"min":-0.5,"max":2.5,"cut":"EventWeight%s"%cut,"xlabel":"nElectron","logy":0},
#"mass_dilep":{"nbin":10,"min":0.,"max":250,"cut":"EventWeight%s"%cut,"xlabel":"mass_dilep","logy":1},
#"nLightJet":{"nbin":6,"min":-0.5,"max":5.5,"cut":"EventWeight%s"%cut,"xlabel":"nLightJet","logy":0},
#"min_Deta_mostfwdJet_jet":{"nbin":10,"min":0.,"max":5,"cut":"EventWeight%s"%cut,"xlabel":"min_Deta_mostfwdJet_jet","logy":1},
#"jet1_QGdiscr":{"nbin":15,"min":0.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"jet1_QGdiscr","logy":0},
#"jet2_QGdiscr":{"nbin":15,"min":0.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"jet2_QGdiscr","logy":0},
#"lep1_ptratio":{"nbin":15,"min":0.,"max":1.5,"cut":"EventWeight %s"%cut,"xlabel":"lep1_ptratio","logy":0},
#"lep2_ptratio":{"nbin":15,"min":0.,"max":1.5,"cut":"EventWeight %s"%cut,"xlabel":"lep2_ptratio","logy":0},
#"lep1_ptrel":{"nbin":15,"min":0.,"max":50.,"cut":"EventWeight %s"%cut,"xlabel":"lep1_ptrel","logy":0},
#"lep2_ptrel":{"nbin":15,"min":0.,"max":50.,"cut":"EventWeight %s"%cut,"xlabel":"lep2_ptrel","logy":0},
#"mhtT":{"nbin":15,"min":0.,"max":300,"cut":"EventWeight %s"%cut,"xlabel":"mhtT","logy":0},
#"mhtT_met":{"nbin":15,"min":0.,"max":300,"cut":"EventWeight %s"%cut,"xlabel":"mhtT_met","logy":0},
#"massll":{"nbin":15,"min":0.,"max":300,"cut":"EventWeight %s"%cut,"xlabel":"massll","logy":0},
#"min_Deta_leadfwdJet_jet":{"nbin":10,"min":0.,"max":5,"cut":"EventWeight%s"%cut,"xlabel":"min_Deta_leadfwdJet_jet","logy":1},
#"mT2_top_3particle":{"nbin":10,"min":0.,"max":500,"cut":"EventWeight%s"%cut,"xlabel":"mT2_top_3particle","logy":0},
#"mT2_top_2particle":{"nbin":10,"min":0.,"max":500,"cut":"EventWeight%s"%cut,"xlabel":"mT2_top_2particle","logy":0},
#"mT2_W":{"nbin":10,"min":0.,"max":250,"cut":"EventWeight%s"%cut,"xlabel":"mT2_W","logy":0},
#"angle_bbpp_highest2b":{"nbin":10,"min":0.,"max":3.3,"cut":"EventWeight%s"%cut,"xlabel":"angle_bbpp_highest2b","logy":0},
#"mbb_loose":{"nbin":10,"min":0.,"max":250,"cut":"EventWeight%s"%cut,"xlabel":"mbb_loose","logy":0},
#"hadTop_pt":{"nbin":10,"min":0.,"max":500,"cut":"EventWeight%s"%cut,"xlabel":"hadTop_pt","logy":0},
}


variables = []
TTW_sep = []
TTJ_sep = []
THQ_sep = []

systematics=["nominal"]
upDown=["_SysUp","_SysDown"]



Color={"%s_SR_%i"%(dataset,year):kBlack,"%s_TR_%i"%(dataset,year):kRed}
Style={"%s_SR_%i"%(dataset,year):1,"%s_TR_%i"%(dataset,year):2}
sampleName = ["%s_SR_%i"%(dataset,year),"%s_TR_%i"%(dataset,year)]

postfix = ".root"
plotname = "%s_SRTR_%i"%(dataset,year)

if dataset4 != "NULL":
    Color={
     "%s_TR_%i"%(dataset,year):kBlack,"%s_TR_%i"%(dataset2,year):kRed,"%s_TR_%i"%(dataset3,year):kBlue, "%s_TR_%i"%(dataset4,year):kViolet
    }
    Style={
     "%s_TR_%i"%(dataset,year):2,"%s_TR_%i"%(dataset2,year):2,"%s_TR_%i"%(dataset3,year):2, "%s_TR_%i"%(dataset4,year):2
    }
    sampleName = [
        "%s_TR_%i"%(dataset,year),"%s_TR_%i"%(dataset2,year), "%s_TR_%i"%(dataset3,year),"%s_TR_%i"%(dataset4,year)
    ]
    plotname = "%svs%svs%svs%s_all_%i"%(dataset,dataset2,dataset3,dataset4,year)
elif dataset3 != "NULL":
    Color={
     "%s_TR_%i"%(dataset,year):kBlack,"%s_TR_%i"%(dataset2,year):kRed,"%s_TR_%i"%(dataset3,year):kBlue,
    }
    Style={
     "%s_TR_%i"%(dataset,year):2,"%s_TR_%i"%(dataset2,year):2,"%s_TR_%i"%(dataset3,year):2,
    }
    sampleName = [
        "%s_TR_%i"%(dataset,year),"%s_TR_%i"%(dataset2,year), "%s_TR_%i"%(dataset3,year),
    ]
    plotname = "%svs%svs%s_all_%i"%(dataset,dataset2,dataset3,year)
elif dataset2 != "NULL":
    Color={
     "%s_TR_%i"%(dataset,year):kBlack,"%s_TR_%i"%(dataset2,year):kRed,
    }
    Style={
     "%s_TR_%i"%(dataset,year):2,"%s_TR_%i"%(dataset2,year):2,
    }
    sampleName = [
        "%s_TR_%i"%(dataset,year),"%s_TR_%i"%(dataset2,year),
    ]
elif year == -1:
    Color={"%s_TR_2016"%(dataset):kBlack,"%s_TR_2017"%(dataset):kRed, "%s_TR_2018"%(dataset): kBlue}
    Style={"%s_TR_2016"%(dataset):2,"%s_TR_2017"%(dataset):2, "%s_TR_2018"%(dataset): 2}
    sampleName = ["%s_TR_2016"%(dataset),"%s_TR_2017"%(dataset),"%s_TR_2018"%(dataset)]
    plotname = "%s_TR_161718"%(dataset)
elif year == -2:
    Color={"%s_SR_2016"%(dataset):kBlack,"%s_SR_2017"%(dataset):kRed, "%s_SR_2018"%(dataset): kBlue}
    Style={"%s_SR_2016"%(dataset):1,"%s_SR_2017"%(dataset):1, "%s_SR_2018"%(dataset): 1}
    sampleName = ["%s_SR_2016"%(dataset),"%s_SR_2017"%(dataset),"%s_SR_2018"%(dataset)]
    plotname = "%s_SR_161718"%(dataset)


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

def getSeparation(hsig, hbkg):
    separation = 0
    if (hsig.GetNbinsX() != hbkg.GetNbinsX()):
        print('Number of bins different for sig. and bckg')
    nBins = hsig.GetNbinsX()
    hsig_norm = hsig.Integral()
    hbkg_norm = hbkg.Integral()
    if hsig_norm == 0. or hbkg_norm ==0.:
        print (' hsig or hbkg is empty ')
        return separation
    for i in range(1,nBins):
        sig_bin = hsig.GetBinContent(i)/hsig_norm
        bkg_bin = hbkg.GetBinContent(i)/hbkg_norm
        # Separation:
        if(sig_bin+bkg_bin > 0):
            separation += 0.5 * ((sig_bin - bkg_bin) * (sig_bin - bkg_bin)) / (sig_bin + bkg_bin)
    return separation
    

def plotSysts():
    inputfile = TFile(filename,"read")
    if inputfile.IsZombie():
        print("inputfile is Zombie")
        sys.exit()
    # loop over features
    for feature, values in features.items():
        # set up legend
        #legend = TLegend(0.55,0.8,0.95,0.98)
        legend = TLegend(0.65,0.6,0.95,0.98)
        #legend.SetHeader("CMS preliminary")
        legend.SetHeader("")
        legend.SetNColumns(2)
        legend.SetBorderSize(0)
        
        text = TPaveText(0.15, 0.6,  0.45, 0.98, "brNDC");
        logfile.write("\\\\\hline\n {}  ".format(feature))

        variables.append(feature)

        c, pad1, pad2 = createCanvasPads()

        # loop over samples
        hist_vars = []
        sep_vars = []
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
                hist_nom.SetLineStyle(Style[sample])
                sep_var = getSeparation(hist_nom, hist_nom)
                sep_vars.append(sep_var)
                text.AddText("TTH vs {} seperation:  {:.3f}".format(sample.replace("_TR_{}".format(year),""), sep_var))
                h_ratio = createRatio(hist_nom, hist_nom, values["xlabel"],normalization)
                h_ratio.SetMarkerColor(Color[sample])
                legend.AddEntry(hist_nom, sample.replace("_{}".format(year),""),"l")
            else:    
                hist_name = sample+"_"+feature
                if not inputfile.GetListOfKeys().Contains(hist_name): 
                    print ( "%s doesn't have histogram %s"%(filename, hist_name))
                    continue
                hist_var = inputfile.Get(hist_name)
                hist_var.SetFillColor(0)
                hist_var.SetLineColor(Color[sample])
                hist_var.SetMarkerColor(Color[sample])
                hist_var.SetLineStyle(Style[sample])
                hist_vars.append(hist_var)
                sep_var = getSeparation(hist_nom, hist_var)
                sep_vars.append(sep_var)
                text.AddText("TTH vs {} seperation:  {:.3f}".format(sample.replace("_TR_{}".format(year),""), sep_var))
                #logfile.write("& {:.3f} ".format(sep_var))
                if sample.replace("_TR_{}".format(year),"") == "TTW":
                    TTW_sep.append(sep_var)
                if sample.replace("_TR_{}".format(year),"") == "TTJ":
                    TTJ_sep.append(sep_var)
                if sample.replace("_TR_{}".format(year),"") == "THQ":
                    THQ_sep.append(sep_var)
                h_ratio_var = createRatio(hist_var, hist_nom,values["xlabel"], normalization)
                h_ratio_var.SetMarkerColor(Color[sample])
                hist_ratio_vars.append(h_ratio_var)
                legend.AddEntry(h_ratio_var, sample.replace("_{}".format(year),"") ,"l")
                
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
        hist_nom.SetTitle("")
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
        text.Draw("same")
        
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
        y = h_ratio.GetYaxis()
        y.SetTitle("MC/{}".format(dataset))
        h_ratio.Draw("E2")
        h_ratio.SetMinimum(0.5)
        h_ratio.SetMaximum(1.5)
        for i in range(len(hist_ratio_vars)):
            hist_ratio_vars[i].Draw("EPsame")
        
        
        
        line.Draw("same")

        c.SaveAs("%s%s_%s_DNN_inputs_separation.png"%(outputdir,feature,plotname))
    
    import pandas as pd
    sep_data= {"feature":variables, "ttHvsttW": TTW_sep, "ttHvsttJ":TTJ_sep, "ttHvstHq":THQ_sep }
    df = pd.DataFrame(sep_data)
    df.to_csv("separation_all.csv")

# Draw all canvases 
if __name__ == "__main__":
    plotSysts()
