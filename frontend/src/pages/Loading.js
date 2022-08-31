import React, { useState, useEffect } from "react";
import axios from "axios";
import { useLocation } from "react-router-dom";
import ScaleLoader from "react-spinners/ScaleLoader";

function Loading() {
  const [taskNum, setTaskNum] = useState(1);
  const [taskMessage, setTaskMessage] = useState();

  const location = useLocation();

  const client = axios.create({
    baseURL: "http://localhost:8000",
  });

  const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  useEffect(() => {
    delay(2000);
    const msg = "Starting YOLOv4 Localization";
    console.log(msg);
    setTaskMessage(msg);
  }, []);

  useEffect(() => {
    client.post(`/predict/${location.state.id}`).then((response) => {
      setTaskNum(taskNum + 1);
    });
  }, [client, location.state.id, taskNum]);

  useEffect(() => {
    delay(2000);
    const msg = "Done with YOLOv4 Localization";
    console.log(msg);
    setTaskMessage(msg);
  }, []);

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
          {taskNum}/4 Task, {taskMessage}.
        </span>
      </div>
    </div>
  );
}

export default Loading;
