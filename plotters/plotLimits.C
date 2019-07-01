/// \file
/// \ingroup tutorial_roofit
/// \notebook -js
/// \author 07/2008 - Wouter Verkerke 

#include "RooRealVar.h"
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
TString FileName = "LimitSummary_2019M5D1";
TString TreeName = "limit";
vector<TString> ErrorTypes = {"All","NoSyst","NoShape","NoStat","None"};
//vector<TString> ErrorTypes = {"All","NoSyst","NoShape"};
//vector<TString> ErrorTypes = {"All","NoStat"};
std::map<string,int> syst_color = {{"m2sig",4},{"m1sig",8},{"exp",1},{"p1sig",8},{"p2sig",4}};
std::map<string,int> syst_mark = {{"m2sig",23},{"m1sig",23},{"exp",8},{"p1sig",22},{"p2sig",22}};

string region = "DiLepRegion";
vector<TString> Versions = {"V0426_loose_newVar"};
//vector<TString> Versions = {"V0319_loose","V0405_loose_Preprocess","V0403_loose_newVar","V0403_loose_PreProcess"};
//vector<TString> Versions = {"V0321_loose","V0321_loose_regBin3","V0321_loose_regBin5"};
//string region = "2lss";
//vector<TString> Versions = {"V0321_loose_regBin5","V0321_loose","V0321_loose_regBin10","V0321_loose_regBin15"};
//vector<TString> CatNames = {"DNNCat","DNNCat_option2","DNNSubCat1_option1","DNNSubCat1_option2","DNNSubCat2_option1","DNNSubCat2_option2"};
vector<TString> CatNames = {"DNNCat","DNNSubCat1_option1","DNNSubCat2_option1"};
//vector<TString> CatNames = {"DNNCat","DNNCat_option2","DNNCat_option3","DNNSubCat1_option1","DNNSubCat1_option2","DNNSubCat1_option3","DNNSubCat2_option1","DNNSubCat2_option2","DNNSubCat2_option3"};
std::map<string,string> Version_TR = {{"V0307.2.1_fakeable","TR1"},{"V0319_loose","TR2"},{"V0321_loose","TR3"},{"V0321_loose_regBin","TR4"},{"V0402_loose_NTrainFake","TR5"},{"V0403_loose_PreProcess","TR6"},{"V0321_loose_regBin5","TR7"},{"V0321_loose_regBin10","TR8"},{"V0321_loose_regBin15","TR9"},{"V0403_loose_newVar","TR10"},{"V0321_loose_regBin1","TR11"},{"V0321_loose_regBin3","TR12"},{"V0405_loose_Preprocess","TR13"},{"V0409_loose_loose_newVars","OTNV"},{"V0409_newsel_loose_newVars","NTNV"},{"V0409_newsel_loose_StdScalar_newVars","NTNVP"},{"V0426_loose_newVar","OTNV"}};
std::map<string,string> CatName_OptCat = {{"DNNCat","Opt1CatA"},{"DNNCat_option2","Opt2CatA"},{"DNNCat_option3","Opt3CatA"},{"DNNSubCat1_option1","Opt1CatB"},{"DNNSubCat1_option2","Opt2CatB"},{"DNNSubCat1_option3","Opt3CatB"},{"DNNSubCat2_option1","Opt1CatC"},{"DNNSubCat2_option2","Opt2CatC"},{"DNNSubCat2_option3","Opt3CatC"}};



void plotLimits()
{
    TFile* f = new TFile(inputBaseDir+FileName+".root");
    // loop over errorType
    for(auto ErrorType: ErrorTypes){
        TString treeName =TreeName+ "_"+ErrorType;
        std::cout<< treeName<<std::endl;
        TTree* readTree = (TTree*) f->Get(treeName);
        double limit_m2sig = -1.;
        double limit_m1sig = -1.;
        double limit_exp = -1.;
        double limit_p1sig = -1.;
        double limit_p2sig = -1.;
        TString* label=0;
        readTree->SetBranchAddress("limit_m2sig",&limit_m2sig);
        readTree->SetBranchAddress("limit_m1sig",&limit_m1sig);
        readTree->SetBranchAddress("limit_exp",&limit_exp);
        readTree->SetBranchAddress("limit_p1sig",&limit_p1sig);
        readTree->SetBranchAddress("limit_p2sig",&limit_p2sig);
        readTree->SetBranchAddress("label",&label);
        int nentries = readTree->GetEntries();
        std::vector<double> limit_m2sig_vec,limit_m1sig_vec, limit_exp_vec, limit_p1sig_vec, limit_p2sig_vec;
        std::vector<TString> label_vec;
        std::vector<TString> new_label_vec;
        std::vector<double> limit_2DBDT;
        //loop over entries
        for (Long64_t i=0;i<nentries; i++) {
            limit_m2sig = -1.;
            limit_m1sig = -1.;
            limit_exp = -1.;
            limit_p1sig = -1.;
            limit_p2sig = -1.;
            //label = "";
            readTree->GetEntry(i);
            if(label->Contains(Versions[0]+"_SubCat2l_"+region) && limit_2DBDT.size()==0){
                limit_2DBDT.push_back(limit_m2sig);
                limit_2DBDT.push_back(limit_m1sig);
                limit_2DBDT.push_back(limit_exp);
                limit_2DBDT.push_back(limit_p1sig);
                limit_2DBDT.push_back(limit_p2sig);
            }
            Bool_t toSave = false;
            string labelName = "";
            for(auto Version : Versions){
                for(auto CatName: CatNames){
                    if(label->Contains(Version+"_"+CatName+"_"+region)){
                        toSave = true;
                        labelName = Version_TR.at(Version.Data())+CatName_OptCat.at(CatName.Data());
                        break;
                    }
                }
                if(toSave) break;
            }
            if(toSave){
                limit_m2sig_vec.push_back(limit_m2sig);
                limit_m1sig_vec.push_back(limit_m1sig);
                limit_exp_vec.push_back(limit_exp);
                limit_p1sig_vec.push_back(limit_p1sig);
                limit_p2sig_vec.push_back(limit_p2sig);
                label_vec.push_back(*label);
                new_label_vec.push_back(labelName);
            }
        }
        //end loop over entries
        // prepare canvas and legend
        TCanvas* c1 = new TCanvas(treeName,treeName,200,200,800,600);
        //gStyle->SetOptTitle(0);
        c1->SetBottomMargin(0.15);
        c1->SetGridy();
        c1->SetGridx();
        c1->SetLogy();
        TLegend *leg_DNN = new TLegend(0.8, 0.8, 1, 1);
        leg_DNN->SetHeader("limit_band");
        leg_DNN->SetNColumns(2);
        leg_DNN->SetBorderSize(0);
        leg_DNN->SetTextSize(0.02);
        // prepare arrays
        int Bin = label_vec.size();
        double* X = new double[Bin];
        double* Y_m2sig = new double[Bin];
        double* Y_m1sig = new double[Bin];
        double* Y_exp = new double[Bin];
        double* Y_p1sig = new double[Bin];
        double* Y_p2sig = new double[Bin];
        std::cout<<"m2sig     m1sig     expec     p1sig     p2sig  xlabel     label "<<std::endl;
        std::cout<<limit_2DBDT.at(0)<<"  "<<  limit_2DBDT.at(1)<<"  "<<limit_2DBDT.at(2)<<"  "<< limit_2DBDT.at(3)<<"  "<<limit_2DBDT.at(4)<<"   nan          2DBDT"<<std::endl;
        for(int i=0; i< label_vec.size(); i++){
            X[i]=i+1;
            Y_m2sig[i]= limit_m2sig_vec.at(i);
            Y_m1sig[i]= limit_m1sig_vec.at(i);
            Y_exp[i]= limit_exp_vec.at(i);
            Y_p1sig[i]= limit_p1sig_vec.at(i);
            Y_p2sig[i]= limit_p2sig_vec.at(i);
            std::cout<<limit_m2sig_vec.at(i)<<"  "<<  limit_m1sig_vec.at(i)<<"  "<<limit_exp_vec.at(i)<<"  "<< limit_p1sig_vec.at(i)<<"  "<<limit_p2sig_vec.at(i)<<"  "<<new_label_vec.at(i)<<" "<<label_vec.at(i)<<std::endl;
        }
        // prepare Graphs
        TGraph* gr_m2sig = new TGraph(Bin, X, Y_m2sig);
        gr_m2sig->SetTitle(treeName);
        gr_m2sig->SetMaximum(3);
        gr_m2sig->SetMinimum(limit_2DBDT.at(0)*0.9);
        //gr_m2sig->GetXaxis()->SetTitle("TR_Opt_Cat");
        gr_m2sig->GetYaxis()->SetTitle("ExpLimit");
        gr_m2sig->SetMarkerColor(syst_color.at("m2sig"));
        gr_m2sig->SetFillColor(syst_color.at("m2sig"));
        gr_m2sig->SetLineColor(syst_color.at("m2sig"));
        gr_m2sig->SetMarkerStyle(syst_mark.at("m2sig"));
        
        TGraph* gr_m1sig = new TGraph(Bin, X, Y_m1sig);
        gr_m1sig->SetMarkerColor(syst_color.at("m1sig"));
        gr_m1sig->SetFillColor(syst_color.at("m1sig"));
        gr_m1sig->SetLineColor(syst_color.at("m1sig"));
        gr_m1sig->SetMarkerStyle(syst_mark.at("m1sig"));
        
        TGraph* gr_exp = new TGraph(Bin, X, Y_exp);
        gr_exp->SetMarkerColor(syst_color.at("exp"));
        gr_exp->SetFillColor(syst_color.at("exp"));
        gr_exp->SetLineColor(syst_color.at("exp"));
        gr_exp->SetMarkerStyle(syst_mark.at("exp"));
        
        TGraph* gr_p1sig = new TGraph(Bin, X, Y_p1sig);
        gr_p1sig->SetMarkerColor(syst_color.at("p1sig"));
        gr_p1sig->SetFillColor(syst_color.at("p1sig"));
        gr_p1sig->SetLineColor(syst_color.at("p1sig"));
        gr_p1sig->SetMarkerStyle(syst_mark.at("p1sig"));
        
        TGraph* gr_p2sig = new TGraph(Bin, X, Y_p2sig);
        gr_p2sig->SetMarkerColor(syst_color.at("p2sig"));
        gr_p2sig->SetFillColor(syst_color.at("p2sig"));
        gr_p2sig->SetLineColor(syst_color.at("p2sig"));
        gr_p2sig->SetMarkerStyle(syst_mark.at("p2sig"));
   
        // prepare lines
        int xlow = gr_m2sig->GetXaxis()->GetFirst();
        TLine* l_m2sig = new TLine(xlow, limit_2DBDT.at(0), Bin, limit_2DBDT.at(0)); 
        l_m2sig->SetLineColor(syst_color.at("m2sig"));
        l_m2sig->SetLineStyle(2);
        
        TLine* l_m1sig = new TLine(xlow, limit_2DBDT.at(1), Bin, limit_2DBDT.at(1)); 
        l_m1sig->SetLineColor(syst_color.at("m1sig"));
        l_m1sig->SetLineStyle(2);
        
        TLine* l_exp = new TLine(xlow, limit_2DBDT.at(2), Bin, limit_2DBDT.at(2)); 
        l_exp->SetLineColor(syst_color.at("exp"));
        l_exp->SetLineStyle(1);
        
        TLine* l_p1sig = new TLine(xlow, limit_2DBDT.at(3), Bin, limit_2DBDT.at(3)); 
        l_p1sig->SetLineColor(syst_color.at("p1sig"));
        l_p1sig->SetLineStyle(2);
        
        TLine* l_p2sig = new TLine(xlow, limit_2DBDT.at(4), Bin, limit_2DBDT.at(4)); 
        l_p2sig->SetLineColor(syst_color.at("p2sig"));
        l_p2sig->SetLineStyle(2);
        
        
        leg_DNN->AddEntry(gr_p2sig,"+2sig","P");
        leg_DNN->AddEntry(l_p2sig,"+2sig BDT","L");
        leg_DNN->AddEntry(gr_p1sig,"+1sig","P");
        leg_DNN->AddEntry(l_p1sig,"+1sig BDT","L");
        leg_DNN->AddEntry(gr_exp,"central","P");
        leg_DNN->AddEntry(l_exp,"central BDT","L");
        leg_DNN->AddEntry(gr_m1sig,"-1sig","P");
        leg_DNN->AddEntry(l_m1sig,"-1sig BDT","L");
        leg_DNN->AddEntry(gr_m2sig,"-2sig","P");
        leg_DNN->AddEntry(l_m2sig,"-2sig BDT","L");
        // make plots

        c1->cd();
        gr_m2sig->Draw("AP");
        
        // set bin label
        for(int i=0; i< label_vec.size(); i++){
            int bin_index = gr_m2sig->GetXaxis()->FindBin(X[i]);
            gr_m2sig->GetXaxis()->SetLabelSize(0.03);
            gr_m2sig->GetXaxis()->SetBinLabel(bin_index,new_label_vec.at(i));
        }
        
        gr_m1sig->Draw("Psame");
        gr_exp->Draw("Psame");
        gr_p1sig->Draw("Psame");
        gr_p2sig->Draw("Psame");
        l_m2sig->Draw("same");
        l_m2sig->Draw("same");
        l_m1sig->Draw("same");
        l_exp->Draw("same");
        l_p1sig->Draw("same");
        l_p2sig->Draw("same");
        leg_DNN->Draw("same");
        
        TString plotName =  treeName+"_"+region+"_"+FileName;
        c1->SaveAs(plotName+".png");
        //c1->SaveAs(plotName+".pdf");
    
    }// end loop over errorType
}
