import React from "react";
import {FieldArray, Formik, Field, ErrorMessage} from "formik";
import {Form, Table, Button, Icon, Label, Card} from "semantic-ui-react";

const MatchingError = (message) => {
    return (
        <Label basic pointing color='red'>
            {message}
        </Label>
    )
}

const MatchingL2S = ({props, changeMatchesCallback, interactionDisabled}) => {  
    const {t, l2sPairs} = props;

    const validate = (value) => {
        let errorMessage;
        if (/[^\s]+\s+[^\s]+/.test(value)) {
            errorMessage = t("pronDict.matching.whitespaceErrorMessage");
            errorMessage = t("pronDict.matching.whitespaceErrorMessage");
        }
        return errorMessage;
    };

    return (
        <Formik
            enableReinitialize={true}
            initialValues={{
                pairs: l2sPairs
            }}
            onSubmit={(values) => {
                console.log(`Submitting l2s pairs (${JSON.stringify(values.pairs[0])}...)`);
                changeMatchesCallback(values);
            }}
        >
            {({
                values,
                handleSubmit,
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
                                                <Table.Cell className='matching-table-data'>
                                                    <Field name={`pairs.${index}.letter`} validate={validate}/>
                                                    <ErrorMessage
                                                        name={`pairs.${index}.letter`}
                                                        render={(msg) => <MatchingError message={msg}/>}
                                                    />
                                                </Table.Cell>
                                                <Table.Cell className='matching-table-data'>
                                                    <Field name={`pairs.${index}.sound`} validate={validate}/>
                                                    <ErrorMessage
                                                        name={`pairs.${index}.sound`}
                                                        render={(msg) => <MatchingError message={msg}/>}
                                                    />
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
                                                type="button"
                                                onClick={handleSubmit}
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