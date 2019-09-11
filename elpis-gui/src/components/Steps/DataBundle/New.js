import React, { Component } from 'react';
import { Link, withRouter } from 'react-router-dom';
import { Grid, Header, Segment, Form, Input, Button } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { Formik, ErrorMessage } from 'formik';
import { dataBundleNew } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import urls from 'urls'

class DataBundleNew extends Component {

    componentDidMount() {}

    render() {
        const { t, name, dataBundleNew } = this.props;
        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 4 }>
                            <Informer />
                        </Grid.Column>

                        <Grid.Column width={ 12 }>
                            <Header as='h1' text="true">
                                { t('dataBundle.new.title') }
                            </Header>

                            <Formik
                                enableReinitialize
                                initialValues={ {
                                    name: ''
                                } }
                                validate={ values => {
                                    let errors = {};
                                    if (!values.name) {
                                        errors.name = 'Required';
                                    } else if (
                                        !/^[ 0-9a-zA-Z\-_@]+$/i.test(values.name)
                                    ) {
                                        errors.name = t('common.invalidCharacterErrorMessage');
                                    }
                                    return errors;
                                } }
                                onSubmit={ (values, { setSubmitting }) => {
                                    const postData = {name:values.name}
                                    dataBundleNew(postData)
                                    this.props.history.push(urls.gui.dataset.files)
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
                                                    label={ t('dataBundle.new.nameLabel') }
                                                    value={ values.name }
                                                    placeholder={ t('dataBundle.new.namePlaceholder') }
                                                    name="name"
                                                    type="text"
                                                    onChange={ handleChange } />
                                                    <ErrorMessage component="div" className="error" name="name" />
                                            </Form.Field>
                                            <Button type="button" onClick={ handleSubmit }>
                                                { t('dataBundle.new.nextButton') }
                                            </Button>
                                        </Form>
                                    ) }
                            </Formik>
                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        )
    }
}

const mapStateToProps = state => {
    return {
        name: state.dataBundle.name
    }
}
const mapDispatchToProps = dispatch => ({
    dataBundleNew: name => {
        dispatch(dataBundleNew(name))
    }
})
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(translate('common')(DataBundleNew)));
