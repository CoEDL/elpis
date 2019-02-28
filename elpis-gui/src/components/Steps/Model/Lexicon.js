import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Button, Divider, Grid, Header, Message, Segment } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { modelLexicon } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import CurrentModelName from "./CurrentModelName";
import urls from 'urls'

class ModelLexicon extends Component {
    componentDidMount() {
        const { l2s, modelLexicon } = this.props
        console.log("ModelLexicon has l2s?", l2s)

        // TODO get this from a status code instead of some string
        if ((l2s === '') || (l2s === 'No l2s yet')) {
            console.log("No l2s yet")
        } else {
            // only do this if we have real l2s data
            modelLexicon()
        }
    }

    render() {
        const { t, lexicon } = this.props;
        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 4 }>
                            <Informer />
                        </Grid.Column>

                        <Grid.Column width={ 12 }>

                            <Header as='h1'>
                                { t('model.lexicon.title') }
                            </Header>

                            <CurrentModelName />

                            <Message content={ t('model.lexicon.description') } />

                            <Button as={ Link } to={ urls.gui.model.settings } >
                                { t('model.lexicon.nextButton') }
                            </Button>

                            <Divider />

                            <Segment>
                                <pre>
                                    { lexicon }
                                </pre>
                            </Segment>

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        lexicon: state.model.lexicon,
        name: state.model.name,
        l2s: state.model.l2s,
    }
}

const mapDispatchToProps = dispatch => ({
    modelLexicon: () => {
        dispatch(modelLexicon());
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(ModelLexicon));
