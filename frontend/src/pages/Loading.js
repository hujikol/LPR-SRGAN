import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link, useLocation, useNavigate } from "react-router-dom";
import ScaleLoader from "react-spinners/ScaleLoader";

const getDescription = (num) => {
  if (num === -99)
    return "I'm sorry but no magic for today! I'm feeling something was wrong..";

  if (num === -1) return "Oh no.. I Can't find the plates in your image..";

  if (num === 0) return "Done Uploading.. Searching for License Plates now..";

  if (num === 1) return "Found the plates! Extracting the Plates now..";

  if (num === 2)
    return "Plates extracted.. Generating Super Resolution Image now...";

  if (num === 3) return "Eureka! Analyzing Character in the Image..";

  if (num === 4) return "All Done! Let me wrap up the data to be visualized..";
};

const defaultPredictRes = {
  res1: null,
  res2: null,
  res3: null,
  res4: null,
  res5: null,
  taskNum: null,
};

function Loading() {
  const [predictRes, setPredictRes] = useState(defaultPredictRes);

  const location = useLocation();
  let navigate = useNavigate();

  const client = axios.create({
    baseURL: "http://localhost:8000",
  });

  // eslint-disable-next-line react-hooks/exhaustive-deps
  const predictImage = async (predictStep) => {
    try {
      if (predictRes.res1?.img_id === -1)
        setPredictRes((curRes) => ({
          ...curRes,
          taskNum: -1,
        }));

      // first response get bounding box
      if (predictStep === 0) {
        const apiRes1 = await client.post(
          `/get-bounding-box/${location.state.id}`
        );
        console.log("res1", apiRes1);
        if (apiRes1.data)
          setPredictRes((curRes) => ({
            ...curRes,
            res1: apiRes1.data,
            taskNum: 1,
          }));
      }

      // crop the image from bounding box
      if (predictStep === 1 && predictRes.res1?.img_id) {
        const apiRes2 = await client.post(
          `/get-cropped-img/${predictRes.res1.img_id}`
        );
        console.log("res2", apiRes2);
        if (apiRes2)
          setPredictRes((curRes) => ({
            ...curRes,
            res2: apiRes2.data,
            taskNum: 2,
          }));
      }

      // create super-resoultion img
      if (predictStep === 2 && predictRes.res2?.historyId) {
        const apiRes3 = await client.post(
          `/super-img/${predictRes.res2.historyId}`
        );
        console.log("res3", apiRes3);
        if (apiRes3)
          setPredictRes((curRes) => ({
            ...curRes,
            res3: apiRes3.data,
            taskNum: 3,
          }));
      }

      // extract character ocr
      if (predictStep === 3 && predictRes.res3?.historyId) {
        const apiRes4 = await client.post(
          `/easy-ocr/${predictRes.res3.historyId}`
        );
        console.log("res4", apiRes4);
        if (apiRes4)
          setPredictRes((curRes) => ({
            ...curRes,
            res4: apiRes4.data,
            taskNum: 4,
          }));
      }

      // wrap all
      if (predictStep === 4 && predictRes.res4?.historyId) {
        const apiRes5 = await client.post(
          `/get-history/${predictRes.res4.historyId}`
        );
        console.log("res5", apiRes5);
        if (apiRes5)
          setPredictRes((curRes) => ({
            ...curRes,
            res5: apiRes5.data,
            taskNum: 5,
          }));
      }
      // navigate to result page
      if (predictStep === 5 && predictRes?.res5) {
        navigate("/hasil", { state: predictRes.res5 });
      }
    } catch (error) {
      console.error(error);
      setPredictRes({ ...defaultPredictRes, taskNum: -99 });
    }
  };

  // first render + first initiate, componentDidMount()
  useEffect(() => {
    setPredictRes((curRes) => ({ ...curRes, taskNum: 0 }));
  }, []);

  // next stepper
  useEffect(() => {
    console.log("step", predictRes);
    predictImage(predictRes.taskNum);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [predictRes.taskNum]);

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
        <span className='mt-1 text-center font-medium text-gray-500'>
          {predictRes.taskNum === -99 ? 0 : predictRes.taskNum + 1}
          /5 Task
          <br /> {getDescription(predictRes.taskNum)}
        </span>
        {predictRes.taskNum === -99 && (
          <Link
            to='/'
            className='inline-flex items-center mt-16 mb-8 py-2 px-3 text-sm font-medium text-center text-white bg-blue-500 rounded-lg hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300'
          >
            Kembali
            <svg
              xmlns='http://www.w3.org/2000/svg'
              fill='none'
              viewBox='0 0 24 24'
              strokeWidth={3}
              stroke='currentColor'
              className='ml-1 w-4 h-4'
            >
              <path
                strokeLinecap='round'
                strokeLinejoin='round'
                d='M9 15L3 9m0 0l6-6M3 9h12a6 6 0 010 12h-3'
              />
            </svg>
          </Link>
        )}
      </div>
    </div>
  );
}

export default Loading;
