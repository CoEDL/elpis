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
                (known bug: this is only showing the last trained results, not necessarily for the selected model)
                <Grid.Row columns={5}>
                    <Grid.Column>wer {results.wer_val}</Grid.Column>
                    <Grid.Column>{results.count_val}</Grid.Column>
                    <Grid.Column>del {results.del_val}</Grid.Column>
                    <Grid.Column>ins {results.ins_val}</Grid.Column>
                    <Grid.Column>sub {results.sub_val}</Grid.Column>
                </Grid.Row>
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
