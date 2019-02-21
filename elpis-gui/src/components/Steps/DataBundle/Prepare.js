import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Divider, Grid, Header, Segment, List, Button } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';

class DataBundlePrepare extends Component {
    componentDidMount() {
    }
    render() {
        const { t, preparedData } = this.props;
        const wordlistTable = preparedData.wordlist ? (
            <Segment>
                <Header as='h1'>{ t('dataBundle.prepare.wordlistHeader') }</Header>
                <ul>
                    {preparedData.wordlist.map( word =><li key={word}>{word}</li>)}
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

                            <Button type='submit' as={ Link } to="/model/pronunciation-dictionary">{ t('dataBundle.prepare.nextButton') }</Button>
                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        preparedData: state.dataBundle.preparedData
    }
}
export default connect(mapStateToProps)(translate('common')(DataBundlePrepare))

