import React from 'react';

import Container from 'react-bootstrap/Container';

import './footer.scss';

import Poro from '../../img/poro.svg';

/**
 * Footer comp.
 */
const Footer = () => {
  return (
    <div style={{ backgroundColor: '#000000b8' }}>
      <Container>
        <div className="d-flex flex-column justify-content-center align-items-center">
          <div className="contact-header">
            <h3>Contact Us</h3>
          </div>

          <div className="divider w-75 my-4" />

          <div className="d-flex justify-content-around w-75 text-white">
            <div className="w-50">
              <p>
                If there is any issues or have any questions regarding our bot, please mention in our{' '}
                <a
                  className="server-link-text"
                  href="https://discord.gg/KHAZxSWsUJ"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  discord server
                </a>
                .
              </p>
              <div className="mt-4">
                <a href="https://discord.gg/KHAZxSWsUJ" target="_blank" rel="noopener noreferrer">
                  <img src="https://discordapp.com/api/guilds/877799693902569492/embed.png" />
                </a>
              </div>
            </div>

            <div className="w-50 text-center inline">
              <a href="/">
                <img className="footer-logo" alt="Poro logo" src={Poro} />
              </a>
            </div>
          </div>

          <br />

          <div className="footer-legal d-flex flex-column justify-content-center align-items-center text-white">
            <p>
              PoroBot isn&apos;t endorsed by Riot Games and doesn&apos;t reflect the views or opinions of Riot Games or
              anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games
              are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
            </p>
          </div>
        </div>
      </Container>
    </div>
  );
};

export default Footer;
