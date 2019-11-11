/// \file
/// \ingroup tutorial_roofit
/// \notebook -js
///
///
#include <ctime>
#include "RooDataSet.h"
#include "RooDataHist.h"
#include "RooGaussian.h"
#include "RooConstVar.h"
#include "RooFormulaVar.h"
#include "RooGenericPdf.h"
#include "RooPolynomial.h"
#include "RooChi2Var.h"
#include "RooMinimizer.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "RooPlot.h"
#include "RooFitResult.h"
using namespace RooFit ;


TString inputBaseDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/CombineStuff/CMSSW_8_1_0/src/HiggsAnalysis/";
TString TreeName = "limit";
TString FileName = "higgsCombineTest.AsymptoticLimits.mH125.root";

/*
TString Version = "V0319_loose";
TString CatName = "SubCat2l";
TString POI = "Bin2l";
TString ErrorType = "All";
*/

vector<TString> Versions = {"V0426_loose_newVar"};
//vector<TString> Versions = {"V0321_loose","V0321_loose_regBin1","V0321_loose_regBin3","V0321_loose_regBin5"};
//vector<TString> Versions = {"V0321_loose","V0321_loose_regBin3","V0321_loose_regBin5"};
//vector<TString> Versions = {"V0321.1_loose_AMSBin"};
//vector<TString> CatNames = {"SubCat2l","DNNCat","DNNCat_option2","DNNCat_option3","DNNAMS2Cat1_option1","DNNAMS2Cat1_option2","DNNAMS2Cat1_option3","DNNAMS3Cat1_option1","DNNAMS3Cat1_option2","DNNAMS3Cat1_option3"};
//vector<TString> CatNames = {"SubCat2l","DNNCat","DNNCat_option2","DNNCat_option3","DNNSubCat1_option1","DNNSubCat1_option2","DNNSubCat1_option3","DNNSubCat2_option1","DNNSubCat2_option2","DNNSubCat2_option3"};
vector<TString> CatNames = {"SubCat2l","DNNCat","DNNSubCat1_option1","DNNSubCat2_option1"};
vector<TString> ErrorTypes = {"All","NoSyst","NoShape","NoStat","None"};
//vector<TString> ErrorTypes = {"All","NoSyst","NoShape"};
//vector<TString> ErrorTypes = {"All"};
std::map<string,string> CatName_POI = {{"SubCat2l","Bin2l"},{"DNNCat","DNN_maxval"},{"DNNCat_option2","DNN_maxval_option2"},{"DNNCat_option3","DNN_maxval_option3"},{"DNNSubCat1_option1","DNN_maxval"},{"DNNSubCat1_option2","DNN_maxval_option2"},{"DNNSubCat1_option3","DNN_maxval_option3"},{"DNNSubCat2_option1","DNN_maxval"},{"DNNSubCat2_option2","DNN_maxval_option2"},{"DNNSubCat2_option3","DNN_maxval_option3"},{"DNNAMS2Cat1_option1","DNN_maxval"},{"DNNAMS2Cat1_option2","DNN_maxval_option2"},{"DNNAMS2Cat1_option3","DNN_maxval_option3"},{"DNNAMS3Cat1_option1","DNN_maxval"},{"DNNAMS3Cat1_option2","DNN_maxval_option2"},{"DNNAMS3Cat1_option3","DNN_maxval_option3"}};
std::map<string,string> Version_Region = {{"V0307.2.1_fakeable","2lss_ttWctrl"},{"V0319_loose","2lss_ttWctrl"},{"V0321_loose","2lss_ttWctrl"},{"V0321_loose_regBin","2lss"},{"V0321_loose_AMSBin","2lss_ttWctrl"},{"V0402_loose_NTrainFake","2lss_ttWctrl"},{"V0403_loose_PreProcess","2lss_ttWctrl"},{"V0321_loose_regBin5","2lss_ttWctrl"},{"V0321_loose_regBin10","2lss_ttWctrl"},{"V0321_loose_regBin15","2lss_ttWctrl"},{"V0403_loose_newVar","2lss_ttWctrl"},{"V0321_loose_regBin1","2lss_ttWctrl"},{"V0321_loose_regBin3","2lss_ttWctrl"},{"V0405_loose_Preprocess","2lss_ttWctrl"},{"V0409_loose_loose_newVars","2lss_ttWctrl"},{"V0409_newsel_loose_newVars","2lss_ttWctrl"},{"V0409_newsel_loose_StdScalar_newVars","2lss_ttWctrl"},{"V0426_loose_newVar","DiLepRegion"}};

void readlimit()
{
    // current date/time 
    time_t now = time(0);
    
    tm* ltm = localtime(&now);
    
    //create newTree
    TString newFileName = inputBaseDir +"LimitSummary_"+to_string(1900+ltm->tm_year)+"M"+to_string(1+ltm->tm_mon)+"D"+to_string(ltm->tm_mday)+".root";
    TFile* newFile = new TFile(newFileName,"reCreate");
    
    // loop over errorType
    for(auto ErrorType : ErrorTypes){
        TString newTreeName = "limit_"+ErrorType;
        TTree* newTree = new TTree(newTreeName, newTreeName);
        double limit_m2sig;
        double limit_m1sig;
        double limit_exp;
        double limit_p1sig;
        double limit_p2sig;
        double limit_obs;
        TString label;
        newTree->Branch("limit_m2sig",&limit_m2sig);
        newTree->Branch("limit_m1sig",&limit_m1sig);
        newTree->Branch("limit_exp",&limit_exp);
        newTree->Branch("limit_p1sig",&limit_p1sig);
        newTree->Branch("limit_p2sig",&limit_p2sig);
        newTree->Branch("limit_obs",&limit_obs);
        newTree->Branch("label",&label);
        
        // loop over Version
        for(auto Version : Versions){
            // loop over CatName
            for(auto CatName : CatNames){
                // read input file
                TString POI = CatName_POI[CatName.Data()];
                TString oldFileName = inputBaseDir + "/"+Version+"/"+Version+"_datacards_"+ErrorType+"/"+CatName+"/"+POI+"/"+FileName;
                TFile* f = new TFile(oldFileName);
                TTree* limitTree = (TTree*) f->Get(TreeName);
                double limit = -1.;
                limitTree->SetBranchAddress("limit",&limit);
            
                //Fill new branches
                int nentries = limitTree->GetEntries();
                for (Long64_t i=0;i<nentries; i++) {
                    limit = -1;
                    limitTree->GetEntry(i);
                    if(i==0){
                        limit_m2sig = limit;
                        TString Region = Version_Region[Version.Data()];
                        TString TR_Opt_Cat = Version+"_"+CatName+"_"+Region;
                        label = TR_Opt_Cat;
                        std::cout<< " save " << oldFileName << std::endl;
                    }
                    else if(i==1)limit_m1sig = limit;
                    else if(i==2)limit_exp = limit;
                    else if(i==3)limit_p1sig = limit;
                    else if(i==4)limit_p2sig = limit;
                    else if(i==5)limit_obs = limit;
                    else{
                        std::cout << " limit Tree Error " << std::endl;
                    }
                }
                newTree->Fill();
            }// end loop over CatName
        }// end loop over Version
        newFile->cd();
        newTree->Write();
    }// end loop over ErrorType
}
