// Input : 
// the output skim root file of tWIHEPFramework
// Output:
// rootplas for plotting and statistics study


#include "function.C"
#include "TTree.h"
#include "TFile.h"

// options
Bool_t _useReWeight = true; // set to true if we recalculate Global Weight.
Bool_t _useFakeRate = false; // set to true if we recalculate FakeRate Weighting.
Bool_t _useTrigSF = false; // set to true if we recalculate Trig SFs.
Bool_t _useHjVar = false; // set to true if we use Hjvar.
Bool_t _reWeight = false; // set to true if we want to reWeight some samples.

void Rootplas_TrainMVA(TString InputDir, TString OutputDir, TString FileName, TString Postfix){

    if(Postfix!="DiLepRegion" ){
        std::cout<< " ##################  ERROR ############ "<<std::endl;
        std::cout<< " Postfix must be DiLepRegion, please pass a correct Postfix "<< std::endl;
        return;
    }
    if(InputDir.Contains("TrainHj"))_useHjVar = true;
    TString Input = InputDir +"/"+ FileName + "Skim.root";
    TString Output = OutputDir  +"/"+FileName+ "_"+Postfix+".root";
    std::cout <<" inpupt file is " << Input << std::endl;
    std::cout <<" outpupt file is " << Output << std::endl;
    TFile *oldfile = new TFile(Input);
    TTree *oldtree = (TTree*)oldfile->Get("TNT/BOOM");


    Long64_t nentries = oldtree->GetEntries(); 
    
    std::vector<double>* EVENT_rWeights = 0;
    int HiggsDecay = 0;
    float cpodd_rwgt = 0;
    float fourthLep_isFromB = 0;
    float fourthLep_isFromC = 0;
    float fourthLep_isFromH = 0;
    float fourthLep_isFromTop = 0;
    float fourthLep_isFromZWH = 0;
    float fourthLep_isMatchRightCharge = 0;
    float fourthLep_mcMatchId = 0;
    float fourthLep_mcPromptFS = 0;
    float fourthLep_mcPromptGamma = 0;
    float isDiLepFake = 0;
    float isDiLepOS = 0;
    float isDiLepSR = 0;
    float isQuaLepFake = 0;
    float isQuaLepSR = 0;
    float isTriLepFake = 0;
    float isTriLepSR = 0;
    float isWZctrlFake = 0;
    float isWZctrlSR = 0;
    float isZZctrlFake = 0;
    float isZZctrlSR = 0;
    float is_tH_like_and_not_ttH_like = 0;
    float istHlikeDiLepFake = 0;
    float istHlikeDiLepOS = 0;
    float istHlikeDiLepSR = 0;
    float istHlikeQuaLepFake = 0;
    float istHlikeQuaLepSR = 0;
    float istHlikeTriLepFake = 0;
    float istHlikeTriLepSR = 0;
    float isttWctrlFake = 0;
    float isttWctrlOS = 0;
    float isttWctrlSR = 0;
    float isttZctrlFake = 0;
    float isttZctrlSR = 0;
    float leadLep_isFromB = 0;
    float leadLep_isFromC = 0;
    float leadLep_isFromH = 0;
    float leadLep_isFromTop = 0;
    float leadLep_isFromZWH = 0;
    float leadLep_isMatchRightCharge = 0;
    float leadLep_mcMatchId = 0;
    float leadLep_mcPromptFS = 0;
    float leadLep_mcPromptGamma = 0;
    int ls = 0;
    int nEvent = 0;
    int run = 0;
    float secondLep_isFromB = 0;
    float secondLep_isFromC = 0;
    float secondLep_isFromH = 0;
    float secondLep_isFromTop = 0;
    float secondLep_isFromZWH = 0;
    float secondLep_isMatchRightCharge = 0;
    float secondLep_mcMatchId = 0;
    float secondLep_mcPromptFS = 0;
    float secondLep_mcPromptGamma = 0;
    float thirdLep_isFromB = 0;
    float thirdLep_isFromC = 0;
    float thirdLep_isFromH = 0;
    float thirdLep_isFromTop = 0;
    float thirdLep_isFromZWH = 0;
    float thirdLep_isMatchRightCharge = 0;
    float thirdLep_mcMatchId = 0;
    float thirdLep_mcPromptFS = 0;
    float thirdLep_mcPromptGamma = 0;
    float xsec_rwgt = 0;
    float global_rwgt = 0;
    float EventWeight = 0;
    float DataEra = 0;
    
    oldtree->SetBranchAddress("EVENT_rWeights",&EVENT_rWeights);
    oldtree->SetBranchAddress("EventWeight",&EventWeight);
    oldtree->SetBranchAddress("DataEra",&DataEra);
    oldtree->SetBranchAddress("HiggsDecay",&HiggsDecay);
    oldtree->SetBranchAddress("fourthLep_isFromB",&fourthLep_isFromB);
    oldtree->SetBranchAddress("fourthLep_isFromC",&fourthLep_isFromC);
    oldtree->SetBranchAddress("fourthLep_isFromH",&fourthLep_isFromH);
    oldtree->SetBranchAddress("fourthLep_isFromTop",&fourthLep_isFromTop);
    oldtree->SetBranchAddress("fourthLep_isFromZWH",&fourthLep_isFromZWH);
    oldtree->SetBranchAddress("fourthLep_isMatchRightCharge",&fourthLep_isMatchRightCharge);
    oldtree->SetBranchAddress("fourthLep_mcMatchId",&fourthLep_mcMatchId);
    oldtree->SetBranchAddress("fourthLep_mcPromptFS",&fourthLep_mcPromptFS);
    oldtree->SetBranchAddress("fourthLep_mcPromptGamma",&fourthLep_mcPromptGamma);
    oldtree->SetBranchAddress("isDiLepFake",&isDiLepFake);
    oldtree->SetBranchAddress("isDiLepOS",&isDiLepOS);
    oldtree->SetBranchAddress("isDiLepSR",&isDiLepSR);
    oldtree->SetBranchAddress("isQuaLepFake",&isQuaLepFake);
    oldtree->SetBranchAddress("isQuaLepSR",&isQuaLepSR);
    oldtree->SetBranchAddress("isTriLepFake",&isTriLepFake);
    oldtree->SetBranchAddress("isTriLepSR",&isTriLepSR);
    oldtree->SetBranchAddress("isWZctrlFake",&isWZctrlFake);
    oldtree->SetBranchAddress("isWZctrlSR",&isWZctrlSR);
    oldtree->SetBranchAddress("isZZctrlFake",&isZZctrlFake);
    oldtree->SetBranchAddress("isZZctrlSR",&isZZctrlSR);
    oldtree->SetBranchAddress("istHlikeDiLepFake",&istHlikeDiLepFake);
    oldtree->SetBranchAddress("istHlikeDiLepOS",&istHlikeDiLepOS);
    oldtree->SetBranchAddress("istHlikeDiLepSR",&istHlikeDiLepSR);
    oldtree->SetBranchAddress("istHlikeQuaLepFake",&istHlikeQuaLepFake);
    oldtree->SetBranchAddress("istHlikeQuaLepSR",&istHlikeQuaLepSR);
    oldtree->SetBranchAddress("istHlikeTriLepFake",&istHlikeTriLepFake);
    oldtree->SetBranchAddress("istHlikeTriLepSR",&istHlikeTriLepSR);
    oldtree->SetBranchAddress("isttWctrlFake",&isttWctrlFake);
    oldtree->SetBranchAddress("isttWctrlOS",&isttWctrlOS);
    oldtree->SetBranchAddress("isttWctrlSR",&isttWctrlSR);
    oldtree->SetBranchAddress("isttZctrlFake",&isttZctrlFake);
    oldtree->SetBranchAddress("isttZctrlSR",&isttZctrlSR);
    oldtree->SetBranchAddress("leadLep_isFromB",&leadLep_isFromB);
    oldtree->SetBranchAddress("leadLep_isFromC",&leadLep_isFromC);
    oldtree->SetBranchAddress("leadLep_isFromH",&leadLep_isFromH);
    oldtree->SetBranchAddress("leadLep_isFromTop",&leadLep_isFromTop);
    oldtree->SetBranchAddress("leadLep_isFromZWH",&leadLep_isFromZWH);
    oldtree->SetBranchAddress("leadLep_isMatchRightCharge",&leadLep_isMatchRightCharge);
    oldtree->SetBranchAddress("leadLep_mcMatchId",&leadLep_mcMatchId);
    oldtree->SetBranchAddress("leadLep_mcPromptFS",&leadLep_mcPromptFS);
    oldtree->SetBranchAddress("leadLep_mcPromptGamma",&leadLep_mcPromptGamma);
    oldtree->SetBranchAddress("ls",&ls);
    oldtree->SetBranchAddress("nEvent",&nEvent);
    oldtree->SetBranchAddress("run",&run);
    oldtree->SetBranchAddress("secondLep_isFromB",&secondLep_isFromB);
    oldtree->SetBranchAddress("secondLep_isFromC",&secondLep_isFromC);
    oldtree->SetBranchAddress("secondLep_isFromH",&secondLep_isFromH);
    oldtree->SetBranchAddress("secondLep_isFromTop",&secondLep_isFromTop);
    oldtree->SetBranchAddress("secondLep_isFromZWH",&secondLep_isFromZWH);
    oldtree->SetBranchAddress("secondLep_isMatchRightCharge",&secondLep_isMatchRightCharge);
    oldtree->SetBranchAddress("secondLep_mcMatchId",&secondLep_mcMatchId);
    oldtree->SetBranchAddress("secondLep_mcPromptFS",&secondLep_mcPromptFS);
    oldtree->SetBranchAddress("secondLep_mcPromptGamma",&secondLep_mcPromptGamma);
    oldtree->SetBranchAddress("thirdLep_isFromB",&thirdLep_isFromB);
    oldtree->SetBranchAddress("thirdLep_isFromC",&thirdLep_isFromC);
    oldtree->SetBranchAddress("thirdLep_isFromH",&thirdLep_isFromH);
    oldtree->SetBranchAddress("thirdLep_isFromTop",&thirdLep_isFromTop);
    oldtree->SetBranchAddress("thirdLep_isFromZWH",&thirdLep_isFromZWH);
    oldtree->SetBranchAddress("thirdLep_isMatchRightCharge",&thirdLep_isMatchRightCharge);
    oldtree->SetBranchAddress("thirdLep_mcMatchId",&thirdLep_mcMatchId);
    oldtree->SetBranchAddress("thirdLep_mcPromptFS",&thirdLep_mcPromptFS);
    oldtree->SetBranchAddress("thirdLep_mcPromptGamma",&thirdLep_mcPromptGamma);

    SetOldTreeBranchStatus(oldtree, _useHjVar);
   
    TFile *newfile = new TFile(Output,"recreate");
    TString TreeName = "syncTree";
    TTree *newtree = new TTree(TreeName,TreeName);

    newtree = oldtree->CloneTree(0);
    newtree->Branch("cpodd_rwgt",&cpodd_rwgt);
    newtree->Branch("is_tH_like_and_not_ttH_like",&is_tH_like_and_not_ttH_like);
    newtree->Branch("xsec_rwgt",&xsec_rwgt);
    newtree->Branch("global_rwgt",&global_rwgt);
    
    
    std::map<std::string,double> inputs;
    
    for (Long64_t i=0;i<nentries; i++) {
        EVENT_rWeights->clear();
        HiggsDecay = -9;
        cpodd_rwgt = 1;
        fourthLep_isFromB = -9;
        fourthLep_isFromC = -9;
        fourthLep_isFromH = -9;
        fourthLep_isFromTop = -9;
        fourthLep_isFromZWH = -9;
        fourthLep_isMatchRightCharge = -9;
        fourthLep_mcMatchId = -9;
        fourthLep_mcPromptFS = -9;
        fourthLep_mcPromptGamma = -9;
        isDiLepFake = -9;
        isDiLepOS = -9;
        isDiLepSR = -9;
        isQuaLepFake = -9;
        isQuaLepSR = -9;
        isTriLepFake = -9;
        isTriLepSR = -9;
        isWZctrlFake = -9;
        isWZctrlSR = -9;
        isZZctrlFake = -9;
        isZZctrlSR = -9;
        is_tH_like_and_not_ttH_like = -9;
        istHlikeDiLepFake = -9;
        istHlikeDiLepOS = -9;
        istHlikeDiLepSR = -9;
        istHlikeQuaLepFake = -9;
        istHlikeQuaLepSR = -9;
        istHlikeTriLepFake = -9;
        istHlikeTriLepSR = -9;
        isttWctrlFake = -9;
        isttWctrlOS = -9;
        isttWctrlSR = -9;
        isttZctrlFake = -9;
        isttZctrlSR = -9;
        leadLep_isFromB = -9;
        leadLep_isFromC = -9;
        leadLep_isFromH = -9;
        leadLep_isFromTop = -9;
        leadLep_isFromZWH = -9;
        leadLep_isMatchRightCharge = -9;
        leadLep_mcMatchId = -9;
        leadLep_mcPromptFS = -9;
        leadLep_mcPromptGamma = -9;
        ls = -9;
        nEvent = -9;
        run = -9;
        secondLep_isFromB = -9;
        secondLep_isFromC = -9;
        secondLep_isFromH = -9;
        secondLep_isFromTop = -9;
        secondLep_isFromZWH = -9;
        secondLep_isMatchRightCharge = -9;
        secondLep_mcMatchId = -9;
        secondLep_mcPromptFS = -9;
        secondLep_mcPromptGamma = -9;
        thirdLep_isFromB = -9;
        thirdLep_isFromC = -9;
        thirdLep_isFromH = -9;
        thirdLep_isFromTop = -9;
        thirdLep_isFromZWH = -9;
        thirdLep_isMatchRightCharge = -9;
        thirdLep_mcMatchId = -9;
        thirdLep_mcPromptFS = -9;
        thirdLep_mcPromptGamma = -9;
        xsec_rwgt = 1;
        global_rwgt = 1;
        EventWeight = 1;
        DataEra = -9;
        oldtree->GetEntry(i);
        Bool_t passCut = kFALSE;
        Bool_t passTH = kTRUE;
        is_tH_like_and_not_ttH_like = (istHlikeDiLepSR==1 && isDiLepSR!=1 && isttWctrlSR!=1) ? 1:0;
        passCut = ((istHlikeDiLepSR==1 || isDiLepSR==1 || isttWctrlSR==1 )); 
        if(DataEra == 2018 && nEvent % 3 == 0 && (FileName.Contains("THW") || FileName.Contains("THQ"))) passTH = kFALSE; // 1/3 for signal extraction
        if(passCut && passTH){
            if(_reWeight){
                if(oldtree->GetListOfBranches()->FindObject("EVENT_rWeights") && EVENT_rWeights->size()>=12 && FileName.Contains("ctcvcp")){
                    xsec_rwgt = get_rewgtlumi(FileName, EVENT_rWeights->at(11));
                }
                else{
                    xsec_rwgt = get_rewgtlumi(FileName, 1);
                }
                EventWeight = EventWeight * xsec_rwgt;
            }
            if(_useReWeight){
                global_rwgt = get_rwgtGlobal(FileName, DataEra, true);
                EventWeight = EventWeight * global_rwgt;
            }
            
            newtree->Fill();
        }
    }

    newtree->SetName(TreeName);
    newtree->SetTitle(TreeName);
    //newtree->Write();
    newtree->AutoSave();
    gDirectory->Delete("BOOM;*");
   
    
    delete oldfile;    
    delete newfile;
}

