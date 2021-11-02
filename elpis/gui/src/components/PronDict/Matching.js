import React, {Component} from "react";
import {Link} from "react-router-dom";
import {connect} from "react-redux";
import {FieldArray, Formik, Field} from "formik";
import {withTranslation} from "react-i18next";
import {Form, Table, Button, Icon, Input} from "semantic-ui-react";
import {pronDictMatching, pronDictLoad} from "redux/actions/pronDictActions";
import urls from "urls";

class MatchingL2S extends Component {  
    saveMatches = (values) => {
        console.log(`Values: ${JSON.stringify(values)}`);
        this.props.pronDictMatching(values)
    }
    
    render() {
        const {t, disabled} = this.props;

        return (
            <Formik
                initialValues={{
                    pairs: [{
                        letter: "",
                        sound: "",
                    }],
                }}
            >
                {({
                    values,
                }) => (
                    <Form> 
                        <FieldArray name="pairs">
                            {({remove, push}) => (
                                <Table striped>
                                    <Table.Header>
                                        <Table.Row>
                                            <Table.HeaderCell>
                                                {t("pronDict.matching.lettersHeader")}
                                            </Table.HeaderCell>
                                            <Table.HeaderCell>
                                                {t("pronDict.matching.soundsHeader")}
                                            </Table.HeaderCell>
                                            <Table.HeaderCell />
                                        </Table.Row>
                                    </Table.Header>
                                    <Table.Body>
                                        {values.pairs.length > 0 &&
                                            values.pairs.map((letter, index) => (
                                                <Table.Row key={index}>
                                                    <Table.Cell>
                                                        <Field name={`pairs.${index}.letter`}/>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Field name={`pairs.${index}.sound`}/>
                                                    </Table.Cell>
                                                    <Table.Cell textAlign="center">
                                                        <Button icon type="button" disabled={values.pairs.length <= 1} onClick={() => remove(index)}>
                                                            <Icon name="trash" />
                                                        </Button>
                                                    </Table.Cell>
                                                </Table.Row>
                                            ))
                                        }
                                    </Table.Body>
                                    <Table.Footer>
                                        <Table.Row>
                                            <Table.HeaderCell />
                                            <Table.HeaderCell />
                                            <Table.HeaderCell textAlign="center">
                                                <Button icon type="button" color="olive" onClick={() => push({letter: "", sound: ""})}>
                                                    <Icon name="add" />
                                                </Button>
                                            </Table.HeaderCell>
                                        </Table.Row>
                                    </Table.Footer>
                                </Table>
                            )}
                        </FieldArray>
                        <Button
                            color="olive"
                            onClick={() => {
                                this.saveMatches(values)
                            }}
                            disabled={disabled}
                        >
                            {t("pronDict.matching.save")}
                        </Button>
                        <Button as={Link} to={urls.gui.pronDict.lexicon} disabled={disabled}>
                            {t("common.nextButton")}
                        </Button>
                    </Form>
                )}
            </Formik>
        )
    }
}

const mapStateToProps = state => {
    return {
    };
};

const mapDispatchToProps = dispatch => ({
    pronDictMatching: postData => {
        dispatch(pronDictMatching(postData))
    }
});

export default connect(mapStateToProps, mapDispatchToProps)(
    withTranslation("common")(MatchingL2S)
);