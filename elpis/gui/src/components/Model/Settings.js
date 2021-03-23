import React, {Component} from "react";
import {Link} from "react-router-dom";
import {Button, Divider, Form, Grid, Header, Message, Segment} from "semantic-ui-react";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import {Formik, Field} from "formik";
import {modelSettings} from "redux/actions/modelActions";
import Branding from "../Shared/Branding";
import SideNav from "../Shared/SideNav";
import CurrentModelName from "./CurrentModelName";
import urls from "urls";

class ModelSettings extends Component {


    render() {
        const {t, currentEngine, settings, modelSettings, name} = this.props;
        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={4}>
                            <SideNav />
                        </Grid.Column>

                        <Grid.Column width={12}>

                            <Header as="h1" text="true">
                                {t("model.settings.title")}
                            </Header>

                            <CurrentModelName />

                            {!currentEngine &&
                            <p>{t("engine.common.noCurrentEngineLabel")}</p>
                            }

                            {currentEngine && !name &&
                            <p>{t("model.common.noCurrentModelLabel")}</p>
                            }

                            {currentEngine && currentEngine === "espnet" && name &&
                                <div>
                                    <p>No settings for now...</p>
                                    <Button as={Link} to={urls.gui.model.train}>{t("common.nextButton")}</Button>
                                </div>
                            }

                            {currentEngine && currentEngine === "kaldi" && name &&
                            <>
                                <Message content={t("model.settings.description")} />
                                <Message attached content={t("model.settings.ngramDescription")} />
                                <Formik
                                    className="attached"
                                    enableReinitialize
                                    initialValues={{
                                        ngram: settings.ngram,
                                    }}
                                    validate={values => {
                                        let errors = {};
                                        if (!values.ngram) {
                                            errors.ngram = "Required";
                                        } else if (
                                            !/^[0-9]+$/i.test(values.ngram)
                                        ) {
                                            errors.ngram = "Invalid ngram";
                                        }
                                        return errors;
                                    }}
                                    onSubmit={(values) => {
                                        const postData = {ngram: values.ngram};
                                        modelSettings(postData);
                                        this.props.history.push(urls.gui.model.train);
                                    }}
                                >
                                    {({
                                        handleSubmit,
                                        handleChange,
                                    }) => (
                                        <Form onSubmit={handleChange}>
                                            <Field component="select" name="ngram">
                                                <option key="1" value="1">1</option>
                                                <option key="2" value="2">2</option>
                                                <option key="3" value="3">3</option>
                                                <option key="4" value="4">4</option>
                                                <option key="5" value="5">5</option>
                                            </Field>
                                            <Divider />
                                            <Button type="button" onClick={handleSubmit} disabled={!name}>
                                                {t("common.nextButton")}
                                            </Button>
                                        </Form>
                                        ) }
                                </Formik>
                            </>
                            }

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        name: state.model.name,
        settings: state.model.settings,
        currentEngine: state.engine.engine,
    };
};

const mapDispatchToProps = dispatch => ({
    modelSettings: postData => {
        dispatch(modelSettings(postData));
    },
});

export default connect(mapStateToProps, mapDispatchToProps)(
    withTranslation("common")(ModelSettings)
);
