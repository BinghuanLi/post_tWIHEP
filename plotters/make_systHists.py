import sys
import argparse
import os
import math
from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TString, TFile, TH1, THStack, gROOT, TStyle, TAttFill, TLegend, TGraphAsymmErrors, TLine
from ROOT import kBlack, kBlue, kRed, kCyan, kViolet, kGreen, kOrange, kGray, kPink, kTRUE
from ROOT import Double
from ROOT import gROOT, gStyle
from functools import reduce

gROOT.SetBatch(1)
gROOT.Reset()
gStyle.SetCanvasColor(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetOptStat(0)
gStyle.SetTitleX(0.5) # title X location
gStyle.SetTitleY(0.96) # title Y location 
gStyle.SetPaintTextFormat(".2f")

# options
usage = 'usage: %prog [options]'
parser = argparse.ArgumentParser(usage)


Nuisances_lnN={
"pdf_Higgs_ttH":0.036,
"QCDscale_ttH":0.093,
"pdf_tHq":0.010,
"QCDscale_tHq":0.067, 
"pdf_tHW":0.027, 
"QCDscale_tHW":0.061, 
"pdf_TTW":0.04,"QCDscale_TTW":0.129, 
"pdf_TTWW":0.03,"QCDscale_TTWW":0.109, 
"pdf_TTZ":0.035, "QCDscale_TTZ":0.112,
"CMS_ttHl_WZ_theo":0.07,
"pdf_WH":0.019,"QCDscale_WH":0.07,
"pdf_ZH":0.016,"QCDscale_ZH":0.038,
"pdf_qqH":0.021,"QCDscale_qqH":0.04,
"pdf_ggH":0.031,"QCDscale_ggH":0.081,
"BR_htt":0.016,"BR_hww":0.015,"BR_hzz":0.015,"BR_hzg":0.010,"BR_hmm":0.010,
"lumi":0.03,"CMS_ttHl_QF":0.300,"CMS_ttHl_EWK_4j":0.300,"CMS_ttHl_Convs":0.500,"CMS_ttHl_Rares":0.500,"CMS_ttHl_EWK":0.500,
}
lnN_per_sample={
"data_flips":["CMS_ttHl_QF"],
"TTZ":["pdf_TTZ","QCDscale_TTZ","lumi"],
"TTW":["pdf_TTW","QCDscale_TTW","lumi"],
"TTWW":["pdf_TTWW","QCDscale_TTWW","lumi"],
"WZ":["CMS_ttHl_EWK_4j","CMS_ttHl_EWK","lumi"],
"ZZ":["CMS_ttHl_EWK_4j","CMS_ttHl_EWK","lumi"],
"Convs":["CMS_ttHl_Convs","lumi"],
"Rares":["CMS_ttHl_Rares","lumi"],
"ttH_hww":["pdf_Higgs_ttH","QCDscale_ttH","BR_hww","lumi"],
"ttH_hzz":["pdf_Higgs_ttH","QCDscale_ttH","BR_hzz","lumi"],
"ttH_hmm":["pdf_Higgs_ttH","QCDscale_ttH","BR_hmm","lumi"],
"ttH_htt":["pdf_Higgs_ttH","QCDscale_ttH","BR_htt","lumi"],
"ttH_hzg":["pdf_Higgs_ttH","QCDscale_ttH","BR_hzg","lumi"],
"tHW_hww":["pdf_tHW","QCDscale_tHW","BR_hww","lumi"],
"tHW_hzz":["pdf_tHW","QCDscale_tHW","BR_hzz","lumi"],
"tHW_hmm":["pdf_tHW","QCDscale_tHW","BR_hmm","lumi"],
"tHW_htt":["pdf_tHW","QCDscale_tHW","BR_htt","lumi"],
"tHW_hzg":["pdf_tHW","QCDscale_tHW","BR_hzg","lumi"],
"tHq_hww":["pdf_tHq","QCDscale_tHq","BR_hww","lumi"],
"tHq_hzz":["pdf_tHq","QCDscale_tHq","BR_hzz","lumi"],
"tHq_hmm":["pdf_tHq","QCDscale_tHq","BR_hmm","lumi"],
"tHq_htt":["pdf_tHq","QCDscale_tHq","BR_htt","lumi"],
"tHq_hzg":["pdf_tHq","QCDscale_tHq","BR_hzg","lumi"],
"qqH_hww":["pdf_qqH","QCDscale_qqH","BR_hww","lumi"],
"qqH_hzz":["pdf_qqH","QCDscale_qqH","BR_hzz","lumi"],
"qqH_htt":["pdf_qqH","QCDscale_qqH","BR_htt","lumi"],
"ggH_hww":["pdf_ggH","QCDscale_ggH","BR_hww","lumi"],
"ggH_hzz":["pdf_ggH","QCDscale_ggH","BR_hzz","lumi"],
"ggH_htt":["pdf_ggH","QCDscale_ggH","BR_htt","lumi"],
"WH_hww":["pdf_WH","QCDscale_WH","BR_hww","lumi"],
"WH_hzz":["pdf_WH","QCDscale_WH","BR_hzz","lumi"],
"WH_htt":["pdf_WH","QCDscale_WH","BR_htt","lumi"],
"ZH_hww":["pdf_ZH","QCDscale_ZH","BR_hww","lumi"],
"ZH_hzz":["pdf_ZH","QCDscale_ZH","BR_hzz","lumi"],
"ZH_htt":["pdf_ZH","QCDscale_ZH","BR_htt","lumi"],
"TTWH_hww":["BR_hww","lumi"],
"TTWH_hzz":["BR_hzz","lumi"],
"TTWH_htt":["BR_htt","lumi"],
"TTZH_hww":["BR_hww","lumi"],
"TTZH_hzz":["BR_hzz","lumi"],
"TTZH_htt":["BR_htt","lumi"],

}


common_shape = ["CMS_ttHl_lepEff_muloose","CMS_ttHl_lepEff_elloose", "CMS_ttHl_lepEff_mutight","CMS_ttHl_lepEff_eltight", "CMS_ttHl_JER","CMS_ttHl_UnclusteredEn","CMS_scale_j_jesFlavorQCD", "CMS_scale_j_jesRelativeBal","CMS_scale_j_jesHF","CMS_scale_j_jesBBEC1","CMS_scale_j_jesEC2","CMS_scale_j_jesAbsolute"]
thuShape_samples = ["ttH_htt","ttH_hzz","ttH_hww","ttH_hmm","ttH_hzg","tHq_htt","tHq_hww","tHq_hzz","tHW_htt","tHW_hww","tHW_hzz","TTW","TTZ"]
thuShape = ["CMS_ttHl_thu_shape_ttH_x1","CMS_ttHl_thu_shape_ttH_y1"]
fakeShape = ["CMS_ttHl_Clos_e_shape","CMS_ttHl_Clos_m_shape","CMS_ttHl_FRm_norm","CMS_ttHl_FRm_pt","CMS_ttHl_FRm_be","CMS_ttHl_FRe_norm","CMS_ttHl_FRe_pt","CMS_ttHl_FRe_be"]

shape_2016=[
"CMS_ttHl16_L1PreFiring", "CMS_ttHl16_btag_HFStats1","CMS_ttHl16_btag_HFStats2","CMS_ttHl16_btag_LFStats1","CMS_ttHl16_btag_LFStats2","PU_16",
"CMS_scale_j_jesRelativeSample_2016","CMS_scale_j_jesBBEC1_2016","CMS_scale_j_jesEC2_2016","CMS_scale_j_jesAbsolute_2016","CMS_scale_j_jesHF_2016",
]

shape_2017=[
"CMS_ttHl17_L1PreFiring", "CMS_ttHl17_btag_HFStats1","CMS_ttHl17_btag_HFStats2","CMS_ttHl17_btag_LFStats1","CMS_ttHl17_btag_LFStats2","PU_17",
"CMS_scale_j_jesRelativeSample_2017","CMS_scale_j_jesBBEC1_2017","CMS_scale_j_jesEC2_2017","CMS_scale_j_jesAbsolute_2017","CMS_scale_j_jesHF_2017",
]

shape_2018=[
"CMS_ttHl18_btag_HFStats1","CMS_ttHl18_btag_HFStats2","CMS_ttHl18_btag_LFStats1","CMS_ttHl18_btag_LFStats2","PU_18",
"CMS_scale_j_jesRelativeSample_2018","CMS_scale_j_jesBBEC1_2018","CMS_scale_j_jesEC2_2018","CMS_scale_j_jesAbsolute_2018","CMS_scale_j_jesHF_2018",
]



def draw_underflow_overflow(h1):
    h1.GetXaxis().SetRange(0, h1.GetNbinsX() + 1)
    h1.Draw()
    return h1

def fill_underflow_overflow(h1):
    nbin = h1.GetNbinsX()
    h1.Fill(h1.GetBinCenter(1),h1.GetBinContent(0))
    h1.Fill(h1.GetBinCenter(nbin),h1.GetBinContent(nbin+1)) 
    h1.Draw()
    return h1

def fill_lnN_error(hist_nom, lnNs):
    if len(lnNs) ==0:
        return hist_nom
    nbin = hist_nom.GetNbinsX()
    error_rel = 0
    error_rel = reduce((lambda x,y : math.sqrt(x**2 + y**2)), lnNs)
    for i in range(1,nbin+1):
        central_val = hist_nom.GetBinContent(i)
        error_lnN = central_val * error_rel
        error_nom = hist_nom.GetBinError(i)
        error = math.sqrt(error_nom**2 + error_lnN**2)
        hist_nom.SetBinError(i, error)
    return hist_nom

def set_lnN_error(hist_nom, lnNs):
    nbin = hist_nom.GetNbinsX()
    error_rel = 0
    if len(lnNs) ==0:
        for i in range(1,nbin+1):
            hist_nom.SetBinError(i, 0)
        return hist_nom
    error_rel = reduce((lambda x,y : math.sqrt(x**2 + y**2)), lnNs)
    for i in range(1,nbin+1):
        central_val = hist_nom.GetBinContent(i)
        error_lnN = central_val * error_rel
        hist_nom.SetBinError(i, error_lnN)
    return hist_nom



def fill_shape_error(hist_nom, hist_up, hist_down):
    nbin = hist_nom.GetNbinsX()
    for i in range(1,nbin+1):
        central_val = hist_nom.GetBinContent(i)
        error_nom = hist_nom.GetBinError(i)
        error_up = abs(central_val - hist_up.GetBinContent(i))
        error_down = abs(central_val - hist_up.GetBinContent(i))
        error_syst = max(error_up, error_down)
        error = math.sqrt(error_nom**2 + error_syst**2)
        hist_nom.SetBinError(i, error)
    return hist_nom 
   

def find_lnN(keyname):
    names_lnN=[]
    if keyname in lnN_per_sample:
        names_lnN = lnN_per_sample[keyname]
    else:
        print("########## WARNING #########  {} is not found in lnN_per_sample, set it to empty list ".format(keyname))
    err_lnNs = []    
    for name_lnN in names_lnN:
        if name_lnN in Nuisances_lnN:
            err_lnNs.append(Nuisances_lnN[name_lnN])
        else:
            print("########## WARNING #########  {} is not found in Nuisances_lnN, skip this nuisance ".format(name_lnN))

    return err_lnNs

def find_shapes(keyname, era):
    names_shapes = []
    if era == "2016":
        mc_shapes = common_shape + shape_2016
    elif era == "2017":
        mc_shapes = common_shape + shape_2017
    elif era == "2018":
        mc_shapes = common_shape + shape_2018
    else:
        print("ERROR year must be 2016 2017 or 2018")
        sys.exit()
    if "fakes" in keyname or "Fakes" in keyname:
        names_shapes = fakeShape
    elif "data" in keyname:
        return names_shapes
    elif keyname in thuShape_samples:
        names_shapes = mc_shapes + thuShape
    else:
        names_shapes = mc_shapes
    return names_shapes 

def getvarhists(rfile, keyname, systname):
    h_up = rfile.Get("{}_{}Up".format(keyname,systname)) 
    h_up.SetDirectory(0)
    h_down = rfile.Get("{}_{}Down".format(keyname,systname))
    h_down.SetDirectory(0)
    return h_up, h_down

# outtput
outfilename = "{}/ttH_{}_{}_full_uncertanty_runII.root".format(outputdir,region , cutname)
f_out = TFile(outfilename,"recreate")
print(" recreate file {}".format(outfilename))

for feature, values in features.items():
    for sample in sampleName:
        outhist_sum = sample+"_"+feature+"_runII"
        outhist_sum_stat = sample+"_"+feature+"_runII_stat"
        outhist_sum_syst = sample+"_"+feature+"_runII_syst"
        ycount = 0
        for y in ["2016","2017","2018"]:
            file0 = TFile("{}/{}/{}/ttH_{}_{}_{}.root".format(inputDir, catflag, feature, region, cutname, y),"read")
            errorlnNs = find_lnN(sample)
            errShapes = find_shapes(sample, y)
            file0.cd()
            h_nom = file0.Get(sample)
            h_nom.SetDirectory(0)
            h_stat = h_nom.Clone(sample+"_stat")
            h_stat.SetDirectory(0)
            h_syst = h_nom.Clone(sample+"_syst")
            h_syst.SetDirectory(0)
            hist_all = fill_lnN_error(h_nom, errorlnNs)
            h_syst = set_lnN_error(h_syst, errorlnNs)
           # count = 0
            for shapeName in errShapes:
                #print( "sample {} syst {} ".format(sample, shapeName))
                hist_up, hist_down = getvarhists(file0, sample, shapeName) 
                hist_all = fill_shape_error(hist_all, hist_up, hist_down)
                h_syst = fill_shape_error(h_syst, hist_up, hist_down)

            outhist_name = sample+"_"+feature+"_"+y
            h_out = hist_all.Clone(outhist_name)
            h_out.SetTitle(outhist_name)
            h_out.SetName(outhist_name)
            
            outhist_name_stat = sample+"_"+feature+"_"+y + "_stat"
            h_out_stat = h_stat.Clone(outhist_name_stat)
            h_out_stat.SetTitle(outhist_name_stat)
            h_out_stat.SetName(outhist_name_stat)
            
            outhist_name_syst = sample+"_"+feature+"_"+y + "_syst"
            h_out_syst = h_syst.Clone(outhist_name_syst)
            h_out_syst.SetTitle(outhist_name_syst)
            h_out_syst.SetName(outhist_name_syst)
            
            f_out.cd()
            h_out.Write()
            h_out_stat.Write()
            h_out_syst.Write()
            
            # sum 
            if ycount ==0:
                h_outsum = hist_all.Clone(outhist_sum)
                h_outsum.SetTitle(outhist_sum)
                h_outsum.SetName(outhist_sum)
                h_outsum_stat = h_out_stat.Clone(outhist_sum_stat)
                h_outsum_stat.SetTitle(outhist_sum_stat)
                h_outsum_stat.SetName(outhist_sum_stat)
                h_outsum_syst = h_out_syst.Clone(outhist_sum_syst)
                h_outsum_syst.SetTitle(outhist_sum_syst)
                h_outsum_syst.SetName(outhist_sum_syst)
            else:
                h_outsum.Add(hist_all)
                h_outsum_stat.Add(h_out_stat)
                h_outsum_syst = h_syst_add(h_outsum_syst, h_out_syst)
            ycount +=1
        f_out.cd()
        h_outsum.Write()
        h_outsum_stat.Write()
        h_outsum_syst.Write()

f_out.Close()
            
            

