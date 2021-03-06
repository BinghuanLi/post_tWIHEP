// Input : merged rootplas
// Function: copytrees and split higgs to different decay channels
// Output : rootplas ready for statistics study 
void copytree(TString InputDir, TString OutputDir, TString inputName, TString outputName, TString varName, Int_t HiggsFilter= 0){
 
    TString Input = InputDir + "/"+inputName+".root";
    TString Output = OutputDir  +"/"+outputName+".root";
    std::cout <<" inpupt file is " << Input << std::endl;
    std::cout <<" outpupt file is " << Output << std::endl;
    TString TreeName = "syncTree"+varName;
    TFile *oldfile = new TFile(Input);
    TTree *oldtree = (TTree*)oldfile->Get(TreeName);

    Long64_t nentries = oldtree->GetEntries(); 
    
    int HiggsDecay=0;
    float isWHfromVH=0.; 
    
    oldtree->SetBranchAddress("HiggsDecay", &HiggsDecay);
    oldtree->SetBranchAddress("isWHfromVH", &isWHfromVH);
    oldtree->SetBranchStatus("*", 1);

    TFile *newfile = new TFile(Output,"recreate");
    TTree *newtree = new TTree(TreeName,TreeName);

    newtree = oldtree->CloneTree(0);
    
    for (Long64_t i=0;i<nentries; i++) {
        oldtree->GetEntry(i);
        Bool_t passHiggsDecay = kTRUE;
        Bool_t passVHSplit = kTRUE;
        //if(HiggsFilter!=HiggsDecay )passHiggsDecay = kFALSE;//hzz,ww,tt,mm,zg
        if(HiggsFilter>0 && HiggsFilter<999 && HiggsFilter!=HiggsDecay )passHiggsDecay = kFALSE;//hzz,ww,tt,mm,zg
        if(HiggsFilter==999 && (HiggsDecay==2 || HiggsDecay==3 || HiggsDecay==6 || HiggsDecay==11 || HiggsDecay==7))passHiggsDecay = kFALSE; // hot
        if((inputName.Contains("WH_DiLepRegion") && isWHfromVH !=1) || (inputName.Contains("ZH_DiLepRegion") && isWHfromVH ==1)) passVHSplit = kFALSE;
    
        if(passHiggsDecay && passVHSplit) newtree->Fill();
        HiggsDecay =0;
    }

    newtree->SetName(TreeName);
    newtree->SetTitle(TreeName);
    //newtree->Write();
    newtree->AutoSave();
    //gDirectory->Delete("BOOM;*");
    
    delete oldfile;    
    delete newfile;
}

