import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Divider, Grid, Header, Segment, Icon, Button, Table, Modal } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { modelResults } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import CurrentModelName from "./CurrentModelName";

class ModelResults extends Component {
    componentDidMount() {
        const { name, modelResults } = this.props
        console.log("name", name)
        if (name) modelResults()
    }

    render() {
        const { t, results } = this.props;

        console.log("results", results)
        const resultsEl = results ? (
            <Segment>

                <Table celled>
                    <Table.Body>
                        <Table.Row>
                            <Table.Cell>WER {results.wer}</Table.Cell>
                            <Table.Cell>{results.count_val}</Table.Cell>
                            <Table.Cell>DEL {results.del_val}</Table.Cell>
                            <Table.Cell>INS {results.ins_val}</Table.Cell>
                            <Table.Cell>SUB {results.sub_val}</Table.Cell>
                        </Table.Row>
                    </Table.Body>
                </Table>
                <p className="bug">
                    This is showing the most recently trained results, not necessarily for the selected model.
                </p>

            </Segment>
        ) : null

        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 4 }>
                            <Informer />
                        </Grid.Column>

                        <Grid.Column width={ 12 }>
                            <Header as='h1' text='true'>
                                { t('model.results.title') }
                            </Header>

                            <CurrentModelName />

                            { resultsEl }

                            <Divider />

                            <Button as={ Link } to="/transcription/new">
                                { t('model.results.newTranscribeButton') }
                            </Button>

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
        results: state.model.results
    }
}

const mapDispatchToProps = dispatch => ({
    modelResults: () => {
        dispatch(modelResults());
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(ModelResults));
