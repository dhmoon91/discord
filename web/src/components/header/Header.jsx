import React, { useRef, useState, useEffect } from 'react';

import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';

import Poro from '../../img/poro.svg';

import './header.scss';

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
      const show = window.scrollY > 300;
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
      <Navbar
        collapseOnSelect
        expand="md"
        fixed="top"
        style={{ transition: '0.5s ease', backgroundColor: navBackground ? 'black' : 'transparent' }}
      >
        <Container>
          <Navbar.Brand href="#home">
            <div className="d-flex justify-content-between align-items-center">
              <img alt="Poro logo" src={Poro} width="50" height="50" className="d-inline-block align-top" />
              <div className="text-white">Poro</div>
            </div>
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />

          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="ml-auto">
              <Nav.Link href="#deets">Home</Nav.Link>
              <Nav.Link href="#deets">About</Nav.Link>
              <Nav.Link href="#deets">Commands</Nav.Link>
              <Nav.Link onClick="window.open('http://google.com','_blank')">Get PoroBot</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </div>
  );
};

export default Header;
