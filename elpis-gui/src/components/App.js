import React, { Component } from 'react';
import './App.css';
import {
  StepWelcome,
  StepBuildPronunciationDictionary,
  StepDataPreparation,
  StepNaming,
  StepAddData,
  StepNewTranscription,
  StepTrainingSuccess,
  StepTranscriptionResults,
  StepModelSettings,
  StepTrainingModel,
} from './steps/index';
import PageContainer from './PageContainer';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      // step: this.makeStepWelcome(),
      step: this.makeStepAddData()
    };
  }

  makeStepWelcome() {
    return (<StepWelcome
      toStepNaming={() => this.setState({step: this.makeStepNaming()})}
      toStepNewTranscription={() => this.setState({step: this.makeStepNewTranscription()})}
      goBack={()=>{}} // no back here
    />);
  }

  makeStepNaming() {
    return (<StepNaming
      toStepAddData={() => this.setState({step: this.makeStepAddData()})}
      goBack={() => this.setState({step: this.makeStepWelcome()})}
    />);
  }

  makeStepAddData() {
    return (<StepAddData 
    toStepDataPreparation={() => this.setState({step: this.makeStepDataPreparation()})}
    goBack={() => this.setState({step: this.makeStepNaming()})}
    />);
  }

  makeStepDataPreparation() {
    return (<StepDataPreparation />);
  }

  makeStepBuildPronunciationDictionary() {
    return (<StepBuildPronunciationDictionary />);
  }

  makeStepNewTranscription() {
    return (<StepNewTranscription />);
  }

  makeStepTrainingSuccess() {
    return (<StepTrainingSuccess />);
  }

  makeStepTranscriptionResults() {
    return (<StepTranscriptionResults />);
  }

  makeStepModelSettings() {
    return (<StepModelSettings />);
  }

  makeStepTrainingModel() {
    return (<StepTrainingModel />);
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
