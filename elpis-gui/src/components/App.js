import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import './App.css';
import {
    Welcome,
    DataBundleList,
    DataBundleNew,
    DataBundleAddFiles,
    DataBundlePreparation,
    DataBundlePreparationError,
    ModelList,
    ModelNew,
    ModelPronunciationDictionary,
    ModelLexicon,
    ModelSettings,
    ModelTraining,
    ModelTrainingResults,
    ModelTrainingError,
    NewTranscription,
    NewTranscriptionResults
} from './Steps/index';
import PageContainer from './PageContainer';


class App extends Component {
    render() {
        return (
            <div className="App">
                <Router>
                    <PageContainer>
                        <Route exact path="/" component={ Welcome } />

                        <Route exact path="/data-bundles" component={ DataBundleList } />
                        <Route path="/data-bundle/new" component={ DataBundleNew } />
                        <Route path="/data-bundle/files" component={ DataBundleAddFiles } />
                        <Route exact path="/data-bundle/clean" component={ DataBundlePreparation } />
                        <Route path="/data-bundle/preparation/error" component={ DataBundlePreparationError } />

                        <Route exact path="/models" component={ ModelList } />
                        <Route path="/model/new" component={ ModelNew } />
                        <Route path="/model/pronunciation" component={ ModelPronunciationDictionary } />
                        <Route path="/model/lexicon" component={ ModelLexicon } />
                        <Route path="/model/settings" component={ ModelSettings } />
                        <Route exact path="/model/training" component={ ModelTraining } />
                        <Route exact path="/model/training/results" component={ ModelTrainingResults } />
                        <Route exact path="/model/training/error" component={ ModelTrainingError } />

                        <Route path="/transcription/new" component={ NewTranscription } />
                        <Route path="/transcription/results" component={ NewTranscriptionResults } />
                    </PageContainer>
                </Router>
            </div>
        );
    }
}



export default App;
