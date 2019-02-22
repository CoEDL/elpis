import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Divider, Grid, Header, Segment, List, Button } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import _ from 'lodash'
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import urls from 'urls'

class DataBundlePrepare extends Component {
    componentDidMount() {
    }
    render() {
        const { t, wordlist } = this.props;
        console.log("wordlist", wordlist)
        const wordlistTable = wordlist ? (
            <Segment>
                <Header as='h1'>{ t('dataBundle.prepare.wordlistHeader') }</Header>
                <ul>
                    {
                        Object.keys(wordlist).map(function (key) {
                            return (<li>{key} {wordlist[key]}</li>)
                        })
                    }
                </ul>
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
                            <Header as='h1'>{ t('dataBundle.prepare.title') }</Header>

                            <h2>{ t('dataBundle.prepare.header') }</h2>
                            <p>{ t('dataBundle.prepare.bannerMessage') }</p>
                            <p>{ t('dataBundle.prepare.bannerMessageDetailed') }</p>

                            { wordlistTable }

                            <Button as={ Link } to={urls.gui.model.new}>
                                { t('dataBundle.prepare.nextButton') }
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
        wordlist: state.dataBundle.wordlist
    }
}
export default connect(mapStateToProps)(translate('common')(DataBundlePrepare))

