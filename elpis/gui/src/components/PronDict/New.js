import React, {Component} from "react";
import {withRouter} from "react-router-dom";
import {Grid, Header, Segment} from "semantic-ui-react";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import Branding from "../Shared/Branding";
import SideNav from "../Shared/SideNav";
import NewForm from "../PronDict/NewForm";


class PronDictNew extends Component {

    componentDidMount() {}

    render() {
        const {t} = this.props;
        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={4}>
                            <SideNav />
                        </Grid.Column>
                        <Grid.Column width={12}>
                            <Header as="h1" text="true">
                                {t("pronDict.new.title")}
                            </Header>
                            <NewForm />
                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        name: state.pronDict.name,
    };
};

export default withRouter(connect(mapStateToProps)(
    withTranslation("common")(PronDictNew)
));
