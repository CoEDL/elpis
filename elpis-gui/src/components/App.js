import React, { Component } from 'react';
import { BrowserRouter as Router, Route} from "react-router-dom";
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
  StepDataPreparationError
} from './steps/index';
import PageContainer from './PageContainer';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }

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
            <Route path="/data-preparation-error" component={StepDataPreparationError} />
          </PageContainer>
        </Router>
      </div>
    );
  }
}



export default App;
