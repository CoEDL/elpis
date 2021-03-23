import React, {Component} from "react";
import {withRouter} from "react-router-dom";
import {Formik, Field, ErrorMessage} from "formik";
import {Button, Form, Input} from "semantic-ui-react";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import {interfaceObjectNames} from "redux/actions/configActions";
import {modelNew} from "redux/actions/modelActions";
import urls from "urls";


class NewForm extends Component {

    // Get me a list of all the data sets and pron dicts we have
    componentDidMount() {
        const {interfaceObjectNames} = this.props;
        interfaceObjectNames();
    }

    // TODO handle error when attempting to make a new model with no dataset / pron dict selected

    render() {
        const {t, engine, error, currentDataset, datasets, currentPronDict, pronDicts, modelNew} = this.props;
        /**
         *  If we have a current dataset or pron-dict, pre-select them in the form,
         *  else preselect the first item in each list.
         *  This allows the values to be passed to onsubmit without having to explicitly select either
        */
        let defaultDatasetName = "";
        if (currentDataset) {
            defaultDatasetName = currentDataset;
        } else if (datasets.length > 0) {
            defaultDatasetName = datasets[0];
        }
        let defaultPronDictName = "";
        if (currentPronDict) {
            defaultPronDictName = currentPronDict;
        } else if (pronDicts.length > 0) {
            defaultPronDictName = pronDicts[0].name;
        }

        return (
            <Formik
                enableReinitialize
                initialValues={{
                    name: "m",
                    dataset_name: defaultDatasetName,
                    pron_dict_name: defaultPronDictName,
                }}
                validate={values => {
                    let errors = {};
                    if (!values.name) {
                        errors.name = "Required";
                    } else if (
                        !/^[ 0-9a-zA-Z\-_@]+$/i.test(values.name)
                    ) {
                        errors.name = t("common.invalidCharacterErrorMessage");
                    }
                    return errors;
                }}
                onSubmit={(values) => {
                    const filtered_pd = pronDicts.filter(pd => (pd.name === values.pron_dict_name));
                    const modelData = {name: values.name, engine};
                    if (engine === "kaldi"){
                        // Get the dataset name from the pron dicts setting if we are using Kaldi
                        modelData["pron_dict_name"] = filtered_pd[0].name;
                        modelData["dataset_name"] = filtered_pd[0].dataset_name;
                    } else {
                        // Non-kaldi, use the specified dataset
                        modelData["dataset_name"] = values.dataset_name;
                    }
                    const redirectAfterModel = engine === "kaldi" ? urls.gui.model.settings : urls.gui.model.train;
                    modelNew(modelData, this.props.history, redirectAfterModel);
                }}
            >
                {({
                    values,
                    handleSubmit,
                    handleChange,
                    /* and other goodies */
                }) => (
                        <Form onSubmit={handleSubmit}>
                            <Form.Field>
                                <Input
                                    label={t("model.new.nameLabel")}
                                    value={values.name}
                                    placeholder={t("model.new.namePlaceholder")}
                                    name="name"
                                    type="text"
                                    onChange={handleChange} />
                                <ErrorMessage component="div" className="error" name="name" />
                            </Form.Field>

                            {/* For Kaldi engines, base the model on the pron dict.
                                Pron dicts have single dataset dependency */}
                            {engine && engine === "kaldi" &&
                                <Form.Field>
                                    <label>{t("model.new.selectPronDictLabel")}</label>
                                    <Field component="select" name="pron_dict_name">
                                        {pronDicts.map(pronDict =>
                                            (<option
                                                key={pronDict.name}
                                                value={pronDict.name}>
                                                {pronDict.name} | {pronDict.dataset_name}
                                            </option>))
                                        }
                                    </Field>
                                </Form.Field>
                            }

                            {/* If the engine is not Kaldi, base the model on a dataset only */}
                            {engine && engine !== "kaldi" &&
                                <Form.Field>
                                    <label>{t("model.new.selectDatasetLabel")}</label>
                                    <Field component="select" name="dataset_name">
                                        {datasets.map(dataset =>
                                            (<option key={dataset} value={dataset}>{dataset}</option>))
                                        }
                                    </Field>
                                </Form.Field>
                            }

                            {error &&
                                <p className={"error-message"}>{error}</p>
                            }
                            <Button type="button" onClick={handleSubmit}>
                                {t("common.addNewButton")}
                            </Button>
                        </Form>
                    )}
            </Formik>
        );
    }
}

const mapStateToProps = state => {
    return {
        engine: state.engine.engine,
        name: state.model.name,
        datasets: state.config.datasetList,
        pronDicts: state.config.pronDictList,
        currentDataset: state.dataset.name,
        currentPronDict: state.pronDict.name,
        error: state.model.error,
    };
};
const mapDispatchToProps = dispatch => ({
    interfaceObjectNames: () => {
        dispatch(interfaceObjectNames());
    },
    modelNew: (postData, history, redirectAfterModel) => {
        dispatch(modelNew(postData))
            .then(response => {
                if (response.status === 500) {
                    throw Error(response.error);
                }
                return response;
            })
            .then(() => {
                history.push(redirectAfterModel);
            })
            .catch(error => console.log("error", error));
    },
});
export default withRouter(connect(
    mapStateToProps, mapDispatchToProps)(
        withTranslation("common")(NewForm)
    )
);
