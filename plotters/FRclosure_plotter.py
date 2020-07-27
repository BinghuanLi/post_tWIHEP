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
parser.add_argument('-r', '--region', nargs='?', help = 'region to plot', const="e", default="e")
parser.add_argument('-y', '--year', nargs='?', help = 'year to plot', const=2018, type=int ,default=2018)
parser.add_argument('-i', '--inputDir', nargs='?', help = 'inputDir', const="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/data/rootplas_closure_test/", default="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/data/rootplas_closure_test/")
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
#syncTree->Draw("jet1_pt>>h_e_TT(50,0,500)","(leadLep_mcPromptFS != 1 || secondLep_mcPromptFS!=1)*((leadLep_isMatchRightCharge==1 && secondLep_isMatchRightCharge==1 && FakeRate_m_TT == FakeRate_m_central))*(EventWeight/lepSF)*FakeRate_e_TT/FakeRate_e_central")
#syncTree->Draw("jet1_pt>>h_e_QCD(50,0,500)","(leadLep_mcPromptFS != 1 || secondLep_mcPromptFS!=1)*((leadLep_isMatchRightCharge==1 && secondLep_isMatchRightCharge==1 && FakeRate_m_TT == FakeRate_m_central))*(EventWeight/lepSF)*FakeRate_e_QCD/FakeRate_e_central")
#syncTree->Draw("jet1_pt>>h_m_TT(50,0,500)","(leadLep_mcPromptFS != 1 || secondLep_mcPromptFS!=1)*((leadLep_isMatchRightCharge==1 && secondLep_isMatchRightCharge==1 && FakeRate_e_TT == FakeRate_e_central))*(EventWeight/lepSF)*FakeRate_m_TT/FakeRate_m_central")
#syncTree->Draw("jet1_pt>>h_m_QCD(50,0,500)","(leadLep_mcPromptFS != 1 || secondLep_mcPromptFS!=1)*((leadLep_isMatchRightCharge==1 && secondLep_isMatchRightCharge==1 && FakeRate_e_TT == FakeRate_e_central))*(EventWeight/lepSF)*FakeRate_m_QCD/FakeRate_m_central")
#syncTree->Draw("jet1_pt>>h_m(50,0,500)","!((abs(lep1_pdgId)+abs(leadLep_mcPromptFS))==11 || (abs(lep2_pdgId)+abs(secondLep_mcPromptFS))==11) * EventWeight/lepSF")
#syncTree->Draw("jet1_pt>>h_e(50,0,500)","!((abs(lep1_pdgId)+abs(leadLep_mcPromptFS))==13 || (abs(lep2_pdgId)+abs(secondLep_mcPromptFS))==13) * EventWeight/lepSF")

Cuts = {
    "TT_mcFakes_mFakes":"* !((abs(lep1_pdgId)+abs(leadLep_mcPromptFS))==11 || (abs(lep2_pdgId)+abs(secondLep_mcPromptFS))==11)",
    "TT_ddFakes_mQCD":"* (leadLep_mcPromptFS != 1 || secondLep_mcPromptFS!=1)*((leadLep_isMatchRightCharge==1 && secondLep_isMatchRightCharge==1 && FakeRate_e_QCD == FakeRate_e_central))*FakeRate_m_QCD/FakeRate_m_central",
    "TT_ddFakes_mTT":"* (leadLep_mcPromptFS != 1 || secondLep_mcPromptFS!=1)*((leadLep_isMatchRightCharge==1 && secondLep_isMatchRightCharge==1 && FakeRate_e_TT == FakeRate_e_central))*FakeRate_m_TT/FakeRate_m_central",
    "TT_mcFakes_eFakes":"* !((abs(lep1_pdgId)+abs(leadLep_mcPromptFS))==13 || (abs(lep2_pdgId)+abs(secondLep_mcPromptFS))==13)",
    "TT_ddFakes_eQCD":"* (leadLep_mcPromptFS != 1 || secondLep_mcPromptFS!=1)*((leadLep_isMatchRightCharge==1 && secondLep_isMatchRightCharge==1 && FakeRate_m_QCD == FakeRate_m_central))*FakeRate_e_QCD/FakeRate_e_central",
    "TT_ddFakes_eTT":"* (leadLep_mcPromptFS != 1 || secondLep_mcPromptFS!=1)*((leadLep_isMatchRightCharge==1 && secondLep_isMatchRightCharge==1 && FakeRate_m_TT == FakeRate_m_central))*FakeRate_e_TT/FakeRate_e_central",
    }

# specify the corresponding root files used for each region
PostFix={
"DiLepRegion":"DiLepRegion",
"e":"DiLepRegion",
"m":"DiLepRegion",
}
 
# input path

inputDirectories = "%s/%s/%s/%s/"%(inputDir,PostFix[region],year,PostFix[region]);
treename = "syncTree";

systematics=["nominal","clos"]
upDown=["QCD","TT"]
Color={"nominal":kBlack,"QCD":kRed, "TT":kBlue}

# regions and postfix

postfix = "_%s.root"%PostFix[region]
plotname = "%sClos_%i"%(region,year)

# root file names
sampleName = ["TT_ddFakes","TT_mcFakes"]

cut = ""

# feature informations
features={
"jet1_pt":{"nbin":25,"min":0.,"max":500.,"cut":"(EventWeight/lepSF)","xlabel":"jet1_pt"},
"jet1_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight/lepSF","xlabel":"jet1_eta"},
"n_presel_jetFwd":{"nbin":5,"min":-0.5,"max":4.5,"cut":"EventWeight/lepSF","xlabel":"n_forwardJet"},
"nBJetLoose":{"nbin":4,"min":0.5,"max":4.5,"cut":"EventWeight/lepSF","xlabel":"nBJetLoose"},
"nBJetMedium":{"nbin":5,"min":-0.5,"max":4.5,"cut":"EventWeight/lepSF","xlabel":"nBJetLoose"},
"n_presel_jet":{"nbin":5,"min":-0.5,"max":4.5,"cut":"EventWeight/lepSF","xlabel":"n_jet"},
"nElectron":{"nbin":3,"min":-0.5,"max":2.5,"cut":"EventWeight/lepSF","xlabel":"nElectron"},
"max_lep_eta":{"nbin":15,"min":0.,"max":2.5,"cut":"EventWeight/lepSF","xlabel":"max lep |#eta|"},
"DNN_ttHnode_all":{"nbin":15,"min":0.,"max":1.,"cut":"EventWeight/lepSF","xlabel":"DNN_score_ttHnode"},
"DNN_Restnode_all":{"nbin":15,"min":0.,"max":1.,"cut":"EventWeight/lepSF","xlabel":"DNN_score_Restnode"},
"DNN_ttWnode_all":{"nbin":15,"min":0.,"max":1.,"cut":"EventWeight/lepSF","xlabel":"DNN_score_ttWnode"},
"DNN_tHQnode_all":{"nbin":15,"min":0.,"max":1.,"cut":"EventWeight/lepSF","xlabel":"DNN_score_tHQnode"},
"lep1_conePt":{"nbin":15,"min":0.,"max":150.,"cut":"EventWeight/lepSF","xlabel":"lep1_conePt"},
"lep2_conePt":{"nbin":15,"min":0.,"max":100.,"cut":"EventWeight/lepSF","xlabel":"lep2_conePt"},
"lep1_eta":{"nbin":15,"min":-2.5,"max":2.5,"cut":"EventWeight/lepSF","xlabel":"lep1 #eta"},
"lep2_eta":{"nbin":15,"min":-2.5,"max":2.5,"cut":"EventWeight/lepSF","xlabel":"lep2 #eta"},
}



# directory of output
outputdir = outputDir+"/FR_closure/"

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
    exec(open("/home/binghuan/Work/Macros/plotters/make_FRhists.py").read())

def createRatio(h1, h2, POI, norm):
    if norm:
        h1.Scale(1./h1.Integral())
        h2.Scale(1./h2.Integral())
    h3 = h1.Clone("h3")
    h3.SetMarkerStyle(1)
    #h3.SetFillColor(0)
    #h3.SetLineColor(col)
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
    y.SetTitle("FR/MC")
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
    # loop over samples
    file = open("%s%s_isNorm%s_wtStat%s.txt"%(outputdir,plotname,normalization,showStats),"w")
    # loop over features
    for feature, values in features.items():
        # get nominal histograms
        hist_nom_name = "TT_mcFakes_"+feature + "_" + region +"Fakes"
        if not inputfile.GetListOfKeys().Contains(hist_nom_name): 
            print ( "%s doesn't have histogram %s"%(filename, hist_nom_name))
            continue
        hist_nom = inputfile.Get(hist_nom_name)
        hist_nom.SetFillColor(0)
        hist_nom.SetLineColor(Color["nominal"])
        hist_nom.SetLineWidth(2)
        hist_nom.SetMarkerColor(Color["nominal"])
        #h_ratio = createRatio(hist_nom, hist_nom, values["xlabel"], Color["nominal"],normalization)
        h_ratio = createRatio(hist_nom, hist_nom, values["xlabel"], normalization)
        # loop over variations
        for syst in systematics:
            if syst=="nominal": continue
            file.write(" sample TT mcFakes, feature %s, nominal yield %f\n"%( feature, hist_nom.Integral()))
            
            # set up legend
            legend = TLegend(0.5,0.7,0.8,0.88)
            #legend.SetHeader("CMS preliminary %i  %s"%(year,region))
            #legend.SetNColumns(3)
            legend.SetBorderSize(0)
            
            legend.AddEntry(hist_nom,"TT_mcFakes_%s"%region,"l")

            c, pad1, pad2 = createCanvasPads()
            hist_vars = []
            hist_ratio_vars = []
            for var in upDown:
                hist_name = "TT_ddFakes_"+feature+"_"+syst+"_"+region+var
                if not inputfile.GetListOfKeys().Contains(hist_name): 
                    print ( "%s doesn't have histogram %s"%(filename, hist_name))
                    continue
                hist_var = inputfile.Get(hist_name)
                hist_var.SetFillColor(0)
                hist_var.SetLineColor(Color[var])
                hist_var.SetLineWidth(2)
                hist_var.SetMarkerColor(Color[var])
                hist_vars.append(hist_var)
                var_yield = hist_var.Integral()
                delta = (100.*(var_yield/hist_nom.Integral() - 1.))
                file.write(" sample TT ddFakes, feature {}, {}{} yield {} diff {}% \n".format( feature, syst, var, var_yield, delta))
                h_ratio_var = createRatio(hist_var, hist_nom,values["xlabel"], normalization)
                hist_ratio_vars.append(h_ratio_var)
                legend.AddEntry(h_ratio_var,"FR_%s_%s"%(var,region),"l")
            
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
            x.SetTitleSize(25)
            x.SetTitleFont(43)
            x.SetTitleOffset(1.55)
            x.SetLabelFont(43)
            x.SetLabelSize(20)
            x.SetTitle(values["xlabel"])
           
            hist_nom.SetTitle("#scale[1.0]{%i at %.2f fb^{-1}(13TeV)}"%(year,luminosity[year]))
            hist_nom.GetXaxis().SetRangeUser(values["min"], values["max"])
            hist_nom.Draw("EP")
            
            for hist in hist_vars:
                hist.Draw("EPsame") 

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
            line.SetLineColor(kBlack)
            h_ratio.GetXaxis().SetRangeUser(values["min"], values["max"])
            h_ratio.SetFillColor(kGray+3)
            h_ratio.SetFillStyle(3001)
            h_ratio.Draw("E2")
            h_ratio.SetMinimum(0.0)
            h_ratio.SetMaximum(2.0)
            for i in range(len(hist_ratio_vars)):
                hist_ratio_vars[i].Draw("EPsame")
            line.Draw("same")

            c.SaveAs("%s%s_%s_SF%s_isNorm%s_wtStat%s.png"%(outputdir,plotname,hist_nom_name,syst,normalization,showStats))
    file.close()

# Draw all canvases 
if __name__ == "__main__":
    gStyle.SetLegendTextSize(0.05)
    plotSysts()
