import { Button, TextField, Typography } from '@mui/material';
import { DesktopDatePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterMoment } from '@mui/x-date-pickers/AdapterMoment';
import axios from 'axios';
import moment from 'moment';
import 'moment-timezone';
import React, { useEffect, useState } from 'react'
import "./MainForm.css"

const NOW = new Date();
const START_DATE = new Date(NOW.getFullYear(), NOW.getMonth() - 8, NOW.getDate());
const END_DATE = new Date(NOW.getFullYear(), NOW.getMonth(), NOW.getDate() + 15);

const MainForm = (props) => {
    // State variables to store user inputs
    const [cargoMass, setCargoMass] = useState('');
    const [startDate, setStartDate] = useState(moment().tz('GMT'));


    // Function to handle form submission
    const handleSubmit = async (event) => {
        event.preventDefault();
        props.onSubmit(cargoMass, startDate);
    };

    return (

        <div className='form__main-container'>
            <Typography sx={{ marginBottom: "10px" }} variant='h3'>Shimshon Calculator</Typography>
            <form className='form__content' onSubmit={handleSubmit}>
                <TextField
                    sx={{ margin: "10px 0" }}
                    name="cargo_mass"
                    id="cargo_mass"
                    label="Cargo Mass"
                    required
                    value={cargoMass}
                    onChange={(event) => setCargoMass(event.target.value)}
                />
                <LocalizationProvider dateAdapter={AdapterMoment} adapterLocale="he-il">
                    <DesktopDatePicker
                        label="Date"
                        inputFormat="DD/MM/YYYY"
                        value={moment(startDate).tz('GMT')}
                        onChange={(newValue) => setStartDate(moment(newValue).tz('GMT'))}
                        maxDate={END_DATE}
                        minDate={START_DATE}
                        renderInput={(params) => <TextField required {...params} sx={{ margin: "10px 0" }} error={false} />}
                    />
                </LocalizationProvider>
                <Button sx={{ marginTop: "50px", backgroundColor: "#87e4e0", "&:hover": { backgroundColor: "#87e4e0", filter: "brightness(0.9)" } }} type="submit" variant="contained">Submit</Button>

            </form>

        </div>
    );
}

export default MainForm;
