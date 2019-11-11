// Input : 
// the output skim root file of tWIHEPFramework
// Function: 
//      Region cuts : 
//      SigRegion: n_presel_jets >=4
//      ttWctrl: n_presel_jets ==3
//      DiLepRegion: ""
// Output:
// rootplas for plotting and statistics study

#include "function.C"

// options
Bool_t _useReWeight = false; // set to true if we recalculate Global Weight.
Bool_t _useFakeRate = true; // set to true if we recalculate FakeRate Weighting.
Bool_t _useTrigSF = true; // set to true if we recalculate Trig SFs.


//Fake Rate
//Histograms that are used for applying lepton fake rate weight
std::vector<std::string> _frSystNames = {"central","up","down","pt1","pt2","be1","be2","QCD","TT"};
TString fakeRateFileName = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/tWIHEPFramework/config/weights/ttH2018/FR_data_ttH_mva.root";
TString fakeRateMuonHistName = "FR_mva090_mu_data_comb";
TString fakeRateElectronHistName = "FR_mva090_el_data_comb_NC";
std::map<std::string,TH2F*> _MuonFakeRate;
std::map<std::string,TH2F*> _ElectronFakeRate;


void Rootplas_TrainMVA_2lss(TString InputDir, TString OutputDir, TString FileName, TString Postfix){

    if(Postfix!="SigRegion" && Postfix!="ttWctrl" && Postfix!="DiLepRegion"){
        std::cout<< " ##################  ERROR ############ "<<std::endl;
        std::cout<< " Postfix must be SigRegion,ttWctrl or DiLepRegion, please pass a correct Postfix "<< std::endl;
        return;
    }
    TString Input = InputDir +"/"+ FileName + "Skim.root";
    TString Output = OutputDir  +"/"+FileName+ "_TrainMVA_"+Postfix+".root";
    std::cout <<" inpupt file is " << Input << std::endl;
    std::cout <<" outpupt file is " << Output << std::endl;
    
    // fake rate  
    if (_useFakeRate){
        for (auto const frSystName: _frSystNames){
            setFakeRateHistograms(fakeRateFileName, fakeRateMuonHistName, fakeRateElectronHistName, _MuonFakeRate, _ElectronFakeRate, frSystName, frSystName);
        }
    }
    
    TFile *oldfile = new TFile(Input);
    TTree *oldtree = (TTree*)oldfile->Get("TNT/BOOM");


    Long64_t nentries = oldtree->GetEntries(); 
    
    float nLooseJet=0;
    float nLightJet=0;
    float nBJetLoose=0;
    float nBJetMedium=0;
    int HiggsDecay=0;
    double rtrueInteractions=0;
    int rnBestVtx=0;
    Long64_t nEvt = 0;
    Long64_t nEvent = 0;
   
    float firstLep_mcPromptGamma(0.), secondLep_mcPromptGamma(0.), thirdLep_mcPromptGamma(0.);
    float firstLep_mcPromptFS(0.), secondLep_mcPromptFS(0.), thirdLep_mcPromptFS(0.);
    float firstLep_isMatchRightCharge(0.), secondLep_isMatchRightCharge(0.), thirdLep_isMatchRightCharge(0.);
    float lep1_pdgId(0.), lep2_pdgId(0.), lep3_pdgId(0.);
    float lep1_conept(0.), lep2_conept(0.);// lep3_conept(0.);
    float lep1_ismvasel(0.), lep2_ismvasel(0.), lep3_ismvasel(0.);
    float lep1_eta(0.), lep2_eta(0.), lep3_eta(0.);
    float lep1_phi(0.), lep2_phi(0.), lep3_phi(0.);
    float lep1_E(0.), lep2_E(0.), lep3_E(0.);
    float Sum2lCharge(0.), Dilep_nTight(0.), massL_SFOS(0.), Trilep_nTight(0.), Dilep_pdgId(0.), Sum3LCharge(0.);
    float xsec_rwgt(0.),cpodd_rwgt(0.);
    float mvaOutput_2lss_ttV(0.), mvaOutput_2lss_ttbar(0.);
    float EventWeight(0.), FakeRate(0.);
    float TriggerSF(0.), TriggerSF_SysUp(0.), TriggerSF_SysDown(0.);
    float FakeRate_m_central(0.), FakeRate_m_up(0.), FakeRate_m_down(0.), FakeRate_m_pt1(0.), FakeRate_m_pt2(0.), FakeRate_m_be1(0.), FakeRate_m_be2(0.), FakeRate_m_QCD(0.), FakeRate_m_TT(0.); 
    float FakeRate_e_central(0.), FakeRate_e_up(0.), FakeRate_e_down(0.), FakeRate_e_pt1(0.), FakeRate_e_pt2(0.), FakeRate_e_be1(0.), FakeRate_e_be2(0.), FakeRate_e_QCD(0.), FakeRate_e_TT(0.); 
    float TTHLep_2L(0.), massL(0.), n_fakeablesel_tau(0.), mass_dilep(0.), metLD(0.), lep1_TightCharge(0.), lep2_TightCharge(0.), nLepTight(0.);

    std::vector<double>* EVENT_rWeights =0;
    std::vector<double>* Jet25_pt =0;
    std::vector<double>* Jet25_eta =0;
    std::vector<double>* Jet25_phi =0;
    std::vector<double>* Jet25_energy =0;
    std::vector<double>* Jet25_bDiscriminator =0;
    
    
    oldtree->SetBranchAddress("EVENT_rWeights", &EVENT_rWeights);
    oldtree->SetBranchAddress("Jet25_pt", &Jet25_pt);
    oldtree->SetBranchAddress("Jet25_eta", &Jet25_eta);
    oldtree->SetBranchAddress("Jet25_phi", &Jet25_phi);
    oldtree->SetBranchAddress("Jet25_energy", &Jet25_energy);
    oldtree->SetBranchAddress("Jet25_bDiscriminator", &Jet25_bDiscriminator);
    oldtree->SetBranchAddress("trueInteractions", &rtrueInteractions);
    oldtree->SetBranchAddress("nBestVtx", &rnBestVtx);
    oldtree->SetBranchAddress("n_presel_jet", &nLooseJet);
    oldtree->SetBranchAddress("nBJetLoose", &nBJetLoose);
    oldtree->SetBranchAddress("nBJetMedium", &nBJetMedium);
    oldtree->SetBranchAddress("nLightJet", &nLightJet);
    oldtree->SetBranchAddress("HiggsDecay", &HiggsDecay);
    oldtree->SetBranchAddress("TTHLep_2L", &TTHLep_2L);
    oldtree->SetBranchAddress("massL", &massL);
    oldtree->SetBranchAddress("n_fakeablesel_tau", &n_fakeablesel_tau);
    oldtree->SetBranchAddress("mass_dilep", &mass_dilep);
    oldtree->SetBranchAddress("metLD", &metLD);
    oldtree->SetBranchAddress("nLepTight", &nLepTight);
    oldtree->SetBranchAddress("lep1_TightCharge", &lep1_TightCharge);
    oldtree->SetBranchAddress("lep2_TightCharge", &lep2_TightCharge);
    oldtree->SetBranchAddress("lep1_pdgId", &lep1_pdgId);
    oldtree->SetBranchAddress("lep2_pdgId", &lep2_pdgId);
    oldtree->SetBranchAddress("lep3_pdgId", &lep3_pdgId);
    oldtree->SetBranchAddress("leadLep_corrpt", &lep1_conept);
    oldtree->SetBranchAddress("secondLep_corrpt", &lep2_conept);
    //oldtree->SetBranchAddress("thirdLep_corrpt", &lep3_conept);
    oldtree->SetBranchAddress("lep1_ismvasel", &lep1_ismvasel);
    oldtree->SetBranchAddress("lep2_ismvasel", &lep2_ismvasel);
    oldtree->SetBranchAddress("lep3_ismvasel", &lep3_ismvasel);
    oldtree->SetBranchAddress("lep1_eta", &lep1_eta);
    oldtree->SetBranchAddress("lep2_eta", &lep2_eta);
    oldtree->SetBranchAddress("lep3_eta", &lep3_eta);
    oldtree->SetBranchAddress("lep1_phi", &lep1_phi);
    oldtree->SetBranchAddress("lep2_phi", &lep2_phi);
    oldtree->SetBranchAddress("lep3_phi", &lep3_phi);
    oldtree->SetBranchAddress("lep1_E", &lep1_E);
    oldtree->SetBranchAddress("lep2_E", &lep2_E);
    oldtree->SetBranchAddress("lep3_E", &lep3_E);
    oldtree->SetBranchAddress("leadLep_mcPromptGamma", &firstLep_mcPromptGamma);
    oldtree->SetBranchAddress("secondLep_mcPromptGamma", &secondLep_mcPromptGamma);
    oldtree->SetBranchAddress("thirdLep_mcPromptGamma", &thirdLep_mcPromptGamma);
    oldtree->SetBranchAddress("leadLep_mcPromptFS", &firstLep_mcPromptFS);
    oldtree->SetBranchAddress("secondLep_mcPromptFS", &secondLep_mcPromptFS);
    oldtree->SetBranchAddress("thirdLep_mcPromptFS", &thirdLep_mcPromptFS);
    oldtree->SetBranchAddress("leadLep_isMatchRightCharge", &firstLep_isMatchRightCharge);
    oldtree->SetBranchAddress("secondLep_isMatchRightCharge", &secondLep_isMatchRightCharge);
    oldtree->SetBranchAddress("thirdLep_isMatchRightCharge", &thirdLep_isMatchRightCharge);
    oldtree->SetBranchAddress("Sum2lCharge", &Sum2lCharge);
    oldtree->SetBranchAddress("Sum3LCharge", &Sum3LCharge);
    oldtree->SetBranchAddress("Dilep_nTight", &Dilep_nTight);
    oldtree->SetBranchAddress("Dilep_pdgId", &Dilep_pdgId);
    oldtree->SetBranchAddress("massL_SFOS", &massL_SFOS);
    oldtree->SetBranchAddress("Trilep_nTight", &Trilep_nTight);
    oldtree->SetBranchAddress("nEvent", &nEvent);
    oldtree->SetBranchAddress("mvaOutput_2lss_ttV", &mvaOutput_2lss_ttV);
    oldtree->SetBranchAddress("mvaOutput_2lss_ttbar", &mvaOutput_2lss_ttbar);
    oldtree->SetBranchAddress("EventWeight", &EventWeight);
    oldtree->SetBranchAddress("TriggerSF", &TriggerSF);
    oldtree->SetBranchAddress("TriggerSF_SysUp", &TriggerSF_SysUp);
    oldtree->SetBranchAddress("TriggerSF_SysDown", &TriggerSF_SysDown);
    oldtree->SetBranchAddress("FakeRate", &FakeRate);
    oldtree->SetBranchAddress("FakeRate_m_central", &FakeRate_m_central);
    oldtree->SetBranchAddress("FakeRate_m_up", &FakeRate_m_up);
    oldtree->SetBranchAddress("FakeRate_m_down", &FakeRate_m_down);
    oldtree->SetBranchAddress("FakeRate_m_pt1", &FakeRate_m_pt1);
    oldtree->SetBranchAddress("FakeRate_m_pt2", &FakeRate_m_pt2);
    oldtree->SetBranchAddress("FakeRate_m_be1", &FakeRate_m_be1);
    oldtree->SetBranchAddress("FakeRate_m_be2", &FakeRate_m_be2);
    oldtree->SetBranchAddress("FakeRate_m_QCD", &FakeRate_m_QCD);
    oldtree->SetBranchAddress("FakeRate_m_TT", &FakeRate_m_TT);
    oldtree->SetBranchAddress("FakeRate_e_central", &FakeRate_e_central);
    oldtree->SetBranchAddress("FakeRate_e_up", &FakeRate_e_up);
    oldtree->SetBranchAddress("FakeRate_e_down", &FakeRate_e_down);
    oldtree->SetBranchAddress("FakeRate_e_pt1", &FakeRate_e_pt1);
    oldtree->SetBranchAddress("FakeRate_e_pt2", &FakeRate_e_pt2);
    oldtree->SetBranchAddress("FakeRate_e_be1", &FakeRate_e_be1);
    oldtree->SetBranchAddress("FakeRate_e_be2", &FakeRate_e_be2);
    oldtree->SetBranchAddress("FakeRate_e_QCD", &FakeRate_e_QCD);
    oldtree->SetBranchAddress("FakeRate_e_TT", &FakeRate_e_TT);

    SetOldTreeBranchStatus(oldtree);
    
    //TFile *newfile = new TFile("IHEP_test.root","recreate");
    TFile *newfile = new TFile(Output,"recreate");
    TTree *newtree = new TTree("syncTree","syncTree");
    

    float trueInteractions=0;
    float nBestVtx=0;
    float n_presel_jet=0;
    // angles
    float angle_bbpp_highest2b(-99);
    float cosa_bbpp_highest2b(-99);
    float acuteangle_bbpp_highest2b(-99);
    float deta_highest2b(-99);
    float cosa_highest2b(-99);
    // shape theoretical uncertainties 
    float CMS_ttHl_thu_shape_ttH(0.), CMS_ttHl_thu_shape_ttH_SysUp(0.), CMS_ttHl_thu_shape_ttH_SysDown(0.);
    float CMS_ttHl_thu_shape_ttW(0.), CMS_ttHl_thu_shape_ttW_SysUp(0.), CMS_ttHl_thu_shape_ttW_SysDown(0.);
    float CMS_ttHl_thu_shape_ttZ(0.), CMS_ttHl_thu_shape_ttZ_SysUp(0.), CMS_ttHl_thu_shape_ttZ_SysDown(0.);
    // closure shape uncertainties
    float CMS_ttHl17_Clos_e_shape_ee(0.), CMS_ttHl17_Clos_e_shape_ee_SysUp(0.), CMS_ttHl17_Clos_e_shape_ee_SysDown(0.);
    float CMS_ttHl17_Clos_e_shape_em(0.), CMS_ttHl17_Clos_e_shape_em_SysUp(0.), CMS_ttHl17_Clos_e_shape_em_SysDown(0.);
    float CMS_ttHl17_Clos_m_shape_mm(0.), CMS_ttHl17_Clos_m_shape_mm_SysUp(0.), CMS_ttHl17_Clos_m_shape_mm_SysDown(0.);
    float CMS_ttHl17_Clos_m_shape_em(0.), CMS_ttHl17_Clos_m_shape_em_SysUp(0.), CMS_ttHl17_Clos_m_shape_em_SysDown(0.);
    // cut flags 
    float passTrigCut(0.), passMassllCut(0.), passTauNCut(0.), passZvetoCut(0.), passMetLDCut(0.);
    float passTightChargeCut(0.), passLepTightNCut(0.), passGenMatchCut(0.);
    float is_tH_like_and_not_ttH_like=0.;

    newtree = oldtree->CloneTree(0);
    newtree->Branch("TrueInteractions", &trueInteractions);
    newtree->Branch("nBestVTX", &nBestVtx);
    newtree->Branch("is_tH_like_and_not_ttH_like", &is_tH_like_and_not_ttH_like);
    newtree->Branch("nEvt", &nEvt);
    newtree->Branch("angle_bbpp_highest2b", &angle_bbpp_highest2b);
    newtree->Branch("cosa_bbpp_highest2b", &cosa_bbpp_highest2b);
    newtree->Branch("acuteangle_bbpp_highest2b", &acuteangle_bbpp_highest2b);
    newtree->Branch("deta_highest2b", &deta_highest2b);
    newtree->Branch("cosa_highest2b", &cosa_highest2b);
    newtree->Branch("xsec_rwgt", &xsec_rwgt);
    newtree->Branch("cpodd_rwgt", &cpodd_rwgt);
    newtree->Branch("nLooseJet", &n_presel_jet);
    newtree->Branch("passTrigCut", &passTrigCut);
    newtree->Branch("passMassllCut", &passMassllCut);
    newtree->Branch("passTauNCut", &passTauNCut);
    newtree->Branch("passZvetoCut", &passZvetoCut);
    newtree->Branch("passMetLDCut", &passMetLDCut);
    newtree->Branch("passTightChargeCut", &passTightChargeCut);
    newtree->Branch("passLepTightNCut", &passLepTightNCut);
    newtree->Branch("passGenMatchCut", &passGenMatchCut);
    newtree->Branch("CMS_ttHl_thu_shape_ttH", &CMS_ttHl_thu_shape_ttH);
    newtree->Branch("CMS_ttHl_thu_shape_ttH_SysUp", &CMS_ttHl_thu_shape_ttH_SysUp);
    newtree->Branch("CMS_ttHl_thu_shape_ttH_SysDown", &CMS_ttHl_thu_shape_ttH_SysDown);
    newtree->Branch("CMS_ttHl_thu_shape_ttW", &CMS_ttHl_thu_shape_ttW);
    newtree->Branch("CMS_ttHl_thu_shape_ttW_SysUp", &CMS_ttHl_thu_shape_ttW_SysUp);
    newtree->Branch("CMS_ttHl_thu_shape_ttW_SysDown", &CMS_ttHl_thu_shape_ttW_SysDown);
    newtree->Branch("CMS_ttHl_thu_shape_ttZ", &CMS_ttHl_thu_shape_ttZ);
    newtree->Branch("CMS_ttHl_thu_shape_ttZ_SysUp", &CMS_ttHl_thu_shape_ttZ_SysUp);
    newtree->Branch("CMS_ttHl_thu_shape_ttZ_SysDown", &CMS_ttHl_thu_shape_ttZ_SysDown);
    newtree->Branch("CMS_ttHl17_Clos_e_shape_ee", &CMS_ttHl17_Clos_e_shape_ee);
    newtree->Branch("CMS_ttHl17_Clos_e_shape_ee_SysUp", &CMS_ttHl17_Clos_e_shape_ee_SysUp);
    newtree->Branch("CMS_ttHl17_Clos_e_shape_ee_SysDown", &CMS_ttHl17_Clos_e_shape_ee_SysDown);
    newtree->Branch("CMS_ttHl17_Clos_e_shape_em", &CMS_ttHl17_Clos_e_shape_em);
    newtree->Branch("CMS_ttHl17_Clos_e_shape_em_SysUp", &CMS_ttHl17_Clos_e_shape_em_SysUp);
    newtree->Branch("CMS_ttHl17_Clos_e_shape_em_SysDown", &CMS_ttHl17_Clos_e_shape_em_SysDown);
    newtree->Branch("CMS_ttHl17_Clos_m_shape_mm", &CMS_ttHl17_Clos_m_shape_mm);
    newtree->Branch("CMS_ttHl17_Clos_m_shape_mm_SysUp", &CMS_ttHl17_Clos_m_shape_mm_SysUp);
    newtree->Branch("CMS_ttHl17_Clos_m_shape_mm_SysDown", &CMS_ttHl17_Clos_m_shape_mm_SysDown);
    newtree->Branch("CMS_ttHl17_Clos_m_shape_em", &CMS_ttHl17_Clos_m_shape_em);
    newtree->Branch("CMS_ttHl17_Clos_m_shape_em_SysUp", &CMS_ttHl17_Clos_m_shape_em_SysUp);
    newtree->Branch("CMS_ttHl17_Clos_m_shape_em_SysDown", &CMS_ttHl17_Clos_m_shape_em_SysDown);
    
    
    //newtree = oldtree->CopyTree("jet4_pt>=30");
    
    for (Long64_t i=0;i<nentries; i++) {
        passTrigCut=0;
        passMassllCut=0;
        passTauNCut=0; 
        passZvetoCut=0;
        passMetLDCut=0;
        passTightChargeCut=0; 
        passLepTightNCut=0;
        passGenMatchCut=0;
        trueInteractions = -999;
        n_presel_jet = -999;
        nBJetLoose = -999;
        nBJetMedium = -999;
        nLightJet = -999;
        nBestVtx = -999;
        nEvt = -999;
        acuteangle_bbpp_highest2b = -9.;
        angle_bbpp_highest2b = -9.;
        cosa_bbpp_highest2b = -9.;
        deta_highest2b = -9.;
        cosa_highest2b = -9.;
        xsec_rwgt = 1.;
        cpodd_rwgt = 1.;
        oldtree->GetEntry(i);
        Bool_t pass2LRegionCut = kTRUE;
        Bool_t passTHSelectionCut = kFALSE;
        Bool_t passCut = kFALSE;
        if(Postfix=="SigRegion" && ( (nBJetLoose < 2 && nBJetMedium < 1) || nLooseJet <4))pass2LRegionCut = kFALSE;
        if(Postfix=="ttWctrl" && ( (nBJetLoose < 2 && nBJetMedium < 1) || nLooseJet !=3))pass2LRegionCut = kFALSE;
        if(Postfix=="DiLepRegion" && ( (nBJetLoose < 2 && nBJetMedium < 1) || nLooseJet <3))pass2LRegionCut = kFALSE;
        if(nBJetMedium >0 && nLightJet >0)passTHSelectionCut=kTRUE;
        passCut = pass2LRegionCut || passTHSelectionCut;
    
        if(passCut){
            trueInteractions = rtrueInteractions;
            nBestVtx = rnBestVtx;
            nEvt = nEvent;
            //xsec_rwgt = get_rewgtlumi(FileName);
            // Global Weight
            if(_useReWeight){
             double rwgt = get_rwgtGlobal(FileName);
             EventWeight *= rwgt;
            }
            n_presel_jet = nLooseJet;
            is_tH_like_and_not_ttH_like = (passTHSelectionCut && !pass2LRegionCut)? 1:0;
            if(oldtree->GetListOfBranches()->FindObject("EVENT_rWeights") && EVENT_rWeights->size()>68){
                cpodd_rwgt = EVENT_rWeights->at(59)/EVENT_rWeights->at(11);
            }
            if (nEvent <0) nEvt = nEvent + 4294967296; // 4294967296 = 2^32, this is to fix the problem saving EVENT_event as a wrong type
            else nEvt = nEvent;
            // fill lnN1D_p1()
            // https://github.com/peruzzim/cmgtools-lite/blob/94X_dev_ttH/TTHAnalysis/python/plotter/ttH-multilepton/systsUnc.txt
            CMS_ttHl_thu_shape_ttH = 1.;
            CMS_ttHl_thu_shape_ttH_SysUp = lnN1D_p1(1.05, mvaOutput_2lss_ttbar, -1, 1) * lnN1D_p1(1.02, mvaOutput_2lss_ttV, -1, 1)/1.04;
            CMS_ttHl_thu_shape_ttH_SysDown = 1./CMS_ttHl_thu_shape_ttH_SysUp;
            CMS_ttHl_thu_shape_ttW = 1.;
            CMS_ttHl_thu_shape_ttW_SysUp = lnN1D_p1(1.02, mvaOutput_2lss_ttbar, -1, 1) * lnN1D_p1(1.03, mvaOutput_2lss_ttV, -1, 1)/1.04;
            CMS_ttHl_thu_shape_ttW_SysDown = 1./CMS_ttHl_thu_shape_ttW_SysUp;
            CMS_ttHl_thu_shape_ttZ = 1.;
            CMS_ttHl_thu_shape_ttZ_SysUp = lnN1D_p1(1.06, mvaOutput_2lss_ttbar, -1, 1) * lnN1D_p1(1.06, mvaOutput_2lss_ttV, -1, 1)/1.04;
            CMS_ttHl_thu_shape_ttZ_SysDown = 1./CMS_ttHl_thu_shape_ttZ_SysUp;
            CMS_ttHl17_Clos_e_shape_ee = 1.;
            CMS_ttHl17_Clos_e_shape_ee_SysUp = lnN1D_p1(1.5, mvaOutput_2lss_ttbar, -1, 1)/1.2;
            CMS_ttHl17_Clos_e_shape_ee_SysDown = 1./CMS_ttHl17_Clos_e_shape_ee_SysUp;
            CMS_ttHl17_Clos_e_shape_em = 1.;
            CMS_ttHl17_Clos_e_shape_em_SysUp = lnN1D_p1(1.25, mvaOutput_2lss_ttbar, -1, 1)/1.1;
            CMS_ttHl17_Clos_e_shape_em_SysDown = 1./CMS_ttHl17_Clos_e_shape_em_SysUp;
            CMS_ttHl17_Clos_m_shape_mm = 1.;
            CMS_ttHl17_Clos_m_shape_mm_SysUp = lnN1D_p1(1.5, mvaOutput_2lss_ttV, -1, 1)/1.24;
            CMS_ttHl17_Clos_m_shape_mm_SysDown = 1./CMS_ttHl17_Clos_m_shape_mm_SysUp;
            CMS_ttHl17_Clos_m_shape_em = 1.;
            CMS_ttHl17_Clos_m_shape_em_SysUp = lnN1D_p1(1.8, mvaOutput_2lss_ttV, -1, 1)/1.35;
            CMS_ttHl17_Clos_m_shape_em_SysDown = 1./CMS_ttHl17_Clos_m_shape_em_SysUp;
            
            // calculate lorentz angle
            TLorentzVector Lep1_CMS, Lep2_CMS, p1_CMS, p2_CMS;
            Lep1_CMS.SetPtEtaPhiE(lep1_conept,lep1_eta,lep1_phi,lep1_E);
            Lep2_CMS.SetPtEtaPhiE(lep2_conept,lep2_eta,lep2_phi,lep2_E);
            p1_CMS.SetXYZM(0,0,-1,0.938); // proton mass 938MeV
            p2_CMS.SetXYZM(0,0,1,0.938); 
            TLorentzVector  bJet1, bJet2;
            double b1_CSV= -99;
            double b2_CSV= -999;
            for(uint jet_en=0; jet_en < Jet25_pt->size(); jet_en++){
               // deep CSV value ordered
               if(Jet25_bDiscriminator->at(jet_en)>b1_CSV){
                   // set b2 to old b1
                   b2_CSV = b1_CSV;
                   bJet2 = bJet1;
                   // set b1 to current jet
                   b1_CSV = Jet25_bDiscriminator->at(jet_en);
                   bJet1.SetPtEtaPhiE(Jet25_pt->at(jet_en),Jet25_eta->at(jet_en),Jet25_phi->at(jet_en),Jet25_energy->at(jet_en));
               } else if(Jet25_bDiscriminator->at(jet_en)>b2_CSV){
                   // set b1 to current jet
                   b2_CSV = Jet25_bDiscriminator->at(jet_en);
                   bJet2.SetPtEtaPhiE(Jet25_pt->at(jet_en),Jet25_eta->at(jet_en),Jet25_phi->at(jet_en),Jet25_energy->at(jet_en));
               }
            }
            if(fabs(bJet2.Pt())>0.0001){
                angle_bbpp_highest2b = get_boostedAngle( Lep1_CMS, Lep2_CMS, p1_CMS, p2_CMS, bJet1, bJet2, cosa_bbpp_highest2b);
                deta_highest2b = bJet1.Eta() - bJet2.Eta();
                double temp_angle_2b = getAngleOfVecs(bJet1, bJet2, cosa_highest2b);
            }
            acuteangle_bbpp_highest2b = TMath::Pi()/2.-fabs(angle_bbpp_highest2b-TMath::Pi()/2.);

            // FakeRate
            if(_useFakeRate){
                std::map<std::string,float> mFakeRate;
                std::map<std::string,float> eFakeRate;
                float old_FakeRate = FakeRate;
                FakeRate = getFakeRateWeight( lep1_ismvasel,  lep1_pdgId,  lep1_conept,  lep1_eta,  lep2_ismvasel,  lep2_pdgId,  lep2_conept,  lep2_eta , _MuonFakeRate, _ElectronFakeRate);
                for(auto const frSystName: _frSystNames){
                    mFakeRate[frSystName] = getFakeRateWeight(lep1_ismvasel,  lep1_pdgId,  lep1_conept,  lep1_eta,  lep2_ismvasel,  lep2_pdgId,  lep2_conept,  lep2_eta, _MuonFakeRate, _ElectronFakeRate, frSystName,"central"); 
                    eFakeRate[frSystName] = getFakeRateWeight(lep1_ismvasel,  lep1_pdgId,  lep1_conept,  lep1_eta,  lep2_ismvasel,  lep2_pdgId,  lep2_conept,  lep2_eta, _MuonFakeRate, _ElectronFakeRate, "central",frSystName); 
                }
                EventWeight *= FakeRate/old_FakeRate;
                FakeRate_m_central=mFakeRate["central"];
                FakeRate_m_up=mFakeRate["up"];
                FakeRate_m_down=mFakeRate["down"];
                FakeRate_m_pt1=mFakeRate["pt1"];
                FakeRate_m_pt2=mFakeRate["pt2"];
                FakeRate_m_be1=mFakeRate["be1"];
                FakeRate_m_be2=mFakeRate["be2"];
                FakeRate_m_TT=mFakeRate["TT"];
                FakeRate_m_QCD=mFakeRate["QCD"];
                FakeRate_e_central=eFakeRate["central"];
                FakeRate_e_up=eFakeRate["up"];
                FakeRate_e_down=eFakeRate["down"];
                FakeRate_e_pt1=eFakeRate["pt1"];
                FakeRate_e_pt2=eFakeRate["pt2"];
                FakeRate_e_be1=eFakeRate["be1"];
                FakeRate_e_be2=eFakeRate["be2"];
                FakeRate_e_TT=eFakeRate["TT"];
                FakeRate_e_QCD=eFakeRate["QCD"];
            }

            // Trigger SFs
            if(_useTrigSF){
                float old_trigSF = TriggerSF;
                std::tie(TriggerSF, TriggerSF_SysUp, TriggerSF_SysDown)= getTriggerWeight( lep1_pdgId,  lep1_conept,  lep2_pdgId,  lep2_conept );
                EventWeight = EventWeight * TriggerSF/old_trigSF;
            }

            // add flags
            passTrigCut= TTHLep_2L==1 ? 1:0;
            passMassllCut= massL>=12 ? 1:0;
            passTauNCut= n_fakeablesel_tau<1 ? 1:0; 
            passZvetoCut= (mass_dilep>101.2 || mass_dilep<81.2)? 1:0;
            passMetLDCut= metLD>30 ? 1:0;
            passTightChargeCut= (lep1_TightCharge ==1 && lep2_TightCharge==1) ? 1:0; 
            passLepTightNCut= nLepTight<=2 ? 1:0;
            if(FileName.Contains("TT_PSwgt") || FileName.Contains("TTTo")){// TTJets
                passGenMatchCut=( firstLep_isMatchRightCharge==1 && secondLep_isMatchRightCharge ==1 )? 0 : 1;
            }else{
                passGenMatchCut=( firstLep_isMatchRightCharge==1 && secondLep_isMatchRightCharge ==1 )? 1 : 0;
            }
            newtree->Fill();
        }
        HiggsDecay =0;
        is_tH_like_and_not_ttH_like =0;
        TTHLep_2L=0;
        massL=0;
        n_fakeablesel_tau=0;
        mass_dilep=0;
        metLD=0;
        nLepTight=0;
        lep1_TightCharge=0;
        lep2_TightCharge=0;
        lep1_pdgId=0;
        lep2_pdgId=0;
        lep3_pdgId=0;
        lep1_conept=0;
        lep2_conept=0;
        //lep3_conept=0;
        lep1_ismvasel=0;
        lep2_ismvasel=0;
        lep3_ismvasel=0;
        lep1_eta=0;
        lep2_eta=0;
        lep3_eta=0;
        lep1_phi=0;
        lep2_phi=0;
        lep3_phi=0;
        lep1_E=0;
        lep2_E=0;
        lep3_E=0;
        firstLep_isMatchRightCharge=0;
        secondLep_isMatchRightCharge=0;
        thirdLep_isMatchRightCharge=0;
        firstLep_mcPromptGamma=0;
        secondLep_mcPromptGamma=0;
        thirdLep_mcPromptGamma=0;
        firstLep_mcPromptFS=0;
        secondLep_mcPromptFS=0;
        thirdLep_mcPromptFS=0;
        nLooseJet = 0;
        Sum2lCharge =0;
        Dilep_nTight =0;
        Dilep_pdgId =0;
        massL_SFOS =0;
        Trilep_nTight =0;
        mvaOutput_2lss_ttV=0;
        mvaOutput_2lss_ttbar=0;
        EventWeight=0;
        TriggerSF=0;
        TriggerSF_SysUp=0;
        TriggerSF_SysDown=0;
        FakeRate=0;
        FakeRate_m_central=0;
        FakeRate_m_up=0;
        FakeRate_m_down=0;
        FakeRate_m_pt1=0;
        FakeRate_m_pt2=0;
        FakeRate_m_be1=0;
        FakeRate_m_be2=0;
        FakeRate_m_TT=0;
        FakeRate_m_QCD=0;
        FakeRate_e_central=0;
        FakeRate_e_up=0;
        FakeRate_e_down=0;
        FakeRate_e_pt1=0;
        FakeRate_e_pt2=0;
        FakeRate_e_be1=0;
        FakeRate_e_be2=0;
        FakeRate_e_TT=0;
        FakeRate_e_QCD=0;
    }

    newtree->SetName("syncTree");
    newtree->SetTitle("syncTree");
    //newtree->Write();
    newtree->AutoSave();
    gDirectory->Delete("BOOM;*");
    
    delete oldfile;    
    delete newfile;
}

