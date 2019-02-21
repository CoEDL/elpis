import React, { Component } from 'react';
import { Link, withRouter } from "react-router-dom";
import { Checkbox, Grid, Header, Segment, Icon, List, Form, Input, Button } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { replaceFiles, triggerApiWaiting, dataBundleSettings } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import FileUpload from './FileUpload';
import { Formik } from 'formik';
import urls from 'urls'

class DataBundleFiles extends Component {

    handleFilesReplaceToggle = () => {
        this.props.replaceFiles()
    }

    handleNextButton = () => {
        this.props.triggerApiWaiting('preparing data')
        this.props.history.push('/data-bundle/prepare')
    }

    render() {

        const { t, audioFiles, transcriptionFiles, additionalTextFiles, replace, settings, dataBundleSettings } = this.props;

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

        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 4 }>
                            <Informer />
                        </Grid.Column>

                        <Grid.Column width={ 12 }>
                            <Header as='h1'>
                                { t('dataBundle.files.title') }
                            </Header>

                            <p>
                                { t('dataBundle.files.description') }
                            </p>

                            <Segment>
                                <FileUpload />

                                {/*
                                TODO: change implementation to have a remove all files button instead
                                <Checkbox
                                    toggle
                                    onChange={ this.handleFilesReplaceToggle }
                                    defaultChecked={ replace }
                                    label={ t('dataBundle.files.filesReplaceLabel') }
                                />
                                */}

                                <Header as='h3'>
                                    { t('dataBundle.files.filesHeader') }
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
                                    { t('dataBundle.files.settingsHeader') }
                                </Header>
                                { t('dataBundle.files.settingsDescription') }




                                <Formik
                                    enableReinitialize
                                    initialValues={ {
                                        tier: settings.tier
                                    } }
                                    validate={ values => {
                                        let errors = {};
                                        if (!values.tier) {
                                            errors.tier = 'Required';
                                        } else if (
                                            !/^[A-Za-z ]+$/i.test(values.tier)
                                        ) {
                                            errors.tier = 'Invalid tier name';
                                        }
                                        return errors;
                                    } }
                                    onSubmit={ (values, { setSubmitting }) => {
                                        // demo
                                        setTimeout(() => {
                                            alert(JSON.stringify(values, null, 2));
                                            setSubmitting(false);
                                        }, 400);

                                        // redux action

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
                                                    <Input label={ t('dataBundle.files.tierLabel') } value={ values.tier } name="tier" type="text" onChange={ handleChange } />
                                                </Form.Field>
                                                <Button type='submit' onClick={ handleSubmit } >
                                                    { t('dataBundle.files.saveButton') }
                                                </Button>
                                            </Form>
                                        ) }
                                </Formik>


                            </Segment>

                            <Grid container>
                                <Button type='submit' onClick={ this.handleNextButton }>
                                    { t('dataBundle.files.nextButton') }
                                </Button>
                                <Button type='submit' as={ Link } to="/data-bundle/prepare/error" icon>
                                    <Icon name='warning sign' />
                                    { t('dataBundle.files.nextButtonError') }
                                </Button>
                            </Grid>
                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}


const mapStateToProps = state => {
    return {
        audioFiles: state.dataBundle.audioFiles,
        transcriptionFiles: state.dataBundle.transcriptionFiles,
        additionalTextFiles: state.dataBundle.additionalTextFiles,
        replace: state.dataBundle.replaceFiles,
        settings: state.dataBundle.settings
    }
}

const mapDispatchToProps = dispatch => ({
    replaceFiles: () => {
        dispatch(replaceFiles());
    },
    triggerApiWaiting: message => {
        dispatch(triggerApiWaiting(message));
    },
    dataBundleSettings: postData => {
        dispatch(dataBundleSettings(postData));
    }

})

export default withRouter(
    connect(
        mapStateToProps,
        mapDispatchToProps
    )(
        translate('common')(DataBundleFiles)
    )
);
