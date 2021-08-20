import React, { useRef, useState, useEffect } from 'react';

import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';

import Poro from '../../img/poro.svg';

import './header.scss';
import { ADD_URL } from '../../constants';

import { scroller } from 'react-scroll';

import { Default, Mobile } from '../../constants';

/**
 * Header comp.
 */
const Header = () => {
  const [navBackground, setNavBackground] = useState(false);

  const navRef = useRef();
  navRef.current = navBackground;

  // Handle changing background color of nav bar upon scrolling
  useEffect(() => {
    const handleScroll = () => {
      const show = window.scrollY > 50;
      if (navRef.current !== show) {
        setNavBackground(show);
      }
    };
    document.addEventListener('scroll', handleScroll);
    return () => {
      document.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <div>
      <Default>
        <div>
          <Navbar
            collapseOnSelect
            expand="md"
            fixed="top"
            style={{ transition: '0.5s ease', backgroundColor: navBackground ? '#2C394B' : 'transparent' }}
          >
            <Container>
              <Navbar.Brand href="#home">
                <div className="d-flex justify-content-between align-items-center">
                  <a href="/">
                    <img alt="Poro logo" src={Poro} width="50" height="50" className="d-inline-block align-top" />
                  </a>
                  <a href="/">
                    <div className="text-white">Poro</div>
                  </a>
                </div>
              </Navbar.Brand>
              <Navbar.Toggle aria-controls="responsive-navbar-nav" />

              <Navbar.Collapse id="responsive-navbar-nav">
                <Nav className="ml-auto">
                  <Nav.Link
                    onClick={() =>
                      scroller.scrollTo('home', {
                        smooth: true,
                        duration: 500,
                      })
                    }
                  >
                    Home
                  </Nav.Link>
                  <Nav.Link
                    onClick={() =>
                      scroller.scrollTo('about', {
                        smooth: true,
                        offset: -70,
                        duration: 500,
                      })
                    }
                  >
                    About
                  </Nav.Link>
                  <Nav.Link
                    onClick={() =>
                      scroller.scrollTo('commands', {
                        smooth: true,
                        offset: -70,
                        duration: 500,
                      })
                    }
                  >
                    Commands
                  </Nav.Link>
                  {navBackground ? (
                    <Nav.Link className="get-porobot" onClick={() => window.open(ADD_URL, '_blank')}>
                      Get PoroBot
                    </Nav.Link>
                  ) : null}
                </Nav>
              </Navbar.Collapse>
            </Container>
          </Navbar>
        </div>
      </Default>

      <Mobile>
        <div>
          <Navbar
            collapseOnSelect
            expand="md"
            fixed="top"
            style={{ transition: '0.5s ease', backgroundColor: navBackground ? '#2C394B' : 'transparent' }}
          >
            <Container>
              <Navbar.Brand href="#home">
                <div className="d-flex justify-content-between align-items-center">
                  <a href="/">
                    <img alt="Poro logo" src={Poro} width="50" height="50" className="d-inline-block align-top" />
                  </a>
                  <a href="/">
                    <div className="text-white">Poro</div>
                  </a>
                </div>
              </Navbar.Brand>
              <Nav className="ml-auto">
                {navBackground ? (
                  <Nav.Link className="get-porobot" onClick={() => window.open(ADD_URL, '_blank')}>
                    &nbsp;&nbsp;Get PoroBot&nbsp;&nbsp;
                  </Nav.Link>
                ) : null}
              </Nav>
            </Container>
          </Navbar>
        </div>
      </Mobile>
    </div>
  );
};

export default Header;
