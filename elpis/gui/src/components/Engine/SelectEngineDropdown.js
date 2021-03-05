import React, { Component } from 'react';
import { Grid, Segment, Header, Button, Dropdown, Divider } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { engineLoad } from 'redux/actions/engineActions';
import { setCurrentStep } from 'redux/actions/sideNavActions'

class SelectEngineDropdown extends Component {

    render() {

        let { t, currentEngine, engineHumanNames, list, _engineLoad } = this.props;

        let handleChange = (_event, data) => {
            let engine_name = data.value;
            let postData = { engine_name };
            _engineLoad(postData);
        };

        let options = list.map((name, i) => ({key: name, text: engineHumanNames[name], value: name}));

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
        engineHumanNames: state.engine.engine_human_names
    }
}

const mapDispatchToProps = dispatch => ({
    _engineLoad: postData => {
        dispatch(engineLoad(postData))
    }
})

export default
    connect(
        mapStateToProps,
        mapDispatchToProps
    )(
        translate('common')(SelectEngineDropdown)
    )
