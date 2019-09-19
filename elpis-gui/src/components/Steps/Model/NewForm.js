import React, { Component } from 'react';
import { Link, withRouter } from 'react-router-dom';
import { Formik, Field, ErrorMessage } from 'formik';
import { Button, Form, Input, Divider } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { pronDictList, modelNew } from 'redux/actions';
import urls from 'urls'


class NewForm extends Component {

    // Get me a list of all the data sets and pron dicts we have
    componentDidMount() {
        const { pronDictList } = this.props
        pronDictList()
    }


    render() {
        const { t, name, currentPronDict, pronDicts, modelNew } = this.props;

        /**
         *  If we have a current pron dict, pre-select that in the form,
         *  else preselect the first item in each list.
         *  This allows the values to be passed to onsubmit without having to explicitly select either
        */
        let defaultPronDictName = ''
        if (currentPronDict) {
            defaultPronDictName = currentPronDict
        } else if (pronDicts.length > 0) {
            defaultPronDictName = pronDicts[0]["name"]
        }

        return (
            <Formik
                enableReinitialize
                initialValues={{
                    name: '',
                    pron_dict_name: defaultPronDictName
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
                    const modelData = { name: values.name, pron_dict_name: values.pron_dict_name }
                    console.log("new model onsubmit", modelData)
                    modelNew(modelData)
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
                                <label>{t('model.new.selectPronDictLabel')}</label>
                                <Field component="select" name="pron_dict_name">
                                { pronDicts.map(pronDict =>
                                    (<option key={pronDict.name} value={pronDict.name}>{pronDict.name} ( {pronDict.dataset_name} ) </option>))
                                }
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
        pronDicts: state.pronDict.pronDictList,
        currentPronDict: state.pronDict.name,
    }
}
const mapDispatchToProps = dispatch => ({
    pronDictList: () => {
        dispatch(pronDictList())
    },
    modelNew: (postData) => {
        // need to pass the new name, the selected pron_dict_name. we get its dataset_name in flask
        dispatch(modelNew(postData))
    }
})
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(translate('common')(NewForm)));
