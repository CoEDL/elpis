import React, { Component } from 'react';
import { useTranslation } from 'react-i18next';
import { withRouter, Link } from "react-router-dom";
import { connect } from 'react-redux';
import { Grid, Segment, Header, Button, Dropdown, Divider } from 'semantic-ui-react';
import Branding from '../Shared/Branding';
import SideNav from '../Shared/SideNav';
import ChooseEngine from './ChooseEngine';

import urls from 'urls';

const EngineDashboard = props => {
    let { currentEngine } = props;
    const { t, i18n } = useTranslation("common");
    return (
        <div>
            <Branding />
            <Segment>
            <Grid centered>
                <Grid.Row>
                    <Grid.Column>
                        <Header as='h1'>
                            { t('engine.select.title') }
                        </Header>
                    </Grid.Column>
                </Grid.Row>
            </Grid>

            <ChooseEngine />

            </Segment>
        </div>
    );
};

const mapStateToProps = state => {
    return {
        list: state.engine.engine_list,
        currentEngine: state.engine.engine
    };
};


export default withRouter(
    connect(mapStateToProps)(
        EngineDashboard
    )
);
