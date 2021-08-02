import React from 'react';

import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import './footer.scss';

/**
 * Footer comp.
 */
const Footer = () => {
  return (
    <div style={{ backgroundColor: '#000000b8' }}>
      <Container>
        <div className="d-flex flex-column justify-content-center align-items-center">
          <Button variant="primary" size="small" className="rounded mt-4">
            ADD TO DISCORD
          </Button>

          <div className="divider w-75 my-4" />

          <div className="d-flex justify-content-around w-75 text-white">
            <div className="d-flex flex-column">
              <h5>Block header</h5>
              <p>Block content</p>
            </div>

            <div className="d-flex flex-column">
              <h5>Block header</h5>
              <p>Block content</p>
            </div>

            <div className="d-flex flex-column">
              <h5>Block header</h5>
              <p>Block content</p>
            </div>

            <div className="d-flex flex-column">
              <h5>Block header</h5>
              <p>Block content</p>
            </div>
          </div>
        </div>
      </Container>
    </div>
  );
};

export default Footer;
