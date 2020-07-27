import sys
import argparse
import os
from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TString, TFile, TH1, THStack, gROOT, TStyle, TAttFill, TLegend, TGraphAsymmErrors, TLine, gStyle
from ROOT import kBlack, kBlue, kRed, kCyan, kViolet, kGreen, kOrange, kGray, kPink, kTRUE

#### start  user defined variables

inputDirectories = "/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/plots/mvaTool_LegacyAll_ITC_20200622/Output_2018_GT5/SubCat2l/inclusive/Var_DiLepRegion/";

usage = 'usage: %prog [options]'
parser = argparse.ArgumentParser(usage)
parser.add_argument('-y', '--year', nargs='?', help = 'year to plot -1 to compare TR in three years ', const=2018, type=int ,default=2018)
parser.add_argument('-d', '--dataset', nargs='?', help = 'samples to plot', const="THQ", default="THQ")
args = parser.parse_args()
year = args.year
dataset = args.dataset

cut=""
features={
"n_presel_jet":{"xlabel":"n_presel_jet","logy":0},
"nBJetLoose":{"xlabel":"nBJetLoose","logy":0},
"nBJetMedium":{"xlabel":"nBJetMedium","logy":0},
"lep1_conePt":{"xlabel":"lep1_conePt","logy":0},
"lep2_conePt":{"xlabel":"lep2_conePt","logy":0},
"n_presel_jetFwd":{"xlabel":"n_presel_jetFwd","logy":0},
}


systematics=["nominal"]
upDown=["_SysUp","_SysDown"]
Color={"kt_1_kv_1":kBlack,"kt_2_kv_1":kRed,"kt_3_kv_1":kBlue, "kt_0_kv_1":kViolet}
ktkvName=["kt_1_kv_1", "kt_2_kv_1", "kt_3_kv_1", "kt_0_kv_1"]
legName={"kt_1_kv_1":"kt/kv = 1","kt_2_kv_1":"kt/kv = 2","kt_3_kv_1":"kt/kv = 3", "kt_0_kv_1":"kt/kv = 0"}
Style={"kt_1_kv_1":2,"kt_2_kv_1":3,"kt_3_kv_1":4, "kt_0_kv_1":26}

plotname = "{}_ktkv".format(dataset)

# directory of output
outputdir = "/home/binghuan/Work/Presentations/PHD/plots/kt_kv_distribution/"

# options
normalization = True # Normalize to unit
showStats = False

##### end user defined variables
# check outputdir
if not os.path.exists(outputdir):
    print ('mkdir: ', outputdir)
    os.makedirs(outputdir)

# create root file, this will overwrite the root file
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
    y.SetTitle("kappa modified/SM")
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
    for feature, values in features.items():
        # set up legend
        legend = TLegend(0.5,0.65,0.9,0.88)
        legend.SetHeader("2lss {} process".format(dataset))
        #legend.SetNColumns(3)
        legend.SetBorderSize(0)
                
        #c, pad1, pad2 = createCanvasPads()

        # loop over samples
        hist_vars = []
        hist_ratio_vars = []
        i=0
        for ktkv in ktkvName:
            filename = "{}/output_inclusive_{}_{}.root".format(inputDirectories,dataset, ktkv)
            inputfile = TFile(filename,"read")
            if inputfile.IsZombie():
                print("inputfile is Zombie")
                sys.exit()
            # loop over features
            if i ==0:
                # get nominal histograms
                hist_nom_name = feature + "_" + dataset
                if not inputfile.GetListOfKeys().Contains(hist_nom_name): 
                    print ( "%s doesn't have histogram %s"%(filename, hist_nom_name))
                    continue
                hist_nom = inputfile.Get(hist_nom_name)
                hist_nom.SetDirectory(0)
                hist_nom.SetFillColor(0)
                hist_nom.SetLineColor(Color[ktkv])
                hist_nom.SetMarkerColor(Color[ktkv])
                hist_nom.SetMarkerStyle(Style[ktkv])
                hist_nom.SetMarkerSize(2)
                hist_nom.SetLineWidth(2)
                h_ratio = createRatio(hist_nom, hist_nom, values["xlabel"],normalization)
                h_ratio.SetDirectory(0)
                h_ratio.SetMarkerColor(Color[ktkv])
                legend.AddEntry(hist_nom,legName[ktkv] ,"lp")
            else:    
                hist_name = feature + "_" + dataset
                if not inputfile.GetListOfKeys().Contains(hist_name): 
                    print ( "%s doesn't have histogram %s"%(filename, hist_name))
                    continue
                hist_var = inputfile.Get(hist_name)
                hist_var.SetDirectory(0)
                hist_var.SetFillColor(0)
                hist_var.SetLineColor(Color[ktkv])
                hist_var.SetMarkerColor(Color[ktkv])
                hist_var.SetMarkerStyle(Style[ktkv])
                hist_var.SetMarkerSize(2)
                hist_var.SetLineWidth(2)
                hist_vars.append(hist_var)
                h_ratio_var = createRatio(hist_var, hist_nom,values["xlabel"], normalization)
                h_ratio_var.SetMarkerColor(Color[ktkv])
                h_ratio_var.SetDirectory(0)
                hist_ratio_vars.append(h_ratio_var)
                legend.AddEntry(hist_var,legName[ktkv],"lp")
             
            i = i+1     
            inputfile.Close()

        # draw everything

        c = TCanvas("c", "canvas", 800, 800)
        c.cd()
        #c.SetGridx()
        #c.SetGridy()
        c.SetLeftMargin(1.65)
        c.SetBottomMargin(1.65)
        
        #pad1.cd()
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
        if not showStats:
            hist_nom.SetStats(0)

            
        hist_nom.SetMaximum(upperbound)
        hist_nom.SetMinimum(lowerbound)
        hist_nom.SetTitle("{}".format(year))
        # Adjust y-axis settings
        y = hist_nom.GetYaxis()
        y.SetTitleSize(40)
        y.SetTitleFont(43)
        y.SetTitleOffset(0.8)
        y.SetLabelFont(43)
        y.SetLabelSize(20)
        y.SetTitle(Y_name) 
        
        # Adjust x-axis settings
        x = hist_nom.GetXaxis()
        x.SetTitleSize(40)
        x.SetTitleFont(43)
        x.SetTitleOffset(0.8)
        x.SetLabelFont(43)
        x.SetLabelSize(20)
        x.SetTitle(values["xlabel"])
        
        hist_nom.Draw("EP")
        
        for hist in hist_vars:
            hist.Draw("EPsame") 

        legend.Draw("same")

        
        #pad2.cd()
        #pad2.SetGridx()
        #pad2.SetGridy()
        #bins = h_ratio.GetNbinsX()
        #LowEdge = h_ratio.GetBinLowEdge(1)
        #HighEdge = h_ratio.GetBinLowEdge(bins+1)
        #line = TLine(LowEdge,1,HighEdge,1)
        #line.SetLineColor(kBlack)
        #h_ratio.SetFillColor(kGray+3)
        #h_ratio.SetFillStyle(3001)
        #h_ratio.Draw("E2")
        #h_ratio.SetMinimum(0.5)
        #h_ratio.SetMaximum(1.5)
        #for i in range(len(hist_ratio_vars)):
        #    hist_ratio_vars[i].Draw("EPsame")
        
        
        
        #line.Draw("same")

        c.SaveAs("%s%s_%s_isNorm%s_%s.png"%(outputdir,feature,plotname,normalization,year))

# Draw all canvases 
if __name__ == "__main__":
    gStyle.SetLegendTextSize(0.04)
    plotSysts()
