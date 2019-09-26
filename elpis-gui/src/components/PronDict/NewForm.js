import React, { Component } from 'react';
import { Link, withRouter } from 'react-router-dom';
import { Formik, Field, ErrorMessage } from 'formik';
import { Button, Form, Input, Divider } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { pronDictNew } from 'redux/actions/pronDictActions';
import { datasetList } from 'redux/actions/datasetActions';
import urls from 'urls'


class NewForm extends Component {

    componentDidMount() {
        this.props.datasetList()
    }

    render() {
        const { t, currentDataset, datasets, pronDictNew } = this.props;

        let defaultDatasetName = ''
        if (currentDataset) {
            defaultDatasetName = currentDataset
        } else if (datasets.length > 0) {
            defaultDatasetName = datasets[0]
        }

        return (

            <Formik
                enableReinitialize
                initialValues={{
                    name: 'pd',
                    dataset_name: defaultDatasetName
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
                    const postData = { name: values.name, dataset_name: values.dataset_name }
                    pronDictNew(postData)
                    this.props.history.push(urls.gui.pronDict.l2s)
                }}
            >
                {({
                    values,
                    errors,
                    handleSubmit,
                    handleChange,
                    /* and other goodies */
                }) => (
                        <Form onSubmit={handleSubmit}>
                            <Form.Field>
                                <Input
                                    label={t('pronDict.new.nameLabel')}
                                    value={values.name}
                                    placeholder={t('pronDict.new.namePlaceholder')}
                                    name="name"
                                    type="text"
                                    onChange={handleChange} />
                                <ErrorMessage component="div" className="error" name="name" />
                            </Form.Field>

                            <Form.Field>
                                <label>select a group of recordings</label>
                                <Field component="select" name="dataset_name">
                                    {datasets.map(name =>
                                        (<option key={name} value={name}>{name}</option>))
                                    }
                                </Field>
                            </Form.Field>

                            <Divider />

                            <Button type="button" onClick={handleSubmit}>
                                {t('common.addNewButton')}
                            </Button>
                        </Form>
                    )}
            </Formik>
        )
    }
}

const mapStateToProps = state => {
    return {
        name: state.pronDict.name,
        currentDataset: state.dataset.name,
        datasets: state.dataset.datasetList
    }
}
const mapDispatchToProps = dispatch => ({
    datasetList: () => {
        dispatch(datasetList())
    },
    pronDictNew: postData => {
        dispatch(pronDictNew(postData))
    }
})
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(translate('common')(NewForm)));
