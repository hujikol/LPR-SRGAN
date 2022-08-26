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
    <div className='container mx-auto mt-2 mb-24'>
      <div className='flex flex-col items-center'>
        <div>
          <Link
            to='/'
            className='inline-flex items-center mt-16 mb-8 py-2 px-3 text-sm font-medium text-center text-white bg-blue-500 rounded-lg hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300'
          >
            Coba Lagi
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
        </div>
        <div>
          <h2 className='text-2xl text-center font-bold'>
            Hasil Lokalisasi YOLOv4
          </h2>
        </div>
        {/* Main Image Start*/}
        <div className='max-w-2xl mx-auto mt-2 rounded-md'>
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
