import React, { Component } from 'react';
import { translate } from 'react-i18next';
import { withRouter, Link } from "react-router-dom";
import { connect } from 'react-redux';
import { Grid, Segment, Header, Button, Dropdown, Divider } from 'semantic-ui-react';
import Branding from 'components/Shared/Branding';
import SideNav from 'components/Shared/SideNav';
import SelectEngineDropdown from './SelectEngineDropdown'

import urls from 'urls';

const EngineDashboard = props => {
    let { t, currentEngine } = props;
    return (
    <div>
        <Branding />
        <Segment>
            <Grid centered>
                <Grid.Column width={ 8 }>
                    <Header as='h1'>
                        { t('engine.select.title') }
                    </Header>

                    <SelectEngineDropdown />

                    <br />
                    <br />

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
