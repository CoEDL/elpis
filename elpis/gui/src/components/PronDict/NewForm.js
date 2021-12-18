import React, {Component} from "react";
import {withRouter} from "react-router-dom";
import {Formik, Field, ErrorMessage} from "formik";
import {Button, Form, Input} from "semantic-ui-react";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import {pronDictNew} from "redux/actions/pronDictActions";
import {datasetList} from "redux/actions/datasetActions";
import urls from "urls";
import dataset from "redux/reducers/datasetReducer";


class NewForm extends Component {
    componentDidMount() {
        this.props.datasetList();
    }

    render() {
        const {t, currentEngine, error, currentDataset, datasets, pronDictNew} = this.props;
        let defaultDatasetName = "";

        if (currentDataset) {
            defaultDatasetName = currentDataset;
        } else if (datasets.length > 0) {
            defaultDatasetName = datasets[0];
        }

        return (
            <Formik
                enableReinitialize
                initialValues={{
                    name: "pd",
                    dataset_name: defaultDatasetName,
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
                    const postData = {name: values.name, dataset_name: values.dataset_name};

                    pronDictNew(postData, this.props.history);
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
                                label={t("pronDict.new.nameLabel")}
                                value={values.name}
                                placeholder={t("pronDict.new.namePlaceholder")}
                                name="name"
                                type="text"
                                onChange={handleChange}
                            />
                            <ErrorMessage component="div" className="error" name="name" />
                        </Form.Field>
                        {currentEngine && datasets.length === 0 &&
                            <p>{t("pronDict.common.noDatasetsLabel")}</p>
                        }
                        {currentEngine && datasets.length > 0 &&
                            <Form.Field>
                                <label>{t("pronDict.new.select")}</label>
                                <Field component="select" name="dataset_name" disabled={datasets.length === 0}>
                                    {datasets.map(name =>
                                            (<option key={name} value={name}>{name}</option>))
                                        }
                                </Field>
                            </Form.Field>
                        }
                        {error &&
                            <p className={"error-message"}>{error}</p>
                        }
                        <Button type="button" onClick={handleSubmit} disabled={datasets.length === 0}>
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
        name: state.pronDict.name,
        currentDataset: state.dataset.name,
        datasets: state.dataset.datasetList,
        error: state.pronDict.error,
        currentEngine: state.engine.engine,
    };
};
const mapDispatchToProps = dispatch => ({
    datasetList: () => {
        dispatch(datasetList());
    },
    pronDictNew: (postData, history) => {
        dispatch(pronDictNew(postData))
            .then(response => {
                if (response.status === 500) {
                    throw Error(response.error);
                }

                return response;
            })
            .then(() => {
                history.push(urls.gui.pronDict.l2s);
            })
            .catch(error => console.log("error", error));
    },
});

export default withRouter(
    connect(mapStateToProps, mapDispatchToProps)(
        withTranslation("common")(NewForm)
    )
);

