import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Button, Divider, Form, Grid, Header, Message, Segment, TextArea } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { pronDictGenerateLexicon, pronDictSaveLexicon, pronDictUpdateLexicon } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import CurrentPronDictName from "./CurrentPronDictName";
import urls from 'urls'

class PronDictLexicon extends Component {


    componentDidMount = () => {
    }

    generateLexicon = () => {
        this.props.pronDictGenerateLexicon()
    }

    saveLexicon = () => {
        const data = { "lexicon": this.props.lexicon }
        this.props.pronDictSaveLexicon(data)
    }

    handleChange = (event) => {
        this.props.pronDictUpdateLexicon( { "lexicon": event.target.value } )
    }


    render() {

        const { t, lexicon } = this.props

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

                            <Segment>
                                <Form>
                                    <TextArea
                                        className="lexicon"
                                        onChange={this.handleChange}
                                        value={lexicon} >
                                    </TextArea>
                                </Form>
                                <Button.Group attached='bottom'>
                                    <Button onClick={this.generateLexicon}>reset</Button>
                                    <Button onClick={this.saveLexicon} positive>save</Button>
                                </Button.Group>
                            </Segment>

                            <Button as={Link} to={urls.gui.model.index}>
                                {t('common.nextButton')}
                            </Button>

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        )
    }
}

const mapStateToProps = (state) => {
    return {
        name: state.pronDict.name,
        l2s: state.pronDict.l2s,
        lexicon: state.pronDict.lexicon
    }
}

const mapDispatchToProps = dispatch => ({
    pronDictGenerateLexicon: () => {
        dispatch(pronDictGenerateLexicon())
    },
    pronDictSaveLexicon: data => {
        dispatch(pronDictSaveLexicon(data))
    },
    pronDictUpdateLexicon: data => {
        dispatch(pronDictUpdateLexicon(data))
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(PronDictLexicon))
