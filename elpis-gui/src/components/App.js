import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import './App.css'

import Welcome from './Welcome'
import DatasetDashboard from './Dataset/Dashboard'
import DatasetNew from './Dataset/New'
import DatasetFiles from './Dataset/Files'
import DatasetPrepare from './Dataset/Prepare'
import PronDictDashboard from './PronDict/Dashboard'
import PronDictNew from './PronDict/New'
import PronDictL2S from './PronDict/L2S'
import PronDictLexicon from './PronDict/Lexicon'
import ModelDashboard from './Model/Dashboard'
import ModelNew from './Model/New'
import ModelSettings from './Model/Settings'
import ModelTrain from './Model/Train'
import ModelResults from './Model/Results'
import NewTranscription from './Transcription/New'

import SelectEngine from './Engine/SelectEngine'

import PageContainer from './PageContainer';
import urls from 'urls'


class App extends Component {
    render() {
        return (
            <div className="App">
                <Router>
                    <PageContainer>
                        <Route path="/" exact component={ Welcome } />

                        <Route path={urls.gui.dataset.index} exact component={ DatasetDashboard } />
                        <Route path={urls.gui.dataset.new} component={ DatasetNew } />
                        <Route path={urls.gui.dataset.files} component={ DatasetFiles } />
                        <Route path={urls.gui.dataset.prepare} exact component={ DatasetPrepare } />

                        <Route path={urls.gui.engine.index} exact component={SelectEngine} />

                        <Route path={urls.gui.pronDict.index} exact component={PronDictDashboard} />
                        <Route path={urls.gui.pronDict.new} component={PronDictNew} />
                        <Route path={urls.gui.pronDict.l2s} component={PronDictL2S} />
                        <Route path={urls.gui.pronDict.lexicon} component={PronDictLexicon} />

                        <Route path={urls.gui.model.index} exact component={ ModelDashboard } />
                        <Route path={urls.gui.model.new} component={ ModelNew } />
                        <Route path={urls.gui.model.settings} component={ ModelSettings } />
                        <Route path={urls.gui.model.train} exact component={ ModelTrain } />
                        <Route path={urls.gui.model.results} exact component={ ModelResults } />

                        <Route path={urls.gui.transcription.new} component={ NewTranscription } />
                    </PageContainer>
                </Router>
            </div>
        );
    }
}



export default App;
