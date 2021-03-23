import React, {Component} from "react";
import {Button, Grid, Header, Segment, Table} from "semantic-ui-react";
import {Link} from "react-router-dom";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import {modelLoad, modelList} from "redux/actions/modelActions";
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

    render() {
        const {t, currentEngine, name, list} = this.props;
        const {column, direction} = this.state;
        const redirectAfterModel = currentEngine === "kaldi" ?
            urls.gui.model.settings :
            urls.gui.model.train;
        const listEl = list.length > 0 ? (
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
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {list.map(model => {
                        const className = (name === model.name) ? "current" : "";
                        return (
                            <Table.Row key={model.name} className={className}>
                                <Table.Cell>
                                    <Button
                                        className={className}
                                        fluid
                                        onClick={() => this.handleLoad(model)}
                                    >
                                        {model.name}
                                    </Button>
                                </Table.Cell>
                                <Table.Cell>
                                    {model.dataset_name}
                                </Table.Cell>
                                <Table.Cell>
                                    {model.pron_dict_name}
                                </Table.Cell>
                            </Table.Row>
                        );
                    })}
                </Table.Body>
            </Table>) :
            <p>{t("model.dashboard.noneMessage")}</p>;

        return (
            <div>
                <Branding/>
                <Segment>
                    <Grid centered>
                        <Grid.Column width={4}>
                            <SideNav/>
                        </Grid.Column>

                        <Grid.Column width={12}>

                            <Header as="h1">
                                {t("model.dashboard.title")}
                            </Header>

                            <CurrentModelName/>

                            {currentEngine &&
                            <>
                                {list.length === 0 &&
                                    <NewForm/>
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
                                    <Button as={Link} to={redirectAfterModel} disabled={!name}>
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
        currentEngine: state.engine.engine,
    };
};

const mapDispatchToProps = dispatch => ({
    modelList: () => {
        dispatch(modelList());
    },
    modelLoad: (modelData, datasetData, pronDictData) => {
        dispatch(modelLoad(modelData))
            .then(() => dispatch(datasetLoad(datasetData)))
            .then(() => {
                if (pronDictData.name) {
                    return dispatch(pronDictLoad(pronDictData));
                } else {
                    console.log("No pron dict to load for this model");
                }
            });
    },
});

export default connect(mapStateToProps, mapDispatchToProps)(
    withTranslation("common")(ModelDashboard)
);
