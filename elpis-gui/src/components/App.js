import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import './App.css';
import {
    Welcome,
    DataBundleList,
    DataBundleNew,
    DataBundleFiles,
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
import urls from 'urls'


class App extends Component {
    render() {
        return (
            <div className="App">
                <Router>
                    <PageContainer>
                        <Route path="/" exact component={ Welcome } />

                        <Route path={urls.gui.dataBundle.index} exact component={ DataBundleList } />
                        <Route path={urls.gui.dataBundle.new} component={ DataBundleNew } />
                        <Route path={urls.gui.dataBundle.files} component={ DataBundleFiles } />
                        <Route path={urls.gui.dataBundle.clean} exact component={ DataBundlePreparation } />
                        <Route path={urls.gui.dataBundle.preparationError} component={ DataBundlePreparationError } />

                        <Route path={urls.gui.model.index} exact component={ ModelList } />
                        <Route path={urls.gui.model.new} component={ ModelNew } />
                        <Route path={urls.gui.model.pronunciation} component={ ModelPronunciationDictionary } />
                        <Route path={urls.gui.model.lexicon} component={ ModelLexicon } />
                        <Route path={urls.gui.model.settings} component={ ModelSettings } />
                        <Route path={urls.gui.model.training} exact component={ ModelTraining } />
                        <Route path={urls.gui.model.trainingResults} exact component={ ModelTrainingResults } />
                        <Route path={urls.gui.model.trainingError} exact component={ ModelTrainingError } />

                        <Route path={urls.gui.transcription.new} component={ NewTranscription } />
                        <Route path={urls.gui.transcription.results} component={ NewTranscriptionResults } />
                    </PageContainer>
                </Router>
            </div>
        );
    }
}



export default App;
