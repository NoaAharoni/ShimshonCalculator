import React, { useState } from 'react';
import './Results.css';

const Results = (props) => {
    return (
        <div className='results-container'>

            {
                Object.keys(props.results).length > 0 && (
                    <ul>
                        <li>Time: {props.results?.time} seconds</li>
                        <li>Distance: {props.results?.distance} meters</li>
                        {props.results['excess weight'] && <li>Excess Weight that should be destroyed : {props.results['excess weight']} kg</li>}
                        {props.results['weather_message'] && <li>{props.results['weather_message']}</li>}
                    </ul>
                )
            }
        </div>
    )
}


export default Results;