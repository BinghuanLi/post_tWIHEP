// utils
double getMTlepmet(double phi1, double phi2, double pt1, double pt2);
double deltaPhi(double phi1, double phi2);
double get_rewgtlumi(TString FileName);
float lnN1D_p1(float kappa, float x, float xmin, float xmax); 
double getAngleOfPlanes(TVector3 plane1_vectA, TVector3 plane1_vectB, TVector3 plane2_vectA, TVector3 plane2_vectB);
// fake rate
void setFakeRateHistograms(TString FakeRateFileName,TString FakeRateMuonHistName, TString FakeRateElectronHistName, std::map<std::string, TH2F*> &_MuonFakeRate, std::map<std::string, TH2F*> &_ElectronFakeRate, std::string muSystName="central", std::string eleSystName="central");
Double_t getFakeRateWeight(float lep1_ismvasel, float lep1_pdgId, float lep1_conept, float lep1_eta, float lep2_ismvasel, float lep2_pdgId, float lep2_conept, float lep2_eta , std::map<std::string,TH2F*> _MuonFakeRate, std::map<std::string,TH2F*> _ElectronFakeRate, std::string muSystName="central", std::string eleSystName="central");
//SFs
std::tuple<Double_t,Double_t,Double_t> getTriggerWeight(float lep1_pdgId, float lep1_conept, float lep2_pdgId, float lep2_conept );
// charge Mis
void setChargeMisHistograms(TString ChargeMisFileName,TString ChargeMisHistName, TH2F** _chargeMis);
std::tuple<Double_t,Double_t,Double_t> getChargeMisWeight(float lep1_pdgId, float lep1_charge, float lep1_conept, float lep1_eta, float lep2_pdgId, float lep2_charge, float lep2_conept, float lep2_eta, TH2F* _chargeMis);
// Calculate Lorentz boosted angle
double get_boostedAngle(TLorentzVector Particle1_CMS, TLorentzVector Particle2_CMS, TLorentzVector plane1_vectA, TLorentzVector plane1_vectB, TLorentzVector plane2_vectA, TLorentzVector plane2_vectB);

//utils
double get_rewgtlumi(TString FileName){
    double wgt=1.;
    if(FileName.Contains("ttW_ext_Jets")) wgt=9070386./15458438.;
    if(FileName.Contains("ttWJets")) wgt=6388052./15458438.;
    if(FileName.Contains("ttZ_ext_Jets")) wgt=8455616./18134307.;
    if(FileName.Contains("ttZ_Jets")) wgt=9678691./18134307.;
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

double getAngleOfPlanes(TVector3 plane1_vectA, TVector3 plane1_vectB, TVector3 plane2_vectA, TVector3 plane2_vectB){
    double angle = -999;
    TVector3 plane1_norm = plane1_vectA.Cross(plane1_vectB);// get the vector perp to plane 1
    TVector3 plane2_norm = plane2_vectA.Cross(plane2_vectB);// get the vector perp to plane 2
    if(plane1_norm.Mag()==0){
        std::cout<< "two vectors provided to plane1 cannot determine a plane" << std::endl;
        return angle;
    }
    if(plane2_norm.Mag()==0){
        std::cout<< "two vectors provided to plane2 cannot determine a plane" << std::endl;
        return angle;
    }
    angle = plane1_norm.Angle(plane2_norm);
    return angle;
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
std::tuple<Double_t,Double_t,Double_t> getTriggerWeight(float lep1_pdgId, float lep1_conept, float lep2_pdgId, float lep2_conept ){
  Double_t TriggerWeight = 1.0, TriggerWeightUp = 1.0, TriggerWeightDown = 1.0;
  Int_t category = 0;
  if((fabs(lep1_pdgId)+fabs(lep2_pdgId))==22)category =1;
  else if((fabs(lep1_pdgId)+fabs(lep2_pdgId))==24)category =2;
  else if((fabs(lep1_pdgId)+fabs(lep2_pdgId))==26)category =3;
  // updated trigger SF for 2017 , see link :
  // https://gitlab.cern.ch/ttH_leptons/doc/blob/master/2017/appendix_1.md#for-lepton-id-scale-factors
  if(category ==3){//mm
      if(lep1_conept <35){
          TriggerWeight = 0.972; 
          TriggerWeightUp = 0.972 + 0.006;
          TriggerWeightDown = 0.972 - 0.006;
      }else{
          TriggerWeight = 0.994; 
          TriggerWeightUp = 0.994 + 0.001;
          TriggerWeightDown = 0.994 - 0.001;
      }
  }else if(category==1){//ee
      if(lep1_conept < 30){
          TriggerWeight = 0.937; 
          TriggerWeightUp = 0.937 + 0.027;
          TriggerWeightDown = 0.937 - 0.027;
      }else{
          TriggerWeight = 0.991; 
          TriggerWeightUp = 0.991 + 0.002;
          TriggerWeightDown = 0.991 - 0.002;
      }
  }else if(category==2){//em
      if(lep1_conept < 35){
          TriggerWeight = 0.952; 
          TriggerWeightUp = 0.952 + 0.008;
          TriggerWeightDown = 0.952 - 0.008;
      }else if(lep1_conept <50){
          TriggerWeight = 0.983; 
          TriggerWeightUp = 0.983 + 0.003;
          TriggerWeightDown = 0.983 - 0.003;
      }else{
          TriggerWeight = 1.0; 
          TriggerWeightUp = 1.0 + 0.001;
          TriggerWeightDown = 1.0 - 0.001;
      }
  }
  return std::make_tuple(TriggerWeight,TriggerWeightUp,TriggerWeightDown);
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
double get_boostedAngle(TLorentzVector Particle1_CMS, TLorentzVector Particle2_CMS, TLorentzVector plane1_vectA, TLorentzVector plane1_vectB, TLorentzVector plane2_vectA, TLorentzVector plane2_vectB){
    // Input : All six vectors are in lab frame
    //  Particle1_CMS and Particle2_CMS => rod frame
    //  plane1(2)_vectA and plane1(2)_vectB => vectors to determine plane 1 and plane 2
    // Output : the angle of plane1 and plane2 in the center of mass system of Particle1_CMS and Particle2_CMS
    // https://root-forum.cern.ch/t/how-to-use-boost-in-tlorentzvector/4102
    double angle = -99;
    TLorentzVector MyParticleCombi;
    MyParticleCombi.SetPxPyPzE(Particle1_CMS.Px()+Particle2_CMS.Px(),Particle1_CMS.Py()+Particle2_CMS.Py(), Particle1_CMS.Pz()+Particle2_CMS.Pz(), Particle1_CMS.E()+Particle2_CMS.E());
    TVector3  MyParticleCombi_BoostVector = MyParticleCombi.BoostVector();
    // minus because we boost from lab to rod
    plane1_vectA.Boost(-MyParticleCombi_BoostVector); 
    plane1_vectB.Boost(-MyParticleCombi_BoostVector); 
    plane2_vectA.Boost(-MyParticleCombi_BoostVector); 
    plane2_vectB.Boost(-MyParticleCombi_BoostVector); 

    angle = getAngleOfPlanes( plane1_vectA.Vect(),  plane1_vectB.Vect(),  plane2_vectA.Vect(),  plane2_vectB.Vect());

    return angle;
    
}
