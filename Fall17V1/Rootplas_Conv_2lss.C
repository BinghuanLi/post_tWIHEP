// Input : 
// the output skim root file of tWIHEPFramework
// Function: 
// select Conv MC 2lss events according to Regions/Postfix and save/reconstruct only interested branches
// mcMatching prompt gamma: leadLep_mcPromptGamma ==1 && secondLep_mcPromptGamma==1 
// same sign lepton : fabs(Sum2lCharge)==2 
// dilep are tight tight: Dilep_nTight ==2 
//      Region cuts : 
//      SigRegion: n_presel_jets >=4
//      ttWctrl: n_presel_jets ==3
//      DiLepRegion: ""
// Output:
// rootplas for plotting and statistics study

#include "function.C"



void Rootplas_Conv_2lss(TString InputDir, TString OutputDir, TString FileName, TString Postfix){

    if(Postfix!="SigRegion" && Postfix!="ttWctrl" && Postfix!="DiLepRegion"){
        std::cout<< " ##################  ERROR ############ "<<std::endl;
        std::cout<< " Postfix must be SigRegion,ttWctrl or DiLepRegion, please pass a correct Postfix "<< std::endl;
        return;
    }
    TString Input = InputDir +"/"+ FileName + "Skim.root";
    TString Output = OutputDir  +"/"+FileName+ "_Conv2lss_"+Postfix+".root";
    std::cout <<" inpupt file is " << Input << std::endl;
    std::cout <<" outpupt file is " << Output << std::endl;
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
    float Sum2lCharge(0.), Dilep_nTight(0.), massL_SFOS(0.), Trilep_nTight(0.), Dilep_pdgId(0.), Sum3LCharge(0.);
    float xsec_rwgt(0.), EventWeight(0.);
    float mvaOutput_2lss_ttV(0.), mvaOutput_2lss_ttbar(0.);
    
   
    

    oldtree->SetBranchAddress("trueInteractions", &rtrueInteractions);
    oldtree->SetBranchAddress("nBestVtx", &rnBestVtx);
    oldtree->SetBranchAddress("n_presel_jet", &nLooseJet);
    oldtree->SetBranchAddress("nBJetLoose", &nBJetLoose);
    oldtree->SetBranchAddress("nBJetMedium", &nBJetMedium);
    oldtree->SetBranchAddress("nLightJet", &nLightJet);
    oldtree->SetBranchAddress("HiggsDecay", &HiggsDecay);
    oldtree->SetBranchAddress("lep1_pdgId", &lep1_pdgId);
    oldtree->SetBranchAddress("lep2_pdgId", &lep2_pdgId);
    oldtree->SetBranchAddress("lep3_pdgId", &lep3_pdgId);
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

    SetOldTreeBranchStatus(oldtree);
    
    //TFile *newfile = new TFile("IHEP_test.root","recreate");
    TFile *newfile = new TFile(Output,"recreate");
    TTree *newtree = new TTree("syncTree","syncTree");
    

    float trueInteractions=0;
    float nBestVtx=0;
    float n_presel_jet=0;
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
    float is_tH_like_and_not_ttH_like=0.;

    newtree = oldtree->CloneTree(0);
    newtree->Branch("TrueInteractions", &trueInteractions);
    newtree->Branch("nBestVTX", &nBestVtx);
    newtree->Branch("nEvt", &nEvt);
    newtree->Branch("xsec_rwgt", &xsec_rwgt);
    newtree->Branch("nLooseJet", &n_presel_jet);
    newtree->Branch("is_tH_like_and_not_ttH_like", &is_tH_like_and_not_ttH_like);
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
        trueInteractions = -999;
        n_presel_jet = -999;
        is_tH_like_and_not_ttH_like =0;
        nBestVtx = -999;
        nEvt = -999;
        xsec_rwgt = 1.;
        oldtree->GetEntry(i);
        Bool_t pass2LMatchGamma = kTRUE;
        Bool_t pass2LCharge = kTRUE;
        Bool_t pass2LTightID = kTRUE;
        Bool_t pass2LRegionCut = kTRUE;
        Bool_t passTHSelectionCut = kFALSE;
        Bool_t passCut = kFALSE;
        if(!(firstLep_mcPromptGamma==1 || secondLep_mcPromptGamma==1))pass2LMatchGamma = kFALSE;
        if(!(fabs(Sum2lCharge)==2))pass2LCharge = kFALSE;
        if(!(Dilep_nTight ==2))pass2LTightID = kFALSE;
        if(Postfix=="SigRegion" && ( (nBJetLoose < 2 && nBJetMedium < 1) || nLooseJet <4))pass2LRegionCut = kFALSE;
        if(Postfix=="ttWctrl" && ( (nBJetLoose < 2 && nBJetMedium < 1) || nLooseJet !=3))pass2LRegionCut = kFALSE;
        if(Postfix=="DiLepRegion" && ( (nBJetLoose < 2 && nBJetMedium < 1) || nLooseJet <3))pass2LRegionCut = kFALSE;
        if(nBJetMedium >0 && nLightJet >0)passTHSelectionCut=kTRUE;
        passCut = pass2LMatchGamma && pass2LCharge && pass2LTightID && (pass2LRegionCut || passTHSelectionCut);
    
        if(passCut){
            trueInteractions = rtrueInteractions;
            nBestVtx = rnBestVtx;
            nEvt = nEvent;
            xsec_rwgt = get_rewgtlumi(FileName);
            EventWeight = EventWeight * xsec_rwgt;
            n_presel_jet = nLooseJet;
            is_tH_like_and_not_ttH_like = (passTHSelectionCut && !pass2LRegionCut)? 1:0;
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
            
            
            newtree->Fill();
        }
        HiggsDecay =0;
        lep1_pdgId=0;
        lep2_pdgId=0;
        lep3_pdgId=0;
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
    }

    newtree->SetName("syncTree");
    newtree->SetTitle("syncTree");
    //newtree->Write();
    newtree->AutoSave();
    gDirectory->Delete("BOOM;*");
    
    delete oldfile;    
    delete newfile;
}

