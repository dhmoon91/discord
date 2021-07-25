import React from 'react';

import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Container from 'react-bootstrap/Container';
import Logo from '../logo.svg';

/**
 * Header comp.
 */
const Header = () => {
  return (
    <>
    <Navbar collapseOnSelect expand="md" bg="dark" variant="dark">
    <Container>
    <Navbar.Brand href="#home">
        <img
          alt="Poro logo"
          src={Logo}
          width="30"
          height="30"
          className="d-inline-block align-top"
        />
        Poro
      </Navbar.Brand>
    <Navbar.Toggle aria-controls="responsive-navbar-nav" />

    <Navbar.Collapse id="responsive-navbar-nav">
      <Nav className="me-auto">
        <Nav.Link href="#features">Poro1</Nav.Link>
        <Nav.Link href="#pricing">Poro2</Nav.Link>

        {/* Dropdown */}
        <NavDropdown title="poro" id="collasible-nav-dropdown">
          <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
          <NavDropdown.Item href="#action/3.2">Another action</NavDropdown.Item>
          <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
          <NavDropdown.Divider />
          <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
        </NavDropdown>
      </Nav>
      <Nav>
        <Nav.Link href="#deets">Right item</Nav.Link>
        <Nav.Link eventKey={2} href="#memes">
        Right item
        </Nav.Link>
      </Nav>
    </Navbar.Collapse>
    </Container>
  </Navbar>
  </>
  );
};

export default Header;