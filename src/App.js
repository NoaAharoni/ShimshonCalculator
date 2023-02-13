import React, { useState } from 'react';
import axios from 'axios';
import MainForm from './MainForm';
import Results from './Results';

const Form = () => {
  // State variables to store results from the server
  const [results, setResults] = useState({});
  const [error, setError] = useState('');

  // Function to handle form submission
  const getResults = async (cargoMass, startDate) => {
    // Clear previous results and error messages
    setResults({});
    setError('');
    try {
      // Send a post request to the server with user inputs
      const response = await axios.post('/', { cargo_mass: cargoMass, start_date: startDate });
      // If the server returns an error, set the error message
      if (response.data.error) {
        setError(response.data.error);
        // If the server returns results, set the results
      } else {
        setResults(response.data);
      }
    } catch (err) {
      // If there is a network error, set the error message
      setError(err.message);
    }
  };

  // // Variables to set the date limits for the start date input
  // const currentDate = new Date();
  // const startLimit = new Date();
  // startLimit.setMonth(currentDate.getMonth() - 8); // Set month to be from now until 8 month ago
  // const endLimit = new Date(currentDate.getTime() + 15 * 24 * 60 * 60 * 1000); // Set the day to be from now to 15 days forward

  // Render the form and the results
  return (
    <div>
      <MainForm onSubmit={getResults} />
      {error && <div>Error: {error}</div>}
      <Results results={results} />
    </div>
  );
};

export default Form;
