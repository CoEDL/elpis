import React, { Component } from 'react';
import { Button, Grid, Header, Segment } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { dataBundleList, dataBundleLoad } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import CurrentDataBundleName from "./CurrentDataBundleName";

class DataBundleDashboard extends Component {
    componentDidMount() {
        const { dataBundleList } = this.props
        dataBundleList()
    }

    handleLoad = name => {
        const { dataBundleLoad } = this.props
        const postData = { name: name }
        dataBundleLoad(postData)
    }

    render() {
        const { t, list, currentName } = this.props;
        const listEl = list.length > 0 ? (
            <ul className="data-bundle-list">
                {list.map( name => {
                    const className = (name === currentName) ? 'current-data-bundle' : ''
                    const color = (name === currentName) ? 'purple' : ''
                    return (
                        <li key={name}>
                            <Button className={className} fluid onClick={ () => this.handleLoad(name) }>{ name }</Button>
                        </li>
                    )}
                )}
            </ul>
        ) : <p>{ t('dataBundle.dashboard.noneMessage') }</p>

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
                                { t('dataBundle.dashboard.title') }
                            </Header>

                            <CurrentDataBundleName name={ name } />

                            <Segment>
                                { listEl }
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
        list: state.dataBundle.dataBundleList,
        currentName: state.dataBundle.name
    }
}

const mapDispatchToProps = dispatch => ({
    dataBundleList: () => {
        dispatch(dataBundleList())
    },
    dataBundleLoad: postData => {
        dispatch(dataBundleLoad(postData))
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(DataBundleDashboard))
