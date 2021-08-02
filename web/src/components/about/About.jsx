import React from 'react';

import Container from 'react-bootstrap/Container';

import './about.scss';

/**
 * About comp.
 */
const About = () => {
  return (
    <div className="about-section" style={{ backgroundColor: '#e9f2fa' }}>
      <Container>
        <div className="text-center mb-4">
          <h2>Why PoroBot?</h2>
        </div>
        <div className="d-flex justify-content-around">
          <div className="d-flex flex-column align-items-center">
            <p>Used by</p>
            <h3>Over 1000 servers</h3>
          </div>

          <div className="d-flex flex-column align-items-center">
            <p>Used by</p>
            <h3>Over 1000 servers</h3>
          </div>

          <div className="d-flex flex-column align-items-center">
            <p>Used by</p>
            <h3>Over 1000 servers</h3>
          </div>
        </div>
      </Container>
    </div>
  );
};

export default About;
