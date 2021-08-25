import React from 'react';

import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';

import PoroBG from '../../img/bg.jpeg';

import { ADD_URL, Default } from '../../constants';

import './hero.scss';

import { scroller } from 'react-scroll';

/*
 *  HeroDesktop comp.
 */

const HeroDesktop = () => {
  return (
    <Default>
      <div id="home" className="hero d-flex justify-content-start" style={{ backgroundImage: `url(${PoroBG})` }}>
        <Container className="d-flex align-items-center">
          <div className="d-flex flex-column text-white">
            <div className="mb-4">
              <h1>PoroBot</h1>
            </div>

            <div className="mb-4">
              <h2>Discord Bot for</h2>
              <h2>League of Legends</h2>
            </div>

            <div className="d-flex mt-1">
              <div className="mr-2">
                <Button variant="primary" size="lg" className="rounded" onClick={() => window.open(ADD_URL, '_blank')}>
                  ADD TO DISCORD
                </Button>
              </div>

              <div>
                <Button
                  variant="secondary"
                  size="lg"
                  className="rounded"
                  onClick={() =>
                    scroller.scrollTo('commands', {
                      smooth: true,
                      offset: -70,
                      duration: 500,
                    })
                  }
                >
                  GO TO COMMANDS
                </Button>
              </div>
            </div>
          </div>
        </Container>
      </div>
    </Default>
  );
};

export default HeroDesktop;
