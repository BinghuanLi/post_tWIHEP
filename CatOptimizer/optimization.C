
double FOM(double sig, double bkg, TString fom="AMS1", double unc_bkg = 0.1, int b_reg = 0);
double Sum(double A, double B, double correlation = 0.);

void optimization(TString BasePath, int dnn_cat=1, TString region = "SigRegion")
{
gROOT->Reset();
gStyle->SetCanvasColor(0);
gStyle->SetFrameBorderMode(0);
gStyle->SetOptStat(0);
gStyle->SetPalette(1,0);
gStyle->SetTitleX(0.5); //title X location 
gStyle->SetTitleY(0.96); //title Y location 
gStyle->SetPaintTextFormat(".2f");
gErrorIgnoreLevel = kWarning;
  TCanvas* c1 = new TCanvas("c1","c1",0,0,800,600);
  using namespace std;

  TString OutPath = BasePath+region+"/";
  //CUT VALUES
 
  float Hj1_BDT = -1.;
  float leadLep_jetdr = 2.416;
  float secondLep_jetdr = 1.984;
  float lep1_conePt = 280.;
  float lep2_conePt = 200.;
  float n_presel_jet = 3.5;
  float maxeta = 2.16;
  float Mt_metleadlep = 680.;
  float hadTop_BDT = -1;

  vector<string> PLOT; vector<string> DNN;                 vector<int> BIN;     vector<float> MIN;   vector<float> MAX;    vector<bool> ReWeight;      vector<TString> AXIS; vector<TString> FOMs; vector<float> ERROR; vector<int> Regularization; vector<float> CORRELATION;
  PLOT.push_back("DNN_maxval"); DNN.push_back("DNNCat");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(true);   AXIS.push_back("#DNN_maxval"); FOMs.push_back("AMS1");  ERROR.push_back(0.1); Regularization.push_back(1); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval"); DNN.push_back("DNNCat");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(true);   AXIS.push_back("#DNN_maxval"); FOMs.push_back("AMS2");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval"); DNN.push_back("DNNCat");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(true);   AXIS.push_back("#DNN_maxval"); FOMs.push_back("AMS3");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval"); DNN.push_back("DNNCat");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(true);   AXIS.push_back("#DNN_maxval"); FOMs.push_back("AMS4");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval"); DNN.push_back("DNNCat");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(true);   AXIS.push_back("#DNN_maxval"); FOMs.push_back("AMS5");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval"); DNN.push_back("DNNCat");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(false);   AXIS.push_back("#DNN_maxval"); FOMs.push_back("AMS1");  ERROR.push_back(0.1); Regularization.push_back(1); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval"); DNN.push_back("DNNCat");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(false);   AXIS.push_back("#DNN_maxval"); FOMs.push_back("AMS2");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval"); DNN.push_back("DNNCat");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(false);   AXIS.push_back("#DNN_maxval"); FOMs.push_back("AMS3");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval"); DNN.push_back("DNNCat");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(false);   AXIS.push_back("#DNN_maxval"); FOMs.push_back("AMS4");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval"); DNN.push_back("DNNCat");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(false);   AXIS.push_back("#DNN_maxval"); FOMs.push_back("AMS5");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option2"); DNN.push_back("DNNCat_option2");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(true);   AXIS.push_back("#DNN_maxval_option2"); FOMs.push_back("AMS1");  ERROR.push_back(0.1); Regularization.push_back(1); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option2"); DNN.push_back("DNNCat_option2");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(true);   AXIS.push_back("#DNN_maxval_option2"); FOMs.push_back("AMS2");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option2"); DNN.push_back("DNNCat_option2");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(true);   AXIS.push_back("#DNN_maxval_option2"); FOMs.push_back("AMS3");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option2"); DNN.push_back("DNNCat_option2");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(true);   AXIS.push_back("#DNN_maxval_option2"); FOMs.push_back("AMS4");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option2"); DNN.push_back("DNNCat_option2");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(true);   AXIS.push_back("#DNN_maxval_option2"); FOMs.push_back("AMS5");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option2"); DNN.push_back("DNNCat_option2");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(false);   AXIS.push_back("#DNN_maxval_option2"); FOMs.push_back("AMS1");  ERROR.push_back(0.1); Regularization.push_back(1); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option2"); DNN.push_back("DNNCat_option2");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(false);   AXIS.push_back("#DNN_maxval_option2"); FOMs.push_back("AMS2");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option2"); DNN.push_back("DNNCat_option2");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(false);   AXIS.push_back("#DNN_maxval_option2"); FOMs.push_back("AMS3");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option2"); DNN.push_back("DNNCat_option2");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(false);   AXIS.push_back("#DNN_maxval_option2"); FOMs.push_back("AMS4");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option2"); DNN.push_back("DNNCat_option2");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(false);   AXIS.push_back("#DNN_maxval_option2"); FOMs.push_back("AMS5");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option3"); DNN.push_back("DNNCat_option3");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(true);   AXIS.push_back("#DNN_maxval_option3"); FOMs.push_back("AMS1");  ERROR.push_back(0.1); Regularization.push_back(1); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option3"); DNN.push_back("DNNCat_option3");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(true);   AXIS.push_back("#DNN_maxval_option3"); FOMs.push_back("AMS2");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option3"); DNN.push_back("DNNCat_option3");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(true);   AXIS.push_back("#DNN_maxval_option3"); FOMs.push_back("AMS3");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option3"); DNN.push_back("DNNCat_option3");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(true);   AXIS.push_back("#DNN_maxval_option3"); FOMs.push_back("AMS4");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option3"); DNN.push_back("DNNCat_option3");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(true);   AXIS.push_back("#DNN_maxval_option3"); FOMs.push_back("AMS5");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option3"); DNN.push_back("DNNCat_option3");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(false);   AXIS.push_back("#DNN_maxval_option3"); FOMs.push_back("AMS1");  ERROR.push_back(0.1); Regularization.push_back(1); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option3"); DNN.push_back("DNNCat_option3");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(false);   AXIS.push_back("#DNN_maxval_option3"); FOMs.push_back("AMS2");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option3"); DNN.push_back("DNNCat_option3");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(false);   AXIS.push_back("#DNN_maxval_option3"); FOMs.push_back("AMS3");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option3"); DNN.push_back("DNNCat_option3");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(false);   AXIS.push_back("#DNN_maxval_option3"); FOMs.push_back("AMS4");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
  PLOT.push_back("DNN_maxval_option3"); DNN.push_back("DNNCat_option3");   BIN.push_back(100);   MIN.push_back(0);    MAX.push_back(1);   ReWeight.push_back(false);   AXIS.push_back("#DNN_maxval_option3"); FOMs.push_back("AMS5");  ERROR.push_back(0.1); Regularization.push_back(0); CORRELATION.push_back(0);
	
  std::cout << BasePath+region+"/TTH_"+region+".root" << std::endl;
  TFile *file01 = TFile::Open(BasePath+region+"/TTH_"+region+".root");
  TFile *file02 = TFile::Open(BasePath+region+"/TTW_"+region+".root");
  TFile *file03 = TFile::Open(BasePath+region+"/TTZ_"+region+".root");
  TFile *file04 = TFile::Open(BasePath+region+"/Conv_"+region+".root");
  TFile *file05 = TFile::Open(BasePath+region+"/Fakes_"+region+".root");
  TFile *file06 = TFile::Open(BasePath+region+"/FakeSub_"+region+".root");
  TFile *file07 = TFile::Open(BasePath+region+"/Flips_"+region+".root");
  TFile *file08 = TFile::Open(BasePath+region+"/Rest_"+region+".root");
  TTree *Tree01 = (TTree*)file01->Get("output_tree");
  TTree *Tree02 = (TTree*)file02->Get("output_tree");
  TTree *Tree03 = (TTree*)file03->Get("output_tree");
  TTree *Tree04 = (TTree*)file04->Get("output_tree");
  TTree *Tree05 = (TTree*)file05->Get("output_tree");
  TTree *Tree06 = (TTree*)file06->Get("output_tree");
  TTree *Tree07 = (TTree*)file07->Get("output_tree");
  TTree *Tree08 = (TTree*)file08->Get("output_tree");
  
    for(int p=0; p<PLOT.size(); p++){
      const char *plot = PLOT[p].c_str();
      const char *catName = DNN[p].c_str();
      TString name = PLOT[p];
      TString FigureOfMerit = FOMs[p];
      int bin=BIN[p]; 
      float err = ERROR[p];
      int bkg_reg = Regularization[p]; 
      float corr_factor = CORRELATION[p];
      float min=MIN[p]; 
      float max=MAX[p]; 
      TString axis = AXIS[p];
      TH1F *MediumZ           = new TH1F("MediumZ",               "MediumZ",               bin+1,min-(max-min)/(2*bin),max+(max-min)/(2*bin));
      TH1F *ROC               = new TH1F("ROC",               "ROC",               bin+1,min-(max-min)/(2*bin),max+(max-min)/(2*bin));
      TH1F *SignalEfficiency1 = new TH1F("SignalEfficiency1", "SignalEfficiency1", bin+1,min-(max-min)/(2*bin),max+(max-min)/(2*bin));
      TH1F *BackgroundYield1  = new TH1F("BackgroundYield1",  "BackgroundYield1",  bin+1,min-(max-min)/(2*bin),max+(max-min)/(2*bin));
      float max1 = 0;
      float Tprime_0900Integral = 0;
      float Tprime_1700Integral = 0;
      float cutValue = 0;
      cutValue = min;
      float bestFoM=-99;
      float bestCut=-99;
      float bestSigUp=-99;
      float bestBkgUp=-99;
  

      for(int i=0; i<bin+1; i++){
	char CUT [1000]; char CUTdown [1000];    
	if(ReWeight[p]){
        sprintf(CUT, "EventWeight*%s*(%s>%f && %s == %i)", plot, plot, cutValue, catName, dnn_cat);
        sprintf(CUTdown, "EventWeight*%s*(%s<=%f && %s == %i)", plot, plot, cutValue, catName, dnn_cat);
    }
	else{
        sprintf(CUT, "EventWeight*(%s>=%f && %s == %i)", plot, cutValue, catName, dnn_cat);
        sprintf(CUTdown, "EventWeight*(%s<=%f && %s == %i)", plot, cutValue, catName, dnn_cat);
    }
    
	char variable[50]; 
	sprintf(variable, "lep1_conePt");
      
	char input01[50]; sprintf(input01, "%s>>h01(1,-9,999999)",variable);
	char input02[50]; sprintf(input02, "%s>>h02(1,-9,999999)",variable);
	char input03[50]; sprintf(input03, "%s>>h03(1,-9,999999)",variable);
	char input04[50]; sprintf(input04, "%s>>h04(1,-9,999999)",variable);
	char input05[50]; sprintf(input05, "%s>>h05(1,-9,999999)",variable);
	char input06[50]; sprintf(input06, "%s>>h06(1,-9,999999)",variable);
	char input07[50]; sprintf(input07, "%s>>h07(1,-9,999999)",variable);
	char input08[50]; sprintf(input08, "%s>>h08(1,-9,999999)",variable);
	TH1F *temp = new TH1F("", "", 1,-9,999999);
	Tree01->Draw(input01,CUT);  TH1F* h01=(TH1F*)gDirectory->Get("h01"); TH1F *TTH =(TH1F*)h01->Clone();
	Tree02->Draw(input02,CUT);  TH1F* h02=(TH1F*)gDirectory->Get("h02"); TH1F *TTW =(TH1F*)h02->Clone();
	Tree03->Draw(input03,CUT);  TH1F* h03=(TH1F*)gDirectory->Get("h03"); TH1F *TTZ =(TH1F*)h03->Clone();
	Tree04->Draw(input04,CUT);  TH1F* h04=(TH1F*)gDirectory->Get("h04"); TH1F *Conv =(TH1F*)h04->Clone();
	Tree05->Draw(input05,CUT);  TH1F* h05=(TH1F*)gDirectory->Get("h05"); TH1F *Fakes =(TH1F*)h05->Clone();
	Tree06->Draw(input06,CUT);  TH1F* h06=(TH1F*)gDirectory->Get("h06"); TH1F *FakeSub         =(TH1F*)h06->Clone();
	Tree07->Draw(input07,CUT);  TH1F* h07=(TH1F*)gDirectory->Get("h07"); TH1F *Flips         =(TH1F*)h07->Clone();
	Tree08->Draw(input08,CUT);  TH1F* h08=(TH1F*)gDirectory->Get("h08"); TH1F *Rest         =(TH1F*)h08->Clone();
	delete h01; delete h02; delete h03; delete h04; delete h05; delete h06; delete h07; delete h08;  

    Fakes->Add(Conv);
	Fakes->Add(FakeSub,-1);
    
	double sig = 0.;
    double bkg = 0.;
    if(dnn_cat ==1){//ttHnode
        sig = TTH->Integral();
        bkg = TTW->Integral() + TTZ->Integral() + Fakes->Integral() + Rest->Integral();
    }else if(dnn_cat==2){// ttJnode
        sig = Fakes->Integral();
        bkg = TTW->Integral() + TTZ->Integral() + TTH->Integral() + Rest->Integral();
    }else if(dnn_cat==3){// ttWnode
        sig = TTW->Integral();
        bkg = Fakes->Integral() + TTZ->Integral() + TTH->Integral() + Rest->Integral();
    }else if(dnn_cat==4){// ttZnode
        sig = TTZ->Integral();
        bkg = Fakes->Integral() + TTW->Integral() + TTH->Integral() + Rest->Integral();
    }else{
        std::cout<<" ERROR : dnn_cat must be 1/2/3 or 4,  you pass dnn_cat a value "<< dnn_cat<<std::endl;
    }
    double  FoM = FOM(sig, bkg, FigureOfMerit, err, bkg_reg); 
	
	char inputdown01[50]; sprintf(inputdown01, "%s>>hdown01(1,-9,999999)",variable);
	char inputdown02[50]; sprintf(inputdown02, "%s>>hdown02(1,-9,999999)",variable);
	char inputdown03[50]; sprintf(inputdown03, "%s>>hdown03(1,-9,999999)",variable);
	char inputdown04[50]; sprintf(inputdown04, "%s>>hdown04(1,-9,999999)",variable);
	char inputdown05[50]; sprintf(inputdown05, "%s>>hdown05(1,-9,999999)",variable);
	char inputdown06[50]; sprintf(inputdown06, "%s>>hdown06(1,-9,999999)",variable);
	char inputdown07[50]; sprintf(inputdown07, "%s>>hdown07(1,-9,999999)",variable);
	char inputdown08[50]; sprintf(inputdown08, "%s>>hdown08(1,-9,999999)",variable);
    Tree01->Draw(inputdown01,CUTdown);  TH1F* hdown01=(TH1F*)gDirectory->Get("hdown01"); TH1F *TTHdown =(TH1F*)hdown01->Clone();
	Tree02->Draw(inputdown02,CUTdown);  TH1F* hdown02=(TH1F*)gDirectory->Get("hdown02"); TH1F *TTWdown =(TH1F*)hdown02->Clone();
	Tree03->Draw(inputdown03,CUTdown);  TH1F* hdown03=(TH1F*)gDirectory->Get("hdown03"); TH1F *TTZdown =(TH1F*)hdown03->Clone();
	Tree04->Draw(inputdown04,CUTdown);  TH1F* hdown04=(TH1F*)gDirectory->Get("hdown04"); TH1F *Convdown =(TH1F*)hdown04->Clone();
	Tree05->Draw(inputdown05,CUTdown);  TH1F* hdown05=(TH1F*)gDirectory->Get("hdown05"); TH1F *Fakesdown =(TH1F*)hdown05->Clone();
	Tree06->Draw(inputdown06,CUTdown);  TH1F* hdown06=(TH1F*)gDirectory->Get("hdown06"); TH1F *FakeSubdown         =(TH1F*)hdown06->Clone();
	Tree07->Draw(inputdown07,CUTdown);  TH1F* hdown07=(TH1F*)gDirectory->Get("hdown07"); TH1F *Flipsdown         =(TH1F*)hdown07->Clone();
	Tree08->Draw(inputdown08,CUTdown);  TH1F* hdown08=(TH1F*)gDirectory->Get("hdown08"); TH1F *Restdown         =(TH1F*)hdown08->Clone();
	delete hdown01; delete hdown02; delete hdown03; delete hdown04; delete hdown05; delete hdown06; delete hdown07; delete hdown08;  
        
	TTWdown->Add(TTZdown);
	TTWdown->Add(Convdown);
	TTWdown->Add(Fakesdown);
	TTWdown->Add(FakeSubdown,-1);
	TTWdown->Add(Flipsdown);
	TTWdown->Add(Restdown);
    
	double sigdown = TTHdown->Integral();
    double bkgdown = TTWdown->Integral();
    double  FoMdown = FOM(sigdown, bkgdown, FigureOfMerit, err, bkg_reg); 
	
    double FoM_sum = -1.;
    if(FoM >0 && FoMdown > 0)FoM_sum = Sum(FoM, FoMdown, corr_factor);
   
	if(bestFoM< FoM_sum && FoM_sum >0 ){
	    bestFoM = FoM_sum; 
	    bestCut = ROC->GetBinCenter(i+1);
        bestSigUp = sig;
        bestBkgUp = bkg; 
	}
	MediumZ          ->SetBinContent(i+1, FoM_sum);
	ROC              ->SetBinContent(i+1, FoM);
	SignalEfficiency1->SetBinContent(i+1, sig);
	BackgroundYield1 ->SetBinContent(i+1, bkg);
	MediumZ          ->SetBinError(i+1, 0.00001);
	ROC              ->SetBinError(i+1, 0.00001);
	SignalEfficiency1->SetBinError(i+1, 0.00001);
	BackgroundYield1 ->SetBinError(i+1, 0.00001);
	cutValue = cutValue + (max-min)/bin;
    
	delete TTH; 
	delete TTW; delete TTZ; delete Conv; delete Fakes; delete Flips; delete FakeSub; delete Rest;
	delete TTHdown; 
	delete TTWdown; delete TTZdown; delete Convdown; delete Fakesdown; delete Flipsdown; delete FakeSubdown; delete Restdown;
      }
 
    if (!ReWeight[p]){
      cout<<"Best cut for dnn_cat "<<dnn_cat<<" and variable '"<<axis<<"' is <"<<bestCut<<" FOM is "<<FigureOfMerit<< " : "<< bestFoM<<" BestSigUp is "<< bestSigUp<< " BestBkgUp is "<< bestBkgUp << " b_reg is "<< bkg_reg << " syst_unc is "<< err << " correlation is " << corr_factor << std::endl;
    }else{
      cout<<"Best cut for dnn_cat "<<dnn_cat<<" and variable '"<<axis<<"' is <"<<bestCut<<" ReWeight FOM is "<<FigureOfMerit<< " : "<< bestFoM<<" BestSigUp is "<< bestSigUp<< " BestBkgUp is "<< bestBkgUp << " b_reg is "<< bkg_reg << " syst_unc is "<< err << " correlation is " << corr_factor << std::endl;
    }
      
      TCanvas* c2 = new TCanvas("c2","c2",0,0,800,600);
      c2->cd();
      c2->SetGridy();
      ROC->Draw("E");
      ROC->SetMinimum(0.0);
      //ROC->SetMaximum(0.05);
      ROC->SetMarkerStyle(21);
      ROC->SetLineColor(1);
      ROC->GetYaxis()->SetTitleSize(0.040);
      ROC->GetXaxis()->SetTitleSize(0.045);
      ROC->GetYaxis()->SetLabelSize(0.035);
      ROC->GetXaxis()->SetLabelSize(0.045);
      ROC->SetTitle("");
      ROC->GetXaxis()->SetTitle(axis);
      ROC->GetYaxis()->SetTitleOffset(1.25);
      ROC->GetYaxis()->SetTitle("Accumalative "+FigureOfMerit);
      
  

      char cat[2]; sprintf(cat,"%i",   dnn_cat); TString CAT = cat;
      char drf[2]; sprintf(drf,"%.0f", leadLep_jetdr   ); TString DRF = drf;
      char drs[2]; sprintf(drs,"%.0f", secondLep_jetdr   ); TString DRS = drs;
      char fPt[2]; sprintf(fPt,"%.0f", lep1_conePt); TString FPT = fPt;
      char sPt[2]; sprintf(sPt,"%.0f", lep2_conePt); TString SPT = sPt;
      char nJt[2]; sprintf(nJt,"%.0f", n_presel_jet   ); TString NJT = nJt;
      char bta[2]; sprintf(bta,"%.0f", maxeta     ); TString BTA = bta;
      char mtL[2]; sprintf(mtL,"%.0f",   Mt_metleadlep    ); TString MTL = mtL;
      char hTp[2]; sprintf(hTp,"%.0f", hadTop_BDT   ); TString HTP = hTp;
      char Cor[4]; sprintf(Cor,"%.2f", corr_factor); TString COR = Cor;
      char Err[4]; sprintf(Err,"%.2f", err); TString ERR = Err;
      char Cut[4]; sprintf(Cut,"%.2f", bestCut); TString CUT = Cut;
      char Reg[2]; sprintf(Reg,"%i", bkg_reg); TString REG= Reg;
      
      if(ReWeight[p]) c2->SaveAs(OutPath+name+"_cat"+CAT+"_"+FigureOfMerit+"_Cut"+CUT+"_Err"+ERR+"_Reg"+REG+"_COR"+COR+"_ROC_ReWeight.png");
      else c2->SaveAs(OutPath+name+"_cat"+CAT+"_"+FigureOfMerit+"_Cut"+CUT+"_Err"+ERR+"_Reg"+REG+"_COR"+COR+"_ROC.png");
     
      TCanvas* c3 = new TCanvas("c3","c3",0,0,800,600);
      c3->SetGridy();
      MediumZ->Draw("E");
      MediumZ->SetMinimum(0.0);
      MediumZ->SetMarkerStyle(21);
      MediumZ->SetLineColor(1);
      MediumZ->GetYaxis()->SetTitleSize(0.040);
      MediumZ->GetXaxis()->SetTitleSize(0.045);
      MediumZ->GetYaxis()->SetLabelSize(0.035);
      MediumZ->GetXaxis()->SetLabelSize(0.045);
      MediumZ->SetTitle("");
      MediumZ->GetXaxis()->SetTitle(axis);
      MediumZ->GetYaxis()->SetTitleOffset(1.25);
      MediumZ->GetYaxis()->SetTitle(FigureOfMerit);
      if(ReWeight[p]) c3->SaveAs(OutPath+name+"_cat"+CAT+"_"+FigureOfMerit+"_Cut"+CUT+"_Err"+ERR+"_Reg"+REG+"_COR"+COR+"_MediumZ_ReWeight.png");
      else c3->SaveAs(OutPath+name+"_cat"+CAT+"_"+FigureOfMerit+"_Cut"+CUT+"_Err"+ERR+"_Reg"+REG+"_COR"+COR+"_MediumZ.png");



      TCanvas* c4 = new TCanvas("c4","c4",0,0,800,600);
      TPad *pad1 = new TPad("pad1","",0,0,1,1);
      TPad *pad2 = new TPad("pad2","",0,0,1,1);
      pad2->SetFillStyle(4000); //will be transparent
      pad1->Draw();
      pad1->cd();
      
      SignalEfficiency1->Draw("E");
      SignalEfficiency1->SetMinimum(0.0);
      //SignalEfficiency1->SetMaximum(1.4);
      SignalEfficiency1->SetMarkerStyle(21);
      SignalEfficiency1->SetLineColor(1);
      SignalEfficiency1->GetYaxis()->SetTitleSize(0.045);
      SignalEfficiency1->GetXaxis()->SetTitleSize(0.045);
      SignalEfficiency1->GetYaxis()->SetLabelSize(0.045);
      SignalEfficiency1->GetXaxis()->SetLabelSize(0.045);
      SignalEfficiency1->SetTitle("");
      SignalEfficiency1->GetXaxis()->SetTitle(axis);
      SignalEfficiency1->GetYaxis()->SetTitle("Signal yield");
      
      c4->cd();
      Double_t ymin = 0;
      Double_t  ymax = BackgroundYield1->Integral();//max1*1.5;
      ymax = BackgroundYield1->GetBinContent(1)+10;
      Double_t dy = (ymax-ymin)/0.8; //10 per cent margins top and bottom
      Double_t xmin = SignalEfficiency1->GetXaxis()->GetXmin();
      Double_t xmax = SignalEfficiency1->GetXaxis()->GetXmax();
      Double_t dx = (xmax-xmin)/0.8; //10 per cent margins left and right
      pad2->Range(xmin-0.1*dx,ymin-0.1*dy,xmax+0.1*dx,ymax+0.1*dy);
      pad2->Draw();
      pad2->cd();
      
      BackgroundYield1->SetMinimum(0.0);
      BackgroundYield1->GetYaxis()->SetTitleSize(0.045);
      BackgroundYield1->GetXaxis()->SetTitleSize(0.045);
      BackgroundYield1->GetYaxis()->SetLabelSize(0.045);
      BackgroundYield1->GetXaxis()->SetLabelSize(0.045);
      BackgroundYield1->SetTitle("");
      BackgroundYield1->GetXaxis()->SetTitle(axis);
      BackgroundYield1->GetYaxis()->SetTitle("Background yield");
      BackgroundYield1->SetMarkerStyle(21);
      BackgroundYield1->SetMarkerColor(2);
      BackgroundYield1->SetLineColor(2);
      BackgroundYield1->Draw("][sames");
       
      // draw axis on the right side of the pad
      TGaxis *Axis1 = new TGaxis(xmax,ymin,xmax,ymax,ymin,ymax,510,"+L");
      Axis1->SetLabelColor(kRed);
      Axis1->SetTitle("Background Yield");
      Axis1->SetTitleOffset(1.2);
      Axis1->SetTitleColor(kRed);
      Axis1->SetTitleSize(0.045);
      Axis1->SetLabelSize(0.045);
      Axis1->Draw();
      
      TLegend *pl = new TLegend(0.57,0.75,0.89,0.89);
      pl->SetTextSize(0.03); 
      pl->SetFillColor(0);
      TLegendEntry *ple = pl->AddEntry(SignalEfficiency1, "Signal Yield",  "LP");
      ple               = pl->AddEntry(BackgroundYield1,  "Background Yield",  "LP");
      pl->Draw();
      if(ReWeight[p]) c4->SaveAs(OutPath+name+"_cat"+CAT+"_"+FigureOfMerit+"_Cut"+CUT+"_Err"+ERR+"_Reg"+REG+"_COR"+COR+"_Yield_ReWeight.png");
      else c4->SaveAs(OutPath+name+"_cat"+CAT+"_"+FigureOfMerit+"_Cut"+CUT+"_Err"+ERR+"_Reg"+REG+"_COR"+COR+"_Yield.png");
      delete MediumZ;
      delete ROC;
      delete SignalEfficiency1;
      delete BackgroundYield1;
      delete c2;
      delete c3;
      delete c4;
  }
}
double FOM(double sig, double bkg, TString fom, double unc_bkg , int b_reg ){
    /*
    "AMS1": FOM = S/B, purity
    "AMS2": FOM = S/sqrt(B), medium significance when s<<b and b is  certain
    "AMS3": FOM = S/sqrt(b+var(b)), medium significance when s << b and b is uncertain with variance var(b)
    "AMS4": FOM = sqrt(2(s+b)ln(1+s/b)-s), medium significance when s << b deosn't hold and b is certain
    "AMS5": FOM = sqrt(2{(s+b)ln[(s+b)(b+var(b))/(b^2+(s+b)var(b))]-(b^2/var(b))*ln[1+var(b)*s/(b(b+var(b)))]}),
            medium significance when s << b doesn't hold and b is uncertain with variance var(b)
            https://www.pp.rhul.ac.uk/~cowan/stat/medsig/medsigNote.pdf
    unc_bkg = sigma(b)/b
    var(b) = (sigma(b))^2 = (b * unc_bkg)^2
    */
    double FOM = -1.;
    bkg = bkg + b_reg; // rescale bkg if necessary
    if(sig <= 0 || bkg <= 0 ) return FOM;
    double var_b = (bkg * bkg * unc_bkg * unc_bkg); 
    if(fom=="AMS1"){
        FOM = sig/bkg; 
    }else if(fom=="AMS2"){
        FOM = sig/sqrt(bkg);
    }else if(fom=="AMS3"){
        FOM = sig/sqrt(bkg+var_b);
    }else if(fom=="AMS4"){
        FOM = sqrt(2.*((sig+bkg)*log(1.+sig/bkg)-sig));
    }else if(fom=="AMS5"){
        FOM = sqrt(2.*((sig+bkg)*log((sig+bkg)*(bkg+var_b)/(bkg*bkg+(sig+bkg)*var_b))-bkg*bkg*log(1.+var_b*sig/(bkg*(bkg+var_b)))/var_b));
    }else{
        std::cout << "ERROR: fom must be AMS1, AMS2, AMS3, AMS4 or AMS5, the provided is : "<< fom << std::endl;
    }
    return FOM;
};
double Sum(double A, double B, double correlation){
    double sum_of_square = A*A + B*B + 2*correlation*A*B;
    double sum = -1.;
    if(sum_of_square <0){
        std::cout<< "#### ERROR : sum_of_square < 0 #########" << std::endl;
    }else{
        sum = sqrt(sum_of_square);
    }
    return sum;
};
