import React, {Component} from "react";
import {Button, Grid, Header, Icon, Label, Segment, Table} from "semantic-ui-react";
import {Link} from "react-router-dom";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import {pronDictDelete, pronDictList, pronDictLoad} from "redux/actions/pronDictActions";
import {datasetLoad} from "redux/actions/datasetActions";
import arraySort from "array-sort";
import Branding from "../Shared/Branding";
import SideNav from "../Shared/SideNav";
import NewForm from "../PronDict/NewForm";
import CurrentPronDictName from "./CurrentPronDictName";
import urls from "urls";

class PronDictDashboard extends Component {
    state = {
        column: null,
        reverse: false,
    }

    componentDidMount() {
        this.props.pronDictList();
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
        const {pronDictLoad} = this.props;
        const postData = {name: values.name};
        const datasetData = {name: values.dataset_name};

        pronDictLoad(postData, datasetData);
    }

    handleDelete = values => {
        const {pronDictDelete} = this.props;
        const postData = {name: values.name};

        pronDictDelete(postData);
    }

    render() {
        const {t, currentEngine, name, list} = this.props;
        const listArray = Array.from(list.keys());
        const {column, direction} = this.state;
        let listEl = <p>{t("pronDict.dashboard.noneMessage")}</p>;

        if (list.length > 0) {
            listEl = (
                <Table sortable celled fixed unstackable>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell
                                sorted={column === "name" ? direction : null}
                                onClick={this.handleSort("name", listArray)}
                            >
                                Name
                            </Table.HeaderCell>
                            <Table.HeaderCell>
                                Recordings
                            </Table.HeaderCell>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {list.map(pronDict => {
                            const className = (pronDict.name === name) ? "pron-dict-label current" : "pron-dict-label";

                            return (
                                <Table.Row key={pronDict.name}>
                                    <Table.Cell>
                                        <Button as="div" labelPosition="left" className="pron-dict-button">
                                            <Label
                                                as="a"
                                                className={className}
                                                onClick={() => this.handleLoad(pronDict)}
                                                basic
                                            >
                                                <div className="pron-dict-truncate">{pronDict.name}</div>
                                            </Label>
                                            <Button icon onClick={() => this.handleDelete(pronDict)}>
                                                <Icon name="trash" />
                                            </Button>
                                        </Button>
                                    </Table.Cell>
                                    <Table.Cell>
                                        {pronDict.dataset_name}
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
                                {t("pronDict.dashboard.title")}
                            </Header>
                            <CurrentPronDictName />
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
                                                    to={urls.gui.pronDict.new}
                                                />
                                            </Segment>
                                            {listEl}
                                            <Button as={Link} to={urls.gui.pronDict.l2s} disabled={!name}>
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
        list: state.pronDict.pronDictList,
        name: state.pronDict.name,
        currentEngine: state.engine.engine,
    };
};
const mapDispatchToProps = dispatch => ({
    pronDictList: () => {
        dispatch(pronDictList());
    },
    pronDictLoad: (pronDictData, datasetData) => {
        dispatch(pronDictLoad(pronDictData))
            .then(() => dispatch(datasetLoad(datasetData)));
    },
    pronDictDelete: (pronDictData) => {
        dispatch(pronDictDelete(pronDictData))
            .then(response => {
                console.log("Pron dict deleted", response);
            })
            .catch(error => console.log("error", error));
    },
});

export default connect(mapStateToProps, mapDispatchToProps)(
    withTranslation("common")(PronDictDashboard)
);
