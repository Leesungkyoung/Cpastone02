import React from 'react';
import Navbar from '../components/layout/Navbar';
import HeroSection from '../components/sections/HeroSection';
import IntroSection from '../components/sections/IntroSection';
import DashboardPreview from '../components/sections/DashboardPreview';
import InquirySection from '../components/sections/InquirySection';
import Footer from '../components/layout/Footer';

const LandingPage = () => {
  return (
    <React.Fragment>
      <Navbar />
      <main>
        <HeroSection />
        <IntroSection />
        <DashboardPreview />
        <InquirySection />
      </main>
      <Footer />
    </React.Fragment>
  );
};

export default LandingPage;
