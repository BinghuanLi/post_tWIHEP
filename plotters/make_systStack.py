import sys
import argparse
import os
import math
from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TString, TFile, TH1, THStack, gROOT, TStyle, TAttFill, TLegend, TGraphAsymmErrors, TLine, gStyle
from ROOT import kBlack, kBlue, kRed, kCyan, kViolet, kGreen, kOrange, kGray, kPink, kTRUE
from ROOT import Double
from ROOT import gROOT 

gROOT.SetBatch(1)

######### to run #########
## python make_systStack.py  -y runII -c DNNSubCat2_option1 -n inclusive -r 2lss_0tau --createROOTfile
##########################

#### start  user defined variables


# options
usage = 'usage: %prog [options]'
parser = argparse.ArgumentParser(usage)
parser.add_argument('-r', '--region', nargs='?', help = 'region to plot', const="2lss_0tau", default="2lss_0tau")
parser.add_argument('-n', '--cutname', nargs='?', help = 'cutname to plot', const="inclusive", default="inclusive")
parser.add_argument('-y', '--year', nargs='?', help = 'year to plot', const="2018",default="2018")
parser.add_argument('-t', '--tH', nargs='?', help = 'tHq scaling factor', const=3, type=int ,default=1)
parser.add_argument('-i', '--inputDir', nargs='?', help = 'inputDir', const="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/plots/mvaTool_LegacyAll_20200611/ttH_2lss_0tau_newFr_20200611_datacards/", default="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/plots/mvaTool_LegacyAll_20200611/ttH_2lss_0tau_20200611_SM_results_datacards/")
parser.add_argument('-o', '--outputDir', nargs='?', help = 'outputDir', const="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/plots/mvaTool_LegacyAll_20200611/ttH_2lss_0tau_newFr_20200611_datacards/", default="/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/plots/mvaTool_LegacyAll_20200611/ttH_2lss_0tau_20200611_SM_results_datacards/")
parser.add_argument('--blind', help='if blind: no data is plot, ratio is S/sqrt(B)', action='store_true')
parser.add_argument('--createROOTfile',        dest='createROOTfile'  ,      help='create or not the root files containing all the hist, must be true for the first time you run a given region',  action='store_true')
parser.add_argument('-c', '--catflag', nargs='?', help = 'category flag', const="SubCat2l", default="SubCat2l")


args = parser.parse_args()
region = args.region
cutname = args.cutname
catflag = args.catflag
year = args.year
inputDir = args.inputDir
outputDir = args.outputDir
createROOTfile = args.createROOTfile
blind = args.blind
tH = args.tH
print ( " scale tH by %i "%tH)

# dictionaries
# specify additional cuts for some regions
Color={"TTH":kRed,"TH":kRed+3,"TTZ":kGreen,"TTW+TTWW":kGreen+3,"Conv":kOrange,"EWK":kViolet,"WZ+ZZ":kViolet-3,"Rares":kCyan,"Fakes":kBlack,"Flips":kBlack,"mcFakes":kBlack,"mcFlips":kBlack,"ST":kGray,"HOther":kBlue-7, "WZ":kViolet, "ZZ": kViolet-3, "ggZZ":kViolet+3}
Style={"TTH":1001,"TH":1001,"TTZ":1001,"TTW+TTWW":1001,"Conv":1001,"EWK":1001,"WZ+ZZ":1001,"Rares":1001,"Fakes":3005,"Flips":3006,"mcFakes":3005,"mcFlips":3006,"ST":1001,"HOther":1001,"WZ":1001, "ZZ": 1001, "ggZZ":1001}

# regions and postfix

plotname = "%s_%s_%s_%s"%(region, catflag, cutname,year)


# set up the way we plot the samples
Signals=["TTH","TH"]
#Samples=["TTH","TH","VH+ggH+qqH","TTW+TTWW","TTZ","EWK","WZ+ZZ","Rares","Conv","ST","mcFakes","mcFlips","Data"]
#Samples=  ['Data', 'Fakes', 'Conv', 'Rares', 'WZ', 'ggZZ', 'ZZ', 'TTZ', 'TTW+TTWW', 'HOther', 'TH', 'TTH']
#Samples=  ['Data', 'Fakes', 'Conv', 'Rares', 'WZ', 'ZZ', 'TTZ', 'TTW+TTWW', 'HOther', 'TH', 'TTH','Flips']
Samples=  ['Data', 'Flips', 'Fakes', 'Conv', 'Rares', 'WZ+ZZ', 'TTZ', 'TTW+TTWW', 'HOther', 'TH', 'TTH']

Process={
    "TTH":["ttH_hww","ttH_hzz","ttH_htt","ttH_hmm","ttH_hzg"],
    "TH":["tHW_hww","tHW_hzz","tHW_htt","tHq_hww","tHq_hzz","tHq_htt"],
    "VH+ggH+qqH":["ggH_hmm","ggH_htt","ggH_hww","ggH_hzg","ggH_hzz", "qqH_hmm","qqH_htt","qqH_hww","qqH_hzg","qqH_hzz", "VH_hmm","VH_htt","VH_hww","VH_hzg","VH_hzz", "ZH_hmm","ZH_htt","ZH_hww","ZH_hzg","ZH_hzz"],
    "HOther":["ggH_htt","ggH_hww","ggH_hzz", "qqH_htt","qqH_hww","qqH_hzz","WH_htt","WH_hww","WH_hzz","ZH_htt","ZH_hww","ZH_hzz","TTWH_htt","TTWH_hww","TTWH_hzz","TTZH_htt","TTZH_hww","TTZH_hzz"],
    "TTZ":["TTZ"],"TTW+TTWW":["TTW","TTWW"],"Conv":["Convs"],"EWK":["EWK"],"WZ+ZZ":["WZ","ZZ"],"Rares":["Rares"],"Fakes":["data_fakes"],"Flips":["data_flips"],"Data":["data_obs"],
    "ST":["ST"],"mcFlips":["mcFlips"],"mcFakes":["mcFakes"],
    "WZ":["WZ"], "ZZ":["ZZ"], "ggZZ":["ggZZ"],
    }


# hist file names
sampleName = [ 
"data_obs","data_fakes","data_flips",
"TTZ","TTW","Convs","WZ", "ZZ", "Rares","TTWW",
"ggH_htt","ggH_hww","ggH_hzz", "qqH_htt","qqH_hww","qqH_hzz", "WH_htt","WH_hww","WH_hzz", "ZH_htt","ZH_hww","ZH_hzz", "ttH_hmm","ttH_htt","ttH_hww","ttH_hzg","ttH_hzz", "tHq_htt","tHq_hww","tHq_hzz", "tHW_htt","tHW_hww","tHW_hzz", "TTWH_htt","TTWH_hww","TTWH_hzz", "TTZH_htt","TTZH_hww","TTZH_hzz",
]


features={
#"DNN_maxval":{"xlabel":"DNN_maxval","logy":0}, 
"DNNSubCat2_BIN":{"xlabel":"DNN_Bin","logy":0}, 
#"DNNSubCat2_nBin13":{"xlabel":"DNN_nBin13","logy":0}, 
#"DNNSubCat2_nBin3":{"xlabel":"DNN_nBin3","logy":0}, 
#"DNNSubCat2_nBin5":{"xlabel":"DNN_nBin5","logy":0}, 
#"Bin2l":{"xlabel":"Bin2l","logy":0},
#"DNN_ttHnode_all":{"xlabel":"DNN_ttHnode_all","logy":0}, 
#"DNN_ttWnode_all":{"xlabel":"DNN_ttWnode_all","logy":0}, 
#"DNN_Restnode_all":{"xlabel":"DNN_Restnode_all","logy":0}, 
#"DNN_tHQnode_all":{"xlabel":"DNN_tHQnode_all","logy":0}, 
#"nBJetMedium":{"xlabel":"nBJetMedium","logy":0},
# "nBJetLoose":{"xlabel":"nBJetLoose","logy":0},
# "n_presel_jet":{"xlabel":"n_presel_jet","logy":0},
# "n_presel_jetFwd":{"xlabel":"n_presel_jetFwd","logy":0},
# "SVABin2l":{"xlabel":"SVABin2l","logy":0},
# "mvaOutput_2lss_ttV":{"xlabel":"mvaOutput_2lss_ttV","logy":0},
# "mvaOutput_2lss_ttbar":{"xlabel":"mvaOutput_2lss_ttbar","logy":0},
# "Hj_tagger_hadTop":{"xlabel":"Hj_tagger_hadTop","logy":0},
# "Hj_tagger":{"xlabel":"Hj_tagger","logy":0},
# "hadTop_BDT":{"xlabel":"hadTop_BDT","logy":0},
# "Dilep_pdgId":{"xlabel":"Dilep_pdgId","logy":0},
# "avg_dr_jet":{"xlabel":"avg_dr_jet","logy":0},
# "lep1_charge":{"xlabel":"lep1_charge","logy":0},
# "lep1_conePt":{"xlabel":"lep1_conePt","logy":0},
# "lep2_conePt":{"xlabel":"lep2_conePt","logy":0},
# "lep1_eta":{"xlabel":"lep1_eta","logy":0},
# "lep2_eta":{"xlabel":"lep2_eta","logy":0},
# "lep1_phi":{"xlabel":"lep1_phi","logy":0},
# "lep2_phi":{"xlabel":"lep2_phi","logy":0},
# "jet1_pt":{"xlabel":"jet1_pt","logy":0},
# "jet2_pt":{"xlabel":"jet2_pt","logy":0},
# "jet3_pt":{"xlabel":"jet3_pt","logy":0},
# "jet4_pt":{"xlabel":"jet4_pt","logy":0},
# "jet1_eta":{"xlabel":"jet1_eta","logy":0},
# "jet2_eta":{"xlabel":"jet2_eta","logy":0},
# "jet3_eta":{"xlabel":"jet3_eta","logy":0},
# "jet4_eta":{"xlabel":"jet4_eta","logy":0},
# "jet1_phi":{"xlabel":"jet1_phi","logy":0},
# "jet2_phi":{"xlabel":"jet2_phi","logy":0},
# "jet3_phi":{"xlabel":"jet3_phi","logy":0},
# "jet4_phi":{"xlabel":"jet4_phi","logy":0},
# "jetFwd1_pt":{"xlabel":"jetFwd1_pt","logy":0},
# "jetFwd1_eta":{"xlabel":"jetFwd1_eta","logy":0},
# "mT_lep1":{"xlabel":"mT_lep1","logy":0},
# "mT_lep2":{"xlabel":"mT_lep2","logy":0},
# "maxeta":{"xlabel":"maxeta","logy":0},
# "mbb":{"xlabel":"mbb","logy":0},
# "metLD":{"xlabel":"metLD","logy":0},
# "mindr_lep1_jet":{"xlabel":"mindr_lep1_jet","logy":0},
# "mindr_lep2_jet":{"xlabel":"mindr_lep2_jet","logy":0},

}

# directory of output
outputdir = "%s/plots_%s_%s/"%(outputDir,region, catflag)

# the root file saving the histograms
filename = "{}/ttH_{}_{}_full_uncertanty_runII.root".format(outputdir, region, cutname)

# lumi information
luminosity = {"2016": 35.92 , "2017": 41.53  , "2018": 59.74, "runII": 137.19}

# dummy options, please don't change it
normalization = False # Normalize to unit 
showStats = False


##### end user defined variables
# check outputdir
if not os.path.exists(outputdir):
    print ('mkdir: ', outputdir)
    os.makedirs(outputdir)

# create root file, this will overwrite the root file
def h_syst_add(h1, h2, add=1):
    h_sum = h1.Clone()
    h_sum.Sumw2()
    h_sum.SetStats(0)
    nbins = h2.GetNbinsX()
    for b in range(nbins+1):
        error = h2.GetBinError(b) + h1.GetBinError(b)
        content = h2.GetBinContent(b) + add*h1.GetBinContent(b)
        h_sum.SetBinContent(b, content)
        h_sum.SetBinError(b, error)
    return h_sum

if createROOTfile:
    #exec(open("/home/binghuan/Work/Macros/plotters/make_systHists.py").read())
    exec(open("/home/binghuan/Work/TTHLep/TTHLep_RunII/Legacy_ctrls/plots/mvaTool_LegacyAll_20200611/make_systHists.py").read())

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
    y.SetTitleSize(30)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.3)
    y.SetLabelFont(43)
    y.SetLabelSize(20)

    # Adjust x-axis settings
    x = h2.GetXaxis()
    x.SetTitle(POI)
    x.SetTitleSize(35)
    x.SetTitleFont(43)
    x.SetTitleOffset(3.0)
    x.SetLabelFont(43)
    x.SetLabelSize(20)

    return h2

def getErrors(rfile, hstat, hsyst):
    err_syst =0
    err_stat =0
    if rfile.GetListOfKeys().Contains(hstat): 
        h_stat = rfile.Get(hstat)
        error = Double(0)
        h_stat.IntegralAndError(0,h_stat.GetNbinsX(),error)
        err_stat = error
    else:
        print (  " ##### WARNING ###### %s doesn't have statistic errors %s "%(rfile, hstat))
    if rfile.GetListOfKeys().Contains(hstat): 
        h_syst = rfile.Get(hsyst)
        nbins = h_syst.GetNbinsX()
        for i in range(1, nbins+1):
            # assuming 100% correlation across bins
            err_syst += h_syst.GetBinError(i)
    else:
        print (  " ##### WARNING ###### %s doesn't have systematic errors %s "%(rfile, hsyst))
    err = math.sqrt(err_stat**2 + err_syst**2)
    return err

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
        legend = TLegend(0.2,0.6,0.9,0.88)
        legend.SetHeader("%s  %s %s"%(year,region, cutname))
        legend.SetNColumns(4)
        legend.SetBorderSize(0)
                
        c, pad1, pad2 = createCanvasPads()

        hstack = THStack("hstack","hstack")
        hstack.SetTitle("#scale[1.0]{%s at %.2f fb^{-1}(13TeV)}"%(year,luminosity[year]))
            
        histName = "ttH_hww_"+feature+"_"+year  # assuming TTH 2018 is always there
        if not inputfile.GetListOfKeys().Contains(histName): 
            print ( "%s doesn't have histogram %s, please use another hist "%(inputfile, histName))
            sys.exit()

        h0 = inputfile.Get(histName)
    
        h_totalsig = h0.Clone("h_totalsig")
        h_totalsig.SetDirectory(0)
        h_totalsig.Reset()
        h_totalsig.SetMarkerStyle(20)
        h_totalsig.Sumw2()
        
        h_totalsig_stat = h0.Clone("h_totalsig_stat")
        h_totalsig_stat.SetDirectory(0)
        h_totalsig_stat.Reset()
        h_totalsig_stat.SetMarkerStyle(20)
        h_totalsig_stat.Sumw2()
        
        h_totalsig_syst = h0.Clone("h_totalsig_syst")
        h_totalsig_syst.SetDirectory(0)
        h_totalsig_syst.Reset()
        h_totalsig_syst.SetMarkerStyle(20)
        h_totalsig_syst.Sumw2()
        
        h_totalbkg = h0.Clone("h_totalbkg")
        h_totalbkg.SetDirectory(0)
        h_totalbkg.Reset()
        h_totalbkg.SetMarkerStyle(20)
        h_totalbkg.Sumw2()
        
        h_totalbkg_stat = h0.Clone("h_totalbkg_stat")
        h_totalbkg_stat.SetDirectory(0)
        h_totalbkg_stat.Reset()
        h_totalbkg_stat.SetMarkerStyle(20)
        h_totalbkg_stat.Sumw2()
        
        h_totalbkg_syst = h0.Clone("h_totalbkg_syst")
        h_totalbkg_syst.SetDirectory(0)
        h_totalbkg_syst.Reset()
        h_totalbkg_syst.SetMarkerStyle(20)
        h_totalbkg_syst.Sumw2()
        
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
                    hist_name = p + "_" + feature + "_" + year
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
                    hist_name = p + "_" + feature + "_" + year
                    hist_name_stat =  hist_name+"_stat"
                    hist_name_syst =  hist_name+"_syst"
                    if not inputfile.GetListOfKeys().Contains(hist_name): 
                        print ( "%s doesn't have histogram %s"%(filename, hist_name))
                        continue
                    h1 = inputfile.Get(hist_name).Clone(hist_name)
                    h1.SetDirectory(0)
                    h1_stat = inputfile.Get(hist_name_stat).Clone(hist_name_stat)
                    h1_stat.SetDirectory(0)
                    h1_syst = inputfile.Get(hist_name_syst).Clone(hist_name_syst)
                    h1_syst.SetDirectory(0)
                    if p == "FakeSub" and sample == "Fakes":
                        hist.Add(h1,-1)
                        h_totalsig.Add(h1,-1)
                        h_totalmc.Add(h1,-1)
                        h_totalsig_stat.Add(h1_stat,-1)
                        #h_totalsig_syst.Add(h1_syst,-1)
                        h_totalsig_syst = h_syst_add(h_totalsig_syst, h1_syst,-1)
                    else:
                        hist.Add(h1)
                        h_totalsig.Add(h1)
                        h_totalmc.Add(h1)
                        h_totalsig_stat.Add(h1_stat)
                        #h_totalsig_syst.Add(h1_syst)
                        h_totalsig_syst = h_syst_add(h_totalsig_syst, h1_syst)
                    error = getErrors(inputfile, hist_name_stat, hist_name_syst)
                    if h1.Integral() < 0.05 or h1.GetEntries() < 100:
                        file.write("\\textcolor{red}{%s} &  %.2f +/- %.2f &   %i \\\\ \\hline \n"%(p.replace('_','\\_'),h1.Integral(),error, h1.GetEntries()))
                    else:
                        file.write("%s &  %.2f +/- %.2f &   %i \\\\ \\hline \n"%(p.replace('_','\\_'),h1.Integral(),error, h1.GetEntries()))
                hist.SetFillColor(Color[sample])
                hist.SetLineColor(kBlack)
                hist.SetFillStyle(Style[sample])
                if sample == "TH" and tH !=1 :
                    hist.Scale(tH)
                    hist.SetFillColor(Color[sample])
                    hist.SetLineColor(kBlack)
                    hist.SetFillStyle(Style[sample])
                    hstack.Add(hist)
                    legend.AddEntry(hist,"%s * %i"%(sample, tH),"f")
                else:
                    hstack.Add(hist)
                    legend.AddEntry(hist,sample,"f")
                     
        # create required parts
            # loop over bkg
            else:
                for p in Process[sample]:
                    if p not in sampleName:
                        print ("process %s is not in sampleName "%p)
                        continue
                    hist_name = p + "_" + feature + "_" + year
                    hist_name_stat =  hist_name+"_stat"
                    hist_name_syst =  hist_name+"_syst"
                    if not inputfile.GetListOfKeys().Contains(hist_name): 
                        print ( "%s doesn't have histogram %s"%(filename, hist_name))
                        continue
                    h1 = inputfile.Get(hist_name).Clone(hist_name)
                    h1.SetDirectory(0)
                    h1_stat = inputfile.Get(hist_name_stat).Clone(hist_name_stat)
                    h1_stat.SetDirectory(0)
                    h1_syst = inputfile.Get(hist_name_syst).Clone(hist_name_syst)
                    h1_syst.SetDirectory(0)
                    if p == "FakeSub" and sample == "Fakes":
                        hist.Add(h1,-1)
                        h_totalmc.Add(h1,-1)
                        h_totalbkg.Add(h1,-1)
                        h_totalbkg_stat.Add(h1_stat,-1)
                        #h_totalbkg_syst.Add(h1_syst,-1)
                        h_totalbkg_syst = h_syst_add(h_totalbkg_syst, h1_syst,-1)
                    else:
                        hist.Add(h1)
                        h_totalmc.Add(h1)
                        h_totalbkg.Add(h1)
                        h_totalbkg_stat.Add(h1_stat)
                        h_totalbkg_syst = h_syst_add(h_totalbkg_syst, h1_syst)
                    error = getErrors(inputfile, hist_name_stat, hist_name_syst)
                    if h1.Integral() < 0.05 or h1.GetEntries() < 100:
                        file.write("\\textcolor{red}{%s} &  %.2f +/- %.2f &   %i \\\\ \\hline \n"%(p.replace('_','\\_'),h1.Integral(),error, h1.GetEntries()))
                    else:
                        file.write("%s &  %.2f +/- %.2f &   %i \\\\ \\hline \n"%(p.replace('_','\\_'),h1.Integral(),error, h1.GetEntries()))
                hist.SetFillColor(Color[sample])
                hist.SetLineColor(kBlack)
                hist.SetFillStyle(Style[sample])
                if sample == "TH" and tH !=1 :
                    hist.Scale(tH)
                    hist.SetFillColor(Color[sample])
                    hist.SetLineColor(kBlack)
                    hist.SetFillStyle(Style[sample])
                    hstack.Add(hist)
                    legend.AddEntry(hist,"%s * %i"%(sample, tH),"f")
                else:
                    hstack.Add(hist)
                    legend.AddEntry(hist,sample,"f")
                     
        error_stat = Double(0)
        h_totalsig_stat.IntegralAndError(0,h_totalsig_stat.GetNbinsX(),error_stat)
        nbins_syst = h_totalsig_syst.GetNbinsX()
        error_syst = 0
        for i in range(1, nbins_syst+1):
            # assuming 100% correlation across bins
            error_syst += h_totalsig_syst.GetBinError(i)
        error = math.sqrt(error_stat**2 + error_syst**2)
        file.write("signal &  %.2f +/- %.2f &   %i \\\\ \\hline \n"%(h_totalsig_stat.Integral(),error, h_totalsig_stat.GetEntries()))

        error_stat = Double(0)
        h_totalbkg.IntegralAndError(0,h_totalbkg_stat.GetNbinsX(),error_stat)
        nbins_syst = h_totalbkg_syst.GetNbinsX()
        for i in range(1, nbins_syst+1):
            # assuming 100% correlation across bins
            error_syst += h_totalbkg_syst.GetBinError(i)
        error = math.sqrt(error_stat**2 + error_syst**2)
        file.write("bkg &  %.2f +/- %.2f &   %i \\\\ \\hline \n"%(h_totalbkg_stat.Integral(),error, h_totalbkg_stat.GetEntries()))
        
        # create required parts
        
        #if blind :
        #    h_sqrtB = createSqrt(h_totalbkg)
        #    h_MCerr = createTotalMCErr(h_sqrtB, values["xlabel"])
        #    h_ratio = createRatio(h_totalsig, h_sqrtB, values["xlabel"], normalization)
        #else:
        #    h_MCerr = createTotalMCErr(h_totalmc, feature)
        #    h_ratio = createRatio(h_dataobs, h_totalmc, values["xlabel"], normalization)
        #    legend.AddEntry(h_dataobs,"observed","lep")
        
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
        if values["logy"]==1:
            pad1.SetLogy()
        maximum = h_dataobs.GetMaximum()
        upperbound = 2.*maximum
        lowerbound = -maximum/40.
        if values["logy"]==1:
            upperbound = 1000*maximum
            lowerbound = 0.1
       
        
        hstack.SetMinimum(lowerbound)
        hstack.SetMaximum(upperbound)
        hstack.Draw("HISTY") 
        # Adjust y-axis settings
        y = hstack.GetYaxis()
        y.SetTitle("Events ")
        y.SetTitleSize(30)
        y.SetTitleFont(43)
        y.SetTitleOffset(1.3)
        y.SetLabelFont(43)
        y.SetLabelSize(20)
        
        nbins = h_ratio.GetNbinsX()
        xmin = h_ratio.GetBinLowEdge(1)
        xmax = h_ratio.GetBinLowEdge(nbins+1)
        #hstack.GetXaxis().SetRange(0, nbins+1)
        hstack.GetXaxis().SetRangeUser(xmin, xmax)
        
        h_totalmc.Draw("e2same")
        if not blind:
            h_dataobs.Draw("same")
        legend.Draw("same")
            
    
        pad2.cd()
        #pad2.SetGridy()
        if blind :
            h_ratio.SetMinimum(0.)
            #maximum = h_ratio.GetMaximum()
            #upperbound = 1.5*maximum
            #h_ratio.SetMaximum(upperbound)
            h_ratio.SetMaximum(5.)
            h_ratio.GetXaxis().SetRangeUser(xmin, xmax)
            h_ratio.Draw("")
        else:
            h_MCerr.SetMinimum(0.5)
            h_MCerr.SetMaximum(1.8)
            h_MCerr.GetXaxis().SetRangeUser(xmin, xmax)
            h_MCerr.Draw("e2") 
            h_ratio.Draw("same")

  
        c.SaveAs("%s%s_%s_isBlind%s_stack.png"%(outputdir,feature,plotname,blind))
        file.write("\\end{tabular}\n}\n\\end{table}\n")
        file.close()
    inputfile.Close()

# Draw all canvases 
if __name__ == "__main__":
    gStyle.SetLegendTextSize(0.05)
    plotStack()
