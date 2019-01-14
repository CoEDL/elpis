import React, { Component } from 'react';
import './App.css';
import {
  StepWelcome,
  StepBuildPronunciationDictionary,
  StepDataPreperation,
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
      step: this.makeStepWelcome(),
      // step: this.makeStepAddData()
    };
  }

  stepProps = {
    toStepWelcome: () => this.setState({step: this.makeStepWelcome()}),
    toStepBuildPronunciationDictionary: () => this.setState({step: this.makeStepBuildPronunciationDictionary()}),
    toStepDataPreperation: () => this.setState({step: this.makeStepDataPreperation()}),
    toStepNaming: () => this.setState({step: this.makeStepNaming()}),
    toStepAddData: () => this.setState({step: this.makeStepAddData()}),
    toStepNewTranscription: () => this.setState({step: this.makeStepNewTranscription()}),
    toStepTrainingSuccess: () => this.setState({step: this.makeStepTrainingSuccess()}),
    toStepTranscriptionResults: () => this.setState({step: this.makeStepTranscriptionResults()}),
    toStepModelSettings: () => this.setState({step: this.makeStepModelSettings()}),
    toStepTrainingModel: () => this.setState({step: this.makeStepTrainingModel()}),
  };

  makeStepWelcome() {
    return (<StepWelcome
      {... this.stepProps}
      goBack={()=>{}} // no back here
    />);
  }

  makeStepNaming() {
    return (<StepNaming
      {... this.stepProps}
      goBack={() => this.setState({step: this.makeStepWelcome()})}
    />);
  }

  makeStepAddData() {
    return (<StepAddData
      {... this.stepProps}
      goBack={() => this.setState({step: this.makeStepNaming()})}
    />);
  }

  makeStepBuildPronunciationDictionary() {
    return (<StepBuildPronunciationDictionary
      {... this.stepProps}
      goBack={()=>{}} // no back here
    />);
  }

  makeStepDataPreperation() {
    return (<StepDataPreperation
      {... this.stepProps}
      goBack={()=>{}} // no back here
    />);
  }

  makeStepNewTranscription() {
    return (<StepNewTranscription
      {... this.stepProps}
      goBack={()=>{}} // no back here
    />);
  }

  makeStepTrainingSuccess() {
    return (<StepTrainingSuccess
      {... this.stepProps}
      goBack={()=>{}} // no back here
    />);
  }

  makeStepTranscriptionResults() {
    return (<StepTranscriptionResults
      {... this.stepProps}
      goBack={()=>{}} // no back here
    />);
  }

  makeStepModelSettings() {
    return (<StepModelSettings
      {... this.stepProps}
      goBack={()=>{}} // no back here
    />);
  }

  makeStepTrainingModel() {
    return (<StepTrainingModel
      {... this.stepProps}
      goBack={()=>{}} // no back here
    />);
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
