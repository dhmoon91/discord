import React, { useState, useEffect } from 'react';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { COMMANDS_LIST } from '../../constants';

import CommandsBG from '../../img/commands-bg.jpg';

import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

import './commands.scss';

import Add from '../../img/add-command.PNG';
import Clear from '../../img/clear-command.PNG';
import Help from '../../img/help-command.PNG';
import List from '../../img/list-command.PNG';
import Rank from '../../img/rank-command.PNG';
import Remove from '../../img/remove-command.PNG';
import Teams from '../../img/teams-command.PNG';

import { Default, Mobile } from '../../constants';

/**
 * List of commands comp.
 */
const Commands = () => {
  const [show, setShow] = useState(false);
  const [text, setText] = useState('');
  const [image, setImage] = useState('');

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  var commandName;

  function activateShow(event) {
    commandName = event.currentTarget.textContent.replace('@poro ', '').split(' [')[0];
    setText(commandName.charAt(0).toUpperCase() + commandName.slice(1));
    handleShow();
  }

  useEffect(() => {
    switch (text) {
      case 'Add':
        setImage(Add);
        break;
      case 'Clear':
        setImage(Clear);
        break;
      case 'Help':
        setImage(Help);
        break;
      case 'List':
        setImage(List);
        break;
      case 'Rank':
        setImage(Rank);
        break;
      case 'Remove':
        setImage(Remove);
        break;
      case 'Teams':
        setImage(Teams);
        break;

      default:
        break;
    }
  }, [text]);

  return (
    <div>
      <Default>
        <div id="commands" className="hero" style={{ backgroundImage: `url(${CommandsBG})` }}>
          <Container>
            <div className="d-flex flex-column justify-content-center align-items-center">
              <div className="text-white mt-5 mb-3">
                <h2>Commands</h2>
              </div>

              {/* Table */}
              <div className="w-100">
                <Row className="commands-table commands-header text-white font-weight-bold">
                  <Col xs="2">COMMANDS</Col>
                  <Col>DESCRIPTION</Col>
                  <Col>USAGE</Col>
                </Row>

                {COMMANDS_LIST.map((command, idx) => (
                  <Row key={`commands-${idx}`} className="commands-table commands-row">
                    <Col xs="2">{command.command}</Col>
                    <Col>{command.desciprtion}</Col>
                    <Col className="usage" onClick={activateShow}>
                      {command.usage}
                    </Col>

                    <Modal
                      show={show}
                      onHide={() => setShow(false)}
                      dialogClassName="my-modal"
                      aria-labelledby="example-custom-modal-styling-title"
                    >
                      <Modal.Header closeButton>
                        <Modal.Title>{text} Command</Modal.Title>
                      </Modal.Header>
                      <Modal.Body className="mh-100">
                        <img className="img-fluid" alt="Poro logo" src={image} />
                      </Modal.Body>
                      <Modal.Footer>
                        <Button variant="secondary" onClick={handleClose}>
                          Close
                        </Button>
                      </Modal.Footer>
                    </Modal>
                  </Row>
                ))}
              </div>
            </div>
          </Container>
        </div>
      </Default>
      <Mobile>
        <div id="commands" className="hero" style={{ backgroundImage: `url(${CommandsBG})` }}>
          <Container>
            <div className="d-flex flex-column justify-content-center align-items-center">
              <div className="text-white mt-5 mb-3">
                <h3>Commands</h3>
              </div>

              {/* Table */}
              <div className="w-100">
                {COMMANDS_LIST.map((command, idx) => (
                  <div className="m-4" key={`commands-${idx}`}>
                    <Row className="commands-table commands-header text-white">
                      <Col className="ml-0 p-0 font-weight-bold">COMMANDS</Col>
                      <Col className="mr-0 p-0">{command.command}</Col>
                    </Row>

                    <Row className="commands-table commands-row">
                      <Col className="ml-0 p-0 font-weight-bold">DESCRIPTION</Col>
                      <Col className="text-left">{command.desciprtion}</Col>
                    </Row>

                    <Row className="commands-table commands-row">
                      <Col className="ml-0 p-0 font-weight-bold">USAGE</Col>
                      <Col className="text-left usage" onClick={activateShow}>
                        {command.usage}
                      </Col>
                    </Row>

                    <Modal
                      show={show}
                      onHide={() => setShow(false)}
                      dialogClassName="my-modal"
                      aria-labelledby="example-custom-modal-styling-title"
                    >
                      <Modal.Header closeButton>
                        <Modal.Title>{text} Command</Modal.Title>
                      </Modal.Header>
                      <Modal.Body className="mh-100">
                        <img className="img-fluid" alt="Poro logo" src={image} />
                      </Modal.Body>
                      <Modal.Footer>
                        <Button variant="secondary" onClick={handleClose}>
                          Close
                        </Button>
                      </Modal.Footer>
                    </Modal>
                  </div>
                ))}
              </div>
            </div>
          </Container>
        </div>
      </Mobile>
    </div>
  );
};

export default Commands;
