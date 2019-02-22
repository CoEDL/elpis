import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import './App.css';
import {
    Welcome,
    DataBundleDashboard,
    DataBundleNew,
    DataBundleFiles,
    DataBundlePrepare,
    DataBundlePrepareError,
    ModelDashboard,
    ModelNew,
    ModelL2S,
    ModelLexicon,
    ModelSettings,
    ModelTrain,
    ModelResults,
    ModelError,
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

                        <Route path={urls.gui.dataBundle.index} exact component={ DataBundleDashboard } />
                        <Route path={urls.gui.dataBundle.new} component={ DataBundleNew } />
                        <Route path={urls.gui.dataBundle.files} component={ DataBundleFiles } />
                        <Route path={urls.gui.dataBundle.prepare} exact component={ DataBundlePrepare } />
                        <Route path={urls.gui.dataBundle.prepareError} component={ DataBundlePrepareError } />

                        <Route path={urls.gui.model.index} exact component={ ModelDashboard } />
                        <Route path={urls.gui.model.new} component={ ModelNew } />
                        <Route path={urls.gui.model.l2s} component={ ModelL2S } />
                        <Route path={urls.gui.model.lexicon} component={ ModelLexicon } />
                        <Route path={urls.gui.model.settings} component={ ModelSettings } />
                        <Route path={urls.gui.model.train} exact component={ ModelTrain } />
                        <Route path={urls.gui.model.results} exact component={ ModelResults } />
                        <Route path={urls.gui.model.error} exact component={ ModelError } />

                        <Route path={urls.gui.transcription.new} component={ NewTranscription } />
                        <Route path={urls.gui.transcription.results} component={ NewTranscriptionResults } />
                    </PageContainer>
                </Router>
            </div>
        );
    }
}



export default App;
