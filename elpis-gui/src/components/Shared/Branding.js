import React, { Component } from 'react';
import { Button, Image, Segment } from 'semantic-ui-react';
import { Link } from "react-router-dom";
import elpisLogo from './elpis.png'
import { connect } from 'react-redux';
import { configReset } from 'redux/actions/appActions';

class StepBranding extends Component {

    reset = () => {
        this.props.configReset()
        window.location.href = "/dataset/new"
    }

    render() {
        return (
            <Segment clearing as='h1'>
                <Link to="/">
                    <Image floated="left" src={elpisLogo} className="logo" alt="logo" />
                </Link>
                <Button floated="right" basic onClick={this.reset}>reset</Button>
            </Segment>
        )
    }
}

const mapDispatchToProps = dispatch => ({
    configReset: postData => {
        dispatch(configReset(postData))
            .then(response => console.log(response))
    }
})

export default connect(null, mapDispatchToProps)(StepBranding)
