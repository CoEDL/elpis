import React, {Component} from "react";
import {Button, Divider, Form, Grid, Header, Message, Segment, Table} from "semantic-ui-react";
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

        console.log("Settings.js", settings);

        return (
            <div className="training_settings">
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
                            {currentEngine && currentEngine === "kaldi" && name && settings.ngram &&
                                <>
                                    <Message content={t("model.settings.description")} />
                                    <Message attached content={t("model.settings.ngramDescription")} />
                                    <Formik
                                        className="attached"
                                        enableReinitialize
                                        // This performs magic by preselecting the value in the matching form component
                                        initialValues={{ngram: settings.ngram}}
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
                                            console.log(settings);
                                            console.log(values);

                                            const postData = {settings: {ngram: values.ngram}};

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
                            {currentEngine && currentEngine === "hft" && name &&
                                <>
                                    <Message content={t("model.settings.description")} />
                                    <Formik
                                        className="attached"
                                        enableReinitialize
                                        initialValues={{
                                            word_delimiter_token: settings.word_delimiter_token,
                                            num_train_epochs: settings.num_train_epochs,
                                            min_duration_s: settings.min_duration_s,
                                            max_duration_s: settings.max_duration_s,
                                            learning_rate: settings.learning_rate,
                                            batch_size: settings.batch_size,
                                            debug: settings.debug,
                                            data_split_train: settings.data_split_train,
                                            data_split_val: settings.data_split_val,
                                        }}
                                        validate={values => {
                                            let errors = {};

                                            // TODO add validation
                                            console.log(values);

                                            return errors;
                                        }}
                                        onSubmit={(values) => {
                                            const postData = {settings: {
                                                word_delimiter_token: values.word_delimiter_token,
                                                num_train_epochs: values.num_train_epochs,
                                                min_duration_s: values.min_duration_s,
                                                max_duration_s: values.max_duration_s,
                                                learning_rate: values.learning_rate,
                                                batch_size: values.batch_size,
                                                debug: values.debug,
                                                data_split_train: values.data_split_train,
                                                data_split_val: values.data_split_val,
                                            }};

                                            modelSettings(postData);
                                            this.props.history.push(urls.gui.model.train);
                                        }}
                                    >
                                        {({
                                            values,
                                            handleSubmit,
                                            handleChange,
                                        }) => (
                                            <Form onSubmit={handleChange}>
                                                <Table>
                                                    <Table.Body>
                                                        <Table.Row key="word_delimiter_token">
                                                            <Table.Cell collapsing>
                                                                Word delimiter token
                                                            </Table.Cell>
                                                            <Table.Cell>
                                                                <Field
                                                                    name="word_delimiter_token"
                                                                    placeholder=" "
                                                                    label="Word delimiter"
                                                                />
                                                            </Table.Cell>
                                                        </Table.Row>
                                                        <Table.Row key="num_train_epochs">
                                                            <Table.Cell collapsing>
                                                                Number of epochs
                                                            </Table.Cell>
                                                            <Table.Cell>
                                                                <Field
                                                                    name="num_train_epochs"
                                                                    placeholder="2"
                                                                />
                                                            </Table.Cell>
                                                        </Table.Row>
                                                        <Table.Row key="min_duration_s">
                                                            <Table.Cell collapsing>
                                                                Min duration
                                                            </Table.Cell>
                                                            <Table.Cell>
                                                                <Field
                                                                    name="min_duration_s"
                                                                    placeholder="0"
                                                                />
                                                            </Table.Cell>
                                                        </Table.Row>
                                                        <Table.Row key="max_duration_s">
                                                            <Table.Cell collapsing>
                                                                Max duration
                                                            </Table.Cell>
                                                            <Table.Cell>
                                                                <Field
                                                                    name="max_duration_s"
                                                                    placeholder="60"
                                                                />
                                                            </Table.Cell>
                                                        </Table.Row>
                                                        <Table.Row key="learning_rate">
                                                            <Table.Cell collapsing>
                                                                Learning rate
                                                            </Table.Cell>
                                                            <Table.Cell>
                                                                <Field
                                                                    name="learning_rate"
                                                                    placeholder="1e-4"
                                                                />
                                                            </Table.Cell>
                                                        </Table.Row>
                                                        <Table.Row key="batch_size">
                                                            <Table.Cell collapsing>
                                                                Batch size
                                                            </Table.Cell>
                                                            <Table.Cell>
                                                                <Field
                                                                    name="batch_size"
                                                                    placeholder="4"
                                                                />
                                                            </Table.Cell>
                                                        </Table.Row>
                                                        <Table.Row key="debug">
                                                            <Table.Cell collapsing>
                                                                Debug using a subset of the data
                                                            </Table.Cell>
                                                            <Table.Cell>
                                                                <Grid className="settings_debug">
                                                                    <Grid.Column width={2}>
                                                                        <Field
                                                                            type="checkbox"
                                                                            name="debug"
                                                                        />
                                                                    </Grid.Column>
                                                                    {values && values.debug &&
                                                                        <Grid.Column
                                                                            width={14}
                                                                            className="data_split_inputs"
                                                                        >
                                                                            <Grid.Row>
                                                                                <Field name="data_split_train" />
                                                                                <span>
                                                                                    Number of items for training
                                                                                </span>
                                                                            </Grid.Row>
                                                                            <Grid.Row>
                                                                                <Field name="data_split_val" />
                                                                                <span>
                                                                                    Number of items for validation
                                                                                </span>
                                                                            </Grid.Row>
                                                                        </Grid.Column>
                                                                    }
                                                                </Grid>
                                                            </Table.Cell>
                                                        </Table.Row>
                                                    </Table.Body>
                                                </Table>
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
