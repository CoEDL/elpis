import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Button, Divider, Form, Grid, Header, Message, Segment, TextArea } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { withTranslation } from 'react-i18next';
import { pronDictBuildLexicon, pronDictSaveLexicon, pronDictUpdateLexicon } from 'redux/actions/pronDictActions';
import Branding from '../Shared/Branding';
import SideNav from '../Shared/SideNav';
import CurrentPronDictName from "./CurrentPronDictName";
import urls from 'urls'

class PronDictLexicon extends Component {


    componentDidMount = () => {
        const { lexicon } = this.props
        if (!lexicon) this.generateLexicon()

    }

    generateLexicon = () => {
        this.props.pronDictBuildLexicon()
    }

    saveLexicon = () => {
        const data = { "lexicon": this.props.lexicon }
        this.props.pronDictSaveLexicon(data)
    }

    handleChange = (event) => {
        this.props.pronDictUpdateLexicon( { "lexicon": event.target.value } )
    }


    render() {

        const { t, currentEngine, lexicon, name } = this.props

        const interactionDisabled = name ? false : true

        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 4 }>
                            <SideNav />
                        </Grid.Column>

                        <Grid.Column width={ 12 }>

                            <Header as='h1'>
                                { t('pronDict.lexicon.title') }
                            </Header>

                            <CurrentPronDictName />

                            {!currentEngine &&
                              <p>{ t('engine.common.noCurrentEngineLabel') }</p>
                            }

                            {currentEngine && !name &&
                              <p>{ t('pronDict.common.noCurrentPronDictLabel') }</p>
                            }

                            {currentEngine && name &&
                            <>
                                <Message content={ t('pronDict.lexicon.description') } />

                                <Button as={Link} to={urls.gui.model.index} disabled={interactionDisabled}>
                                    {t('common.nextButton')}
                                </Button>

                                <div className="form-wrapper">
                                    <Form>
                                        <TextArea
                                            className="lexicon"
                                            onChange={this.handleChange}
                                            value={lexicon} >
                                        </TextArea>
                                    </Form>

                                    <Button size="tiny" basic onClick={this.generateLexicon} disabled={interactionDisabled}>{ t('pronDict.lexicon.reset') }</Button>
                                    <Button size="tiny" onClick={this.saveLexicon} disabled={interactionDisabled}>{ t('pronDict.lexicon.save') }</Button>

                                </div>

                            </>
                            }

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
        lexicon: state.pronDict.lexicon,
        currentEngine: state.engine.engine
    }
}

const mapDispatchToProps = dispatch => ({
    pronDictBuildLexicon: () => {
        dispatch(pronDictBuildLexicon())
            .then(response => console.log(response))
    },
    pronDictSaveLexicon: data => {
        dispatch(pronDictSaveLexicon(data))
            .then(response => console.log(response))
    },
    pronDictUpdateLexicon: data => {
        dispatch(pronDictUpdateLexicon(data))
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(
    withTranslation("common")(PronDictLexicon)
)
