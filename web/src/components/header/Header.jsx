import React from 'react';

import HeaderDesktop from './HeaderDesktop';
import HeaderMobile from './HeaderMobile';

/*
 * Header comp.
 */

const Header = () => {
  return (
    <div>
      <HeaderDesktop />
      <HeaderMobile />
    </div>
  );
};

export default Header;
