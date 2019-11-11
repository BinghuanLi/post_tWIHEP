// Input : rootplas with DNN maxval and DNN Cat Flag
// Function: copytrees and add channel flags, add BinOptimized Histograms
// Output : rootplas ready for statistics study and histograms for Optimized Binning 
#include "Maps.C"

std::vector<TString> samplesAll = {"Conv","TTW","TTZ","Fakes","FakeSub","Flips","TTH"};
double err_Fakes = 0.25;
double err_TTH = 0.12;
double err_Others = 0.15;
// SubCatNames should be mapped to VarNames 1 to 1
std::vector<TString> SubCatNames = {
    "DNNCat0","DNNCat1","DNNCat2","DNNCat3",
    "ee_DNNCat0","ee_DNNCat1","ee_DNNCat2","ee_DNNCat3",
    "em_DNNCat0","em_DNNCat1","em_DNNCat2","em_DNNCat3",
    "mm_DNNCat0","mm_DNNCat1","mm_DNNCat2","mm_DNNCat3",
    };
std::vector<int> minEvts = {5,10,15,20};
std::map<TString,TH2F*> the2DHistoMap;
std::map<TString,TH2F*> the2DBinMap;
std::map<TString,std::vector<TH1F*>> the1DHistoVecMap;// 0: significance pdf, 1: significance cdf 
std::map<TString,std::vector<TH2F*>> the2DHistoVecMap;// 0: sig, 1: bkg, 2: significance, >=3: significance map with different nbins
TString RegName;

void createHists();
void getHists(TFile* f_input, TFile* f_output, TString SampleName, TString SubCatName);
void fillHists(TString SubCatName, Bool_t SigDNN);
double get_effective_error(std::vector<double> bkgs, std::vector<double> errs, double& sumBkg, double threshold=0.000001);
void fillMaps(TString SubCatName, int minEvt);

void makeBins(TString InputDir, TString OutputDir, TString RegionName){
    TString BinRootFile = OutputDir +"/DNNBin_"+RegionName+".root";
    std::vector<TString> samples;
    TFile* newBinFile = new TFile(BinRootFile,"recreate");
    Bool_t sigDNN = true;

    for(auto s : samplesAll){
        TString Input = InputDir + "/" + s + "_" + RegionName + ".root";
        TString Output = OutputDir + "/" + s + "_" + RegionName + ".root";
        std::cout <<" input file is " << Input << std::endl;
        TFile *oldfile = new TFile(Input);
        if(oldfile->IsZombie()){
            std::cout << " Input deosn't exist " <<std::endl;
            continue; 
        }
        for(auto catname : SubCatNames){
            getHists(oldfile, newBinFile, s, catname);
        }
        
        std::cout << " loop over entries in sample "<< s <<std::endl;
        
        delete oldfile;    
    }
    
    createHists();
    
    for(auto subCatName: SubCatNames){
        fillHists(subCatName, sigDNN);
    }
    
    for(auto subCatName: SubCatNames){
        for(auto minEvt: minEvts){
            fillMaps(subCatName, minEvt);
        }
    }
    
    newBinFile->cd();
    
    for (auto histoMapElement: the1DHistoVecMap){
        for (auto hist:histoMapElement.second) hist->Write();
    }
    for (auto histoMap: the2DBinMap){
        histoMap.second->Write();
    }
    for (auto histoMapElement: the2DHistoVecMap){
        for (auto hist:histoMapElement.second) hist->Write();
    }
    
    delete newBinFile; 
    std::cout << " end of sample loop " <<std::endl;
    
}

void getHists(TFile* f_input, TFile* f_output, TString SampleName, TString SubCatName){
    TString histoName = "histo_"+SubCatName;
    TH2F* histo = (TH2F*) f_input->Get(histoName);
    TH2F* myhist = (TH2F*) histo->Clone((SampleName+"_"+histoName));
    myhist->SetDirectory(0);
    myhist->SetTitle((SampleName + "_" + histoName));
    the2DHistoMap[(SampleName + "_" + histoName)] = myhist;
    f_output->cd();
    myhist->Write();
};

double get_effective_error(std::vector<double> bkgs, std::vector<double> errs, double& sumBkg, double threshold=0.000001){
    double err = 0.;
    double sumW = 0.;
    sumW = std::accumulate(bkgs.begin(), bkgs.end(), 0.0);
    // calculate effective error only when a+b > threshold
    if (sumW > threshold){
        double sumVars = 0;
        for (int i =0; i < bkgs.size(); i++){
            sumVars += bkgs.at(i)*errs.at(i);
        }
        err = TMath::Sqrt(sumVars)/sumW;
    }
    sumBkg = sumW;
    return err;
};

void createHists(){
    for(auto SubCatName : SubCatNames){
        TString histoName = "histo_"+SubCatName;
        int nbinsX, nbinsY;
        double xmin, xmax, ymin, ymax;
        TH2F* temp_hist = (TH2F*) the2DHistoMap[("TTH_" + histoName)]->Clone(); 
       
        nbinsX = temp_hist->GetNbinsX();
        xmin = temp_hist->GetXaxis()->GetBinLowEdge(1);
        xmax = temp_hist->GetXaxis()->GetBinLowEdge(nbinsX+1);
        nbinsY = temp_hist->GetNbinsY();
        ymin = temp_hist->GetYaxis()->GetBinLowEdge(1);
        ymax = temp_hist->GetYaxis()->GetBinLowEdge(nbinsY+1);
        
        TH2F* histo_sig = new TH2F((SubCatName +"_Sig").Data(), (SubCatName + "_Sig").Data(),nbinsX,xmin,xmax, nbinsY, ymin, ymax);
        histo_sig->Sumw2();
        TH2F* histo_bkg = new TH2F((SubCatName +"_Bkg").Data(), (SubCatName + "_Bkg").Data(),nbinsX,xmin,xmax, nbinsY, ymin, ymax);
        histo_bkg->Sumw2();
        TH2F* histo_significance = new TH2F((SubCatName +"_significance").Data(), (SubCatName + "_significance").Data(),nbinsX,xmin,xmax, nbinsY, ymin, ymax);
        histo_significance->Sumw2();
        the2DHistoVecMap[SubCatName].push_back(histo_sig);
        the2DHistoVecMap[SubCatName].push_back(histo_bkg);
        the2DHistoVecMap[SubCatName].push_back(histo_significance);
        std::cout << (" the2DHistoVecMap key: "+SubCatName +" size ")<< the2DHistoVecMap[SubCatName].size() << std::endl; 
        for(auto minEvt : minEvts){
            TH2F* histo = new TH2F((SubCatName +"_Map_GT"+to_string(minEvt)).Data(), (SubCatName + "Map_GT"+to_string(minEvt)).Data(),nbinsX,xmin,xmax, nbinsY, ymin, ymax);
            histo->Sumw2();
            the2DBinMap[SubCatName+"_Map_GT"+to_string(minEvt)]=histo;
        }
        TH1F* histo_pdf_sig = new TH1F((SubCatName +"_pdf_significance").Data(), (SubCatName + "_pdf_significance").Data(), 100, 0, 5);
        histo_pdf_sig->Sumw2();
        TH1F* histo_cdf_sig = new TH1F((SubCatName +"_cdf_significance").Data(), (SubCatName + "_cdf_significance").Data(), 100, 0, 5);
        histo_cdf_sig->Sumw2();
        the1DHistoVecMap[SubCatName].push_back(histo_pdf_sig);
        the1DHistoVecMap[SubCatName].push_back(histo_cdf_sig);
    }
}

void fillHists(TString SubCatName, Bool_t SigDNN){
  std::vector<double> X_centers, Y_centers, significance;
  // I'm assuming TTH always exists in sample list
  TH2F* temp_hist = the2DHistoMap[("TTH_histo_" + SubCatName)];
  int nBinsX = temp_hist->GetNbinsX();
  int nBinsY = temp_hist->GetNbinsY();
  TH1F* my_hist =  the1DHistoVecMap[SubCatName].at(0);
  int nbin = my_hist->GetNbinsX();
  double xmin = my_hist->GetXaxis()->GetBinLowEdge(1);
  double xmax = my_hist->GetXaxis()->GetBinLowEdge(nbin+1);
  std::cout<< " SubCatName is " << SubCatName << std::endl;
  for(int i_x = 1; i_x < nBinsX+1; i_x++){// 0: underflow; n+1: overflow
    for(int i_y = 1; i_y < nBinsY+1; i_y++){// 0: underflow; n+1: overflow
       double x_center = temp_hist->GetXaxis()->GetBinCenter(i_x);
       double y_center = temp_hist->GetYaxis()->GetBinCenter(i_y);
       std::vector<double> bkgs;
       std::vector<double> errs;
       double signal=0.;
       double sumBkg = 0.;
       double error = 0.; 
       for(auto SampleName : samplesAll){
          if(SampleName.Contains("FakeSub"))continue;
          int isSig = -1;
          int wgt = 1;
          // get the nEvent
          double sumW = the2DHistoMap[(SampleName+"_histo_"+SubCatName)]->GetBinContent(i_x,i_y);
          if(SampleName.Contains("Fakes")){
            sumW -= the2DHistoMap[("FakeSub_histo_"+SubCatName)]->GetBinContent(i_x,i_y);
          }
          // get the Error
          double err = 0.;
          if(SampleName.Contains("Fakes"))err = err_Fakes;
          else if(SampleName.Contains("TTH"))err = err_TTH;
          else err = err_Others;
          // normal case of Sig Bkg
          if(SampleName.Contains("TTH"))isSig=1;
          else if(SampleName.Contains("TTW") || SampleName.Contains("TTZ") || SampleName.Contains("Fakes") || SampleName.Contains("FakeSub") || SampleName.Contains("Flip") || SampleName.Contains("Conv"))isSig=0;
          // Sig Bkg according to DNN
          if(SubCatName.Contains("DNNCat1") && SigDNN){// ttJ
            if(SampleName.Contains("Fakes") || SampleName.Contains("FakeSub") || SampleName.Contains("Flip") || SampleName.Contains("Conv"))isSig=1;
            else if(SampleName.Contains("TTW") || SampleName.Contains("TTZ") || SampleName.Contains("TTH"))isSig=0;
          }else if(SubCatName.Contains("DNNCat2") && SigDNN){// ttW
            if(SampleName.Contains("TTW"))isSig=1;
            else if(SampleName.Contains("TTH") || SampleName.Contains("TTZ") || SampleName.Contains("Fakes") || SampleName.Contains("FakeSub") || SampleName.Contains("Flip") || SampleName.Contains("Conv"))isSig=0;
          }else if(SubCatName.Contains("DNNCat3") && SigDNN){// ttZ
            if(SampleName.Contains("TTZ"))isSig=1;
            else if(SampleName.Contains("TTH") || SampleName.Contains("TTW") || SampleName.Contains("Fakes") || SampleName.Contains("FakeSub") || SampleName.Contains("Flip") || SampleName.Contains("Conv"))isSig=0;
          }
          if(the2DHistoVecMap[SubCatName].size() <3 ){
            std::cout<< " ERROR the 2DHistoVecMap key: "<< SubCatName <<" size : "<< the2DHistoVecMap[SubCatName].size() << std::endl;
            continue;
          }
          if(isSig==0){
              bkgs.push_back(sumW);
              errs.push_back(err);
              the2DHistoVecMap[SubCatName].at(1)->Fill(x_center,y_center,sumW);
          }else if(isSig==1){
              signal += sumW;
              the2DHistoVecMap[SubCatName].at(0)->Fill(x_center,y_center,sumW);
          }else{
            std::cout<< " WARNING isSig is -1 "<< SubCatName << std::endl;
          }
       }// end loop over samples
       error = get_effective_error(bkgs, errs, sumBkg);
       float App_sig =0.;
       if (signal > 0){
         App_sig = RooStats::AsimovSignificance(signal, sumBkg, error); 
       }
       int isNan_value =  TMath::IsNaN(App_sig);
       if(isNan_value==1 || isinf(App_sig)){
          App_sig = RooStats::AsimovSignificance(signal, 0.000001, error); 
          //std::cout << "found nan value and recalculate it x_center is " << x_center << " y_center is " << y_center << " signal is "<< signal << " bkg is " << sumBkg << " error is " << error <<" App_sig is " << App_sig <<std::endl;
       }
       significance.push_back(App_sig);
       X_centers.push_back(x_center);
       Y_centers.push_back(y_center);
       the2DHistoVecMap[SubCatName].at(2)->Fill(x_center,y_center,App_sig);
       if(App_sig < xmin){
        the1DHistoVecMap[SubCatName].at(0)->Fill(xmin+0.00001);
       }else if( App_sig > xmax){
        the1DHistoVecMap[SubCatName].at(0)->Fill(xmax-0.00001);
       }else{
        the1DHistoVecMap[SubCatName].at(0)->Fill(App_sig);
       }
    }
  }
  TH1F* h1 = the1DHistoVecMap[SubCatName].at(0);
  h1->Scale(1./h1->Integral());
  TH1F* h2 = (TH1F*) h1->GetCumulative();
  the1DHistoVecMap[SubCatName].at(1) = h2;
};

void fillMaps(TString SubCatName, int minEvt){
  int nbin = floor((the2DHistoVecMap[SubCatName].at(0)->Integral() + the2DHistoVecMap[SubCatName].at(1)->Integral())/minEvt);
  // get the significance edges from culmulative distributions
  TH1F* h1 = the1DHistoVecMap[SubCatName].at(1);
  double c_min = h1->GetMinimum();
  double c_step  = (1.-c_min)/max(1,min(nbin,100));
  std::vector<double> edges;
  double y_edge = c_min;
  edges.push_back(0.);
  for(int i=1;i<nbin; i++){
    y_edge += c_step;
    int binx = h1->FindFirstBinAbove(y_edge);
    double x_edge = h1->GetBinLowEdge(binx);
    edges.push_back(x_edge);
    if(y_edge > 1){
        std::cout<< " WARNING: y_edge > 1, it is weird " << std::endl;
        std::cout<< " SubCatName is  " << SubCatName << " nbin is " << nbin << std::endl;
    }
  }
  // sort and remove duplicated
  sort( edges.begin(), edges.end() );
  edges.erase( unique( edges.begin(), edges.end() ), edges.end() );
  // now fill the map
  TH2F* temp_hist = the2DHistoVecMap[SubCatName].at(2);
  for (auto histoMap: the2DBinMap){
      if(histoMap.first!=(SubCatName+"_Map_GT"+to_string(minEvt)))continue;
      // loop over 2D hist
      int nBinsX = temp_hist->GetNbinsX();
      int nBinsY = temp_hist->GetNbinsY();
      for(int i_x = 1; i_x < nBinsX+1; i_x++){// 0: underflow; n+1: overflow
       for(int i_y = 1; i_y < nBinsY+1; i_y++){// 0: underflow; n+1: overflow
        double x_center = temp_hist->GetXaxis()->GetBinCenter(i_x);
        double y_center = temp_hist->GetYaxis()->GetBinCenter(i_y);
        double sig_value = temp_hist->GetBinContent(i_x,i_y) ;
        auto it =lower_bound(edges.begin(),edges.end(),sig_value);
        int BIN = it - edges.begin();
        histoMap.second->Fill(x_center,y_center,BIN);       
       }
      }
      break;
  }
  
}
