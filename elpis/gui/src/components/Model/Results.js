import React, {Component} from "react";
import {Grid, Header, Segment, Table, Message} from "semantic-ui-react";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import {modelResults} from "redux/actions/modelActions";
import Branding from "../Shared/Branding";
import SideNav from "../Shared/SideNav";
import CurrentModelName from "./CurrentModelName";

class ModelResults extends Component {
    componentDidMount() {
        const {name, modelResults} = this.props;
        if (name) modelResults();
    }

    render() {
        const {t, currentEngine, name, results} = this.props;

        console.log("currentEngine", currentEngine);
        console.log("results", results);

        const wer_text = currentEngine === "kaldi" ? t("model.results.kaldi.wer") : t("model.results.espnet.wer");
        const count_text = currentEngine === "kaldi" ? t("model.results.kaldi.count") : t("model.results.espnet.count");
        const per_text = t("model.results.espnet.per");
        const del_text = currentEngine === "kaldi" ? t("model.results.kaldi.del") : t("model.results.espnet.del");
        const ins_text = currentEngine === "kaldi" ? t("model.results.kaldi.ins") : t("model.results.espnet.ins");
        const sub_text = currentEngine === "kaldi" ? t("model.results.kaldi.sub") : t("model.results.espnet.sub");

        const resultsEl = results ? (
            <>

                <Message attached content={t("model.results.description")} />

                <Table celled className="attached">
                    <Table.Body>

                        <Table.Row>
                            <Table.Cell className="results-title">
                                {wer_text}
                            </Table.Cell>
                            <Table.Cell className="results-title">
                                {results.wer}
                                {results.wer &&
                                <>%</>
                                }
                            </Table.Cell>
                        </Table.Row>

                        <Table.Row>
                            <Table.Cell>
                                {count_text}
                            </Table.Cell>
                            <Table.Cell>
                                {results.count_val}
                            </Table.Cell>
                        </Table.Row>

                        {currentEngine && currentEngine === "espnet" &&
                            <Table.Row>
                                <Table.Cell>
                                    {per_text}
                                    {results.per}
                                </Table.Cell>
                            </Table.Row>
                        }

                        <Table.Row>
                            <Table.Cell>
                                {del_text}
                            </Table.Cell>
                            <Table.Cell>
                                {results.del_val}
                            </Table.Cell>
                        </Table.Row>

                        <Table.Row>
                            <Table.Cell>
                                {ins_text}
                            </Table.Cell>
                            <Table.Cell>
                                {results.ins_val}
                            </Table.Cell>
                        </Table.Row>

                        <Table.Row>
                            <Table.Cell>
                                {sub_text}
                            </Table.Cell>
                            <Table.Cell>
                                {results.sub_val}
                            </Table.Cell>
                        </Table.Row>
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
