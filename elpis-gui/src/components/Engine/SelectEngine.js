import React, { useEffect } from 'react';
import { Grid, Segment, Header, Button, Dropdown, Divider } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { engineList, engineLoad } from 'redux/actions/appActions';

const SelectEngine = props => {
    let { t, currentEngine, list, engineList, engineLoad } = props;

    let handleChange = (_event, data) => {
        let engine_name = data.value;
        let postData = { engine_name };
        engineLoad(postData);
    };

    let options = list.map((name, i) => ({key: name, text: name, value: name}));

    // If the engines list has not been populated, fetch the list and display a wait message.
    if (list.length === 0) {
        useEffect(engineList); // Alternative to componentDidMount
        return (
            <div>Updating engine list...</div>
        )
    } else {
        // Otherwise if list is populated, allow engine selections.
        return (
            <Dropdown
                placeholder={currentEngine?currentEngine:"select engine"}
                selection
                options={options}
                value={currentEngine}
                onChange={handleChange} />
        )
    }
}

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

export default
    connect(
        mapStateToProps,
        mapDispatchToProps
    )(
        translate('common')(SelectEngine)
    )
