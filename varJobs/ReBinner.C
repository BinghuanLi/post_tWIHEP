// Input : rootplas with DNN maxval and DNN Cat Flag
// Function: copytrees and add channel flags, add BinOptimized Histograms
// Output : rootplas ready for statistics study and histograms for Optimized Binning 
//#include "Maps.C"
#include "Maps_5nodes.C"

std::vector<TString> samplesAll = {"Rares","WW","WZ","Convs","TTW","TTZ","TTWW","Fakes","FakeSub","Flips","TTH_htt","TTH_hww","TTH_hzz","TTH_hzg","TTH_hmm","THQ_htt","THQ_hww","THQ_hzz","THW_htt","THW_hww","THW_hzz","Data"};
//std::vector<TString> samplesAll = {"Data"};
std::vector<TString> samplesJES = {"WW","WZ","Rares","Convs","TTW","TTZ","TTWW","TTH_htt","TTH_hww","TTH_hzz","TTH_hzg","TTH_hmm","THQ_htt","THQ_hww","THQ_hzz","THW_htt","THW_hww","THW_hzz","FakeSub"};
// SubCatNames should be mapped to VarNames 1 to 1
//std::vector<TString> SubCatNames = {"DNNCat","DNNCat_option2","DNNCat_option3","DNNSubCat1_option1","DNNSubCat1_option2","DNNSubCat1_option3","DNNSubCat2_option1","DNNSubCat2_option2","DNNSubCat2_option3","DNNAMS2Cat1_option1","DNNAMS2Cat1_option2","DNNAMS2Cat1_option3","DNNAMS3Cat1_option1","DNNAMS3Cat1_option2","DNNAMS3Cat1_option3"};
//std::vector<TString> VarNames = {"DNN_maxval","DNN_maxval_option2","DNN_maxval_option3","DNN_maxval","DNN_maxval_option2","DNN_maxval_option3","DNN_maxval","DNN_maxval_option2","DNN_maxval_option3","DNN_maxval","DNN_maxval_option2","DNN_maxval_option3","DNN_maxval","DNN_maxval_option2","DNN_maxval_option3"};
std::vector<TString> SubCatNames = {"DNNCat","DNNSubCat1_option1","DNNSubCat2_option1"};
std::vector<TString> VarNames = {"DNN_maxval","DNN_maxval","DNN_maxval"};
std::map<TString,std::vector<TH1F*>> theHistoMap;
TString RegName;

void createHists();
void fillHists(TString SampleName, TString SubCatName, TString VarName, Int_t theChannel, float var, float theweight, Bool_t SigDNN);

void ReBinner(TString InputDir, TString OutputDir, TString RegionName , Bool_t DNNSig = true, Bool_t OptBin=true){
    TString BinDataDir = "BinData_SigDNN"; 
    if (!DNNSig) BinDataDir = "BinData_SigTTH";
    if(RegionName.Contains("ttWctrl")){
        RegName = "ttWctrl";
    }else if(RegionName.Contains("SigRegion")){
        RegName = "SigRegion";
    }else if(RegionName.Contains("DiLepRegion")){
        RegName = "DiLepRegion";
    }else{
        std::cout<< "ERROR: RegionName is "<<RegionName<< " RegionName must contains ttWctrl/DiLepRegion or SigRegion "<<std::endl;
        return;
    }
    TString BinRootFile = OutputDir +"/"+BinDataDir+"/OptBin_"+RegionName+".root";
    std::vector<TString> samples;
    if(RegionName.Contains("JES")){
        OptBin = false;
        samples = samplesJES;
    }else{
        samples = samplesAll;
    }
    TFile *newBinFile;
    if(OptBin){
        newBinFile = new TFile(BinRootFile,"recreate");
        createHists();
    }
  
    TString MapRegionName = RegionName;
    MapRegionName.ReplaceAll("JESUp",""); 
    MapRegionName.ReplaceAll("JESDown",""); 
    
    for(auto s : samples){
        TString Input = InputDir + "/"+RegionName+"/"+s + "_"+RegionName+".root";
        TString Output = OutputDir + "/"+RegionName+"/"+s + "_"+RegionName+".root";
        std::cout <<" input file is " << Input << std::endl;
        std::cout <<" output file is " << Output << std::endl;
        TFile *oldfile = new TFile(Input);
        if(oldfile->IsZombie()){
            std::cout << " Input deosn't exist " <<std::endl;
            continue; 
        }
        TTree *oldtree = (TTree*)oldfile->Get("syncTree");

        Long64_t nentries = oldtree->GetEntries(); 
        float is_tH_like_and_not_ttH_like=0;
        float DNNCat=0;
        float DNNSubCat1_option1=0;
        float DNNSubCat2_option1=0;
        float DNN_maxval=0;
        float DNN_ttHnode_all=0.;
        float DNN_ttJnode_all=0.;
        float DNN_ttWnode_all=0.;
        float DNN_ttZnode_all=0.;
        float DNN_tHQnode_all=0.;
        float EventWeight(0.); 
        
        oldtree->SetBranchAddress("EventWeight", &EventWeight);
        oldtree->SetBranchAddress("is_tH_like_and_not_ttH_like", &is_tH_like_and_not_ttH_like);
        oldtree->SetBranchAddress("DNNCat", &DNNCat);
        oldtree->SetBranchAddress("DNNSubCat1_option1", &DNNSubCat1_option1);
        oldtree->SetBranchAddress("DNNSubCat2_option1", &DNNSubCat2_option1);
        oldtree->SetBranchAddress("DNN_maxval", &DNN_maxval);
        oldtree->SetBranchAddress("DNN_ttHnode_all", &DNN_ttHnode_all);
        oldtree->SetBranchAddress("DNN_ttJnode_all", &DNN_ttJnode_all);
        oldtree->SetBranchAddress("DNN_ttWnode_all", &DNN_ttWnode_all);
        oldtree->SetBranchAddress("DNN_ttZnode_all", &DNN_ttZnode_all);
        oldtree->SetBranchAddress("DNN_tHQnode_all", &DNN_tHQnode_all);
        oldtree->SetBranchStatus("*", 1);
    

        
        std::cout << " loop over entries in sample "<< s <<std::endl;
        for (Long64_t i=0;i<nentries; i++) {
            EventWeight=0;
            is_tH_like_and_not_ttH_like=0;
            DNNCat=0;
            DNNSubCat1_option1=0;
            DNNSubCat2_option1=0;
            DNN_maxval=0;
            DNN_ttHnode_all=0;
            DNN_ttJnode_all=0;
            DNN_ttWnode_all=0;
            DNN_ttZnode_all=0;
            DNN_tHQnode_all=0;
            oldtree->GetEntry(i);
            //if(is_tH_like_and_not_ttH_like==1) continue;
            if(OptBin){
                fillHists(s, "DNNCat" , "DNN_maxval", DNNCat, DNN_maxval, EventWeight, DNNSig);
                fillHists(s, "DNNSubCat1_option1" , "DNN_maxval", DNNSubCat1_option1, DNN_maxval, EventWeight, DNNSig);
                fillHists(s, "DNNSubCat2_option1" , "DNN_maxval", DNNSubCat2_option1, DNN_maxval, EventWeight, DNNSig);
            }
        }
        std::cout << " end of loop over entries in sample "<< s <<std::endl;
         
        delete oldfile;    
    }
    std::cout << " end of sample loop " <<std::endl;
    if(OptBin){
        std::cout << " save bin file " <<std::endl;
        newBinFile->cd();
        for (auto histoMapElement: theHistoMap){
            for (auto hist:histoMapElement.second) hist->Write();
        }
        delete newBinFile;
    }
}

void createHists(){
    for(unsigned int i=0; i < SubCatNames.size(); i++){
        int nbins =1;
        double xmin = -1000;
        double xmax = 1000;
        TString varName = VarNames.at(i);
        TString subCatName = SubCatNames.at(i); 
        // smaller bins for quantiles
        if(varName== "DNN_maxval") {nbins= 100; xmin= 0; xmax= 1;};
        if(varName== "DNN_maxval_option2") {nbins= 100; xmin= 0; xmax= 1;};
        if(varName== "DNN_maxval_option3") {nbins= 100; xmin= 0; xmax= 1;};
        std::map<Int_t, TString>::iterator it;
        for(it = MapOfChannelMap[subCatName].begin(); it!=MapOfChannelMap[subCatName].end(); it++){
            TString subChannel = it->second;
            if(subChannel=="inclusive")continue;
            if(subChannel.Contains("loose_ttHnode")){
                xmin=0;
                if(AMS_MapOfCuts[subCatName]["ttHnode_"+RegName]>0){
                    xmax=AMS_MapOfCuts[subCatName]["ttHnode_"+RegName];
                }else{
                    xmax = 0.5;
                }
            }else if(subChannel.Contains("tight_ttHnode")){
                xmax=1;
                if(AMS_MapOfCuts[subCatName]["ttHnode_"+RegName]>0){
                    xmin=AMS_MapOfCuts[subCatName]["ttHnode_"+RegName];
                }else{
                    xmin=0.5;
                }
            }
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

void fillHists(TString SampleName, TString SubCatName, TString VarName, Int_t theChannel, float var, float theweight, Bool_t SigDNN){
      if(theChannel==0) return;
      int isSig = -1;
      int wgt = 1;
      if(SampleName.Contains("FakeSub"))wgt=-1;
      // normal case of Sig Bkg
      if(SampleName.Contains("TTH"))isSig=1;
      else if(SampleName.Contains("TTW") || SampleName.Contains("TTZ") || SampleName.Contains("Fakes") || SampleName.Contains("FakeSub") || SampleName.Contains("Flip") || SampleName.Contains("Convs") || SampleName.Contains("THQ") || SampleName.Contains("THW"))isSig=0;
      // Sig Bkg according to DNN
      TString histoName = SubCatName+"_"+VarName+"_"+MapOfChannelMap[SubCatName][theChannel];
      if(histoName.Contains("ttJnode") && SigDNN){
        if(SampleName.Contains("Fakes") || SampleName.Contains("FakeSub") || SampleName.Contains("Flip") || SampleName.Contains("Convs"))isSig=1;
        else if(SampleName.Contains("TTW") || SampleName.Contains("TTZ") || SampleName.Contains("TTH") || SampleName.Contains("THQ") || SampleName.Contains("THW") )isSig=0;
      }else if(histoName.Contains("ttWnode") && SigDNN){
        if(SampleName.Contains("TTW"))isSig=1;
        else if(SampleName.Contains("TTH") || SampleName.Contains("TTZ") || SampleName.Contains("Fakes") || SampleName.Contains("FakeSub") || SampleName.Contains("Flip") || SampleName.Contains("Convs") || SampleName.Contains("THQ") || SampleName.Contains("THW"))isSig=0;
      }else if(histoName.Contains("ttZnode") && SigDNN){
        if(SampleName.Contains("TTZ"))isSig=1;
        else if(SampleName.Contains("TTH") || SampleName.Contains("TTW") || SampleName.Contains("Fakes") || SampleName.Contains("FakeSub") || SampleName.Contains("Flip") || SampleName.Contains("Convs") || SampleName.Contains("THQ") || SampleName.Contains("THW"))isSig=0;
      }else if(histoName.Contains("tHnode") && SigDNN && ! histoName.Contains("ttHnode")){
        if(SampleName.Contains("THQ") || SampleName.Contains("THW"))isSig=1;
        else if(SampleName.Contains("TTH") || SampleName.Contains("TTW") || SampleName.Contains("Fakes") || SampleName.Contains("FakeSub") || SampleName.Contains("Flip") || SampleName.Contains("Convs"))isSig=0;
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

