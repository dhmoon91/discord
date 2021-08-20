import React from 'react';

import Container from 'react-bootstrap/Container';

import { Default, Mobile } from '../../constants';

import './about.scss';

/**
 * About comp.
 */
const About = () => {
  return (
    <div>
      <Default>
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
                  <p>Used By</p>
                  <h4>Over 1,000 Users</h4>
                </div>

                <div className="d-flex flex-column align-items-center text-center">
                  <p>Used By</p>
                  <h4>Over 1,000 Servers</h4>
                </div>

                <div className="d-flex flex-column align-items-center text-center">
                  <p>Used By</p>
                  <h4>Over 1,000 Channels</h4>
                </div>
              </div>
            </div>
          </Container>
        </div>
      </Default>

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
                  <p>Used By</p>
                  <h7>Over 1,000 Users</h7>
                </div>

                <div className="d-flex flex-column align-items-center text-center">
                  <p>Used By</p>
                  <h7>Over 1,000 Servers</h7>
                </div>

                <div className="d-flex flex-column align-items-center text-center">
                  <p>Used By</p>
                  <h7>Over 1,000 Channels</h7>
                </div>
              </div>
            </div>
          </Container>
        </div>
      </Mobile>
    </div>
  );
};

export default About;
