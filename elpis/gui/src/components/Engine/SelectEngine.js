import React, { Component } from 'react';
import { Grid, Segment, Header, Button, Dropdown, Divider } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { engineList, engineLoad } from 'redux/actions/engineActions';
import { setCurrentStep } from 'redux/actions/sideNavActions'

class SelectEngine extends Component {

    render() {

        let { t, currentEngine, list, doEngineList, doEngineLoad } = this.props;

        let handleChange = (_event, data) => {
            let engine_name = data.value;
            let postData = { engine_name };
            doEngineLoad(postData);
        };

        let options = list.map((name, i) => ({key: name, text: name, value: name}));

        return (
            <>
                {list.length === 0 &&
                    <p>{t('engine.select.waitingForEngineList')}</p>
                }
                {list.length > 0 &&
                    <Dropdown
                        placeholder={currentEngine?currentEngine: t('engine.select.shortcutPlaceholder')}
                        selection
                        options={options}
                        value={currentEngine}
                        onChange={handleChange} />
                }
            </>
        )
    }
}

const mapStateToProps = state => {
    return {
        list: state.engine.engine_list,
        currentEngine: state.engine.engine,
    }
}

const mapDispatchToProps = dispatch => ({
    doEngineList: () => {
        dispatch(engineList())
    },
    doEngineLoad: postData => {
        dispatch(engineLoad(postData))
            .then(response => {
                // Rebuild the sidenav via set current step
                dispatch(setCurrentStep(null))
            })
            .catch(error => console.log("error", error))
    }
})

export default
    connect(
        mapStateToProps,
        mapDispatchToProps
    )(
        translate('common')(SelectEngine)
    )
