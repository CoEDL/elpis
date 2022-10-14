import React, {Component} from "react";
import {Grid, Header, Segment, Table, Message} from "semantic-ui-react";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import {modelResults} from "redux/actions/modelActions";
import Branding from "../Shared/Branding";
import SideNav from "../Shared/SideNav";
import CurrentModelName from "./CurrentModelName";
import DownloadButton from "./DownloadButton";

class ModelResults extends Component {
    componentDidMount() {
        const {name, modelResults} = this.props;

        if (name) modelResults();
    }

    render() {
        const {t, currentEngine, name, results} = this.props;
        const resultsEl = results ? (
            <>
                <Message attached content={t("model.results.description")} />
                <Table celled className="attached">
                    <Table.Body>
                        {currentEngine && currentEngine === "hft" &&
                            <>
                                <Table.Row>
                                    <Table.Cell>
                                        {t("model.results.hft.wer")}
                                    </Table.Cell>
                                    <Table.Cell>
                                        {results.wer}
                                    </Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>
                                        {t("model.results.hft.eval_loss")}
                                    </Table.Cell>
                                    <Table.Cell>
                                        {results.eval_loss}
                                    </Table.Cell>
                                </Table.Row>
                            </>
                        }
                        {currentEngine && currentEngine === "kaldi" &&
                            <>
                                <Table.Row>
                                    <Table.Cell>
                                        {t("model.results.kaldi.count")}
                                    </Table.Cell>
                                    <Table.Cell>
                                        {results.count_val}
                                    </Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>
                                        {t("model.results.kaldi.del")}
                                    </Table.Cell>
                                    <Table.Cell>
                                        {results.del_val}
                                    </Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>
                                        {t("model.results.kaldi.ins")}
                                    </Table.Cell>
                                    <Table.Cell>
                                        {results.ins_val}
                                    </Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>
                                        {t("model.results.kaldi.sub")}
                                    </Table.Cell>
                                    <Table.Cell>
                                        {results.sub_val}
                                    </Table.Cell>
                                </Table.Row>
                            </>
                        }
                    </Table.Body>
                </Table>
            </>
        ) : (
            <p>{t("model.results.noResults")}</p>
        );

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
                                {t("model.results.title")}
                            </Header>
                            <CurrentModelName />
                            {!currentEngine &&
                                <p>{t("engine.common.noCurrentEngineLabel")}</p>
                            }
                            {currentEngine && !name &&
                                <p>{t("model.common.noCurrentModelLabel")}</p>
                            }
                            {currentEngine && name &&
                                resultsEl
                            }
                        </Grid.Column>
                    </Grid>
                    {currentEngine && name && currentEngine === "hft" &&
                        <DownloadButton />
                    }
                </Segment>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        name: state.model.name,
        results: state.model.results,
        currentEngine: state.engine.engine,
    };
};
const mapDispatchToProps = dispatch => ({
    modelResults: () => {
        dispatch(modelResults());
    },
});

export default connect(mapStateToProps, mapDispatchToProps)(
    withTranslation("common")(ModelResults)
);
