import React from 'react';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { COMMANDS_LIST } from '../../constants';

import CommandsBG from '../../img/commands-bg.jpg';

import './commands.scss';

/**
 * List of commands comp.
 */
const Commands = () => {
  return (
    <div className="hero" style={{ backgroundImage: `url(${CommandsBG})` }}>
      <Container>
        <div className="d-flex flex-column justify-content-center align-items-center">
          <div className="text-white mt-5 mb-3">
            <h2>Commands</h2>
          </div>

          {/* Table */}
          <div className="w-100">
            <Row className="commands-table commands-header text-white font-weight-bold">
              <Col>COMMANDS</Col>
              <Col>DESCRIPTION</Col>
              <Col>USAGE</Col>
            </Row>

            {COMMANDS_LIST.map((command, idx) => (
              <Row key={`commands-${idx}`} className="commands-table commands-row">
                <Col>{command.command}</Col>
                <Col>{command.desciprtion}</Col>
                <Col>{command.usage}</Col>
              </Row>
            ))}
          </div>
        </div>
      </Container>
    </div>
  );
};

export default Commands;
