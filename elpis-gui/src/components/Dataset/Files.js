import React, { Component } from 'react';
import { Link, withRouter } from "react-router-dom";
import { Button, Checkbox, Divider, Form, Grid, Header, Icon, Input, List, Message, Segment } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { Formik, ErrorMessage } from 'formik';
import { datasetSettings, datasetPrepare } from 'redux/actions/datasetActions';
import Branding from 'components/Shared/Branding';
import SideNav from 'components/Shared/SideNav';
import FileUpload from './FileUpload';
import CurrentDatasetName from "./CurrentDatasetName";
import urls from 'urls'

class DatasetFiles extends Component {

    handleNextButton = () => {
        const { history, datasetPrepare} = this.props
        datasetPrepare(history)
    }

    render() {

        const { t, name, status, audioFiles, transcriptionFiles, additionalTextFiles, settings, datasetSettings } = this.props;

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
                                    { t('dataset.files.settingsHeader') }
                                </Header>

                                <Message attached content={ t('dataset.files.settingsDescription') } />

                                <Formik
                                    className="attached"
                                    enableReinitialize
                                    initialValues={ {
                                        tier: settings.tier
                                    } }
                                    validate={ values => {
                                        let errors = {};
                                        if (!values.tier) {
                                            errors.tier = 'Required';
                                        } else if (
                                            !/^[ 0-9a-zA-Z\-_@]+$/i.test(values.tier)
                                        ) {
                                            errors.tier = t('dataset.common.invalidCharacterErrorMessage');
                                        }
                                        return errors;
                                    } }
                                    onSubmit={ (values, { setSubmitting }) => {
                                        const postData = { tier: values.tier }
                                        datasetSettings(postData)
                                    } }
                                >
                                    { ({
                                        values,
                                        errors,
                                        dirty,
                                        touched,
                                        handleSubmit,
                                        handleChange,
                                        isSubmitting,
                                        /* and other goodies */
                                    }) => (
                                            <Form onSubmit={ handleSubmit }>
                                                <Form.Field>
                                                    <Input
                                                        label={ t('dataset.files.tierLabel') }
                                                        value={ values.tier }
                                                        name="tier"
                                                        type="text"
                                                        onChange={ handleChange } />
                                                    <ErrorMessage component="div" className="error" name="tier" />
                                                </Form.Field>
                                                <Button type="button" onClick={handleSubmit} disabled={interactionDisabled}>
                                                    { t('dataset.files.saveButton') }
                                                </Button>
                                            </Form>
                                        ) }
                                </Formik>

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
