// Input : 
// the output skim root file of tWIHEPFramework
// Output:
// rootplas for plotting and statistics study


#include "function.C"
#include "TTree.h"
#include "TFile.h"
#include "mvaTool/Maps.C"

// options
Bool_t _checkPU = true; // set to true if we call checkPU() cut 
Bool_t _useReWeight = true; // set to true if we recalculate Global Weight.
Bool_t _useFakeRate = false; // set to true if we recalculate FakeRate Weighting.
Bool_t _useTrigSF = false; // set to true if we recalculate Trig SFs.
Bool_t _useHjVar = false; // set to true if we use Hjvar.
Bool_t _reWeight = false; // set to true if we want to reWeight some samples.
Bool_t _saveWeight = true; // set to true if we want to reWeight some samples.
Bool_t _useNNBins = true; // set to true if we want to BIN NN distribution.

std::vector<int> _bins = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19};
// NN bins
std::map<TString,TH1F*> _DNNSubCat2NNMapHists;
TString DNNSubCat2_FileName = "DNN_BIN";
std::vector<TString> _DNNSubCat2Maps = {"ee_ttHnode","ee_Restnode","ee_ttWnode","ee_tHQnode","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"};
std::map<TString, float> _DNNSubCat2BinNames;

std::map<TString,TH1F*> _DNNSubCat2_option2NNMapHists;
TString DNNSubCat2_option2_FileName = "DNNBin_v3_xmas";
std::vector<TString> _DNNSubCat2_option2Maps = {"ee_ttHnode","ee_Restnode","ee_ttWnode","ee_tHQnode","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"};
std::map<TString, float> _DNNSubCat2_option2BinNames;


void Rootplas_LegacyAll(TString InputDir, TString OutputDir, TString FileName, TString Region, TString PostFix, TString varName){
    
    if(PostFix!="DiLepRegion" && PostFix!="TriLepRegion" && PostFix!="QuaLepRegion" && PostFix !="ttZctrl" && PostFix != "WZctrl" && PostFix != "ZZctrl"){
        std::cout<< " ##################  ERROR ############ "<<std::endl;
        std::cout<< " PostFix must be DiLepRegion, TriLepRegion, ttZctrl, WZctrl, QuaLepRegion, ZZctrl, please pass a correct PostFix "<< std::endl;
        exit(0);
    }else if(Region!="datafakes" && Region!="dataflips" && Region != "prompt" && Region != "mcfakes" && Region != "mcflips" && Region != "fakesub" && Region != "dataobs" && Region!="conv"){
        std::cout<< " ##################  ERROR ############ "<<std::endl;
        std::cout<< " Region must be datafakes, dataflips, prompt, mcfakes, mcflips, fakesub, dataobs, conv, please pass a correct Region "<< std::endl;
        exit(0);
    }else if(PostFix!="DiLepRegion" && (Region == "dataflips" || Region == "mcflips" )){
        std::cout<< " ##################  ERROR ############ "<<std::endl;
        std::cout<< " Region must not be dataflips and mcflips if PostFix is DiLepRegion, please pass a correct Region "<< std::endl;
        exit(0);
    }

    // NN bins
    if(_useNNBins){
        // DNNSubCat2
        TString CatFlag = "DNNSubCat2";
        for(auto const category: _DNNSubCat2Maps){
            for(auto const bin: _bins){
                setDNNBinHistograms(input_DNNBin_path, DNNSubCat2_FileName, category+"_2018", _DNNSubCat2NNMapHists, bin);
                _DNNSubCat2BinNames[CatFlag+"_"+category+"_nBin"+std::to_string(bin)] = 0.;
            }
        }
        // DNNSubCat2_option2
        for(auto const category: _DNNSubCat2_option2Maps){
            for(auto const bin: _bins){
                setDNNBinHistograms(input_DNNBin_path, DNNSubCat2_option2_FileName, category+"_2018", _DNNSubCat2_option2NNMapHists, bin);
                _DNNSubCat2_option2BinNames[CatFlag+"_option2_"+category+"_nBin"+std::to_string(bin)] = 0.;
            }
        }
    }
    
    if(InputDir.Contains("TrainHj"))_useHjVar = true;
    TString Input = InputDir +"/"+ FileName + "Skim.root";
    TString Output = OutputDir  +"/"+FileName+ "_"+ Region +"_"+PostFix+".root";
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
    double trueInteractions = 0;
    // nn vars
    float Dilep_pdgId = 0;
    float Hj_tagger_hadTop = 0;
    float avg_dr_jet = 0;
    float jet1_eta = 0;
    float jet1_phi = 0;
    float jet1_pt = 0;
    float jet2_eta = 0;
    float jet2_phi = 0;
    float jet2_pt = 0;
    float jet3_eta = 0;
    float jet3_phi = 0;
    float jet3_pt = 0;
    float jet4_eta = 0;
    float jet4_phi = 0;
    float jet4_pt = 0;
    float jetFwd1_eta = 0;
    float jetFwd1_pt = 0;
    float lep1_charge = 0;
    float lep1_conePt = 0;
    float lep1_eta = 0;
    float lep1_phi = 0;
    float lep2_conePt = 0;
    float lep2_eta = 0;
    float lep2_phi = 0;
    float mT_lep1 = 0;
    float mT_lep2 = 0;
    float mass_dilep = 0;
    float mT2_top_2particle = 0;
    float min_Deta_leadfwdJet_jet = 0;
    float min_Deta_mostfwdJet_jet = 0;
    float maxeta = 0;
    float mbb = 0;
    float metLD = 0;
    float mindr_lep1_jet = 0;
    float mindr_lep2_jet = 0;
    float nBJetLoose = 0;
    float nBJetMedium = 0;
    float n_presel_jet = 0;
    float n_presel_jetFwd = 0;
    float hadTop_BDT = 0;
    float DNNCat = 0;
    float DNNSubCat1_option1 = 0;
    float DNNSubCat2_option1 = 0;
    float DNN_Restnode_all = 0;
    float DNN_maxval = 0;
    float DNN_tHQnode_all = 0;
    float DNN_ttHnode_all = 0;
    float DNN_ttWnode_all = 0;
    
    float DNNCat_option2 = 0;
    float DNNSubCat1_option2 = 0;
    float DNNSubCat2_option2 = 0;
    float DNN_Restnode_all_option2 = 0;
    float DNN_maxval_option2 = 0;
    float DNN_tHQnode_all_option2 = 0;
    float DNN_ttHnode_all_option2 = 0;
    float DNN_ttWnode_all_option2 = 0;
    
    /////// cut vars

    oldtree->SetBranchAddress("EVENT_rWeights",&EVENT_rWeights);
    oldtree->SetBranchAddress("EventWeight",&EventWeight);
    oldtree->SetBranchAddress("DataEra",&DataEra);
    oldtree->SetBranchAddress("trueInteractions",&trueInteractions);
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

    // nn vars
    oldtree->SetBranchAddress("Dilep_pdgId",&Dilep_pdgId);
    oldtree->SetBranchAddress("Hj_tagger_hadTop",&Hj_tagger_hadTop);
    oldtree->SetBranchAddress("avg_dr_jet",&avg_dr_jet);
    oldtree->SetBranchAddress("jet1_eta",&jet1_eta);
    oldtree->SetBranchAddress("jet1_phi",&jet1_phi);
    oldtree->SetBranchAddress("jet1_pt",&jet1_pt);
    oldtree->SetBranchAddress("jet2_eta",&jet2_eta);
    oldtree->SetBranchAddress("jet2_phi",&jet2_phi);
    oldtree->SetBranchAddress("jet2_pt",&jet2_pt);
    oldtree->SetBranchAddress("jet3_eta",&jet3_eta);
    oldtree->SetBranchAddress("jet3_phi",&jet3_phi);
    oldtree->SetBranchAddress("jet3_pt",&jet3_pt);
    oldtree->SetBranchAddress("jet4_eta",&jet4_eta);
    oldtree->SetBranchAddress("jet4_phi",&jet4_phi);
    oldtree->SetBranchAddress("jet4_pt",&jet4_pt);
    oldtree->SetBranchAddress("jetFwd1_eta",&jetFwd1_eta);
    oldtree->SetBranchAddress("jetFwd1_pt",&jetFwd1_pt);
    oldtree->SetBranchAddress("lep1_charge",&lep1_charge);
    oldtree->SetBranchAddress("lep1_conePt",&lep1_conePt);
    oldtree->SetBranchAddress("lep1_eta",&lep1_eta);
    oldtree->SetBranchAddress("lep1_phi",&lep1_phi);
    oldtree->SetBranchAddress("lep2_conePt",&lep2_conePt);
    oldtree->SetBranchAddress("lep2_eta",&lep2_eta);
    oldtree->SetBranchAddress("lep2_phi",&lep2_phi);
    oldtree->SetBranchAddress("mT_lep1",&mT_lep1);
    oldtree->SetBranchAddress("mT_lep2",&mT_lep2);
    oldtree->SetBranchAddress("mass_dilep",&mass_dilep);
    oldtree->SetBranchAddress("min_Deta_mostfwdJet_jet",&min_Deta_mostfwdJet_jet);
    oldtree->SetBranchAddress("min_Deta_leadfwdJet_jet",&min_Deta_leadfwdJet_jet);
    oldtree->SetBranchAddress("mT2_top_2particle",&mT2_top_2particle);
    oldtree->SetBranchAddress("maxeta",&maxeta);
    oldtree->SetBranchAddress("mbb",&mbb);
    oldtree->SetBranchAddress("metLD",&metLD);
    oldtree->SetBranchAddress("mindr_lep1_jet",&mindr_lep1_jet);
    oldtree->SetBranchAddress("mindr_lep2_jet",&mindr_lep2_jet);
    oldtree->SetBranchAddress("nBJetLoose",&nBJetLoose);
    oldtree->SetBranchAddress("nBJetMedium",&nBJetMedium);
    oldtree->SetBranchAddress("n_presel_jet",&n_presel_jet);
    oldtree->SetBranchAddress("n_presel_jetFwd",&n_presel_jetFwd);
    oldtree->SetBranchAddress("hadTop_BDT",&hadTop_BDT);
    
    SetOldTreeBranchStatus(oldtree, _useHjVar);
   
    TFile *newfile = new TFile(Output,"recreate");
    TString TreeName = "syncTree"+varName;
    TTree *newtree = new TTree(TreeName,TreeName);

    newtree = oldtree->CloneTree(0);
    newtree->Branch("cpodd_rwgt",&cpodd_rwgt);
    newtree->Branch("is_tH_like_and_not_ttH_like",&is_tH_like_and_not_ttH_like);
    newtree->Branch("xsec_rwgt",&xsec_rwgt);
    newtree->Branch("global_rwgt",&global_rwgt);
    
    // nn vars 
    // nn instance 1 
    newtree->Branch("DNNCat",&DNNCat);
    newtree->Branch("DNNSubCat1_option1",&DNNSubCat1_option1);
    newtree->Branch("DNNSubCat2_option1",&DNNSubCat2_option1);
    newtree->Branch("DNN_Restnode_all",&DNN_Restnode_all);
    newtree->Branch("DNN_maxval",&DNN_maxval);
    newtree->Branch("DNN_tHQnode_all",&DNN_tHQnode_all);
    newtree->Branch("DNN_ttHnode_all",&DNN_ttHnode_all);
    newtree->Branch("DNN_ttWnode_all",&DNN_ttWnode_all);
    
    // nn instance 2 
    newtree->Branch("DNNCat_option2",&DNNCat_option2);
    newtree->Branch("DNNSubCat1_option2",&DNNSubCat1_option2);
    newtree->Branch("DNNSubCat2_option2",&DNNSubCat2_option2);
    newtree->Branch("DNN_Restnode_all_option2",&DNN_Restnode_all_option2);
    newtree->Branch("DNN_maxval_option2",&DNN_maxval_option2);
    newtree->Branch("DNN_tHQnode_all_option2",&DNN_tHQnode_all_option2);
    newtree->Branch("DNN_ttHnode_all_option2",&DNN_ttHnode_all_option2);
    newtree->Branch("DNN_ttWnode_all_option2",&DNN_ttWnode_all_option2);
    
    
    float DNNSubCat2_BIN = 0;
    float DNNSubCat2_option2_BIN = 0;
    // NN bins
    if(_useNNBins){
        // _DNNSubCat2BinNames
        newtree -> Branch("DNNSubCat2_BIN", &DNNSubCat2_BIN);
        for (auto& x : _DNNSubCat2BinNames){
            newtree->Branch( x.first.Data(), &(x.second));
        }
        // _DNNSubCat2_option2BinNames
        newtree -> Branch("DNNSubCat2_option2_BIN", &DNNSubCat2_option2_BIN);
        for (auto& x : _DNNSubCat2_option2BinNames){
            newtree->Branch( x.first.Data(), &(x.second));
        }
    }
    
    
    // nn setup
    // nn instance 1
    std::map<std::string,double> inputs;
    create_lwtnn(input_json_file, nn_instance);
    
    // nn instance 2
    std::map<std::string,double> inputs_newvars;
    create_lwtnn(input_json_file_newvars, nn_instance_newvars);
    
    std::cout<<" input nentires: " << nentries << std::endl; 
    for (Long64_t i=0;i<nentries; i++) {
    //for (Long64_t i=0;i<10; i++) {
        /*
        if ( int(i) % 10000==0){
            std::cout << " finish events : " << i << std::endl;
        }
        */
        if(_useNNBins){
            DNNSubCat2_BIN = 0.;
            for (auto& x : _DNNSubCat2BinNames){
                x.second = -1;
            }
            DNNSubCat2_option2_BIN = 0.;
            for (auto& x : _DNNSubCat2_option2BinNames){
                x.second = -1;
            }
        }
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
        trueInteractions = -9;
        // nn vars
        Dilep_pdgId = -9;
        Hj_tagger_hadTop = -9;
        avg_dr_jet = -9;
        jet1_eta = -9;
        jet1_phi = -9;
        jet1_pt = -9;
        jet2_eta = -9;
        jet2_phi = -9;
        jet2_pt = -9;
        jet3_eta = -9;
        jet3_phi = -9;
        jet3_pt = -9;
        jet4_eta = -9;
        jet4_phi = -9;
        jet4_pt = -9;
        jetFwd1_eta = -9;
        jetFwd1_pt = -9;
        lep1_charge = -9;
        lep1_conePt = -9;
        lep1_eta = -9;
        lep1_phi = -9;
        lep2_conePt = -9;
        lep2_eta = -9;
        lep2_phi = -9;
        mT_lep1 = -9;
        mT_lep2 = -9;
        mass_dilep = -9;
        min_Deta_leadfwdJet_jet = -9;
        mT2_top_2particle = -9;
        min_Deta_mostfwdJet_jet = -9;
        maxeta = -9;
        mbb = -9;
        metLD = -9;
        mindr_lep1_jet = -9;
        mindr_lep2_jet = -9;
        nBJetLoose = -9;
        nBJetMedium = -9;
        n_presel_jet = -9;
        n_presel_jetFwd = -9;
        hadTop_BDT = -9;
        DNNCat = -9;
        DNNSubCat1_option1 = -9;
        DNNSubCat2_option1 = -9;
        DNN_Restnode_all = -9;
        DNN_maxval = -9;
        DNN_tHQnode_all = -9;
        DNN_ttHnode_all = -9;
        DNN_ttWnode_all = -9;
        DNNCat_option2 = -9;
        DNNSubCat1_option2 = -9;
        DNNSubCat2_option2 = -9;
        DNN_Restnode_all_option2 = -9;
        DNN_maxval_option2 = -9;
        DNN_tHQnode_all_option2 = -9;
        DNN_ttHnode_all_option2 = -9;
        DNN_ttWnode_all_option2 = -9;
        oldtree->GetEntry(i);
        Bool_t passCut = kFALSE;
        Bool_t passPU = kTRUE;
        Bool_t passTH = kTRUE;
        if(_checkPU){
            passPU = checkPU(trueInteractions, DataEra);    
        }
        if(DataEra == 2018 && nEvent % 3 != 0 && (FileName.Contains("THQ"))) passTH = kFALSE; // 1/3 for signal extraction
        is_tH_like_and_not_ttH_like = ( istHlikeDiLepSR==1 && isDiLepSR!=1 && isttWctrlSR!=1 ) ? 1:0;
        // DiLepRegion
        if(Region=="prompt" && PostFix=="DiLepRegion"){
            is_tH_like_and_not_ttH_like = ( istHlikeDiLepSR==1 && isDiLepSR!=1 && isttWctrlSR!=1 ) ? 1:0;
            passCut = ( ( istHlikeDiLepSR==1 || isDiLepSR==1 || isttWctrlSR==1 )
                && (fabs(leadLep_mcMatchId)==13 || fabs(leadLep_mcMatchId)==11)
                && (fabs(secondLep_mcMatchId)==13 || fabs(secondLep_mcMatchId)==11)
                && (leadLep_mcPromptFS==1 && leadLep_isMatchRightCharge==1)
                && (secondLep_mcPromptFS==1 && secondLep_isMatchRightCharge==1)
                );
        }else if(Region=="mcfakes" && PostFix=="DiLepRegion"){
            is_tH_like_and_not_ttH_like = ( istHlikeDiLepSR==1 && isDiLepSR!=1 && isttWctrlSR!=1 ) ? 1:0;
            passCut = ( ( istHlikeDiLepSR==1 || isDiLepSR==1 || isttWctrlSR==1 )
                && (fabs(leadLep_mcMatchId)==13 || fabs(leadLep_mcMatchId)==11)
                && (fabs(secondLep_mcMatchId)==13 || fabs(secondLep_mcMatchId)==11)
                && (!(leadLep_mcPromptFS == 1 && secondLep_mcPromptFS==1))
                && (leadLep_isMatchRightCharge==1 && secondLep_isMatchRightCharge==1)
                );
        }else if(Region=="mcflips" && PostFix=="DiLepRegion"){
            is_tH_like_and_not_ttH_like = ( istHlikeDiLepSR==1 && isDiLepSR!=1 && isttWctrlSR!=1 ) ? 1:0;
            passCut = ( ( istHlikeDiLepSR==1 || isDiLepSR==1 || isttWctrlSR==1 )
                && (fabs(leadLep_mcMatchId)==13 || fabs(leadLep_mcMatchId)==11)
                && (fabs(secondLep_mcMatchId)==13 || fabs(secondLep_mcMatchId)==11)
                && (leadLep_mcPromptFS == 1 && secondLep_mcPromptFS==1)
                && !(leadLep_isMatchRightCharge==1 && secondLep_isMatchRightCharge==1)
                );
        }else if(Region=="conv" && PostFix=="DiLepRegion"){
            is_tH_like_and_not_ttH_like = ( istHlikeDiLepSR==1 && isDiLepSR!=1 && isttWctrlSR!=1 ) ? 1:0;
            passCut = ( ( istHlikeDiLepSR==1 || isDiLepSR==1 || isttWctrlSR==1 )
                && ((leadLep_mcPromptGamma == 1 && leadLep_mcPromptFS ==1 )|| (secondLep_mcPromptGamma==1 && secondLep_mcPromptFS ==1))
                )
                ;
        }else if(Region=="dataobs" && PostFix=="DiLepRegion"){
            is_tH_like_and_not_ttH_like = ( istHlikeDiLepSR==1 && isDiLepSR!=1 && isttWctrlSR!=1 ) ? 1:0;
            passCut =  ( istHlikeDiLepSR==1 || isDiLepSR==1 || isttWctrlSR==1 );
        }else if(Region=="datafakes" && PostFix=="DiLepRegion"){
            is_tH_like_and_not_ttH_like = ( istHlikeDiLepFake==1 && isDiLepFake!=1 && isttWctrlFake!=1 ) ? 1:0;
            passCut = (istHlikeDiLepFake==1 || isDiLepFake==1 || isttWctrlFake==1);
        }else if(Region=="fakesub" && PostFix=="DiLepRegion"){
            is_tH_like_and_not_ttH_like = ( istHlikeDiLepFake==1 && isDiLepFake!=1 && isttWctrlFake!=1 ) ? 1:0;
            passCut = ((istHlikeDiLepFake==1 || isDiLepFake==1 || isttWctrlFake==1)
                && (fabs(leadLep_mcMatchId)==13 || fabs(leadLep_mcMatchId)==11)
                && (fabs(secondLep_mcMatchId)==13 || fabs(secondLep_mcMatchId)==11)
                && (leadLep_mcPromptFS == 1 && secondLep_mcPromptFS==1)
                && (leadLep_isMatchRightCharge==1 && secondLep_isMatchRightCharge==1)
            );
        }else if(Region=="dataflips" && PostFix=="DiLepRegion"){
            is_tH_like_and_not_ttH_like = ( istHlikeDiLepOS==1 && isDiLepOS!=1 && isttWctrlOS!=1 ) ? 1:0;
            passCut = (istHlikeDiLepOS==1 || isDiLepOS==1 || isttWctrlOS==1);
        }
        //TriLepRegion
        else if(Region=="prompt" && PostFix=="TriLepRegion"){
            is_tH_like_and_not_ttH_like = (istHlikeTriLepSR==1 && isTriLepSR!=1) ? 1:0;
            passCut = ((istHlikeTriLepSR==1 || isTriLepSR==1) 
                && leadLep_mcPromptFS==1 
                && secondLep_mcPromptFS==1 
                && thirdLep_mcPromptFS==1 
                && (fabs(leadLep_mcMatchId)==13 || fabs(leadLep_mcMatchId)==11)
                && (fabs(secondLep_mcMatchId)==13 || fabs(secondLep_mcMatchId)==11)
                && (fabs(thirdLep_mcMatchId)==13 || fabs(thirdLep_mcMatchId)==11)
            );
        }else if(Region=="mcfakes" && PostFix=="TriLepRegion"){
            is_tH_like_and_not_ttH_like = (istHlikeTriLepSR==1 && isTriLepSR!=1) ? 1:0;
            passCut = ((istHlikeTriLepSR==1 || isTriLepSR==1) 
                && !(leadLep_mcPromptFS==1 && secondLep_mcPromptFS==1 && thirdLep_mcPromptFS==1) 
            );
        }else if(Region=="conv" && PostFix=="TriLepRegion"){
            is_tH_like_and_not_ttH_like = (istHlikeTriLepSR==1 && isTriLepSR!=1) ? 1:0;
            passCut = ((istHlikeTriLepSR==1 || isTriLepSR==1) 
                && ((leadLep_mcPromptGamma==1 && leadLep_mcPromptFS == 1) || (secondLep_mcPromptGamma==1 && secondLep_mcPromptFS ==1) || (thirdLep_mcPromptGamma==1 && thirdLep_mcPromptFS==1)) 
            );
        }else if(Region=="dataobs" && PostFix=="TriLepRegion"){
            is_tH_like_and_not_ttH_like = (istHlikeTriLepSR==1 && isTriLepSR!=1) ? 1:0;
            passCut = (istHlikeTriLepSR==1 || isTriLepSR==1); 
        }else if(Region=="datafakes" && PostFix=="TriLepRegion"){
            is_tH_like_and_not_ttH_like = (istHlikeTriLepFake==1 && isTriLepFake!=1) ? 1:0;
            passCut = ((istHlikeTriLepFake==1 || isTriLepFake==1)
            ); 
        }else if(Region=="fakesub" && PostFix=="TriLepRegion"){
            is_tH_like_and_not_ttH_like = (istHlikeTriLepFake==1 && isTriLepFake!=1) ? 1:0;
            passCut = ((istHlikeTriLepFake==1 || isTriLepFake==1)
                && leadLep_mcPromptFS==1 
                && secondLep_mcPromptFS==1 
                && thirdLep_mcPromptFS==1 
                && (fabs(leadLep_mcMatchId)==13 || fabs(leadLep_mcMatchId)==11)
                && (fabs(secondLep_mcMatchId)==13 || fabs(secondLep_mcMatchId)==11)
                && (fabs(thirdLep_mcMatchId)==13 || fabs(thirdLep_mcMatchId)==11)
            ); 
        }
        else if(Region=="prompt" && PostFix=="ttZctrl"){
            is_tH_like_and_not_ttH_like = 0;
            passCut = (isttZctrlSR==1
                && leadLep_mcPromptFS==1 
                && secondLep_mcPromptFS==1 
                && thirdLep_mcPromptFS==1 
                && (fabs(leadLep_mcMatchId)==13 || fabs(leadLep_mcMatchId)==11)
                && (fabs(secondLep_mcMatchId)==13 || fabs(secondLep_mcMatchId)==11)
                && (fabs(thirdLep_mcMatchId)==13 || fabs(thirdLep_mcMatchId)==11)
            );
        }else if(Region=="mcfakes" && PostFix=="ttZctrl"){
            is_tH_like_and_not_ttH_like = 0;
            passCut = (isttZctrlSR==1 
                && !(leadLep_mcPromptFS==1 && secondLep_mcPromptFS==1 && thirdLep_mcPromptFS==1) 
            );
        }else if(Region=="conv" && PostFix=="ttZctrl"){
            is_tH_like_and_not_ttH_like = 0;
            passCut = ( isttZctrlSR==1 
                && ((leadLep_mcPromptGamma==1 && leadLep_mcPromptFS == 1) || (secondLep_mcPromptGamma==1 && secondLep_mcPromptFS ==1) || (thirdLep_mcPromptGamma==1 && thirdLep_mcPromptFS==1)) 
            );
        }else if(Region=="dataobs" && PostFix=="ttZctrl"){
            is_tH_like_and_not_ttH_like = 0;
            passCut = ( isttZctrlSR==1); 
        }else if(Region=="datafakes" && PostFix=="ttZctrl"){
            is_tH_like_and_not_ttH_like = 0;
            passCut = ( isttZctrlFake==1);
             
        }else if(Region=="fakesub" && PostFix=="ttZctrl"){
            is_tH_like_and_not_ttH_like = 0;
            passCut = ( isttZctrlFake==1
                && leadLep_mcPromptFS==1 
                && secondLep_mcPromptFS==1 
                && thirdLep_mcPromptFS==1 
                && (fabs(leadLep_mcMatchId)==13 || fabs(leadLep_mcMatchId)==11)
                && (fabs(secondLep_mcMatchId)==13 || fabs(secondLep_mcMatchId)==11)
                && (fabs(thirdLep_mcMatchId)==13 || fabs(thirdLep_mcMatchId)==11)
            ); 
        }
        else if(Region=="prompt" && PostFix=="WZctrl"){
            is_tH_like_and_not_ttH_like = 0;
            passCut = (isWZctrlSR==1
                && leadLep_mcPromptFS==1 
                && secondLep_mcPromptFS==1 
                && thirdLep_mcPromptFS==1 
                && (fabs(leadLep_mcMatchId)==13 || fabs(leadLep_mcMatchId)==11)
                && (fabs(secondLep_mcMatchId)==13 || fabs(secondLep_mcMatchId)==11)
                && (fabs(thirdLep_mcMatchId)==13 || fabs(thirdLep_mcMatchId)==11)
            );
        }else if(Region=="mcfakes" && PostFix=="WZctrl"){
            is_tH_like_and_not_ttH_like = 0;
            passCut = (isWZctrlSR==1 
                && !(leadLep_mcPromptFS==1 && secondLep_mcPromptFS==1 && thirdLep_mcPromptFS==1) 
            );
        }else if(Region=="conv" && PostFix=="WZctrl"){
            is_tH_like_and_not_ttH_like = 0;
            passCut = ( isWZctrlSR==1 
                && ((leadLep_mcPromptGamma==1 && leadLep_mcPromptFS == 1) || (secondLep_mcPromptGamma==1 && secondLep_mcPromptFS ==1) || (thirdLep_mcPromptGamma==1 && thirdLep_mcPromptFS==1)) 
            );
        }else if(Region=="dataobs" && PostFix=="WZctrl"){
            is_tH_like_and_not_ttH_like = 0;
            passCut = ( isWZctrlSR==1); 
        }else if(Region=="datafakes" && PostFix=="WZctrl"){
            is_tH_like_and_not_ttH_like = 0;
            passCut = ( isWZctrlFake==1);
             
        }else if(Region=="fakesub" && PostFix=="WZctrl"){
            is_tH_like_and_not_ttH_like = 0;
            passCut = ( isWZctrlFake==1
                && leadLep_mcPromptFS==1 
                && secondLep_mcPromptFS==1 
                && thirdLep_mcPromptFS==1 
                && (fabs(leadLep_mcMatchId)==13 || fabs(leadLep_mcMatchId)==11)
                && (fabs(secondLep_mcMatchId)==13 || fabs(secondLep_mcMatchId)==11)
                && (fabs(thirdLep_mcMatchId)==13 || fabs(thirdLep_mcMatchId)==11)
            ); 
        }
        //QuaLepRegion
        else if(Region=="prompt" && PostFix=="QuaLepRegion"){
            is_tH_like_and_not_ttH_like = (istHlikeQuaLepSR==1 && isQuaLepSR!=1) ? 1:0;
            passCut = ((istHlikeQuaLepSR==1 || isQuaLepSR==1) 
                && leadLep_mcPromptFS==1 
                && secondLep_mcPromptFS==1 
                && thirdLep_mcPromptFS==1 
                && fourthLep_mcPromptFS==1 
                && (fabs(leadLep_mcMatchId)==13 || fabs(leadLep_mcMatchId)==11)
                && (fabs(secondLep_mcMatchId)==13 || fabs(secondLep_mcMatchId)==11)
                && (fabs(thirdLep_mcMatchId)==13 || fabs(thirdLep_mcMatchId)==11)
                && (fabs(fourthLep_mcMatchId)==13 || fabs(fourthLep_mcMatchId)==11)
            );
        }else if(Region=="mcfakes" && PostFix=="QuaLepRegion"){
            is_tH_like_and_not_ttH_like = (istHlikeQuaLepSR==1 && isQuaLepSR!=1) ? 1:0;
            passCut = ((istHlikeQuaLepSR==1 || isQuaLepSR==1) 
                && !(leadLep_mcPromptFS==1 && secondLep_mcPromptFS==1 && thirdLep_mcPromptFS==1 &&fourthLep_mcPromptFS==1) 
            );
        }else if(Region=="conv" && PostFix=="QuaLepRegion"){
            is_tH_like_and_not_ttH_like = (istHlikeQuaLepSR==1 && isQuaLepSR!=1) ? 1:0;
            passCut = ((istHlikeQuaLepSR==1 || isQuaLepSR==1) 
                && ((leadLep_mcPromptGamma==1 && leadLep_mcPromptFS == 1) || (secondLep_mcPromptGamma==1 && secondLep_mcPromptFS ==1) || (thirdLep_mcPromptGamma==1 && thirdLep_mcPromptFS==1) || (fourthLep_mcPromptGamma==1 && fourthLep_mcPromptFS==1)) 
            );
        }else if(Region=="dataobs" && PostFix=="QuaLepRegion"){
            is_tH_like_and_not_ttH_like = (istHlikeQuaLepSR==1 && isQuaLepSR!=1) ? 1:0;
            passCut = (istHlikeQuaLepSR==1 || isQuaLepSR==1); 
        }else if(Region=="datafakes" && PostFix=="QuaLepRegion"){
            is_tH_like_and_not_ttH_like = (istHlikeQuaLepFake==1 && isQuaLepFake!=1) ? 1:0;
            passCut = ((istHlikeQuaLepFake==1 || isQuaLepFake==1)
            ); 
        }else if(Region=="fakesub" && PostFix=="QuaLepRegion"){
            is_tH_like_and_not_ttH_like = (istHlikeQuaLepFake==1 && isQuaLepFake!=1) ? 1:0;
            passCut = ((istHlikeQuaLepFake==1 || isQuaLepFake==1)
                && leadLep_mcPromptFS==1 
                && secondLep_mcPromptFS==1 
                && thirdLep_mcPromptFS==1 
                && fourthLep_mcPromptFS==1 
                && (fabs(leadLep_mcMatchId)==13 || fabs(leadLep_mcMatchId)==11)
                && (fabs(secondLep_mcMatchId)==13 || fabs(secondLep_mcMatchId)==11)
                && (fabs(thirdLep_mcMatchId)==13 || fabs(thirdLep_mcMatchId)==11)
                && (fabs(fourthLep_mcMatchId)==13 || fabs(fourthLep_mcMatchId)==11)
            ); 
        }else if(Region=="prompt" && PostFix=="ZZctrl"){
            is_tH_like_and_not_ttH_like = 0;
            passCut = (isZZctrlSR==1
                && leadLep_mcPromptFS==1 
                && secondLep_mcPromptFS==1 
                && thirdLep_mcPromptFS==1 
                && fourthLep_mcPromptFS==1 
                && (fabs(leadLep_mcMatchId)==13 || fabs(leadLep_mcMatchId)==11)
                && (fabs(secondLep_mcMatchId)==13 || fabs(secondLep_mcMatchId)==11)
                && (fabs(thirdLep_mcMatchId)==13 || fabs(thirdLep_mcMatchId)==11)
                && (fabs(fourthLep_mcMatchId)==13 || fabs(fourthLep_mcMatchId)==11)
            );
        }else if(Region=="mcfakes" && PostFix=="ZZctrl"){
            is_tH_like_and_not_ttH_like = 0;
            passCut = (isZZctrlSR==1 
                && !(leadLep_mcPromptFS==1 && secondLep_mcPromptFS==1 && thirdLep_mcPromptFS==1 && fourthLep_mcPromptFS==1) 
            );
        }else if(Region=="conv" && PostFix=="ZZctrl"){
            is_tH_like_and_not_ttH_like = 0;
            passCut = ( isZZctrlSR==1 
                && ((leadLep_mcPromptGamma==1 && leadLep_mcPromptFS == 1) || (secondLep_mcPromptGamma==1 && secondLep_mcPromptFS ==1) || (thirdLep_mcPromptGamma==1 && thirdLep_mcPromptFS==1) || (fourthLep_mcPromptGamma==1 && fourthLep_mcPromptFS==1)) 
            );
        }else if(Region=="dataobs" && PostFix=="ZZctrl"){
            is_tH_like_and_not_ttH_like = 0;
            passCut = ( isZZctrlSR==1); 
        }else if(Region=="datafakes" && PostFix=="ZZctrl"){
            is_tH_like_and_not_ttH_like = 0;
            passCut = ( isZZctrlFake==1);
             
        }else if(Region=="fakesub" && PostFix=="ZZctrl"){
            is_tH_like_and_not_ttH_like = 0;
            passCut = ( isZZctrlFake==1
                && leadLep_mcPromptFS==1 
                && secondLep_mcPromptFS==1 
                && thirdLep_mcPromptFS==1 
                && fourthLep_mcPromptFS==1 
                && (fabs(leadLep_mcMatchId)==13 || fabs(leadLep_mcMatchId)==11)
                && (fabs(secondLep_mcMatchId)==13 || fabs(secondLep_mcMatchId)==11)
                && (fabs(thirdLep_mcMatchId)==13 || fabs(thirdLep_mcMatchId)==11)
                && (fabs(fourthLep_mcMatchId)==13 || fabs(fourthLep_mcMatchId)==11)
            ); 
        }
        if(passCut && passPU && passTH){
            if(_saveWeight || _reWeight){
                if(oldtree->GetListOfBranches()->FindObject("EVENT_rWeights") && EVENT_rWeights->size()>=12 && FileName.Contains("ctcvcp")){
                    xsec_rwgt = get_rewgtlumi(FileName, EVENT_rWeights->at(11));
                }
                else{
                    xsec_rwgt = get_rewgtlumi(FileName, 1);
                }
                if(_reWeight){
                    EventWeight = EventWeight * xsec_rwgt;
                }
            }
            if(_useReWeight){
                global_rwgt = get_rwgtGlobal(FileName, DataEra, false);
                EventWeight = EventWeight * global_rwgt;
            }
            // calculate nn
            inputs["Dilep_pdgId"]=Dilep_pdgId;
            inputs["Hj_tagger_hadTop"]=Hj_tagger_hadTop;
            inputs["avg_dr_jet"]=avg_dr_jet;
            inputs["jet1_eta"]=abs(jet1_eta);
            inputs["jet1_phi"]=jet1_phi;
            inputs["jet1_pt"]=jet1_pt;
            inputs["jet2_eta"]=abs(jet2_eta);
            inputs["jet2_phi"]=jet2_phi;
            inputs["jet2_pt"]=jet2_pt;
            inputs["jet3_eta"]=abs(jet3_eta);
            inputs["jet3_phi"]=jet3_phi;
            inputs["jet3_pt"]=jet3_pt;
            inputs["jet4_eta"]=abs(jet4_eta);
            inputs["jet4_phi"]=jet4_phi;
            inputs["jet4_pt"]=jet4_pt;
            inputs["jetFwd1_eta"]=abs(jetFwd1_eta);
            inputs["jetFwd1_pt"]=jetFwd1_pt;
            inputs["lep1_charge"]=lep1_charge;
            inputs["lep1_conePt"]=lep1_conePt;
            inputs["lep1_eta"]=lep1_eta;
            inputs["lep1_phi"]=lep1_phi;
            inputs["lep2_conePt"]=lep2_conePt;
            inputs["lep2_eta"]=lep2_eta;
            inputs["lep2_phi"]=lep2_phi;
            inputs["mT_lep1"]=mT_lep1;
            inputs["mT_lep2"]=mT_lep2;
            inputs["maxeta"]=maxeta;
            inputs["mbb"]=mbb;
            inputs["metLD"]=metLD;
            inputs["mindr_lep1_jet"]=mindr_lep1_jet;
            inputs["mindr_lep2_jet"]=mindr_lep2_jet;
            inputs["nBJetLoose"]=nBJetLoose;
            inputs["nBJetMedium"]=nBJetMedium;
            inputs["n_presel_jet"]=n_presel_jet;
            inputs["n_presel_jetFwd"]=n_presel_jetFwd;
            inputs["hadTop_BDT"]=hadTop_BDT;
   
            // nn instance 2 vars
            inputs_newvars = inputs;
            //inputs_newvars["mass_dilep"]=mass_dilep;
            //inputs_newvars["mT2_top_2particle"]=mT2_top_2particle;
            //inputs_newvars["min_Deta_leadfwdJet_jet"]=min_Deta_leadfwdJet_jet;
            //inputs_newvars["min_Deta_mostfwdJet_jet"]=min_Deta_mostfwdJet_jet;
            
            // debug
            /*
            std::cout << " nEvent " << nEvent << std::endl;
            for (const auto& in_var: inputs) {
                float input_value = in_var.second;
                std::cout<< " input NN " << in_var.first << " = " << input_value << std::endl;
            }
            for (const auto& in_var: inputs_newvars) {
                float input_value = in_var.second;
                std::cout<< " input NN " << in_var.first << " = " << input_value << std::endl;
            }
            */
            // nn 1 evaluation
            double output_value;
            auto out_vals = nn_instance->compute(inputs);
            for (const auto& out: out_vals) {
                output_value = out.second;
                if (out.first=="predictions_ttH")DNN_ttHnode_all=out.second;
                if (out.first=="predictions_Rest")DNN_Restnode_all=out.second;
                if (out.first=="predictions_ttW")DNN_ttWnode_all=out.second;
                if (out.first=="predictions_tHq")DNN_tHQnode_all=out.second;
                
                //std::cout<< " output NN " << out.first << " = " << output_value << std::endl;
            }
            std::vector<double> DNN_vals;
            DNN_vals.push_back(DNN_ttHnode_all);
            DNN_vals.push_back(DNN_Restnode_all);
            DNN_vals.push_back(DNN_ttWnode_all);
            DNN_vals.push_back(DNN_tHQnode_all);
            
            setDNNflag(DNN_vals, DNN_maxval, DNNCat, DNNSubCat1_option1, DNNSubCat2_option1 , Dilep_pdgId, lep1_charge);
           
            // nn 2 evaluation
            double output_value_option2;
            auto out_vals_option2 = nn_instance_newvars->compute(inputs_newvars);
            for (const auto& out: out_vals_option2) {
                output_value_option2 = out.second;
                if (out.first=="predictions_ttH")DNN_ttHnode_all_option2=out.second;
                if (out.first=="predictions_Rest")DNN_Restnode_all_option2=out.second;
                if (out.first=="predictions_ttW")DNN_ttWnode_all_option2=out.second;
                if (out.first=="predictions_tHq")DNN_tHQnode_all_option2=out.second;
                
                //std::cout<< " output NN " << out.first << " = " << output_value << std::endl;
            }
            std::vector<double> DNN_vals_option2;
            DNN_vals_option2.push_back(DNN_ttHnode_all_option2);
            DNN_vals_option2.push_back(DNN_Restnode_all_option2);
            DNN_vals_option2.push_back(DNN_ttWnode_all_option2);
            DNN_vals_option2.push_back(DNN_tHQnode_all_option2);
            
            setDNNflag(DNN_vals_option2, DNN_maxval_option2, DNNCat_option2, DNNSubCat1_option2, DNNSubCat2_option2 , Dilep_pdgId, lep1_charge);
            
            // NN bins
            if(_useNNBins){
                TString CatFlag = "DNNSubCat2";
                // DNNSubCat2
                for(auto const category: _DNNSubCat2Maps){
                    //std::cout << MapOfChannelMap[CatFlag+"_option1"][DNNSubCat2_option1] << "  " << category << std::endl;
                    if (MapOfChannelMap[CatFlag+"_option1"][DNNSubCat2_option1] != category) continue;
                    int n = BinMap[CatFlag+"_option1"][category];
                    for(auto const bin: _bins){
                        float dnn_bin = getDNNBin(DNN_maxval, DNNSubCat2_FileName, category+"_2018", _DNNSubCat2NNMapHists, bin);
                        //_DNNSubCat2BinNames[CatFlag+"_"+category+"_nBin"+std::to_string(bin)] = getDNNBin(DNN_maxval, DNNSubCat2_FileName, category+"_2018", _DNNSubCat2NNMapHists, bin);
                        _DNNSubCat2BinNames[CatFlag+"_"+category+"_nBin"+std::to_string(bin)] = dnn_bin; 
                        if (n == bin){
                            DNNSubCat2_BIN = dnn_bin;
                        }
                    }
                }
                // DNNSubCat2
                for(auto const category: _DNNSubCat2_option2Maps){
                    //std::cout << MapOfChannelMap[CatFlag+"_option1"][DNNSubCat2_option2] << "  " << category << std::endl;
                    if (MapOfChannelMap[CatFlag+"_option2"][DNNSubCat2_option2] != category) continue;
                    int n = BinMap[CatFlag+"_option2"][category];
                    for(auto const bin: _bins){
                        float dnn_bin = getDNNBin(DNN_maxval, DNNSubCat2_option2_FileName, category+"_2018", _DNNSubCat2_option2NNMapHists, bin);
                        //_DNNSubCat2_option2BinNames[CatFlag+"_"+category+"_nBin"+std::to_string(bin)] = getDNNBin(DNN_maxval, DNNSubCat2_option2_FileName, category+"_2018", _DNNSubCat2_option2NNMapHists, bin);
                        _DNNSubCat2_option2BinNames[CatFlag+"_option2_"+category+"_nBin"+std::to_string(bin)] = dnn_bin; 
                        if (n == bin){
                            DNNSubCat2_option2_BIN = dnn_bin;
                        }
                    }
                }
            }
            newtree->Fill();
        }
    }

    Long64_t out_nentries = newtree->GetEntries(); 
    std::cout<<" output nentires: " << out_nentries << std::endl; 
    newtree->SetName(TreeName);
    newtree->SetTitle(TreeName);
    //newtree->Write();
    newtree->AutoSave();
    gDirectory->Delete("BOOM;*");
   
    
    delete oldfile;    
    delete newfile;
}

