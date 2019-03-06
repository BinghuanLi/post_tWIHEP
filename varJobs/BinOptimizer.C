// Input : rootplas with DNN maxval and DNN Cat Flag
// Function: copytrees and add channel flags, add BinOptimized Histograms
// Output : rootplas ready for statistics study and histograms for Optimized Binning 
#include "Maps.C"

//std::vector<TString> samples = {"Rares","EWK","Conv","TTW","TTZ","TTWW","Fakes","FakeSub","Flips","TTH_htt","TTH_hww","TTH_hzz","TTH_hot","TTH_hmm","THQ_htt","THQ_hww","THQ_hzz","THW_htt","THW_hww","THW_hzz"};
std::vector<TString> samples = {"Fakes","TTZ","FakeSub","Flips","TTH_htt"};
// SubCatNames should be mapped to VarNames 1 to 1
std::vector<TString> SubCatNames = {"DNNCat","DNNCat_option2","DNNCat_option3","DNNSubCat1_option1","DNNSubCat1_option2","DNNSubCat1_option3","DNNSubCat2_option1","DNNSubCat2_option2","DNNSubCat2_option3"};
std::vector<TString> VarNames = {"DNN_maxval","DNN_maxval_option2","DNN_maxval_option3","DNN_maxval","DNN_maxval_option2","DNN_maxval_option3","DNN_maxval","DNN_maxval_option2","DNN_maxval_option3"};
std::map<TString,std::vector<TH1F*>> theHistoMap;

void createHists();
void fillHists(TString SampleName, TString SubCatName, TString VarName, Int_t theChannel, float var, float theweight);


void BinOptimizer(TString InputDir, TString OutputDir, TString RegionName , Bool_t OptBin = true, TString JESVar=""){
 
    TString BinRootFile = OutputDir+"/BinData/OptBin_"+RegionName+".root";
    TFile *newBinFile;
    if(OptBin){
        newBinFile = new TFile(BinRootFile,"recreate");
        createHists();
    }

    for(auto s : samples){
        TString Input = InputDir + "/"+JESVar+RegionName+"/"+s + "_"+JESVar+RegionName+".root";
        TString Output = OutputDir + "/"+JESVar+RegionName+"/"+s + "_"+JESVar+RegionName+".root";
        std::cout <<" input file is " << Input << std::endl;
        std::cout <<" output file is " << Output << std::endl;
        TFile *oldfile = new TFile(Input);
        TTree *oldtree = (TTree*)oldfile->Get("output_tree");

        Long64_t nentries = oldtree->GetEntries(); 
        float Dilep_pdgId=0; // 1 mm; 2 em; 3 ee
        float Sum2lCharge=0; // >0 ss+; =0 os; <0 ss-
        float nBJetMedium=0; // >=2 bt
        float DNNCat=0;
        float DNNCat_option2=0;
        float DNNCat_option3=0;
        float DNN_maxval=0;
        float DNN_maxval_option2=0;
        float DNN_maxval_option3=0;
        float EventWeight(0.); 
        
        oldtree->SetBranchAddress("Dilep_pdgId", &Dilep_pdgId);
        oldtree->SetBranchAddress("EventWeight", &EventWeight);
        oldtree->SetBranchAddress("Sum2lCharge", &Sum2lCharge);
        oldtree->SetBranchAddress("nBJetMedium", &nBJetMedium);
        oldtree->SetBranchAddress("DNNCat", &DNNCat);
        oldtree->SetBranchAddress("DNNCat_option2", &DNNCat_option2);
        oldtree->SetBranchAddress("DNNCat_option3", &DNNCat_option3);
        oldtree->SetBranchAddress("DNN_maxval", &DNN_maxval);
        oldtree->SetBranchAddress("DNN_maxval_option2", &DNN_maxval_option2);
        oldtree->SetBranchAddress("DNN_maxval_option3", &DNN_maxval_option3);
        oldtree->SetBranchStatus("*", 1);
    
        TFile *newfile = new TFile(Output,"recreate");
        TTree *newtree = new TTree("syncTree","syncTree");
    
        // new flags
        // ee->charge; em->DNN; mm->DNN
        float DNNSubCat1_option1(0.), DNNSubCat1_option2(0.), DNNSubCat1_option3(0.);
        // ee->DNN; em->DNN; mm->DNN
        float DNNSubCat2_option1(0.), DNNSubCat2_option2(0.), DNNSubCat2_option3(0.);
        newtree = oldtree->CloneTree(0);
        newtree->Branch("DNNSubCat1_option1",&DNNSubCat1_option1);
        newtree->Branch("DNNSubCat1_option2",&DNNSubCat1_option2);
        newtree->Branch("DNNSubCat1_option3",&DNNSubCat1_option3);
        newtree->Branch("DNNSubCat2_option1",&DNNSubCat2_option1);
        newtree->Branch("DNNSubCat2_option2",&DNNSubCat2_option2);
        newtree->Branch("DNNSubCat2_option3",&DNNSubCat2_option3);
    
        
        for (Long64_t i=0;i<nentries; i++) {
            EventWeight=0;
            Dilep_pdgId=0;
            Sum2lCharge=0;
            nBJetMedium=0;
            DNNCat=0;
            DNNCat_option2=0;
            DNNCat_option3=0;
            DNN_maxval=0;
            DNN_maxval_option2=0;
            DNN_maxval_option3=0;
            DNNSubCat1_option1=0;
            DNNSubCat1_option2=0;
            DNNSubCat1_option3=0;
            DNNSubCat2_option1=0;
            DNNSubCat2_option2=0;
            DNNSubCat2_option3=0;
            oldtree->GetEntry(i);
            // DNNSubCat1_option1
            if(Dilep_pdgId==3){//ee
                DNNSubCat1_option1 = Sum2lCharge<0? 1:2; // neg:pos
            }else if(DNNCat==1){// ttH node
                DNNSubCat1_option1 = Dilep_pdgId>1.5? 3:7;// em:mm
            }else if(DNNCat==2){// ttJnode
                DNNSubCat1_option1 = Dilep_pdgId>1.5? 4:8;// em:mm
            }else if(DNNCat==3){// ttWnode
                DNNSubCat1_option1 = Dilep_pdgId>1.5? 5:9;// em:mm
            }else if(DNNCat==4){// ttZnode
                DNNSubCat1_option1 = Dilep_pdgId>1.5? 6:10;// em:mm
            }else{
                std::cout<< " DNNCat is : "<<DNNCat << std::endl;
            }
            // DNNSubCat2_option1
            if(DNNCat==1){// ttH node
                if(Dilep_pdgId==3)DNNSubCat2_option1=1; //ee
                else if(Dilep_pdgId==2)DNNSubCat2_option1=5; //em
                else if(Dilep_pdgId==1)DNNSubCat2_option1=9; //mm
                else std::cout<< " Dilep_pdgId is "<<Dilep_pdgId<<std::endl;
            }else if(DNNCat==2){// ttJnode
                if(Dilep_pdgId==3)DNNSubCat2_option1=2; //ee
                else if(Dilep_pdgId==2)DNNSubCat2_option1=6; //em
                else if(Dilep_pdgId==1)DNNSubCat2_option1=10; //mm
                else std::cout<< " Dilep_pdgId is "<<Dilep_pdgId<<std::endl;
            }else if(DNNCat==3){// ttWnode
                if(Dilep_pdgId==3)DNNSubCat2_option1=3; //ee
                else if(Dilep_pdgId==2)DNNSubCat2_option1=7; //em
                else if(Dilep_pdgId==1)DNNSubCat2_option1=11; //mm
                else std::cout<< " Dilep_pdgId is "<<Dilep_pdgId<<std::endl;
            }else if(DNNCat==4){// ttZnode
                if(Dilep_pdgId==3)DNNSubCat2_option1=4; //ee
                else if(Dilep_pdgId==2)DNNSubCat2_option1=8; //em
                else if(Dilep_pdgId==1)DNNSubCat2_option1=12; //mm
                else std::cout<< " Dilep_pdgId is "<<Dilep_pdgId<<std::endl;
            }else{
                std::cout<< " DNNCat is : "<<DNNCat << std::endl;
            }
            
            // DNNSubCat1_option2
            if(Dilep_pdgId==3){//ee
                DNNSubCat1_option2 = Sum2lCharge<0? 1:2; // neg:pos
            }else if(DNNCat_option2==1){// ttH node
                DNNSubCat1_option2 = Dilep_pdgId>1.5? 3:7;// em:mm
            }else if(DNNCat_option2==2){// ttJnode
                DNNSubCat1_option2 = Dilep_pdgId>1.5? 4:8;// em:mm
            }else if(DNNCat_option2==3){// ttWnode
                DNNSubCat1_option2 = Dilep_pdgId>1.5? 5:9;// em:mm
            }else if(DNNCat_option2==4){// ttZnode
                DNNSubCat1_option2 = Dilep_pdgId>1.5? 6:10;// em:mm
            }else{
                std::cout<< " DNNCat_option2 is : "<<DNNCat_option2 << std::endl;
            }
            // DNNSubCat2_option2
            if(DNNCat_option2==1){// ttH node
                if(Dilep_pdgId==3)DNNSubCat2_option2=1; //ee
                else if(Dilep_pdgId==2)DNNSubCat2_option2=5; //em
                else if(Dilep_pdgId==1)DNNSubCat2_option2=9; //mm
                else std::cout<< " Dilep_pdgId is "<<Dilep_pdgId<<std::endl;
            }else if(DNNCat_option2==2){// ttJnode
                if(Dilep_pdgId==3)DNNSubCat2_option2=2; //ee
                else if(Dilep_pdgId==2)DNNSubCat2_option2=6; //em
                else if(Dilep_pdgId==1)DNNSubCat2_option2=10; //mm
                else std::cout<< " Dilep_pdgId is "<<Dilep_pdgId<<std::endl;
            }else if(DNNCat_option2==3){// ttWnode
                if(Dilep_pdgId==3)DNNSubCat2_option2=3; //ee
                else if(Dilep_pdgId==2)DNNSubCat2_option2=7; //em
                else if(Dilep_pdgId==1)DNNSubCat2_option2=11; //mm
                else std::cout<< " Dilep_pdgId is "<<Dilep_pdgId<<std::endl;
            }else if(DNNCat_option2==4){// ttZnode
                if(Dilep_pdgId==3)DNNSubCat2_option2=4; //ee
                else if(Dilep_pdgId==2)DNNSubCat2_option2=8; //em
                else if(Dilep_pdgId==1)DNNSubCat2_option2=12; //mm
                else std::cout<< " Dilep_pdgId is "<<Dilep_pdgId<<std::endl;
            }else{
                std::cout<< " DNNCat_option2 is : "<<DNNCat_option2 << std::endl;
            }
            
            // DNNSubCat1_option3
            if(Dilep_pdgId==3){//ee
                DNNSubCat1_option3 = Sum2lCharge<0? 1:2; // neg:pos
            }else if(DNNCat_option3==1){// ttH node
                DNNSubCat1_option3 = Dilep_pdgId>1.5? 3:7;// em:mm
            }else if(DNNCat_option3==2){// ttJnode
                DNNSubCat1_option3 = Dilep_pdgId>1.5? 4:8;// em:mm
            }else if(DNNCat_option3==3){// ttWnode
                DNNSubCat1_option3 = Dilep_pdgId>1.5? 5:9;// em:mm
            }else if(DNNCat_option3==4){// ttZnode
                DNNSubCat1_option3 = Dilep_pdgId>1.5? 6:10;// em:mm
            }else{
                std::cout<< " DNNCat_option3 is : "<<DNNCat_option3 << std::endl;
            }
            // DNNSubCat2_option3
            if(DNNCat_option3==1){// ttH node
                if(Dilep_pdgId==3)DNNSubCat2_option3=1; //ee
                else if(Dilep_pdgId==2)DNNSubCat2_option3=5; //em
                else if(Dilep_pdgId==1)DNNSubCat2_option3=9; //mm
                else std::cout<< " Dilep_pdgId is "<<Dilep_pdgId<<std::endl;
            }else if(DNNCat_option3==2){// ttJnode
                if(Dilep_pdgId==3)DNNSubCat2_option3=2; //ee
                else if(Dilep_pdgId==2)DNNSubCat2_option3=6; //em
                else if(Dilep_pdgId==1)DNNSubCat2_option3=10; //mm
                else std::cout<< " Dilep_pdgId is "<<Dilep_pdgId<<std::endl;
            }else if(DNNCat_option3==3){// ttWnode
                if(Dilep_pdgId==3)DNNSubCat2_option3=3; //ee
                else if(Dilep_pdgId==2)DNNSubCat2_option3=7; //em
                else if(Dilep_pdgId==1)DNNSubCat2_option3=11; //mm
                else std::cout<< " Dilep_pdgId is "<<Dilep_pdgId<<std::endl;
            }else if(DNNCat_option3==4){// ttZnode
                if(Dilep_pdgId==3)DNNSubCat2_option3=4; //ee
                else if(Dilep_pdgId==2)DNNSubCat2_option3=8; //em
                else if(Dilep_pdgId==1)DNNSubCat2_option3=12; //mm
                else std::cout<< " Dilep_pdgId is "<<Dilep_pdgId<<std::endl;
            }else{
                std::cout<< " DNNCat_option3 is : "<<DNNCat_option3 << std::endl;
            }
            newtree->Fill();
std::vector<TString> SubCatNames = {"DNNCat","DNNCat_option2","DNNCat_option3","DNNSubCat1_option1","DNNSubCat1_option2","DNNSubCat1_option3","DNNSubCat2_option1","DNNSubCat2_option2","DNNSubCat2_option3"};
std::vector<TString> VarNames = {"DNN_maxval","DNN_maxval_option2","DNN_maxval_option3","DNN_maxval","DNN_maxval_option2","DNN_maxval_option3","DNN_maxval","DNN_maxval_option2","DNN_maxval_option3"};
            fillHists(s, "DNNCat" , "DNN_maxval", DNNCat, DNN_maxval, EventWeight);
            fillHists(s, "DNNSubCat1_option1" , "DNN_maxval", DNNSubCat1_option1, DNN_maxval, EventWeight);
            fillHists(s, "DNNSubCat2_option1" , "DNN_maxval", DNNSubCat2_option1, DNN_maxval, EventWeight);
            fillHists(s, "DNNCat_option2" , "DNN_maxval_option2", DNNCat_option2, DNN_maxval_option2, EventWeight);
            fillHists(s, "DNNSubCat1_option2" , "DNN_maxval_option2", DNNSubCat1_option2, DNN_maxval_option2, EventWeight);
            fillHists(s, "DNNSubCat2_option2" , "DNN_maxval_option2", DNNSubCat2_option2, DNN_maxval_option2, EventWeight);
            fillHists(s, "DNNCat_option3" , "DNN_maxval_option3", DNNCat_option3, DNN_maxval_option3, EventWeight);
            fillHists(s, "DNNSubCat1_option3" , "DNN_maxval_option3", DNNSubCat1_option3, DNN_maxval_option3, EventWeight);
            fillHists(s, "DNNSubCat2_option3" , "DNN_maxval_option3", DNNSubCat2_option3, DNN_maxval_option3, EventWeight);
        }
    
        newtree->SetName("syncTree");
        newtree->SetTitle("syncTree");
        //newtree->Write();
        newtree->AutoSave();
        gDirectory->Delete("output_tree;*");
        
        delete oldfile;    
        delete newfile;
    }
    if(OptBin){
        newBinFile->cd();
        for (auto histoMapElement: theHistoMap){
            for (auto hist:histoMapElement.second) hist->Write();
        }
    }
    delete newBinFile;
}

void createHists(){
    for(unsigned int i=0; i < SubCatNames.size(); i++){
        int nbins =1;
        double xmin = -1000;
        double xmax = 1000;
        TString varName = VarNames.at(i);
        TString subCatName = SubCatNames.at(i); 
        if(varName== "DNN_maxval") {nbins= 20; xmin= 0; xmax= 1;};
        if(varName== "DNN_maxval_option2") {nbins= 20; xmin= 0; xmax= 1;};
        if(varName== "DNN_maxval_option3") {nbins= 20; xmin= 0; xmax= 1;};
        std::map<Int_t, TString>::iterator it;
        for(it = MapOfChannelMap[subCatName].begin(); it!=MapOfChannelMap[subCatName].end(); it++){
            TString subChannel = it->second;
            TH1F* histo_sig = new TH1F((subCatName + "_" + varName+"_"+subChannel+"_Sig").Data(), (subCatName + "_" + varName+"_"+subChannel+"_Sig").Data(),nbins,xmin,xmax);
            histo_sig->Sumw2();
            TH1F* histo_bkg = new TH1F((subCatName + "_" + varName+"_"+subChannel+"_Bkg").Data(), (subCatName + "_" + varName+"_"+subChannel+"_Bkg").Data(),nbins,xmin,xmax);
            histo_bkg->Sumw2();
            TH1F* histo_TTH = new TH1F((subCatName + "_" + varName+"_"+subChannel+"_TTH").Data(), (subCatName + "_" + varName+"_"+subChannel+"_TTH").Data(),nbins,xmin,xmax);
            histo_TTH->Sumw2();
            theHistoMap[(subCatName + "_" + varName+"_"+subChannel)].push_back(histo_sig);
            theHistoMap[(subCatName + "_" + varName+"_"+subChannel)].push_back(histo_bkg);
            theHistoMap[(subCatName + "_" + varName+"_"+subChannel)].push_back(histo_TTH);
            std::cout << (" theHistoMap key: "+subCatName + "_" + varName+"_"+subChannel+" size ")<< theHistoMap[(subCatName + "_" + varName+"_"+subChannel)].size() << std::endl; 
        }
    }
}

void fillHists(TString SampleName, TString SubCatName, TString VarName, Int_t theChannel, float var, float theweight){
      int isSig = -1;
      int wgt = 1;
      if(SampleName.Contains("FakeSub"))wgt=-1;
      // normal case of Sig Bkg
      if(SampleName.Contains("TTH"))isSig=1;
      else if(SampleName.Contains("TTW") || SampleName.Contains("TTZ") || SampleName.Contains("Fakes") || SampleName.Contains("FakeSub") || SampleName.Contains("Flip") || SampleName.Contains("Conv"))isSig=0;
      // Sig Bkg according to DNN
      TString histoName = SubCatName+"_"+VarName+"_"+MapOfChannelMap[SubCatName][theChannel];
      if(histoName.Contains("ttJnode")){
        if(SampleName.Contains("Fakes") || SampleName.Contains("FakeSub") || SampleName.Contains("Flip") || SampleName.Contains("Conv"))isSig=1;
        else if(SampleName.Contains("TTW") || SampleName.Contains("TTZ") || SampleName.Contains("TTH"))isSig=0;
      }else if(histoName.Contains("ttWnode")){
        if(SampleName.Contains("TTW"))isSig=1;
        else if(SampleName.Contains("TTH") || SampleName.Contains("TTZ") || SampleName.Contains("Fakes") || SampleName.Contains("FakeSub") || SampleName.Contains("Flip") || SampleName.Contains("Conv"))isSig=0;
      }else if(histoName.Contains("ttZnode")){
        if(SampleName.Contains("TTZ"))isSig=1;
        else if(SampleName.Contains("TTH") || SampleName.Contains("TTW") || SampleName.Contains("Fakes") || SampleName.Contains("FakeSub") || SampleName.Contains("Flip") || SampleName.Contains("Conv"))isSig=0;
      }
      if(theHistoMap[histoName].size()!=3){
        std::cout<< " ERROR the HistoMap key: "<< histoName <<" size : "<< theHistoMap[histoName].size() << std::endl;
        return;
      }
      int binN = theHistoMap[histoName][0]->GetNbinsX();
      float minValue = theHistoMap[histoName][0]->GetBinLowEdge(1);
      float maxValue = theHistoMap[histoName][0]->GetBinLowEdge(binN+1);
      float fillValue = -999.;
      if(var < minValue){
        //std::cout<<" taking care of underflow "<<std::endl;
        fillValue = minValue + 0.0001;
      }else if(var > maxValue){
        //std::cout<<" taking care of overflow "<<std::endl;
        fillValue = maxValue - 0.0001;
      }else{
        //std::cout<<" fill value "<<std::endl;
        fillValue = var;
      }
      if(isSig==1){
        theHistoMap[histoName][0]->Fill(fillValue,wgt*theweight);
      }else if(isSig==0){
        theHistoMap[histoName][1]->Fill(fillValue,wgt*theweight);
      }
      if(SampleName.Contains("TTH")){
        theHistoMap[histoName][2]->Fill(fillValue,wgt*theweight);
      }
};
