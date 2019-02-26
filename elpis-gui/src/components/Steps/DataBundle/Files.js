import React, { Component } from 'react';
import { Link, withRouter } from "react-router-dom";
import { Button, Checkbox, Divider, Form, Grid, Header, Input, List, Message, Segment } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { Formik } from 'formik';
import { dataBundleSettings, dataBundlePrepare } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import FileUpload from './FileUpload';
import CurrentDataBundleName from "./CurrentDataBundleName";
import urls from 'urls'

class DataBundleFiles extends Component {

    handleNextButton = () => {
        this.props.history.push('/data-bundle/prepare')
    }

    render() {

        const { t, name, audioFiles, transcriptionFiles, additionalTextFiles, settings, dataBundleSettings } = this.props;

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
                 t('dataBundle.files.filesHeader')
            ) : null

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

                            <CurrentDataBundleName name={ name } />

                            <Message attached content={ t('dataBundle.files.description') } />

                            <Segment className="attached">
                                <FileUpload />

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
                                        // setTimeout(() => {
                                        //     alert(JSON.stringify(values, null, 2));
                                        //     setSubmitting(false);
                                        // }, 400);

                                        // redux action
                                        const postData = { tier: values.tier }
                                        dataBundleSettings(postData)

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
                                                        label={ t('dataBundle.files.tierLabel') }
                                                        value={ values.tier }
                                                        name="tier"
                                                        type="text"
                                                        onChange={ handleChange } />
                                                </Form.Field>
                                                <Button onClick={ handleSubmit } >
                                                    { t('dataBundle.files.saveButton') }
                                                </Button>
                                            </Form>
                                        ) }
                                </Formik>

                            </Segment>

                            <Divider />

                            <Button onClick={ this.handleNextButton }>
                                { t('dataBundle.files.nextButton') }
                            </Button>
                            {/*
                            <Button as={ Link } to="/data-bundle/prepare/error">
                                { t('dataBundle.files.nextButtonError') }
                            </Button>
 */}
                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}


const mapStateToProps = state => {
    return {
        name: state.dataBundle.name,
        audioFiles: state.dataBundle.audioFiles,
        transcriptionFiles: state.dataBundle.transcriptionFiles,
        additionalTextFiles: state.dataBundle.additionalTextFiles,
        settings: state.dataBundle.settings
    }
}

const mapDispatchToProps = dispatch => ({
    dataBundleSettings: postData => {
        dispatch(dataBundleSettings(postData));
    },
    dataBundlePrepare: () => {
        dispatch(dataBundlePrepare());
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
