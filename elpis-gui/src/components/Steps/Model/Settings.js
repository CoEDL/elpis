import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Divider, Grid, Header, Segment, Form, Input, Button } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { Formik } from 'formik';
import { modelSettings } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import urls from 'urls'

class ModelSettings extends Component {
    render() {
        const { t, settings, modelSettings } = this.props;
        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 4 }>
                            <Informer />
                        </Grid.Column>

                        <Grid.Column width={ 12 }>

                            <Header as='h1' text='true'>
                                { t('model.settings.title') }
                            </Header>

                            <Divider />

                            <Formik
                                enableReinitialize
                                initialValues={ {
                                    ngram: settings.ngram
                                } }
                                validate={ values => {
                                    let errors = {};
                                    if (!values.ngram) {
                                        errors.ngram = 'Required';
                                    } else if (
                                        !/^[0-9]+$/i.test(values.ngram)
                                    ) {
                                        errors.ngram = 'Invalid ngram';
                                    }
                                    return errors;
                                } }
                                onSubmit={ (values, { setSubmitting }) => {
                                    const newSettings = {...settings, ngram: values.ngram}
                                     // demo
                                    //  setTimeout(() => {
                                    //     alert(JSON.stringify(newSettings, null, 2));
                                    //     setSubmitting(false);
                                    // }, 400);

                                    // redux action
                                    const postData = { settings: newSettings }
                                    modelSettings(postData)

                                    // go to next page
                                    this.props.history.push(urls.gui.model.train)
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
                                                    label={ t('model.settings.ngramLabel') }
                                                    value={ values.ngram }
                                                    name="ngram"
                                                    type="text"
                                                    onChange={ handleChange } />
                                            </Form.Field>
                                            <Button type='submit' onClick={ handleSubmit } >
                                                { t('model.settings.nextButton') }
                                            </Button>
                                        </Form>
                                    ) }
                            </Formik>
                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        settings: state.model.settings
    }
}

const mapDispatchToProps = dispatch => ({
    modelSettings: postData => {
        dispatch(modelSettings(postData));
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(ModelSettings));
