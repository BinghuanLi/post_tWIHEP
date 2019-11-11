import sys
import argparse
import os
from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TString, TFile, TH1, THStack, gROOT, TStyle, TAttFill, TLegend, TGraphAsymmErrors, TLine
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
parser.add_argument('-i', '--inputDir', nargs='?', help = 'inputDir', const="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/data/rootplas_V0_20190927/", default="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/data/rootplas_V0_20190927/")
parser.add_argument('-o', '--outputDir', nargs='?', help = 'outputDir', const="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/plots/rootplas_V0_20190927/", default="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/plots/rootplas_V0_20190927/")
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
"jet1_pt":{"nbin":25,"min":0.,"max":500.,"cut":"EventWeight %s"%cut,"xlabel":"jet1_pt"},
#"jet1_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"jet1_eta"},
}

systematics=["nominal","genWeight"]
#upDown=["_SysUp","_SysDown"]
upDown=["_muF0p5","_muF2","_muR0p5","_muR2"]
#Color={"nominal":kBlack,"_SysUp":kRed,"_SysDown":kBlue}
Color={"nominal":kBlack,"_muF0p5":kRed,"_muF2":kBlue, "_muR0p5":kCyan, "_muR2":kGreen}

# regions and postfix

postfix = "_%s.root"%PostFix[region]
plotname = "%s_%i"%(region,year)

# root file names
sampleName = ["TTH","TTW","TTWW","TTZ","THQ","THW"]




# directory of output
outputdir = "/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/plots/rootplas_V1_20190927/plots_DiLepRegion_variations/"

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
    # loop over samples
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
            hist_nom.SetLineColor(Color["nominal"])
            hist_nom.SetMarkerColor(Color["nominal"])
            h_ratio = createRatio(hist_nom, hist_nom, values["xlabel"],normalization)
            # loop over variations
            for syst in systematics:
                file = open("%s%s_%s_%s_isNorm%s_wtStat%s.txt"%(outputdir,plotname,hist_nom_name,syst,normalization,showStats),"w")
                file.write(" sample %s, feature %s, nominal yield %f\n"%(sample, feature, hist_nom.Integral()))
                if syst=="nominal": continue
                
                # set up legend
                legend = TLegend(0.2,0.6,0.7,0.88)
                legend.SetHeader("CMS preliminary %i  %s"%(year,region))
                #legend.SetNColumns(3)
                legend.SetBorderSize(0)
                
                legend.AddEntry(hist_nom,hist_nom_name,"l")

                c, pad1, pad2 = createCanvasPads()
                hist_vars = []
                hist_ratio_vars = []
                for var in upDown:
                    hist_name = sample+"_"+feature+"_"+syst+var
                    if not inputfile.GetListOfKeys().Contains(hist_name): 
                        print ( "%s doesn't have histogram %s"%(filename, hist_name))
                        continue
                    hist_var = inputfile.Get(hist_name)
                    hist_var.SetFillColor(0)
                    hist_var.SetLineColor(Color[var])
                    hist_var.SetMarkerColor(Color[var])
                    hist_vars.append(hist_var)
                    file.write(" sample %s, feature %s, %s%s yield %f \n"%(sample, feature, syst, var, hist_var.Integral()))
                    h_ratio_var = createRatio(hist_var, hist_nom,values["xlabel"], normalization)
                    hist_ratio_vars.append(h_ratio_var)
                    legend.AddEntry(h_ratio_var,hist_name,"l")
                
                # draw everything

                pad1.cd()
                pad1.SetGridx()
                pad1.SetGridy()
                
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
               
                hist_nom.SetTitle("#scale[0.9]{#font[22]{CMS} #font[12]{Preliminary}                                                            %i at %.2f fb^{-1}(13TeV)}"%(year,luminosity[year]))
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
                        hist_ratio_vars[i].Draw("hist")
                        hist_ratio_vars[i].SetMinimum(0.5)
                        hist_ratio_vars[i].SetMaximum(1.5)
                    else:
                        hist_ratio_vars[i].Draw("histsame")
                line.Draw("same")

                c.SaveAs("%s%s_%s_%s_isNorm%s_wtStat%s.png"%(outputdir,plotname,hist_nom_name,syst,normalization,showStats))
                file.close()

# Draw all canvases 
if __name__ == "__main__":
    plotSysts()
