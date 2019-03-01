#!/usr/bin/env python
import ROOT
from ROOT import TString, TFile, TTree, TCanvas, TH1F, TH1, THStack, TColor, gROOT
from array import array

######## the script is used to print yield of nominal and variation of one nuisance ##################

DirOfRootplas = "/afs/cern.ch/work/b/binghuan/private/TTHLep2017/datacards/V0909V3datacards_"

channels = [ "ee_neg","ee_pos", "em_bl_neg","em_bl_pos","em_bt_neg","em_bt_pos", "mm_bl_neg","mm_bl_pos","mm_bt_neg","mm_bt_pos" ]
#channels = [ "em_bl_neg"]

inPercentage = True

Regions = ["ttWctrl","2L"]
#Regions = ["2L"]

#POIs = ["Dilep_mtWmin","Bin2l","Hj_tagger"]
#POIs = ["Dilep_bestMVA"]
#POIs=["Bin2l","mT_lep2","Hj_tagger","mT_lep1","Dilep_mtWmin","massll","Sum2lCharge","nLooseJet","mht","metLD","Dilep_bestMVA","Dilep_worseMVA","Dilep_pdgId","Dilep_htllv","Dilep_nTight","HighestJetCSV","HtJet","Mt_metleadlep","maxeta","leadLep_jetdr","secondLep_jetdr","minMllAFOS","minMllAFAS","minMllSFOS","nLepFO","nLepTight","puWeight","bWeight","TriggerSF","lepSF","leadLep_BDT","secondLep_BDT","TrueInteractions","nBestVTX","mvaOutput_2lss_ttV","mvaOutput_2lss_ttbar","nBJetLoose","nBJetMedium","lep1_conePt","lep2_conePt","PFMET","PFMETphi","jet1_CSV","jet2_CSV","jet3_CSV","jet4_CSV"]
POIs = ["Bin2l"]
Nuisance = "Fakes" # "Jes","Pileup","Trigger","Bweight"

#numberOfBins={"Bin2l":11, "Hj_tagger":10, "Dilep_mtWmin":8}
numberOfBins={"Bin2l": 11,"mT_lep2":10,"Hj_tagger":10,"mT_lep1":10,"Dilep_mtWmin":10,"massll":10,"Sum2lCharge":2,"nLooseJet":7,"mht":10,"metLD":10,"Dilep_bestMVA":8,"Dilep_worseMVA":8,"Dilep_pdgId":3,"Dilep_htllv":10,"Dilep_nTight":3,"HighestJetCSV":15,"HtJet":10,"Mt_metleadlep":10,"maxeta":10,"leadLep_jetdr":10,"secondLep_jetdr":10,"minMllAFOS":10,"minMllAFAS":10,"minMllSFOS":10,"nLepFO":6,"nLepTight":6,"puWeight":30,"bWeight":30,"TriggerSF":30,"lepSF":30,"leadLep_BDT":10,"secondLep_BDT":10,"TrueInteractions":100,"nBestVTX":100,"mvaOutput_2lss_ttV":10,"mvaOutput_2lss_ttbar":10,"nBJetLoose":5,"nBJetMedium":5,"lep1_conePt":50,"lep2_conePt":50,"PFMET":40,"PFMETphi":10,"jet1_CSV":10,"jet2_CSV":10,"jet3_CSV":10,"jet4_CSV":10}

Prefix = "ttH_"
Postfix = ".root"

h_data_name ="data_obs"

logfilename = ""

samplesToUse=[]

samples = [
#"TTH_hww","TTH_hzz","TTH_htt","TTH_hot",
"TTH_hww","TTH_hzz","TTH_htt","TTH_hmm","TTH_hot",
"THQ_hww","THQ_hzz","THQ_htt",
"THW_hww","THW_hzz","THW_htt",
"TTWW","TTW","TTZ","EWK","Rares","Conv","Fakes","Flips"]

samplesMM = [
#"TTH_hww","TTH_hzz","TTH_htt","TTH_hot",
"TTH_hww","TTH_hzz","TTH_htt","TTH_hmm","TTH_hot",
"THQ_hww","THQ_hzz","THQ_htt",
"THW_hww","THW_hzz","THW_htt",
"TTWW","TTW","TTZ","EWK","Rares","Fakes"]

samplesEE = ["TTH_hww","TTH_hzz","TTH_htt","TTH_hot",
"THQ_hww","THQ_hzz","THQ_htt",
"THW_hww","THW_hzz","THW_htt",
"TTWW","TTW","TTZ","EWK","Rares","Conv","Fakes","Flips"]

Rates = {
"Rares":0, "EWK":0, "Conv":0, "TTW":0, "TTWW":0, "TTZ":0, "Fakes":0, "Flips":0, 
"TTH_htt":0,"TTH_hww":0,"TTH_hzz":0,"TTH_hot":0,"TTH_hmm":0,
"THQ_htt":0,"THQ_hww":0,"THQ_hzz":0,
"THW_htt":0,"THW_hww":0,"THW_hzz":0
 }

Uncertainties = {
"Rares":0, "EWK":0, "Conv":0, "TTW":0, "TTWW":0, "TTZ":0, "Fakes":0, "Flips":0, 
"TTH_htt":0,"TTH_hww":0,"TTH_hzz":0,"TTH_hot":0,"TTH_hmm":0,
"THQ_htt":0,"THQ_hww":0,"THQ_hzz":0,
"THW_htt":0,"THW_hww":0,"THW_hzz":0
 }

### the shapes ##########
Nuisances ={
"Fakes":["CMS_ttHl16_FRm_norm","CMS_ttHl16_FRm_pt","CMS_ttHl16_FRm_be","CMS_ttHl16_FRe_norm","CMS_ttHl16_FRe_pt","CMS_ttHl16_FRe_be","CMS_ttHl17_Clos_e_shape","CMS_ttHl17_Clos_m_shape"],
"Jes":["CMS_scale_j"],
"Pileup":["PU"],
"Trigger":["CMS_ttHl17_trigger"],
"Bweight":["CMS_ttHl17_btag_HFStats1","CMS_ttHl17_btag_HFStats2","CMS_ttHl16_btag_cErr1","CMS_ttHl16_btag_cErr2","CMS_ttHl16_btag_LF","CMS_ttHl16_btag_HF","genWeight_muF","genWeight_muR","CMS_scale_j","CMS_ttHl17_btag_LFStats1","CMS_ttHl17_btag_LFStats2"],
}

ShapeSysts={
"PU": ["Rares","EWK","Conv","TTW","TTZ","TTWW","TTH_htt","TTH_hww","TTH_hzz","TTH_hmm","TTH_hot", "THQ_htt","THQ_hww","THQ_hzz","THW_htt","THW_hww","THW_hzz"],
"CMS_scale_j": ["Rares","EWK","Conv","TTW","TTZ","TTWW","TTH_htt","TTH_hww","TTH_hzz","TTH_hmm","TTH_hot", "THQ_htt","THQ_hww","THQ_hzz","THW_htt","THW_hww","THW_hzz"],
"CMS_ttHl17_trigger":["Rares","EWK","Conv","TTW","TTZ","TTWW","TTH_htt","TTH_hww","TTH_hzz","TTH_hmm","TTH_hot", "THQ_htt","THQ_hww","THQ_hzz","THW_htt","THW_hww","THW_hzz"],
"CMS_ttHl17_btag_HFStats1":["Rares","EWK","Conv","TTW","TTZ","TTWW","TTH_htt","TTH_hww","TTH_hzz","TTH_hmm","TTH_hot", "THQ_htt","THQ_hww","THQ_hzz","THW_htt","THW_hww","THW_hzz"],
"CMS_ttHl17_btag_HFStats2":["Rares","EWK","Conv","TTW","TTZ","TTWW","TTH_htt","TTH_hww","TTH_hzz","TTH_hmm","TTH_hot", "THQ_htt","THQ_hww","THQ_hzz","THW_htt","THW_hww","THW_hzz"],
"CMS_ttHl16_btag_cErr1":["Rares","EWK","Conv","TTW","TTZ","TTWW","TTH_htt","TTH_hww","TTH_hzz","TTH_hmm","TTH_hot", "THQ_htt","THQ_hww","THQ_hzz","THW_htt","THW_hww","THW_hzz"],
"CMS_ttHl16_btag_cErr2":["Rares","EWK","Conv","TTW","TTZ","TTWW","TTH_htt","TTH_hww","TTH_hzz","TTH_hmm","TTH_hot", "THQ_htt","THQ_hww","THQ_hzz","THW_htt","THW_hww","THW_hzz"],
"CMS_ttHl16_btag_LF":["Rares","EWK","Conv","TTW","TTZ","TTWW","TTH_htt","TTH_hww","TTH_hzz","TTH_hmm","TTH_hot", "THQ_htt","THQ_hww","THQ_hzz","THW_htt","THW_hww","THW_hzz"],
"CMS_ttHl16_btag_HF":["Rares","EWK","Conv","TTW","TTZ","TTWW","TTH_htt","TTH_hww","TTH_hzz","TTH_hmm","TTH_hot", "THQ_htt","THQ_hww","THQ_hzz","THW_htt","THW_hww","THW_hzz"],
"CMS_ttHl17_btag_LFStats1":["Rares","EWK","Conv","TTW","TTZ","TTWW","TTH_htt","TTH_hww","TTH_hzz","TTH_hmm","TTH_hot", "THQ_htt","THQ_hww","THQ_hzz","THW_htt","THW_hww","THW_hzz"],
"CMS_ttHl17_btag_LFStats2":["Rares","EWK","Conv","TTW","TTZ","TTWW","TTH_htt","TTH_hww","TTH_hzz","TTH_hmm","TTH_hot", "THQ_htt","THQ_hww","THQ_hzz","THW_htt","THW_hww","THW_hzz"],
"genWeight_muF":["TTH_htt","TTH_hzz","TTH_hww","TTH_hmm","TTH_hot","TTW","TTZ"],
"genWeight_muR":["TTH_htt","TTH_hzz","TTH_hww","TTH_hmm","TTH_hot","TTW","TTZ"],

"CMS_ttHl16_FRm_norm":["Fakes"],
"CMS_ttHl16_FRm_pt":["Fakes"],
"CMS_ttHl16_FRm_be":["Fakes"],
"CMS_ttHl17_Clos_m_shape":["Fakes"],
"CMS_ttHl16_FRe_norm":["Fakes"],
"CMS_ttHl16_FRe_pt":["Fakes"],
"CMS_ttHl16_FRe_be":["Fakes"],
"CMS_ttHl17_Clos_e_shape":["Fakes"],

}

def read_rootfile(samplename, dirOfRootpla):
    ''' read a root file '''
    fullfilename = dirOfRootpla+samplename
    inputfile = TFile(fullfilename,"read")
    return inputfile


def writecard(Process , syst, channel, rootfile, systLog):
    ''' write the line of cards for a specific systmatic '''
    
    # loop over processes
    for p in Process:
        # check whether the process is affected by certain systematics
        if p in ShapeSysts[Nuisances[syst][0]]: 
            stringToWrite= p + "    "
            # check the up down yield
            nominal = Rates[p]
            Uncertainty = Uncertainties[p]
            stringToWrite += str(nominal) +"   "
            if inPercentage and nominal !=0:
                stringToWrite += str(100*Uncertainty/nominal)+"%    "
            else:        
                stringToWrite += str(Uncertainty) +"   "
            #loop over np
            for np in Nuisances[syst]:
                histonameUp = p+"_"+np+"Up"
                print histonameUp
                histoUp = rootfile.Get(histonameUp)
                yieldUp = round(histoUp.Integral(),3)
                histonameDown = p+"_"+np+"Down"
                histoDown = rootfile.Get(histonameDown)
                yieldDown = round(histoDown.Integral(),3)
                systError = max(abs(yieldUp-nominal),abs(yieldDown-nominal))
                if inPercentage and nominal !=0:
                    stringToWrite += str(100*systError/nominal) + "%    "
                else:
                    stringToWrite += str(systError) + "    "
            print >> systLog, stringToWrite


def main():
    ''' please make sure the script is running on ROOT>=6 , otherwise you need to add SumW2 when you declare a histograms '''
    for region in Regions:
        for POI in POIs:
            dirOfRootplas = DirOfRootplas + POI + "/"
            
            for channel in channels:
                # select which samples to loop over for each channel
                if "mm" in channel: samplesToLoop = samplesMM
                elif "ee" in channel: samplesToLoop = samplesEE
                else : samplesToLoop = samples
                
                samplesToUse = samplesToLoop[:]

                # create a log file to save the output
                SystLogName = dirOfRootplas+Prefix+region+"_"+channel + "_TableOfSystematics_"+Nuisance+".txt"
                SystLogFile = file(SystLogName,"w")
        
                # open and read root file
                filename = Prefix + region + "_" +channel + Postfix
                inputfile  = read_rootfile(filename, dirOfRootplas)
                gROOT.cd()
                
                print samplesToLoop 
                for sample in samplesToLoop:
                    hist = inputfile.Get(sample)
                    hist_error = ROOT.Double(0)
                    hist_integral = hist.IntegralAndError(0,hist.GetNbinsX(),hist_error)                              
                    Rates[sample] = round(hist_integral,3)
                    Uncertainties[sample] = round(hist_error,3)

                # write begin parts of datacards
                print >> SystLogFile, "In Channel "+channel+":"
                begin = "Samples Nominal Stats"
                for np in Nuisances[Nuisance]:
                    begin += "  "+np
                print >> SystLogFile, begin
               
                
                # write each systematics
                writecard(samplesToUse ,Nuisance, channel, inputfile, SystLogFile)
             
                

main()
