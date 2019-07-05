// Input : 
// the output skim root file of tWIHEPFramework
// Function: 
// select prompt MC 2lss events according to Regions/Postfix and save/reconstruct only interested branches
// mcMatching prompt right charge: leadLep_isMatchRightCharge && leadLep_mcPromptFS && secondLep_isMatchRightCharge && secondLep_mcPromptFS  
// same sign lepton : fabs(Sum2lCharge)==2 
// dilep are tight tight: Dilep_nTight ==2 
//      Region cuts : 
//      SigRegion: n_presel_jets >=4
//      ttWctrl: n_presel_jets ==3
//      DiLepRegion: ""
// Output:
// rootplas for plotting and statistics study

#include "function.C"


void Rootplas_Prompt_2lss(TString InputDir, TString OutputDir, TString FileName, TString Postfix){

    if(Postfix!="SigRegion" && Postfix!="ttWctrl" && Postfix!="DiLepRegion"){
        std::cout<< " ##################  ERROR ############ "<<std::endl;
        std::cout<< " Postfix must be SigRegion,ttWctrl or DiLepRegion, please pass a correct Postfix "<< std::endl;
        return;
    }
    TString Input = InputDir +"/"+ FileName + "Skim.root";
    TString Output = OutputDir  +"/"+FileName+ "_Prompt2lss_"+Postfix+".root";
    std::cout <<" inpupt file is " << Input << std::endl;
    std::cout <<" outpupt file is " << Output << std::endl;
    TFile *oldfile = new TFile(Input);
    TTree *oldtree = (TTree*)oldfile->Get("TNT/BOOM");


    //Long64_t nentries = 100; 
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
    float lep1_eta(0.), lep2_eta(0.), lep3_eta(0.);
    float lep1_phi(0.), lep2_phi(0.), lep3_phi(0.);
    float lep1_E(0.), lep2_E(0.), lep3_E(0.);
    float Sum2lCharge(0.), Dilep_nTight(0.), massL_SFOS(0.), Trilep_nTight(0.), Dilep_pdgId(0.), Sum3LCharge(0.);
    float xsec_rwgt(0.), EventWeight(0.), cpodd_rwgt(0.);
    float mvaOutput_2lss_ttV(0.), mvaOutput_2lss_ttbar(0.);
    
    std::vector<double>* EVENT_rWeights =0;
    std::vector<double>* Jet25_pt =0;
    std::vector<double>* Jet25_eta =0;
    std::vector<double>* Jet25_phi =0;
    std::vector<double>* Jet25_energy =0;
    std::vector<double>* Jet25_bDiscriminator =0;
    std::vector<double>* Jet25_isFromH =0;
    std::vector<double>* Jet25_isFromTop =0;
    std::vector<double>* Jet25_matchId =0;
   
    

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
    oldtree->SetBranchAddress("leadLep_corrpt", &lep1_conept);
    oldtree->SetBranchAddress("secondLep_corrpt", &lep2_conept);
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
    oldtree->SetBranchAddress("EventWeight", &EventWeight);
    oldtree->SetBranchAddress("mvaOutput_2lss_ttV", &mvaOutput_2lss_ttV);
    oldtree->SetBranchAddress("mvaOutput_2lss_ttbar", &mvaOutput_2lss_ttbar);
    oldtree->SetBranchAddress("EVENT_rWeights", &EVENT_rWeights);
    oldtree->SetBranchAddress("Jet25_pt", &Jet25_pt);
    oldtree->SetBranchAddress("Jet25_eta", &Jet25_eta);
    oldtree->SetBranchAddress("Jet25_phi", &Jet25_phi);
    oldtree->SetBranchAddress("Jet25_energy", &Jet25_energy);
    oldtree->SetBranchAddress("Jet25_bDiscriminator", &Jet25_bDiscriminator);
    oldtree->SetBranchAddress("Jet25_isFromH", &Jet25_isFromH);
    oldtree->SetBranchAddress("Jet25_isFromTop", &Jet25_isFromTop);
    oldtree->SetBranchAddress("Jet25_matchId", &Jet25_matchId);

    SetOldTreeBranchStatus(oldtree);
    
    //TFile *newfile = new TFile("IHEP_test.root","recreate");
    TFile *newfile = new TFile(Output,"recreate");
    TTree *newtree = new TTree("syncTree","syncTree");
    

    float trueInteractions=0;
    float nBestVtx=0;
    float n_presel_jet=0;
    // angles
    float angle_bbpp_match2b(-99);
    float angle_bbpp_loose2b(-99);
    float angle_bbpp_highest2b(-99);
    float cosa_bbpp_match2b(-99);
    float cosa_bbpp_loose2b(-99);
    float cosa_bbpp_highest2b(-99);
    float deta_match2b(-99);
    float deta_loose2b(-99);
    float deta_highest2b(-99);
    float cosa_match2b(-99);
    float cosa_loose2b(-99);
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
    float is_tH_like_and_not_ttH_like=0.;

    newtree = oldtree->CloneTree(0);
    newtree->Branch("TrueInteractions", &trueInteractions);
    newtree->Branch("nBestVTX", &nBestVtx);
    newtree->Branch("nEvt", &nEvt);
    newtree->Branch("angle_bbpp_match2b", &angle_bbpp_match2b);
    newtree->Branch("angle_bbpp_loose2b", &angle_bbpp_loose2b);
    newtree->Branch("angle_bbpp_highest2b", &angle_bbpp_highest2b);
    newtree->Branch("cosa_bbpp_match2b", &cosa_bbpp_match2b);
    newtree->Branch("cosa_bbpp_loose2b", &cosa_bbpp_loose2b);
    newtree->Branch("cosa_bbpp_highest2b", &cosa_bbpp_highest2b);
    newtree->Branch("deta_match2b", &deta_match2b);
    newtree->Branch("deta_loose2b", &deta_loose2b);
    newtree->Branch("deta_highest2b", &deta_highest2b);
    newtree->Branch("cosa_match2b", &cosa_match2b);
    newtree->Branch("cosa_loose2b", &cosa_loose2b);
    newtree->Branch("cosa_highest2b", &cosa_highest2b);
    newtree->Branch("xsec_rwgt", &xsec_rwgt);
    newtree->Branch("cpodd_rwgt", &cpodd_rwgt);
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
        cpodd_rwgt = 1.;
        angle_bbpp_highest2b = -9.;
        angle_bbpp_loose2b = -9.;
        angle_bbpp_match2b = -9.;
        cosa_bbpp_highest2b = -9.;
        cosa_bbpp_loose2b = -9.;
        cosa_bbpp_match2b = -9.;
        deta_highest2b = -9.;
        deta_loose2b = -9.;
        deta_match2b = -9.;
        cosa_highest2b = -9.;
        cosa_loose2b = -9.;
        cosa_match2b = -9.;
        oldtree->GetEntry(i);
        Bool_t pass2LMatchRightCharge = kTRUE;
        Bool_t pass2LPromptFS = kTRUE;
        Bool_t pass2LCharge = kTRUE;
        Bool_t pass2LTightID = kTRUE;
        Bool_t pass2LRegionCut = kTRUE;
        Bool_t passTHSelectionCut = kFALSE;
        Bool_t passCut = kFALSE;
        if(!(firstLep_mcPromptFS==1 && secondLep_mcPromptFS==1))pass2LPromptFS = kFALSE;
        if(!(firstLep_isMatchRightCharge==1 && secondLep_isMatchRightCharge==1))pass2LMatchRightCharge = kFALSE;
        if(!(fabs(Sum2lCharge)==2))pass2LCharge = kFALSE;
        if(!(Dilep_nTight ==2))pass2LTightID = kFALSE;
        if(Postfix=="SigRegion" && ( (nBJetLoose < 2 && nBJetMedium < 1) || nLooseJet <4))pass2LRegionCut = kFALSE;
        if(Postfix=="ttWctrl" && ( (nBJetLoose < 2 && nBJetMedium < 1) || nLooseJet !=3))pass2LRegionCut = kFALSE;
        if(Postfix=="DiLepRegion" && ( (nBJetLoose < 2 && nBJetMedium < 1) || nLooseJet <3))pass2LRegionCut = kFALSE;
        if(nBJetMedium >0 && nLightJet >0)passTHSelectionCut=kTRUE;
        passCut = pass2LMatchRightCharge && pass2LPromptFS && pass2LCharge && pass2LTightID && (pass2LRegionCut || passTHSelectionCut);
    
        if(passCut){
            trueInteractions = rtrueInteractions;
            nBestVtx = rnBestVtx;
            nEvt = nEvent;
            xsec_rwgt = get_rewgtlumi(FileName);
            if(oldtree->GetListOfBranches()->FindObject("EVENT_rWeights") && EVENT_rWeights->size()>68){
                cpodd_rwgt = EVENT_rWeights->at(59)/EVENT_rWeights->at(11);
            }
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
            
            // calculate lorentz angle
            TLorentzVector Lep1_CMS, Lep2_CMS, p1_CMS, p2_CMS;
            Lep1_CMS.SetPtEtaPhiE(lep1_conept,lep1_eta,lep1_phi,lep1_E);
            Lep2_CMS.SetPtEtaPhiE(lep2_conept,lep2_eta,lep2_phi,lep2_E);
            p1_CMS.SetXYZM(0,0,-1,0.938); // proton mass 938MeV
            p2_CMS.SetXYZM(0,0,1,0.938); 
            TLorentzVector loosebJet1, loosebJet2, bJet1, bJet2, matchbJet1, matchbJet2;
            double b1_CSV= -99;
            double b2_CSV= -999;
            for(uint jet_en=0; jet_en < Jet25_pt->size(); jet_en++){
               // deep CSV loose b
               if(Jet25_isFromTop->at(jet_en)==1 && fabs(Jet25_matchId->at(jet_en)) == 5){
                    if(fabs(matchbJet1.Pt())<0.0001) matchbJet1.SetPtEtaPhiE(Jet25_pt->at(jet_en),Jet25_eta->at(jet_en),Jet25_phi->at(jet_en),Jet25_energy->at(jet_en));
                    else if(fabs(matchbJet2.Pt())<0.0001) matchbJet2.SetPtEtaPhiE(Jet25_pt->at(jet_en),Jet25_eta->at(jet_en),Jet25_phi->at(jet_en),Jet25_energy->at(jet_en));
               }
               // deep CSV loose b
               if(Jet25_bDiscriminator->at(jet_en)>0.1522){
                    if(fabs(loosebJet1.Pt())<0.0001) loosebJet1.SetPtEtaPhiE(Jet25_pt->at(jet_en),Jet25_eta->at(jet_en),Jet25_phi->at(jet_en),Jet25_energy->at(jet_en));
                    else if(fabs(loosebJet2.Pt())<0.0001) loosebJet2.SetPtEtaPhiE(Jet25_pt->at(jet_en),Jet25_eta->at(jet_en),Jet25_phi->at(jet_en),Jet25_energy->at(jet_en));
               }
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
            //std::cout << " nEvent : "<<nEvent<<" loosebJet1.Pt "<< loosebJet1.Pt() << " loosebJet2.Pt "<<loosebJet2.Pt() << " bJet1.Pt "<< bJet1.Pt() << " bJet2.Pt "<< bJet2.Pt() << std::endl;
            // if there exist 2 loose b 
            if(fabs(loosebJet2.Pt())>0.0001){
                angle_bbpp_loose2b =get_boostedAngle(Lep1_CMS, Lep2_CMS, p1_CMS, p2_CMS, loosebJet1, loosebJet2, cosa_bbpp_loose2b); 
                deta_loose2b = loosebJet1.Eta() - loosebJet2.Eta();
                double temp_angle_2b = getAngleOfVecs(loosebJet1, loosebJet2, cosa_loose2b);
            }
            if(fabs(matchbJet2.Pt())>0.0001){
                angle_bbpp_match2b =get_boostedAngle(Lep1_CMS, Lep2_CMS, p1_CMS, p2_CMS, matchbJet1, matchbJet2, cosa_bbpp_match2b); 
                deta_match2b = matchbJet1.Eta() - matchbJet2.Eta();
                double temp_angle_2b = getAngleOfVecs(matchbJet1, matchbJet2, cosa_match2b);
            }
            if(fabs(bJet2.Pt())>0.0001){
                angle_bbpp_highest2b = get_boostedAngle( Lep1_CMS, Lep2_CMS, p1_CMS, p2_CMS, bJet1, bJet2, cosa_bbpp_highest2b);
                deta_highest2b = bJet1.Eta() - bJet2.Eta();
                double temp_angle_2b = getAngleOfVecs(bJet1, bJet2, cosa_highest2b);
            }
            
            newtree->Fill();
        }
        EVENT_rWeights->clear();
        Jet25_pt->clear();
        Jet25_eta->clear();
        Jet25_phi->clear();
        Jet25_energy->clear();
        Jet25_bDiscriminator->clear();
        Jet25_isFromTop->clear();
        Jet25_isFromH->clear();
        Jet25_matchId->clear();
        HiggsDecay =0;
        lep1_pdgId=0;
        lep2_pdgId=0;
        lep3_pdgId=0;
        lep1_conept=0;
        lep2_conept=0;
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
    }

    newtree->SetName("syncTree");
    newtree->SetTitle("syncTree");
    //newtree->Write();
    newtree->AutoSave();
    gDirectory->Delete("BOOM;*");
    
    delete oldfile;    
    delete newfile;
}

