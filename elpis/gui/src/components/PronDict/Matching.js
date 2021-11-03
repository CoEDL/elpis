import React, {useEffect} from "react";
import {FieldArray, Formik, Field} from "formik";
import {Form, Table, Button, Icon, Input} from "semantic-ui-react";

const MatchingL2S = ({props, changeMatchesCallback, interactionDisabled}) => {  
    // TODO Implement error checking (e.g. spaces in fields)

    const {t, l2sPairs} = props;

    const saveMatches = (values) => {
        console.log(`Values: ${JSON.stringify(values)}`);
        changeMatchesCallback(values);
    }

    return (
        <Formik
            enableReinitialize={true}
            initialValues={{
                pairs: l2sPairs
            }}
        >
            {({
                values,
            }) => (
                <Form> 
                    <FieldArray name="pairs">
                        {({remove, push}) => (
                            <Table striped className="matching-table">
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
                                        <Table.HeaderCell>
                                            <Button
                                                color="olive"
                                                onClick={() => {
                                                    saveMatches(values)
                                                }}
                                                disabled={interactionDisabled}
                                            >
                                                {t("pronDict.matching.save")}
                                            </Button>
                                        </Table.HeaderCell>
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
                </Form>
            )}
        </Formik>
    )
}

export default MatchingL2S;