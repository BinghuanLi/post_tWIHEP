R__LOAD_LIBRARY(/cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-slc6-gcc8-opt/lib/libboost_thread.so);
R__LOAD_LIBRARY(/cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-slc6-gcc8-opt/lib/liblwtnn.so);
R__LOAD_LIBRARY(/cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-slc6-gcc8-opt/lib/libboost_system.so);
R__ADD_INCLUDE_PATH(/cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-slc6-gcc8-opt/include/eigen3);

#include "lwtnn/NNLayerConfig.hh"
#include "lwtnn/LightweightNeuralNetwork.hh"
#include "lwtnn/parse_json.hh"
#include "lwtnn/Stack.hh" 
#include <fstream> 
#include <iostream>
#include "TString.h"

// lwtnn evaluations
// the actual NN instance
lwt::LightweightNeuralNetwork *nn_instance;
// frozen post xmas
TString input_json_file = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/LegacyV2/nn_weights/2017samples_xmasupdates_tH_selection/NN_2lss_0tau.json";
// frozen pre xmas
lwt::LightweightNeuralNetwork *nn_instance_newvars;
TString input_json_file_newvars = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/LegacyV2/nn_weights/2017samples_tau2p1_tH_xsecwgtonly/NN_2lss_0tau.json";
void create_lwtnn(TString input_json_file, lwt::LightweightNeuralNetwork*& NN_instance );
void setDNNflag(std::vector<double> DNN_vals, float& DNN_maxval, float& DNNCat, float& DNNSubCat1, float& DNNSubCat2, float Dilep_pdgId, float lep1_charge);

// utils
double getMTlepmet(double phi1, double phi2, double pt1, double pt2);
double deltaPhi(double phi1, double phi2);
double get_rewgtlumi(TString FileName, double rwgt);
double get_rwgtGlobal(TString FileName, int dataEra, bool isTrainMVA=false);
float lnN1D_p1(float kappa, float x, float xmin, float xmax); 
double getAngleOfPlanes(TVector3 plane1_vectA, TVector3 plane1_vectB, TVector3 plane2_vectA, TVector3 plane2_vectB, float &cosa);
double getAngleOfVecs(TLorentzVector vectA, TLorentzVector vectB, float& cosa);
// pu helper
// this is to fix the bug where puWeight is infinite
// this is caused by trueInteraction greater than an intended value
// https://github.com/BinghuanLi/BSMFramework/blob/CMSSW_10_2_16/BSM3G_TNT_Maker/src/PileupReweight.cc#L74-L76
// this happens so rare, only one event in all interested control region and date taking period, so I simply drop it here, it should be fine
// 2017 ZZ_WZctrl.root trueInteractions = 99
bool checkPU(float nPU, int dataEra);
// event selection
bool IsDiLepTR(double massL_SFOS, int n_presel_jet, int nBJetLoose, int nBJetMedium, int n_presel_ele, int n_presel_mu, double lep1_charge, double lep2_charge, double mass_diele, double metLD, double lep1_pdgId, double lep2_pdgId);
bool IsttWctrlTR(double massL_SFOS, int n_presel_jet, int nBJetLoose, int nBJetMedium, int n_presel_ele, int n_presel_mu, double lep1_charge, double lep2_charge, double mass_diele, double metLD, double lep1_pdgId, double lep2_pdgId);
bool IstHlikeDiLepTR(double massL_SFOS, int nLightJet, int nBJetMedium, int n_presel_ele, int n_presel_mu, double lep1_charge, double lep2_charge, double mass_diele, double metLD, double lep1_pdgId, double lep2_pdgId);
// DNNBin
TString input_DNNBin_path = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/LegacyV2/data/rootplas_deeptau2p1_20191205/";
void setDNNBinHistograms(TString MapFileName,TString MapHistName, std::map<TString, TH1F*> &_HistMaps, int nBin);
float getDNNBin(float DNNValue, TString MapFileName, TString MapHistName, std::map<TString,TH1F*> _HistMaps, int nBin);
// fake rate
void setFakeRateHistograms(TString FakeRateFileName,TString FakeRateMuonHistName, TString FakeRateElectronHistName, std::map<std::string, TH2F*> &_MuonFakeRate, std::map<std::string, TH2F*> &_ElectronFakeRate, std::string muSystName="central", std::string eleSystName="central");
Double_t getFakeRateWeight(float lep1_ismvasel, float lep1_pdgId, float lep1_conept, float lep1_eta, float lep2_ismvasel, float lep2_pdgId, float lep2_conept, float lep2_eta , std::map<std::string,TH2F*> _MuonFakeRate, std::map<std::string,TH2F*> _ElectronFakeRate, std::string muSystName="central", std::string eleSystName="central");
//SFs
float triggerSF_ttH(int pdgid1, float pt1, int pdgid2, float pt2, int nlep, int year, int var=0);
// charge Mis
void setChargeMisHistograms(TString ChargeMisFileName,TString ChargeMisHistName, TH2F** _chargeMis);
std::tuple<Double_t,Double_t,Double_t> getChargeMisWeight(float lep1_pdgId, float lep1_charge, float lep1_conept, float lep1_eta, float lep2_pdgId, float lep2_charge, float lep2_conept, float lep2_eta, TH2F* _chargeMis);
// Calculate Lorentz boosted angle
double get_boostedAngle(TLorentzVector Particle1_CMS, TLorentzVector Particle2_CMS, TLorentzVector plane1_vectA, TLorentzVector plane1_vectB, TLorentzVector plane2_vectA, TLorentzVector plane2_vectB, float& cosa);
// read trees
void SetOldTreeBranchStatus(TTree* readtree, bool isHjtagger);
// SVA bins
int ttH_catIndex_2lss_SVA(int LepGood1_pdgId, int LepGood2_pdgId, int LepGood1_charge, int nJet25, int is_tH_enlarged);
int ttH_catIndex_2lss_3j_SVA(int LepGood1_pdgId, int LepGood2_pdgId, int LepGood1_charge, int nJet25, int is_tH_enlarged);
int SVAbin(double mass2l);

//utils
double get_rwgtGlobal(TString FileName, int dataEra, bool isTrainMVA){
    double wgt=1.;
    // in 2018, THQ are split into 1/3 for signal extraction and 2/3 for trainMVA
    if(FileName.Contains("THQ")){
        if(dataEra == 2018 && isTrainMVA){
            wgt= 3./2.;
        }else if(dataEra ==2018 && !isTrainMVA){
            wgt = 3.;
        }
    }
    // TTZ xsec reweighting 
    if(FileName.Contains("TTZ_M10")) wgt *= (0.2814 / 0.2072); // fixes TTZ_M10 xsec
    if(FileName.Contains("TTZ_M1to10")) wgt *= (0.0822 / 0.04537); // fixes TTZ_M1to10 xsec
    // CTCVCP reweighting considering EVENT_originalXWGTUP
    // fix the effective events
    if(FileName.Contains("Legacy18V2_TTH_ctcvcp")) wgt *= 3300.343823/28925000 ;
    if(FileName.Contains("Legacy18V2_THQ_ctcvcp")) wgt *= 519.5817131/2100776.494 ;
    if(FileName.Contains("Legacy18V2_THW_ctcvcp")) wgt *= 235.4400443/1556985.016 ;
    if(FileName.Contains("Legacy16V2_TTH_ctcvcp")) wgt *= 6530.053024/9566400 ; 
    if(FileName.Contains("Legacy16V2_THQ_TuneCP5_ctcvcp")) wgt *= 851.5929841/701252.7066; 
    if(FileName.Contains("Legacy16V2_THW_TuneCP5_ctcvcp")) wgt *= 162.224309/551719.9575 ; 
    if(FileName.Contains("Legacy17V2_TTH_ctcvcp")) wgt *= 1640.57915/9618000 ; 
    if(FileName.Contains("Legacy17V2_THQ_ctcvcp")) wgt *= 174.0414875/715953.8736; 
    if(FileName.Contains("Legacy17V2_THW_ctcvcp")) wgt *= 192.9545578/524938.1638 ; 
    return wgt;
}
double get_rewgtlumi(TString FileName, double rwgt){
    // it may looks stupid now, but it gives the convenience to add rwgt for other samples too
    double wgt=1.;
    if(FileName.Contains("ctcvcp")) wgt=rwgt; //only applyied for samples before 20190929
    return wgt;
}
double deltaPhi(double phi1, double phi2){
    double result = phi1 - phi2;
    while (result > M_PI) result -= 2*M_PI;
    while (result <= -M_PI) result += 2*M_PI;
    return result;
}

double getMTlepmet(double phi1, double phi2, double pt1, double pt2){
    double Mass =0;
    Mass = sqrt(2*pt1*pt2*(1-cos(deltaPhi(phi1,phi2))));
    return Mass;
}

float lnN1D_p1(float kappa, float x, float xmin, float xmax) {
        return std::pow(kappa,(x-xmin)/(xmax-xmin));
}

double getAngleOfVecs(TLorentzVector vectA, TLorentzVector vectB, float& cosa){
    double angle = -9;
    TVector3 v3A = vectA.Vect();
    TVector3 v3B = vectB.Vect();
    if(v3A.Mag()==0){
        angle = -5;
        cosa = -5;
        return angle; 
    }
    if(v3B.Mag()==0){
        angle = -5;
        cosa = -5;
        return angle; 
    }
    angle = v3A.Angle(v3B);
    cosa = v3A.Dot(v3B)/(v3A.Mag()*v3B.Mag());
    return angle;
};
  
double getAngleOfPlanes(TVector3 plane1_vectA, TVector3 plane1_vectB, TVector3 plane2_vectA, TVector3 plane2_vectB, float & cosa){
    double angle = -9;
    TVector3 plane1_norm = plane1_vectA.Cross(plane1_vectB);// get the vector perp to plane 1
    TVector3 plane2_norm = plane2_vectA.Cross(plane2_vectB);// get the vector perp to plane 2
    if(plane1_norm.Mag()==0){
        //std::cout<< "two vectors provided to plane1 cannot determine a plane" << std::endl;
        angle = -5;
        cosa = -5;
        return angle;
    }
    if(plane2_norm.Mag()==0){
        //std::cout<< "two vectors provided to plane2 cannot determine a plane" << std::endl;
        angle = -5;
        cosa = -5;
        return angle;
    }
    angle = plane1_norm.Angle(plane2_norm);
    cosa = plane1_norm.Dot(plane2_norm)/(plane1_norm.Mag()*plane2_norm.Mag());
    return angle;
}
// pu helper
bool checkPU(float nPU, int dataEra){
    bool nPU_isFinite = true;
    if(dataEra==2018){
         if(nPU >= 100) nPU_isFinite=false;
    }else if(dataEra==2017){
         if(nPU >= 99) nPU_isFinite=false;
    }else if(dataEra==2016){
         if(nPU >= 75) nPU_isFinite=false;
    }else{
        std::cout<< " WARNING dataEra is " << dataEra << " please check " << std::endl;
    }
    return nPU_isFinite;
};

// event selection
bool IsDiLepTR(double massL_SFOS, int n_presel_jet, int nBJetLoose, int nBJetMedium, int n_presel_ele, int n_presel_mu, double lep1_charge, double lep2_charge, double mass_diele, double metLD, double lep1_pdgId, double lep2_pdgId){
    if(!(massL_SFOS > 101.2 || massL_SFOS < 81.2)) return false; // cut Z veto
    if(!(n_presel_jet>=4)) return false; //nJet cut
    if(!(nBJetLoose>=2 || nBJetMedium >=1)) return false; //BJet cut
    if((n_presel_ele + n_presel_mu) <2) return false;
    if(!( lep1_charge * lep2_charge >0))return false; // same sign leptons
    if(!(mass_diele > 101.2 || mass_diele < 81.2)) return false; // cut Z veto
    if(metLD <= 30 && fabs(lep1_pdgId)==11 && fabs(lep2_pdgId)==11 ) return false; // metLD if isEE, then metLD > 30GeV
    return true;
};
bool IsttWctrlTR(double massL_SFOS, int n_presel_jet, int nBJetLoose, int nBJetMedium, int n_presel_ele, int n_presel_mu, double lep1_charge, double lep2_charge, double mass_diele, double metLD, double lep1_pdgId, double lep2_pdgId){
    if(!(massL_SFOS > 101.2 || massL_SFOS < 81.2)) return false; // cut Z veto
    if(!(n_presel_jet==3)) return false; //nJet cut
    if(!(nBJetLoose>=2 || nBJetMedium >=1)) return false; //BJet cut
    if((n_presel_ele + n_presel_mu) <2) return false;
    if(!( lep1_charge * lep2_charge >0))return false; // same sign leptons
    if(!(mass_diele > 101.2 || mass_diele < 81.2)) return false; // cut Z veto
    if(metLD <= 30 && fabs(lep1_pdgId)==11 && fabs(lep2_pdgId)==11 ) return false; // metLD if isEE, then metLD > 30GeV
    return true;
};
bool IstHlikeDiLepTR(double massL_SFOS, int nLightJet, int nBJetMedium, int n_presel_ele, int n_presel_mu, double lep1_charge, double lep2_charge, double mass_diele, double metLD, double lep1_pdgId, double lep2_pdgId){
    if(!(nLightJet >=1)) return false; //nLightJet cut
    if(!(nBJetMedium>=1)) return false; //BJet cut
    if(!(massL_SFOS > 101.2 || massL_SFOS < 81.2)) return false; // cut Z veto
    if((n_presel_ele + n_presel_mu) <2) return false;
    if(!( lep1_charge * lep2_charge >0))return false; // same sign leptons
    if(!(mass_diele > 101.2 || mass_diele < 81.2)) return false; // cut Z veto
    if(metLD <= 30 && fabs(lep1_pdgId)==11 && fabs(lep2_pdgId)==11 ) return false; // metLD if isEE, then metLD > 30GeV
    return true;
};

// DNN Bin Maps
void setDNNBinHistograms(TString inputpath, TString MapFileName,TString MapHistName, std::map<TString, TH1F*> &_HistMaps, int nBin){
  TFile* MapFile = TFile::Open((inputpath+MapFileName+".root"),"READ");
  if (!MapFile) std::cout << "MapFile file not found!" << std::endl;
  TString str_nBin = std::to_string(nBin);
  //std::cout<< " try to get " << MapHistName <<"_nBin"<<str_nBin<< " from " << inputpath<<MapFileName<<".root"<< std::endl;
  _HistMaps[(MapFileName+"_"+MapHistName+"_nBin"+str_nBin)] = (TH1F*) MapFile->Get(MapHistName+"_Map_nBin"+str_nBin)->Clone();
  _HistMaps[(MapFileName+"_"+MapHistName+"_nBin"+str_nBin)]->SetDirectory(0);
  MapFile->Close();
  delete MapFile;
}

float getDNNBin(float DNNValue, TString MapFileName, TString MapHistName, std::map<TString,TH1F*> _HistMaps, int nBin){
    float DNNBin = 1.0;
    TString maphistName = MapFileName+"_"+MapHistName+"_nBin"+std::to_string(nBin);
    int xAxisBin  = std::max(1, std::min(_HistMaps[maphistName]->GetNbinsX(), _HistMaps[maphistName]->GetXaxis()->FindBin(DNNValue)));
    DNNBin = _HistMaps[maphistName]->GetBinContent(xAxisBin);
    /*
    if(MapHistName.Contains("em_ttWnode")){
        std::cout <<" DNNValue " << DNNValue <<  " em_ttHnode_nBin " << nBin << " DNNBin " << DNNBin << std::endl; 
    }
    */
    return DNNBin;
}

// Fake Rate
void setFakeRateHistograms(TString FakeRateFileName,TString FakeRateMuonHistName, TString FakeRateElectronHistName, std::map<std::string, TH2F*> &_MuonFakeRate, std::map<std::string, TH2F*> &_ElectronFakeRate, std::string muSystName, std::string eleSystName){
  TFile* FakeRateFile = TFile::Open(FakeRateFileName,"READ");
  if (!FakeRateFile) std::cout << "FakeRate file not found!" << std::endl;
  if(muSystName=="central"){
      _MuonFakeRate[muSystName] = (TH2F*)FakeRateFile->Get(FakeRateMuonHistName)->Clone();
  }else if(muSystName=="QCD"){
      // histograms QCD and TT are used for fake rate closure systematics, I'm not going to put it in config files, because it's ttH exclusive file and I may need to change all(dozens of) config files if I do put it in config files
      _MuonFakeRate[muSystName] = (TH2F*)FakeRateFile->Get("FR_mva090_mu_QCD")->Clone();
  
  }else if(muSystName=="TT"){
      _MuonFakeRate[muSystName] = (TH2F*)FakeRateFile->Get("FR_mva090_mu_TT")->Clone();
  }else{
      _MuonFakeRate[muSystName] = (TH2F*)FakeRateFile->Get(FakeRateMuonHistName+"_"+muSystName)->Clone();
  }
  _MuonFakeRate[muSystName]->SetDirectory(0);
  if(eleSystName=="central"){
    _ElectronFakeRate[eleSystName] = (TH2F*)FakeRateFile->Get(FakeRateElectronHistName)->Clone();
  }else if(eleSystName=="QCD"){
    _ElectronFakeRate[eleSystName] = (TH2F*)FakeRateFile->Get("FR_mva090_el_QCD_NC")->Clone();
  }else if(eleSystName=="TT"){
    _ElectronFakeRate[eleSystName] = (TH2F*)FakeRateFile->Get("FR_mva090_el_TT")->Clone();
  }else{
     _ElectronFakeRate[eleSystName] = (TH2F*)FakeRateFile->Get(FakeRateElectronHistName+"_"+eleSystName)->Clone();
  } 
   _ElectronFakeRate[eleSystName]->SetDirectory(0);
  FakeRateFile->Close();
  delete FakeRateFile;
}

Double_t getFakeRateWeight(float lep1_ismvasel, float lep1_pdgId, float lep1_conept, float lep1_eta, float lep2_ismvasel, float lep2_pdgId, float lep2_conept, float lep2_eta , std::map<std::string,TH2F*> _MuonFakeRate, std::map<std::string,TH2F*> _ElectronFakeRate, std::string muSystName, std::string eleSystName){

  Double_t FakeRateWeight = 1.0;
  if(lep2_conept>0){//if it is ttH 2l category
      if(lep1_ismvasel==1 && lep2_ismvasel==1) return FakeRateWeight;
      int xAxisBin1 = 0, yAxisBin1 = 0, xAxisBin2 = 0, yAxisBin2 = 0;
      Double_t FakeRateWeight1 = 0., FakeRateWeight2 = 0.;
      //Get the bin and fake rate for each lepton
      if(lep1_ismvasel==1){
        // choose fr so that fr/(1-fr)==1
        FakeRateWeight1 = 0.5;
      }else if(fabs(lep1_pdgId)==13){
        xAxisBin1  = std::max(1, std::min(_MuonFakeRate[muSystName]->GetNbinsX(), _MuonFakeRate[muSystName]->GetXaxis()->FindBin(lep1_conept)));
        yAxisBin1  = std::max(1, std::min(_MuonFakeRate[muSystName]->GetNbinsY(), _MuonFakeRate[muSystName]->GetYaxis()->FindBin(std::fabs(lep1_eta))));
        FakeRateWeight1 = _MuonFakeRate[muSystName]->GetBinContent(xAxisBin1,yAxisBin1);
      }else{
        xAxisBin1  = std::max(1, std::min(_ElectronFakeRate[eleSystName]->GetNbinsX(), _ElectronFakeRate[eleSystName]->GetXaxis()->FindBin(lep1_conept)));
        yAxisBin1  = std::max(1, std::min(_ElectronFakeRate[eleSystName]->GetNbinsY(), _ElectronFakeRate[eleSystName]->GetYaxis()->FindBin(std::fabs(lep1_eta))));
        FakeRateWeight1 = _ElectronFakeRate[eleSystName]->GetBinContent(xAxisBin1,yAxisBin1);
      }
      if(lep2_ismvasel==1){
        // choose fr so that fr/(1-fr)==1
        FakeRateWeight2 = 0.5;
      }else if(fabs(lep2_pdgId)==13){
        xAxisBin2  = std::max(1, std::min(_MuonFakeRate[muSystName]->GetNbinsX(), _MuonFakeRate[muSystName]->GetXaxis()->FindBin(lep2_conept)));
        yAxisBin2  = std::max(1, std::min(_MuonFakeRate[muSystName]->GetNbinsY(), _MuonFakeRate[muSystName]->GetYaxis()->FindBin(std::fabs(lep2_eta))));
        FakeRateWeight2 = _MuonFakeRate[muSystName]->GetBinContent(xAxisBin2,yAxisBin2);
      }else{
        xAxisBin2  = std::max(1, std::min(_ElectronFakeRate[eleSystName]->GetNbinsX(), _ElectronFakeRate[eleSystName]->GetXaxis()->FindBin(lep2_conept)));
        yAxisBin2  = std::max(1, std::min(_ElectronFakeRate[eleSystName]->GetNbinsY(), _ElectronFakeRate[eleSystName]->GetYaxis()->FindBin(std::fabs(lep2_eta))));
        FakeRateWeight2 = _ElectronFakeRate[eleSystName]->GetBinContent(xAxisBin2,yAxisBin2);
      }
      //And now get the Event Weights/uncs
      FakeRateWeight = (FakeRateWeight1/(1-FakeRateWeight1))*(FakeRateWeight2/(1-FakeRateWeight2));
      if(lep1_ismvasel==0 && lep2_ismvasel==0){
          FakeRateWeight *= -1;
      }
      //std::cout << EventContainerObj->eventNumber <<" "<< lep1_conept<< " " << lep1_eta<< " " << lep1_pdgId << " "<< FakeRateWeight1<<" "<< lep2_conept<< " " << lep2_eta<< " " << lep2_pdgId <<" " << FakeRateWeight2 <<FakeRateWeight <<"  " << FakeRateWeightUp << "  " <<FakeRateWeightDown << std::endl;
  }
  return FakeRateWeight;
}
// Trigger SFs
float triggerSF_ttH(int pdgid1, float pt1, int pdgid2, float pt2, int nlep, int year, int var=0){
  if (nlep == 2){
    if (abs(pdgid1*pdgid2) == 121){
      if (year == 2016){
	if (pt2 < 25){
	  return 0.98*(1 + var*0.02);
	}
      else return 1.*(1 + var*0.02);
      }
      else if (year == 2017){
	if (pt2<40) return 0.98*(1 + var*0.01);
	else return 1*(1 + var*0.01);
      }
      else if (year == 2018){
	if (pt2<25){
	return 0.98*(1 + var*0.01);
	}
	else return 1.*(1 + var*0.01);
      }
      else{
       return 1.; 
      }
    }
    
    else if ( abs(pdgid1*pdgid2) == 143){
      if (year == 2016) return 1.*(1 + var*0.01);
      else if (year == 2017){
	if (pt2<40) return 0.98*(1 + var*0.01);
	else return 0.99*(1 + var*0.01);
      }
      else if (year == 2018){
	if (pt2<25) return 0.98*(1 + var*0.01);
	else        return 1*(1 + var*0.01);
      }else{
       return 1.; 
      }
    }
    else{
      if (year == 2016) return 0.99*(1 + var*0.01);
      else if (year == 2017){
	if (pt2 < 40) return 0.97*(1 + var*0.02);
	else if (pt2 < 55 && pt2>40) return 0.995*(1 + var*0.02);
	else if (pt2 < 70 && pt2>55) return 0.96*(1 + var*0.02);
	else                         return 0.94*(1 + var*0.02);
      }
      else if (year == 2018){
	if (pt1 < 40) return 1.01*(1 + var*0.01);
	if (pt1 < 70) return 0.995*(1 + var*0.01);
	else return 0.98*(1 + var*0.01);
      }else{
       return 1.; 
      }
    }
    
  }
  else return 1.;
}



//chargeMis
void setChargeMisHistograms(TString ChargeMisFileName,TString ChargeMisHistName, TH2F** _chargeMis){
  std::cout << " set charegMis TH2 to " << ChargeMisFileName <<"/"<< ChargeMisHistName << std::endl;
  TFile* ChargeMisFile = TFile::Open(ChargeMisFileName,"READ");
  if (!ChargeMisFile) std::cout << "ChargeMis file not found!" << std::endl;
  *_chargeMis = (TH2F*)ChargeMisFile->Get(ChargeMisHistName)->Clone();
  (*_chargeMis)->SetDirectory(0);
  ChargeMisFile->Close();
  
  delete ChargeMisFile;
}

std::tuple<Double_t,Double_t,Double_t> getChargeMisWeight(float lep1_pdgId, float lep1_charge, float lep1_conept, float lep1_eta, float lep2_pdgId, float lep2_charge, float lep2_conept, float lep2_eta, TH2F* _chargeMis){

  Double_t ChargeMisWeight = 1., ChargeMisWeightUp = 1., ChargeMisWeightDown = 1.;
  if(lep2_conept<=0) return std::make_tuple(ChargeMisWeight,ChargeMisWeightUp,ChargeMisWeightDown);
  if(lep1_charge==lep2_charge) return std::make_tuple(ChargeMisWeight,ChargeMisWeightUp,ChargeMisWeightDown);
  Double_t ChargeMisWeight1 = 0.;
  Double_t ChargeMisUnc1 = 0.; 
  Double_t ChargeMisWeight2 = 0.;
  Double_t ChargeMisUnc2 = 0.; 
  if(fabs(lep1_pdgId)==11){
    //Get the bin 
    int xAxisBin1  = std::max(1, std::min(_chargeMis->GetNbinsX(), _chargeMis->GetXaxis()->FindBin(lep1_conept)));
    int yAxisBin1  = std::max(1, std::min(_chargeMis->GetNbinsY(), _chargeMis->GetYaxis()->FindBin(std::fabs(lep1_eta))));
    ChargeMisWeight1 = _chargeMis->GetBinContent(xAxisBin1,yAxisBin1);
    ChargeMisUnc1 = _chargeMis->GetBinError(xAxisBin1,yAxisBin1); 
  }
  if(fabs(lep2_pdgId)==11){
    int xAxisBin2  = std::max(1, std::min(_chargeMis->GetNbinsX(), _chargeMis->GetXaxis()->FindBin(lep2_conept)));
    int yAxisBin2  = std::max(1, std::min(_chargeMis->GetNbinsY(), _chargeMis->GetYaxis()->FindBin(std::fabs(lep2_eta))));
    ChargeMisWeight2 = _chargeMis->GetBinContent(xAxisBin2,yAxisBin2);
    ChargeMisUnc2 = _chargeMis->GetBinError(xAxisBin2,yAxisBin2); 
  }
  ChargeMisWeight = ChargeMisWeight1 + ChargeMisWeight2;
  ChargeMisWeightUp = ChargeMisWeight1 + ChargeMisUnc1 + ChargeMisWeight2 + ChargeMisUnc2;
  ChargeMisWeightDown = ChargeMisWeight1 - ChargeMisUnc1 + ChargeMisWeight2 - ChargeMisUnc2;
  //std::cout << lep1_conept<< " " << lep1_eta()<< " " << lep1_pdgId << " "<< ChargeMisWeight1<<" "<< lep2_conept<< " " << lep2_eta<< " " << lep2_pdgId <<" " << ChargeMisWeight2 <<ChargeMisWeight <<"  " << ChargeMisWeightUp << "  " <<ChargeMisWeightDown << std::endl;
  return std::make_tuple(ChargeMisWeight,ChargeMisWeightUp,ChargeMisWeightDown);
}

// Lorentz Boost
double get_boostedAngle(TLorentzVector Particle1_CMS, TLorentzVector Particle2_CMS, TLorentzVector plane1_vectA, TLorentzVector plane1_vectB, TLorentzVector plane2_vectA, TLorentzVector plane2_vectB, float& cosa){
    // Input : All six vectors are in lab frame
    //  Particle1_CMS and Particle2_CMS => rod frame
    //  plane1(2)_vectA and plane1(2)_vectB => vectors to determine plane 1 and plane 2
    // Output : the angle of plane1 and plane2 in the center of mass system of Particle1_CMS and Particle2_CMS
    // https://root-forum.cern.ch/t/how-to-use-boost-in-tlorentzvector/4102
    double angle = -9;
    TLorentzVector MyParticleCombi;
    MyParticleCombi.SetPxPyPzE(Particle1_CMS.Px()+Particle2_CMS.Px(),Particle1_CMS.Py()+Particle2_CMS.Py(), Particle1_CMS.Pz()+Particle2_CMS.Pz(), Particle1_CMS.E()+Particle2_CMS.E());
    TVector3  MyParticleCombi_BoostVector = MyParticleCombi.BoostVector();
    // minus because we boost from lab to rod
    plane1_vectA.Boost(-MyParticleCombi_BoostVector); 
    plane1_vectB.Boost(-MyParticleCombi_BoostVector); 
    plane2_vectA.Boost(-MyParticleCombi_BoostVector); 
    plane2_vectB.Boost(-MyParticleCombi_BoostVector); 

    angle = getAngleOfPlanes( plane1_vectA.Vect(),  plane1_vectB.Vect(),  plane2_vectA.Vect(),  plane2_vectB.Vect(), cosa);

    return angle;
    
}
//read trees
void SetOldTreeBranchStatus(TTree* readtree, bool isHjtagger){
    readtree->SetBranchStatus("*",0);
    readtree->SetBranchStatus("Bin2l",1);
    readtree->SetBranchStatus("ChargeMis",1);
    readtree->SetBranchStatus("ChargeMis_SysDown",1);
    readtree->SetBranchStatus("ChargeMis_SysUp",1);
    readtree->SetBranchStatus("DataEra",1);
    readtree->SetBranchStatus("Dilep_bestMVA",1);
    readtree->SetBranchStatus("Dilep_htllv",1);
    readtree->SetBranchStatus("Dilep_mtWmin",1);
    readtree->SetBranchStatus("Dilep_nTight",1);
    readtree->SetBranchStatus("Dilep_pdgId",1);
    readtree->SetBranchStatus("Dilep_worseIso",1);
    readtree->SetBranchStatus("Dilep_worseMVA",1);
    readtree->SetBranchStatus("Dilep_worseSip",1);
    readtree->SetBranchStatus("Dilep_worsedz",1);
    readtree->SetBranchStatus("EVENT_genWeights",1);
    readtree->SetBranchStatus("EVENT_psWeights",1);
    readtree->SetBranchStatus("EVENT_genWeight",1);
    readtree->SetBranchStatus("EventWeight",1);
    readtree->SetBranchStatus("EVENT_originalXWGTUP",1);
    readtree->SetBranchStatus("EVENT_event",1);
    readtree->SetBranchStatus("EVENT_rWeights",1);
    readtree->SetBranchStatus("FR_weight",1);
    readtree->SetBranchStatus("FakeRate",1);
    readtree->SetBranchStatus("FakeRate_e_QCD",1);
    readtree->SetBranchStatus("FakeRate_e_TT",1);
    readtree->SetBranchStatus("FakeRate_e_be1",1);
    readtree->SetBranchStatus("FakeRate_e_be2",1);
    readtree->SetBranchStatus("FakeRate_e_central",1);
    readtree->SetBranchStatus("FakeRate_e_down",1);
    readtree->SetBranchStatus("FakeRate_e_pt1",1);
    readtree->SetBranchStatus("FakeRate_e_pt2",1);
    readtree->SetBranchStatus("FakeRate_e_up",1);
    readtree->SetBranchStatus("FakeRate_m_QCD",1);
    readtree->SetBranchStatus("FakeRate_m_TT",1);
    readtree->SetBranchStatus("FakeRate_m_be1",1);
    readtree->SetBranchStatus("FakeRate_m_be2",1);
    readtree->SetBranchStatus("FakeRate_m_central",1);
    readtree->SetBranchStatus("FakeRate_m_down",1);
    readtree->SetBranchStatus("FakeRate_m_pt1",1);
    readtree->SetBranchStatus("FakeRate_m_pt2",1);
    readtree->SetBranchStatus("FakeRate_m_up",1);
    readtree->SetBranchStatus("isWHfromVH",1);
    readtree->SetBranchStatus("HTT",1);
    readtree->SetBranchStatus("HiggsDecay",1);
    readtree->SetBranchStatus("HighestJetCSV",1);
    readtree->SetBranchStatus("Hj_tagger",1);
    readtree->SetBranchStatus("Hj_tagger_hadTop",1);
    readtree->SetBranchStatus("Hj_tagger_resTop",1);
    readtree->SetBranchStatus("resTop_BDT",1);
    readtree->SetBranchStatus("HtJet",1);
    if(isHjtagger){
        readtree->SetBranchStatus("Jet25_bDiscriminator",1);
        readtree->SetBranchStatus("Jet25_energy",1);
        readtree->SetBranchStatus("Jet25_eta",1);
        readtree->SetBranchStatus("Jet25_isFromH",1);
        readtree->SetBranchStatus("Jet25_isFromLepTop",1);
        readtree->SetBranchStatus("Jet25_isFromTop",1);
        readtree->SetBranchStatus("Jet25_isLooseBdisc",1);
        readtree->SetBranchStatus("Jet25_isMediumBdisc",1);
        readtree->SetBranchStatus("Jet25_isTightBdisc",1);
        readtree->SetBranchStatus("Jet25_isToptag",1);
        readtree->SetBranchStatus("Jet25_lepdetamax",1);
        readtree->SetBranchStatus("Jet25_lepdetamin",1);
        readtree->SetBranchStatus("Jet25_lepdphimax",1);
        readtree->SetBranchStatus("Jet25_lepdphimin",1);
        readtree->SetBranchStatus("Jet25_lepdrmax",1);
        readtree->SetBranchStatus("Jet25_lepdrmin",1);
        readtree->SetBranchStatus("Jet25_mass",1);
        readtree->SetBranchStatus("Jet25_matchId",1);
        readtree->SetBranchStatus("Jet25_phi",1);
        readtree->SetBranchStatus("Jet25_pt",1);
        readtree->SetBranchStatus("Jet25_px",1);
        readtree->SetBranchStatus("Jet25_py",1);
        readtree->SetBranchStatus("Jet25_qg",1);
    }
    readtree->SetBranchStatus("MC_weight",1);
    readtree->SetBranchStatus("MHT",1);
    readtree->SetBranchStatus("PFMET",1);
    readtree->SetBranchStatus("PFMETphi",1);
    readtree->SetBranchStatus("PU_weight",1);
    readtree->SetBranchStatus("Prefire",1);
    readtree->SetBranchStatus("Prefire_SysDown",1);
    readtree->SetBranchStatus("Prefire_SysUp",1);
    readtree->SetBranchStatus("SourceNumber",1);
    readtree->SetBranchStatus("SubCat2l",1);
    readtree->SetBranchStatus("Sum2lCharge",1);
    readtree->SetBranchStatus("Sum3LCharge",1);
    readtree->SetBranchStatus("TTHLep_2Ele",1);
    readtree->SetBranchStatus("TTHLep_2L",1);
    readtree->SetBranchStatus("TTHLep_2Mu",1);
    readtree->SetBranchStatus("TTHLep_3L",1);
    readtree->SetBranchStatus("TTHLep_MuEle",1);
    readtree->SetBranchStatus("Trig_1Ele",1);
    readtree->SetBranchStatus("Trig_1Mu",1);
    readtree->SetBranchStatus("Trig_1Mu1Ele",1);
    readtree->SetBranchStatus("Trig_1Mu2Ele",1);
    readtree->SetBranchStatus("Trig_2Ele",1);
    readtree->SetBranchStatus("Trig_2Mu",1);
    readtree->SetBranchStatus("Trig_2Mu1Ele",1);
    readtree->SetBranchStatus("Trig_3Ele",1);
    readtree->SetBranchStatus("Trig_3Mu",1);
    readtree->SetBranchStatus("TriggerSF",1);
    readtree->SetBranchStatus("TriggerSF_SysDown",1);
    readtree->SetBranchStatus("TriggerSF_SysUp",1);
    readtree->SetBranchStatus("Trilep_bestMVA",1);
    readtree->SetBranchStatus("Trilep_mtWmin",1);
    readtree->SetBranchStatus("Trilep_nTight",1);
    readtree->SetBranchStatus("Trilep_n_ele",1);
    readtree->SetBranchStatus("Trilep_n_mu",1);
    readtree->SetBranchStatus("Trilep_worseIso",1);
    readtree->SetBranchStatus("Trilep_worseMVA",1);
    readtree->SetBranchStatus("Trilep_worseSip",1);
    readtree->SetBranchStatus("angle_bbpp_highest2b",1);
    readtree->SetBranchStatus("angle_bbpp_loose2b",1);
    readtree->SetBranchStatus("cosa_highest2b",1);
    readtree->SetBranchStatus("acuteangle_bbpp_highest2b",1);
    readtree->SetBranchStatus("deta_highest2b",1);
    readtree->SetBranchStatus("angle_bbpp_truth2l2b",1);
    readtree->SetBranchStatus("avg_dr_jet",1);
    readtree->SetBranchStatus("bTagSF_weight",1);
    readtree->SetBranchStatus("bWeight",1);
    readtree->SetBranchStatus("bWeight_central",1);
    readtree->SetBranchStatus("bWeight_down_cferr1",1);
    readtree->SetBranchStatus("bWeight_down_cferr2",1);
    readtree->SetBranchStatus("bWeight_down_hf",1);
    readtree->SetBranchStatus("bWeight_down_hfstats1",1);
    readtree->SetBranchStatus("bWeight_down_hfstats2",1);
    readtree->SetBranchStatus("bWeight_down_jes",1);
    readtree->SetBranchStatus("bWeight_down_lf",1);
    readtree->SetBranchStatus("bWeight_down_lfstats1",1);
    readtree->SetBranchStatus("bWeight_down_lfstats2",1);
    readtree->SetBranchStatus("bWeight_up_cferr1",1);
    readtree->SetBranchStatus("bWeight_up_cferr2",1);
    readtree->SetBranchStatus("bWeight_up_hf",1);
    readtree->SetBranchStatus("bWeight_up_hfstats1",1);
    readtree->SetBranchStatus("bWeight_up_hfstats2",1);
    readtree->SetBranchStatus("bWeight_up_jes",1);
    readtree->SetBranchStatus("bWeight_up_lf",1);
    readtree->SetBranchStatus("bWeight_up_lfstats1",1);
    readtree->SetBranchStatus("bWeight_up_lfstats2",1);
    readtree->SetBranchStatus("dr_leps",1);
    readtree->SetBranchStatus("elelooseSF",1);
    readtree->SetBranchStatus("elelooseSF_SysDown",1);
    readtree->SetBranchStatus("elelooseSF_SysUp",1);
    readtree->SetBranchStatus("eletightSF",1);
    readtree->SetBranchStatus("eletightSF_SysDown",1);
    readtree->SetBranchStatus("eletightSF_SysUp",1);
    readtree->SetBranchStatus("fourthLep_isFromB",1);
    readtree->SetBranchStatus("fourthLep_isFromC",1);
    readtree->SetBranchStatus("fourthLep_isFromH",1);
    readtree->SetBranchStatus("fourthLep_isFromTop",1);
    readtree->SetBranchStatus("fourthLep_isFromZWH",1);
    readtree->SetBranchStatus("fourthLep_isMatchRightCharge",1);
    readtree->SetBranchStatus("fourthLep_mcMatchId",1);
    readtree->SetBranchStatus("fourthLep_mcPromptFS",1);
    readtree->SetBranchStatus("fourthLep_mcPromptGamma",1);
    readtree->SetBranchStatus("genWeight_muF0p5",1);
    readtree->SetBranchStatus("genWeight_muF2",1);
    readtree->SetBranchStatus("genWeight_muR0p5",1);
    readtree->SetBranchStatus("genWeight_muR2",1);
    readtree->SetBranchStatus("hadTop_BDT",1);
    readtree->SetBranchStatus("hadTop_pt",1);
    readtree->SetBranchStatus("isDiLepFake",1);
    readtree->SetBranchStatus("isDiLepOS",1);
    readtree->SetBranchStatus("isDiLepSR",1);
    readtree->SetBranchStatus("isQuaLepFake",1);
    readtree->SetBranchStatus("isQuaLepSR",1);
    readtree->SetBranchStatus("isSFOS_metLD",1);
    readtree->SetBranchStatus("isTriLepFake",1);
    readtree->SetBranchStatus("isTriLepSR",1);
    readtree->SetBranchStatus("isWZctrlFake",1);
    readtree->SetBranchStatus("isWZctrlSR",1);
    readtree->SetBranchStatus("isZZctrlFake",1);
    readtree->SetBranchStatus("isZZctrlSR",1);
    readtree->SetBranchStatus("Bin4Lctrl",1);
    readtree->SetBranchStatus("is4lctrlFake",1);
    readtree->SetBranchStatus("is4lctrlSR",1);
    readtree->SetBranchStatus("nZPair",1);
    readtree->SetBranchStatus("istHlikeDiLepFake",1);
    readtree->SetBranchStatus("istHlikeDiLepOS",1);
    readtree->SetBranchStatus("istHlikeDiLepSR",1);
    readtree->SetBranchStatus("istHlikeQuaLepFake",1);
    readtree->SetBranchStatus("istHlikeQuaLepSR",1);
    readtree->SetBranchStatus("istHlikeTriLepFake",1);
    readtree->SetBranchStatus("istHlikeTriLepSR",1);
    readtree->SetBranchStatus("isttWctrlFake",1);
    readtree->SetBranchStatus("isttWctrlOS",1);
    readtree->SetBranchStatus("isttWctrlSR",1);
    readtree->SetBranchStatus("isttZctrlFake",1);
    readtree->SetBranchStatus("isttZctrlSR",1);
    readtree->SetBranchStatus("jet1_DeepJet",1);
    readtree->SetBranchStatus("jet1_E",1);
    readtree->SetBranchStatus("jet1_QGdiscr",1);
    readtree->SetBranchStatus("jet1_eta",1);
    readtree->SetBranchStatus("jet1_phi",1);
    readtree->SetBranchStatus("jet1_pt",1);
    readtree->SetBranchStatus("jet2_DeepJet",1);
    readtree->SetBranchStatus("jet2_E",1);
    readtree->SetBranchStatus("jet2_QGdiscr",1);
    readtree->SetBranchStatus("jet2_eta",1);
    readtree->SetBranchStatus("jet2_phi",1);
    readtree->SetBranchStatus("jet2_pt",1);
    readtree->SetBranchStatus("jet3_DeepJet",1);
    readtree->SetBranchStatus("jet3_E",1);
    readtree->SetBranchStatus("jet3_QGdiscr",1);
    readtree->SetBranchStatus("jet3_eta",1);
    readtree->SetBranchStatus("jet3_phi",1);
    readtree->SetBranchStatus("jet3_pt",1);
    readtree->SetBranchStatus("jet4_DeepJet",1);
    readtree->SetBranchStatus("jet4_E",1);
    readtree->SetBranchStatus("jet4_QGdiscr",1);
    readtree->SetBranchStatus("jet4_eta",1);
    readtree->SetBranchStatus("jet4_phi",1);
    readtree->SetBranchStatus("jet4_pt",1);
    readtree->SetBranchStatus("jetFwd1_E",1);
    readtree->SetBranchStatus("jetFwd1_eta",1);
    readtree->SetBranchStatus("jetFwd1_phi",1);
    readtree->SetBranchStatus("jetFwd1_pt",1);
    readtree->SetBranchStatus("jetFwd2_E",1);
    readtree->SetBranchStatus("jetFwd2_eta",1);
    readtree->SetBranchStatus("jetFwd2_phi",1);
    readtree->SetBranchStatus("jetFwd2_pt",1);
    readtree->SetBranchStatus("jetFwd3_E",1);
    readtree->SetBranchStatus("jetFwd3_eta",1);
    readtree->SetBranchStatus("jetFwd3_phi",1);
    readtree->SetBranchStatus("jetFwd3_pt",1);
    readtree->SetBranchStatus("jetFwd4_E",1);
    readtree->SetBranchStatus("jetFwd4_eta",1);
    readtree->SetBranchStatus("jetFwd4_phi",1);
    readtree->SetBranchStatus("jetFwd4_pt",1);
    readtree->SetBranchStatus("leadLep_BDT",1);
    readtree->SetBranchStatus("leadLep_isFromB",1);
    readtree->SetBranchStatus("leadLep_isFromC",1);
    readtree->SetBranchStatus("leadLep_isFromH",1);
    readtree->SetBranchStatus("leadLep_isFromTop",1);
    readtree->SetBranchStatus("leadLep_isFromZWH",1);
    readtree->SetBranchStatus("leadLep_isMatchRightCharge",1);
    readtree->SetBranchStatus("leadLep_jetcsv",1);
    readtree->SetBranchStatus("leadLep_mcMatchId",1);
    readtree->SetBranchStatus("leadLep_mcPromptFS",1);
    readtree->SetBranchStatus("leadLep_mcPromptGamma",1);
    readtree->SetBranchStatus("lep1_E",1);
    readtree->SetBranchStatus("lep1_TightCharge",1);
    readtree->SetBranchStatus("lep1_charge",1);
    readtree->SetBranchStatus("lep1_conePt",1);
    readtree->SetBranchStatus("lep1_pt",1);
    readtree->SetBranchStatus("lep1_dxy",1);
    readtree->SetBranchStatus("lep1_dz",1);
    readtree->SetBranchStatus("lep1_eta",1);
    readtree->SetBranchStatus("lep1_isfakeablesel",1);
    readtree->SetBranchStatus("lep1_ismvasel",1);
    readtree->SetBranchStatus("lep1_lostHits",1);
    readtree->SetBranchStatus("lep1_minIso",1);
    readtree->SetBranchStatus("lep1_minIsoCh",1);
    readtree->SetBranchStatus("lep1_minIsoNeu",1);
    readtree->SetBranchStatus("lep1_mvaId",1);
    readtree->SetBranchStatus("lep1_passConv",1);
    readtree->SetBranchStatus("lep1_pdgId",1);
    readtree->SetBranchStatus("lep1_phi",1);
    readtree->SetBranchStatus("lep1_ptratio",1);
    readtree->SetBranchStatus("lep1_ptrel",1);
    readtree->SetBranchStatus("lep1_relIso03",1);
    readtree->SetBranchStatus("lep1_relIso04",1);
    readtree->SetBranchStatus("lep1_segment",1);
    readtree->SetBranchStatus("lep1_sig3d",1);
    readtree->SetBranchStatus("lep2_E",1);
    readtree->SetBranchStatus("lep2_TightCharge",1);
    readtree->SetBranchStatus("lep2_charge",1);
    readtree->SetBranchStatus("lep2_conePt",1);
    readtree->SetBranchStatus("lep2_pt",1);
    readtree->SetBranchStatus("lep2_dxy",1);
    readtree->SetBranchStatus("lep2_dz",1);
    readtree->SetBranchStatus("lep2_eta",1);
    readtree->SetBranchStatus("lep2_isfakeablesel",1);
    readtree->SetBranchStatus("lep2_ismvasel",1);
    readtree->SetBranchStatus("lep2_lostHits",1);
    readtree->SetBranchStatus("lep2_minIso",1);
    readtree->SetBranchStatus("lep2_minIsoCh",1);
    readtree->SetBranchStatus("lep2_minIsoNeu",1);
    readtree->SetBranchStatus("lep2_mvaId",1);
    readtree->SetBranchStatus("lep2_passConv",1);
    readtree->SetBranchStatus("lep2_pdgId",1);
    readtree->SetBranchStatus("lep2_phi",1);
    readtree->SetBranchStatus("lep2_ptratio",1);
    readtree->SetBranchStatus("lep2_ptrel",1);
    readtree->SetBranchStatus("lep2_relIso03",1);
    readtree->SetBranchStatus("lep2_relIso04",1);
    readtree->SetBranchStatus("lep2_segment",1);
    readtree->SetBranchStatus("lep2_sig3d",1);
    readtree->SetBranchStatus("lep3_BDT",1);
    readtree->SetBranchStatus("lep3_E",1);
    readtree->SetBranchStatus("lep3_TightCharge",1);
    readtree->SetBranchStatus("lep3_charge",1);
    readtree->SetBranchStatus("lep3_conePt",1);
    readtree->SetBranchStatus("lep3_dxy",1);
    readtree->SetBranchStatus("lep3_dz",1);
    readtree->SetBranchStatus("lep3_eta",1);
    readtree->SetBranchStatus("lep3_isfakeablesel",1);
    readtree->SetBranchStatus("lep3_ismvasel",1);
    readtree->SetBranchStatus("lep3_lostHits",1);
    readtree->SetBranchStatus("lep3_minIso",1);
    readtree->SetBranchStatus("lep3_minIsoCh",1);
    readtree->SetBranchStatus("lep3_minIsoNeu",1);
    readtree->SetBranchStatus("lep3_mvaId",1);
    readtree->SetBranchStatus("lep3_passConv",1);
    readtree->SetBranchStatus("lep3_pdgId",1);
    readtree->SetBranchStatus("lep3_phi",1);
    readtree->SetBranchStatus("lep3_ptratio",1);
    readtree->SetBranchStatus("lep3_ptrel",1);
    readtree->SetBranchStatus("lep3_relIso03",1);
    readtree->SetBranchStatus("lep3_relIso04",1);
    readtree->SetBranchStatus("lep3_segment",1);
    readtree->SetBranchStatus("lep3_sig3d",1);
    readtree->SetBranchStatus("lepSF",1);
    readtree->SetBranchStatus("lepSF_SysDown",1);
    readtree->SetBranchStatus("lepSF_SysUp",1);
    readtree->SetBranchStatus("leptonSF_weight",1);
    readtree->SetBranchStatus("ls",1);
    readtree->SetBranchStatus("mT2_W",1);
    readtree->SetBranchStatus("mT2_top_2particle",1);
    readtree->SetBranchStatus("mT2_top_3particle",1);
    readtree->SetBranchStatus("mT_lep1",1);
    readtree->SetBranchStatus("mT_lep2",1);
    readtree->SetBranchStatus("mass3L",1);
    readtree->SetBranchStatus("massL",1);
    readtree->SetBranchStatus("mass_dillep",1);
    readtree->SetBranchStatus("mass_diele",1);
    readtree->SetBranchStatus("mass_dilep",1);
    readtree->SetBranchStatus("massLT",1);
    readtree->SetBranchStatus("massL_SFOS",1);
    readtree->SetBranchStatus("massl",1);
    readtree->SetBranchStatus("massll",1);
    readtree->SetBranchStatus("max_lep_eta",1);
    readtree->SetBranchStatus("maxeta",1);
    readtree->SetBranchStatus("mbb",1);
    readtree->SetBranchStatus("mbb_loose",1);
    readtree->SetBranchStatus("metLD",1);
    readtree->SetBranchStatus("mht",1);
    readtree->SetBranchStatus("mhtT",1);
    readtree->SetBranchStatus("mhtT_met",1);
    readtree->SetBranchStatus("mht_met",1);
    readtree->SetBranchStatus("minMllAFAS",1);
    readtree->SetBranchStatus("minMllAFOS",1);
    readtree->SetBranchStatus("minMllSFOS",1);
    readtree->SetBranchStatus("min_Deta_leadfwdJet_jet",1);
    readtree->SetBranchStatus("min_Deta_mostfwdJet_jet",1);
    readtree->SetBranchStatus("min_dr_lep_jet",1);
    readtree->SetBranchStatus("mindr_lep1_jet",1);
    readtree->SetBranchStatus("mindr_lep2_jet",1);
    readtree->SetBranchStatus("mindr_lep3_jet",1);
    readtree->SetBranchStatus("mulooseSF",1);
    readtree->SetBranchStatus("mulooseSF_SysDown",1);
    readtree->SetBranchStatus("mulooseSF_SysUp",1);
    readtree->SetBranchStatus("mutightSF",1);
    readtree->SetBranchStatus("mutightSF_SysDown",1);
    readtree->SetBranchStatus("mutightSF_SysUp",1);
    readtree->SetBranchStatus("mvaOutput_2lss_ttV",1);
    readtree->SetBranchStatus("mvaOutput_2lss_ttbar",1);
    readtree->SetBranchStatus("nBJetLoose",1);
    readtree->SetBranchStatus("nBJetMedium",1);
    readtree->SetBranchStatus("nBestVtx",1);
    readtree->SetBranchStatus("nElectron",1);
    readtree->SetBranchStatus("nEvent",1);
    readtree->SetBranchStatus("nLepTight",1);
    readtree->SetBranchStatus("nLep_Cat",1);
    readtree->SetBranchStatus("nLightJet",1);
    readtree->SetBranchStatus("n_fakeablesel_ele",1);
    readtree->SetBranchStatus("n_fakeablesel_mu",1);
    readtree->SetBranchStatus("n_mvasel_ele",1);
    readtree->SetBranchStatus("n_mvasel_mu",1);
    readtree->SetBranchStatus("n_presel_ele",1);
    readtree->SetBranchStatus("n_presel_jet",1);
    readtree->SetBranchStatus("n_presel_jetFwd",1);
    readtree->SetBranchStatus("n_presel_mu",1);
    readtree->SetBranchStatus("n_presel_tau",1);
    readtree->SetBranchStatus("puWeight",1);
    readtree->SetBranchStatus("puWeight_SysDown",1);
    readtree->SetBranchStatus("puWeight_SysUp",1);
    readtree->SetBranchStatus("PUWeight",1);
    readtree->SetBranchStatus("MinBiasUpWeight",1);
    readtree->SetBranchStatus("MinBiasDownWeight",1);
    readtree->SetBranchStatus("run",1);
    readtree->SetBranchStatus("secondLep_BDT",1);
    readtree->SetBranchStatus("secondLep_isFromB",1);
    readtree->SetBranchStatus("secondLep_isFromC",1);
    readtree->SetBranchStatus("secondLep_isFromH",1);
    readtree->SetBranchStatus("secondLep_isFromTop",1);
    readtree->SetBranchStatus("secondLep_isFromZWH",1);
    readtree->SetBranchStatus("secondLep_isMatchRightCharge",1);
    readtree->SetBranchStatus("secondLep_jetcsv",1);
    readtree->SetBranchStatus("secondLep_mcMatchId",1);
    readtree->SetBranchStatus("secondLep_mcPromptFS",1);
    readtree->SetBranchStatus("secondLep_mcPromptGamma",1);
    readtree->SetBranchStatus("thirdLep_isFromB",1);
    readtree->SetBranchStatus("thirdLep_isFromC",1);
    readtree->SetBranchStatus("thirdLep_isFromH",1);
    readtree->SetBranchStatus("thirdLep_isFromTop",1);
    readtree->SetBranchStatus("thirdLep_isFromZWH",1);
    readtree->SetBranchStatus("thirdLep_isMatchRightCharge",1);
    readtree->SetBranchStatus("thirdLep_mcMatchId",1);
    readtree->SetBranchStatus("thirdLep_mcPromptFS",1);
    readtree->SetBranchStatus("thirdLep_mcPromptGamma",1);
    readtree->SetBranchStatus("triggerSF_weight",1);
    readtree->SetBranchStatus("trueInteractions",1);
};

void create_lwtnn(TString input_json_file, lwt::LightweightNeuralNetwork*& NN_instance){
   lwt::JSONConfig network_file;
   // Read in the network file
   cout << " load nn json file : " << input_json_file  << endl;
   std::string in_file_name(input_json_file);
   std::ifstream in_file(in_file_name);
   network_file = lwt::parse_json(in_file);
   // Create a new lwtn netowrk instance
   NN_instance = new lwt::LightweightNeuralNetwork(network_file.inputs, 
      network_file.layers, network_file.outputs);
}

int ttH_catIndex_2lss_SVA(int LepGood1_pdgId, int LepGood2_pdgId, int LepGood1_charge, int nJet25, int is_tH_enlarged){

    int res = -1;
    if(is_tH_enlarged==1) return res;
    if(nJet25 <4){
        res = 0;
        return res;
    }

    if (abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11) res = 1; //ee
    if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && LepGood1_charge<0) res = 3; // em_neg
    if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && LepGood1_charge>0) res = 5; // em_pos
    if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && LepGood1_charge<0) res = 7; // mm_neg
    if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && LepGood1_charge>0) res = 9; // mm_pos
    if (nJet25>=6) res+=1;

    return res; // 1-10
}

int ttH_catIndex_2lss_3j_SVA(int LepGood1_pdgId, int LepGood2_pdgId, int LepGood1_charge, int nJet25, int is_tH_enlarged){

    int res = -1;
    if(is_tH_enlarged==1) return res;
    if(nJet25 !=3){
        res = 0;
        return res;
    }

    if (abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11) res = 1; //ee
    if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && LepGood1_charge<0) res = 2; // em_neg
    if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && LepGood1_charge>0) res = 3; // em_pos
    if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && LepGood1_charge<0) res = 4; // mm_neg
    if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && LepGood1_charge>0) res = 5; // mm_pos
    if (nJet25>=6) res+=1; // this should never happen

    return res; // 1-10
}

int SVAbin(double mass2l){
    std::vector<double> massEdges = {10.,40.0,55.0,70.0,80.0,95.0,110.0,140.0,180.,800.0};
    std::vector<double>::iterator lower; 
    lower = std::lower_bound(massEdges.begin(), massEdges.end(), mass2l);
    int pos = std::distance(massEdges.begin(), lower);
    int nbin = massEdges.size()-1;
    int res = min(nbin, max(1,pos));
    return res;
}

void setDNNflag(std::vector<double> DNN_vals, float& DNN_maxval, float& DNNCat, float& DNNSubCat1, float& DNNSubCat2, float Dilep_pdgId, float lep1_charge){
    std::vector<double>::iterator result; 
    result = std::max_element(DNN_vals.begin(), DNN_vals.end());
    int pos = std::distance(DNN_vals.begin(),result);
    DNNCat = pos + 1;
    DNN_maxval = DNN_vals.at(pos);
    if(Dilep_pdgId==3){//ee
        DNNSubCat1 = lep1_charge<0? 1:2; // neg:pos
    }else if(DNNCat==1){// ttH node
        DNNSubCat1 = Dilep_pdgId>1.5? 3:7;// em:mm
    }else if(DNNCat==2){// ttJnode
        DNNSubCat1 = Dilep_pdgId>1.5? 4:8;// em:mm
    }else if(DNNCat==3){// ttWnode
        DNNSubCat1 = Dilep_pdgId>1.5? 5:9;// em:mm
    }else if(DNNCat==4){// tHnode
        DNNSubCat1 = Dilep_pdgId>1.5? 6:10;// em:mm
    }else{
        std::cout<< " DNNCat is : "<<DNNCat << std::endl;
    }
    // DNNSubCat2
    if(DNNCat==1){// ttH node
        if(Dilep_pdgId==3){
            DNNSubCat2=1; //ee
        }
        else if(Dilep_pdgId==2){
            DNNSubCat2=5; //em
        }
        else if(Dilep_pdgId==1){
            DNNSubCat2=9; //mm
        }
        else std::cout<< " Dilep_pdgId is "<<Dilep_pdgId<<std::endl;
    }else if(DNNCat==2){// ttJnode
        if(Dilep_pdgId==3){
            DNNSubCat2=2; //ee
        }
        else if(Dilep_pdgId==2){
            DNNSubCat2=6; //em
        }
        else if(Dilep_pdgId==1){
            DNNSubCat2=10; //mm
        }
        else std::cout<< " Dilep_pdgId is "<<Dilep_pdgId<<std::endl;
    }else if(DNNCat==3){// ttWnode
        if(Dilep_pdgId==3){
            DNNSubCat2=3; //ee
        }
        else if(Dilep_pdgId==2){
            DNNSubCat2=7; //em
        }
        else if(Dilep_pdgId==1){
            DNNSubCat2=11; //mm
        }
        else std::cout<< " Dilep_pdgId is "<<Dilep_pdgId<<std::endl;
    }else if(DNNCat==4){// tHnode
        if(Dilep_pdgId==3){
            DNNSubCat2=4; //ee
        }
        else if(Dilep_pdgId==2){
            DNNSubCat2=8; //em
        }
        else if(Dilep_pdgId==1){
            DNNSubCat2=12; //mm
        }
        else std::cout<< " Dilep_pdgId is "<<Dilep_pdgId<<std::endl;
    }else{
        std::cout<< " DNNCat is : "<<DNNCat << std::endl;
    }
};

