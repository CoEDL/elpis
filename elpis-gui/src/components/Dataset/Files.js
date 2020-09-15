import React, { Component } from 'react';
import { Link, withRouter } from "react-router-dom";
import { Button, Divider, Grid, Header, Icon, List, Message, Segment, Input, Form, Label } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { datasetSettings, datasetPrepare, datasetDelete } from 'redux/actions/datasetActions';
import Branding from 'components/Shared/Branding';
import SideNav from 'components/Shared/SideNav';
import SelectEngine from 'components/Engine/SelectEngine'
import FileUpload from './FileUpload';
import CurrentDatasetName from "./CurrentDatasetName";
import GeneratedUI from './GeneratedUI';
import urls from 'urls'

class DatasetFiles extends Component {

    handleNextButton = () => {
        const { history, datasetPrepare } = this.props
        datasetPrepare(history)
        history.push(urls.gui.dataset.prepare)
    }

    handleDeleteButton = (file) => {
        var deleteData = new FormData()
        deleteData.append('file', file);
        datasetDelete(deleteData)
    }

    render() {

        const { t,
            currentEngine,
            name,
            status,
            audioFiles,
            transcriptionFiles,
            additionalTextFiles,
            importer_name,
            settings,
            ui,
            datasetSettings } = this.props;

        const interactionDisabled = name ? false : true

        const loadingIcon = (status === 'loading') ? (
            <div className="status">
                <Icon name='circle notched' size="big" loading /> Uploading files
            </div>
        ) : null

        const audioFilesList = audioFiles.map(file => (
            <List.Item key={ file }>
                <Button as='div' labelPosition='left'>
                    <Label as='a' basic>
                        { file }
                    </Label>
                    <Button icon onClick={() => this.handleDeleteButton(file)}>
                        <Icon name='trash' />
                    </Button>
                </Button>
            </List.Item>
        ))
        const transcriptionFilesList = transcriptionFiles.map(file => (
            <List.Item key={ file }>
                <Button as='div' labelPosition='left'>
                    <Label as='a' basic>
                        { file }
                    </Label>
                    <Button icon onClick={() => this.handleDeleteButton(file)}>
                        <Icon name='trash' />
                    </Button>
                </Button>
            </List.Item>
        ))
        const additionalTextFilesList = additionalTextFiles.map(file => (
            <List.Item key={ file }>
                <Button as='div' labelPosition='left'>
                    <Label as='a' basic>
                        { file }
                    </Label>
                    <Button icon onClick={() => this.handleDeleteButton(file)}>
                        <Icon name='trash' />
                    </Button>
                </Button>
            </List.Item>
        ))

        const filesHeader = (
            audioFilesList.length > 0 ||
            transcriptionFilesList.length > 0 ||
            additionalTextFilesList.length > 0) ? (
                 t('dataset.files.filesHeader')
            ) : null

        const audioFilesHeader = audioFilesList.length > 0 
            ? t('dataset.files.audioFilesHeader') 
            : null

        const transcriptionFilesHeader = transcriptionFilesList.length > 0 
            ? t('dataset.files.transcriptionFilesHeader') 
            : null

        const additionalTextFilesHeader = additionalTextFilesList.length > 0 
            ? t('dataset.files.additionalTextFilesHeader') 
            : null

        // const writeCountOptions = []
        // for (var i = 1; i <= settings.tier_max_count; i++) {
        //     writeCountOptions.push(
        //         <option key={i} value={i}>{i}</option>
        //     )
        // }

        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 4 }>
                            <SideNav />
                        </Grid.Column>

                        <Grid.Column width={ 12 }>
                            <Header as='h1'>
                                { t('dataset.files.title') }
                            </Header>

                            <CurrentDatasetName />

                            {!currentEngine &&
                              <p>{ t('engine.common.noCurrentEngineLabel') }</p>
                            }

                            {currentEngine && !name &&
                              <p>{ t('dataset.common.noCurrentDatasetLabel') }</p>
                            }

                            {currentEngine && name &&
                                <>
                                <Message attached content={ t('dataset.files.description') } />
                                <Segment className="attached">

                                    <FileUpload name={name} />

                                    <div>{loadingIcon}</div>

                                    {filesHeader &&
                                        <>
                                        <Header as='h3'>
                                            { filesHeader }
                                        </Header>
                                        <div className="file-list">
                                            <Grid columns={3}>
                                                <Grid.Column>
                                                    <Header as='h4'>
                                                        { audioFilesHeader }
                                                    </Header>
                                                    <List>
                                                        { audioFilesList }
                                                    </List>
                                                </Grid.Column>
                                                <Grid.Column>
                                                    <Header as='h4'>
                                                        { transcriptionFilesHeader }
                                                    </Header>
                                                    <List>
                                                        { transcriptionFilesList }
                                                    </List>
                                                </Grid.Column>
                                                <Grid.Column>
                                                    <Header as='h4'>
                                                        { additionalTextFilesHeader }
                                                    </Header>
                                                    <List>
                                                        { additionalTextFilesList }
                                                    </List>
                                                </Grid.Column>
                                            </Grid>
                                        </div>
                                        </>
                                    }

                                </Segment>
                                <Segment>
                                    <Header as='h3'>
                                        { t('dataset.files.importSettingsHeader') }
                                    </Header>
                                    <GeneratedUI settings={settings} ui={ui} changeSettingsCallback={datasetSettings} />
                                </Segment>

                                <Button onClick={this.handleNextButton} disabled={interactionDisabled}>
                                    { t('common.nextButton') }
                                </Button>
                                </>
                            }
                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        name: state.dataset.name,
        audioFiles: state.dataset.audioFiles,
        transcriptionFiles: state.dataset.transcriptionFiles,
        additionalTextFiles: state.dataset.additionalTextFiles,
        importer_name: state.dataset.importer_name,
        settings: state.dataset.settings,
        ui: state.dataset.ui,
        status: state.dataset.status,
        currentEngine: state.engine.engine
    }
}

const mapDispatchToProps = dispatch => ({
    datasetSettings: postData => {
        dispatch(datasetSettings(postData));
    },
    datasetPrepare: (history) => {
        dispatch(datasetPrepare(history))
            .then((response) => {
                history.push(urls.gui.dataset.prepare)
            })
    },
    datasetDelete: postData => {
        dispatch(datasetDelete(postData));
    },
})

export default withRouter(
    connect(
        mapStateToProps,
        mapDispatchToProps
    )(
        translate('common')(DatasetFiles)
    )
)
