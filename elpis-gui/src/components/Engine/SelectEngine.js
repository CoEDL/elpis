import React, { useEffect } from 'react';
import { Grid, Segment, Header, Button, Dropdown, Divider } from 'semantic-ui-react';
import { withRouter, Link } from "react-router-dom";
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { engineList, engineLoad } from 'redux/actions/appActions';
import Branding from 'components/Shared/Branding';
import SideNav from 'components/Shared/SideNav';
import urls from 'urls';
import CurrentEngineName from './CurrentEngineName'

const SelectEngine = props => {
    let { t, currentEngine, list, engineList, engineLoad } = props;

    let handleChange = (_event, data) => {
        let engine_name = data.value;
        let postData = { engine_name };
        engineLoad(postData);
    };

    let options = list.map((name, i) => ({key: name, text: name, value: name}));
    
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
                            { t('engine.select.title') }
                        </Header>

                        <CurrentEngineName />

                        {(()=>{
                            // If the engines list has not been populated, fetch the list and display a wait message.
                            if (list.length === 0) {
                                useEffect(engineList); // Alternative to componentDidMount
                                return (
                                    <div>Updating engine list...</div>
                                )
                            } else {
                                // Otherwise if list is populated, allow engine selections.
                                return (
                                <div>
                                    <Dropdown
                                        placeholder={currentEngine?currentEngine:"select engine"}
                                        selection
                                        options={options}
                                        onChange={handleChange}/>

                                    <Divider />

                                    <Button
                                        as={Link}
                                        to={(currentEngine==="kaldi") ? urls.gui.pronDict.index : urls.gui.model.index}
                                        disabled={!currentEngine}>
                                            {t('common.nextButton')}
                                    </Button>
                                </div>)
                            }
                        })()}
                        
                    </Grid.Column>
                </Grid>
            </Segment>
        </div>
    );
};

const mapStateToProps = state => {
    return {
        list: state.sideNav.engine_list,
        currentEngine: state.sideNav.engine
    }
}

const mapDispatchToProps = dispatch => ({
    engineList: () => {
        dispatch(engineList())
    },
    engineLoad: postData => {
        dispatch(engineLoad(postData))
            .then(response => {
                console.log("engineLoad", response)
            })
            .catch(error => console.log("error", error))
    }
})

export default withRouter(
    connect(
        mapStateToProps,
        mapDispatchToProps
    )(
        translate('common')(SelectEngine)
    )
);