import React from 'react';

import HeroDesktop from './HeroDesktop';
import HeroMobile from './HeroMobile';
/**
 * Hero comp.
 */
const Hero = () => {
  return (
    <div>
      <HeroDesktop />
      <HeroMobile />
    </div>
  );
};

export default Hero;
