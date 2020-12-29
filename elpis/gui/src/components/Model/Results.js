import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Divider, Grid, Header, Segment, Icon, Button, Table, Modal } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { withTranslation } from 'react-i18next';
import { modelResults } from 'redux/actions/modelActions';
import Branding from '../Shared/Branding';
import SideNav from '../Shared/SideNav';
import CurrentModelName from "./CurrentModelName";

class ModelResults extends Component {
    componentDidMount() {
        const { name, modelResults } = this.props
        if (name) modelResults()
    }

    render() {
        const { t, currentEngine, name, results } = this.props;

        const resultsEl = results ? (
            <Segment>

                <Table celled>
                    <Table.Body>
                        <Table.Row>
                            <Table.Cell>{t('transcription.results.wer')} {results.wer}</Table.Cell>
                            <Table.Cell>{t('transcription.results.per')} {results.per}</Table.Cell>
                            <Table.Cell>{results.count_val}</Table.Cell>
                            <Table.Cell>{t('transcription.results.del')} {results.del_val}</Table.Cell>
                            <Table.Cell>{t('transcription.results.ins')} {results.ins_val}</Table.Cell>
                            <Table.Cell>{t('transcription.results.sub')} {results.sub_val}</Table.Cell>
                        </Table.Row>
                    </Table.Body>
                </Table>
            </Segment>
        ) : (
            <p>{t('model.results.noResults')}</p>
        )

        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 4 }>
                            <SideNav />
                        </Grid.Column>

                        <Grid.Column width={ 12 }>
                            <Header as='h1' text='true'>
                                { t('model.results.title') }
                            </Header>

                            <CurrentModelName />

                            {!currentEngine &&
                              <p>{ t('engine.common.noCurrentEngineLabel') }</p>
                            }

                            {currentEngine && !name &&
                              <p>{ t('model.common.noCurrentModelLabel') }</p>
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
        currentEngine: state.engine.engine
    }
}

const mapDispatchToProps = dispatch => ({
    modelResults: () => {
        dispatch(modelResults());
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(
    withTranslation("common")(ModelResults)
);
