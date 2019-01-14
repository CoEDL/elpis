import React, { Component } from 'react';
import './App.css';
import {
  StepWelcome,
  StepNaming,
} from './steps/index';
import PageContainer from './PageContainer';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      step: this.makeStepWelcome(),
    };
  }

  makeStepWelcome() {
    return <StepWelcome toStepNaming={() => {
      this.setState({step: this.makeStepNaming()});
    }}/>;
  }

  makeStepNaming() {
    return <StepNaming />;
  }

  render() {
    return (
      <div className="App">
        <PageContainer>
          {this.state.step}
        </PageContainer>
      </div>
    );
  }
}



export default App;
