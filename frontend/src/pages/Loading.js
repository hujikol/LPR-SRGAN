import React from "react";
import axios from "axios";
import { useLocation } from "react-router-dom";

function Loading() {
  const location = useLocation();

  axios
    .post(`http://localhost:8000/predict/${location.state.id}`)
    .then((response) => {
      console.log(response);
    })
    .catch((error) => {
      console.log(error);
    });

  return (
    <div className='container mx-auto mt-16 mb-24'>
      {/* tittle div */}
      <div className='flex justify-center mt-16'>
        <h1 className='text-2xl font-bold text-center'>Loading...</h1>
      </div>
      {/* end of tittle div */}
    </div>
  );
}

export default Loading;
