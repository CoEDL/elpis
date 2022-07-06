/**
 * Given a range, the calculateTickValues function returns appropriately
 * spaced integer values that can be used for the axes of a graph.
 * 
 * The function automatically applies a 15% margin to the min and max
 * values supplied to appropriately space the grap.
 * 
 * @param {*} min 
 * @param {*} max 
 */
export const calculateTickValues = (min, max, ticks, hardMin = false, hardMax = false) => {
    const range = max - min;
    const tickMin = hardMin ? min : Math.floor(min - (range * 0.15));

    console.log(tickMin);

    const tickMax = hardMax ? max : Math.floor(max + (range * 0.15));

    console.log(tickMax);

    const realRange = tickMax - tickMin;
    const step = Math.ceil(realRange / ticks);
    var result = [];
    var i = tickMin;

    result.push(i);

    do {
        console.log(i);
        i += step;
        result.push(i);
    }
    while (i < tickMax);

    return result;
};
/**
 * Given an object of key value pairs of frequencies, this function
 * converts it into a format suitable for consumption by the Nivo Bar
 * Chart.
 */
export const convertToBarData = (data) => {
    var newData = [];

    Object.keys(data).map(function(key) {
        newData.push({
            id: key,
            frequency: data[key],
        });
    });

    return newData;
};

