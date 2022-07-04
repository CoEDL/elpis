import React, {Component} from "react";
import {Link} from "react-router-dom";
import {Button, Grid, Header, Icon, Segment, Table, Tab} from "semantic-ui-react";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import arraySort from "array-sort";
import Branding from "../Shared/Branding";
import SideNav from "../Shared/SideNav";
import CurrentDatasetName from "./CurrentDatasetName";
import urls from "urls";

class DatasetPrepare extends Component {
    state = {
        column: null,
        reverse: false,
    }

    componentDidMount() {
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
            this.setState({
                reverse: !this.state.reverse,
            });
            arraySort(data, clickedColumn, {reverse: ! this.state.reverse});
        }
    }

    render() {
        const {t, additionalTextFiles, currentEngine, name, status, wordlist} = this.props;
        const {column, direction} = this.state;
        const interactionDisabled = (this.props.name && wordlist.length > 0) ? false : true;
        let listEl = null;

        if (wordlist.length > 0) {
            listEl = (
                <Table sortable celled fixed unstackable>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell
                                sorted={column === "name" ? direction : null}
                                onClick={this.handleSort("name", wordlist)}
                            >
                                {t("dataset.prepare.wordlistHeader")}
                            </Table.HeaderCell>
                            <Table.HeaderCell
                                sorted={column === "frequency" ? direction : null}
                                onClick={this.handleSort("frequency", wordlist)}
                            >
                                {t("dataset.prepare.frequencyHeader")}
                            </Table.HeaderCell>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {
                            wordlist.map(word => {
                                return (
                                    <Table.Row key={word.name}>
                                        <Table.Cell>
                                            {word.name}
                                        </Table.Cell>
                                        <Table.Cell>
                                            {word.frequency}
                                        </Table.Cell>
                                    </Table.Row>
                                );
                            })
                        }
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
                            <Header as="h1">{t("dataset.prepare.title")}</Header>
                            <CurrentDatasetName />
                            {!currentEngine &&
                                <p>{t("engine.common.noCurrentEngineLabel")}</p>
                            }
                            {currentEngine && !name &&
                                <p>{t("dataset.common.noCurrentDatasetLabel")}</p>
                            }
                            {status === "ready" &&
                                <p>{t("dataset.prepare.ready")}</p>
                            }
                            {status === "loaded" &&
                                <p>
                                    <Icon name="circle notched" size="big" loading />
                                    {t("dataset.prepare.preparing")}
                                </p>
                            }
                            {status === "wordlist-prepared" &&
                                <>
                                    <h3>{t("dataset.prepare.header")}</h3>
                                    {additionalTextFiles.length > 0 &&
                                        <p>{t("dataset.prepare.description")}</p>
                                    }
                                    <Button
                                        as={Link}
                                        disabled={interactionDisabled}
                                        to={(currentEngine === "kaldi") ?
                                            urls.gui.pronDict.index :
                                            urls.gui.model.index}
                                    >
                                        {t("common.nextButton")}
                                    </Button>
                                    {listEl}
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
        name: state.dataset.name,
        currentEngine: state.engine.engine,
        wordlist: state.dataset.wordlist,
        additionalTextFiles: state.dataset.additionalTextFiles,
        status: state.dataset.status,
    };
};

export default connect(mapStateToProps)(
    withTranslation("common")(DatasetPrepare)
);
