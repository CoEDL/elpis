import React, { Component } from 'react';
import { Grid, Header, Segment, Icon, Button } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { dataBundleList } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';

class DataBundleList extends Component {
    componentDidMount() {
        const { dataBundleList } = this.props
        dataBundleList()
    }

    render() {
        const { t, dbNames } = this.props;

        const list = dbNames ? (
            <ul>
                {dbNames.map( name => <li key={name}>{name}</li>)}
            </ul>
        ) : <li>no bundles yet</li>

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
                            { t('dataBundle.list.title') }
                            </Header>

                            { list }

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        dbNames: state.dataBundle.dbNames
    }
}
const mapDispatchToProps = dispatch => ({
    dataBundleList: () => {
        dispatch(dataBundleList())
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(DataBundleList))
