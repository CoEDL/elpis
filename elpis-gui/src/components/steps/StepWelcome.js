import React, { Component } from 'react';
import { Button } from 'semantic-ui-react';

export default class StepWelcome extends Component {
    // constructor(props) {
    //     super(props);
    // }
    render() {
        return <div>
            <Button onClick={() => this.props.toStepNaming()}>Build Model</Button>
        </div>;
    }
}