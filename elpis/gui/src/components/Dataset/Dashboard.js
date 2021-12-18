import React, {Component} from "react";
import {Button, Grid, Header, Icon, Label, Segment, Table} from "semantic-ui-react";
import {Link} from "react-router-dom";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import {datasetDelete, datasetList, datasetLoad} from "redux/actions/datasetActions";
import arraySort from "array-sort";
import Branding from "../Shared/Branding";
import SideNav from "../Shared/SideNav";
import NewForm from "./NewForm";
import CurrentDatasetName from "./CurrentDatasetName";
import urls from "urls";

class DatasetDashboard extends Component {
    state = {
        column: null,
        reverse: false,
    }

    componentDidMount() {
        this.props.datasetList();
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

    handleLoad = name => {
        const {datasetLoad} = this.props;
        const postData = {name: name};

        datasetLoad(postData);
    }

    handleDelete = name => {
        const {datasetDelete} = this.props;
        const postData = {name: name};

        datasetDelete(postData);
    }

    render() {
        const {t, currentEngine, name, list} = this.props;
        const {column, direction} = this.state;
        let listEl;

        if (list.length > 0) {
            listEl = (
                <Table sortable celled fixed unstackable className="choose-dataset">
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell
                                sorted={column === "name" ? direction : null}
                                onClick={this.handleSort("name", list)}
                            >
                                Name
                            </Table.HeaderCell>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {list.map(datasetName => {
                            const className = (datasetName === name) ? "dataset-label current" : "dataset-label";

                            return (
                                <Table.Row key={datasetName}>
                                    <Table.Cell>
                                        <Button as="div" labelPosition="left" className="dataset-button">
                                            <Label as="a" className={className} onClick={() => this.handleLoad(datasetName)} basic>
                                                <div className="dataset-truncate">{datasetName}</div>
                                            </Label>
                                            <Button icon onClick={() => this.handleDelete(datasetName)}>
                                                <Icon name="trash" />
                                            </Button>
                                        </Button>
                                    </Table.Cell>
                                </Table.Row>
                            );
                        })}
                    </Table.Body>
                </Table>
            );
        } else {
            listEl = <p>{t("dataset.dashboard.noneMessage")}</p>;
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
                                {t("dataset.dashboard.title")}
                            </Header>
                            <CurrentDatasetName />
                            {currentEngine &&
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
                                                    to={urls.gui.dataset.new}
                                                />
                                            </Segment>
                                            {listEl}
                                            <Button as={Link} to={urls.gui.dataset.files} disabled={!name}>
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
        list: state.dataset.datasetList,
        name: state.dataset.name,
        currentEngine: state.engine.engine,
    };
};
const mapDispatchToProps = dispatch => ({
    datasetList: () => {
        dispatch(datasetList());
    },
    datasetLoad: postData => {
        dispatch(datasetLoad(postData))
            .then(response => {
                console.log("Dataset loaded", response);
            })
            .catch(error => console.log("error", error));
    },
    datasetDelete: postData => {
        dispatch(datasetDelete(postData))
            .then(response => {
                console.log("Dataset deleted", response);
            })
            .catch(error => console.log("error", error));
    },
});

export default connect(mapStateToProps, mapDispatchToProps)(
    withTranslation("common")(DatasetDashboard)
);
