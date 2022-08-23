// This file will show last 10 recognition and benchmark them
// based on file name (ground truth recognition) with OCR result

import React, { useEffect } from "react";
import { useParams } from "react-router";
import { Link } from "react-router-dom";

function Result() {
  const yoloConfidence = 40;
  const preSrChar = "abcd";
  const postSrChar = "abcdefg";
  const preFileSize = 123;
  const postFileSize = 4567;

  let { postSlug } = useParams();

  useEffect(() => {}, [postSlug]);

  return (
    <div className='container mx-auto mt-2 mb-32'>
      <div className='flex flex-col items-center'>
        <div>
          <Link
            to='/'
            className='inline-flex items-center mt-16 mb-8 py-2 px-3 text-sm font-medium text-center text-white bg-blue-500 rounded-lg hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300'
          >
            Coba Lagi
            <svg
              className='my-auto ml-2 -mr-1 w-5 h-5'
              fill='currentColor'
              viewBox='0 0 20 20'
              xmlns='http://www.w3.org/2000/svg'
            >
              <path
                fill-rule='evenodd'
                d='M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z'
                clip-rule='evenodd'
              ></path>
            </svg>
          </Link>
        </div>
        <div>
          <h2 className='text-2xl text-center font-bold'>
            Hasil Lokalisasi YOLOv4
          </h2>
        </div>
        {/* Main Image Start*/}
        <div className='max-w-2xl mx-auto mt-2 rounded-lg border'>
          <img
            className='rounded-t-lg'
            src={require("./../testAssets/3abf17e4fd8417d7.png")}
            alt=''
          />
        </div>
        {/* Main Image End*/}
        <div className='mt-2'>
          <span className='text-center'>
            Average Confidence YOLOv4: <b>{yoloConfidence}%</b>
          </span>
        </div>
        {/* Result */}
        <div className='flex flex-row justify-between mx-auto mt-12'>
          <div>
            {/*Cropped Card Start */}
            <div className='max-w-xs mr-12 bg-white rounded-lg border border-gray-200 shadow-md'>
              <div className='max-h-42 overflow-hidden'>
                <img
                  className='rounded-t-lg'
                  // change Image here
                  src={require("./../testAssets/3abf17e4fd8417d7.png")}
                  alt=''
                />
              </div>

              <div className='p-5'>
                <h3 className='mb-2 text-xl font-bold tracking-tight text-gray-700'>
                  Hasil <em>Cropping</em> Plat Nomor
                </h3>
                <p className='mb-3 text-gray-700'>
                  <b>Karakter Terdeteksi</b>
                  <br />
                  {preSrChar}
                </p>
                <p className='mb-3 text-gray-700'>
                  <b>Ukuran File</b>
                  <br />
                  {preFileSize} Byte
                </p>
              </div>
            </div>
            {/* Cropped Ends */}
          </div>
          <div>
            {/*SRGAN Card Start */}
            <div className='max-w-xs bg-white rounded-lg border border-gray-200 shadow-md'>
              <div className='max-h-42 overflow-hidden'>
                <img
                  className='rounded-t-lg'
                  // change Image here
                  src={require("./../testAssets/3abf17e4fd8417d7.png")}
                  alt=''
                />
              </div>

              <div className='p-5'>
                <h3 className='mb-2 text-xl font-bold tracking-tight text-gray-700'>
                  Hasil <em>Super-Resolution</em>
                </h3>

                <p className='mb-3 text-gray-700'>
                  <b>Karakter Terdeteksi</b>
                  <br />
                  {postSrChar}
                </p>
                <p className='mb-3 text-gray-700'>
                  <b>Ukuran File</b>
                  <br />
                  {postFileSize} Byte
                </p>
              </div>
            </div>
            {/* SRGAN Ends */}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Result;
