import React, { Component } from 'react';
import { Link, withRouter } from 'react-router-dom';
import { Formik, ErrorMessage } from 'formik';
import { Grid, Header, Segment, Form, Input, Button } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { datasetNew } from 'redux/actions';
import urls from 'urls'


class NewForm extends Component {

    render() {
        const { t, name, datasetNew } = this.props;
        return (

            <Formik
                enableReinitialize
                initialValues={{
                    name: ''
                }}
                validate={values => {
                    let errors = {};
                    if (!values.name) {
                        errors.name = 'Required';
                    } else if (
                        !/^[ 0-9a-zA-Z\-_@]+$/i.test(values.name)
                    ) {
                        errors.name = t('common.invalidCharacterErrorMessage');
                    }
                    return errors;
                }}
                onSubmit={(values, { setSubmitting }) => {
                    const postData = { name: values.name }
                    datasetNew(postData)
                    this.props.history.push(urls.gui.dataset.files)
                }}
            >
                {({
                    values,
                    errors,
                    dirty,
                    touched,
                    handleSubmit,
                    handleChange,
                    isSubmitting,
                    /* and other goodies */
                }) => (
                        <Form onSubmit={handleSubmit}>
                            <Form.Field>
                                <Input
                                    label={t('dataset.new.nameLabel')}
                                    value={values.name}
                                    placeholder={t('dataset.new.namePlaceholder')}
                                    name="name"
                                    type="text"
                                    onChange={handleChange} />
                                <ErrorMessage component="div" className="error" name="name" />
                            </Form.Field>
                            <Button type="button" onClick={handleSubmit}>
                                {t('common.nextButton')}
                            </Button>
                        </Form>
                    )}
            </Formik>
        )
    }
}

const mapStateToProps = state => {
    return {
        name: state.dataset.name
    }
}
const mapDispatchToProps = dispatch => ({
    datasetNew: name => {
        dispatch(datasetNew(name))
    }
})
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(translate('common')(NewForm)));
