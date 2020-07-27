import sys
import argparse
import os
from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TString, TFile, TH1, THStack, gROOT, TStyle, TAttFill, TLegend, TGraphAsymmErrors, TLine, gStyle
from ROOT import kBlack, kBlue, kRed, kCyan, kViolet, kGreen, kOrange, kGray, kPink, kTRUE

gROOT.SetBatch(1)


######### to run #########
#### python make_ratios.py --createROOTfile --norm -r DiLepRegion -y 2016 -i /home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/data/rootplas_V1_20190927/ -o /home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/plots/rootplas_V1_20190927/
##########################


#### start  user defined variables

# options
usage = 'usage: %prog [options]'
parser = argparse.ArgumentParser(usage)
parser.add_argument('-r', '--region', nargs='?', help = 'region to plot', const="DiLepRegion", default="DiLepRegion")
parser.add_argument('-y', '--year', nargs='?', help = 'year to plot', const=2018, type=int ,default=2018)
parser.add_argument('-i', '--inputDir', nargs='?', help = 'inputDir', const="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/data/rootplas_SVATrig_20200215/", default="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/data/rootplas_SVATrig_20200215/")
parser.add_argument('-o', '--outputDir', nargs='?', help = 'outputDir', const="/home/binghuan/Work/Presentations/PHD/plots/", default="/home/binghuan/Work/Presentations/PHD/plots/")
parser.add_argument('--norm', help='if norm: variation is normalizaed to nominal', action='store_true')
parser.add_argument('--stats', help='if stats: show statistics box ', action='store_true')
parser.add_argument('--createROOTfile',        dest='createROOTfile'  ,      help='create or not the root files containing all the hist, must be true for the first time you run a given region',  action='store_true')


args = parser.parse_args()
region = args.region
year = args.year
inputDir = args.inputDir
outputDir = args.outputDir
createROOTfile = args.createROOTfile
normalization = args.norm
showStats = args.stats

# dictionaries
# specify additional cuts for some regions
Cuts = {
    "ttWctrl":"*(n_presel_jet ==3)",
    "ttHgeq4j":"*(n_presel_jet >=4 && is_tH_like_and_not_ttH_like==0)"
    }
# specify the corresponding root files used for each region
PostFix={
"DiLepRegion":"DiLepRegion",
"ttWctrl":"DiLepRegion",
"ttHgeq4j":"DiLepRegion",
"TriLepRegion":"TriLepRegion",
"QuaLepRegion":"QuaLepRegion",
"ttZctrl":"ttZctrl",
"WZctrl":"WZctrl",
"QuaLepRegion":"QuaLepRegion",
"ZZctrl":"ZZctrl"
}
 
# input path

inputDirectories = "%s/%s/%s/%s/"%(inputDir,PostFix[region],year,PostFix[region]);
treename = "syncTree";

cut = ""
if region in Cuts:
    cut = Cuts[region]

# feature informations
features={
#"jet1_pt":{"nbin":25,"min":0.,"max":500.,"cut":"EventWeight %s"%cut,"xlabel":"jet1_pt"},
#"jet1_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"jet1_eta"},
"n_presel_jetFwd":{"nbin":5,"min":-0.5,"max":4.5,"cut":"EventWeight %s"%cut,"xlabel":"n_forwardJet"},
#"nBJetLoose":{"nbin":5,"min":-0.5,"max":4.5,"cut":"EventWeight %s"%cut,"xlabel":"nBJetLoose"},
"nElectron":{"nbin":3,"min":-0.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"nElectron"},
#"max_lep_eta":{"nbin":25,"min":0.,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"max lep |#eta|"},
}

#systematics=["nominal","bWeight","Prefire","lepSF"]
systematics=["nominal","Prefire","lepSF"]
Color={"nominal":kBlack,"noSF":kRed}

# regions and postfix

postfix = "_%s.root"%PostFix[region]
plotname = "%s_%i"%(region,year)

# root file names
sampleName = ["TTH","TTW","TTWW","TTZ","THQ","THW"]




# directory of output
outputdir = outputDir+"/SF_comparisons/"

# the root file saving the histograms
filename = "%s%s.root"%(outputdir,plotname)

# lumi information
luminosity = {2016: 35.92 , 2017: 41.53  , 2018: 59.74}

##### end user defined variables
# check outputdir
if not os.path.exists(outputdir):
    print ('mkdir: ', outputdir)
    os.makedirs(outputdir)

# create root file, this will overwrite the root file
if createROOTfile:
    exec(open("/home/binghuan/Work/Macros/plotters/make_SFhists.py").read())

def createRatio(h1, h2, POI, norm):
    if norm:
        h1.Scale(1./h1.Integral())
        h2.Scale(1./h2.Integral())
    h3 = h1.Clone("h3")
    h3.SetMarkerStyle(1)
    #h3.SetFillColor(0)
    #h3.SetLineWidth(2)
    #h3.SetMarkerColor(col)
    h3.SetTitle("")
    #h3.SetMinimum(0.8)
    #h3.SetMaximum(1.35)
    # Set up plot for markers and errors
    h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)
    
    # Adjust y-axis settings
    y = h3.GetYaxis()
    y.SetTitle("withSF/noSF")
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
    if(POI=="nElectron"):
        x.SetNdivisions(103)
        x.ChangeLabel(1,-1,-1,-1,-1,-1,"#mu#mu")
        x.ChangeLabel(2,-1,-1,-1,-1,-1,"e#mu")
        x.ChangeLabel(3,-1,-1,-1,-1,-1,"ee")
        x.SetLabelSize(40)
        x.SetTitle("")


    return h3

def createCanvasPads():
    c = TCanvas("c", "canvas", 800, 800)
    # Upper histogram plot is pad1
    pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0)  # joins upper and lower plot
    #pad1.SetLeftMargin(1.55)  # joins upper and lower plot
    pad1.SetTicks(0,1) 
    pad1.Draw()
    # Lower ratio plot is pad2
    c.cd()  # returns to main canvas before defining pad2
    pad2 = TPad("pad2", "pad2", 0, 0.01, 1, 0.3)
    pad2.SetTopMargin(0)  # joins upper and lower plot
    pad2.SetBottomMargin(0.28)
    pad2.SetTicks(0,1) 
    #pad2.SetGridx()
    pad2.Draw()

    return c, pad1, pad2


def plotSysts():
    inputfile = TFile(filename,"read")
    if inputfile.IsZombie():
        print("inputfile is Zombie")
        sys.exit()
    # loop over samples
    file = open("%s%s_isNorm%s_wtStat%s.txt"%(outputdir,plotname,normalization,showStats),"w")
    for sample in sampleName:
        # loop over features
        for feature, values in features.items():
            # get nominal histograms
            hist_nom_name = sample+"_"+feature
            if not inputfile.GetListOfKeys().Contains(hist_nom_name): 
                print ( "%s doesn't have histogram %s"%(filename, hist_nom_name))
                continue
            hist_nom = inputfile.Get(hist_nom_name)
            hist_nom.SetFillColor(0)
            hist_nom.SetLineWidth(2)
            hist_nom.SetLineColor(Color["nominal"])
            hist_nom.SetMarkerColor(Color["nominal"])
            #h_ratio = createRatio(hist_nom, hist_nom, values["xlabel"], Color["nominal"],normalization)
            h_ratio = createRatio(hist_nom, hist_nom, values["xlabel"], normalization)
            # loop over variations
            for syst in systematics:
                if syst=="nominal": continue
                file.write(" sample %s, feature %s, nominal yield %f\n"%(sample, feature, hist_nom.Integral()))
                
                # set up legend
                legend = TLegend(0.5,0.7,0.8,0.88)
                #legend.SetHeader("CMS preliminary %i  %s"%(year,region))
                #legend.SetNColumns(3)
                legend.SetBorderSize(0)
                
                legend.AddEntry(hist_nom,sample+"_with"+syst,"l")

                c, pad1, pad2 = createCanvasPads()
                hist_vars = []
                hist_ratio_vars = []
                hist_name = sample+"_"+feature+"_no"+syst
                if not inputfile.GetListOfKeys().Contains(hist_name): 
                    print ( "%s doesn't have histogram %s"%(filename, hist_name))
                    continue
                hist_var = inputfile.Get(hist_name)
                hist_var.SetFillColor(0)
                hist_var.SetLineWidth(2)
                hist_var.SetLineColor(Color["noSF"])
                hist_var.SetMarkerColor(Color["noSF"])
                hist_vars.append(hist_var)
                var_yield = hist_var.Integral()
                delta = (100.*(hist_nom.Integral()/var_yield - 1.))
                file.write(" sample {}, feature {}, no{} yield {} diff {}% \n".format(sample, feature, syst, var_yield, delta))
                #h_ratio_var = createRatio(hist_nom, hist_var,values["xlabel"], Color["noSF"], normalization)
                h_ratio_var = createRatio(hist_nom, hist_var,values["xlabel"],  normalization)
                hist_ratio_vars.append(h_ratio_var)
                legend.AddEntry(hist_var,sample+"_no"+syst,"l")
                
                # draw everything

                pad1.cd()
                #pad1.SetGridx()
                #pad1.SetGridy()
                
                # set bounds
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
                else:
                    hist_nom.SetStats(0)
                    
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
                x.SetTitleSize(30)
                x.SetTitleFont(43)
                x.SetTitleOffset(1.5)
                x.SetLabelFont(43)
                x.SetLabelSize(20)
                x.SetTitle(values["xlabel"])
                if(values["xlabel"]=="nElectron"):
                    x.SetNdivisions(103)
               
                hist_nom.SetTitle("#scale[1.0]{ %i at %.2f fb^{-1}(13TeV)}"%(year,luminosity[year]))
                hist_nom.GetXaxis().SetRangeUser(values["min"], values["max"])
                hist_nom.Draw("HIST")
                
                for hist in hist_vars:
                    hist.Draw("HISTsame") 

                legend.Draw("same")

                
                pad2.cd()
                #pad2.SetGridx(2)
                #pad2.SetGridy(2)
                bins = h_ratio.GetNbinsX()
                LowEdge = h_ratio.GetBinLowEdge(1)
                HighEdge = h_ratio.GetBinLowEdge(bins+1)
                #LowEdge = h_ratio.GetBinLowEdge(0)
                #HighEdge = h_ratio.GetBinLowEdge(bins+2)
                line = TLine(LowEdge,1,HighEdge,1)
                line.SetLineColor(kRed)
                for i in range(len(hist_ratio_vars)):
                    if i==0:
                        hist_ratio_vars[i].GetXaxis().SetRangeUser(values["min"], values["max"])
                        hist_ratio_vars[i].Draw("EP")
                        hist_ratio_vars[i].SetMinimum(0.7)
                        hist_ratio_vars[i].SetMaximum(1.3)
                    else:
                        hist_ratio_vars[i].Draw("EPsame")
                line.Draw("same")

                c.SaveAs("%s%s_%s_SF%s_isNorm%s_wtStat%s.png"%(outputdir,plotname,hist_nom_name,syst,normalization,showStats))
                #c.SaveAs("%s%s_%s_SF%s_isNorm%s_wtStat%s.root"%(outputdir,plotname,hist_nom_name,syst,normalization,showStats))
    file.close()

# Draw all canvases 
if __name__ == "__main__":
    gStyle.SetLegendTextSize(0.05)
    plotSysts()
