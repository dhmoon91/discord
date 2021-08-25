import React from 'react';

import Container from 'react-bootstrap/Container';

import { Mobile } from '../../constants';

import './about.scss';

/*
 * AboutMobile comp.
 */

const AboutMobile = () => {
  return (
    <Mobile>
      <div id="about" className="about-section" style={{ backgroundColor: '#e9f2fa' }}>
        <Container>
          <div className="text-center mb-4">
            <h2>Why PoroBot?</h2>
          </div>

          <hr />

          <div className="text-center mt-5 mb-4">
            <h5>
              PoroBot is a discord bot for League of Legends with various functionalities. Functionalities include
              finding summoner information and making teams for custom games for you and your friends to play!
            </h5>
          </div>

          <br />

          <div className="container p-3 my-3 bg-dark text-light number-of-users">
            <div className="d-flex justify-content-around">
              <div className="d-flex flex-column align-items-center text-center">
                <h7>Used By Over 1,000 Servers</h7>
              </div>

              <div className="d-flex flex-column align-items-center text-center">
                <h7>User Friendly Commands</h7>
              </div>

              <div className="d-flex flex-column align-items-center text-center">
                <h7>Up to date information</h7>
              </div>
            </div>
          </div>
        </Container>
      </div>
    </Mobile>
  );
};

export default AboutMobile;
