import React from "react";
import { Link, useLocation } from "react-router-dom";

function Result() {
  const location = useLocation();
  console.log(location);
  const jsonResponse = location.state;
  console.log(jsonResponse);

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

        <div className='max-w-2xl mx-auto mt-2 rounded-md'>
          <img
            className='rounded-t-lg'
            src={`data:image/jpg;charset=utf-8;base64,${jsonResponse.yolo_img_byte}`}
            alt=''
          />
        </div>
        <div className='mt-2'>
          <span className='text-center'>
            Average YOLOv4 Confidence:{" "}
            <b>
              {parseFloat(
                JSON.stringify(jsonResponse.yolo_confidence) * 100
              ).toFixed(2)}
              %
            </b>
          </span>
        </div>
        {jsonResponse.cns_data.map((resultCns) => {
          return (
            <div className='flex flex-row justify-between mx-auto mt-12'>
              <div>
                {/*Cropped Card Start */}
                <div className='max-w-xs mr-12 bg-white rounded-lg border border-gray-200 shadow-md'>
                  <div className='max-h-42 overflow-hidden'>
                    <img
                      className='object-contain h-42 w-full rounded-t-lg'
                      // change Image here
                      src={`data:image/jpeg;base64,${resultCns.crop_img_byte}`}
                      alt=''
                    />
                  </div>
                  <div className='p-5'>
                    <h3 className='mb-2 text-xl font-bold tracking-tight text-gray-700'>
                      Hasil <em>Cropping</em> Plat Nomor
                    </h3>
                    <p className='mb-3 text-gray-700'>
                      <b>Karakter Terdeteksi Tanpa Otsu's</b>
                      <br />
                      {resultCns.crop_wo_text}
                    </p>
                    <p className='mb-3 text-gray-700'>
                      <b>Karakter Terdeteksi dg Otsu's</b>
                      <br />
                      {resultCns.crop_text}
                    </p>
                    <p className='mb-3 text-gray-700'>
                      <b>Ukuran File</b>
                      <br />
                      {parseFloat(resultCns.crop_img_size).toFixed(2)} KB
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
                      className=' w-full rounded-t-lg'
                      // change Image here
                      src={`data:image/jpeg;base64,${resultCns.super_img_byte}`}
                      alt=''
                    />
                  </div>

                  <div className='p-5'>
                    <h3 className='mb-2 text-xl font-bold tracking-tight text-gray-700'>
                      Hasil <em>Super-Resolution</em>
                    </h3>

                    <p className='mb-3 text-gray-700'>
                      <b>Karakter Terdeteksi Tanpa Otsu's</b>
                      <br />
                      {resultCns.super_wo_text}
                    </p>
                    <p className='mb-3 text-gray-700'>
                      <b>Karakter Terdeteksi dg Otsu's</b>
                      <br />
                      {resultCns.super_text}
                    </p>
                    <p className='mb-3 text-gray-700'>
                      <b>Ukuran File</b>
                      <br />
                      {parseFloat(resultCns.super_img_size).toFixed(2)} KB
                    </p>
                  </div>
                </div>
                {/* SRGAN Ends */}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Result;
