import React, {useCallback} from "react";
import {withTranslation} from "react-i18next";
// import {useOrdinalColorScale} from "@nivo/colors";
import {usePie} from "@nivo/pie";

function computeAnnotatedArcs(data) {
    return [
            (1 - data) * 100,
            data * 100,
    ];
}

const CustomNode = ({
    node,
    x,
    y,
    size,
    // scale,
    // color,
    // borderWidth,
    // borderColor,
    onMouseEnter,
    onMouseMove,
    onMouseLeave,
    onClick,
}) => {
    const handleMouseEnter = useCallback(event => onMouseEnter && onMouseEnter(node, event), [
        node,
        onMouseEnter,
    ]);
    const handleMouseMove = useCallback(event => onMouseMove && onMouseEnter(node, event), [
        node,
        onMouseMove,
    ]);
    const handleMouseLeave = useCallback(event => onMouseLeave && onMouseLeave(node, event), [
        node,
        onMouseLeave,
    ]);
    const handleClick = useCallback(event => onClick && onClick(node, event), [node, onClick]);
    const {arcs, arcGenerator} = usePie({
        data: computeAnnotatedArcs(node.data.annotated),
        radius: size / 2,
        innerRadius: (size / 2) * 0.7,
        sortByValue: true,
    });

    console.log(arcs);
    console.log(arcGenerator);

    return (
        <g transform={`translate(${x},${y})`}>
            <circle 
                r={size / 2} 
                stroke="rgb(216, 218, 235)" 
                strokeWidth={12} 
            />
            <circle 
                r={size / 2} 
                fill="rgb(45, 0, 75)" 
                stroke="rgb(45, 0, 75)" 
                strokeWidth={6}
            />
            {arcs.map((arc, i) => {
                return <path key={i} d={arcGenerator(arc)} fill={["rgb(45, 0, 75)","rgb(211,160,240)"][i]} />;
            })}
            {node.id.length < 10 && (
                <text
                    fill="white"
                    textAnchor="middle"
                    dominantBaseline="central"
                    style={{
                        fontSize: 14,
                        fontWeight: 800,
                    }}
                >
                    {node.id}
                </text>
            )}
            <circle 
                r={size / 2}
                fillOpacity="0"
                onMouseEnter={handleMouseEnter}
                onMouseMove={handleMouseMove}
                onMouseLeave={handleMouseLeave}
                onClick={handleClick}
            />
        </g>
    );
};

export default (withTranslation("common")(CustomNode));
