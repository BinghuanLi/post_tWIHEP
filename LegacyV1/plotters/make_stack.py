import sys
import argparse
import os
import math
from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TString, TFile, TH1, THStack, gROOT, TStyle, TAttFill, TLegend, TGraphAsymmErrors, TLine
from ROOT import kBlack, kBlue, kRed, kCyan, kViolet, kGreen, kOrange, kGray, kPink, kTRUE
from ROOT import Double
from ROOT import gROOT, gStyle

gROOT.SetBatch(1)

######### to run #########
#### python make_stack.py --createROOTfile --blind -r ttWctrl -y 2016 -i /home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/data/rootplas_V0_20190917/
##########################

#### start  user defined variables


# options
usage = 'usage: %prog [options]'
parser = argparse.ArgumentParser(usage)
parser.add_argument('-r', '--region', nargs='?', help = 'region to plot', const="DiLepRegion", default="DiLepRegion")
parser.add_argument('-y', '--year', nargs='?', help = 'year to plot', const=2018, type=int ,default=2018)
parser.add_argument('-i', '--inputDir', nargs='?', help = 'inputDir', const="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/data/rootplas_V0_20190917/", default="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/data/rootplas_V0_20190917/")
parser.add_argument('-o', '--outputDir', nargs='?', help = 'inputDir', const="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/plots/rootplas_V0_20190917/", default="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/plots/rootplas_V0_20190917/")
parser.add_argument('--blind', help='if blind: no data is plot, ratio is S/sqrt(B)', action='store_true')
parser.add_argument('--createROOTfile',        dest='createROOTfile'  ,      help='create or not the root files containing all the hist, must be true for the first time you run a given region',  action='store_true')


args = parser.parse_args()
region = args.region
year = args.year
inputDir = args.inputDir
outputDir = args.outputDir
createROOTfile = args.createROOTfile
blind = args.blind

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
"jet1_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"jet1_eta"},
"jet1_phi":{"nbin":25,"min":-3.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"jet1_phi"},
"jet1_E":{"nbin":25,"min":0.,"max":500,"cut":"EventWeight %s"%cut,"xlabel":"jet1_energy"},
"jet1_QGdiscr":{"nbin":25,"min":0.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"jet1_QGdiscr"},
"jet1_DeepJet":{"nbin":25,"min":0.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"jet1_DeepJet"},
"jet2_pt":{"nbin":25,"min":0.,"max":250.,"cut":"EventWeight %s"%cut,"xlabel":"jet2_pt"},
"jet2_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"jet2_eta"},
"jet2_phi":{"nbin":25,"min":-3.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"jet2_phi"},
"jet2_E":{"nbin":25,"min":0.,"max":500,"cut":"EventWeight %s"%cut,"xlabel":"jet2_energy"},
"jet2_QGdiscr":{"nbin":25,"min":0.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"jet2_QGdiscr"},
"jet2_DeepJet":{"nbin":25,"min":0.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"jet2_DeepJet"},
"jet3_pt":{"nbin":25,"min":0.,"max":250.,"cut":"EventWeight %s"%cut,"xlabel":"jet3_pt"},
"jet3_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"jet3_eta"},
"jet3_phi":{"nbin":25,"min":-3.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"jet3_phi"},
"jet3_E":{"nbin":25,"min":0.,"max":500,"cut":"EventWeight %s"%cut,"xlabel":"jet3_energy"},
"jet3_QGdiscr":{"nbin":25,"min":0.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"jet3_QGdiscr"},
"jet3_DeepJet":{"nbin":25,"min":0.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"jet3_DeepJet"},
"jet4_pt":{"nbin":25,"min":0.,"max":250.,"cut":"EventWeight %s"%cut,"xlabel":"jet4_pt"},
"jet4_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"jet4_eta"},
"jet4_phi":{"nbin":25,"min":-3.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"jet4_phi"},
"jet4_E":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"jet4_energy"},
"jet4_QGdiscr":{"nbin":25,"min":0.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"jet4_QGdiscr"},
"jet4_DeepJet":{"nbin":25,"min":0.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"jet4_DeepJet"},
"jetFwd1_pt":{"nbin":25,"min":0.,"max":250.,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd1_pt"},
"jetFwd1_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd1_eta"},
"jetFwd1_phi":{"nbin":25,"min":-3.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd1_phi"},
"jetFwd1_E":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd1_energy"},
"jetFwd2_pt":{"nbin":25,"min":0.,"max":250.,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd2_pt"},
"jetFwd2_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd2_eta"},
"jetFwd2_phi":{"nbin":25,"min":-3.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd2_phi"},
"jetFwd2_E":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd2_energy"},
"jetFwd3_pt":{"nbin":25,"min":0.,"max":250.,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd3_pt"},
"jetFwd3_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd3_eta"},
"jetFwd3_phi":{"nbin":25,"min":-3.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd3_phi"},
"jetFwd3_E":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd3_energy"},
"jetFwd4_pt":{"nbin":25,"min":0.,"max":250.,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd4_pt"},
"jetFwd4_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd4_eta"},
"jetFwd4_phi":{"nbin":25,"min":-3.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd4_phi"},
"jetFwd4_E":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"jetFwd4_energy"},
"PFMET":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"PFMET"},
"PFMETphi":{"nbin":25,"min":-3.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"PFMETphi"},
"MHT":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"MHT"},
"metLD":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"metLD"},
"lep1_conePt":{"nbin":25,"min":0.,"max":250.,"cut":"EventWeight %s"%cut,"xlabel":"lep1_pt"},
"lep1_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"lep1_eta"},
"lep1_phi":{"nbin":25,"min":-3.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"lep1_phi"},
"lep1_E":{"nbin":25,"min":0.,"max":500,"cut":"EventWeight %s"%cut,"xlabel":"lep1_energy"},
"lep2_conePt":{"nbin":25,"min":0.,"max":250.,"cut":"EventWeight %s"%cut,"xlabel":"lep2_pt"},
"lep2_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"lep2_eta"},
"lep2_phi":{"nbin":25,"min":-3.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"lep2_phi"},
"lep2_E":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"lep2_energy"},
"lep3_conePt":{"nbin":25,"min":0.,"max":250.,"cut":"EventWeight %s"%cut,"xlabel":"lep3_pt"},
"lep3_eta":{"nbin":25,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"lep3_eta"},
"lep3_phi":{"nbin":25,"min":-3.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"lep3_phi"},
"lep3_E":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"lep3_energy"},
"mindr_lep1_jet":{"nbin":25,"min":0.,"max":5.0,"cut":"EventWeight %s"%cut,"xlabel":"mindr_lep1_jet"},
"mindr_lep2_jet":{"nbin":25,"min":0.,"max":5.0,"cut":"EventWeight %s"%cut,"xlabel":"mindr_lep2_jet"},
"mindr_lep3_jet":{"nbin":25,"min":0.,"max":5.0,"cut":"EventWeight %s"%cut,"xlabel":"mindr_lep3_jet"},
"min_dr_lep_jet":{"nbin":25,"min":0.,"max":5.0,"cut":"EventWeight %s"%cut,"xlabel":"min_dr_lep_jet"},
"max_lep_eta":{"nbin":25,"min":0.,"max":3.0,"cut":"EventWeight %s"%cut,"xlabel":"max_lep_eta"},
"dr_leps":{"nbin":25,"min":0.,"max":5.0,"cut":"EventWeight %s"%cut,"xlabel":"dr_leps"},
"nLightJet":{"nbin":6,"min":-0.5,"max":5.5,"cut":"EventWeight %s"%cut,"xlabel":"nLightJet"},
"min_Deta_mostfwdJet_jet":{"nbin":25,"min":0.,"max":5,"cut":"EventWeight %s"%cut,"xlabel":"min_Deta_mostfwdJet_jet"},
"min_Deta_leadfwdJet_jet":{"nbin":25,"min":0.,"max":5,"cut":"EventWeight %s"%cut,"xlabel":"min_Deta_leadfwdJet_jet"},
"mT2_top_3particle":{"nbin":25,"min":0.,"max":500,"cut":"EventWeight %s"%cut,"xlabel":"mT2_top_3particle"},
"mT2_top_2particle":{"nbin":25,"min":0.,"max":500,"cut":"EventWeight %s"%cut,"xlabel":"mT2_top_2particle"},
"mT2_W":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"mT2_W"},
"angle_bbpp_highest2b":{"nbin":25,"min":0.,"max":3.3,"cut":"EventWeight %s"%cut,"xlabel":"angle_bbpp_highest2b"},
"mbb":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"mbb"},
"mbb_loose":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"mbb_loose"},
"hadTop_BDT":{"nbin":25,"min":-1.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"hadTop_BDT"},
"hadTop_pt":{"nbin":25,"min":0.,"max":500,"cut":"EventWeight %s"%cut,"xlabel":"hadTop_pt"},
"Hj_tagger_hadTop":{"nbin":25,"min":-1.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"Hj_tagger_hadTop"},
"Hj_tagger":{"nbin":25,"min":-1.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"Hj_tagger"},
"nBJetLoose":{"nbin":6,"min":-0.5,"max":5.5,"cut":"EventWeight %s"%cut,"xlabel":"nBJetLoose"},
"nBJetMedium":{"nbin":6,"min":-0.5,"max":5.5,"cut":"EventWeight %s"%cut,"xlabel":"nBJetMedium"},
"mvaOutput_2lss_ttbar":{"nbin":25,"min":-1.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"mvaOutput_2lss_ttbar"},
"mvaOutput_2lss_ttV":{"nbin":25,"min":-1.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"mvaOutput_2lss_ttV"},
"avg_dr_jet":{"nbin":25,"min":-0.,"max":6.,"cut":"EventWeight %s"%cut,"xlabel":"avg_dr_jet"},
"n_presel_mu":{"nbin":6,"min":-0.5,"max":5.5,"cut":"EventWeight %s"%cut,"xlabel":"n_presel_mu"},
"n_fakeablesel_mu":{"nbin":5,"min":-0.5,"max":4.5,"cut":"EventWeight %s"%cut,"xlabel":"n_fakeablesel_mu"},
"n_mvasel_mu":{"nbin":4,"min":-0.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"n_mvasel_mu"},
"n_presel_ele":{"nbin":6,"min":-0.5,"max":5.5,"cut":"EventWeight %s"%cut,"xlabel":"n_presel_ele"},
"n_fakeablesel_ele":{"nbin":5,"min":-0.5,"max":4.5,"cut":"EventWeight %s"%cut,"xlabel":"n_fakeablesel_ele"},
"n_mvasel_ele":{"nbin":4,"min":-0.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"n_mvasel_ele"},
"n_presel_tau":{"nbin":4,"min":-0.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"n_presel_tau"},
"n_presel_jet":{"nbin":8,"min":-0.5,"max":7.5,"cut":"EventWeight %s"%cut,"xlabel":"n_presel_jet"},
"n_presel_jetFwd":{"nbin":5,"min":-0.5,"max":4.5,"cut":"EventWeight %s"%cut,"xlabel":"n_presel_jetFwd"},
"Bin2l":{"nbin":11,"min":0.5,"max":11.5,"cut":"EventWeight %s"%cut,"xlabel":"Bin2l"},
"massl":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"massl"},
"massL":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"massL"},
"massL_SFOS":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"massL_SFOS"},
"maxeta":{"nbin":25,"min":0.,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"maxeta"},
"Sum2lCharge":{"nbin":5,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"Sum2lCharge"},
"Dilep_bestMVA":{"nbin":25,"min":0.7,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"Dilep_bestMVA"},
"Dilep_worseMVA":{"nbin":25,"min":0.7,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"Dilep_worseMVA"},
"nElectron":{"nbin":3,"min":-0.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"nElectron"},
"Dilep_htllv":{"nbin":25,"min":0.,"max":500,"cut":"EventWeight %s"%cut,"xlabel":"Dilep_htllv"},
"Dilep_mtWmin":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"Dilep_mtWmin"},
"Dilep_nTight":{"nbin":3,"min":-0.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"Dilep_nTight"},
"HtJet":{"nbin":25,"min":0.,"max":500,"cut":"EventWeight %s"%cut,"xlabel":"HtJet"},
"nLepTight":{"nbin":4,"min":-0.5,"max":3.5,"cut":"EventWeight %s"%cut,"xlabel":"nLepTight"},
"minMllAFAS":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"minMllAFAS"},
"minMllAFOS":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"minMllAFOS"},
"minMllSFOS":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"minMllSFOS"},
"mass3L":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"mass3L"},
"massLT":{"nbin":25,"min":0.,"max":250,"cut":"EventWeight %s"%cut,"xlabel":"massLT"},
"nBestVtx":{"nbin":100,"min":-0.5,"max":100,"cut":"EventWeight %s"%cut,"xlabel":"nBestVtx"},
"Sum3LCharge":{"nbin":5,"min":-2.5,"max":2.5,"cut":"EventWeight %s"%cut,"xlabel":"Sum3LCharge"},
"lep1_charge":{"nbin":3,"min":-1.5,"max":1.5,"cut":"EventWeight %s"%cut,"xlabel":"lep1_charge"},
"lep2_charge":{"nbin":3,"min":-1.5,"max":1.5,"cut":"EventWeight %s"%cut,"xlabel":"lep2_charge"},
"lep3_charge":{"nbin":3,"min":-1.5,"max":1.5,"cut":"EventWeight %s"%cut,"xlabel":"lep3_charge"},
"leadLep_BDT":{"nbin":25,"min":-1.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"leadLep_BDT"},
"secondLep_BDT":{"nbin":25,"min":-1.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"secondLep_BDT"},
"lep3_BDT":{"nbin":25,"min":-1.,"max":1.,"cut":"EventWeight %s"%cut,"xlabel":"lep3_BDT"},

}

systematics=["nominal"]
upDown=["_SysUp","_SysDown"]
Color={"TTH":kRed,"TH":kBlue,"TTZ":kGreen,"TTW+TTWW":kGreen+3,"Conv":kOrange,"EWK":kViolet,"WZ+ZZ":kViolet-3,"Rares":kCyan,"Fakes":kBlack,"Flips":kBlack,"mcFakes":kBlack,"mcFlips":kBlack,"ST":kGray,"VH+ggH+qqH":kBlue-7}
Style={"TTH":1001,"TH":1001,"TTZ":1001,"TTW+TTWW":1001,"Conv":1001,"EWK":1001,"WZ+ZZ":1001,"Rares":1001,"Fakes":3005,"Flips":3006,"mcFakes":3005,"mcFlips":3006,"ST":1001,"VH+ggH+qqH":1001}

# regions and postfix

postfix = "_%s.root"%PostFix[region]
plotname = "%s_%i"%(region,year)

# root file names
sampleName = [ "TTH","THQ", "THW", "VH", "ZH", "ggH", "qqH", "TTZ", "TTW", "Convs", "WZ", "ZZ", "EWK", "Rares","TTWW","ST", "mcFlips", "mcFakes", "Data",
"ggH_hmm","ggH_htt","ggH_hww","ggH_hzg","ggH_hzz", "qqH_hmm","qqH_htt","qqH_hww","qqH_hzg","qqH_hzz", "VH_hmm","VH_htt","VH_hww","VH_hzg","VH_hzz", "ZH_hmm","ZH_htt","ZH_hww","ZH_hzg","ZH_hzz", "TTH_hmm","TTH_htt","TTH_hww","TTH_hzg","TTH_hzz", "THQ_hmm","THQ_htt","THQ_hww","THQ_hzg","THQ_hzz", "THW_hmm","THW_htt","THW_hww","THW_hzg","THW_hzz"]


# set up the way we plot the samples
Signals=["TTH","TH","VH+ggH+qqH"]
#Samples=["TTH","TH","VH+ggH+qqH","TTW+TTWW","TTZ","EWK","WZ+ZZ","Rares","Conv","ST","mcFakes","mcFlips","Data"]
Samples=  ['Data', 'mcFlips', 'mcFakes', 'ST', 'Conv', 'Rares', 'WZ+ZZ', 'EWK', 'TTZ', 'TTW+TTWW', 'VH+ggH+qqH', 'TH', 'TTH']

Process={
    "TTH":["TTH_hww","TTH_hzz","TTH_htt","TTH_hmm","TTH_hzg"],
    "TH":["THW_hww","THW_hzz","THW_htt","THW_hmm","THW_hzg","THQ_hww","THQ_hzz","THQ_htt","THQ_hmm","THQ_hzg"],
    "VH+ggH+qqH":["ggH_hmm","ggH_htt","ggH_hww","ggH_hzg","ggH_hzz", "qqH_hmm","qqH_htt","qqH_hww","qqH_hzg","qqH_hzz", "VH_hmm","VH_htt","VH_hww","VH_hzg","VH_hzz", "ZH_hmm","ZH_htt","ZH_hww","ZH_hzg","ZH_hzz"],
    "TTZ":["TTZ"],"TTW+TTWW":["TTW","TTWW"],"Conv":["Convs"],"EWK":["EWK"],"WZ+ZZ":["WZ","ZZ"],"Rares":["Rares"],"Fakes":["Fakes","FakeSub"],"Flips":["Flips"],"Data":["Data"],
    "ST":["ST"],"mcFlips":["mcFlips"],"mcFakes":["mcFakes"]
    }




# directory of output
outputdir = "%s/plots_%s/"%(outputDir,region)

# the root file saving the histograms
filename = "%s%s.root"%(outputdir,plotname)

# lumi information
luminosity = {2016: 35.92 , 2017: 41.53  , 2018: 59.74}

# dummy options, please don't change it
normalization = False # Normalize to unit 
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
    h3.SetLineColor(kBlack)
    h3.SetMarkerStyle(20)
    h3.SetTitle("")
    #h3.SetMinimum(0.8)
    #h3.SetMaximum(1.35)
    # Set up plot for markers and errors
    h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)
    
    # Adjust y-axis settings
    y = h3.GetYaxis()
    if not blind:
        y.SetTitle("Data/Pred.")
    else:
        y.SetTitle("S/#sqrt{B}")
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

def createSqrt(h1):
    h2 = h1.Clone("h2")
    h2.SetLineColor(kBlack)
    h2.SetMarkerStyle(20)
    h2.SetTitle("")
    #h2.SetMinimum(0.8)
    #h2.SetMaximum(1.35)
    # Set up plot for markers and errors
    h2.Sumw2()
    h2.SetStats(0)
    nbins = h2.GetNbinsX()
    for b in range(nbins+1):
        BinContent = h2.GetBinContent(b)
        BinContentErr = h2.GetBinError(b)
        #print "Bin "+str(b)+" BinContent "+str(BinContent)+" BinContentErr "+str(BinContentErr)
        BinValue = 0
        if BinContent > 0: 
            BinValue = math.sqrt(BinContent)
            h2.SetBinContent(b,BinValue)
            h2.SetBinError(b,BinContentErr/(2*BinValue))
        else: 
            h2.SetBinContent(b,0)
            h2.SetBinError(b,0)
    return h2

def createTotalMCErr(h1, POI):
    h2 = h1.Clone("h2")
    h2.Sumw2()
    nbins = h2.GetNbinsX()

    # Adjust y-axis settings
    y = h2.GetYaxis()
    if blind :
        y.SetTitle("S/#sqrt{B}")
    else:
        for b in range(nbins+1):
            BinContent = h2.GetBinContent(b)
            BinContentErr = h2.GetBinError(b)
            #print "Bin "+str(b)+" BinContent "+str(BinContent)+" BinContentErr "+str(BinContentErr)
            h2.SetBinContent(b,1)
            if BinContent != 0 : h2.SetBinError(b,BinContentErr/BinContent)
            else: h2.SetBinError(b,0)
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


def plotStack():
    inputfile = TFile(filename,"read")
    if inputfile.IsZombie():
        print("inputfile is Zombie")
        sys.exit()
    
     
    # loop over features
    for feature, values in features.items():
        file = open("%s%s_%s_isNorm%s_wtStat%s_isBlind%s.txt"%(outputdir,feature,plotname,normalization,showStats,blind),"w")
        
        file.write("\\begin{table}[]\n\\resizebox{!}{.33\\paperheight}{\n \\begin{tabular}{|l|l|l|}\n\\hline\nProcess & Yield & Entries \\\\ \\hline \n")
        # set up legend
        legend = TLegend(0.2,0.6,0.7,0.88)
        legend.SetHeader("%i  %s"%(year,region))
        legend.SetNColumns(4)
        legend.SetBorderSize(0)
                
        c, pad1, pad2 = createCanvasPads()

        hstack = THStack("hstack","hstack")
        hstack.SetTitle("#scale[0.9]{#font[22]{CMS} #font[12]{Preliminary}                                                            %i at %.2f fb^{-1}(13TeV)}"%(year,luminosity[year]))
            
        histName = "TTH_"+feature  # assuming TTH is always there
        if not inputfile.GetListOfKeys().Contains(histName): 
            print ( "%s doesn't have histogram %s, please use another hist "%(inputfile, histName))
            sys.exit()

        h0 = inputfile.Get(histName)
    
        h_totalsig = h0.Clone("h_totalsig")
        h_totalsig.SetDirectory(0)
        h_totalsig.Reset()
        h_totalsig.SetMarkerStyle(20)
        h_totalsig.Sumw2()
        
        h_totalbkg = h0.Clone("h_totalbkg")
        h_totalbkg.SetDirectory(0)
        h_totalbkg.Reset()
        h_totalbkg.SetMarkerStyle(20)
        h_totalbkg.Sumw2()
        
        h_totalmc = h0.Clone("h_totalmc")
        h_totalmc.SetDirectory(0)
        h_totalmc.Reset()
        h_totalmc.SetLineColor(kBlack)
        h_totalmc.SetFillColor(kGray+3)
        h_totalmc.SetFillStyle(3001)
        h_totalmc.SetTitle("")
        #h_totalmc.SetMinimum(0.8)
        #h_totalmc.SetMaximum(1.35)
        h_totalmc.Sumw2()
        h_totalmc.SetStats(0)
    
        h_dataobs = h0.Clone("h_dataobs")
        h_dataobs.SetDirectory(0)
        h_dataobs.Reset()
        h_dataobs.SetMarkerStyle(20)
        
        # loop over samples
        for sample in Samples:
            hist = h_totalmc.Clone(sample)
            hist.SetDirectory(0)
            hist.Reset()
            if sample not in Process:
                print ( "sample %s is not in Process "%sample)
                continue 
            # loop over data:
            if sample == "Data" or sample == "data":
                for p in Process[sample]:
                    if p not in sampleName:
                        print ("process %s is not in sampleName "%s)
                        continue
                    hist_name = p + "_" + feature
                    if not inputfile.GetListOfKeys().Contains(hist_name): 
                        print ( "%s doesn't have histogram %s"%(inputfile, hist_name))
                        continue
                    h1 = inputfile.Get(hist_name).Clone(hist_name)
                    h1.SetDirectory(0)
                    h_dataobs.Add(h1)
                    error = Double(0)
                    h1.IntegralAndError(0,h1.GetNbinsX(),error)
                    if not blind:
                        file.write("%s &  %.2f +/- %.2f &   %i \\\\ \\hline \n"%(p.replace('_','\\_'),h1.Integral(),error, h1.GetEntries()))
            # loop over mc
            # loop over signal
            elif sample in Signals:
                for p in Process[sample]:
                    if p not in sampleName:
                        print ("process %s is not in sampleName "%s)
                        continue
                    hist_name = p + "_" + feature
                    if not inputfile.GetListOfKeys().Contains(hist_name): 
                        print ( "%s doesn't have histogram %s"%(filename, hist_name))
                        continue
                    h1 = inputfile.Get(hist_name).Clone(hist_name)
                    h1.SetDirectory(0)
                    if p == "FakeSub" and sample == "Fakes":
                        hist.Add(h1,-1)
                        h_totalsig.Add(h1,-1)
                        h_totalmc.Add(h1,-1)
                    else:
                        hist.Add(h1)
                        h_totalsig.Add(h1)
                        h_totalmc.Add(h1)
                    error = Double(0)
                    h1.IntegralAndError(0,h1.GetNbinsX(),error)
                    if h1.Integral() < 0.05 or h1.GetEntries() < 100:
                        file.write("\\textcolor{red}{%s} &  %.2f +/- %.2f &   %i \\\\ \\hline \n"%(p.replace('_','\\_'),h1.Integral(),error, h1.GetEntries()))
                    else:
                        file.write("%s &  %.2f +/- %.2f &   %i \\\\ \\hline \n"%(p.replace('_','\\_'),h1.Integral(),error, h1.GetEntries()))
                hist.SetFillColor(Color[sample])
                hist.SetLineColor(kBlack)
                hist.SetFillStyle(Style[sample])
                hstack.Add(hist)
                legend.AddEntry(hist,sample,"f")
                     
        # create required parts
            # loop over bkg
            else:
                for p in Process[sample]:
                    if p not in sampleName:
                        print ("process %s is not in sampleName "%p)
                        continue
                    hist_name = p + "_" + feature
                    if not inputfile.GetListOfKeys().Contains(hist_name): 
                        print ( "%s doesn't have histogram %s"%(filename, hist_name))
                        continue
                    h1 = inputfile.Get(hist_name).Clone(hist_name)
                    h1.SetDirectory(0)
                    if p == "FakeSub" and sample == "Fakes":
                        hist.Add(h1,-1)
                        h_totalmc.Add(h1,-1)
                        h_totalbkg.Add(h1,-1)
                    else:
                        hist.Add(h1)
                        h_totalmc.Add(h1)
                        h_totalbkg.Add(h1)
                    error = Double(0)
                    h1.IntegralAndError(0,h1.GetNbinsX(),error)
                    if h1.Integral() < 0.05 or h1.GetEntries() < 100:
                        file.write("\\textcolor{red}{%s} &  %.2f +/- %.2f &   %i \\\\ \\hline \n"%(p.replace('_','\\_'),h1.Integral(),error, h1.GetEntries()))
                    else:
                        file.write("%s &  %.2f +/- %.2f &   %i \\\\ \\hline \n"%(p.replace('_','\\_'),h1.Integral(),error, h1.GetEntries()))
                hist.SetFillColor(Color[sample])
                hist.SetLineColor(kBlack)
                hist.SetFillStyle(Style[sample])
                hstack.Add(hist)
                legend.AddEntry(hist,sample,"f")
                     
        error = Double(0)
        h_totalsig.IntegralAndError(0,h_totalsig.GetNbinsX(),error)
        file.write("signal &  %.2f +/- %.2f &   %i \\\\ \\hline \n"%(h_totalsig.Integral(),error, h_totalsig.GetEntries()))
        
        error = Double(0)
        h_totalbkg.IntegralAndError(0,h_totalbkg.GetNbinsX(),error)
        file.write("bkg &  %.2f +/- %.2f &   %i \\\\ \\hline \n"%(h_totalbkg.Integral(),error, h_totalbkg.GetEntries()))
        
        # create required parts
        
        if blind :
            h_sqrtB = createSqrt(h_totalbkg)
            h_MCerr = createTotalMCErr(h_sqrtB, values["xlabel"])
            h_ratio = createRatio(h_totalsig, h_sqrtB, values["xlabel"], normalization)
        else:
            h_MCerr = createTotalMCErr(h_totalmc, feature)
            h_ratio = createRatio(h_dataobs, h_totalmc, values["xlabel"], normalization)
            legend.AddEntry(h_dataobs,"observed","lep")
        
        legend.AddEntry(h_totalmc,"Uncertainty","f")
        
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
        
        nbins = h_ratio.GetNbinsX()
        hstack.GetXaxis().SetRange(0, nbins+1)
        
        h_totalmc.Draw("e2same")
        if not blind:
            h_dataobs.Draw("same")
        legend.Draw("same")
            
    
        pad2.cd()
        if blind :
            h_ratio.SetMinimum(0.)
            #maximum = h_ratio.GetMaximum()
            #upperbound = 1.5*maximum
            #h_ratio.SetMaximum(upperbound)
            h_ratio.SetMaximum(3.)
            h_ratio.Draw("")
        else:
            h_MCerr.SetMinimum(0.5)
            h_MCerr.SetMaximum(1.8)
            h_MCerr.Draw("e2") 
            h_ratio.Draw("same")

  
        c.SaveAs("%s%s_%s_isNorm%s_wtStat%s_isBlind%s_stack.png"%(outputdir,feature,plotname,normalization,showStats,blind))
        file.write("\\end{tabular}\n}\n\\end{table}\n")
        file.close()
    inputfile.Close()

# Draw all canvases 
if __name__ == "__main__":
    plotStack()
