import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Divider, Grid, Header, Segment, Icon, Button } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { modelLexicon } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import urls from 'urls'

class ModelLexicon extends Component {
    componentDidMount() {
        const {modelLexicon} = this.props
        modelLexicon()
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
    }
}

const mapDispatchToProps = dispatch => ({
    modelLexicon: () => {
        dispatch(modelLexicon());
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(ModelLexicon));
