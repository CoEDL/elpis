import React, { Component } from 'react';
import { Link, withRouter } from "react-router-dom";
import { Button, Divider, Grid, Header, Icon, List, Message, Segment, Input, Form } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { datasetSettings, datasetPrepare } from 'redux/actions/datasetActions';
import Branding from 'components/Shared/Branding';
import SideNav from 'components/Shared/SideNav';
import FileUpload from './FileUpload';
import CurrentDatasetName from "./CurrentDatasetName";
import GeneratedUI from './GeneratedUI';
import urls from 'urls'

class DatasetFiles extends Component {

    handleNextButton = () => {
        const { history, datasetPrepare} = this.props
        datasetPrepare(history)
        history.push(urls.gui.dataset.prepare)
    }

    render() {

        const { t, name, status, audioFiles, transcriptionFiles, additionalTextFiles, settings, ui, datasetSettings } = this.props;

        const interactionDisabled = name ? false : true

        const loadingIcon = (status === 'loading') ? (
            <div className="status">
                <Icon name='circle notched' size="big" loading /> Uploading files
            </div>
        ) : null

        const audioFileList = audioFiles.map(file => (
            <List.Item key={ file }>
                <List.Content>{ file }</List.Content>
            </List.Item>
        ))
        const transcriptionFilesList = transcriptionFiles.map(file => (
            <List.Item key={ file }>
                <List.Content>{ file }</List.Content>
            </List.Item>
        ))
        const additionalTextFilesList = additionalTextFiles.map(file => (
            <List.Item key={ file }>
                <List.Content>{ file }</List.Content>
            </List.Item>
        ))

        const filesHeader = (
            audioFileList.length > 0 ||
            transcriptionFilesList.length > 0 ||
            additionalTextFilesList.length > 0) ? (
                 t('dataset.files.filesHeader')
            ) : null

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

                            <Message attached content={ t('dataset.files.description') } />

                            <Segment className="attached">

                                <FileUpload name={name} />

                                <div>{loadingIcon}</div>

                                <Header as='h3'>
                                    { filesHeader }
                                </Header>

                                <Grid columns={ 3 }>
                                    <Grid.Column>
                                        <List>
                                            { audioFileList }
                                        </List>
                                    </Grid.Column>
                                    <Grid.Column>
                                        <List>
                                            { transcriptionFilesList }
                                        </List>
                                    </Grid.Column>
                                    <Grid.Column>
                                        <List>
                                            { additionalTextFilesList }
                                        </List>
                                    </Grid.Column>
                                </Grid>
                            </Segment>
                            <Segment>
                                <Header as='h3'>
                                    { t('dataset.files.importSettingsHeader') }
                                </Header>

                                <GeneratedUI settings={settings} ui={ui} changeSettingsCallback={datasetSettings} />
                            </Segment>
                            <Segment>
                                <Header as='h4'>
                                    { t('dataset.files.generalSettingsHeader') }
                                </Header>
                                <Form>
                                    <Form.Field>
                                        <label>Punctuation to explode by</label>
                                        <Input type='text' />
                                    </Form.Field>
                                    <Form.Field>
                                        <label>Punctuation to collapse by</label>
                                        <Input type='text' />
                                    </Form.Field>
                                </Form>
                            </Segment>

                            <Divider />

                            <Button onClick={this.handleNextButton} disabled={interactionDisabled}>
                                { t('common.nextButton') }
                            </Button>

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
        settings: state.dataset.settings,
        ui: state.dataset.ui,
        status: state.dataset.status
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
    }
})

export default withRouter(
    connect(
        mapStateToProps,
        mapDispatchToProps
    )(
        translate('common')(DatasetFiles)
    )
);
