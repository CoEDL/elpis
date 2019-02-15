import React from 'react';
import styles from './Indicator.module.css';

const Indicator = props => {

    let width;
    if (props.width === undefined) {
        width = 1;
    } else {
        width = props.width;
    }

    //
    let cap;
    if (props.cap === undefined || props.cap === false) {
        cap = <div></div>;
    } else {
        cap = (
            <div
                className={ styles.cap }
                style={ {
                    width: width + "em",
                    height: width + "em",
                    backgroundColor: props.color,
                    borderRadius: 0.5 * width + "em",
                } }
            >
                <div
                    className={ styles.cap_whiteout }
                    style={ {
                        width: width + "em",
                        backgroundColor: props.color,
                    } }
                ></div>

            </div>
        );
    }

    let cup;
    let next;
    if (props.cup === undefined || props.cup === false) {
        cup = <div></div>;
        next = <div className={ styles.next } style={ {
            backgroundColor: props.color,
            width: (Math.sqrt(0.5 * width * width)) + "em",
            height: (Math.sqrt(0.5 * width * width)) + "em",
        } }></div>;
    } else {
        cup = (
            <div
                className={ styles.cup }
                style={ {
                    width: width + "em",
                    height: width + "em",
                    backgroundColor: props.color,
                    borderRadius: 0.5 * width + "em",
                } }
            >
                <div
                    className={ styles.cup_whiteout }
                    style={ {
                        width: width + "em",
                        backgroundColor: props.color,
                    } }
                ></div>

            </div>
        );
    }

    return (
        <div className={ styles.body } style={ { width: width + "em", backgroundColor: props.color, } }>
            { cap }
            { next }
            { cup }
        </div>);
}

export default Indicator;
