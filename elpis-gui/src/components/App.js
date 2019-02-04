import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import './App.css';
import {
    StepWelcome,
    StepNaming,
    StepAddData,
    StepDataPreparation,
    StepDataPreparationError,
    StepBuildPronunciationDictionary,
    StepModelSettings,
    StepModelTraining,
    StepTrainingSuccess,
    StepTrainingError,
    StepNewTranscription,
    StepNewTranscriptionResults
} from './steps/index';
import PageContainer from './PageContainer';


class App extends Component {
    render() {
        return (
            <div className="App">
                <Router>
                    <PageContainer>
                        <Route exact path="/" component={ StepWelcome } />

                        <Route path="/naming" component={ StepNaming } />
                        <Route path="/add-data" component={ StepAddData } />
                        <Route path="/data-preparation" component={ StepDataPreparation } />
                        <Route path="/data-preparation-error" component={ StepDataPreparationError } />
                        <Route path="/build-pronunciation-dictionary" component={ StepBuildPronunciationDictionary } />

                        <Route path="/model-settings" component={ StepModelSettings } />
                        <Route path="/model-training" component={ StepModelTraining } />
                        <Route path="/training-success" component={ StepTrainingSuccess } />
                        <Route path="/training-error" component={ StepTrainingError } />

                        <Route path="/new-transcription" component={ StepNewTranscription } />
                        <Route path="/transcription-results" component={ StepNewTranscriptionResults } />
                    </PageContainer>
                </Router>
            </div>
        );
    }
}



export default App;
