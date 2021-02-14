import './App.css';

import StackList from "./StackList";
import StackDetail from "./StackDetail";
import { useState } from 'react';
import { apiURL } from './api';
import Navbar from "react-bootstrap/Navbar";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFire } from '@fortawesome/free-solid-svg-icons'
import { Container, Row, Col } from 'react-bootstrap';

function App() {
  const [selectedStack, selectStack] = useState(null);
  return (
    <div className="App">
      <Navbar bg="dark" variant="dark">
        <Navbar.Brand href="#home">
          <div>
            <FontAwesomeIcon icon={faFire} color={"red"}/>{' '}
            PyroVision UI - Connected to {apiURL}
          </div>
        </Navbar.Brand>
      </Navbar>
      <Container fluid style={{marginTop: 20}}>
        <Row>
          <Col><StackList selectStack={selectStack}/></Col>
          {selectedStack !== null ? <Col><StackDetail stack={selectedStack} /></Col> : <></>}
        </Row>
      </Container>
    </div>
  );
}

export default App;
