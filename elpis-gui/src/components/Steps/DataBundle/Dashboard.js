import React, { Component } from 'react';
import { Grid, Header, Segment, Icon, Button } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { dataBundleList } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';

class DataBundleDashboard extends Component {
    componentDidMount() {
        const { dataBundleList } = this.props
        dataBundleList()
    }

    render() {
        const { t, list } = this.props;
        console.log('dataBundleList', list)
        const listEl = list.length > 0 ? (
            <ul>
                {list.map( name => <li key={name}>{name}</li>)}
            </ul>
        ) : <p>{ t('dataBundle.list.noneMessage') }</p>

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

                            { listEl }

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        list: state.dataBundle.dataBundleList
    }
}

const mapDispatchToProps = dispatch => ({
    dataBundleList: () => {
        dispatch(dataBundleList())
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(DataBundleDashboard))
