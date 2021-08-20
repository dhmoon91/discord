import { useMediaQuery } from 'react-responsive';

export const COMMANDS_LIST = [
  {
    command: '@poro rank',
    desciprtion: 'Gets rank of summoner',
    usage: '@poro rank [summoner]',
  },
  {
    command: '@poro add',
    desciprtion: 'Adds summoner(s) to list of members to create team',
    usage: '@poro add [summoner1, summoner2, ...]',
  },
  {
    command: '@poro list',
    desciprtion: 'Displays the list of summoner ranks and names added',
    usage: '@poro list',
  },
  {
    command: '@poro teams',
    desciprtion: 'Generates teams',
    usage: '@poro teams',
  },
  {
    command: '@poro clear',
    desciprtion: 'Clears player(s) from the list on standby for a custom game',
    usage: '@poro clear',
  },
  {
    command: '@poro remove',
    desciprtion: 'Removes player(s) from the list on standby for a custom game',
    usage: '@poro remove [summoner1, summoner2, ...]',
  },
  {
    command: '@poro help',
    desciprtion: 'Displays the syntax and the description of all the commands.',
    usage: '@poro help [command_name]',
  },
];

export const ADD_URL = 'https://discord.com/api/oauth2/authorize?client_id=870848582805237800&permissions=0&scope=bot';

export const Desktop = ({ children }) => {
  const isDesktop = useMediaQuery({ minWidth: 992 });
  return isDesktop ? children : null;
};

export const Tablet = ({ children }) => {
  const isTablet = useMediaQuery({ minWidth: 768, maxWidth: 991 });
  return isTablet ? children : null;
};

export const Mobile = ({ children }) => {
  const isMobile = useMediaQuery({ maxWidth: 767 });
  return isMobile ? children : null;
};
export const Default = ({ children }) => {
  const isNotMobile = useMediaQuery({ minWidth: 768 });
  return isNotMobile ? children : null;
};
