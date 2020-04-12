import React, { Component } from 'react';
import { Link, withRouter } from "react-router-dom";
import { Button, Checkbox, Divider, Form, Grid, Header, Icon, Input, List, Message, Segment } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { Formik, Field, ErrorMessage } from 'formik';
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
        history.push(urls.gui.dataset.prepare)
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

        const writeCountOptions = []
        for (var i = 1; i <= settings.tier_max_count; i++) {
            writeCountOptions.push(
                <option key={i} value={i}>{i}</option>
            )
        }

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

                                <Formik
                                    className="attached"
                                    enableReinitialize
                                    initialValues={ {
                                        tier_types: settings.tier_types,
                                        tier_type: settings.tier_type,
                                        tier_names: settings.tier_names,
                                        tier_name: settings.tier_name,
                                        tier_orders: settings.tier_orders,
                                        tier_order: settings.tier_order,
                                        punctuation_to_explode_by: settings.punctuation_to_explode_by
                                    } }
                                    validate={ values => {
                                        let errors = {};
                                        // if (!values.tier) {
                                        //     errors.tier = 'Required';
                                        // } else if (
                                        //     !/^[ 0-9a-zA-Z\-_@]+$/i.test(values.tier)
                                        // ) {
                                        //     errors.tier = t('dataset.common.invalidCharacterErrorMessage');
                                        // }
                                        return errors;
                                    } }
                                    onSubmit={ (values, { setSubmitting }) => {
                                        const postData = {
                                            tier_type: values.tier_type,
                                            tier_name: values.tier_name,
                                            tier_order: values.tier_order,
                                            punctuation_to_explode_by: values.punctuation_to_explode_by
                                        }
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
                                        setFieldValue
                                        /* and other goodies */
                                    }) => (
                                            <Form onSubmit={handleSubmit}>

                                                <Header as='h4'>
                                                    {t('dataset.files.settingsTierHeader')}
                                                </Header>

                                                <Message attached content={t('dataset.files.tierOrderDescription')} />
                                                <Form.Field>
                                                    <Field component="select" name="tier_order" onChange={e => {
                                                        setFieldValue('tier_type', '');
                                                        setFieldValue('tier_name', '');
                                                        setFieldValue('tier_order', e.target.value);
                                                        console.log("setting tier order", e.target.value)
                                                    }}>
                                                        <option></option>
                                                        {writeCountOptions}
                                                    </Field>
                                                </Form.Field>

                                                <Message attached content={t('dataset.files.tierTypeDescription')} />
                                                <Form.Field>
                                                    <Field component="select" name="tier_type" onChange={e => {
                                                        setFieldValue('tier_type', e.target.value);
                                                        setFieldValue('tier_name', '');
                                                        setFieldValue('tier_order', '');
                                                    }}>
                                                        <option></option>
                                                        {values.tier_types.map(name =>
                                                            (<option key={name} value={name}>{name}</option>))
                                                        }
                                                    </Field>
                                                </Form.Field>

                                                <Message attached content={t('dataset.files.tierNameDescription')} />
                                                <Form.Field>
                                                    <Field component="select" name="tier_name" onChange={e => {
                                                        setFieldValue('tier_type', '');
                                                        setFieldValue('tier_order', '');
                                                        setFieldValue('tier_name', e.target.value);
                                                    }}>
                                                        <option></option>
                                                        {values.tier_names.map(name =>
                                                            (<option key={name} value={name}>{name}</option>))
                                                        }
                                                    </Field>
                                                </Form.Field>

                                                <Header as='h4'>
                                                    {t('dataset.files.settingsPunctuationHeader')}
                                                </Header>

                                                <Message attached content={t('dataset.files.puncDescription')} />
                                                <Form.Field>
                                                    <Input
                                                        label={t('dataset.files.puncLabel')}
                                                        value={values.punctuation_to_explode_by}
                                                        name="punctuation_to_explode_by"
                                                        type="text"
                                                        onChange={handleChange} />
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
