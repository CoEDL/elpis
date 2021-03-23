import React, {Component} from "react";
import {withRouter} from "react-router-dom";
import {Formik, ErrorMessage} from "formik";
import {Form, Input, Button} from "semantic-ui-react";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import {datasetNew} from "redux/actions/datasetActions";
import urls from "urls";


class NewForm extends Component {

     render() {
        const {t, error, datasetNew} = this.props;
        return (

            <Formik
                enableReinitialize
                initialValues={{
                    name: "ds",
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
                    const postData = {name: values.name};
                    datasetNew(postData, this.props.history);
                }}
            >
                {({
                    values,
                    handleSubmit,
                    handleChange,
                }) => (
                        <Form onSubmit={handleSubmit}>
                            <Form.Field>
                                <Input
                                    label={t("dataset.new.nameLabel")}
                                    value={values.name}
                                    placeholder={t("dataset.new.namePlaceholder")}
                                    name="name"
                                    type="text"
                                    onChange={handleChange}
                                />
                                <ErrorMessage component="div" className="error" name="name" />
                            </Form.Field>
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
        name: state.dataset.name,
        error: state.dataset.error,
    };
};
const mapDispatchToProps = dispatch => ({
    datasetNew: (name, history) => {
        dispatch(datasetNew(name, history))
            .then(response => {
                if (response.status === 500) {
                    throw Error(response.error);
                }
                return response;
            })
            .then(() => {
                history.push(urls.gui.dataset.files);
            })
            .catch(error => console.log("error", error));
    },
});
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(
    withTranslation("common")(NewForm)
));
