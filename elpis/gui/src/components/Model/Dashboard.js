import React, {Component} from "react";
import {Button, Grid, Header, Icon, Label, Segment, Table} from "semantic-ui-react";
import {Link} from "react-router-dom";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import {modelDelete, modelLoad, modelList} from "redux/actions/modelActions";
import {datasetLoad} from "redux/actions/datasetActions";
import {pronDictLoad} from "redux/actions/pronDictActions";
import arraySort from "array-sort";
import Branding from "../Shared/Branding";
import SideNav from "../Shared/SideNav";
import NewForm from "../Model/NewForm";
import CurrentModelName from "./CurrentModelName";
import urls from "urls";

class ModelDashboard extends Component {
    state = {
        column: null,
        reverse: false,
    }

    componentDidMount() {
        this.props.modelList();
    }

    handleSort = (clickedColumn, data) => () => {
        const {column} = this.state;

        if (column !== clickedColumn) {
            this.setState({
                column: clickedColumn,
                reverse: false,
            });
            arraySort(data, clickedColumn, {reverse: false});
        } else {
            this.setState({reverse: ! this.state.reverse});
            arraySort(data, clickedColumn, {reverse: ! this.state.reverse});
        }
    }

    handleLoad = values => {
        const {modelLoad} = this.props;
        const modelData = {name: values.name};
        const datasetData = {name: values.dataset_name};
        const pronDictData = {name: values.pron_dict_name};

        modelLoad(modelData, datasetData, pronDictData);
    }

    handleDelete = values => {
        const {modelDelete} = this.props;
        const modelData = {name: values.name};

        modelDelete(modelData);
    }

    render() {
        const {t, engine, engineHumanNames, name, list} = this.props;
        const {column, direction} = this.state;
        let listEl = <p>{t("model.dashboard.noneMessage")}</p>;
        const list_sorted = arraySort(list, "name");

        console.log(list_sorted);

        if (list_sorted.length > 0) {
            listEl = (
                <Table sortable celled fixed unstackable>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell
                                sorted={column === "name" ? direction : null}
                                onClick={this.handleSort("name", list)}
                            >
                                Name
                            </Table.HeaderCell>
                            <Table.HeaderCell
                                sorted={column === "engine_name" ? direction : null}
                                onClick={this.handleSort("engine_name", list)}
                            >
                                Type
                            </Table.HeaderCell>
                            <Table.HeaderCell
                                sorted={column === "dataset_name" ? direction : null}
                                onClick={this.handleSort("dataset_name", list)}
                            >
                                Recordings
                            </Table.HeaderCell>
                            <Table.HeaderCell
                                sorted={column === "pron_dict_name" ? direction : null}
                                onClick={this.handleSort("pron_dict_name", list)}
                            >
                                Pronunciation Dictionaries
                            </Table.HeaderCell>
                            <Table.HeaderCell
                                sorted={column === "results" ? direction : null}
                                onClick={this.handleSort("results.comparison_val", list)}
                            >
                                Results
                            </Table.HeaderCell>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {list_sorted.map(model => {
                            const className = (name === model.name) ? "model-label current" : "model-label";

                            return (
                                <Table.Row key={model.name}>
                                    <Table.Cell>
                                        <Button as="div" labelPosition="left" className="model-button">
                                            <Label
                                                as="a"
                                                className={className}
                                                onClick={() => this.handleLoad(model)}
                                                basic
                                            >
                                                <div className="model-truncate">{model.name}</div>
                                            </Label>
                                            <Button icon onClick={() => this.handleDelete(model)}>
                                                <Icon name="trash" />
                                            </Button>
                                        </Button>
                                    </Table.Cell>
                                    <Table.Cell>
                                        {engineHumanNames[model.engine_name]}
                                    </Table.Cell>
                                    <Table.Cell>
                                        {model.dataset_name}
                                    </Table.Cell>
                                    <Table.Cell>
                                        {model.pron_dict_name}
                                    </Table.Cell>
                                    <Table.Cell>
                                        {model.results && model.results.per &&
                                            <>
                                                {model.results.per} (PER)
                                            </>
                                        }
                                        {model.results && model.results.wer &&
                                            <>
                                                {model.results.wer} (WER)
                                            </>
                                        }
                                    </Table.Cell>
                                </Table.Row>
                            );
                        })}
                    </Table.Body>
                </Table>
                );
        }

        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={4}>
                            <SideNav />
                        </Grid.Column>
                        <Grid.Column width={12}>
                            <Header as="h1">
                                {t("model.dashboard.title")}
                            </Header>
                            <CurrentModelName />
                            {engine &&
                                <>
                                    {list.length === 0 &&
                                        <NewForm />
                                    }
                                    {list.length > 0 &&
                                        <>
                                            <Segment>
                                                <Button
                                                    className="add"
                                                    content={t("common.newButton")}
                                                    labelPosition="left"
                                                    icon="add"
                                                    as={Link}
                                                    to={urls.gui.model.new}
                                                />
                                            </Segment>
                                            {listEl}
                                            <Button as={Link} to={urls.gui.model.settings} disabled={!name}>
                                                {t("common.nextButton")}
                                            </Button>
                                        </>
                                    }
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
        list: state.model.modelList,
        engine: state.engine.engine,
        engineHumanNames: state.engine.engine_human_names,
    };
};
const mapDispatchToProps = dispatch => ({
    modelList: () => {
        dispatch(modelList());
    },
    modelLoad: (modelData, datasetData, pronDictData) => {
        dispatch(modelLoad(modelData))
            .then(() => {
                if (datasetData.name) {
                    return dispatch(datasetLoad(datasetData));
                } else {
                    console.log("No dataset to load for this model.");
                }
            })
            .then(() => {
                if (pronDictData.name) {
                    return dispatch(pronDictLoad(pronDictData));
                } else {
                    console.log("No pron dict to load for this model.");
                }
            });
    },
    modelDelete: (modelData) => {
        dispatch(modelDelete(modelData))
            .then(response => {
                console.log("Model deleted", response);
            })
            .catch(error => console.log("error", error));
    },
});

export default connect(mapStateToProps, mapDispatchToProps)(
    withTranslation("common")(ModelDashboard)
);
