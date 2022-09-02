import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import { useLocation } from "react-router-dom";
import ScaleLoader from "react-spinners/ScaleLoader";

const getDescription = (num) => {
  if (num === 1) {
    return "Set up 1";
  }
  if (num === 2) {
    return "Set up 2";
  }
  if (num === 3) {
    return "Set up 3";
  }
  if (num === 4) {
    return "Set up 4";
  }
  return "Error";
};

function Loading() {
  const [taskNum, setTaskNum] = useState(1);

  const location = useLocation();

  const client = axios.create({
    baseURL: "http://localhost:8000",
  });

  // const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  const predictImage = useCallback(async () => {
    try {
      const res1 = await client.post(`/predict/${location.state.id}`);
      console.log(res1);
      if (res1) {
        setTaskNum(2);
        const res2 = await client.get();
        if (res2) {
          setTaskNum(3);
          const res3 = await client.get();
          if (res3) setTaskNum(4);
        }
      }
    } catch (error) {
      console.log(error);
      setTaskNum(0);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    predictImage();
  }, [predictImage]);

  return (
    <div className='container mx-auto mt-16 mb-24'>
      <div className='flex flex-col items-center mt-16'>
        <ScaleLoader
          color='#3F83F8'
          height={30}
          speedMultiplier={0.8}
          width={8}
        />
        <div className='mt-6 text-xl font-medium'>Doing Some Magic!</div>
        <span className='mt-1 font-medium text-gray-500'>
          {taskNum}/4 Task, {getDescription(taskNum)}.
        </span>
      </div>
    </div>
  );
}

export default Loading;
