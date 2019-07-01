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
// read trees
void SetOldTreeBranchStatus(TTree* readtree);
//utils
double get_rewgtlumi(TString FileName){
    double wgt=1.;
    //if(FileName.Contains("ttW_ext_Jets")) wgt=9070386./15458438.;
    //if(FileName.Contains("ttWJets")) wgt=6388052./15458438.;
    //if(FileName.Contains("ttZ_ext_Jets")) wgt=8455616./18134307.;
    //if(FileName.Contains("ttZ_Jets")) wgt=9678691./18134307.;
    if(FileName.Contains("WZTo3LNu")) wgt=4.42965/5.063;
    //if(FileName.Contains("THQ")) wgt=0.07096*8837.23781460*123798.0/(0.7927*25.69875024);
    //if(FileName.Contains("THW")) wgt=0.01561*5458.47479968*49936.0/(0.1472*3.21369648);
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
//read trees
void SetOldTreeBranchStatus(TTree* readtree){
   readtree->SetBranchStatus("*",0);
   /*
   //readtree->SetBranchStatus("pvertex_ndof",1);
   //readtree->SetBranchStatus("pvertex_z",1);
   //readtree->SetBranchStatus("pvertex_dxy",1);
   readtree->SetBranchStatus("mu1_pt",1);
   readtree->SetBranchStatus("mu1_conept",1);
   readtree->SetBranchStatus("mu1_eta",1);
   readtree->SetBranchStatus("mu1_phi",1);
   readtree->SetBranchStatus("mu1_E",1);
   readtree->SetBranchStatus("mu1_miniRelIso",1);
   readtree->SetBranchStatus("mu1_miniIsoCharged",1);
   readtree->SetBranchStatus("mu1_miniIsoNeutral",1);
   readtree->SetBranchStatus("mu1_jetPtRel",1);
   readtree->SetBranchStatus("mu1_jetPtRatio",1);
   readtree->SetBranchStatus("mu1_jetCSV",1);
   readtree->SetBranchStatus("mu1_sip3D",1);
   readtree->SetBranchStatus("mu1_dxyAbs",1);
   readtree->SetBranchStatus("mu1_dz",1);
   readtree->SetBranchStatus("mu1_segmentCompatibility",1);
   readtree->SetBranchStatus("mu1_leptonMVA",1);
   readtree->SetBranchStatus("mu1_dpt_div_pt",1);
   readtree->SetBranchStatus("mu2_pt",1);
   readtree->SetBranchStatus("mu2_conept",1);
   readtree->SetBranchStatus("mu2_eta",1);
   readtree->SetBranchStatus("mu2_phi",1);
   readtree->SetBranchStatus("mu2_E",1);
   readtree->SetBranchStatus("mu2_miniRelIso",1);
   readtree->SetBranchStatus("mu2_miniIsoCharged",1);
   readtree->SetBranchStatus("mu2_miniIsoNeutral",1);
   readtree->SetBranchStatus("mu2_jetPtRel",1);
   readtree->SetBranchStatus("mu2_jetPtRatio",1);
   readtree->SetBranchStatus("mu2_jetCSV",1);
   readtree->SetBranchStatus("mu2_sip3D",1);
   readtree->SetBranchStatus("mu2_dxyAbs",1);
   readtree->SetBranchStatus("mu2_dz",1);
   readtree->SetBranchStatus("mu2_segmentCompatibility",1);
   readtree->SetBranchStatus("mu2_leptonMVA",1);
   readtree->SetBranchStatus("mu2_dpt_div_pt",1);
   readtree->SetBranchStatus("ele1_pt",1);
   readtree->SetBranchStatus("ele1_conept",1);
   readtree->SetBranchStatus("ele1_eta",1);
   readtree->SetBranchStatus("ele1_phi",1);
   readtree->SetBranchStatus("ele1_E",1);
   readtree->SetBranchStatus("ele1_miniRelIso",1);
   readtree->SetBranchStatus("ele1_miniIsoCharged",1);
   readtree->SetBranchStatus("ele1_miniIsoNeutral",1);
   readtree->SetBranchStatus("ele1_jetPtRel",1);
   readtree->SetBranchStatus("ele1_jetPtRatio",1);
   readtree->SetBranchStatus("ele1_jetCSV",1);
   readtree->SetBranchStatus("ele1_sip3D",1);
   readtree->SetBranchStatus("ele1_dxyAbs",1);
   readtree->SetBranchStatus("ele1_dz",1);
   readtree->SetBranchStatus("ele1_ntMVAeleID",1);
   readtree->SetBranchStatus("ele1_leptonMVA",1);
   readtree->SetBranchStatus("ele2_pt",1);
   readtree->SetBranchStatus("ele2_conept",1);
   readtree->SetBranchStatus("ele2_eta",1);
   readtree->SetBranchStatus("ele2_phi",1);
   readtree->SetBranchStatus("ele2_E",1);
   readtree->SetBranchStatus("ele2_miniRelIso",1);
   readtree->SetBranchStatus("ele2_miniIsoCharged",1);
   readtree->SetBranchStatus("ele2_miniIsoNeutral",1);
   readtree->SetBranchStatus("ele2_jetPtRel",1);
   readtree->SetBranchStatus("ele2_jetPtRatio",1);
   readtree->SetBranchStatus("ele2_jetCSV",1);
   readtree->SetBranchStatus("ele2_sip3D",1);
   readtree->SetBranchStatus("ele2_dxyAbs",1);
   readtree->SetBranchStatus("ele2_dz",1);
   readtree->SetBranchStatus("ele2_ntMVAeleID",1);
   readtree->SetBranchStatus("ele2_leptonMVA",1);
   readtree->SetBranchStatus("mu1_mediumID",1);
   readtree->SetBranchStatus("mu1_isfakeablesel",1);
   readtree->SetBranchStatus("mu1_ismvasel",1);
   readtree->SetBranchStatus("mu2_mediumID",1);
   readtree->SetBranchStatus("mu2_isfakeablesel",1);
   readtree->SetBranchStatus("mu2_ismvasel",1);
   readtree->SetBranchStatus("ele1_isfakeablesel",1);
   readtree->SetBranchStatus("ele1_ismvasel",1);
   readtree->SetBranchStatus("ele1_isChargeConsistent",1);
   readtree->SetBranchStatus("ele1_passesConversionVeto",1);
   readtree->SetBranchStatus("ele2_isfakeablesel",1);
   readtree->SetBranchStatus("ele2_ismvasel",1);
   readtree->SetBranchStatus("ele2_isChargeConsistent",1);
   readtree->SetBranchStatus("ele2_passesConversionVeto",1);
   readtree->SetBranchStatus("mu1_charge",1);
   readtree->SetBranchStatus("mu1_jetNDauChargedMVASel",1);
   readtree->SetBranchStatus("mu2_charge",1);
   readtree->SetBranchStatus("mu2_jetNDauChargedMVASel",1);
   readtree->SetBranchStatus("ele1_charge",1);
   readtree->SetBranchStatus("ele1_jetNDauChargedMVASel",1);
   readtree->SetBranchStatus("ele1_nMissingHits",1);
   readtree->SetBranchStatus("ele2_charge",1);
   readtree->SetBranchStatus("ele2_jetNDauChargedMVASel",1);
   readtree->SetBranchStatus("ele2_nMissingHits",1);
   readtree->SetBranchStatus("mu1_PFRelIso04",1);
   readtree->SetBranchStatus("mu2_PFRelIso04",1);
   readtree->SetBranchStatus("ele1_PFRelIso04",1);
   readtree->SetBranchStatus("ele1_sigmaEtaEta",1);
   readtree->SetBranchStatus("ele1_HoE",1);
   readtree->SetBranchStatus("ele1_deltaEta",1);
   readtree->SetBranchStatus("ele1_deltaPhi",1);
   readtree->SetBranchStatus("ele1_OoEminusOoP",1);
   readtree->SetBranchStatus("ele2_PFRelIso04",1);
   readtree->SetBranchStatus("ele2_sigmaEtaEta",1);
   readtree->SetBranchStatus("ele2_HoE",1);
   readtree->SetBranchStatus("ele2_deltaEta",1);
   readtree->SetBranchStatus("ele2_deltaPhi",1);
   readtree->SetBranchStatus("ele2_OoEminusOoP",1);
   */
   readtree->SetBranchStatus("HiggsDecay",1);
   readtree->SetBranchStatus("tau1_pt",1);
   readtree->SetBranchStatus("tau1_eta",1);
   readtree->SetBranchStatus("tau1_phi",1);
   readtree->SetBranchStatus("tau1_E",1);
   readtree->SetBranchStatus("tau1_dxy",1);
   readtree->SetBranchStatus("tau1_dz",1);
   readtree->SetBranchStatus("tau1_byVLooseIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau1_byLooseIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau1_rawMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau1_decayModeFindingOldDMs",1);
   readtree->SetBranchStatus("tau2_pt",1);
   readtree->SetBranchStatus("tau2_eta",1);
   readtree->SetBranchStatus("tau2_phi",1);
   readtree->SetBranchStatus("tau2_E",1);
   readtree->SetBranchStatus("tau2_dxy",1);
   readtree->SetBranchStatus("tau2_dz",1);
   readtree->SetBranchStatus("tau2_byVLooseIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau2_byLooseIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau2_rawMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau2_decayModeFindingOldDMs",1);
   readtree->SetBranchStatus("jet8_pt",1);
   readtree->SetBranchStatus("jet8_eta",1);
   readtree->SetBranchStatus("jet8_phi",1);
   readtree->SetBranchStatus("jet8_E",1);
   readtree->SetBranchStatus("jet8_CSV",1);
   readtree->SetBranchStatus("jet7_pt",1);
   readtree->SetBranchStatus("jet7_eta",1);
   readtree->SetBranchStatus("jet7_phi",1);
   readtree->SetBranchStatus("jet7_E",1);
   readtree->SetBranchStatus("jet7_CSV",1);
   readtree->SetBranchStatus("jet6_pt",1);
   readtree->SetBranchStatus("jet6_eta",1);
   readtree->SetBranchStatus("jet6_phi",1);
   readtree->SetBranchStatus("jet6_E",1);
   readtree->SetBranchStatus("jet6_CSV",1);
   readtree->SetBranchStatus("jet5_pt",1);
   readtree->SetBranchStatus("jet5_eta",1);
   readtree->SetBranchStatus("jet5_phi",1);
   readtree->SetBranchStatus("jet5_E",1);
   readtree->SetBranchStatus("jet5_CSV",1);
   readtree->SetBranchStatus("jet4_pt",1);
   readtree->SetBranchStatus("jet4_eta",1);
   readtree->SetBranchStatus("jet4_phi",1);
   readtree->SetBranchStatus("jet4_E",1);
   readtree->SetBranchStatus("jet4_CSV",1);
   readtree->SetBranchStatus("jet1_pt",1);
   readtree->SetBranchStatus("jet1_eta",1);
   readtree->SetBranchStatus("jet1_phi",1);
   readtree->SetBranchStatus("jet1_E",1);
   readtree->SetBranchStatus("jet1_CSV",1);
   readtree->SetBranchStatus("jet2_pt",1);
   readtree->SetBranchStatus("jet2_eta",1);
   readtree->SetBranchStatus("jet2_phi",1);
   readtree->SetBranchStatus("jet2_E",1);
   readtree->SetBranchStatus("jet2_CSV",1);
   readtree->SetBranchStatus("jet3_pt",1);
   readtree->SetBranchStatus("jet3_eta",1);
   readtree->SetBranchStatus("jet3_phi",1);
   readtree->SetBranchStatus("jet3_E",1);
   readtree->SetBranchStatus("jet3_CSV",1);
   readtree->SetBranchStatus("jetFwd4_pt",1);
   readtree->SetBranchStatus("jetFwd4_eta",1);
   readtree->SetBranchStatus("jetFwd4_phi",1);
   readtree->SetBranchStatus("jetFwd4_E",1);
   readtree->SetBranchStatus("jetFwd1_pt",1);
   readtree->SetBranchStatus("jetFwd1_eta",1);
   readtree->SetBranchStatus("jetFwd1_phi",1);
   readtree->SetBranchStatus("jetFwd1_E",1);
   readtree->SetBranchStatus("jetFwd2_pt",1);
   readtree->SetBranchStatus("jetFwd2_eta",1);
   readtree->SetBranchStatus("jetFwd2_phi",1);
   readtree->SetBranchStatus("jetFwd2_E",1);
   readtree->SetBranchStatus("jetFwd3_pt",1);
   readtree->SetBranchStatus("jetFwd3_eta",1);
   readtree->SetBranchStatus("jetFwd3_phi",1);
   readtree->SetBranchStatus("jetFwd3_E",1);
   readtree->SetBranchStatus("PFMET",1);
   readtree->SetBranchStatus("PFMETphi",1);
   readtree->SetBranchStatus("MHT",1);
   readtree->SetBranchStatus("metLD",1);
   readtree->SetBranchStatus("mht",1);
   readtree->SetBranchStatus("mhtT",1);
   readtree->SetBranchStatus("mhtT_met",1);
   readtree->SetBranchStatus("mht_met",1);
   readtree->SetBranchStatus("lep1_conePt",1);
   readtree->SetBranchStatus("lep2_conePt",1);
   readtree->SetBranchStatus("lep3_conePt",1);
   readtree->SetBranchStatus("mindr_lep1_jet",1);
   readtree->SetBranchStatus("mindr_lep2_jet",1);
   readtree->SetBranchStatus("mindr_lep3_jet",1);
   readtree->SetBranchStatus("mT_lep1",1);
   readtree->SetBranchStatus("mT_lep2",1);
   readtree->SetBranchStatus("min_dr_lep_jet",1);
   readtree->SetBranchStatus("dr_leps",1);
   readtree->SetBranchStatus("max_lep_eta",1);
   readtree->SetBranchStatus("mbb",1);
   readtree->SetBranchStatus("mbb_loose",1);
   readtree->SetBranchStatus("Hj_tagger_resTop",1);
   readtree->SetBranchStatus("Hj_tagger_hadTop",1);
   readtree->SetBranchStatus("HTT",1);
   readtree->SetBranchStatus("nBJetLoose",1);
   readtree->SetBranchStatus("nBJetMedium",1);
   readtree->SetBranchStatus("n_presel_jetFwd",1);
   readtree->SetBranchStatus("nLightJet",1);
   readtree->SetBranchStatus("FR_weight",1);
   readtree->SetBranchStatus("triggerSF_weight",1);
   readtree->SetBranchStatus("bTagSF_weight",1);
   readtree->SetBranchStatus("PU_weight",1);
   readtree->SetBranchStatus("MC_weight",1);
   readtree->SetBranchStatus("mvaOutput_2lss_ttV",1);
   readtree->SetBranchStatus("mvaOutput_2lss_ttbar",1);
   readtree->SetBranchStatus("avg_dr_jet",1);
   readtree->SetBranchStatus("nEvent",1);
   readtree->SetBranchStatus("ls",1);
   readtree->SetBranchStatus("run",1);
   readtree->SetBranchStatus("n_presel_mu",1);
   readtree->SetBranchStatus("n_fakeablesel_mu",1);
   readtree->SetBranchStatus("n_mvasel_mu",1);
   readtree->SetBranchStatus("n_presel_ele",1);
   readtree->SetBranchStatus("n_fakeablesel_ele",1);
   readtree->SetBranchStatus("n_mvasel_ele",1);
   readtree->SetBranchStatus("n_presel_tau",1);
   readtree->SetBranchStatus("n_fakeablesel_tau",1);
   readtree->SetBranchStatus("n_presel_jet",1);
   readtree->SetBranchStatus("tau1_charge",1);
   readtree->SetBranchStatus("tau1_decayModeFindingOldDMs",1);
   readtree->SetBranchStatus("tau1_decayModeFindingNewDMs",1);
   readtree->SetBranchStatus("tau1_byLooseCombinedIsolationDeltaBetaCorr3Hits",1);
   readtree->SetBranchStatus("tau1_byMediumCombinedIsolationDeltaBetaCorr3Hits",1);
   readtree->SetBranchStatus("tau1_byTightCombinedIsolationDeltaBetaCorr3Hits",1);
   readtree->SetBranchStatus("tau1_byLooseCombinedIsolationDeltaBetaCorr3HitsdR03",1);
   readtree->SetBranchStatus("tau1_byMediumCombinedIsolationDeltaBetaCorr3HitsdR03",1);
   readtree->SetBranchStatus("tau1_byTightCombinedIsolationDeltaBetaCorr3HitsdR03",1);
   readtree->SetBranchStatus("tau1_byLooseIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau1_byMediumIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau1_byTightIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau1_byVTightIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau2_charge",1);
   readtree->SetBranchStatus("tau2_decayModeFindingOldDMs",1);
   readtree->SetBranchStatus("tau2_decayModeFindingNewDMs",1);
   readtree->SetBranchStatus("tau2_byLooseCombinedIsolationDeltaBetaCorr3Hits",1);
   readtree->SetBranchStatus("tau2_byMediumCombinedIsolationDeltaBetaCorr3Hits",1);
   readtree->SetBranchStatus("tau2_byTightCombinedIsolationDeltaBetaCorr3Hits",1);
   readtree->SetBranchStatus("tau2_byLooseCombinedIsolationDeltaBetaCorr3HitsdR03",1);
   readtree->SetBranchStatus("tau2_byMediumCombinedIsolationDeltaBetaCorr3HitsdR03",1);
   readtree->SetBranchStatus("tau2_byTightCombinedIsolationDeltaBetaCorr3HitsdR03",1);
   readtree->SetBranchStatus("tau2_byLooseIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau2_byMediumIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau2_byTightIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau2_byVTightIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("maxeta",1);
   readtree->SetBranchStatus("massL",1);
   readtree->SetBranchStatus("massll",1);
   readtree->SetBranchStatus("massL_SFOS",1);
   readtree->SetBranchStatus("mass_diele",1);
   readtree->SetBranchStatus("mass_dilep",1);
   readtree->SetBranchStatus("Bin2l",1);
   readtree->SetBranchStatus("SubCat2l",1);
   readtree->SetBranchStatus("Sum2lCharge",1);
   readtree->SetBranchStatus("Dilep_bestMVA",1);
   readtree->SetBranchStatus("Dilep_worseMVA",1);
   readtree->SetBranchStatus("Dilep_pdgId",1);
   readtree->SetBranchStatus("Dilep_htllv",1);
   readtree->SetBranchStatus("Dilep_mtWmin",1);
   readtree->SetBranchStatus("Dilep_nTight",1);
   readtree->SetBranchStatus("HighestJetCSV",1);
   readtree->SetBranchStatus("HtJet",1);
   readtree->SetBranchStatus("nBestVtx",1);
   readtree->SetBranchStatus("minMllAFAS",1);
   readtree->SetBranchStatus("minMllAFOS",1);
   readtree->SetBranchStatus("minMllSFOS",1);
   readtree->SetBranchStatus("leadLep_isMatchRightCharge",1);
   readtree->SetBranchStatus("leadLep_mcMatchId",1);
   readtree->SetBranchStatus("leadLep_isFromTop",1);
   readtree->SetBranchStatus("leadLep_isFromH",1);
   readtree->SetBranchStatus("leadLep_isFromB",1);
   readtree->SetBranchStatus("leadLep_isFromC",1);
   readtree->SetBranchStatus("leadLep_mcPromptGamma",1);
   readtree->SetBranchStatus("leadLep_mcPromptFS",1);
   readtree->SetBranchStatus("secondLep_isMatchRightCharge",1);
   readtree->SetBranchStatus("secondLep_mcMatchId",1);
   readtree->SetBranchStatus("secondLep_isFromTop",1);
   readtree->SetBranchStatus("secondLep_isFromH",1);
   readtree->SetBranchStatus("secondLep_isFromB",1);
   readtree->SetBranchStatus("secondLep_isFromC",1);
   readtree->SetBranchStatus("secondLep_mcPromptGamma",1);
   readtree->SetBranchStatus("secondLep_mcPromptFS",1);
   //readtree->SetBranchStatus("Jet_numLoose",1);
   readtree->SetBranchStatus("leadLep_corrpt",1);
   readtree->SetBranchStatus("secondLep_corrpt",1);
   readtree->SetBranchStatus("leadLep_jetdr",1);
   readtree->SetBranchStatus("leadLep_jetcsv",1);
   readtree->SetBranchStatus("secondLep_jetdr",1);
   readtree->SetBranchStatus("secondLep_jetcsv",1);
   readtree->SetBranchStatus("Mt_metleadlep",1);
   readtree->SetBranchStatus("hadTop_BDT",1);
   readtree->SetBranchStatus("hadTop_pt",1);
   readtree->SetBranchStatus("leadLep_BDT",1);
   readtree->SetBranchStatus("secondLep_BDT",1);
   readtree->SetBranchStatus("thirdLep_jetcsv",1);
   readtree->SetBranchStatus("nLepTight",1);
   readtree->SetBranchStatus("trueInteractions",1);
   readtree->SetBranchStatus("nLepFO",1);
   readtree->SetBranchStatus("resTop_BDT",1);
   readtree->SetBranchStatus("TTHLep_2L",1);
   //readtree->SetBranchStatus("Hj1_BDT",1);
   //if(skimType ==0){
   /*
       readtree->SetBranchStatus("HadTop_Dr_leph_bfromlTop",1);
       readtree->SetBranchStatus("HadTop_bjet_lepTop_csv",1);
       readtree->SetBranchStatus("HadTop_bjet_hadTop_csv",1);
       readtree->SetBranchStatus("HadTop_reco_hadTop_pt",1);
       readtree->SetBranchStatus("HadTop_reco_hadTop_mass",1);
       readtree->SetBranchStatus("HadTop_reco_WhadTop_mass",1);
       readtree->SetBranchStatus("HadTop_PtRatio_leptOverleph",1);
       readtree->SetBranchStatus("HadTop_Dr_lept_bfromlTop",1);
       readtree->SetBranchStatus("HadTop_Dr_lept_bfromhTop",1);
       readtree->SetBranchStatus("Jet25_isToptag",1);
       readtree->SetBranchStatus("bjet_resTop_index",1);
       readtree->SetBranchStatus("wjet1_resTop_index",1);
       readtree->SetBranchStatus("wjet2_resTop_index",1);
       readtree->SetBranchStatus("Jet25_isResToptag",1);
       readtree->SetBranchStatus("Jet25_axis2",1);
       readtree->SetBranchStatus("Jet25_qg",1);
       readtree->SetBranchStatus("Jet25_bDiscriminator",1);
       readtree->SetBranchStatus("Jet25_pfCombinedInclusiveSecondaryVertexV2BJetTags",1);
       readtree->SetBranchStatus("Jet25_pfCombinedMVAV2BJetTags",1);
       readtree->SetBranchStatus("Jet25_pfJetProbabilityBJetTags",1);
       readtree->SetBranchStatus("Jet25_pfDeepCSVCvsLJetTags",1);
       readtree->SetBranchStatus("Jet25_pfDeepCSVCvsBJetTags",1);
       readtree->SetBranchStatus("Jet25_ptD",1);
       readtree->SetBranchStatus("Jet25_mult",1);
       readtree->SetBranchStatus("Jet25_pfCombinedCvsLJetTags",1);
       readtree->SetBranchStatus("Jet25_pfCombinedCvsBJetTags",1);
       readtree->SetBranchStatus("Jet25_pt",1);
       readtree->SetBranchStatus("Jet25_eta",1);
       readtree->SetBranchStatus("Jet25_phi",1);
       readtree->SetBranchStatus("Jet25_energy",1);
       readtree->SetBranchStatus("Jet25_px",1);
       readtree->SetBranchStatus("Jet25_py",1);
       readtree->SetBranchStatus("Jet25_pz",1);
       readtree->SetBranchStatus("Jet25_mass",1);
       readtree->SetBranchStatus("Jet25_isFromH",1);
       readtree->SetBranchStatus("Jet25_isFromTop",1);
       readtree->SetBranchStatus("Jet25_matchId",1);
       readtree->SetBranchStatus("Jet25_neutralHadEnergyFraction",1);
       //readtree->SetBranchStatus("Jet25_neutralEmEnergyFraction",1);
       readtree->SetBranchStatus("Jet25_chargedHadronEnergyFraction",1);
       readtree->SetBranchStatus("Jet25_chargedEmEnergyFraction",1);
       readtree->SetBranchStatus("Jet25_muonEnergyFraction",1);
       readtree->SetBranchStatus("Jet25_electronEnergy",1);
       readtree->SetBranchStatus("Jet25_photonEnergy",1);
       //readtree->SetBranchStatus("Jet25_emEnergyFraction",1);
       readtree->SetBranchStatus("Jet25_numberOfConstituents",1);
       readtree->SetBranchStatus("Jet25_chargedMultiplicity",1);
       readtree->SetBranchStatus("Jet25_metptratio",1);
       readtree->SetBranchStatus("Jet25_dilepmetptratio",1);
       readtree->SetBranchStatus("Jet25_nonjdr",1);
       readtree->SetBranchStatus("Jet25_nonjdilepdr",1);
       readtree->SetBranchStatus("Jet25_lepdrmin",1);
       readtree->SetBranchStatus("Jet25_lepdrmax",1);
       readtree->SetBranchStatus("Jet25_dilepdr",1);
       readtree->SetBranchStatus("Jet25_bjdr",1);
       readtree->SetBranchStatus("Jet25_nonjdeta",1);
       readtree->SetBranchStatus("Jet25_nonjdilepdeta",1);
       readtree->SetBranchStatus("Jet25_lepdetamin",1);
       readtree->SetBranchStatus("Jet25_lepdetamax",1);
       readtree->SetBranchStatus("Jet25_dilepdeta",1);
       readtree->SetBranchStatus("Jet25_bjdeta",1);
       readtree->SetBranchStatus("Jet25_nonjdphi",1);
       readtree->SetBranchStatus("Jet25_nonjdilepdphi",1);
       readtree->SetBranchStatus("Jet25_lepdphimin",1);
       readtree->SetBranchStatus("Jet25_lepdphimax",1);
       readtree->SetBranchStatus("Jet25_dilepdphi",1);
       readtree->SetBranchStatus("Jet25_bjdphi",1);
       readtree->SetBranchStatus("Jet25_nonjptratio",1);
       readtree->SetBranchStatus("Jet25_nonjdilepptratio",1);
       readtree->SetBranchStatus("Jet25_lepptratiomin",1);
       readtree->SetBranchStatus("Jet25_lepptratiomax",1);
       readtree->SetBranchStatus("Jet25_dilepptratio",1);
       readtree->SetBranchStatus("Jet25_bjptratio",1);
       readtree->SetBranchStatus("FakeLep_corrpt",1);
       readtree->SetBranchStatus("FakeLep_ismvasel",1);
       readtree->SetBranchStatus("FakeLep_charge",1);
       readtree->SetBranchStatus("FakeLep_mvaId",1);
       readtree->SetBranchStatus("FakeLep_minIso",1);
       readtree->SetBranchStatus("FakeLep_minIsoCh",1);
       readtree->SetBranchStatus("FakeLep_minIsoNeu",1);
       readtree->SetBranchStatus("FakeLep_ptratio",1);
       readtree->SetBranchStatus("FakeLep_ptrel",1);
       readtree->SetBranchStatus("FakeLep_sig3d",1);
       readtree->SetBranchStatus("FakeLep_segment",1);
       readtree->SetBranchStatus("FakeLep_lostHits",1);
       readtree->SetBranchStatus("FakeLep_relIso04",1);
       readtree->SetBranchStatus("FakeLep_relIsoRhoEA",1);
       readtree->SetBranchStatus("FakeLep_TightCharge",1);
       readtree->SetBranchStatus("FakeLep_passConv",1);
       readtree->SetBranchStatus("FakeLep_jetdr",1);
       readtree->SetBranchStatus("FakeLep_jetCSV",1);
       readtree->SetBranchStatus("FakeLep_dxyAbs",1);
       readtree->SetBranchStatus("FakeLep_dz",1);
       readtree->SetBranchStatus("FakeLep_leptonMVA",1);
       readtree->SetBranchStatus("FakeLep_jetNDauChargedMVASel",1);
       readtree->SetBranchStatus("FakeLep_isFromB",1);
       readtree->SetBranchStatus("FakeLep_isFromC",1);
       readtree->SetBranchStatus("FakeLep_isFromH",1);
       readtree->SetBranchStatus("FakeLep_isFromTop",1);
       readtree->SetBranchStatus("FakeLep_matchId",1);
       readtree->SetBranchStatus("FakeLep_PdgId",1);
       readtree->SetBranchStatus("FakeLep_matchIndex",1);
       readtree->SetBranchStatus("FakeLep_pt",1);
       readtree->SetBranchStatus("FakeLep_eta",1);
       readtree->SetBranchStatus("FakeLep_phi",1);
       readtree->SetBranchStatus("FakeLep_energy",1);
   */
   //}
   readtree->SetBranchStatus("EventWeight",1);
   readtree->SetBranchStatus("EVENT_genWeight",1);
   //readtree->SetBranchStatus("EVENT_genWeights",1);
   readtree->SetBranchStatus("bWeight",1);
   readtree->SetBranchStatus("puWeight",1);
   readtree->SetBranchStatus("lepSF",1);
   readtree->SetBranchStatus("ChargeMis",1);
   readtree->SetBranchStatus("FakeRate",1);
   readtree->SetBranchStatus("TriggerSF",1);
   readtree->SetBranchStatus("puWeight_SysUp",1);
   readtree->SetBranchStatus("lepSF_SysUp",1);
   readtree->SetBranchStatus("ChargeMis_SysUp",1);
   //readtree->SetBranchStatus("FakeRate_SysUp",1);
   readtree->SetBranchStatus("TriggerSF_SysUp",1);
   readtree->SetBranchStatus("puWeight_SysDown",1);
   readtree->SetBranchStatus("lepSF_SysDown",1);
   readtree->SetBranchStatus("ChargeMis_SysDown",1);
   //readtree->SetBranchStatus("FakeRate_SysDown",1);
   readtree->SetBranchStatus("TriggerSF_SysDown",1);
   readtree->SetBranchStatus("bWeight_central",1);
   readtree->SetBranchStatus("bWeight_up_jes",1);
   readtree->SetBranchStatus("bWeight_up_lf",1);
   readtree->SetBranchStatus("bWeight_up_hf",1);
   readtree->SetBranchStatus("bWeight_up_hfstats1",1);
   readtree->SetBranchStatus("bWeight_up_hfstats2",1);
   readtree->SetBranchStatus("bWeight_up_lfstats1",1);
   readtree->SetBranchStatus("bWeight_up_lfstats2",1);
   readtree->SetBranchStatus("bWeight_up_cferr1",1);
   readtree->SetBranchStatus("bWeight_up_cferr2",1);
   readtree->SetBranchStatus("bWeight_down_jes",1);
   readtree->SetBranchStatus("bWeight_down_lf",1);
   readtree->SetBranchStatus("bWeight_down_hf",1);
   readtree->SetBranchStatus("bWeight_down_hfstats1",1);
   readtree->SetBranchStatus("bWeight_down_hfstats2",1);
   readtree->SetBranchStatus("bWeight_down_lfstats1",1);
   readtree->SetBranchStatus("bWeight_down_lfstats2",1);
   readtree->SetBranchStatus("bWeight_down_cferr1",1);
   readtree->SetBranchStatus("bWeight_down_cferr2",1);
   readtree->SetBranchStatus("TTHLep_3L",1);
   readtree->SetBranchStatus("Trig_1Ele",1);
   readtree->SetBranchStatus("Trig_2Ele",1);
   readtree->SetBranchStatus("Trig_3Ele",1);
   readtree->SetBranchStatus("Trig_1Mu",1);
   readtree->SetBranchStatus("Trig_1Mu1Ele",1);
   readtree->SetBranchStatus("Trig_1Mu2Ele",1);
   readtree->SetBranchStatus("Trig_2Mu",1);
   readtree->SetBranchStatus("Trig_2Mu1Ele",1);
   readtree->SetBranchStatus("Trig_3Mu",1);
   readtree->SetBranchStatus("Dilep_worseIso",1);
   readtree->SetBranchStatus("Dilep_worseSip",1);
   readtree->SetBranchStatus("mass3L",1);
   readtree->SetBranchStatus("Trilep_mtWmin",1);
   readtree->SetBranchStatus("SubCat3L",1);
   readtree->SetBranchStatus("Sum3LCharge",1);
   readtree->SetBranchStatus("Trilep_n_mu",1);
   readtree->SetBranchStatus("Trilep_nTight",1);
   readtree->SetBranchStatus("Trilep_n_ele",1);
   readtree->SetBranchStatus("Trilep_bestMVA",1);
   readtree->SetBranchStatus("Trilep_worseIso",1);
   readtree->SetBranchStatus("Trilep_worseMVA",1);
   readtree->SetBranchStatus("Trilep_worseSip",1);
   readtree->SetBranchStatus("Dilep_worsedz",1);
   readtree->SetBranchStatus("thirdLep_isMatchRightCharge",1);
   readtree->SetBranchStatus("thirdLep_mcMatchId",1);
   readtree->SetBranchStatus("thirdLep_isFromTop",1);
   readtree->SetBranchStatus("thirdLep_isFromH",1);
   readtree->SetBranchStatus("thirdLep_isFromB",1);
   readtree->SetBranchStatus("thirdLep_isFromC",1);
   readtree->SetBranchStatus("thirdLep_mcPromptGamma",1);
   readtree->SetBranchStatus("thirdLep_mcPromptFS",1);
   readtree->SetBranchStatus("lep3_BDT",1);
   readtree->SetBranchStatus("lep1_charge",1);
   readtree->SetBranchStatus("lep1_dxy",1);
   readtree->SetBranchStatus("lep1_dz",1);
   readtree->SetBranchStatus("lep1_mvaId",1);
   readtree->SetBranchStatus("lep1_eta",1);
   readtree->SetBranchStatus("lep1_minIso",1);
   readtree->SetBranchStatus("lep1_minIsoCh",1);
   readtree->SetBranchStatus("lep1_minIsoNeu",1);
   readtree->SetBranchStatus("lep1_pdgId",1);
   readtree->SetBranchStatus("lep1_pt",1);
   readtree->SetBranchStatus("lep1_phi",1);
   readtree->SetBranchStatus("lep1_ptratio",1);
   readtree->SetBranchStatus("lep1_ptrel",1);
   readtree->SetBranchStatus("lep1_segment",1);
   readtree->SetBranchStatus("lep1_sig3d",1);
   readtree->SetBranchStatus("lep1_lostHits",1);
   readtree->SetBranchStatus("lep1_relIso04",1);
   readtree->SetBranchStatus("lep1_relIso03",1);
   readtree->SetBranchStatus("lep1_TightCharge",1);
   readtree->SetBranchStatus("lep1_passConv",1);
   readtree->SetBranchStatus("lep2_charge",1);
   readtree->SetBranchStatus("lep2_dxy",1);
   readtree->SetBranchStatus("lep2_dz",1);
   readtree->SetBranchStatus("lep2_mvaId",1);
   readtree->SetBranchStatus("lep2_eta",1);
   readtree->SetBranchStatus("lep2_minIso",1);
   readtree->SetBranchStatus("lep2_minIsoCh",1);
   readtree->SetBranchStatus("lep2_minIsoNeu",1);
   readtree->SetBranchStatus("lep2_pdgId",1);
   readtree->SetBranchStatus("lep2_pt",1);
   readtree->SetBranchStatus("lep2_phi",1);
   readtree->SetBranchStatus("lep2_ptratio",1);
   readtree->SetBranchStatus("lep2_ptrel",1);
   readtree->SetBranchStatus("lep2_segment",1);
   readtree->SetBranchStatus("lep2_sig3d",1);
   readtree->SetBranchStatus("lep2_lostHits",1);
   readtree->SetBranchStatus("lep2_relIso04",1);
   readtree->SetBranchStatus("lep2_relIso03",1);
   readtree->SetBranchStatus("lep2_TightCharge",1);
   readtree->SetBranchStatus("lep2_passConv",1);
   readtree->SetBranchStatus("lep3_charge",1);
   readtree->SetBranchStatus("lep3_dxy",1);
   readtree->SetBranchStatus("lep3_dz",1);
   readtree->SetBranchStatus("lep3_mvaId",1);
   readtree->SetBranchStatus("lep3_eta",1);
   readtree->SetBranchStatus("lep3_minIso",1);
   readtree->SetBranchStatus("lep3_minIsoCh",1);
   readtree->SetBranchStatus("lep3_minIsoNeu",1);
   readtree->SetBranchStatus("lep3_pdgId",1);
   readtree->SetBranchStatus("lep3_pt",1);
   readtree->SetBranchStatus("lep3_phi",1);
   readtree->SetBranchStatus("lep3_ptratio",1);
   readtree->SetBranchStatus("lep3_ptrel",1);
   readtree->SetBranchStatus("lep3_segment",1);
   readtree->SetBranchStatus("lep3_sig3d",1);
   readtree->SetBranchStatus("lep3_lostHits",1);
   readtree->SetBranchStatus("lep3_relIso04",1);
   readtree->SetBranchStatus("lep3_relIso03",1);
   readtree->SetBranchStatus("lep3_TightCharge",1);
   readtree->SetBranchStatus("lep3_passConv",1);
   readtree->SetBranchStatus("lep1_E",1);
   readtree->SetBranchStatus("lep1_isfakeablesel",1);
   readtree->SetBranchStatus("lep1_ismvasel",1);
   readtree->SetBranchStatus("lep2_E",1);
   readtree->SetBranchStatus("lep2_isfakeablesel",1);
   readtree->SetBranchStatus("lep2_ismvasel",1);
   readtree->SetBranchStatus("lep3_E",1);
   readtree->SetBranchStatus("lep3_isfakeablesel",1);
   readtree->SetBranchStatus("lep3_ismvasel",1);
   readtree->SetBranchStatus("genWeight_muF2",1);
   readtree->SetBranchStatus("genWeight_muF0p5",1);
   readtree->SetBranchStatus("genWeight_muR2",1);
   readtree->SetBranchStatus("genWeight_muR0p5",1);
   readtree->SetBranchStatus("elelooseSF_SysUp",1);
   readtree->SetBranchStatus("elelooseSF",1);
   readtree->SetBranchStatus("elelooseSF_SysDown",1);
   readtree->SetBranchStatus("eletightSF_SysUp",1);
   readtree->SetBranchStatus("eletightSF",1);
   readtree->SetBranchStatus("eletightSF_SysDown",1);
   readtree->SetBranchStatus("mulooseSF_SysUp",1);
   readtree->SetBranchStatus("mulooseSF",1);
   readtree->SetBranchStatus("mulooseSF_SysDown",1);
   readtree->SetBranchStatus("mutightSF_SysUp",1);
   readtree->SetBranchStatus("mutightSF",1);
   readtree->SetBranchStatus("mutightSF_SysDown",1);
   readtree->SetBranchStatus("FakeRate_m_central",1);
   readtree->SetBranchStatus("FakeRate_m_up",1);
   readtree->SetBranchStatus("FakeRate_m_down",1);
   readtree->SetBranchStatus("FakeRate_m_pt1",1);
   readtree->SetBranchStatus("FakeRate_m_pt2",1);
   readtree->SetBranchStatus("FakeRate_m_be1",1);
   readtree->SetBranchStatus("FakeRate_m_be2",1);
   readtree->SetBranchStatus("FakeRate_m_QCD",1);
   readtree->SetBranchStatus("FakeRate_m_TT",1);
   readtree->SetBranchStatus("FakeRate_e_central",1);
   readtree->SetBranchStatus("FakeRate_e_up",1);
   readtree->SetBranchStatus("FakeRate_e_down",1);
   readtree->SetBranchStatus("FakeRate_e_pt1",1);
   readtree->SetBranchStatus("FakeRate_e_pt2",1);
   readtree->SetBranchStatus("FakeRate_e_be1",1);
   readtree->SetBranchStatus("FakeRate_e_be2",1);
   readtree->SetBranchStatus("FakeRate_e_QCD",1);
   readtree->SetBranchStatus("FakeRate_e_TT",1);
   // Hmass variables
   /*
   readtree->SetBranchStatus("Gen_pt",1);
   readtree->SetBranchStatus("Gen_eta",1);
   readtree->SetBranchStatus("Gen_phi",1);
   readtree->SetBranchStatus("Gen_energy",1);
   readtree->SetBranchStatus("Gen_pdg_id",1);
   readtree->SetBranchStatus("gen_lvTop_px",1);
   readtree->SetBranchStatus("gen_lvTop_py",1);
   readtree->SetBranchStatus("gen_lvTop_pz",1);
   readtree->SetBranchStatus("gen_lvTop_E",1);
   readtree->SetBranchStatus("gen_lvTop_Index",1);
   readtree->SetBranchStatus("gen_lvH_px",1);
   readtree->SetBranchStatus("gen_lvH_py",1);
   readtree->SetBranchStatus("gen_lvH_pz",1);
   readtree->SetBranchStatus("gen_lvH_E",1);
   readtree->SetBranchStatus("gen_lvH_Index",1);
   readtree->SetBranchStatus("gen_miss_px",1);
   readtree->SetBranchStatus("gen_miss_py",1);
   readtree->SetBranchStatus("Met_Fake_px",1);
   readtree->SetBranchStatus("Met_Fake_py",1);
   readtree->SetBranchStatus("Met_missFake_px",1);
   readtree->SetBranchStatus("Met_missFake_py",1);
   readtree->SetBranchStatus("n_leptons_fromH",1);
   readtree->SetBranchStatus("n_leptons_fromTop",1);
   readtree->SetBranchStatus("n_leptons_fromB",1);
   readtree->SetBranchStatus("n_jets_fromH",1);
   readtree->SetBranchStatus("n_jets_fromTop",1);
   readtree->SetBranchStatus("jjl_fromH_lvH_mass",1);
   readtree->SetBranchStatus("genWs_fromH_mass",1);
   readtree->SetBranchStatus("genWs_fromTop_mass",1);
   readtree->SetBranchStatus("genZs_fromH_mass",1);
   readtree->SetBranchStatus("genTaus_fromH_mass",1);
   readtree->SetBranchStatus("genWs_fromH_pt",1);
   readtree->SetBranchStatus("genWs_fromTop_pt",1);
   readtree->SetBranchStatus("genZs_fromH_pt",1);
   readtree->SetBranchStatus("genTaus_fromH_pt",1);
   readtree->SetBranchStatus("genWs_fromH_eta",1);
   readtree->SetBranchStatus("genWs_fromTop_eta",1);
   readtree->SetBranchStatus("genZs_fromH_eta",1);
   readtree->SetBranchStatus("genTaus_fromH_eta",1);
   readtree->SetBranchStatus("genWs_fromH_phi",1);
   readtree->SetBranchStatus("genWs_fromTop_phi",1);
   readtree->SetBranchStatus("genZs_fromH_phi",1);
   readtree->SetBranchStatus("genTaus_fromH_phi",1);
   readtree->SetBranchStatus("genWs_fromH_index",1);
   readtree->SetBranchStatus("genWs_fromTop_index",1);
   readtree->SetBranchStatus("genZs_fromH_index",1);
   readtree->SetBranchStatus("genTaus_fromH_index",1);
   readtree->SetBranchStatus("Gen_type1PF_px",1);
   readtree->SetBranchStatus("Gen_type1PF_py",1);
    */
};
