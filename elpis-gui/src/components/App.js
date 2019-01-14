import React, { Component } from 'react';
import './App.css';
import { StepWelcome } from './steps/index';
import PageContainer from './PageContainer';

class App extends Component {
  render() {
    return (
      <div className="App">
        <PageContainer>
          <StepWelcome />
        </PageContainer>
      </div>
    );
  }
}

export default App;
