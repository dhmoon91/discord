import React from 'react';

import CommandsDesktop from './CommandsDesktop';
import CommandsMobile from './CommandsMobile';

/**
 * List of commands comp.
 */
const Commands = () => {
  return (
    <div>
      <CommandsDesktop />
      <CommandsMobile />
    </div>
  );
};

export default Commands;
