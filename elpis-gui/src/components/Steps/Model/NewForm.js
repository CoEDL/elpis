import React, { Component } from 'react';
import { Link, withRouter } from 'react-router-dom';
import { Formik, Field, ErrorMessage } from 'formik';
import { Button, Form, Grid, Header, Input, Label, Segment, Select, Divider } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { datasetList, pronDictList, modelNew } from 'redux/actions';
import urls from 'urls'


class NewForm extends Component {

    // Get me a list of all the data sets and pron dicts we have
    componentDidMount() {
        const { datasetList, pronDictList } = this.props
        datasetList()
        pronDictList()
    }


    render() {
        const { t, name, currentDataset, currentPronDict, datasets, pronDicts, modelNew } = this.props;
        /**
         *  If we have a current dataset or pron dict, pre-select that in the form,
         *  else preselect the firest item in each list.
         *  This allows the values to be passed i onsubmit without haivng to explicitly select either
        */
        return (
            <Formik
                enableReinitialize
                initialValues={{
                    name: '',
                    dataset_name: currentDataset ? currentDataset : datasets[0],
                    pron_dict_name: currentPronDict ? currentPronDict : pronDicts[0]
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
                    const postData = { name: values.name, dataset_name: values.dataset_name, pron_dict_name: values.pron_dict_name }
                    modelNew(postData)
                    this.props.history.push(urls.gui.model.settings)
                }}
            >
                {({
                    values,
                    errors,
                    handleSubmit,
                    handleChange
                    /* and other goodies */
                }) => (
                        <Form onSubmit={handleSubmit}>
                            <Form.Field>
                                <Input
                                    label={t('model.new.nameLabel')}
                                    value={values.name}
                                    placeholder={t('model.new.namePlaceholder')}
                                    name="name"
                                    type="text"
                                    onChange={handleChange} />
                                <ErrorMessage component="div" className="error" name="name" />
                            </Form.Field>

                            <Form.Field>
                                <label>{t('model.new.selectDatasetLabel')}</label>
                                <Field component="select" name="dataset_name">
                                    {datasets.map(name =>(<option key={name} value={name}>{name}</option>))}
                                </Field>
                            </Form.Field>

                            <Form.Field>
                                <label>{t('model.new.selectPronDictLabel')}</label>
                                <Field component="select" name="pron_dict_name">
                                    {pronDicts.map(name =>(<option key={name} value={name}>{name}</option>))}
                                </Field>
                            </Form.Field>

                            <Divider />

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
        name: state.model.name,
        datasets: state.dataset.datasetList,
        currentDataset: state.dataset.name,
        pronDicts: state.pronDict.pronDictList,
        currentPronDict: state.pronDict.name,
    }
}
const mapDispatchToProps = dispatch => ({
    datasetList: () => {
        dispatch(datasetList())
    },
    pronDictList: () => {
        dispatch(pronDictList())
    },
    modelNew: postData => {
        dispatch(modelNew(postData))
    }
})
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(translate('common')(NewForm)));
