import React, {Component} from "react";
import {withRouter} from "react-router-dom";
import {List, Accordion} from "semantic-ui-react";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import classNames from "classnames";
import {setCurrentStep} from "redux/actions/sideNavActions";
import {stepToOrder} from "../../redux/reducers/sideNavReducer";
import "./SideNav.css";


class SideNav extends Component {
    handleStepSelect = (step) => {
        const {history} = this.props;

        history.push(step.path);
    };

    componentDidMount = () => {
        const {match, setCurrentStep} = this.props;

        setCurrentStep(match.url);
    };

    render() {
        const {t, steps} = this.props;

        return (
            <Accordion styled>
                {
                    // for each step (pass down the index too,
                    // we'll use that when we call the action to update redux state)
                    Object.entries(steps)
                        .sort((left, right) => (stepToOrder(left[0]) - stepToOrder(right[0])))
                        // eslint-disable-next-line no-unused-vars
                        .map(([_stepName, step], i) => {
                            return (
                                <div key={i}>
                                    <Accordion styled fluid>
                                        <Accordion.Content active={step.enabled || step.doing}>
                                            <List relaxed className="stepList">
                                                {
                                                    // for each substep (pass in the step index and the substep index)
                                                    // we'll use these to target the selected substep in redux
                                                    step.substeps.map((substep, j) => {
                                                            // substep classes
                                                            const substepClassNames = classNames({
                                                                firstSubstep: j === 0,
                                                                substepDone: substep.done,
                                                                substepDoing: substep.doing,
                                                                disabled: !substep.enabled,
                                                            });

                                                            return (
                                                                <List.Item
                                                                    className={substepClassNames}
                                                                    onClick={() => this.handleStepSelect(substep, i, j)}
                                                                    key={substep.title}
                                                                >
                                                                    <div style={{paddingLeft: "1.4em"}}>
                                                                        {t(substep.title)}
                                                                    </div>
                                                                </List.Item>
                                                            );
                                                        },
                                                    )
                                                }
                                            </List>
                                        </Accordion.Content>
                                    </Accordion>
                                </div>
                            );
                        })
                }
            </Accordion>
        );
    }
}

const mapStateToProps = (state, ownProps) => {
    return {
        steps: state.sideNav.steps,
        ownProps: ownProps,
    };
};

const mapDispatchToProps = dispatch => ({
    setCurrentStep: (urlParams) => {
        dispatch(setCurrentStep(urlParams));
    },
});

export default withRouter(
    connect(mapStateToProps, mapDispatchToProps)(
        withTranslation("common")(SideNav),
    ),
);
