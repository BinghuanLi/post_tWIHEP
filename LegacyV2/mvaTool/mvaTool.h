#ifndef mvaTool_h
#define mvaTool_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TH2F.h>
#include <TH2.h>
#include <TH1F.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TFile.h>
#include <TString.h>

#include <TLorentzVector.h>

#include <iostream>

#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
#include <cmath>
#include <tuple>

#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TThread.h"

//#include "TMVAGui.C"

#include "TMVA/Factory.h"
//#include "TMVA/DataLoader.h"
#include "TMVA/Reader.h"
#include "TMVA/Tools.h"


class mvaTool {
 public :
  mvaTool(TString RegName="SigRegion", TString BinDir="/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/varJobs/BinData/" , Int_t nPerBin=5 ,Int_t channel = 0, TString Category ="SubCat2l", TString TreeName="syncTree", std::map<Int_t,TString> channelNameMap={{0,"inclusive"},{1,"ee_neg"},{2,"ee_pos"},{3,"em_bl_neg"},{4,"em_bl_pos"},{5,"em_bt_neg"},{6,"em_bt_pos"},{7,"mm_bl_neg"},{8,"mm_bl_pos"},{9,"mm_bt_neg"},{10,"mm_bt_pos"}},  std::map<TString, int> IDOfReWeight={{"kt_1_kv_1",12},{"cosa_mp0",60}}, TString inputbaseDir = "", int dataEra=2018, TString varName="", std::map<TString, Int_t> DNNBinMap={{"ee_ttHnode",3},{"ee_Restnode",1},{"ee_ttWnode",8},{"ee_tHQnode",1},{"em_ttHnode",5},{"em_Restnode",15},{"em_ttWnode",18},{"em_tHQnode",6},{"mm_ttHnode",6},{"mm_Restnode",14},{"mm_ttWnode",13},{"mm_tHQnode",5}});
  //  ~mvaTool();

  //void doBothTraining(TString inDir);
  //void doTraining(TString inDir, bool isttbar);
  void doReading(TString sampleName, TString inDir = "tW",TString outDir = "mvaOutput/", bool isData = false);
  void doReadingNoMVA(TString sampleName, TString inDir = "tW",TString outDir = "mvaOutput/", bool isData = false);

  void setChannel(Int_t channel){_channel = channel;};
  //  void doReading();

 private:

  Int_t _channel; //The channel we want to read
  Int_t _nPerBin; //nBin = N_mc / nPerBin
  Int_t _DataEra;
  TString _inputbaseDir;
  TString subCat2l;
  TString treeName;
  std::vector<TString> regionNames;
  std::map<Int_t,TString> ChannelNameMap;
  std::map<TString, int> _IDOfReWeight;
  std::map<TString, Int_t> _DNNBinMap;
  std::map<TString, TString> _systMap;
  std::map<TString, std::vector<double>> _rwgtRatios;
  TString _varName;
  TString BinDir;
  TString RegName;
  TFile* theBinFile;
  TFile* the2DBinFile;
  std::map<TString, std::map<TString, Int_t>> BinMap;
  /*
  std::map<Int_t,TString> ChannelNameMap = {
      {0,"inclusive"},
      {1,"ee_neg"},{2,"ee_pos"},
      {3,"em_bl_neg"},{4,"em_bl_pos"},{5,"em_bt_neg"},{6,"em_bt_pos"},
      {7,"mm_bl_neg"},{8,"mm_bl_pos"},{9,"mm_bt_neg"},{10,"mm_bt_pos"},
      };
  */
 
  //Used to loop over things
  void processMCSample(TString sampleName,TString inDir,TString outDir, float * treevars, bool isData, bool doMVA = true);
  void loopInSample(TString dirName, TString sampleName, float* treevars, bool isData, bool doMVA = true);
  void createHists(TString sampleName);
  std::vector<double> getBins(TFile* theBinFile, TString HistoName, float minN_total, float minN_sig, double& xmin, double& xmax);
  void fillHists(TString sampleName, float* treevars, double mvaValue, double mvawJets, double theweight, float met, float mtw, int theChannel);
  void saveHists(std::vector<TFile *> outFile);
  void setbTagVars(TChain* theTree); 

  void makeStatVariationHists(TString sampleName,std::vector<TFile*> outputFile);

  std::tuple<float,float> calculatebTagSyst(float,std::vector<float>);
  std::tuple<float,float> calculatebMistagSyst(float,std::vector<float>);
  std::tuple<float,float,float,float> calculateClosSyst(float Dilep_flav ,float e_shape_ee_Up, float e_shape_ee_Down, float e_shape_em_Up, float e_shape_em_Down, float m_shape_mm_Up, float m_shape_mm_Down, float m_shape_em_Up, float m_shape_em_Down);
  void calculateClosNormSyst(float Dilep_flav, int nbMedium,float& e_norm_up, float& e_norm_down, float& e_bt_norm_up, float& e_bt_norm_down, float& m_norm_up, float& m_norm_down, float& m_bt_norm_up, float& m_bt_norm_down);
  void calculateLepTightEffSyst(float Dilep_flav, float& eltight_up, float& eltight_down, float& mutight_up, float& mutight_down);
  std::tuple<float,float,float,float> get_muFmuR_factor(TString sampleName);

  std::map<TString,std::vector<std::vector<TH1F*> > > theHistoMap;
  std::map<TString,std::vector<std::vector<TH1F*> > > bdtHistoMap;
  std::map<TString,std::vector<TH2F*> > the2DHistoMap;
 

  std::vector<TString > varList;
  std::vector<TString > samplelist;
  std::vector<TString > systlist;
  TString baseName;
  std::vector<float> bTagSysts;

  TMVA::Reader *reader;

  std::vector<double>* EVENT_rWeights=0 ;
  std::vector<double>* EVENT_genWeights=0 ;
  
  double get_rwgt_ratio(TString sample, int index);
  // effective event ratio: sum[i]/sum[11] (sum[11] : SM)
  float theweight;
  float mvaValue;
  float mvawJetsValue;
  
};

#endif
