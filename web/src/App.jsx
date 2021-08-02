import React from 'react';

import './style.scss';
import Header from './components/header/Header';
import Hero from './components/hero/Hero';
import About from './components/about/About';
import Commands from './components/commands/Commands';
import Footer from './components/footer/Footer';

const App = () => {
  return (
    <>
      <Header />
      <Hero />
      <About />
      <Commands />
      <Footer />
    </>
  );
};

export default App;
