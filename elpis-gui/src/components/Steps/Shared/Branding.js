import React, { Component } from 'react';
import { Header } from 'semantic-ui-react';
import { Link } from "react-router-dom";


export default class StepBranding extends Component {

    render() {
        return (
            <Header as='h1'>
                <Link to="/">
                    <img src="https://github.com/CoEDL/elpis/raw/master/docs/img/elpis.png" className="logo" alt="logo" />
                </Link>
            </Header>
        )
    }
}
