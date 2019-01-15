import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
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
<<<<<<< HEAD
    };
  }

=======
      // step: this.makeStepWelcome()
      step: this.makeStepNewTranscription()
    };
  }

  stepProps = {
    toStepWelcome: () => this.setState({step: this.makeStepWelcome()}),
    toStepBuildDictionary: () => this.setState({step: this.makeStepBuildPronunciationDictionary()}),
    toStepDataPreparation: () => this.setState({step: this.makeStepDataPreparation()}),
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

  makeStepDataPreparation() {
    return (<StepDataPreparation
      {... this.stepProps}
      goBack={() => this.setState({step: this.makeStepAddData()})}
    />);
  }

  makeStepBuildPronunciationDictionary() {
    return (<StepBuildPronunciationDictionary
      {... this.stepProps}
      goBack={() => this.setState({step: this.makeStepDataPreparation()})}
    />);
  }

  makeStepModelSettings() {
    return (<StepModelSettings
      {... this.stepProps}
      goBack={()=> this.setState({step: this.makeStepBuildPronunciationDictionary()})} // no back here
    />);
  }

  makeStepTrainingModel() {
    return (<StepTrainingModel
      {... this.stepProps}
      goBack={()=> this.setState({step: this.makeStepModelSettings()})} // no back here
    />);
  }

  makeStepTrainingSuccess() {
    return (<StepTrainingSuccess
      {... this.stepProps}
      goBack={()=> this.setState({step: this.makeStepTrainingModel()})} // no back here
    />);
  }
  
  makeStepNewTranscription() {
    return (<StepNewTranscription
      {... this.stepProps}
      goBack={()=>this.setState({step: this.makeStepTrainingSuccess()})} // no back here
    />);
  }

  makeStepTranscriptionResults() {
    return (<StepTranscriptionResults
      {... this.stepProps}
      goBack={()=>this.setState({step: this.makeStepNewTranscription()})} // no back here
    />);
  }

  

  

>>>>>>> 1850fa9656fff01d87f6c85d4a2fcf96066fa337
  render() {
    return (
      <div className="App">
        <Router>
          <PageContainer>
            <Route exact path="/" component={StepWelcome} />
            <Route path="/build-pronunciation-dictionary" component={StepBuildPronunciationDictionary} />
            <Route path="/data-preparation" component={StepDataPreparation} />
            <Route path="/naming" component={StepNaming} />
            <Route path="/add-data" component={StepAddData} />
            <Route path="/new-transcription" component={StepNewTranscription} />
            <Route path="/training-success" component={StepTrainingSuccess} />
            <Route path="/transcription-results" component={StepTranscriptionResults} />
            <Route path="/model-settings" component={StepModelSettings} />
            <Route path="/training-model" component={StepTrainingModel} />
          </PageContainer>
        </Router>
      </div>
    );
  }
}



export default App;
