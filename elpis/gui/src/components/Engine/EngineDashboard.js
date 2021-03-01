import React, { Component } from 'react';
import { translate } from 'react-i18next';
import { withRouter, Link, useParams } from "react-router-dom";
import { connect } from 'react-redux';
import { Grid, Segment, Header, Button, Dropdown, Divider } from 'semantic-ui-react';
import Branding from 'components/Shared/Branding';
import SideNav from 'components/Shared/SideNav';
import CurrentEngineName from './CurrentEngineName'
import SelectEngineList from './SelectEngineList'

import urls from 'urls';

const EngineDashboard = props => {
    let { t, currentEngine, params } = props;

    console.log(props.match.params)

    return (
    <div>
        <Branding />
        <Segment>
            <Grid centered>
                <Grid.Column width={ 12 }>
                    <Header as='h1'>
                        { t('engine.select.title') }
                    </Header>

                    {/* <CurrentEngineName /> */}

                    <SelectEngineList />

                    <br /><br />

                    <Button
                        as={Link}
                        to={urls.gui.dataset.index}
                        disabled={!currentEngine}>
                    {t('common.nextButton')}
                    </Button>

                </Grid.Column>
            </Grid>
        </Segment>
    </div>
    )
}

const mapStateToProps = state => {
    return {
        list: state.engine.engine_list,
        currentEngine: state.engine.engine
    }
}


export default withRouter(
    connect(
        mapStateToProps
    )(
        translate('common')(EngineDashboard)))
