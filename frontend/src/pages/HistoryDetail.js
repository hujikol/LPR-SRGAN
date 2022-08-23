import React, { useEffect } from "react";
import { useParams } from "react-router";

function HistoryDetail() {
  const yoloConfidence = 40;
  const preSrChar = "abcd";
  const postSrChar = "abcdefg";
  const preFileSize = 123;
  const postFileSize = 4567;

  let { postSlug } = useParams();

  useEffect(() => {}, [postSlug]);

  return (
    <div className='container mx-auto mt-2'>
      <div className='flex flex-col items-center'>
        <div>
          <h1 className='text-xl font-bold text-center'>
            Detail Pengenalan Ke - {postSlug}
          </h1>
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
              <div className='max-h-52 overflow-hidden'>
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

export default HistoryDetail;
