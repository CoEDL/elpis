import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Button, Divider, Grid, Header, Message, Segment } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { pronDictLexicon } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import CurrentPronDictName from "./CurrentPronDictName";
import urls from 'urls'

class PronDictLexicon extends Component {
    componentDidMount() {
        const { l2s, pronDictLexicon } = this.props
        console.log("PronDictLexicon has l2s?", l2s)

        // TODO get this from a status code instead of some string
        if ((l2s === '') || (l2s === 'No l2s yet')) {
            console.log("No l2s yet")
        } else {
            // only do this if we have real l2s data
            pronDictLexicon()
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
                                { t('pronDict.lexicon.title') }
                            </Header>

                            <CurrentPronDictName />

                            <Message content={ t('pronDict.lexicon.description') } />

                            <Button as={Link} to={urls.gui.model.index } >
                                { t('pronDict.lexicon.nextButton') }
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
        lexicon: state.pronDict.lexicon,
        name: state.pronDict.name,
        l2s: state.pronDict.l2s,
    }
}

const mapDispatchToProps = dispatch => ({
    pronDictLexicon: () => {
        dispatch(pronDictLexicon());
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(PronDictLexicon));
